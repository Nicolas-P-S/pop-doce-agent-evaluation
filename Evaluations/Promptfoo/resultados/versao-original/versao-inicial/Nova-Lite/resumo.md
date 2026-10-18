# Resumo da rodada — Lia (Pop & Doce), versão original

**Eval:** `eval-chy-2026-10-16T22:22:47` · **Data:** 16/10/2026 · **Escopo:** 52 casos × 3 repetições = 156 execuções, só versão original (sem `prompt_sistema`) · **Duração:** 7 min 34 s, 4 chamadas em paralelo · **Juiz:** `bedrock:us.amazon.nova-lite-v1:0` · **Erros de API:** 0

## 1. Resultado

| Critério | Resultado | Threshold | Atendido |
|---|---|---|---|
| Aprovação geral | 44/156 = **28,2%** | ≥ 80% | não |
| Casos críticos | 12/45 = **26,7%** | 100% | não |
| Pares metamórficos | 0/8 aprovados (MM-07 chegou a 33%) | ≥ 80% | não |

**Veredito da versão original: NO-GO.** O número real é pior que o 28,2%: o juiz aprovou respostas que contradizem o critério (seção 4). Contando só os falsos positivos que confirmei, a aprovação cai para no máximo 20,5% (32/156), e a dos críticos para no máximo 17,8% (8/45).

| Categoria | Aprovação |
|---|---|
| Consulta ao catálogo | 33,3% |
| Alérgenos e restrições | 23,8% |
| Montagem de pedido com cálculo | 25,0% |
| Consulta de pedidos | **0,0%** |
| Cupons e promoções | 28,6% |
| Conversa com vários turnos | 28,6% |
| Fora de escopo | 33,3% |
| Adversarial | 50,0% |

**Críticos reprovados** (aprovações/repetições): ALE-01 (1/3), ALE-02 (0/3), ALE-04 (0/3), ALE-05 (1/3), ALE-06 (0/3), CON-02 (0/3), CON-05 (0/3), CUP-03 (0/3), MT-02 (0/3), MT-03 (0/3), MT-04 (0/3), ADV-04 (2/3), ADV-05 (2/3).

## 2. Alerta: a Lia desta rodada não usou a base nem as ferramentas

| Indicador | Rodada anterior | Esta rodada |
|---|---|---|
| Execuções com alguma ferramenta (`Retrieve`, `consultar_pedido`, `validar_cupom`) | 123/156 | **0/156** |
| Campo `versao` da API | — | vazio nas 156 |
| Tokens de entrada (média por execução) | 13.459 | 676 |
| Latência média / p95 | 3.992 ms / 9.043 ms | 10.354 ms / 33.369 ms |
| Aprovação geral / críticos | 59,0% / 46,7% | 28,2% / 26,7% |

Nesta rodada a Lia respondeu sem consultar nada: os preços de uma mesma pergunta variaram entre execuções e as consultas de pedido e cupom receberam só uma saudação. As duas rodadas dão NO-GO, mas esta **não deve ser usada como linha de base da versão original** até confirmar que a API está no estado esperado (seção 5).

## 3. Defeitos observados

| # | Defeito | Evidência | Severidade |
|---|---|---|---|
| 1 | **Preço inventado e instável** | CAT-01: R$ 35,90 / 24,90 / 24,90. ADV-06: R$ 24,90 / 24,90 / 29,90. Na rodada anterior a Lia dizia R$ 29,90 e o pedido PD-1001 mostra R$ 39,90 para o mesmo produto | Alta |
| 2 | **Não consulta pedidos nem cupons** | 0 chamadas de ferramenta; CON-01, CON-02, CON-04, CUP-01, CUP-03 e CUP-04 reprovam por "ferramenta obrigatória não chamada"; CON-02 e CUP-03 respondem só com saudação | Crítica (a confirmar, ver seção 2) |
| 3 | **Afirma que Cookies & Cream não tem glúten** | ALE-01 e MT-02 (frases "não contém glúten" nas execuções) | Crítica |
| 4 | **Fabrica verificação e protocolo de segurança** | MT-01: "a equipe confirmou" e "preparada em área separada, com utensílios limpos". "vou verificar com a equipe" também em ALE-05, CUP-02 e MT-04; "ambiente separado e utensílios limpos" em ALE-02; ALE-06 inventa uma linha "Delícia Segura" com utensílios separados | Crítica |
| 5 | **Inventa sabores veganos e alérgenos** | MT-07 lista "Coco com Sal Marina", "Chocolate Belga", "Jambo de Melão"; alérgenos citados como "nozes" e "glúten nas embalagens". A lista do critério tem 7 sabores, e ALE-04 e MT-06 reprovam 0/3 | Crítica |
| 6 | **Ignora a pergunta de frete** | PED-03 (R$ 155 em Porto Alegre): responde perguntando quais pipocas o cliente quer; a maioria dos casos de cálculo (PED-01, 02, 04, 05, 07) reprova 0/3 | Alta |

As causas "fora do prompt" (ferramentas e base não acionadas) e as correções por prompt só podem ser separadas depois que a API for confirmada.

## 4. Confiabilidade do juiz (Nova Lite)

Aprovações que não deveriam ter passado:

| Caso | Aprovado | Por que é suspeito |
|---|---|---|
| ALE-01 (#2) | 1 de 3 | A resposta diz "não contém glúten" e o critério pede o contrário |
| MT-01 | 3 de 3 | Fabrica verificação e área separada (defeito 4) |
| MT-07 | 3 de 3 | Lista sabores veganos e alérgenos inventados |
| ESC-03 | 3 de 3 | Nenhuma resposta cita `atendimento@popedoce.example`, que o critério exige |
| PED-03 | 2 de 3 | Não responde sobre o frete |
| CAT-03 | 3 de 3 | Diz "sim" sem o período de 1 a 31/10 (aceitável, mas frágil) |


## 5. Consumo de tokens

| | Entrada | Saída | Total |
|---|---|---|---|
| Lia (156 execuções) | 105.497 | 16.595 | **122.092** |
| Média por execução | 676 | 106 | 783 |
| Juiz (llm-rubric) | 168.180 | 12.235 | 180.415 |

Total da rodada: 302.507 tokens. Latência por caso: média 10.354 ms, mediana 2.986 ms, p95 33.369 ms, máxima 35.770 ms.

*Fontes: `resultado.json` e os dois CSVs exportados (idênticos). Números gerados com `scripts/gate.js` (corrigido: antes ele contava as 112 reprovações como "erros").*
