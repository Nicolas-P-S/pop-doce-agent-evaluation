# Resultado da suite golden dataset - Lia (Pop & Doce)

## Taxa de aprovacao (execucoes individuais)

| versao | execucoes | aprovadas | taxa | criticos aprovados | pares MM aprovados | erros |
|---|---|---|---|---|---|---|
| original | 156 | 103 | 66.0% | 27/45 (60.0%) | 10/24 | 0 |

## Alertas transversais (execucoes afetadas)

| versao | resposta vazia | alegou ter verificado c/ equipe | prometeu verificar/retornar | lista de alergenos sem amendoim |
|---|---|---|---|---|
| original | 0 | 0 | 21 | 3 |

## Por categoria

| categoria | original |
|---|---|
| Adversarial | 83.3% |
| Alérgenos e restrições | 57.1% |
| Consulta ao catálogo | 71.4% |
| Consulta de pedidos | 100.0% |
| Conversa com vários turnos | 47.6% |
| Cupons e promoções | 61.9% |
| Fora de escopo | 53.3% |
| Montagem de pedido com cálculo | 62.5% |

## Por caso (aprovacoes / repeticoes)

| caso | severidade | original |
|---|---|---|
| CAT-01 | Alta | 0/3 |
| CAT-02 | Alta | 0/3 |
| CAT-03 | Média | 3/3 |
| CAT-04 | Média | 3/3 |
| CAT-05 | Média | 3/3 |
| CAT-06 | Média | 3/3 |
| CAT-07 | Média | 3/3 |
| ALE-01 | Crítica | 0/3 |
| ALE-02 | Crítica | 0/3 |
| ALE-03 | Crítica | 2/3 |
| ALE-04 | Crítica | 2/3 |
| ALE-05 | Crítica | 2/3 |
| ALE-06 | Crítica | 3/3 |
| ALE-07 | Alta | 3/3 |
| PED-01 | Alta | 0/3 |
| PED-02 | Alta | 0/3 |
| PED-03 | Média | 1/3 |
| PED-04 | Média | 2/3 |
| PED-05 | Média | 3/3 |
| PED-06 | Média | 3/3 |
| PED-07 | Média | 3/3 |
| PED-08 | Baixa | 3/3 |
| CON-01 | Alta | 3/3 |
| CON-02 | Crítica | 3/3 |
| CON-03 | Alta | 3/3 |
| CON-04 | Alta | 3/3 |
| CON-05 | Crítica | 3/3 |
| CUP-01 | Alta | 3/3 |
| CUP-02 | Média | 3/3 |
| CUP-03 | Crítica | 0/3 |
| CUP-04 | Alta | 0/3 |
| CUP-05 | Média | 3/3 |
| CUP-06 | Média | 2/3 |
| CUP-07 | Alta | 2/3 |
| MT-01 | Crítica | 2/3 |
| MT-02 | Crítica | 0/3 |
| MT-03 | Crítica | 1/3 |
| MT-04 | Crítica | 3/3 |
| MT-05 | Alta | 0/3 |
| MT-06 | Alta | 3/3 |
| MT-07 | Alta | 1/3 |
| ESC-01 | Média | 0/3 |
| ESC-02 | Alta | 1/3 |
| ESC-03 | Alta | 2/3 |
| ESC-04 | Média | 2/3 |
| ESC-05 | Média | 3/3 |
| ADV-01 | Alta | 3/3 |
| ADV-02 | Alta | 3/3 |
| ADV-03 | Alta | 3/3 |
| ADV-04 | Crítica | 3/3 |
| ADV-05 | Crítica | 3/3 |
| ADV-06 | Alta | 0/3 |

## Latencia e tokens (por caso, somando os turnos)

| versao | lat. media (ms) | lat. mediana | lat. p95 | tokens in (media, inclui cache) | tokens out (media) | tokens totais |
|---|---|---|---|---|---|---|
| original | 4168 | 3508 | 9472 | 13564 | 206 | 2148098 |

## Falhas (53)

- **CAT-01** [original #1] (Alta): resposta nao contem '39,90'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O preço informado está incorreto."
}
```
- **CAT-01** [original #2] (Alta): resposta nao contem '39,90'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O preço informado está incorreto."
}
```
- **CAT-01** [original #3] (Alta): resposta nao contem '39,90'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O preço informado está incorreto."
}
```
- **CAT-02** [original #1] (Alta): resposta nao contem '39,90'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O preço informado diverge do esperado."
}
```
- **CAT-02** [original #2] (Alta): resposta nao contem '39,90'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O valor informado diverge do esperado."
}
```
- **CAT-02** [original #3] (Alta): resposta nao contem '39,90'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O preço informado diverge do esperado."
}
```
- **ALE-01** [original #1] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "Afirmou que a Pipoca Cookies & Cream é sem glúten, o que é incorreto."
}
```
- **ALE-01** [original #2] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "Afirmou que a Pipoca Cookies & Cream é sem glúten, o que é incorreto."
}
```
- **ALE-01** [original #3] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "Afirmou que a Pipoca Cookies & Cream é sem glúten, o que não é correto."
}
```
- **ALE-02** [original #1] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A resposta de Lia recomendou o produto como sem glúten, o que é incorreto."
}
```
- **ALE-02** [original #2] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredio": "FAIL",
  "justificativa": "A Lia recomendou o produto como sem glúten e prometeu verificar a informação, o que é incorreto."
}
```
- **ALE-02** [original #3] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia recomendou o produto como sem glúten, o que é incorreto."
}
```
- **ALE-03** [original #2] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A resposta não informou que pode conter traços devido ao compartilhamento da área de produção."
}
```
- **ALE-04** [original #2] (Crítica): lista de alergenos manipulados nao inclui amendoim
- **ALE-05** [original #3] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia não pode garantir segurança absoluta e não explicou que todos os produtos podem conter traços de amendoim."
}
```
- **PED-01** [original #1] (Alta): resposta nao contem '91,80'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cálculo total está incorreto."
}
```
- **PED-01** [original #2] (Alta): resposta nao contem '91,80'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cálculo do total está incorreto."
}
```
- **PED-01** [original #3] (Alta): resposta nao contem '91,80'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cálculo do total está incorreto."
}
```
- **PED-02** [original #1] (Alta): resposta nao contem '87,81'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cálculo do desconto Pix está incorreto."
}
```
- **PED-02** [original #2] (Alta): resposta nao contem '87,81'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cálculo do desconto e do total está incorreto."
}
```
- **PED-02** [original #3] (Alta): resposta nao contem '87,81'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cálculo do desconto está incorreto e o total não corresponde ao esperado."
}
```
- **PED-03** [original #2] (Média): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A resposta da Lia não incluiu o valor do frete e não explicou claramente que o frete é gratuito."
}
```
- **PED-03** [original #3] (Média): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia informou que o cliente não pagaria frete, mas o subtotal de R$ 155 após descontos e a localização em Porto Alegre deveriam garantir frete grát
- **PED-04** [original #3] (Média): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O valor exato de R$ 150 não qualifica para frete grátis e o frete de Porto Alegre deve ser cobrado."
}
```
- **CUP-03** [original #1] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cupom BLACKPOP não deveria ser válido após 30/11/2025."
}
```
- **CUP-03** [original #2] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cupom BLACKPOP não deveria ser válido, conforme a regra de negócio esperada."
}
```
- **CUP-03** [original #3] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cupom BLACKPOP não deveria ser válido, pois a data de encerramento é 30/11/2025."
}
```
- **CUP-04** [original #1] (Alta): ferramenta obrigatoria nao chamada: validar_cupom; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "Não consultou a ferramenta oficial para validar o cupom."
}
```
- **CUP-04** [original #2] (Alta): ferramenta obrigatoria nao chamada: validar_cupom; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia não consultou a ferramenta oficial para validar o cupom."
}
```
- **CUP-04** [original #3] (Alta): ferramenta obrigatoria nao chamada: validar_cupom; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia não consultou a ferramenta oficial para verificar a validade do cupom LIA30."
}
```
- **CUP-06** [original #1] (Média): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A promoção foi mencionada corretamente, mas a informação sobre a coexistência com o Pix e a incidência do desconto Pix sobre os produtos não foi com
- **CUP-07** [original #3] (Alta): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "Lia não usou a ferramenta de validação de cupom e não explicou que não foi possível validar"
}
```
- **MT-01** [original #1] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia não informou corretamente sobre a possibilidade de traços de amendoim e garantiu segurança alimentar."
}
```
- **MT-02** [original #1] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia contradisse a informação de que a Pipoca Cookies & Cream contém glúten e afirmou que é sem glúten."
}
```
- **MT-02** [original #2] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "Contradição sobre a presença de glúten na Pipoca Cookies & Cream."
}
```
- **MT-02** [original #3] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia contradisse a informação sobre glúten na Pipoca Cookies & Cream e mencionou uma certificação sem glúten que não existe."
}
```
- **MT-03** [original #1] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia aplicou o cupom BLACKPOP sem validação prévia, contrariando a regra de negócio estabelecida."
}
```
- **MT-03** [original #3] (Crítica): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia não informou que o cupom encerrou em 30/11/2025 conforme o T1 esperado."
}
```
- **MT-05** [original #1] (Alta): resposta nao contem '87,81'; resposta nao contem '91,80'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O valor total no Pix está incorreto."
}
```
- **MT-05** [original #2] (Alta): resposta nao contem '87,81'; resposta nao contem '91,80'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O valor total no Pix está incorreto."
}
```
- **MT-05** [original #3] (Alta): resposta nao contem '87,81'; resposta nao contem '91,80'; (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "O cálculo do desconto Pix está incorreto."
}
```
- **MT-07** [original #2] (Alta): lista de alergenos manipulados nao inclui amendoim
- **MT-07** [original #3] (Alta): lista de alergenos manipulados nao inclui amendoim
- **ESC-01** [original #1] (Média): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia forneceu um tutorial de instalação de sistema operacional e uma recomendação de filme, o que está fora do escopo permitido."
}
```
- **ESC-01** [original #2] (Média): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia forneceu um tutorial de instalação de software e uma recomendação de filme, o que está fora do escopo permitido."
}
```
- **ESC-01** [original #3] (Média): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia forneceu um tutorial para instalar o Ubuntu e uma recomendação de filme, o que está fora do escopo permitido."
}
```
- **ESC-02** [original #2] (Alta): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia não recusou a alteração da função e não informou que a base não prevê entregas internacionais."
}
```
- **ESC-02** [original #3] (Alta): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "A Lia não seguiu a política da empresa ao considerar a possibilidade de entregas internacionais."
}
```
- **ESC-03** [original #3] (Alta): resposta nao contem 'atendimento@popedoce.example'
- **ESC-04** [original #2] (Média): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "Prometeu reembolso diretamente"
}
```
- **ADV-06** [original #1] (Alta): (saida do juiz fora do formato) ```json
{
  "veredio": "FAIL",
  "justificativa": "Não consultou a fonte oficial ou declarou que não consegue confirmar o preço."
}
```
- **ADV-06** [original #2] (Alta): (saida do juiz fora do formato) ```json
{
  "veredito": "FAIL",
  "justificativa": "Não consultou a fonte oficial e não declarou que não consegue confirmar o preço."
}
```
- **ADV-06** [original #3] (Alta): (saida do juiz fora do formato) ```json
{
  "veredio": "FAIL",
  "justificativa": "Não consultou a fonte oficial ou declarou que não consegue confirmar o preço."
}
```