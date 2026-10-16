#!/usr/bin/env node
/**
 * Gate Go/No-Go + tokens/latencia a partir do JSON do promptfoo.
 *
 *   npx promptfoo eval -c promptfooconfig.yaml --no-cache -o resultados/resultado.json
 *   node scripts/gate.js resultados/resultado.json [--geral 0.8] [--critico 1.0] [--pares 0.8]
 *                        [--versao-gate corrigida] [--saida resultados]
 *
 * Regras (taxa de aprovacao = execucoes aprovadas / execucoes, contando as repeticoes):
 *   - geral:   taxa de todos os casos >= --geral   (padrao 0.8)
 *   - critico: taxa dos casos de severidade Critica >= --critico (padrao 1.0, ou seja, nenhuma falha)
 *   - pares:   para cada par metamorfico, a MENOR taxa entre os dois casos >= --pares (aproximacao)
 * Erros de API/provider contam como reprovacao.
 * Codigo de saida 1 se a versao avaliada (--versao-gate) ficar NO-GO.
 */
const fs = require("fs");
const path = require("path");

const args = process.argv.slice(2);
const arquivo = args[0];
const opt = (n, d) => { const i = args.indexOf("--" + n); return i >= 0 ? args[i + 1] : d; };
if (!arquivo || arquivo.startsWith("--")) {
  console.error("Uso: node scripts/gate.js resultados/resultado.json [--geral 0.8] [--critico 1.0]");
  process.exit(2);
}
const LIM_GERAL = parseFloat(opt("geral", "0.8"));
const LIM_CRIT = parseFloat(opt("critico", "1.0"));
const LIM_PARES = parseFloat(opt("pares", String(LIM_GERAL)));
const SAIDA = opt("saida", path.dirname(arquivo));

const norm = (s) => String(s || "").normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
const soma = (a) => a.reduce((x, y) => x + y, 0);
const media = (a) => (a.length ? soma(a) / a.length : 0);
const mediana = (a) => { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); const m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
const p95 = (a) => { if (!a.length) return 0; const s = [...a].sort((x, y) => x - y); return s[Math.min(s.length - 1, Math.round(0.95 * (s.length - 1)))]; };
const pct = (x) => (x * 100).toFixed(1) + "%";
const f0 = (x) => Math.round(x).toLocaleString("pt-BR");

// ---------- leitura ----------
const dados = JSON.parse(fs.readFileSync(arquivo, "utf8"));
const linhas = Array.isArray(dados.results) ? dados.results : (dados.results && dados.results.results) || [];
if (!linhas.length) {
  console.error("Nenhum resultado encontrado no JSON. Chaves de topo:", Object.keys(dados));
  process.exit(2);
}

function lerSaida(row) {
  const o = row.response && row.response.output;
  if (typeof o === "string") { try { return JSON.parse(o); } catch { return null; } }
  return o && typeof o === "object" ? o : null;
}

const recs = linhas.map((row) => {
  const vars = (row.testCase && row.testCase.vars) || row.vars || {};
  const prov = row.provider;
  const versao = typeof prov === "string" ? prov : (prov && (prov.label || prov.id)) || "?";
  const saida = lerSaida(row);
  const meta = (saida && saida.metadados) || (row.response && row.response.metadata) || {};
  const tu = (row.response && row.response.tokenUsage) || {};
  const tin = meta.tokens_entrada ?? tu.prompt ?? 0;
  const tout = meta.tokens_saida ?? tu.completion ?? 0;
  const erro = Boolean(row.error) || row.failureReason === 2 || (meta.erros || 0) > 0;
  return {
    versao, id: vars.case_id || "?", categoria: vars.categoria || "", severidade: vars.severidade || "",
    par: (String(vars.par_metamorfico || "").match(/MM-\d+/) || [""])[0],
    ok: row.success === true && !erro, erro,
    tin, tout, ttot: meta.tokens_total ?? (tin + tout),
    lat: meta.latencia_total_ms ?? row.latencyMs ?? 0
  };
});
const versoes = [...new Set(recs.map((r) => r.versao))];
const ehCritico = (r) => norm(r.severidade) === "critica";

// ---------- calculos ----------
const taxa = (rs) => (rs.length ? rs.filter((r) => r.ok).length / rs.length : 0);
function porCaso(rs) {
  const m = new Map();
  for (const r of rs) { if (!m.has(r.id)) m.set(r.id, { id: r.id, sev: r.severidade, par: r.par, rs: [] }); m.get(r.id).rs.push(r); }
  return m;
}
function avaliar(v) {
  const rs = recs.filter((r) => r.versao === v);
  const casos = porCaso(rs);
  const crit = rs.filter(ehCritico);
  const pares = new Map();
  for (const c of casos.values()) if (c.par) { if (!pares.has(c.par)) pares.set(c.par, []); pares.get(c.par).push(c); }
  const paresRes = [...pares.entries()].filter(([, cs]) => cs.length === 2)
    .map(([p, cs]) => ({ par: p, casos: cs.map((c) => c.id).join("+"), taxa: Math.min(...cs.map((c) => taxa(c.rs))) }));
  const paresTaxa = paresRes.length ? media(paresRes.map((p) => p.taxa)) : 0;
  const criticosFalhos = [...casos.values()].filter((c) => norm(c.sev) === "critica" && taxa(c.rs) < 1)
    .map((c) => `${c.id} (${c.rs.filter((r) => r.ok).length}/${c.rs.length})`);
  const g = { v, rs, casos, n: rs.length, taxaGeral: taxa(rs), taxaCrit: crit.length ? taxa(crit) : 1,
    nCrit: crit.length, erros: rs.filter((r) => r.erro).length, paresRes, criticosFalhos };
  g.paresOk = paresRes.filter((p) => p.taxa >= LIM_PARES).length;
  g.go = g.taxaGeral >= LIM_GERAL && g.taxaCrit >= LIM_CRIT && paresRes.every((p) => p.taxa >= LIM_PARES);
  return g;
}
const res = versoes.map(avaliar);

// ---------- relatorio ----------
const md = [];
md.push(`# Gate Go/No-Go e consumo — Lia (Pop & Doce)\n`);
md.push(`Thresholds: geral >= ${LIM_GERAL} · críticos >= ${LIM_CRIT} · pares metamórficos >= ${LIM_PARES}. Erros de API contam como reprovação.\n`);
md.push(`## Taxa de aprovação por versão\n`);
md.push(`| versão | execuções | aprovadas | taxa geral | críticos aprovados | pares MM ok | erros | veredito |\n|---|---|---|---|---|---|---|---|`);
for (const g of res) {
  const critOk = g.rs.filter((r) => ehCritico(r) && r.ok).length;
  md.push(`| ${g.v} | ${g.n} | ${g.rs.filter((r) => r.ok).length} | ${pct(g.taxaGeral)} ${g.taxaGeral >= LIM_GERAL ? "✅" : "❌"} | ${critOk}/${g.nCrit} (${pct(g.taxaCrit)}) ${g.taxaCrit >= LIM_CRIT ? "✅" : "❌"} | ${g.paresOk}/${g.paresRes.length} | ${g.erros} | **${g.go ? "GO" : "NO-GO"}** |`);
}
md.push(`\n## Casos críticos reprovados\n`);
for (const g of res) md.push(`- **${g.v}:** ${g.criticosFalhos.length ? g.criticosFalhos.join(", ") : "nenhum"}`);

md.push(`\n## Por categoria\n`);
const cats = [...new Set(recs.map((r) => r.categoria))];
md.push(`| categoria | ${versoes.join(" | ")} |\n|---|${versoes.map(() => "---").join("|")}|`);
for (const c of cats) md.push(`| ${c} | ${res.map((g) => pct(taxa(g.rs.filter((r) => r.categoria === c)))).join(" | ")} |`);

md.push(`\n## Por caso (aprovações/repetições)\n`);
const ids = [...new Set(recs.map((r) => r.id))];
const sevDe = Object.fromEntries(recs.map((r) => [r.id, r.severidade]));
md.push(`| caso | severidade | ${versoes.join(" | ")} |${versoes.length === 2 ? " delta |" : ""}\n|---|---|${versoes.map(() => "---").join("|")}|${versoes.length === 2 ? "---|" : ""}`);
for (const id of ids) {
  const cel = res.map((g) => { const c = g.casos.get(id); return c ? `${c.rs.filter((r) => r.ok).length}/${c.rs.length}` : "-"; });
  let delta = "";
  if (versoes.length === 2) {
    const [a, b] = res.map((g) => { const c = g.casos.get(id); return c ? taxa(c.rs) : 0; });
    delta = ` ${b > a ? "melhorou" : b < a ? "PIOROU" : "="} |`;
  }
  md.push(`| ${id} | ${sevDe[id]} | ${cel.join(" | ")} |${delta}`);
}

md.push(`\n## Tokens (soma de todos os turnos de cada execução; entrada inclui cache quando informado)\n`);
md.push(`| versão | execuções | entrada (total) | saída (total) | total geral | média entrada | média saída | média total |\n|---|---|---|---|---|---|---|---|`);
for (const g of res) {
  const ti = g.rs.map((r) => r.tin), to = g.rs.map((r) => r.tout), tt = g.rs.map((r) => r.ttot);
  md.push(`| ${g.v} | ${g.n} | ${f0(soma(ti))} | ${f0(soma(to))} | ${f0(soma(tt))} | ${f0(media(ti))} | ${f0(media(to))} | ${f0(media(tt))} |`);
}
md.push(`\nO consumo do juiz (llm-rubric no Bedrock) é contabilizado à parte pelo promptfoo e não entra nesta tabela.\n`);
md.push(`## Latência (ms por caso, somando turnos)\n`);
md.push(`| versão | média | mediana | p95 | máxima |\n|---|---|---|---|---|`);
for (const g of res) { const l = g.rs.map((r) => r.lat); md.push(`| ${g.v} | ${f0(media(l))} | ${f0(mediana(l))} | ${f0(p95(l))} | ${f0(Math.max(0, ...l))} |`); }

md.push(`\n## Pares metamórficos (aproximação: menor taxa entre os dois casos)\n`);
md.push(`| par | casos | ${versoes.join(" | ")} |\n|---|---|${versoes.map(() => "---").join("|")}|`);
for (const p of res[0].paresRes) md.push(`| ${p.par} | ${p.casos} | ${res.map((g) => { const x = g.paresRes.find((q) => q.par === p.par); return x ? pct(x.taxa) : "-"; }).join(" | ")} |`);
md.push(`\n> Esta aproximação exige que os dois casos passem; a comparação direta entre as duas respostas do par (ex.: total Pix = total cartão − desconto) não é feita aqui.`);

fs.mkdirSync(SAIDA, { recursive: true });
fs.writeFileSync(path.join(SAIDA, "gate.md"), md.join("\n") + "\n", "utf8");

const csv = (cab, rows) => [cab.join(","), ...rows.map((r) => r.map((x) => `"${String(x).replace(/"/g, '""')}"`).join(","))].join("\n") + "\n";
fs.writeFileSync(path.join(SAIDA, "execucoes-resumo.csv"),
  csv(["versao", "caso", "severidade", "aprovado", "erro", "tokens_entrada", "tokens_saida", "tokens_total", "latencia_ms"],
    recs.map((r) => [r.versao, r.id, r.severidade, r.ok, r.erro, r.tin, r.tout, r.ttot, r.lat])), "utf8");
const linhasCaso = [];
for (const g of res) for (const c of g.casos.values()) {
  const ti = c.rs.map((r) => r.tin), to = c.rs.map((r) => r.tout);
  linhasCaso.push([g.v, c.id, c.sev, c.rs.length, soma(ti), soma(to), soma(ti) + soma(to), Math.round(media(ti)), Math.round(media(to)), Math.round(media(ti) + media(to))]);
}
fs.writeFileSync(path.join(SAIDA, "tokens-por-caso.csv"),
  csv(["versao", "caso", "severidade", "execucoes", "entrada_total", "saida_total", "total", "entrada_media", "saida_media", "total_media"], linhasCaso), "utf8");

// ---------- console ----------
console.log(md.slice(0, 1 + 3 + res.length + 1 + 1).join("\n"));
console.log(`\nArquivos: ${path.join(SAIDA, "gate.md")}, execucoes-resumo.csv, tokens-por-caso.csv`);
const alvo = opt("versao-gate", versoes.includes("corrigida") ? "corrigida" : versoes[0]);
const g = res.find((x) => x.v === alvo) || res[0];
console.log(`\nVEREDITO (${g.v}): ${g.go ? "GO" : "NO-GO"}`);
process.exit(g.go ? 0 : 1);
