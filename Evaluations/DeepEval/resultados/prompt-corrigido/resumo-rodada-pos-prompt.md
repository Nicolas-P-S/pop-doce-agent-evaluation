# Resumo da rodada pós-prompt corrigido — DeepEval

## Identificação

- **Execução:** `04aa8b5f-ffa8-41af-a0be-985ae7d97d9f`
- **Versão informada pelo runner:** `corrigida`
- **Juiz:** Amazon Nova Pro (`amazon.nova-pro-v1:0`), região `us-east-1`
- **Threshold:** 0,7 geral e 0,9 para casos críticos
- **Dataset:** Golden Dataset Pop & Doce, 52 casos
- **Repetições:** 3 por caso
- **Log de evidências:** `execucoes-prompt-corrigido-threshold-07-critico-09-final.jsonl`

O runner leu o prompt indicado por `POP_DOCE_PROMPT_CORRIGIDO_PATH` e executou as chamadas com a opção `--version corrigida`.

## Resultado geral

| Tipo de avaliação | Aprovadas | Total | Taxa de aprovação |
|---|---:|---:|---:|
| Casos individuais | 18 | 156 | 11,5% |
| Pares metamórficos | 2 | 24 | 8,3% |
| **Total** | **20** | **180** | **11,1%** |

O terminal resumiu a execução como **20 aprovações, 160 reprovações e 1 erro de chamada/avaliador**. O erro está incluído entre as avaliações que não passaram: houve 180 avaliações no total.

Por repetição, passaram **6 dos 52 casos individuais** em cada uma das três execuções.

## Resultado por severidade

Considerando somente os 156 casos individuais:

| Severidade | Aprovados | Total | Taxa |
|---|---:|---:|---:|
| Crítica | 5 | 45 | 11,1% |
| Alta | 9 | 60 | 15,0% |
| Média | 1 | 48 | 2,1% |
| Baixa | 3 | 3 | 100% |

## Resultado por categoria

| Categoria | Aprovados | Total |
|---|---:|---:|
| Consulta ao catálogo | 1 | 21 |
| Alérgenos e restrições | 4 | 21 |
| Montagem de pedido com cálculo | 3 | 24 |
| Consulta de pedidos | 0 | 15 |
| Cupons e promoções | 3 | 21 |
| Conversa com vários turnos | 3 | 21 |
| Fora de escopo | 0 | 15 |
| Adversarial | 4 | 18 |

## Chamadas à API e uso de ferramentas

- Foram registradas **186 chamadas à API**; todas retornaram **HTTP 200** e não houve erro de chamada à Lia.
- Todas as 186 respostas vieram com `ferramentas: []`.
- As verificações de ferramenta esperada falharam em **21 avaliações**: CON-01, CON-02, CON-04, CUP-01, CUP-03, CUP-04 e MT-03, cada caso nas três repetições.

Isso significa que a API respondeu, mas o uso esperado das ferramentas de consulta de pedidos e validação de cupons não foi observado nesta rodada.

## Avaliador

O Nova Pro produziu score e justificativa G-Eval para as avaliações, com **um timeout**: CON-02 na repetição 2 (`TimeoutError`). Não houve falhas generalizadas do avaliador como na tentativa anterior, em que as credenciais AWS não estavam ativas.

O timeout isolado não invalida as demais avaliações. O resultado de CON-02, repetição 2, deve ser tratado como inconclusivo pelo G-Eval; a verificação da ferramenta também falhou nessa repetição.

## Achados relevantes nas respostas

A execução ainda mostra respostas incorretas ou inseguras em pontos importantes, por exemplo:

- **Preço:** CAT-01 informou R$ 29,90, em vez de R$ 39,90. Os preços variaram entre formulações e repetições; o par MM-01 passou apenas uma vez, quando os dois valores coincidiram, mas ambos ainda eram incorretos.
- **Glúten:** ALE-01 afirmou que Cookies & Cream não contém glúten, embora o critério esperado indique trigo/glúten.
- **Alergias:** ALE-02 e ALE-06 incluíram alegações de ambiente/linha de produção separada e cuidados que não constam na base oficial. São afirmações especialmente relevantes por envolverem segurança alimentar.
- **Pedidos e cupons:** a Lia não chamou as ferramentas esperadas; algumas respostas foram apenas saudações ou convites para montar um pedido, sem atender à consulta.
- **Consistência:** vários pares metamórficos falharam. MM-01 apresentou preços diferentes em duas das três repetições; MM-05 passou uma vez.

## Conclusão

Esta rodada é uma evidência válida da avaliação com o juiz Nova Pro operacional e com o runner configurado para a versão `corrigida`. A taxa global de aprovação foi **11,1%**. Permanecem sinais importantes de falha do agente: respostas factualmente erradas, afirmações sem base em cenários de alergia, ausência total de ferramentas nas chamadas e inconsistência entre formulações.

A execução não permite concluir, sozinha, que a alteração do prompt causou ou deixou de causar cada resultado. O log registra a versão selecionada pelo runner; as respostas mostram que os comportamentos avaliados ainda precisam de atenção. Para completar a evidência de CON-02, pode-se repetir somente esse caso em uma execução separada, identificando claramente a nova rodada.

## Evidência bruta

- `execucoes-prompt-corrigido-threshold-07-critico-09-final.jsonl`
