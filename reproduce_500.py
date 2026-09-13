import asyncio
import httpx
from app.main import app
from httpx import ASGITransport

async def test_500():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First check health
        response = await ac.get("/api/health")
        print("Health:", response.status_code, response.json())
        
        # Test generate summary
        payload = {
            "case_id": "FIC-001",
            "entry_id": "E01",
            "record_ids": ["FIC001-R01"]
        }
        response = await ac.post("/api/summaries", json=payload)
        print("Summary:", response.status_code, response.text)

if __name__ == "__main__":
    asyncio.run(test_500())
