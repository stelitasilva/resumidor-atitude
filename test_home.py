import asyncio
import httpx
from app.main import app
from httpx import ASGITransport
import traceback

async def test_home():
    async with httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        try:
            r = await ac.get("/")
            print(r.status_code)
        except Exception as e:
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_home())
