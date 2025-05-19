import httpx, asyncio 
from opennote.api_types import *


class AsyncVideo:
    def __init__(self, client):
        self._client = client

    async def create(self, 
        sections: int = 5, 
        model: MODEL_CHOICES = "feynman2", 
        messages: list[dict[str, str]] = [], 
        script: list[str] = [],
    ) -> VideoCreateResponse:
        if not messages and not script:
            raise ValueError("Either messages or script must be provided")
        
        headers = {
            "Authorization": f"Bearer {self._client._api_key}",
            "Content-Type": "application/json",
        }
        url = f"{self._client._base_url}/video/make"
        payload = {
            "sections": sections,
            "model": model,
            "messages": messages,
            "script": script,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return VideoCreateResponse(**response.json())
        
    
    async def status(self, video_id: str) -> VideoStatusAPIResponse:
        if not video_id:
            raise ValueError("video_id must be provided")

        url = f"{self._client._base_url}/video/status/{video_id}"
        headers = {
            "Content-Type": "application/json",
        }
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return VideoStatusAPIResponse(**response.json())



class AsyncOpennoteVideoClient:
    def __init__(self, api_key: str, base_url: str | None = None):
        self._api_key = api_key
        self._base_url = base_url or OPENNOTE_BASE_URL
        self.video = AsyncVideo(self)
