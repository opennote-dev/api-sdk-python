from pydantic import BaseModel 
from typing import Literal 

OPENNOTE_BASE_URL = "https://api-video.opennote.me"

MODEL_CHOICES = Literal["feynman2"]

STATUS_CHOICES = Literal["pending", "success", "not_found"]

# video.create Types 
class VideoCreateResponse(BaseModel):
    video_id: str
    timestamp: str
    creation_success: bool
    api_version: str


# video.status Types 

class Source(BaseModel):
    url: str
    content: str

class VideoAPIResponseData(BaseModel): 
    video_url: str
    transcript: str
    sources: list[Source]

class OpennoteUsage(BaseModel):
    total_tokens_used: int
    total_input_tokens: int
    total_output_tokens: int
    search_credits_used: int
    cost: float

class VideoAPIResponse(BaseModel): 
    success: bool
    data: VideoAPIResponseData
    model: str
    usage: OpennoteUsage
    timestamp: str

class VideoStatusAPIResponse(BaseModel): 
    status: STATUS_CHOICES
    total_sections: int 
    completed_sections: int 
    video_id: str
    response: None | VideoAPIResponse
