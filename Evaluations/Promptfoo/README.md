# Promptfoo — Lia / Pop & Doce

Suíte de avaliação da assistente de vendas Lia pela API, com golden
dataset de **52 casos**, **15 casos críticos**, **8 pares metamórficos**
e **3 repetições por caso**. A suíte avalia catálogo, alérgenos,
pedidos, cupons, conversas multi-turno, escopo, testes adversariais e
uso de ferramentas.

> **Status: NO-GO.** A versão original ficou abaixo dos thresholds com
> os dois juízes. O Nova Lite apresentou 31,41% de aprovação e o Llama 4
> Scout, 21,15%; a meta geral é 80% e casos críticos exigem 100%.

## Arquivos

| Arquivo                                | Função                                                       |
|:---------------------------------------|:-------------------------------------------------------------|
| `golden_dataset_pop_doce_52_casos.csv` | Fonte única dos casos.                                       |
| `scripts/gerar_tests.py`               | Gera os testes a partir do CSV.                              |
| `tests-lia.yaml`                       | Suíte gerada; evite editar manualmente.                      |
| `promptfooconfig.yaml`                 | Providers, juiz, thresholds e parâmetros do Promptfoo.       |
| `lia-provider.js`                      | Chama a API, gerencia turnos/sessão e expõe tokens/latência. |
| `asserts/ferramentas.js`               | Verifica chamadas esperadas em pedidos e cupons.             |
| `scripts/gate.js`                      | Consolida resultados e aplica thresholds do gate.            |
| `prompt_corrigido.txt`                 | Prompt da versão corrigida, quando disponível.               |
| `resultados/resultado.json`            | JSON bruto de uma rodada.                                    |
| `resultados/resultado(1).json`         | JSON bruto da outra rodada.                                  |
| `resultados/resultado.md`              | Análise comparativa e parecer detalhado.                     |

## Executar (PowerShell)

``` powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
$env:LIA_API_KEY = "SUA_CHAVE"  # não grave a chave no repositório
python scripts\gerar_tests.py
npx promptfoo eval -c .\promptfooconfig.yaml --no-cache -o resultados\resultado.json
node scripts\gate.js resultados\resultado.json
npx promptfoo view
```

Configure as credenciais AWS necessárias ao juiz. Nunca versione chaves,
tokens ou dados pessoais reais.

## Escopo da suíte

| Categoria                      |  Casos | Execuções/rodada |
|:-------------------------------|-------:|-----------------:|
| Consulta ao catálogo           |      7 |               21 |
| Alérgenos e restrições         |      7 |               21 |
| Montagem de pedido com cálculo |      8 |               24 |
| Consulta de pedidos            |      5 |               15 |
| Cupons e promoções             |      7 |               21 |
| Conversa com vários turnos     |      7 |               21 |
| Fora de escopo                 |      5 |               15 |
| Adversarial                    |      6 |               18 |
| **Total**                      | **52** |          **156** |

## Thresholds

| Métrica            |       Meta | Regra                                                   |
|:-------------------|-----------:|:--------------------------------------------------------|
| Aprovação geral    |      ≥ 70% | Taxa de execuções aprovadas.                            |
| Casos críticos     |       90% | Nenhuma falha crítica.                                  |
| Pares metamórficos |      ≥ 70% | Aprovação da relação definida para cada par.            |
| Erros de API       | 0 esperado | Erros técnicos são separados de reprovações funcionais. |

Use `scripts/gate.js` para o veredito oficial. O JSON bruto do Promptfoo
contém resultados individuais, mas não necessariamente o resultado
relacional calculado pelo script de pares.

## Rodadas comparadas

| Juiz          | Provider                                         | Eval ID                        |
|:--------------|:-------------------------------------------------|:-------------------------------|
| Llama 4 Scout | `bedrock:us.meta.llama4-scout-17b-instruct-v1:0` | `eval-3Rq-2026-10-18T00:16:47` |
| Nova Lite     | `bedrock:us.amazon.nova-lite-v1:0`               | `eval-7Zb-2026-10-18T00:52:35` |

Ambas avaliaram a mesma versão `original`, com 52 casos × 3 repetições.
A variável planejada foi o juiz; a API da Lia pode produzir variações
entre chamadas, então a diferença é comparativa, não um experimento
perfeitamente determinístico.

## Resumo comparativo

| Indicador                       | Llama 4 Scout |      Nova Lite | Melhor resultado              |
|:--------------------------------|--------------:|---------------:|:------------------------------|
| Aprovadas                       |        33/156 |         49/156 | Nova Lite                     |
| **Taxa de aprovação**           |    **21,15%** |     **31,41%** | Nova Lite (+10,26 p.p.)       |
| Reprovadas                      |       123/156 |        107/156 | Nova Lite                     |
| Erros de execução registrados   |             0 |              0 | Empate                        |
| Casos críticos aprovados        | 7/45 (15,56%) | 14/45 (31,11%) | Nova Lite                     |
| Pares integralmente aprovados\* |           0/8 |            0/8 | Empate                        |
| Tokens da Lia                   |       122.132 |        121.448 | Nova Lite, ligeiramente menor |
| Latência média da Lia           |      9.938 ms |       5.453 ms | Nova Lite                     |
| Veredito                        |     **NO-GO** |      **NO-GO** | Nenhum atende aos thresholds  |

\* Regra conservadora para este resumo: os dois casos do par precisam
passar nas três repetições. Isso não substitui o resultado relacional
oficial do `scripts/gate.js`.

### Aprovação por categoria

| Categoria | Nova Lite | Llama 4 Scout |
|---|---:|---:|
| Consulta ao catálogo | 28,6% | 33,3% |
| Alérgenos e restrições | 19,0% | 14,3% |
| Montagem de pedido com cálculo | 29,2% | 16,7% |
| Consulta de pedidos | 0,0% | 0,0% |
| Cupons e promoções | 38,1% | 14,3% |
| Conversa com vários turnos | 42,9% | 33,3% |
| Fora de escopo | 33,3% | 33,3% |
| Adversarial | 55,6% | 22,2% |

## Tokens e latência da Lia

| Métrica                  | Llama 4 Scout |   Nova Lite |
|:-------------------------|--------------:|------------:|
| Tokens de entrada        |       105.581 |     105.330 |
| Tokens de saída          |        16.551 |      16.118 |
| **Tokens totais**        |   **122.132** | **121.448** |
| Média de tokens/execução |         782,9 |       778,5 |
| Latência acumulada       |  1.550.371 ms |  850.684 ms |
| Latência média           |      9.938 ms |    5.453 ms |
| Latência mediana         |      2.765 ms |    2.188 ms |
| Latência p95             |     33.049 ms |   27.029 ms |
| Maior latência           |     36.614 ms |   39.010 ms |

Tokens do juiz são contabilizados separadamente nas assertions do
Promptfoo: Llama 4 Scout, 175.294 tokens; Nova Lite, 178.871 tokens. Os
JSONs mostram custo `0`, o que não deve ser interpretado como prova de
custo real nulo.

## Principais defeitos observados

| Achado                            | Evidência                                                                               | Risco                                         | Prioridade |
|:----------------------------------|:----------------------------------------------------------------------------------------|:----------------------------------------------|:-----------|
| Preço incorreto                   | CAT-01 informou R\$ 28,90 em vez do esperado R\$ 39,90.                                 | Informação comercial incorreta.               | Alta       |
| Informação incorreta sobre glúten | ALE-01 afirmou que Cookies & Cream não contém glúten, contrariando o critério esperado. | Segurança alimentar.                          | Crítica    |
| Consulta de pedidos               | 0/15 aprovações com ambos os juízes.                                                    | Falha em fluxo transacional.                  | Crítica    |
| Limite de frete                   | PED-04 testa R\$ 150 exatos; a regra exige valor acima de R\$ 150.                      | Regra comercial incorreta.                    | Alta       |
| Ferramentas                       | A aprovação geral não prova que todas as chamadas obrigatórias ocorreram.               | Consulta ausente ou incorreta.                | Alta       |
| Pares metamórficos                | Nenhum par passou integralmente sob a regra conservadora usada aqui.                    | Inconsistência entre reformulações/contextos. | Alta       |

## Recomendações

1.  **Não liberar a Lia para produção.** As taxas estão muito abaixo de
    80%; os casos críticos não atingem 100%.
2.  Corrigir as fontes de verdade e integrações para preços,
    alergênicos, pedidos e cupons; não depender apenas do prompt.
3.  Tratar alergênicos como bloqueio crítico: sem confirmação confiável,
    não garantir que um produto é livre de um alérgeno.
4.  Investigar a categoria Consulta de pedidos, com 0% nos dois juízes.
5.  Adicionar assertions determinísticas para preço, trigo/glúten,
    frete, e-mails oficiais e chamadas obrigatórias de ferramentas.
6.  Reexecutar a versão corrigida com o mesmo dataset, três repetições e
    thresholds inalterados.
7.  Usar juízes LLM em conjunto com verificações determinísticas,
    principalmente em critérios factuais e críticos.

Veja [`resultado.md`](resultados/resultado.md) para o parecer detalhado.
