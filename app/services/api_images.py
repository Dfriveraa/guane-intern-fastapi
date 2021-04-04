from app.core.config import get_settings
import httpx
import asyncio

settings = get_settings()


async def get_random_image():
    async with httpx.AsyncClient() as client:
        r = await client.get(settings.api_image)
    return r.json()['message']


