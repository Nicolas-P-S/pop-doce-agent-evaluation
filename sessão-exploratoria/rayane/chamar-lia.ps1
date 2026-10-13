param(
    [Parameter(Mandatory=$true)][string]$Mensagem,
    [string]$Sessao
)

$url = "https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/"

if (-not $env:POP_DOCE_API_KEY) {
    throw "Defina POP_DOCE_API_KEY nesta janela do PowerShell primeiro."
}

$bodyObjeto = @{ mensagem = $Mensagem }
if ($Sessao) { $bodyObjeto.sessao = $Sessao }

$body = $bodyObjeto | ConvertTo-Json -Compress
$headers = @{ "x-api-key" = $env:POP_DOCE_API_KEY }

$resposta = Invoke-RestMethod -Uri $url -Method Post -Headers $headers `
    -ContentType "application/json; charset=utf-8" `
    -Body ([System.Text.Encoding]::UTF8.GetBytes($body))

$registro = [ordered]@{
    mensagem = $Mensagem
    resposta = $resposta
}
$linha = $registro | ConvertTo-Json -Depth 20 -Compress
Add-Content -Path (Join-Path $PSScriptRoot "evidencias.jsonl") -Value $linha -Encoding utf8

$resposta