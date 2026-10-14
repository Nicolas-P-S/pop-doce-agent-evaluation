"""
Testes simples das rotas/contratos da API Pop & Doce.

Instale as dependências:
    pip install pytest requests

Configure a chave no terminal antes de executar:
    PowerShell:
        $env:POP_DOCE_API_KEY="SUA_CHAVE"
    Ubuntu/Linux:
        export POP_DOCE_API_KEY="SUA_CHAVE"

Execute:
    python -m pytest -v test_rotas_api.py

Observação: cada teste faz uma chamada real à API. Execute sem paralelismo.
"""

from dotenv import load_dotenv
import os
import pytest
import requests
load_dotenv()

API_URL = "https://rm4naioqykxiti2srofnqz6hqa0ctlav.lambda-url.us-east-1.on.aws/"
API_KEY = os.getenv("POP_DOCE_API_KEY")

@pytest.fixture
def headers():
    if not API_KEY:
        pytest.fail(
            "Defina a variável de ambiente POP_DOCE_API_KEY com sua chave da API."
        )
    return {
        "Content-Type": "application/json",
        "x-api-key": API_KEY,
    }


def test_post_mensagem_retorna_sucesso(headers):
    """Verifica se a rota aceita uma mensagem válida."""
    response = requests.post(
        API_URL,
        headers=headers,
        json={"mensagem": "Olá, Lia!"}
    )

    assert response.status_code == 200
    assert response.headers.get("Content-Type", "").startswith("application/json")
    assert isinstance(response.json(), dict)


def test_resposta_contem_campos_esperados(headers):
    """Verifica a estrutura básica da resposta da API."""
    response = requests.post(
        API_URL,
        headers=headers,
        json={"mensagem": "Quais produtos vocês vendem?"}
    )

    assert response.status_code == 200
    body = response.json()
    print("Campos retornados:", list(body.keys()))
    assert "resposta" in body
    assert "sessao" in body
    assert "versao" in body
    assert "ferramentas" in body
    assert "metricas" in body


def test_mensagem_ausente_retorna_400(headers):
    """Verifica o comportamento quando o campo obrigatório não é enviado."""
    response = requests.post(
        API_URL,
        headers=headers,
        json={}
    )

    assert response.status_code == 400


def test_continuacao_de_sessao(headers):
    """Verifica se é possível enviar uma segunda mensagem usando a sessão retornada."""
    primeira = requests.post(
        API_URL,
        headers=headers,
        json={"mensagem": "Olá, Lia!"}
    )
    assert primeira.status_code == 200

    dados = primeira.json()
    assert "sessao" in dados
    assert dados["sessao"]

    segunda = requests.post(
        API_URL,
        headers=headers,
        json={
            "mensagem": "Quais opções você recomenda?",
            "sessao": dados["sessao"],
        }
    )

    assert segunda.status_code == 200
    assert "resposta" in segunda.json()


def test_chave_invalida_retorna_401():
    """Teste opcional: verifica se uma chave inválida é rejeitada."""
    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": "CHAVE_INVALIDA",
        },
        json={"mensagem": "Olá!"}
    )

    assert response.status_code == 401
