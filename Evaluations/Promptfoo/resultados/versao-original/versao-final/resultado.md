# Resultado da avaliação — Lia / Pop & Doce

**Data:** 18/10/2026 · **Versão:** `original` · **Dataset:** 52 casos,
15 críticos, 8 pares metamórficos · **Repetições:** 3 por caso ·
**Veredito:** **NO-GO**

## 1. Resumo executivo

| Indicador                       |                  Llama 4 Scout |                      Nova Lite |
|:--------------------------------|-------------------------------:|-------------------------------:|
| Eval ID                         | `eval-3Rq-2026-10-18T00:16:47` | `eval-7Zb-2026-10-18T00:52:35` |
| Aprovadas                       |                         33/156 |                         49/156 |
| **Taxa de aprovação**           |                     **21,15%** |                     **31,41%** |
| Reprovadas                      |                        123/156 |                        107/156 |
| Erros de execução registrados   |                              0 |                              0 |
| Casos críticos aprovados        |                  7/45 (15,56%) |                 14/45 (31,11%) |
| Pares integralmente aprovados\* |                            0/8 |                            0/8 |
| Tokens da Lia                   |                        122.132 |                        121.448 |
| Latência média da Lia           |                       9.938 ms |                       5.453 ms |
| Veredito                        |                      **NO-GO** |                      **NO-GO** |

O Nova Lite aprovou 16 execuções a mais, diferença de **10,26 pontos
percentuais**. Ainda assim, 31,41% está muito abaixo da meta de 80%.
Nenhum dos juízes atingiu a meta de 100% nos casos críticos.

\* Regra conservadora deste resumo: os dois casos do par precisam passar
nas três repetições. O JSON bruto não contém necessariamente o veredito
relacional do script de pares; use o resultado oficial do
`scripts/gate.js` para o gate final.

## 2. Aprovação por categoria

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

**Leitura:** o Nova Lite ficou à frente em seis categorias, sobretudo
adversarial, cupons e montagem de pedidos. O Scout foi melhor em
catálogo. Consulta de pedidos teve 0% nos dois casos, apontando uma
falha sistemática que precisa ser investigada.

## 3. Casos críticos

| Juiz          | Aprovados | Total | Aprovação | Meta |
|:--------------|----------:|------:|----------:|-----:|
| Llama 4 Scout |         7 |    45 |    15,56% | 100% |
| Nova Lite     |        14 |    45 |    31,11% | 100% |

A diferença entre os juízes não altera o parecer: as duas rodadas
tiveram falhas críticas, especialmente preocupantes em segurança
alimentar e fluxos de pedido.

## 4. Pares metamórficos

O dataset contém oito pares. A tabela abaixo resume a quantidade de
aprovações por caso, em três repetições. Para considerar um par
integralmente aprovado nesta análise, ambos os casos precisariam passar
nas três repetições.

| Par   | Casos           | Llama 4 Scout | Nova Lite | Observação                                      |
|:------|:----------------|--------------:|----------:|:------------------------------------------------|
| MM-01 | CAT-01 / CAT-02 |     0/3 + 0/3 | 0/3 + 0/3 | Ambos falham em todas as repetições.            |
| MM-02 | CAT-03 / CAT-04 |     3/3 + 0/3 | 3/3 + 0/3 | Um caso passa; o outro não.                     |
| MM-03 | ALE-01 / ALE-02 |     0/3 + 0/3 | 0/3 + 0/3 | Falha consistente relacionada a glúten.         |
| MM-04 | PED-01 / PED-02 |     0/3 + 0/3 | 0/3 + 0/3 | Ambos falham.                                   |
| MM-05 | PED-03 / PED-04 |     0/3 + 0/3 | 3/3 + 0/3 | Nova Lite passa PED-03, mas falha PED-04.       |
| MM-06 | CON-01 / CON-02 |     0/3 + 0/3 | 0/3 + 0/3 | Ambos falham.                                   |
| MM-07 | CUP-05 / CUP-06 |     0/3 + 0/3 | 2/3 + 3/3 | Nova Lite melhora, mas CUP-05 não passa sempre. |
| MM-08 | MT-06 / MT-07   |     0/3 + 3/3 | 0/3 + 3/3 | MT-06 falha; MT-07 passa.                       |

| Padrão observado                                       | Implicação                                                                         |
|:-------------------------------------------------------|:-----------------------------------------------------------------------------------|
| Um lado do par passa e o outro falha                   | A consistência diante de reformulações ou mudanças controladas não está garantida. |
| O mesmo par falha com ambos os juízes                  | Priorizar investigação da resposta da Lia e validar o critério com a base.         |
| Resultados variam entre repetições                     | Há instabilidade de comportamento.                                                 |
| Nenhum par passa integralmente pela regra conservadora | A suíte ainda não demonstra robustez metamórfica suficiente.                       |

Essa tabela não substitui a avaliação relacional oficial: a aprovação de
um par deve considerar também a relação esperada entre as respostas,
conforme implementada pelo script do projeto.

## 5. Tokens e latência

### Lia

| Métrica                      | Llama 4 Scout |   Nova Lite |
|:-----------------------------|--------------:|------------:|
| Tokens de entrada            |       105.581 |     105.330 |
| Tokens de saída              |        16.551 |      16.118 |
| **Tokens totais**            |   **122.132** | **121.448** |
| Média de tokens por execução |         782,9 |       778,5 |
| Latência acumulada           |  1.550.371 ms |  850.684 ms |
| Latência média               |      9.938 ms |    5.453 ms |
| Latência mediana             |      2.765 ms |    2.188 ms |
| Latência p95                 |     33.049 ms |   27.029 ms |
| Maior latência               |     36.614 ms |   39.010 ms |

### Juiz (assertions do Promptfoo)

| Métrica                   | Llama 4 Scout | Nova Lite |
|:--------------------------|--------------:|----------:|
| Tokens de entrada do juiz |       149.077 |   167.133 |
| Tokens de saída do juiz   |        26.217 |    11.738 |
| Tokens totais do juiz     |       175.294 |   178.871 |

O Nova Lite apresentou menor latência média e mediana, com ligeiramente
menos tokens da Lia. A latência máxima, contudo, foi maior no Nova Lite.
O JSON exportado indica custo `0`, mas isso não prova que o custo real
seja nulo.

## 6. Evidências e defeitos

| Caso/área                | Evidência                                                                                                      | Risco                           | Prioridade |
|:-------------------------|:---------------------------------------------------------------------------------------------------------------|:--------------------------------|:-----------|
| CAT-01 — preço           | A Lia informou **R\$ 28,90**, mas o critério esperado era **R\$ 39,90**.                                       | Informação comercial incorreta. | Alta       |
| ALE-01 — glúten          | A Lia afirmou que Cookies & Cream não contém glúten, contrariando o critério esperado de indicar trigo/glúten. | Segurança alimentar.            | Crítica    |
| Consulta de pedidos      | 0/15 aprovações com ambos os juízes.                                                                           | Falha em fluxo transacional.    | Crítica    |
| PED-04 — limite de frete | O teste usa R\$ 150 exatos, mas a regra exige valor **acima** de R\$ 150.                                      | Regra comercial incorreta.      | Alta       |
| Ferramentas              | A aprovação geral não prova que as ferramentas obrigatórias foram chamadas em todos os casos.                  | Falha de integração/fluxo.      | Alta       |
| Pares metamórficos       | Nenhum par passou integralmente sob a regra conservadora adotada.                                              | Inconsistência entre variações. | Alta       |

## 7. Limitações da comparação

1.  A API da Lia pode variar entre chamadas, mesmo com o mesmo caso;
    portanto, a diferença entre juízes não deve ser atribuída
    exclusivamente ao avaliador.
2.  O score exibido no resumo do Promptfoo não é igual à taxa de testes
    aprovados. Para aprovação por execução, este relatório usa
    `testPassCount / 156`: 21,15% para Scout e 31,41% para Nova Lite.
3.  O JSON bruto não inclui necessariamente o resultado relacional
    produzido pelo script de pares. A tabela da seção 4 usa a regra
    conservadora descrita acima.
4.  `testErrorCount = 0` significa que o Promptfoo não registrou erros
    de execução; não significa que as respostas estejam corretas.

## 8. Parecer final: NO-GO

| Condição                 | Resultado observado                                 | Atendido?                   |
|:-------------------------|:----------------------------------------------------|:----------------------------|
| Aprovação geral ≥ 70%    | Melhor resultado: 31,41%                            | Não                         |
| Casos críticos = 90%    | Melhor resultado: 31,11%                            | Não                         |
| Pares metamórficos ≥ 70% | 0/8 integralmente aprovados pela regra conservadora | Não                         |
| Sem erros de execução    | 0 erros registrados                                 | Sim, apenas neste indicador |

### Recomendações prioritárias

1.  Corrigir dados e integrações para preços, alergênicos, pedidos e
    cupons; não depender apenas de ajustes no prompt.
2.  Tratar alergênicos como bloqueio crítico. Se a informação não
    estiver confirmada, a Lia não deve garantir que um produto é livre
    de um alérgeno.
3.  Investigar a categoria Consulta de pedidos, com 0% em ambas as
    rodadas.
4.  Criar assertions determinísticas para preço, trigo/glúten, frete,
    e-mails oficiais e chamadas obrigatórias de ferramentas.
5.  Reexecutar os pares com o relatório relacional oficial.
6.  Avaliar a versão corrigida com a mesma suíte, três repetições e
    thresholds inalterados.
7.  Combinar avaliação por LLM com verificações determinísticas,
    principalmente para critérios factuais e críticos.

**A Lia não deve ser liberada para produção** até cumprir os thresholds,
eliminar falhas críticas e demonstrar consistência nos pares
metamórficos.
