# Promptfoo — Lia / Pop & Doce

Suíte de avaliação da Lia pela API, com golden dataset de **55 casos** (16 críticos), 8 pares metamórficos,
verificação do campo `ferramentas`, thresholds de aprovação, contagem de tokens e comparação original × corrigida.

## Arquivos

| Arquivo | Função |
|---|---|
| `golden_dataset_pop_doce.csv` | Fonte única dos casos (edite aqui). |
| `scripts/gerar_tests.py` | Gera `tests-lia.yaml` a partir do CSV (thresholds e ferramentas esperadas ficam no topo do script). |
| `tests-lia.yaml` | Gerado. Não edite à mão. |
| `promptfooconfig.yaml` | Providers `original` e `corrigida`, paralelismo 4, repetição 3, juiz. |
| `lia-provider.js` | Chama a API, multi-turno com `sessao`, soma tokens de `metricas`. |
| `asserts/ferramentas.js` | Verifica `ferramentas` em pedidos e cupons. |
| `scripts/gate.js` | Aplica os thresholds e gera tokens/latência. |
| `prompt_corrigido.txt` | **Você cria**: prompt de sistema da versão corrigida. |

## Executar (PowerShell)

```powershell
$env:LIA_API_KEY="SUA_CHAVE"          # nunca coloque a chave em arquivo ou no repositório
# credenciais AWS configuradas para o juiz (Bedrock, us-east-1)

python scripts\gerar_tests.py          # só se você alterou o CSV
npx promptfoo eval -c .\promptfooconfig.yaml --no-cache -o resultados\resultado.json
node scripts\gate.js resultados\resultado.json
npx promptfoo view
```

- Só a versão original (antes de existir o prompt corrigido): `--filter-providers original`
  (se sua versão do promptfoo não tiver a flag, comente o provider `corrigida` no config).
- Poucos casos para validar o ambiente: `--filter-pattern "^(PED-03|CON-01|CUP-04|ALE-01)" --repeat 1`.

## Thresholds

- **Por caso (promptfoo):** o `llm-rubric` de cada caso tem `threshold` **0.8**; casos de severidade **Crítica** têm **1.0**.
- **Por conjunto (`scripts/gate.js`):** taxa geral de aprovação **≥ 0.8** e taxa dos casos críticos **≥ 1.0**
  (nenhuma falha em nenhuma das repetições). Também exige pares metamórficos ≥ 0.8 (`--pares 0` desliga).
  Mude com `--geral`, `--critico` e `--pares`. Erros de API contam como reprovação.
- Código de saída 1 quando a versão avaliada fica NO-GO (padrão: `corrigida`, se existir; use `--versao-gate original` para a outra).

## Tokens e latência

O provider soma `metricas` de todos os turnos de cada execução (entrada inclui tokens de cache quando a API informa)
e devolve em `tokenUsage` (aparece no painel do promptfoo). `scripts/gate.js` gera em `resultados/`:

- `gate.md`: aprovação, tokens (entrada, saída, total, médias) e latência (média, mediana, p95) por versão.
- `tokens-por-caso.csv`: entrada, saída, total e médias por caso e versão.
- `execucoes-resumo.csv`: uma linha por execução.

O consumo do juiz é contabilizado à parte pelo promptfoo.

## Verificação de ferramentas

| Casos | Regra |
|---|---|
| CON-01, CON-02, CON-04, CON-06 | `consultar_pedido` deve ser chamada |
| CUP-01, CUP-03, CUP-04, MT-03 | `validar_cupom` deve ser chamada |
| CON-05 | `consultar_pedido` não pode ser chamada |

## Observações

1. O dataset ainda precisa ser conferido contra a base oficial (`material-turma.zip`): preços, glúten de Cookies & Cream,
   lista vegana, frete e promoções. Valores divergentes viram falso defeito da Lia.
2. Pares metamórficos: o `gate.md` usa uma aproximação (os dois casos precisam passar). A comparação direta entre as respostas do par não é automática.
3. O provider avisa erro se a API devolver `versao` diferente da pedida (prompt corrigido não aplicado).
4. Máximo de 4 chamadas em paralelo (regra do desafio) já está em `evaluateOptions`.
