#!/bin/bash

echo "Iniciando o servidor local do Ollama em segundo plano..."
ollama serve &

echo "Aguardando o Ollama inicializar (5 segundos)..."
sleep 5

echo "Solicitando o modelo qwen3:4b..."
echo "(Na primeira vez, isso pode demorar alguns minutos para baixar os 2.5GB dependendo da internet do servidor)"
ollama pull qwen3:4b

echo "Ollama pronto! Iniciando a interface do Resumidor (FastAPI)..."
# O Railway injeta a variável $PORT automaticamente. Se não existir, usamos a 8000.
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
