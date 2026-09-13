import asyncio
from app.repositories.case_repository import CaseRepository
from app.services.ollama_client import OllamaClient
from app.services.summarizer import SummarizerService
import json

async def run():
    repo = CaseRepository()
    ollama = OllamaClient()
    summarizer = SummarizerService(ollama)
    
    # Garantir que o db dir exista
    import os
    os.makedirs("resultados", exist_ok=True)
    
    from app.repositories.summary_repository import SummaryRepository
    db = SummaryRepository()
    
    cases = repo.list_cases()
    for c_info in cases:
        print(f"Executando {c_info.id}...")
        case = repo.get_case(c_info.id)
        registros = case.registros
        
        resumo, erros, tempos = await summarizer.generate_summary(case, registros)
        
        print(f"Resultados para {c_info.id}:")
        print(json.dumps(resumo, indent=2, ensure_ascii=False))
        if erros:
            print("Erros:", erros)
        print("Tempos:", tempos)
        print("-" * 40)
        
if __name__ == "__main__":
    asyncio.run(run())
