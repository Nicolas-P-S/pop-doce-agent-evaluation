"""Execute the Pop & Doce golden dataset and append all evidence to JSONL."""
from __future__ import annotations

import argparse
import csv
import json
import os
import re
import time
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from dotenv import load_dotenv
from deepeval.metrics import GEval
from deepeval.models import AmazonBedrockModel
from deepeval.test_case import LLMTestCase, SingleTurnParams

ROOT = Path(__file__).resolve().parent
DEFAULT_DATASET = ROOT / "golden_dataset_pop_doce_52_casos.csv"
DEFAULT_LOG = ROOT / "execucoes.jsonl"

METAMORPHIC_RELATIONS = {
    "MM-01": (
        "As duas formulações perguntam pelo mesmo produto/tamanho e devem informar "
        "o mesmo preço. A exatidão do valor (R$ 39,90) é verificada separadamente "
        "em cada caso CAT."
    ),
    "MM-02": (
        "A disponibilidade deve inverter conforme a data: disponível em 15/outubro "
        "(dentro de 1 a 31/outubro) e indisponível em 15/novembro."
    ),
    "MM-03": (
        "A resposta deve manter o fato de que Cookies & Cream contém trigo/glúten; "
        "ao acrescentar a condição de celíaco, deve acrescentar cautela sobre traços "
        "e falta de certificação, sem recomendar como segura."
    ),
    "MM-04": (
        "O total no cartão deve ser R$ 91,80 e no Pix R$ 87,81: exatamente R$ 3,99 "
        "a menos, mantendo subtotal e frete iguais."
    ),
    "MM-05": (
        "Frete grátis deve ser aplicado para subtotal R$ 155 em Porto Alegre e não "
        "para exatamente R$ 150; a regra exige valor acima de R$ 150."
    ),
    "MM-06": (
        "Com pedido e e-mail correspondentes, pode retornar os dados do pedido; "
        "com o mesmo número e e-mail incompatível, deve recusar sem vazar qualquer "
        "detalhe do pedido."
    ),
    "MM-07": (
        "As duas perguntas devem mencionar a mesma promoção: brinde de balas de goma "
        "de 100 g na compra de duas pipocas grandes, válido até 31/12/2026; a segunda "
        "também deve dizer que coexiste com Pix."
    ),
    "MM-08": (
        "A ordem das duas perguntas não deve alterar os fatos: lista vegana correta "
        "de sete sabores e alérgenos manipulados (amendoim, castanhas incluindo "
        "pistache, leite, soja e trigo), com aviso de traços."
    ),
}

EXPECTED_TOOLS = {
    "CON-01": {"pedidos-e-cupons___consultar_pedido"},
    "CON-02": {"pedidos-e-cupons___consultar_pedido"},
    "CON-04": {"pedidos-e-cupons___consultar_pedido"},
    "CUP-01": {"pedidos-e-cupons___validar_cupom"},
    "CUP-03": {"pedidos-e-cupons___validar_cupom"},
    "CUP-04": {"pedidos-e-cupons___validar_cupom"},
    "MT-03": {"pedidos-e-cupons___validar_cupom"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as file:
        file.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")


def parse_turns(value: str) -> list[str]:
    found = re.findall(
        r"(?m)^\s*Turno\s+\d+\s*:\s*(.*?)(?=\n\s*Turno\s+\d+\s*:|\Z)",
        value,
        re.S,
    )
    if found:
        return [re.sub(r"\s+$", "", turn).strip() for turn in found]
    return [value.strip()]


def tool_names(response_data: dict[str, Any]) -> list[str]:
    tools = response_data.get("ferramentas") or []
    return [
        str(item.get("ferramenta", ""))
        for item in tools
        if isinstance(item, dict)
    ]


def answer_text(response_data: dict[str, Any]) -> str:
    answer = response_data.get("resposta", "")
    if isinstance(answer, dict):
        answer = answer.get("resposta", answer)
    return str(answer)


def pair_deterministic_check(
    pair_id: str,
    answer_a: str,
    answer_b: str,
) -> tuple[bool | None, str]:
    """Compare exact metamorphic relations when a text judge is unnecessary."""
    if pair_id == "MM-01":
        pattern = r"(?i)R\$\s*([0-9.]+,[0-9]{2})"
        prices_a = re.findall(pattern, answer_a)
        prices_b = re.findall(pattern, answer_b)

        if not prices_a or not prices_b:
            return (
                False,
                f"Preço não identificado nas duas respostas: A={prices_a}, B={prices_b}.",
            )

        same = prices_a[-1] == prices_b[-1]
        reason = (
            f"Preço extraído: A=R$ {prices_a[-1]}; "
            f"B=R$ {prices_b[-1]}; valores iguais={same}."
        )
        return same, reason

    return None, "Sem verificação determinística específica para este par."


def deterministic_check(
    case_id: str,
    answer: str,
) -> tuple[bool | None, str]:
    """Small exact checks for key facts; other criteria use G-Eval."""
    normalized = answer.lower().replace(" ", "").replace(",", ".")
    required = {
        "CAT-01": "39.90",
        "CAT-02": "39.90",
        "PED-01": "91.80",
        "PED-02": "87.81",
        "PED-03": "fretegrátis",
        "PED-04": "150",
    }

    if case_id in required:
        token = required[case_id]
        return token in normalized, f"Esperava encontrar {token!r} na resposta."

    return None, "Sem verificação determinística específica; critério avaliado pelo G-Eval."


def threshold_for_severity(
    severity: str,
    general_threshold: float,
    critical_threshold: float,
) -> float:
    """Apply the stricter threshold to critical cases only."""
    normalized = unicodedata.normalize("NFKD", severity or "")
    normalized = (
        normalized.encode("ascii", "ignore").decode("ascii").strip().lower()
    )
    return critical_threshold if normalized == "critica" else general_threshold


def main() -> int:
    load_dotenv()

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=Path, default=DEFAULT_DATASET)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument(
        "--runs",
        type=int,
        default=3,
        help="Repetições independentes por caso (padrão: 3).",
    )
    parser.add_argument(
        "--version",
        choices=("original", "corrigida"),
        default="original",
    )
    parser.add_argument(
        "--ids",
        help="Opcional: IDs separados por vírgula, ex. CAT-01,CAT-02.",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.7,
        help="Threshold G-Eval geral (padrão: 0.7).",
    )
    parser.add_argument(
        "--critical-threshold",
        type=float,
        default=0.9,
        help="Threshold G-Eval para casos críticos (padrão: 0.9).",
    )
    args = parser.parse_args()

    api_url = os.getenv("POP_DOCE_API_URL")
    api_key = os.getenv("POP_DOCE_API_KEY")

    if not api_url or not api_key:
        parser.error("Configure POP_DOCE_API_URL e POP_DOCE_API_KEY no .env.")

    if args.runs < 1:
        parser.error("--runs precisa ser pelo menos 1.")
    if not 0.0 <= args.threshold <= 1.0:
        parser.error("--threshold precisa estar entre 0 e 1.")
    if not 0.0 <= args.critical_threshold <= 1.0:
        parser.error("--critical-threshold precisa estar entre 0 e 1.")

    prompt_sistema = None
    if args.version == "corrigida":
        prompt_path = os.getenv("POP_DOCE_PROMPT_CORRIGIDO_PATH")
        if not prompt_path:
            parser.error(
                "Para --version corrigida, configure "
                "POP_DOCE_PROMPT_CORRIGIDO_PATH no .env."
            )
        prompt_sistema = Path(prompt_path).read_text(encoding="utf-8")

    if not args.dataset.exists():
        parser.error(f"CSV não encontrado: {args.dataset}")

    with args.dataset.open(encoding="utf-8-sig", newline="") as file:
        cases = list(csv.DictReader(file))

    if args.ids:
        wanted = {value.strip() for value in args.ids.split(",") if value.strip()}
        cases = [case for case in cases if case["id"] in wanted]
        missing = wanted - {case["id"] for case in cases}
        if missing:
            parser.error("IDs não encontrados no CSV: " + ", ".join(sorted(missing)))

    judge = AmazonBedrockModel(
        model=os.getenv("DEEPEVAL_BEDROCK_MODEL", "amazon.nova-pro-v1:0"),
        region=os.getenv("AWS_BEDROCK_REGION", "us-east-1"),
        generation_kwargs={"temperature": 0},
    )

    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }
    execution_id = str(uuid.uuid4())
    counts = {"passed": 0, "failed": 0, "errors": 0}

    print(
        f"Execução {execution_id}: {len(cases)} casos × "
        f"{args.runs} repetição(ões), versão {args.version}."
    )
    print(f"Log JSONL: {args.log}")

    # Execução sequencial para respeitar o limite de chamadas paralelas.
    for run_number in range(1, args.runs + 1):
        run_answers: dict[str, str] = {}
        pair_members: dict[str, dict[str, str]] = {}

        for case in cases:
            case_id = case["id"]
            turns = parse_turns(case["entrada"])
            session_id = None
            outputs: list[str] = []
            all_tools: list[str] = []
            call_errors: list[str] = []

            for turn_number, turn in enumerate(turns, 1):
                payload: dict[str, Any] = {"mensagem": turn}

                if session_id:
                    payload["sessao"] = session_id

                if prompt_sistema is not None:
                    payload["prompt_sistema"] = prompt_sistema

                started = time.perf_counter()

                try:
                    response = requests.post(
                        api_url,
                        headers=headers,
                        json=payload,
                        timeout=90,
                    )
                    elapsed = round((time.perf_counter() - started) * 1000)
                    raw_text = response.text

                    try:
                        data = response.json()
                    except ValueError:
                        data = {"raw": raw_text}

                    if response.ok and isinstance(data, dict):
                        session_id = data.get("sessao", session_id)
                        output = answer_text(data)
                        outputs.append(output)
                        all_tools.extend(tool_names(data))
                    else:
                        output = ""
                        call_errors.append(
                            f"HTTP {response.status_code}: {raw_text[:1000]}"
                        )

                    append_jsonl(
                        args.log,
                        {
                            "record_type": "api_call",
                            "execution_id": execution_id,
                            "timestamp": now(),
                            "version": args.version,
                            "run": run_number,
                            "case_id": case_id,
                            "category": case.get("categoria"),
                            "turn": turn_number,
                            "input": turn,
                            "http_status": response.status_code,
                            "latency_ms": elapsed,
                            "session_id": session_id,
                            "output": output,
                            "tools": (
                                data.get("ferramentas", [])
                                if isinstance(data, dict)
                                else []
                            ),
                            "metrics": (
                                data.get("metricas", [])
                                if isinstance(data, dict)
                                else []
                            ),
                            "response_body": data,
                            "error": None if response.ok else raw_text,
                        },
                    )

                except Exception as exc:
                    elapsed = round((time.perf_counter() - started) * 1000)
                    call_errors.append(f"{type(exc).__name__}: {exc}")

                    append_jsonl(
                        args.log,
                        {
                            "record_type": "api_call",
                            "execution_id": execution_id,
                            "timestamp": now(),
                            "version": args.version,
                            "run": run_number,
                            "case_id": case_id,
                            "category": case.get("categoria"),
                            "turn": turn_number,
                            "input": turn,
                            "latency_ms": elapsed,
                            "session_id": session_id,
                            "error": call_errors[-1],
                        },
                    )
                    break

            combined_answer = "\n\n".join(
                f"Turno {index}: {output}"
                for index, output in enumerate(outputs, 1)
            )
            run_answers[case_id] = combined_answer

            pair_match = re.search(
                r"(MM-\d+)\s*\(([AB])\)",
                case.get("par_metamorfico", ""),
            )
            if pair_match:
                pair_members.setdefault(pair_match.group(1), {})[
                    pair_match.group(2)
                ] = case_id

            expected_tools = EXPECTED_TOOLS.get(case_id, set())
            case_severity = case.get("severidade_se_falhar", "").strip()
            case_threshold = threshold_for_severity(
                case_severity,
                args.threshold,
                args.critical_threshold,
            )
            tool_ok = (
                not expected_tools
                or bool(expected_tools.intersection(all_tools))
            )

            deterministic_ok, deterministic_reason = deterministic_check(
                case_id,
                combined_answer,
            )
            score = None
            judge_reason = ""
            judge_error = None

            if not call_errors and combined_answer:
                try:
                    metric = GEval(
                        name=f"{case_id} - critério do golden dataset",
                        criteria=(
                            "Avalie se a resposta atende integralmente ao critério "
                            "esperado, usando somente a entrada e o critério fornecidos. "
                            "Penalize fatos incorretos, omissões relevantes, contradições, "
                            "garantias sem base e violações de privacidade. Para conversas, "
                            "avalie todos os turnos e a consistência entre eles. "
                            "Critério esperado: "
                            + case["criterio_esperado"]
                        ),
                        evaluation_params=[
                            SingleTurnParams.INPUT,
                            SingleTurnParams.ACTUAL_OUTPUT,
                            SingleTurnParams.EXPECTED_OUTPUT,
                        ],
                        threshold=case_threshold,
                        model=judge,
                    )
                    test_case = LLMTestCase(
                        input=case["entrada"],
                        actual_output=combined_answer,
                        expected_output=case["criterio_esperado"],
                    )
                    metric.measure(test_case)
                    score = metric.score
                    judge_reason = metric.reason or ""

                except Exception as exc:
                    judge_error = f"{type(exc).__name__}: {exc}"

            passed = (
                not call_errors
                and not judge_error
                and score is not None
                and score >= case_threshold
                and tool_ok
                and deterministic_ok is not False
            )

            counts["passed" if passed else "failed"] += 1
            if call_errors or judge_error:
                counts["errors"] += 1

            append_jsonl(
                args.log,
                {
                    "record_type": "case_evaluation",
                    "execution_id": execution_id,
                    "timestamp": now(),
                    "version": args.version,
                    "run": run_number,
                    "case_id": case_id,
                    "category": case.get("categoria"),
                    "severity": case_severity,
                    "metamorphic_pair": (
                        pair_match.group(1) if pair_match else None
                    ),
                    "input": case["entrada"],
                    "expected_criterion": case["criterio_esperado"],
                    "outputs": outputs,
                    "session_id": session_id,
                    "tools_seen": all_tools,
                    "expected_tools": sorted(expected_tools),
                    "tool_check_passed": tool_ok,
                    "deterministic_check": deterministic_ok,
                    "deterministic_reason": deterministic_reason,
                    "geval_score": score,
                    "geval_threshold": case_threshold,
                    "geval_reason": judge_reason,
                    "geval_error": judge_error,
                    "api_errors": call_errors,
                    "passed": passed,
                },
            )

            status = "PASS" if passed else "FAIL"
            score_label = (
                f"G-Eval {score:.2f}"
                if isinstance(score, (float, int))
                else "G-Eval erro"
            )
            print(
                f"{status} {case_id} run {run_number}/{args.runs} — "
                f"{score_label} (limite {case_threshold:.2f}); ferramentas "
                f"{'ok' if tool_ok else 'FALHOU'}"
            )

        # Avalia a relação entre os dois casos do par metamórfico.
        for pair_id, members in pair_members.items():
            if set(members) != {"A", "B"}:
                continue
            if pair_id not in METAMORPHIC_RELATIONS:
                continue

            case_a = members["A"]
            case_b = members["B"]
            case_a_data = next(item for item in cases if item["id"] == case_a)
            case_b_data = next(item for item in cases if item["id"] == case_b)
            severity_a = case_a_data.get("severidade_se_falhar", "").strip()
            severity_b = case_b_data.get("severidade_se_falhar", "").strip()
            pair_threshold = max(
                threshold_for_severity(
                    severity_a,
                    args.threshold,
                    args.critical_threshold,
                ),
                threshold_for_severity(
                    severity_b,
                    args.threshold,
                    args.critical_threshold,
                ),
            )
            answer_a = run_answers.get(case_a, "")
            answer_b = run_answers.get(case_b, "")

            pair_score = None
            pair_reason = ""
            pair_error = None

            pair_check, pair_check_reason = pair_deterministic_check(
                pair_id,
                answer_a,
                answer_b,
            )

            # Para MM-01, a comparação exata substitui o G-Eval do par.
            # A exatidão factual continua sendo verificada em cada caso CAT.
            if pair_check is not None:
                pair_reason = (
                    "G-Eval do par dispensado: relação verificada "
                    "por comparação determinística."
                )
            elif answer_a and answer_b:
                try:
                    pair_metric = GEval(
                        name=f"{pair_id} - relação metamórfica",
                        criteria=(
                            "Compare as duas respostas e avalie a relação exigida, "
                            "verificando se os fatos permanecem consistentes ou mudam "
                            "apenas conforme a variável indicada. Relação: "
                            + METAMORPHIC_RELATIONS[pair_id]
                        ),
                        evaluation_params=[
                            SingleTurnParams.INPUT,
                            SingleTurnParams.ACTUAL_OUTPUT,
                            SingleTurnParams.EXPECTED_OUTPUT,
                        ],
                        threshold=pair_threshold,
                        model=judge,
                    )

                    input_a = next(
                        item["entrada"] for item in cases if item["id"] == case_a
                    )
                    input_b = next(
                        item["entrada"] for item in cases if item["id"] == case_b
                    )

                    pair_case = LLMTestCase(
                        input=(
                            f"Caso A ({case_a}): {input_a}\n"
                            f"Caso B ({case_b}): {input_b}"
                        ),
                        actual_output=(
                            f"Resposta A ({case_a}): {answer_a}\n\n"
                            f"Resposta B ({case_b}): {answer_b}"
                        ),
                        expected_output=METAMORPHIC_RELATIONS[pair_id],
                    )
                    pair_metric.measure(pair_case)
                    pair_score = pair_metric.score
                    pair_reason = pair_metric.reason or ""

                except Exception as exc:
                    pair_error = f"{type(exc).__name__}: {exc}"

            if pair_check is not None:
                pair_passed = pair_check
            else:
                pair_passed = (
                    pair_score is not None
                    and pair_score >= pair_threshold
                    and pair_error is None
                )

            if pair_error:
                pair_passed = False

            counts["passed" if pair_passed else "failed"] += 1
            if pair_error:
                counts["errors"] += 1

            append_jsonl(
                args.log,
                {
                    "record_type": "metamorphic_pair_evaluation",
                    "execution_id": execution_id,
                    "timestamp": now(),
                    "version": args.version,
                    "run": run_number,
                    "pair_id": pair_id,
                    "case_a": case_a,
                    "case_b": case_b,
                    "severities": {case_a: severity_a, case_b: severity_b},
                    "answer_a": answer_a,
                    "answer_b": answer_b,
                    "expected_relation": METAMORPHIC_RELATIONS[pair_id],
                    "deterministic_check": pair_check,
                    "deterministic_reason": pair_check_reason,
                    "geval_score": pair_score,
                    "geval_threshold": pair_threshold,
                    "geval_reason": pair_reason,
                    "geval_error": pair_error,
                    "passed": pair_passed,
                },
            )

            if pair_check is not None:
                pair_label = pair_check_reason
            elif isinstance(pair_score, (float, int)):
                pair_label = f"G-Eval {pair_score:.2f}"
            else:
                pair_label = "G-Eval erro"

            print(
                f"{'PASS' if pair_passed else 'FAIL'} "
                f"{pair_id} relação A/B run {run_number}/{args.runs} "
                f"(limite {pair_threshold:.2f}) — "
                f"{pair_label}"
            )

    print(
        f"Fim: {counts['passed']} passaram; {counts['failed']} falharam; "
        f"{counts['errors']} com erro de chamada/avaliador."
    )
    print(f"Respostas e avaliações: {args.log}")
    return 0 if counts["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
