import pytest
from app.services.validator import validar_resumo
from app.models import Record

def test_validar_resumo_sucesso():
    registros = [
        Record(id="R1", data="2026-08-01", entrada="E01", texto="Teste de moradia rua"),
    ]
    resumo = {
        "consumo": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []},
        "familia": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []},
        "moradia": {"status_dados": "com_dados", "situacao_atual": "Em 01/08/2026 moradia na rua", "mudancas": "", "lacunas_divergencias": [], "evidencias": ["R1"]}
    }
    erros = validar_resumo(resumo, registros)
    assert len(erros) == 0

def test_validar_resumo_temas_faltantes():
    registros = [Record(id="R1", data="2026-08-01", entrada="E01", texto="Teste")]
    resumo = {
        "consumo": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []},
    }
    erros = validar_resumo(resumo, registros)
    assert any("três temas obrigatórios" in e for e in erros)

def test_validar_resumo_sem_dados_com_evidencia():
    registros = [Record(id="R1", data="2026-08-01", entrada="E01", texto="Teste")]
    resumo = {
        "consumo": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": ["R1"]},
        "familia": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []},
        "moradia": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []}
    }
    erros = validar_resumo(resumo, registros)
    assert any("tema sem dados não deve conter evidências" in e for e in erros)

def test_validar_resumo_fonte_inexistente():
    registros = [Record(id="R1", data="2026-08-01", entrada="E01", texto="Teste")]
    resumo = {
        "consumo": {"status_dados": "com_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": ["R2"]},
        "familia": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []},
        "moradia": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []}
    }
    erros = validar_resumo(resumo, registros)
    assert any("inexistente ou fora da seleção" in e for e in erros)

def test_validar_resumo_data_nao_sustentada():
    registros = [Record(id="R1", data="2026-08-01", entrada="E01", texto="Teste")]
    resumo = {
        "consumo": {"status_dados": "com_dados", "situacao_atual": "Em 02/08/2026", "mudancas": "", "lacunas_divergencias": [], "evidencias": ["R1"]},
        "familia": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []},
        "moradia": {"status_dados": "sem_dados", "situacao_atual": "", "mudancas": "", "lacunas_divergencias": [], "evidencias": []}
    }
    erros = validar_resumo(resumo, registros)
    assert any("não encontrada nas fontes citadas" in e for e in erros)
