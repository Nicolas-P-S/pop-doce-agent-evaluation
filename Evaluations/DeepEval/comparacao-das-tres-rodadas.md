# Comparação das três rodadas do DeepEval

## Escopo da comparação

Foram comparados os três JSONL da branch `feature/rayaneduarte`: a rodada original com threshold 0,7, a rodada com threshold 0,7 geral e 0,9 para casos críticos, e a rodada pós-prompt corrigido. Cada execução contém 52 casos com três repetições, 156 avaliações individuais e 24 avaliações de pares metamórficos, totalizando 180 avaliações.

## Configurações

| Rodada | Versão do agente registrada | Threshold | Execução |
|---|---|---|---|
| 1. Nova Pro — versão original | `original` | 0,7 geral | `d4965b72-78d1-4077-b22a-055af74a7443` |
| 2. Threshold crítico | `original` | 0,7 geral; 0,9 crítico | `9a7c2c44-ca63-4223-86c4-0390d83f72cd` |
| 3. Pós-prompt | `corrigida` | 0,7 geral; 0,9 crítico | `04aa8b5f-ffa8-41af-a0be-985ae7d97d9f` |

## Aprovações

| Rodada | Casos individuais | Pares metamórficos | Total aprovado |
|---|---:|---:|---:|
| 1. Original / threshold geral 0,7 | 94/156 (60,3%) | 16/24 (66,7%) | **110/180 (61,1%)** |
| 2. Threshold crítico 0,9 | 15/156 (9,6%) | 0/24 (0%) | **15/180 (8,3%)** |
| 3. Pós-prompt corrigido | 18/156 (11,5%) | 2/24 (8,3%) | **20/180 (11,1%)** |

Casos individuais aprovados em cada repetição:

| Rodada | Repetição 1 | Repetição 2 | Repetição 3 |
|---|---:|---:|---:|
| 1 | 31/52 | 28/52 | 35/52 |
| 2 | 4/52 | 8/52 | 3/52 |
| 3 | 6/52 | 6/52 | 6/52 |

## Casos individuais por severidade

| Severidade | Rodada 1 | Rodada 2 | Rodada 3 |
|---|---:|---:|---:|
| Crítica | 24/45 (53,3%) | 3/45 (6,7%) | 5/45 (11,1%) |
| Alta | 34/60 (56,7%) | 7/60 (11,7%) | 9/60 (15,0%) |
| Média | 35/48 (72,9%) | 2/48 (4,2%) | 1/48 (2,1%) |
| Baixa | 1/3 (33,3%) | 3/3 (100%) | 3/3 (100%) |

## Chamadas da API e ferramentas

| Medida | Rodada 1 | Rodada 2 | Rodada 3 |
|---|---:|---:|---:|
| Chamadas à Lia | 185 | 186 | 186 |
| HTTP 200 | 184 | 186 | 186 |
| Chamadas com ferramentas registradas | 132 | 0 | 0 |
| Verificações de ferramenta esperada que falharam | 0 | 21 | 21 |

As 21 falhas de ferramenta nas rodadas 2 e 3 correspondem a CON-01, CON-02, CON-04, CUP-01, CUP-03, CUP-04 e MT-03, cada um executado três vezes. Portanto, a API respondeu em todas as chamadas das rodadas 2 e 3, mas não registrou nenhuma ferramenta.

## Erros técnicos

- **Rodada 1:** uma chamada à API falhou por `RemoteDisconnected`, em MT-06, repetição 3. As demais chamadas à Lia foram HTTP 200 e não houve erro do juiz.
- **Rodada 2:** não houve erro de chamada nem do avaliador.
- **Rodada 3:** houve um `TimeoutError` do G-Eval em CON-02, repetição 2. As chamadas à Lia foram HTTP 200; as demais avaliações do juiz foram executadas.

## O que os resultados permitem concluir

### Rodada 1 para rodada 2

A aprovação caiu de 110 para 15, mas essa comparação **não isola o efeito do threshold**. A segunda rodada também coincide com a ausência completa de ferramentas: a primeira registrou ferramentas em 132 chamadas, enquanto a segunda não registrou nenhuma. A mudança no uso das ferramentas pode ter afetado respostas de pedidos e cupons, então não é correto atribuir a queda toda ao limite de 0,9.

### Rodada 2 para rodada 3

As duas rodadas usam thresholds iguais e registraram zero chamadas de ferramentas. A rodada pós-prompt teve **cinco aprovações a mais** (20 contra 15): três casos individuais a mais e dois pares aprovados, contra nenhum par aprovado na rodada 2. É uma melhora observada, mas pequena; como as respostas do agente variam entre repetições e houve um timeout isolado, isso não prova que a alteração do prompt, sozinha, causou o aumento.

### Falhas que persistem após o prompt

Na rodada 3, ainda houve erros factuais e de segurança, como preço incorreto para o Caramelo Clássico grande, afirmação de que Cookies & Cream não contém glúten e alegações sem base sobre uma linha separada para pessoas com alergia. Também permaneceram ausentes as ferramentas esperadas em consultas de pedido e cupons.

## Conclusão

A rodada original teve a maior taxa de aprovação, mas ocorreu com ferramentas presentes em boa parte das chamadas. Nas duas rodadas posteriores, a aprovação foi muito menor e nenhuma ferramenta foi registrada. A rodada pós-prompt subiu de 15 para 20 aprovações em relação à rodada com threshold crítico de 0,9, mas ainda apresentou falhas graves e não restabeleceu o uso das ferramentas.

Os resultados documentam três estados observados do agente e do avaliador. Eles **não demonstram isoladamente** o efeito causal do threshold nem do prompt, porque o comportamento das ferramentas mudou entre as rodadas. A comparação mais útil para continuidade é investigar por que a Lia não está chamando as ferramentas e revisar os achados críticos de segurança alimentar.

## Arquivos comparados

- `versao-original/execucoes- nova-pro.jsonl`
- `versao-original/execucoes-threshold-07-critico-09.jsonl`
- `prompt-corrigido/execucoes-prompt-corrigido-threshold-07-critico-09-final.jsonl`
