FROM python:3.12-slim

# Instalar dependências do sistema, o curl e zstd (necessário para o Ollama)
RUN apt-get update && apt-get install -y curl bash zstd

# Instalar o Ollama no sistema
RUN curl -fsSL https://ollama.com/install.sh | sh

# Configurar a pasta do nosso app
WORKDIR /app
RUN mkdir -p resultados
COPY . /app

# Instalar as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar o script que liga o Ollama e o FastAPI juntos
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama..."\n\
export OLLAMA_HOST=0.0.0.0:11434\n\
ollama serve > /var/log/ollama.log 2>&1 &\n\
OLLAMA_PID=$!\n\
echo "Waiting for Ollama to be ready..."\n\
for i in {1..60}; do\n\
  if curl -s http://127.0.0.1:11434/api/tags > /dev/null 2>&1; then\n\
    echo "Ollama is ready!"\n\
    break\n\
  fi\n\
  echo "Waiting... ($i/60)"\n\
  sleep 1\n\
done\n\
echo "Starting FastAPI server..."\n\
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}\n' > /app/start.sh

# Dar permissão de execução para o nosso script de inicialização
RUN chmod +x /app/start.sh

# Comando que será executado quando o servidor ligar
CMD ["/bin/bash", "/app/start.sh"]
