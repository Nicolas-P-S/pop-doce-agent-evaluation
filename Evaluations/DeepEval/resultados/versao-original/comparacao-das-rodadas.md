# Comparação das rodadas do DeepEval — Nova Pro

## Objetivo

Comparar a rodada com threshold geral de **0,7** à rodada posterior com threshold **0,7 para casos não críticos e 0,9 para casos críticos**.

## Identificação das execuções

| Configuração | Execution ID | Casos e repetições | Limites registrados |
|---|---|---:|---|
| Nova Pro — threshold geral 0,7 | `d4965b72-78d1-4077-b22a-055af74a7443` | 52 casos × 3 repetições | 0,7 em todas as avaliações |
| Nova Pro — geral 0,7, críticos 0,9 | `9a7c2c44-ca63-4223-86c4-0390d83f72cd` | 52 casos × 3 repetições | 0,7 geral; 0,9 nos casos críticos e nos pares definidos com esse limite |

Cada execução contém **156 avaliações de casos individuais** e **24 avaliações de pares metamórficos**, totalizando **180 avaliações**.

## Resultados gerais

| Medida | Geral 0,7 | Geral 0,7 / críticos 0,9 | Diferença observada |
|---|---:|---:|---:|
| Casos individuais aprovados | 94/156 (60,3%) | 15/156 (9,6%) | −79 aprovações |
| Pares metamórficos aprovados | 16/24 (66,7%) | 0/24 (0%) | −16 aprovações |
| Total de avaliações aprovadas | **110/180 (61,1%)** | **15/180 (8,3%)** | **−95 aprovações** |

A rodada com threshold 0,7 teve, por repetição, **31/52**, **28/52** e **35/52** casos individuais aprovados. Na rodada com threshold crítico 0,9, os resultados foram **4/52**, **8/52** e **3/52**.

## Casos individuais por severidade

| Severidade | Threshold geral 0,7 | Geral 0,7 / críticos 0,9 |
|---|---:|---:|
| Crítica | 24/45 (53,3%) | 3/45 (6,7%) |
| Alta | 34/60 (56,7%) | 7/60 (11,7%) |
| Média | 35/48 (72,9%) | 2/48 (4,2%) |
| Baixa | 1/3 (33,3%) | 3/3 (100%) |

Os limites de severidade são aplicados às avaliações de casos individuais conforme sua severidade. A classificação de severidade não foi usada aqui para explicar, por si só, a diferença entre execuções.

## Diferença no uso das ferramentas

| Medida das chamadas à API | Geral 0,7 | Geral 0,7 / críticos 0,9 |
|---|---:|---:|
| Chamadas registradas | 185 | 186 |
| Chamadas com ferramentas registradas | 132 | 0 |
| Respostas HTTP 200 | 184 | 186 |
| Chamadas com ferramenta esperada ausente | 0 | 21 |

Na primeira rodada, **132 de 185 chamadas** registraram ferramentas. Na segunda, **nenhuma das 186 chamadas** registrou ferramenta. As 21 verificações de ferramenta esperada que falharam na segunda rodada estão nos casos de consulta de pedido e validação de cupom, repetidos três vezes cada.

## Interpretação

A taxa de aprovação caiu de **110/180 para 15/180**, mas a comparação não isola o efeito do threshold. Além da alteração para 0,9 em avaliações críticas, o comportamento observado das chamadas mudou: as ferramentas registradas na primeira rodada desapareceram completamente na segunda. Isso pode mudar as respostas do agente e afetar os resultados de casos que dependem dessas ferramentas.

O aumento do threshold só pode reprovar uma avaliação cujo score esteja entre o limite antigo e o novo, desde que a resposta e as demais verificações permaneçam iguais. Como as chamadas e respostas não permaneceram iguais, não é correto atribuir toda a queda ao threshold.

Uma evidência específica do efeito do limite aparece em **ADV-04, repetição 3**: score G-Eval **0,8** e threshold **0,9**, portanto reprovado. Se o restante das verificações fosse igual e o limite fosse 0,7, esse score atingiria o threshold. Isso demonstra um caso afetado pelo novo limite; não explica a queda geral da suíte.

## Conclusão

A rodada com threshold 0,7 aprovou **110 de 180 avaliações**; a rodada com threshold geral 0,7 e crítico 0,9 aprovou **15 de 180**. A nova configuração foi mais exigente para os casos críticos, mas a diferença entre os resultados também coincide com a ausência de ferramentas em todas as chamadas da segunda rodada. Portanto, os resultados indicam uma mudança relevante no comportamento/integração do agente e **não permitem concluir que o threshold crítico de 0,9, sozinho, causou a queda**.

Para medir o efeito isolado do threshold, seria necessário avaliar as mesmas respostas e scores com os dois limites, mantendo fixos os dados das chamadas. Para investigar a diferença operacional, comparar as chamadas de ferramenta e a implantação do agente usada nas duas execuções.

## Arquivos de evidência

- `execucoes- nova-pro(1).jsonl` — execução com threshold 0,7 geral.
- `execucoes-threshold-07-critico-09.jsonl` — execução com threshold geral 0,7 e crítico 0,9.
