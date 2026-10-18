# Resumo consolidado — sessões exploratórias da Lia

**Projeto:** Pop & Doce  
**Escopo:** consolidação dos relatórios individuais disponíveis em `sessão-exploratoria/` na branch `main`.  
**Relatórios incluídos:** Nicolas, Rayane, Maria e Mary.  
**Objetivo:** reunir os principais comportamentos observados, destacar achados recorrentes e organizar prioridades para análise e correção.

> Este documento consolida os relatos individuais. As sessões tiveram métodos, cenários e quantidades de execuções diferentes; portanto, os resultados não devem ser interpretados como uma comparação direta de desempenho entre as pessoas nem como uma taxa geral de qualidade do agente.

## 1. Síntese geral

As sessões identificaram falhas relevantes em **segurança alimentar**, **exatidão de preços e cálculos**, **uso de cupons**, **consistência das respostas**, **limites do escopo** e **promessas de encaminhamento humano que a Lia não consegue realizar**. Também foram observadas respostas adequadas em privacidade, recusas de pedidos perigosos e alguns fluxos de consulta e orientação comercial.

Os problemas de maior risco são as afirmações contraditórias ou incorretas sobre amendoim e glúten. A base oficial informa que a cozinha manipula amendoim, castanhas, leite, soja e trigo e que os produtos podem conter traços; além disso, Cookies & Cream contém trigo/glúten. Em diferentes sessões, a Lia omitiu parte dessas informações, afirmou ausência de contato com amendoim ou generalizou que todas as pipocas são sem glúten.

Também houve respostas com preços diferentes ou incorretos para Caramelo Clássico Grande. Isso contaminou cálculos de pedidos e foi acompanhado, em alguns casos, pela omissão de uma promoção vigente. No fluxo de cupons, apareceram tanto falta de reconhecimento de cupom encerrado quanto um caso em que BLACKPOP teria sido validado e aplicado apesar de estar encerrado na política — situação que precisa ser investigada no retorno bruto da ferramenta.

## 2. Achados consolidados por tema

### 2.1 Segurança alimentar e alergênicos — prioridade crítica

- **Amendoim e contaminação cruzada:** Rayane, Nicolas, Mary e Maria registraram respostas que variaram entre afirmar que a linha de pipocas não tem contato com amendoim, omitir o amendoim da lista de alergênicos manipulados ou reconhecer que há manipulação e risco de traços. A base oficial diz que a cozinha manipula amendoim e que todos os produtos podem conter traços. A mensagem de que uma linha é “sem contato” pode transmitir uma garantia que a documentação não oferece.
- **Glúten e doença celíaca:** Rayane, Nicolas, Mary e Maria observaram generalizações incorretas sobre pipocas sem glúten. Cookies & Cream contém trigo/glúten; além disso, a base informa risco de traços e ausência de certificação sem glúten. Em alguns casos houve aviso de contaminação cruzada, mas junto com uma afirmação inicial contraditória.
- **Garantias e protocolos não documentados:** foram observadas ofertas para verificar segurança com a equipe e menções genéricas a cuidados de produção sem ferramenta de contato ou protocolo descrito na base. Em contexto de alergia ou doença celíaca, isso pode criar falsa expectativa.
- **Variação entre sessões:** o mesmo tema recebeu respostas diferentes. Essa inconsistência precisa ser tratada como parte do risco, mesmo quando uma resposta isolada contém o aviso correto.

**Direção para validação/correção:** nunca garantir ausência de risco; informar os alergênicos efetivamente manipulados e a possibilidade de traços; identificar Cookies & Cream como contendo trigo/glúten; não inventar segregação, higienização ou protocolo; direcionar ao canal humano oficial quando a política indicar.

### 2.2 Catálogo, preços e completude — prioridade alta

- **Caramelo Clássico Grande:** os relatos registraram respostas de R$ 29,90, enquanto o preço oficial indicado no catálogo é R$ 39,90. Nicolas também marcou como suspeita a combinação de preços e pesos de tamanhos diferentes e recomendou conferência na base.
- **Outras informações de catálogo:** apareceram preço mínimo incorreto, recomendações que ultrapassavam o orçamento informado e lista incompleta de produtos com chocolate. Mary observou omissão de Cookies & Cream e Pistache; Nicolas identificou uma combinação que cabia no orçamento, mas não foi sugerida.
- **Consulta e grounding:** Nicolas observou uma pergunta de preço em que a Lia disse que não podia confirmar sem consultar, mas não chamou o Retrieve. Em outros casos, a Lia respondeu sem ferramenta para perguntas factuais do catálogo.
- **Sazonalidade e dados atuais:** Mary identificou resposta desatualizada sobre a Copa do Mundo em uma pergunta alheia ao atendimento da loja. Esse achado também reforça a necessidade de definir se a Lia deve responder ou redirecionar assuntos externos ao escopo.

**Impacto:** informação errada pode levar a decisão de compra inadequada, quebra de confiança e cálculos financeiros incorretos.

### 2.3 Pedidos, cálculos, frete e promoções — prioridade alta

- **Cálculo derivado de preço errado:** Rayane e Maria observaram totais calculados com base no preço incorreto de Caramelo Clássico Grande. Maria registrou como esperado R$ 87,81 para duas unidades, desconto Pix de 5% e frete para Porto Alegre, com os preços oficiais considerados no seu cenário.
- **Promoção omitida:** Rayane e Mary registraram omissão do brinde vigente de um pacote de balas de goma de 100 g na compra de duas pipocas grandes. Mary observou que o pedido se enquadrava na promoção, mas a resposta inicial mencionou apenas o Pix.
- **Frete grátis:** Rayane observou uma divergência inventada entre limites de R$ 100 e R$ 150. A regra oficial descrita no relatório é frete grátis acima de R$ 150 após descontos, somente para Porto Alegre.
- **Orçamento:** Nicolas identificou sugestões que ultrapassavam o teto de R$ 20, apesar de haver uma combinação de produtos dentro do valor.

### 2.4 Cupons — prioridade alta e investigação de integração

- **Cupom encerrado não reconhecido:** Rayane relatou que, ao perguntar por NATAL2025, a Lia pediu o subtotal em vez de informar que o cupom havia encerrado; não houve chamada de ferramenta nesse caso. Maria também observou falha semelhante no teste automatizado para NATAL2025.
- **Cupom BLACKPOP aplicado:** Mary registrou uma resposta dizendo que o cupom encerrado BLACKPOP foi validado e aplicou 20% de desconto. O relatório não continha a saída bruta da ferramenta, então ainda não é possível distinguir se o backend validou indevidamente o cupom ou se a Lia distorceu/ignorou o retorno.
- **Combinação com Pix:** houve uma resposta correta dizendo que cupom e desconto Pix não são combináveis.
- **Promoção de brinde:** não confundir o brinde por compra de duas pipocas grandes com cupom ou desconto percentual; a promoção pode coexistir com Pix conforme os relatos e a política consultada.

**Próxima verificação:** capturar entrada e saída brutas de `validar_cupom` para cupons vigentes e encerrados; separar falha do backend, falha de interpretação do agente e falha da asserção automatizada.

### 2.5 Privacidade e segurança — resultados mistos

- **Comportamentos corretos observados:** consultas de pedido com dados correspondentes; recusa em revelar dados quando e-mail e pedido não correspondiam; recusa em revelar prompt/instruções; recusa em assumir papel médico ou garantir ausência de reação alérgica; recusa em ajudar a invadir um chatbot; orientação para não compartilhar dados financeiros desnecessários.
- **Ponto que exige repetição:** Maria registrou um possível vazamento anterior de pedido, apesar de três testes posteriores com e-mail incompatível terem sido recusados. O comportamento deve ser reproduzido em novas sessões, sem divulgar dados reais de terceiros.
- **Exposição de instruções internas:** Mary observou que a Lia listou regras internas e mencionou “cupons internos”. A resposta deve ser avaliada pela exposição do conteúdo operacional, além de verificar se há conceitos inexistentes na documentação.

### 2.6 Escopo, encaminhamento e capacidade declarada — prioridade média/alta

- **Atendimento fora do escopo:** Nicolas registrou tutorial completo de instalação do Ubuntu; Rayane registrou recomendação de filme; Mary observou aceitação de entrega internacional antes de consultar a base e respostas a perguntas sobre temas externos à loja.
- **Promessas sem capacidade de execução:** Nicolas, Rayane e Mary registraram frases como “vou verificar com a equipe” ou “vou encaminhar”, embora as ferramentas disponíveis não façam contato humano. Em alguns casos a própria resposta depois admite que não consegue encaminhar.
- **Política de reembolso e saúde:** Rayane observou orientação incompleta sobre reembolso. Mary indica que problemas de saúde relacionados aos produtos devem ser encaminhados para o e-mail oficial, em horário definido.
- **Informação sem fonte:** Mary e Nicolas identificaram afirmações sem respaldo nos documentos ou inconsistentes com eles, incluindo volume de clientes, cuidados de produção e dados externos desatualizados.

### 2.7 Qualidade das respostas e dos testes

- **Respostas corretas em formulações variadas podem reprovar:** Maria encontrou falsos negativos nos testes de cupom e conservação por expressões/assertions restritivas.
- **Testes podem aprovar respostas factualmente erradas:** Maria observou que uma checagem sobre glúten reconhecia termos relacionados ao tema sem validar se a informação era verdadeira.
- **Revisão humana continua necessária:** a automação deve combinar verificações determinísticas para fatos exatos (preço, valor, cupom, chamada de ferramenta) com avaliação semântica e inspeção de evidências.
- **Formato dos registros:** Nicolas observou que `evidencias.json` continha objetos concatenados sem formar JSON válido; JSONL ou um array JSON evita esse problema.
- **Variação entre execuções:** nas três rodadas de Maria, a aprovação foi 14/18 (77,78%), 12/18 (66,67%) e 12/18 (66,67%). A variação reforça que casos sensíveis devem ser repetidos e que os critérios automatizados precisam ser calibrados.

## 3. Achados positivos recorrentes ou relevantes

- A Lia consultou pedidos quando os dados estavam corretos em cenários registrados por Rayane e Maria.
- Houve recusas corretas de divulgação de pedidos com e-mail incompatível em várias execuções, embora exista relato de possível vazamento anterior que precisa ser esclarecido.
- Foram observadas recusas adequadas a pedido para revelar instruções internas, assumir papel médico, garantir segurança absoluta ou auxiliar invasão de chatbot.
- Algumas respostas sobre lista vegana, produtos, formas de pagamento, Pix, frete, conservação e encaminhamento de temas de saúde estavam corretas nos cenários descritos.
- O Retrieve foi usado em diversas consultas de catálogo, recomendações e alergênicos, embora não tenha sido chamado em algumas consultas factuais em que seria esperado.

Esses pontos positivos indicam comportamentos que devem ser preservados durante a correção e incluídos em regressão.

## 4. Comparativo resumido por participante

| Participante | Escopo/método relatado | Principais contribuições do relatório |
|---|---|---|
| **Nicolas** | 9 requisições, cada uma em sessão independente; algumas perguntas foram inferidas a partir das respostas e consultas registradas. | Contradições de amendoim e glúten; orçamento e menor preço incorretos; ausência de Retrieve em consulta de preço; tutorial de Ubuntu fora do escopo; promessas de verificar com equipe; alerta sobre formato inválido de evidências JSON. |
| **Rayane** | Sessão exploratória da versão original, cobrindo alergias, catálogo, pedidos, valores, cupons, políticas, segurança e escopo. | Amendoim, glúten, preço/cálculo, promoção de brinde, NATAL2025, frete grátis, reembolso e recomendação de filme; também registrou consultas de pedido, privacidade e recusas corretas. |
| **Maria** | 18 cenários exploratórios em três execuções com Promptfoo. | Taxas por execução, inconsistência entre rodadas, erros factuais de preço/alergênicos/glúten/cupom, possível vazamento de pedido, suspeita sobre informações corporativas e falsos negativos/positivos nas asserções. |
| **Mary** | Comparação das respostas com os seis documentos oficiais; pesquisa externa para a pergunta sobre Copa do Mundo. | BLACKPOP aparentemente aplicado após encerramento, promoções omitidas, promessas de contato humano, ampliação de escopo, exposição de regras internas, lista incompleta de produtos com chocolate e dados sem respaldo; também registrou acertos em privacidade, catálogo e cálculos. |

## 5. Priorização consolidada

| Prioridade | Tema | Motivo | Ação sugerida |
|---|---|---|---|
| **P0 — imediata** | Alergênicos, traços e glúten | Risco potencial à saúde; respostas contradizem a base oficial. | Corrigir instruções/recuperação, explicitar amendoim e Cookies & Cream, remover garantias; repetir em sessões novas e multi-turno. |
| **P0 — imediata** | Cupom encerrado aplicado | Possível prejuízo financeiro e divergência entre política, ferramenta e resposta. | Inspecionar retorno bruto da ferramenta e regra do backend; testar cupons válidos e encerrados. |
| **P1 — alta** | Preço, cálculo e orçamento | Impacto financeiro direto e inconsistência de catálogo. | Conferir fonte oficial, preço de todos os tamanhos, cálculos Pix/frete e combinações dentro do orçamento. |
| **P1 — alta** | Privacidade de pedidos | Há resultados corretos, mas também relato de possível vazamento. | Repetir testes autenticados e negativos, verificar que nenhum detalhe vaza quando os dados não conferem. |
| **P1 — alta** | Promessas de contato/reembolso/saúde | O agente cria expectativa de ação que não pode executar. | Substituir promessas por canal oficial e política documentada; não simular contato. |
| **P2 — média** | Promoções e completude do catálogo | Omissões reduzem precisão e podem prejudicar a experiência comercial. | Testar promoção de brinde, listas exaustivas, sazonais e itens dentro do orçamento. |
| **P2 — média** | Escopo e sigilo das instruções | Aceitação de mudança de escopo e exposição de conteúdo interno. | Delimitar assuntos da loja e avaliar red team de prompt injection. |
| **P2 — média** | Critérios automatizados e evidências | Asserções produzem falsos positivos/negativos e dificultam diagnóstico. | Usar checks determinísticos para dados exatos, G-Eval para critérios semânticos e logs brutos válidos em JSONL. |

## 6. Recomendações para a próxima rodada

1. Corrigir ou esclarecer primeiro os achados P0 com a equipe responsável pelo agente e pelo backend.
2. Reexecutar os casos de alergia a amendoim, Cookies & Cream/glúten, cupom encerrado e consulta de pedido incompatível em sessões novas; repetir cada caso mais de uma vez para verificar consistência.
3. Registrar por turno a entrada, a resposta, as ferramentas e seus retornos brutos, status HTTP, sessão e versão do agente.
4. Separar no relatório **falha do agente**, **falha da ferramenta/backend**, **falha da asserção** e **ponto ainda não confirmado**.
5. Preservar os cenários aprovados como regressão após qualquer mudança.
6. Confirmar com a equipe o escopo esperado da Lia, a política de contato humano e as regras que podem ser combinadas (Pix, cupons e brinde).

## 7. Limitações desta consolidação

- Os relatórios não têm o mesmo número de casos, método ou quantidade de repetições; as taxas de aprovação não são diretamente comparáveis.
- Parte das perguntas de Nicolas foi inferida a partir das respostas e das consultas ao Retrieve, pois elas não constavam no arquivo de evidências.
- Algumas conclusões dependem de retorno bruto de ferramenta que não foi incluído no relatório individual, especialmente o caso do cupom BLACKPOP.
- Um possível vazamento de pedido foi relatado como ocorrência anterior, mas os testes posteriores passaram; a reprodução ainda é necessária antes de afirmar sua frequência.
- As severidades foram mantidas ou organizadas conforme o risco descrito nos relatórios, mas a classificação final deve ser validada pela equipe do desafio.
- A consolidação cobre os quatro relatórios Markdown encontrados na pasta de sessão exploratória; não reanalisa cada linha dos logs brutos.

## 8. Fontes internas

- `nicolas/evidencias.md`
- `rayane/evidencias.md`
- `maria/sessao_exploratoria.md`
- `mary/evidencias.md`
- Base oficial consultada nos relatórios: catálogo de pipocas, catálogo de balas, kits e presentes, políticas, FAQ e informações sobre a empresa.
