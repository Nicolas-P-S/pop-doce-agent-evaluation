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
    response = requests.post(
        API_URL,
        headers=headers,
        json={"mensagem": "Olá, Lia!"}
    )

    assert response.status_code == 200
    assert response.headers.get("Content-Type", "").startswith("application/json")
    assert isinstance(response.json(), dict)


def test_resposta_contem_campos_esperados(headers):
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
    response = requests.post(
        API_URL,
        headers=headers,
        json={}
    )

    assert response.status_code == 400


def test_continuacao_de_sessao(headers):
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
    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "x-api-key": "CHAVE_INVALIDA",
        },
        json={"mensagem": "Olá!"}
    )

    assert response.status_code == 401
