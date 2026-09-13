# iniciar.ps1
# Script para iniciar o protótipo do Resumidor Atitude

Write-Host "Verificando dependências..." -ForegroundColor Cyan

# 1. Verificar Ollama
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:11434" -Method Get -TimeoutSec 2 -ErrorAction Stop
    Write-Host "[OK] Ollama está em execução." -ForegroundColor Green
} catch {
    Write-Host "[ERRO] Ollama não está respondendo em 127.0.0.1:11434." -ForegroundColor Red
    Write-Host "Por favor, inicie o Ollama localmente."
    exit 1
}

# 2. Verificar modelo qwen3:4b
try {
    $tags = Invoke-RestMethod -Uri "http://127.0.0.1:11434/api/tags" -Method Get -ErrorAction Stop
    $modelFound = $tags.models | Where-Object { $_.name -like "qwen3:4b*" }
    if ($modelFound) {
        Write-Host "[OK] Modelo qwen3:4b está instalado." -ForegroundColor Green
    } else {
        Write-Host "[ERRO] Modelo qwen3:4b não encontrado no Ollama." -ForegroundColor Red
        Write-Host "Por favor, execute: ollama run qwen3:4b"
        exit 1
    }
} catch {
    Write-Host "[ERRO] Não foi possível verificar os modelos no Ollama." -ForegroundColor Red
    exit 1
}

# 3. Iniciar backend
Write-Host "Iniciando aplicação backend..." -ForegroundColor Cyan
Write-Host "[INFO] A aplicação estará disponível em http://127.0.0.1:8000" -ForegroundColor Yellow

$env:OLLAMA_NO_CLOUD="1"

# Executar usando python -m uvicorn
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
