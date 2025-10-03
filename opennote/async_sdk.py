from typing import Optional, List, Dict, Any, Literal
import httpx
from opennote.types import (
    GradeFRQResponse,
    PracticeProblem,
    VideoCreateJobRequest,
    VideoCreateJobResponse,
    VideoJobStatusResponse,
    JournalsResponse,
    JournalContentResponse,
    VideoAPIRequestMessage,
    JournalDeleteResponse,
    FlashcardCreateRequest,
    FlashcardCreateResponse,
    PracticeProblemSetJobCreateRequest,
    PracticeProblemSetJobCreateResponse,
    PracticeProblemSetStatusResponse,
    GradeFRQRequest,
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


class AsyncVideo:
    """Async video endpoints for Opennote API."""
    
    def __init__(self, client: "AsyncOpennoteClient"):
        self._client = client

    async def create(
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
        Create a new video job asynchronously.
        
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
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
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

        response = await self._client._request(
            "POST",
            "/v1/video/create",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )

        return VideoCreateJobResponse(**response)

    async def status(self, video_id: str, extra_headers: Optional[Dict[str, str]] = None) -> VideoJobStatusResponse:
        """
        Get the status of a video job asynchronously.
        
        Args:
            video_id: ID of the video job
            extra_headers: Additional headers to include in the request
            
        Returns:
            VideoJobStatusResponse with status and completion details
        """
        if not video_id:
            raise ValueError("video_id must be provided")
        
        response = await self._client._request(
            "GET",
            f"/v1/video/status/{video_id}",
            extra_headers=extra_headers,
        )
        return VideoJobStatusResponse(**response)


class AsyncJournalEditor:
    """Async journal editing endpoints for the Opennote API."""

    def __init__(self, client: "AsyncOpennoteClient"):
        self._client = client

    async def import_from_markdown(self, markdown: str, title: Optional[str] = "Imported Journal", team_slug: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> ImportFromMarkdownResponse:
        """
        Import a journal from markdown content asynchronously.
        
        Args:
            markdown: The markdown content to import
            title: Optional title for the journal (default: "Imported Journal")
            team_slug: The team slug that the journal is associated with
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
            
        Returns:
            ImportFromMarkdownResponse with journal_id and journal_url
        """
        request = ImportFromMarkdownRequest(
            markdown=markdown,
            title=title,
            team_slug=team_slug
        )
        
        response = await self._client._request(
            "PUT",
            "/v1/journals/editor/import_from_markdown",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return ImportFromMarkdownResponse(**response)

    async def edit(self, journal_id: str, operations: List[EditOperation], sync_realtime_state: bool = True, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> EditJournalResponse:
        """
        Edit a journal with a list of operations asynchronously.
        
        Args:
            journal_id: ID of the journal to edit
            operations: List of edit operations to perform
            sync_realtime_state: Whether to directly update the state of the journal to all connected users. WARNING: Operations through synced states CANNOT be undone, and will remove Ctrl+Z functionality for all users for the changes made.
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
            
        Returns:
            EditJournalResponse with results for each operation
        """
        request = EditJournalRequest(
            journal_id=journal_id,
            operations=operations,
            sync_realtime_state=sync_realtime_state
        )
        
        response = await self._client._request(
            "PATCH",
            "/v1/journals/editor/edit",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return EditJournalResponse(**response)
    
    async def model_info(self, journal_id: str, extra_headers: Optional[Dict[str, str]] = None) -> ModelInfoResponse:
        """
        Get the ProseMirror model representation of a journal asynchronously.
        
        Args:
            journal_id: ID of the journal
            extra_headers: Additional headers to include in the request
            
        Returns:
            ModelInfoResponse with the JSON representation of the journal
        """
        if not journal_id:
            raise ValueError("journal_id must be provided")
        
        response = await self._client._request(
            "GET",
            f"/v1/journals/editor/model/{journal_id}",
            extra_headers=extra_headers,
        )
        return ModelInfoResponse(**response)
    
    async def delete(self, journal_id: str, extra_headers: Optional[Dict[str, str]] = None) -> JournalDeleteResponse:
        """
        Delete a journal asynchronously.
        
        Args:
            journal_id: ID of the journal to delete
            extra_headers: Additional headers to include in the request
            
        Returns:
            JournalDeleteResponse confirming deletion
        """
        if not journal_id:
            raise ValueError("journal_id must be provided")
        
        response = await self._client._request(
            "DELETE",
            f"/v1/journals/editor/delete/{journal_id}",
            extra_headers=extra_headers,
        )
        return JournalDeleteResponse(**response)


class AsyncJournals:
    """Async journal endpoints for Opennote API."""
    
    def __init__(self, client: "AsyncOpennoteClient"):
        self._client = client
        self.editor = AsyncJournalEditor(client)

    async def create(self, title: str, team_slug: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> CreateJournalResponse:
        """
        Create a new journal asynchronously.
        
        Args:
            title: The title of the journal
            team_slug: The team slug that the journal is associated with, if the type is `team`
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
            
        Returns:
            CreateJournalResponse with journal_id and journal_url
        """
        request = CreateJournalRequest(title=title, team_slug=team_slug)
        
        response = await self._client._request(
            "PUT",
            "/v1/journals/editor/create",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return CreateJournalResponse(**response)
    
    async def rename(self, journal_id: str, title: str, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> RenameJournalResponse:
        """
        Rename a journal asynchronously.
        
        Args:
            journal_id: ID of the journal to rename
            title: New title for the journal
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
            
        Returns:
            RenameJournalResponse with old and new titles
        """
        request = RenameJournalRequest(journal_id=journal_id, title=title)
        
        response = await self._client._request(
            "PATCH",
            "/v1/journals/editor/rename",
            json=request.model_dump(exclude_none=True),
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        return RenameJournalResponse(**response)

    async def list(self, page_token: Optional[int] = None, extra_headers: Optional[Dict[str, str]] = None) -> JournalsResponse:
        """
        List journals with pagination asynchronously.
        
        Args:
            page_token: Token for pagination
            extra_headers: Additional headers to include in the request
            
        Returns:
            JournalsResponse with list of journals and next page token
        """
        params = {}
        if page_token is not None:
            params["page_token"] = page_token
            
        response = await self._client._request(
            "GET",
            "/v1/journals/list",
            params=params,
            extra_headers=extra_headers,
        )
        return JournalsResponse(**response)

    async def content(self, journal_id: str, extra_headers: Optional[Dict[str, str]] = None) -> JournalContentResponse:
        """
        Get content of a specific journal asynchronously.
        
        Args:
            journal_id: ID of the journal
            extra_headers: Additional headers to include in the request
            
        Returns:
            JournalContentResponse with journal content
        """
        if not journal_id:
            raise ValueError("journal_id must be provided")
        
        response = await self._client._request(
            "GET",
            f"/v1/journals/content/{journal_id}",
            extra_headers=extra_headers,
        )
        return JournalContentResponse(**response)


class AsyncFlashcards:
    """Async flashcard endpoints for Opennote API."""
    
    def __init__(self, client: "AsyncOpennoteClient"):
        self._client = client


    async def create(self, set_description: str, count: int = 10, set_name: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> FlashcardCreateResponse:
        """
        Create a new flashcard set asynchronously.

        Args:
            set_description: The description of the flashcard set, i.e. what you want to include in the set.
            count: The number of flashcards to generate
            set_name: The name of the flashcard set, if you want to provide one. If you do not, one will be generated for you at additional cost.
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request

        Returns:
            FlashcardCreateResponse with success status and flashcard set name
        """
        if not set_description:
            raise ValueError("set_description must be provided")
        if not count:
            raise ValueError("count must be provided")

        request = FlashcardCreateRequest(set_description=set_description, count=count, set_name=set_name)
        response = await self._client._request("POST", "/v1/interactives/flashcards/create", json=request.model_dump(exclude_none=True), extra_headers=extra_headers, extra_body=extra_body)
        return FlashcardCreateResponse(**response)


class AsyncPracticeProblemSets:
    """Async practice problem set endpoints for Opennote API."""
    
    def __init__(self, client: "AsyncOpennoteClient"):
        self._client = client

    async def create(self, set_description: str, count: int = 5, set_name: Optional[str] = None, search_for_problems: bool = False, webhook_url: Optional[str] = None, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> PracticeProblemSetJobCreateResponse:
        """
        Create a new practice problem set asynchronously.
        
        Args:
            set_description: The description of the practice problem set
            count: The number of practice problems to create
            set_name: The name of the practice problem set
            search_for_problems: Whether to search the web for additional context
            webhook_url: The webhook URL to send the creation status to
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
        """
        request = PracticeProblemSetJobCreateRequest(set_description=set_description, count=count, set_name=set_name, search_for_problems=search_for_problems, webhook_url=webhook_url)
        response = await self._client._request("POST", "/v1/interactives/practice/create", json=request.model_dump(exclude_none=True), extra_headers=extra_headers, extra_body=extra_body)
        return PracticeProblemSetJobCreateResponse(**response)

    async def status(self, set_id: str, extra_headers: Optional[Dict[str, str]] = None) -> PracticeProblemSetStatusResponse:
        """
        Get the status of a practice problem set asynchronously.
        
        Args:
            set_id: The ID of the practice problem set
            extra_headers: Additional headers to include in the request
        """
        response = await self._client._request("GET", f"/v1/interactives/practice/status/{set_id}", extra_headers=extra_headers)
        return PracticeProblemSetStatusResponse(**response)

    async def grade(self, problem: PracticeProblem, extra_headers: Optional[Dict[str, str]] = None, extra_body: Optional[Dict[str, Any]] = None) -> GradeFRQResponse:
        """
        Grade a practice problem set asynchronously.
        
        Args:
            problem: The practice problem to grade
            extra_headers: Additional headers to include in the request
            extra_body: Additional body parameters to include in the request
        """
        request = GradeFRQRequest(problem=problem)
        response = await self._client._request("POST", f"/v1/interactives/practice/grade", json=request.model_dump(exclude_none=True), extra_headers=extra_headers, extra_body=extra_body)
        return GradeFRQResponse(**response)


class AsyncInteractives: 
    """Async interactives endpoints for Opennote API."""

    def __init__(self, client: "AsyncOpennoteClient"):
        self._client = client
        self.practice = AsyncPracticeProblemSets(client)
        self.flashcards = AsyncFlashcards(client)


class AsyncOpennoteClient(BaseClient):
    """Asynchronous client for Opennote API."""
    
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
        self.video = AsyncVideo(self)
        self.journals = AsyncJournals(self)
        self.interactives = AsyncInteractives(self)
        self._client = None

    async def __aenter__(self):
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=self._get_headers(),
            timeout=self.timeout,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._client:
            await self._client.aclose()

    async def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        extra_headers: Optional[Dict[str, str]] = None,
        extra_body: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> dict:
        """Make an async request to the API."""
        headers = self._get_headers(extra_headers)
        
        # Merge body if provided
        if json is not None:
            json = self._merge_body(json, extra_body)
        
        if not self._client:
            # Create a client for one-off requests
            async with httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            ) as client:
                response = await client.request(method, path, json=json, params=params, **kwargs)
                return self._process_response(response)
        else:
            # Update headers for this request
            response = await self._client.request(method, path, headers=headers, json=json, params=params, **kwargs)
            return self._process_response(response)

    async def _health(self, extra_headers: Optional[Dict[str, str]] = None) -> Literal["OK"] | Any:
        """Check API health status asynchronously."""
        headers = self._get_headers(extra_headers)
        
        if not self._client:
            # Create a client for one-off requests
            async with httpx.AsyncClient(
                base_url=self.base_url,
                headers=headers,
                timeout=self.timeout,
            ) as client:
                response = await client.request("GET", "/v1/health")
                response.raise_for_status()
                return response.text
        else:
            # Update headers for this request
            response = await self._client.request("GET", "/v1/health", headers=headers)
            response.raise_for_status()
            return response.text


AsyncOpennote: AsyncOpennoteClient = AsyncOpennoteClient