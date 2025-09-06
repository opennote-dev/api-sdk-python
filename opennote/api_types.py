from pydantic import BaseModel, Field
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


class PracticeProblem(BaseModel):
    problem_type: Literal["mcq", "frq", "selectall"]
    problem_statement: str
    correct_answer: Optional[str | List[str]] = None # for MCQ
    difficulty: Literal["easy", "medium", "hard"] = "medium"
    answer_choices: Optional[dict[str, str]] = None  # Only for MCQ
    explanation: Optional[str] = None
    scoring_details: Optional[str] = None  # Only for FRQ
    include_graph: bool = False
    graph_description: Optional[str] = None
    graph_url: Optional[str] = None
    user_answer: Optional[str | List[str]] = None  # User's selected option(s) or textarea response

class PracticeProblemSet(BaseModel):
    set_id: str
    set_name: Optional[str] = None
    problems: Optional[list[PracticeProblem]] = None
    cost: Optional[float] = None

class PracticeProblemSetJobCreateRequest(BaseModel): 
    set_description: str = Field(description="The description of the practice problem set")
    count: int = Field(default=5, description="The number of practice problems to create", ge=1, le=15)
    set_name: Optional[str] = Field(default=None, description="The name of the practice problem set. One will be generated for you at additional cost if you do not provide one.")
    search_for_problems: bool = Field(default=False, description="Whether to search the web for additional context to help with the practice problem set, at additional cost.")
    webhook_url: Optional[str] = Field(default=None, description="The webhook URL to send the practice problem set creation status to.")

class PracticeProblemSetJobCreateResponse(BaseModel):
    success: bool
    message: Optional[str] = None
    set_id: Optional[str] = None
    timestamp: str

class PracticeProblemSetStatusResponse(BaseModel):
    set_id: str
    success: bool
    status: Literal["pending", "completed", "failed", "status_error"]
    message: Optional[str] = None
    total_problems: int 
    completed_problems: int
    response: Optional[PracticeProblemSet] = None
    timestamp: str

class GradeFRQRequest(BaseModel):
    problem: PracticeProblem = Field(description="The practice problem to grade")

class GradeFRQResponse(BaseModel):
    success: bool
    timestamp: str
    score: int
    explanation: str
    max_score: int
    percentage: float
