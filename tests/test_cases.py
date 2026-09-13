from app.repositories.case_repository import CaseRepository
from app.repositories.summary_repository import SummaryRepository
import os

def test_load_cases():
    repo = CaseRepository("dados/casos_ficticios.json")
    cases = repo.list_cases()
    assert len(cases) == 3

def test_exclusao_registros_outra_entrada():
    repo = CaseRepository("dados/casos_ficticios.json")
    case = repo.get_case("FIC-002")
    assert case is not None
    assert case.entrada == "E02"
    
    # FIC-002 originally has 4 records, 1 is from E01 and 3 are from E02
    assert len(case.registros) == 3
    for r in case.registros:
        assert r.entrada == "E02"

def test_preservacao_geracao_apos_revisao(tmp_path):
    db_path = str(tmp_path / "test.db")
    repo = SummaryRepository(db_path)
    
    data = {
        "case_id": "FIC-001",
        "entry_id": "E01",
        "selected_record_ids": ["R1"],
        "model": "test",
        "prompt_version": "1",
        "generated_json": {"test": "original"},
        "validation_errors": []
    }
    
    exec_id = repo.save_execution(data)
    repo.save_review(exec_id, "Revisor", {"test": "revised"})
    
    summary = repo.get_summary(exec_id)
    assert summary["generated_json"] == {"test": "original"}
    assert len(summary["reviews"]) == 1
    assert summary["reviews"][0]["revised_json"] == {"test": "revised"}
