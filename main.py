from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from app.models import GenerateSummaryRequest, ReviewRequest
from app.repositories.case_repository import CaseRepository
from app.repositories.summary_repository import SummaryRepository
from app.services.ollama_client import OllamaClient
from app.services.summarizer import SummarizerService

app = FastAPI(title="Resumidor Temático Atitude")

# Configurar arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Injeção de dependência simples
case_repo = CaseRepository()
summary_repo = SummaryRepository()
ollama_client = OllamaClient()
summarizer = SummarizerService(ollama_client)

@app.get("/", response_class=HTMLResponse)
async def get_index(request: Request):
    return FileResponse("app/templates/index.html")

@app.get("/api/health")
async def health_check():
    ollama_ok = await ollama_client.check_health()
    return {"status": "ok", "ollama_available": ollama_ok}

@app.get("/api/cases")
async def get_cases():
    return case_repo.list_cases()

@app.get("/api/cases/{case_id}")
async def get_case(case_id: str):
    case = case_repo.get_case(case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")
    return case

@app.post("/api/summaries")
async def generate_summary(req: GenerateSummaryRequest):
    if not req.record_ids:
        raise HTTPException(status_code=400, detail="Selecione ao menos um registro para gerar o resumo.")
        
    case = case_repo.get_case(req.case_id)
    if not case:
        raise HTTPException(status_code=404, detail="Caso não encontrado.")
    
    if case.entrada != req.entry_id:
        raise HTTPException(status_code=400, detail="A entrada fornecida não corresponde à entrada ativa do caso.")
        
    # Filtrar registros que foram selecionados pelo usuário
    registros_selecionados = [r for r in case.registros if r.id in req.record_ids]
    if not registros_selecionados:
        raise HTTPException(status_code=400, detail="Nenhum registro válido selecionado.")
        
    # Verificar se Ollama está respondendo antes de tentar
    if not await ollama_client.check_health():
        raise HTTPException(status_code=503, detail="O mecanismo local de resumo não está disponível. Inicie o Ollama e tente novamente.")
        
    try:
        resumo, erros, tempos = await summarizer.generate_summary(case, registros_selecionados)
        
        # Persistir
        exec_id = summary_repo.save_execution({
            "case_id": req.case_id,
            "entry_id": req.entry_id,
            "selected_record_ids": req.record_ids,
            "model": summarizer.model_name,
            "prompt_version": "3.1",
            "generated_json": resumo,
            "validation_errors": erros,
            "total_seconds": tempos["total_seconds"],
            "load_seconds": tempos["load_seconds"],
            "generation_seconds": tempos["generation_seconds"]
        })
        
        return {
            "id": exec_id,
            "resumo": resumo,
            "erros": erros,
            "tempos": tempos,
            "fontes_consultaveis": {r.id: {"data": r.data, "texto_original": r.texto} for r in registros_selecionados}
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/summaries/search")
async def search_summaries(req: GenerateSummaryRequest):
    history = summary_repo.find_by_selection(req.case_id, req.entry_id, req.record_ids)
    return {"history": history}

@app.get("/api/summaries/{summary_id}")
async def get_summary(summary_id: str):
    summary = summary_repo.get_summary(summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary

@app.post("/api/summaries/{summary_id}/reviews")
async def add_review(summary_id: str, req: ReviewRequest):
    summary = summary_repo.get_summary(summary_id)
    if not summary:
        raise HTTPException(status_code=404, detail="Summary not found")
        
    review_id = summary_repo.save_review(
        summary_id=summary_id,
        reviewer=req.reviewer,
        revised_json=req.revised_json.model_dump()
    )
    return {"id": review_id, "status": "success"}
