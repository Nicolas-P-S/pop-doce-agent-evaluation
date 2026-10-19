# Avaliação da assistente Lia — Pop & Doce

Repositório do projeto de Quality Engineering do hackathon **Go/No-Go da assistente de vendas Pop & Doce**. O trabalho reúne evidências exploratórias e automatizadas para avaliar a correção, a consistência, a segurança e o uso de ferramentas da Lia.

Este README apresenta o projeto e orienta a execução das principais suítes. As análises completas ficam nos relatórios de cada rodada; o parecer final da equipe deve consolidar os resultados e apresentar a decisão Go/No-Go.

## Escopo do projeto

A equipe avaliou a Lia em relação a:

- catálogo, preços, ingredientes e disponibilidade sazonal;
- alergênicos, restrições alimentares e risco de contaminação cruzada;
- montagem de pedidos, cálculos, frete, cupons e promoções;
- consulta autenticada de pedidos e proteção de dados;
- conversas com vários turnos e consistência entre reformulações;
- delimitação de escopo, resistência a prompt injection e uso correto das ferramentas.

## Atividades realizadas

- Sessões exploratórias individuais, reunidas em um resumo consolidado da equipe.
- Organização da base de conhecimento oficial usada como referência nos testes.
- Construção e evolução de um golden dataset com casos simples, multi-turno, metamórficos e adversariais.
- Testes básicos do contrato da API e do fluxo de sessão.
- Avaliações da suíte principal com Promptfoo e juízes configurados no Amazon Bedrock.
- Execuções complementares em Python, com verificações determinísticas, avaliação por LLM e logs detalhados.
- Testes de red team manuais e automatizados.
- Registro e comparação de rodadas da versão original e da versão com prompt corrigido, quando aplicável.

As rodadas usaram configurações e juízes diferentes. Consulte o relatório de cada rodada antes de comparar taxas; elas não formam, por si só, uma única métrica diretamente comparável.

## Estrutura do repositório

| Caminho | Conteúdo |
|---|---|
| `base-de-conhecimento-oficial/` | Catálogos, políticas, FAQ e informações da empresa usados como referência factual. |
| `sessão-exploratoria/` | Evidências e relatos individuais, mais o resumo consolidado. |
| `golden-dataset/original/` e `golden-dataset/atual/` | Versões do conjunto de casos de avaliação. |
| `prompt-corrigido/` | Arquivos do prompt corrigido usados pelas rodadas correspondentes. |
| `API_tests/` | Testes básicos de contrato e continuidade da API. |
| `Evaluations/Promptfoo/` | Suíte principal Promptfoo, provider da Lia, assertions, dataset, configurações e resultados. |
| `Evaluations/SuiteComplementar/` | Runner Python complementar, verificações determinísticas e resultados próprios. |
| `Evaluations/DeepEval/` | Evidências e relatórios de rodadas anteriores executadas com DeepEval. |
| `red-teaming/` | Configurações e evidências de testes adversariais da equipe. |
| `massa-de-teste.md` | Dados e cenários de apoio aos testes. |

## Requisitos

- Git;
- Python 3.10 ou superior para as suítes Python;
- Node.js e npm para Promptfoo;
- uma chave válida para chamar a API da Lia;
- credenciais AWS com acesso ao Amazon Bedrock para as suítes que usam juiz ou gerador hospedado.

O modelo de juiz depende da suíte e da configuração da rodada. A suíte Promptfoo configura seu provider nos YAML; o runner Python complementar usa Amazon Nova Lite por padrão. Os relatórios DeepEval preservam rodadas anteriores com Nova Pro.

## Instalação e segredos

Clone o repositório e entre na pasta:

```powershell
git clone https://github.com/Nicolas-P-S/pop-doce-agent-evaluation.git
cd pop-doce-agent-evaluation
```

Crie e ative um ambiente virtual Python no PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependências Python usadas pelas suítes:

```powershell
python -m pip install requests python-dotenv pytest boto3
```

Crie um `.env` local na raiz do repositório. As suítes usam nomes de variáveis diferentes; se a mesma chave da API servir para os dois clientes, informe-a localmente em ambos:

```dotenv
# API_tests e red-teaming
POP_DOCE_API_KEY=PREENCHA_LOCALMENTE

# Suíte principal Promptfoo e SuiteComplementar
LIA_API_KEY=PREENCHA_LOCALMENTE
LIA_API_URL=https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/

# Opcionais para SuiteComplementar
AWS_REGION=us-east-1
JUDGE_MODEL_ID=us.amazon.nova-lite-v1:0
```

O `.env` está no `.gitignore`. **Nunca coloque chaves, credenciais AWS ou dados pessoais reais no README, nos arquivos de configuração versionados ou nos commits.** Configure as credenciais AWS localmente por perfil, AWS CLI/SSO ou pelo mecanismo aprovado para sua conta. `API_tests` e as configurações de red team usam `POP_DOCE_API_KEY`; Promptfoo e `SuiteComplementar` usam `LIA_API_KEY`. Se todas as atividades usam a mesma chave da squad, preencha os dois nomes apenas no `.env` local.

## Como executar

### 1. Testes básicos da API

Com `POP_DOCE_API_KEY` preenchida no `.env`:

```powershell
python -m pytest .\API_tests\test_rotas_api.py -v
```

### 2. Suíte principal — Promptfoo

Execute a partir da raiz do repositório. O comando abaixo roda uma amostra curta; remova `--filter-first-n 2` para executar todos os casos definidos em `tests-lia.yaml`:

```powershell
npx promptfoo eval `
  -c .\Evaluations\Promptfoo\promptfooconfig.yaml `
  --env-file .env `
  --filter-first-n 2 `
  --max-concurrency 1 `
  --no-cache `
  -o .\Evaluations\Promptfoo\resultados\smoke.json
```

Os YAML da suíte configuram as versões original e corrigida, as repetições, os juízes e os critérios; `scripts/gate.js` calcula o gate. Para a rodada completa, use um nome novo no caminho de saída para preservar cada evidência. Depois, para calcular o gate a partir do JSON gerado:

```powershell
node .\Evaluations\Promptfoo\scripts\gate.js `
  .\Evaluations\Promptfoo\resultados\smoke.json
```

Detalhes da suíte e dos resultados estão em [Evaluations/Promptfoo](Evaluations/Promptfoo/README.md).

### 3. Suíte Python complementar

O runner Python complementar lê as variáveis do ambiente do processo; ele não carrega o `.env` automaticamente. Configure a chave na janela atual do PowerShell e as credenciais AWS localmente (por exemplo, com `aws configure` ou um perfil/SSO):

```powershell
$env:LIA_API_KEY = Read-Host "Chave da API da Lia"
$env:AWS_REGION = "us-east-1"
$env:JUDGE_MODEL_ID = "us.amazon.nova-lite-v1:0"
```

Faça primeiro um subconjunto:

```powershell
python .\Evaluations\SuiteComplementar\run_golden.py `
  --dataset .\golden-dataset\atual\golden_dataset_pop_doce_52_casos.csv `
  --versao original `
  --casos CAT-01,ALE-01 `
  --repeticoes 1 `
  --saida .\Evaluations\SuiteComplementar\resultados\smoke
```

Para avaliar a versão corrigida, use `--versao corrigida` e informe o arquivo local versionado, por exemplo `--prompt-corrigido .\prompt-corrigido\prompt-corrigido.txt`. Para executar ambas as versões, use `--versao ambas`. Consulte o [guia da suíte complementar](Evaluations/SuiteComplementar/README.md) para parâmetros, thresholds e formato dos relatórios.

### 4. Red team com Promptfoo

As configurações de red team estão organizadas por participante. Exemplos para os arquivos do Nicolas, executados a partir da raiz:

```powershell
npx promptfoo eval `
  -c .\red-teaming\nicolas\promptfooconfig.manu.yaml `
  --env-file .env
```

```powershell
npx promptfoo redteam run `
  -c .\red-teaming\nicolas\promptfooconfig.auto.yaml `
  --env-file .env
```

A execução automática pode gerar muitas chamadas. Revise a configuração e os limites de chamada antes de iniciar a rodada completa.

## Prompt corrigido

O prompt está versionado em `prompt-corrigido/`. Há arquivos com nomes próximos, usados por diferentes execuções:

- `prompt-corrigido/prompt-corrigido.txt` — pode ser passado ao runner `SuiteComplementar` por `--prompt-corrigido`;
- `prompt-corrigido/prompt_corrigido.txt` — usado pela configuração da suíte Promptfoo.

Use o arquivo correspondente à configuração da avaliação e registre no relatório qual versão foi testada.

## Evidências e relatórios

- [Resumo consolidado das sessões exploratórias](sessão-exploratoria/resumo-consolidado.md)
- [Relatórios da suíte Promptfoo](Evaluations/Promptfoo/README.md)
- [Relatórios da suíte complementar](Evaluations/SuiteComplementar/README.md)
- [Comparação das três rodadas DeepEval](Evaluations/DeepEval/comparacao-das-tres-rodadas.md)
- [Resultados Promptfoo da versão corrigida](Evaluations/Promptfoo/resultados/versao-corrigida/README.md)

Os arquivos JSON, JSONL e CSV guardam evidências brutas ou agregadas de cada execução. Mantenha rodadas distintas em arquivos separados e consulte o relatório associado para conhecer versão, juiz, thresholds, repetições e limitações.

## Interpretação dos resultados

Uma reprovação pode decorrer de uma resposta incorreta da Lia, de ausência ou comportamento de uma ferramenta, de falha de chamada ou de um critério automatizado inadequado. Analise a resposta bruta, as ferramentas, os erros e a justificativa do juiz em conjunto. O parecer final da equipe deve sintetizar esses achados, explicitar limitações e registrar a decisão Go/No-Go.
