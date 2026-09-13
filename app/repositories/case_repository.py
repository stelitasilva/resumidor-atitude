import json
from pathlib import Path
from typing import List, Optional
from app.models import Case, CaseSummaryInfo

class CaseRepository:
    def __init__(self, data_path: str = "dados/casos_ficticios.json"):
        self.data_path = Path(data_path)
        self.cases = []
        self._load_data()

    def _load_data(self):
        if not self.data_path.exists():
            return
        try:
            data = json.loads(self.data_path.read_text(encoding="utf-8"))
            self.cases = [Case(**c) for c in data.get("casos", [])]
        except Exception as e:
            print(f"Error loading cases: {e}")

    def list_cases(self) -> List[CaseSummaryInfo]:
        return [
            CaseSummaryInfo(
                id=c.id,
                nome=c.nome,
                entrada=c.entrada,
                quantidade_registros=len([r for r in c.registros if r.entrada == c.entrada])
            ) for c in self.cases
        ]

    def get_case(self, case_id: str) -> Optional[Case]:
        for c in self.cases:
            if c.id == case_id:
                # Filtrar registros da entrada ativa
                filtered_records = [r for r in c.registros if r.entrada == c.entrada]
                return Case(
                    id=c.id,
                    nome=c.nome,
                    entrada=c.entrada,
                    registros=filtered_records,
                    objetivo_teste=c.objetivo_teste
                )
        return None
