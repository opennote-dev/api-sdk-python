from typing import Optional, List, Literal, Dict, Any
import httpx
from opennote.types import (
    VideoCreateJobRequest,
    VideoCreateJobResponse,
    VideoJobStatusResponse,
    JournalsResponse,
    JournalContentResponse,
    VideoAPIRequestMessage,
    FlashcardCreateRequest,
    FlashcardCreateResponse,
    PracticeProblemSetJobCreateRequest,
    PracticeProblemSetJobCreateResponse,
    PracticeProblemSetStatusResponse,
    GradeFRQResponse,
    JournalDeleteResponse,
    GradeFRQRequest,
    PracticeProblem,
    ImportFromMarkdownRequest,
    ImportFromMarkdownResponse,
    EditJournalRequest,
    EditJournalResponse,
    ModelInfoResponse,
    EditOperation,
    CreateJournalRequest,
    CreateJournalResponse,
    RenameJournalRequest,
    RenameJournalResponse,
)
from opennote.base_client import BaseClient
from opennote.types import OPENNOTE_BASE_URL, MODEL_CHOICES


class Video:
    """Video endpoints for Opennote API."""
    
    def __init__(self, client: "OpennoteClient"):
        self._client = client

    def create(
        self,
        messages: Optional[List[VideoAPIRequestMessage]] = None,
        model: Optional[MODEL_CHOICES] = "picasso",
        include_sources: Optional[bool] = False,
        search_for: Optional[str] = None,
        source_count: Optional[int] = 3,
        length: Optional[int] = 3,
        script: Optional[str] = None,
        upload_to_s3: Optional[bool] = False,
        title: Optional[str] = "",
        webhook_url: Optional[str] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
    ) -> VideoCreateJobResponse:
        """
        Create a new video job.
        
        Args:
            messages: List of messages for video script generation
            model: Model to use (default: "picasso")
            include_sources: Whether to gather web data for the script
            search_for: Query to search the web (max 100 chars)
            source_count: Number of web sources to gather (1-5)
            length: Number of paragraphs in script (1-5)
            script: Pre-written script with sections delimited by '-----' (max 6000 chars)
            upload_to_s3: Whether to upload video to S3
            title: Title of the video
            webhook_url: URL to send the final completion status to (same response type as the status endpoint)
        Returns:
            VideoCreateJobResponse with success status and video_id
        """
        request = VideoCreateJobRequest(
            messages=messages,
            model=model,
            include_sources=include_sources,
            search_for=search_for,
            source_count=source_count,
            length=length,
            script=script,
            upload_to_s3=upload_to_s3,
            title=title,
            webhook_url=webhook_url,
        )
        
        response = self._client._request(
            "POST",
            "/v1/video/create",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return VideoCreateJobResponse(**response)

    def status(self, video_id: str, extra_headers: Optional[Dict[str, str]] = None) -> VideoJobStatusResponse:
        """
        Get the status of a video job.
        
        Args:
            video_id: ID of the video job
            
        Returns:
            VideoJobStatusResponse with status and completion details
        """
        if not video_id:
            raise ValueError("video_id must be provided")
        
        response = self._client._request(
            "GET",
            f"/v1/video/status/{video_id}",
            extra_headers=extra_headers,
        )
        return VideoJobStatusResponse(**response)


class JournalEditor:
    """Journal editing endpoints for the Opennote API."""

    def __init__(self, client: "OpennoteClient"):
        self._client = client

    def import_from_markdown(self, markdown: str, title: Optional[str] = "Imported Journal", team_slug: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> ImportFromMarkdownResponse:
        """
        Import a journal from markdown content.
        
        Args:
            markdown: The markdown content to import
            title: Optional title for the journal (default: "Imported Journal")
            team_slug: The team slug that the journal is associated with
            
        Returns:
            ImportFromMarkdownResponse with journal_id and journal_url
        """
        request = ImportFromMarkdownRequest(
            markdown=markdown,
            title=title,
            team_slug=team_slug
        )
        
        response = self._client._request(
            "PUT",
            "/v1/journals/editor/import_from_markdown",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return ImportFromMarkdownResponse(**response)

    def edit(self, journal_id: str, operations: List[EditOperation], sync_realtime_state: bool = True, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> EditJournalResponse:
        """
        Edit a journal with a list of operations.
        
        Args:
            journal_id: ID of the journal to edit
            operations: List of edit operations to perform
            sync_realtime_state: Whether to directly update the state of the journal to all connected users. 
                WARNING: Operations through synced states CANNOT be undone, and will remove Ctrl+Z functionality for all users for the changes made.

        Returns:
            EditJournalResponse with results for each operation
        """
        request = EditJournalRequest(
            journal_id=journal_id,
            operations=operations,
            sync_realtime_state=sync_realtime_state
        )
        
        response = self._client._request(
            "PATCH",
            "/v1/journals/editor/edit",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return EditJournalResponse(**response)
    
    def model_info(self, journal_id: str, extra_headers: Optional[Dict[str, str]] = None) -> ModelInfoResponse:
        """
        Get the ProseMirror model representation of a journal.
        
        Args:
            journal_id: ID of the journal
            
        Returns:
            ModelInfoResponse with the JSON representation of the journal
        """
        if not journal_id:
            raise ValueError("journal_id must be provided")
        
        response = self._client._request(
            "GET",
            f"/v1/journals/editor/model/{journal_id}",
            extra_headers=extra_headers,
        )
        return ModelInfoResponse(**response)
    
    def delete(self, journal_id: str, extra_headers: Optional[Dict[str, str]] = None) -> JournalDeleteResponse:
        """
        Delete a journal.
        
        Args:
            journal_id: ID of the journal to delete
            
        Returns:
            JournalDeleteResponse confirming deletion
        """
        if not journal_id:
            raise ValueError("journal_id must be provided")
        
        response = self._client._request(
            "DELETE",
            f"/v1/journals/editor/delete/{journal_id}",
            extra_headers=extra_headers,
        )
        return JournalDeleteResponse(**response)

class Journals:
    """Journal endpoints for Opennote API."""
    
    def __init__(self, client: "OpennoteClient"):
        self._client = client
        self.editor = JournalEditor(client)

    def create(self, title: str, team_slug: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> CreateJournalResponse:
        """
        Create a new journal.
        
        Args:
            title: The title of the journal
            team_slug: The team slug that the journal is associated with, if the type is `team`
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
            
        Returns:
            CreateJournalResponse with journal_id and journal_url
        """
        request = CreateJournalRequest(title=title, team_slug=team_slug)
        
        response = self._client._request(
            "PUT",
            "/v1/journals/editor/create",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return CreateJournalResponse(**response)
    
    def rename(self, journal_id: str, title: str, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> RenameJournalResponse:
        """
        Rename a journal.
        
        Args:
            journal_id: ID of the journal to rename
            title: New title for the journal
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
            
        Returns:
            RenameJournalResponse with old and new titles
        """
        request = RenameJournalRequest(journal_id=journal_id, title=title)
        
        response = self._client._request(
            "PATCH",
            "/v1/journals/editor/rename",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return RenameJournalResponse(**response)

    def list(self, page_token: Optional[int] = None, extra_headers: Optional[Dict[str, str]] = None) -> JournalsResponse:
        """
        List journals with pagination.
        
        Args:
            page_token: Token for pagination
            
        Returns:
            JournalsResponse with list of journals and next page token
        """
        params = {}
        if page_token is not None:
            params["page_token"] = page_token
            
        response = self._client._request(
            "GET",
            "/v1/journals/list",
            params=params,
            extra_headers=extra_headers,
        )
        return JournalsResponse(**response)

    def content(self, journal_id: str, extra_headers: Optional[Dict[str, str]] = None) -> JournalContentResponse:
        """
        Get content of a specific journal.
        
        Args:
            journal_id: ID of the journal
            
        Returns:
            JournalContentResponse with journal content
        """
        if not journal_id:
            raise ValueError("journal_id must be provided")
        
        response = self._client._request(
            "GET",
            f"/v1/journals/content/{journal_id}",
            extra_headers=extra_headers,
        )
        return JournalContentResponse(**response)
    

class Flashcards:
    """Flashcard endpoints for Opennote API."""
    
    def __init__(self, client: "OpennoteClient"):
        self._client = client

    def create(self, set_description: str, count: int = 10, set_name: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> FlashcardCreateResponse:
        """
        Create a new flashcard set.

        Args:
            set_description: The description of the flashcard set, i.e. what you want to include in the set.
            count: The number of flashcards to generate
            set_name: The name of the flashcard set, if you want to provide one. If you do not, one will be generated for you at additional cost.

        Returns:
            FlashcardCreateResponse with success status and flashcard set name
        """
        if not set_description:
            raise ValueError("set_description must be provided")
        if not count:
            raise ValueError("count must be provided")

        request = FlashcardCreateRequest(set_description=set_description, count=count, set_name=set_name)
        response = self._client._request("POST", "/v1/interactives/flashcards/create", json=request.model_dump(exclude_none=True), extra_headers=extra_headers, extra_body=extra_body)
        return FlashcardCreateResponse(**response)


class PracticeProblemSets:
    """Practice problem set endpoints for Opennote API."""
    
    def __init__(self, client: "OpennoteClient"):
        self._client = client

    def create(self, set_description: str, count: int = 5, set_name: Optional[str] = None, search_for_problems: bool = False, webhook_url: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> PracticeProblemSetJobCreateResponse:
        """
        Create a new practice problem set.
        """
        request = PracticeProblemSetJobCreateRequest(set_description=set_description, count=count, set_name=set_name, search_for_problems=search_for_problems, webhook_url=webhook_url)
        response = self._client._request("POST", "/v1/interactives/practice/create", json=request.model_dump(exclude_none=True), extra_headers=extra_headers, extra_body=extra_body)
        return PracticeProblemSetJobCreateResponse(**response)

    def status(self, set_id: str, extra_headers: Optional[Dict[str, str]] = None) -> PracticeProblemSetStatusResponse:
        """
        Get the status of a practice problem set.
        """
        response = self._client._request("GET", f"/v1/interactives/practice/status/{set_id}", extra_headers=extra_headers)
        return PracticeProblemSetStatusResponse(**response)

    def grade(self, problem: PracticeProblem, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> GradeFRQResponse:
        """
        Grade a practice problem set.
        """
        request = GradeFRQRequest(problem=problem)
        response = self._client._request("POST", f"/v1/interactives/practice/grade", json=request.model_dump(exclude_none=True), extra_headers=extra_headers, extra_body=extra_body)
        return GradeFRQResponse(**response)


class Interactives: 
    """Interactives endpoints for Opennote API."""

    def __init__(self, client: "OpennoteClient"):
        self._client = client
        self.practice = PracticeProblemSets(client)
        self.flashcards = Flashcards(client)


class OpennoteClient(BaseClient):
    """Synchronous client for Opennote API."""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = OPENNOTE_BASE_URL,
        timeout: float = 60.0,
        max_retries: int = 3,
        default_headers: Optional[Dict[str, str]] = None,
        default_body: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(api_key, base_url, timeout, max_retries, default_headers, default_body)
        self.video = Video(self)
        self.journals = Journals(self)
        self.interactives = Interactives(self)
        self._client = None

    def __enter__(self):
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            self._client.close()

    def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> dict:
        """Make a request to the API."""
        headers = self._get_headers(extra_headers)
        
        # Merge body if provided
        if json is not None:
            json = self._merge_body(json, extra_body)
        
        if not self._client:
            # Create a client for one-off requests
            with httpx.Client(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            ) as client:
                response = client.request(method, path, json=json, params=params, **kwargs)
                return self._process_response(response)
        else:
            # Update headers for this request
            response = self._client.request(method, path, headers=headers, json=json, params=params, **kwargs)
            return self._process_response(response)

    def _health(self, extra_headers: Optional[Dict[str, str]] = None) -> Literal["OK"] | Any:
        """Check API health status."""
        headers = self._get_headers(extra_headers)
        
        if not self._client:
            # Create a client for one-off requests
            with httpx.Client(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            ) as client:
                response = client.request("GET", "/v1/health")
                response.raise_for_status()
                return response.text
        else:
            # Update headers for this request
            response = self._client.request("GET", "/v1/health", headers=headers)
            response.raise_for_status()
            return response.text


Opennote: OpennoteClient = OpennoteClient
