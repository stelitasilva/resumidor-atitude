from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class Record(BaseModel):
    id: str
    data: str
    entrada: str
    texto: str

class Case(BaseModel):
    id: str
    nome: str
    entrada: str
    registros: List[Record]
    objetivo_teste: str = ""

class CaseSummaryInfo(BaseModel):
    id: str
    nome: str
    entrada: str
    quantidade_registros: int

class TemaSummary(BaseModel):
    status_dados: str = Field(..., pattern="^(com_dados|sem_dados|divergente)$")
    situacao_atual: str
    mudancas: str
    lacunas_divergencias: List[str]
    evidencias: List[str]

class GenerateSummaryRequest(BaseModel):
    case_id: str
    entry_id: str
    record_ids: List[str]

class SummaryResponse(BaseModel):
    consumo: TemaSummary
    familia: TemaSummary
    moradia: TemaSummary

class ReviewRequest(BaseModel):
    reviewer: str
    revised_json: SummaryResponse
