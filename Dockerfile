FROM python:3.12-slim

# Instalar dependências do sistema e o curl
RUN apt-get update && apt-get install -y curl bash zstd

# Instalar o Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Iniciar o Ollama e baixar o modelo durante a montagem do servidor
# Isso evita que o modelo tenha que ser baixado toda vez que o servidor ligar
RUN ollama serve & sleep 5 && ollama pull qwen3:4b

# Configurar a pasta do nosso app
WORKDIR /app
COPY . /app

# Instalar as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# Criar o script que liga o Ollama e o FastAPI juntos
RUN echo '#!/bin/bash\n\
set -e\n\
echo "Starting Ollama..."\n\
ollama serve > /var/log/ollama.log 2>&1 &\n\
OLLAMA_PID=$!\n\
echo "Waiting for Ollama to be ready..."\n\
for i in {1..60}; do\n\
  if curl -s http://localhost:11434 > /dev/null 2>&1; then\n\
    echo "Ollama is ready!"\n\
    break\n\
  fi\n\
  echo "Waiting... ($i/60)"\n\
  sleep 1\n\
done\n\
echo "Starting FastAPI server..."\n\
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}\n' > /app/start.sh

RUN chmod +x /app/start.sh

# Expor a porta padrão
EXPOSE 8000

# Comando que será executado quando o servidor ligar
CMD ["/app/start.sh"]
