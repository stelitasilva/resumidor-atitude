import httpx
import json
from typing import Dict, Any

class OllamaClient:
    def __init__(self, base_url: str = "http://127.0.0.1:11434"):
        self.base_url = base_url

    async def check_health(self) -> bool:
        try:
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                return response.status_code == 200
        except:
            return False

    async def generate_chat(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=300.0) as client:  # Increased from 180 to 300
            try:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload
                )
                response.raise_for_status()
                return response.json()
            except httpx.ReadTimeout as e:
                raise Exception(f"ReadTimeout after 300 seconds: {e}")
            except httpx.TimeoutException as e:
                raise Exception(f"Timeout: {e}")
            except httpx.HTTPError as e:
                raise Exception(f"Erro HTTP: {e}")
