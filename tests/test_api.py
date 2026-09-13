import pytest
from fastapi.testclient import TestClient
from app.main import app, ollama_client, summarizer
from unittest.mock import AsyncMock

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200

def test_bloqueio_geracao_sem_registros():
    response = client.post("/api/summaries", json={
        "case_id": "FIC-001",
        "entry_id": "E01",
        "record_ids": []
    })
    assert response.status_code == 400
    assert "Selecione ao menos um registro" in response.json()["detail"]

@pytest.mark.asyncio
async def test_ollama_indisponivel(mocker):
    mocker.patch.object(ollama_client, 'check_health', return_value=False)
    response = client.post("/api/summaries", json={
        "case_id": "FIC-001",
        "entry_id": "E01",
        "record_ids": ["FIC001-R01"]
    })
    assert response.status_code == 503
    assert "não está disponível" in response.json()["detail"]

@pytest.mark.asyncio
async def test_timeout_simulado(mocker):
    mocker.patch.object(ollama_client, 'check_health', return_value=True)
    mocker.patch.object(summarizer, 'generate_summary', side_effect=Exception("A geração excedeu o tempo previsto. Tente novamente com menos registros."))
    
    response = client.post("/api/summaries", json={
        "case_id": "FIC-001",
        "entry_id": "E01",
        "record_ids": ["FIC001-R01"]
    })
    assert response.status_code == 500
    assert "excedeu o tempo previsto" in response.json()["detail"]

@pytest.mark.asyncio
async def test_json_invalido_simulado(mocker):
    mocker.patch.object(ollama_client, 'check_health', return_value=True)
    mocker.patch.object(summarizer, 'generate_summary', side_effect=Exception("O modelo retornou um JSON inválido. Tente novamente."))
    
    response = client.post("/api/summaries", json={
        "case_id": "FIC-001",
        "entry_id": "E01",
        "record_ids": ["FIC001-R01"]
    })
    assert response.status_code == 500
    assert "JSON inválido" in response.json()["detail"]
