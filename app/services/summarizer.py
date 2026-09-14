import json
from pathlib import Path
from typing import List, Dict, Any, Tuple
from app.models import Record, Case
from app.services.ollama_client import OllamaClient
from app.services.validator import validar_resumo

TEMAS = ("consumo", "familia", "moradia")

TEMA_SCHEMA = {
    "type": "object",
    "properties": {
        "status_dados": {"type": "string", "enum": ["com_dados", "sem_dados", "divergente"]},
        "situacao_atual": {"type": "string"},
        "mudancas": {"type": "string"},
        "lacunas_divergencias": {"type": "array", "items": {"type": "string"}},
        "evidencias": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["status_dados", "situacao_atual", "mudancas", "lacunas_divergencias", "evidencias"],
    "additionalProperties": False,
}

SCHEMA = {
    "type": "object",
    "properties": {tema: TEMA_SCHEMA for tema in TEMAS},
    "required": list(TEMAS),
    "additionalProperties": False,
}

SYSTEM = """Você prepara uma síntese documental temática em português para conferência humana.
Use exclusivamente os registros selecionados. Preencha obrigatoriamente: consumo, familia, moradia.

Consumo: substâncias, frequência, padrão, situações de risco.
Família: contatos, vínculos, conflitos, apoio.
Moradia: situação atual, residência, acolhimento, mudanças.

Para cada tema retorne apenas este JSON (sem explicações, sem markdown):
{
  "status_dados": "com_dados|sem_dados|divergente",
  "situacao_atual": "última informação com data",
  "mudancas": "comparação com datas",
  "lacunas_divergencias": ["lista de gaps"],
  "evidencias": ["IDs dos registros"]
}

Não faça diagnóstico, prognóstico ou causalidade. Retorne APENAS JSON válido."""

class SummarizerService:
    def __init__(self, ollama_client: OllamaClient):
        self.ollama = ollama_client
        self.treino_path = Path("dados/exemplos_treinamento.json")
        self.model_name = "tinyllama"

    def _carregar_mensagens_treinamento(self) -> List[Dict[str, str]]:
        mensagens = [{"role": "system", "content": SYSTEM}]
        if not self.treino_path.exists():
            return mensagens
            
        try:
            treino = json.loads(self.treino_path.read_text(encoding="utf-8"))
            # Limit to 2 examples maximum to reduce payload
            for exemplo in treino.get("exemplos", [])[:2]:
                mensagens.append({"role": "user", "content": json.dumps(exemplo["entrada"], ensure_ascii=False)})
                mensagens.append({"role": "assistant", "content": json.dumps(exemplo["saida"], ensure_ascii=False)})
        except Exception as e:
            print(f"Erro carregando exemplos de treinamento: {e}")
            
        return mensagens

    async def generate_summary(self, case: Case, registros: List[Record]) -> Tuple[Dict[str, Any], List[str], Dict[str, Any]]:
        mensagens = self._carregar_mensagens_treinamento()

        registros_simplificados = [
            {
                "id": r.id,
                "data": r.data,
                "texto": r.texto
            }
            for r in registros
        ]

        entrada_user = {
            "caso": case.id,
            "entrada": case.entrada,
            "registros": registros_simplificados
        }
        mensagens.append({"role": "user", "content": json.dumps(entrada_user, ensure_ascii=False)})

        payload = {
            "model": self.model_name,
            "stream": False,
            "think": False,
            "format": SCHEMA,
            "messages": mensagens,
            "options": {"temperature": 0, "num_ctx": 8192, "num_predict": 2200},
            "keep_alive": "5m",
        }

        try:
            raw_response = await self.ollama.generate_chat(payload)
        except Exception as e:
            error_msg = str(e)
            print(f"[DEBUG] Ollama error: {error_msg}")
            raise Exception(error_msg)

        try:
            content = raw_response["message"]["content"]
            resumo = json.loads(content)
        except json.JSONDecodeError:
            # Retornar JSON inválido com erros, ao invés de quebrar totalmente
            # Assim a tela pode exibir erro.
            # No SDD diz: "JSON inválido: Não perder a resposta bruta; registrar falha e permitir nova tentativa."
            # Lançamos exceção que será capturada no router e convertida em erro.
            raise Exception("O modelo retornou um JSON inválido. Tente novamente.")

        erros = validar_resumo(resumo, registros)
        
        tempos = {
            "load_seconds": round(raw_response.get("load_duration", 0) / 1e9, 2),
            "generation_seconds": round(raw_response.get("eval_duration", 0) / 1e9, 2),
            "total_seconds": round(raw_response.get("total_duration", 0) / 1e9, 2)
        }

        return resumo, erros, tempos
