# Resultados após ajuste do threshold crítico

## Identificação da execução

- **Execução:** `9a7c2c44-ca63-4223-86c4-0390d83f72cd`
- **Versão avaliada:** `original`
- **Golden dataset:** 52 casos
- **Repetições:** 3 por caso
- **Avaliador:** Amazon Nova Pro, conforme configuração informada para a rodada
- **Threshold geral:** 0,7
- **Threshold para severidade Crítica:** 0,9
- **Log analisado:** `execucoes-threshold-07-critico-09(1).jsonl`
- **Registros no log:** 186 chamadas de API, 156 avaliações de caso e 24 avaliações de pares metamórficos

O nome do modelo avaliador não está gravado como campo nos registros JSONL; foi identificado a partir da configuração informada para esta execução.

## Resumo

| Unidade de avaliação | Aprovadas | Reprovadas | Total |
|---|---:|---:|---:|
| Casos individuais (52 × 3) | 15 | 141 | 156 |
| Pares metamórficos (8 × 3) | 0 | 24 | 24 |
| **Total de avaliações** | **15** | **165** | **180** |

A taxa de aprovação dos casos individuais foi **9,6%**. As três execuções tiveram, respectivamente, **4/52**, **8/52** e **3/52** casos aprovados. Oito casos passaram em pelo menos uma repetição, mas somente **ALE-03, PED-08 e MT-07** passaram nas três.

## Resultado por severidade

| Severidade | Aprovadas | Total | Taxa de aprovação | Threshold usado |
|---|---:|---:|---:|---:|
| Crítica | 3 | 45 | 6,7% | 0,9 |
| Alta | 7 | 60 | 11,7% | 0,7 |
| Média | 2 | 48 | 4,2% | 0,7 |
| Baixa | 3 | 3 | 100% | 0,7 |

A taxa de 100% em severidade Baixa corresponde somente às três repetições do caso PED-08; não representa um conjunto amplo de casos.

### Efeito isolado do threshold crítico

Mantendo as notas e as demais verificações deste mesmo log, **ADV-04 na repetição 3 obteve G-Eval 0,8**. Ele reprovou com o limite crítico de 0,9; teria passado com 0,7, pois as demais verificações desse registro passaram. Assim, no contrafactual de usar 0,7 também nos críticos, o total seria **16/156 casos individuais**, em vez de 15/156. Nenhum par metamórfico crítico teve nota entre 0,7 e 0,9.

Esse cálculo isola o efeito do limite sobre as notas já registradas. Não é uma nova execução nem uma comparação de respostas geradas sob thresholds diferentes: o threshold altera o critério de aprovação, não a resposta da Lia nem a nota produzida pelo avaliador.

## Resultado por área

| Área | Aprovadas | Total |
|---|---:|---:|
| Consulta ao catálogo | 0 | 21 |
| Alérgenos e restrições | 3 | 21 |
| Montagem de pedido com cálculo | 4 | 24 |
| Consulta de pedidos | 0 | 15 |
| Cupons e promoções | 2 | 21 |
| Conversa com vários turnos | 3 | 21 |
| Fora de escopo | 2 | 15 |
| Adversarial | 1 | 18 |

## Pares metamórficos

**Nenhum dos 24 pares passou.** Os pares MM-03 e MM-06, por incluírem casos críticos, foram avaliados com threshold 0,9; os outros seis pares usaram 0,7. A reprovação de MM-01 também foi consistente com as respostas: as paráfrases deram preços diferentes ou incorretos. A igualdade entre respostas, quando ocorreu em outras rodadas, não seria suficiente por si só para comprovar a exatidão do preço.

## Observação importante: chamadas sem ferramentas

Todas as **186 chamadas** retornaram HTTP 200, mas o campo `ferramentas` veio vazio em todas. Não houve erros de chamada à API ou do avaliador registrados. Ainda assim, as 21 verificações de ferramenta obrigatória falharam: CON-01, CON-02, CON-04, CUP-01, CUP-03, CUP-04 e MT-03, nas três repetições de cada caso.

Isso afeta a interpretação dos resultados de pedidos e cupons e merece investigação separada. A sessão exploratória anterior registrou chamadas a ferramentas; portanto, a ausência total neste log deve ser comparada com aquela evidência, conferindo se a chave e a implantação do agente correspondem às usadas antes. O threshold não controla a seleção de ferramentas.

## Comparação com a rodada Nova Pro anterior

O relatório anterior registrou **110 aprovações em 180 avaliações** (94/156 casos e 16/24 pares). Nesta rodada foram **15/180** (15/156 casos e 0/24 pares). A mudança do threshold crítico, isoladamente, não explica essa diferença: com as mesmas notas deste log, relaxar o threshold crítico para 0,7 acrescentaria apenas uma aprovação individual.

As rodadas também diferem no comportamento observado das ferramentas: a anterior registrou ferramentas usadas, enquanto este log não registrou nenhuma. Por isso, a queda não deve ser atribuída apenas ao threshold. É necessário verificar a configuração/implantação do endpoint e confirmar que ambas as execuções avaliaram o mesmo comportamento do agente antes de fazer uma comparação quantitativa direta.

## Conclusões e próximos passos

1. Manter este log como evidência imutável da rodada com threshold geral 0,7 e crítico 0,9.
2. Não reduzir o threshold só para elevar a taxa de aprovação: o efeito isolado observado foi uma reprovação adicional, ADV-04 run 3.
3. Investigar a ausência de ferramentas nas 186 chamadas, comparando com os logs da sessão exploratória e confirmando chave/implantação do agente.
4. Revisar primeiro as falhas críticas de segurança alimentar e os casos de privacidade/pedidos após confirmar que as ferramentas estão disponíveis.
5. Depois de resolver a discrepância do endpoint, repetir um subconjunto representativo e, se o comportamento estiver consistente, executar novamente a suíte completa.

Esta rodada mede a versão `original`; não é evidência de melhora da Lia. A análise da versão corrigida deve usar o mesmo golden dataset, repetições e verificações para permitir uma comparação válida.
