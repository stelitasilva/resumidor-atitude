import httpx
import json
from typing import Dict, Any

class OllamaClient:
    def __init__(self, base_url: str = "http://127.0.0.1:11434"):
        self.base_url = base_url

    async def check_health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(self.base_url)
                return response.status_code == 200
        except:
            return False

    async def generate_chat(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=180.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.ReadTimeout:
                raise Exception("Timeout")
            except httpx.HTTPError as e:
                raise Exception(f"Erro HTTP: {e}")
