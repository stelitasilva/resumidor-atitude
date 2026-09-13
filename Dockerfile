FROM python:3.12-slim

# Instalar dependências do sistema e o curl
RUN apt-get update && apt-get install -y curl bash

# Instalar o Ollama no sistema
RUN curl -fsSL https://ollama.com/install.sh | sh

# Configurar a pasta do nosso app
WORKDIR /app
COPY . /app

# Instalar as bibliotecas do Python
RUN pip install --no-cache-dir -r requirements.txt

# Dar permissão de execução para o nosso script de inicialização
RUN chmod +x /app/start.sh

# Comando que será executado quando o servidor ligar
CMD ["/app/start.sh"]
