# Resumidor Temático do Acompanhamento Atitude - Protótipo Funcional

Este é o protótipo funcional do Resumidor Temático, desenvolvido conforme o SDD para a prova de conceito.
A aplicação opera estritamente de forma local, comunicando-se com o Ollama em `127.0.0.1:11434` e utilizando o modelo `qwen3:4b`.

## Instalação

1. Certifique-se de ter o Python 3.12+ e o Ollama instalados localmente.
2. Certifique-se de que o modelo `qwen3:4b` esteja baixado no Ollama (`ollama run qwen3:4b`).
3. Instale as dependências Python:
   ```powershell
   pip install -r requirements.txt
   ```

## Testes

Para executar a suíte de testes (unitários e da API):
```powershell
python -m pytest tests/
```

## Execução

O script de inicialização executa as validações do Ollama e modelo, e inicia o servidor local.

```powershell
.\iniciar.ps1
```

O aplicativo estará disponível em: `http://127.0.0.1:8000`

## Funcionalidades (Must)

- Seleção de casos e exclusão de registros fora da entrada.
- Geração local por Ollama + qwen3:4b, bloqueada se nenhum registro for selecionado.
- Exibição de cartões temáticos com Situação Atual, Mudanças, Lacunas e Fontes.
- Validação estrutural de presença de dados.
- Link direto para a fonte original sem reescrita e sem adulteração.
- Revisão humana (salva no banco local SQLite separadamente).
- Nenhuma API de terceiros na nuvem.

*Protótipo Acadêmico — Usa somente os dados fictícios.*
