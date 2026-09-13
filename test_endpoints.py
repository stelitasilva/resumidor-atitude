import asyncio
import httpx
from app.main import app
from httpx import ASGITransport

async def test_all():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        print("Testing /api/health")
        try:
            r = await ac.get("/api/health")
            print(r.status_code, r.text[:100])
        except Exception as e:
            print("Error:", e)
            
        print("\nTesting /api/cases")
        try:
            r = await ac.get("/api/cases")
            print(r.status_code, r.text[:100])
        except Exception as e:
            print("Error:", e)
            
        print("\nTesting /api/cases/FIC-001")
        try:
            r = await ac.get("/api/cases/FIC-001")
            print(r.status_code, r.text[:100])
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    asyncio.run(test_all())
