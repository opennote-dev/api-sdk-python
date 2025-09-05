from pydantic import BaseModel
from typing import Literal, Optional, List, Union

OPENNOTE_BASE_URL = "https://api.opennote.com"

# Enums/Literals
MODEL_CHOICES = Literal["picasso"]
VIDEO_STATUS_CHOICES = Literal["pending", "completed", "failed", "status_error"]
MESSAGE_ROLE_CHOICES = Literal["user", "assistant", "system"]

# Error Types
class ValidationError(BaseModel):
    loc: List[Union[str, int]]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: List[ValidationError]

# Video Request Types
class VideoAPIRequestMessage(BaseModel):
    role: MESSAGE_ROLE_CHOICES
    content: str

class VideoCreateJobRequest(BaseModel):
    model: Optional[MODEL_CHOICES] = "picasso"
    messages: Optional[List[VideoAPIRequestMessage]] = None
    include_sources: Optional[bool] = False
    search_for: Optional[str] = None
    source_count: Optional[int] = 3
    length: Optional[int] = 3
    script: Optional[str] = None
    upload_to_s3: Optional[bool] = False
    title: Optional[str] = ""
    webhook_url: Optional[str] = None

# Video Response Types
class VideoCreateJobResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    video_id: Optional[str] = None

class VideoSource(BaseModel):
    url: str
    content: str

class VideoResponse(BaseModel):
    success: bool
    error: Optional[str] = None
    s3_url: Optional[str] = None
    b64_video: Optional[str] = None
    title: Optional[str] = None
    transcript: Optional[str] = None
    sources: Optional[List[VideoSource]] = None
    cost: Optional[float] = 0
    model: Optional[MODEL_CHOICES] = "picasso"
    timestamp: Optional[str] = None

class VideoJobStatusResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    completion_percentage: Optional[float] = None
    video_id: Optional[str] = None
    status: VIDEO_STATUS_CHOICES
    response: Optional[VideoResponse] = None
    error: Optional[str] = None

# Journal Types
class ApiResponseJournal(BaseModel):
    id: str
    title: str
    created_at: str
    updated_at: str

class JournalsResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    journals: Optional[List[ApiResponseJournal]] = None
    next_page_token: Optional[int] = None

class JournalContentResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    title: Optional[str] = None
    journal_id: Optional[str] = None
    content: Optional[str] = None
    timestamp: str

class Flashcard(BaseModel):
    front: str
    back: str

class FlashcardCreateRequest(BaseModel):
    set_description: str
    count: Optional[int] = 10
    set_name: Optional[str] = None

class FlashcardCreateResponse(BaseModel):
    success: bool 
    message: Optional[str] = None 
    set_name: Optional[str] = None
    flashcards: Optional[List[Flashcard]] = None 
    timestamp: str
