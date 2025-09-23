"""Base client for Opennote API with authentication and request handling."""

from typing import Dict, Any, Optional
from httpx import Response, HTTPStatusError
from os import getenv
from opennote.types import OPENNOTE_BASE_URL


class OpennoteAPIError(Exception):
    """Base exception for Opennote API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Response] = None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response


class AuthenticationError(OpennoteAPIError):
    """Raised when authentication fails (401)."""
    pass


class InsufficientCreditsError(OpennoteAPIError):
    """Raised when user has insufficient credits (402)."""
    pass


class ValidationError(OpennoteAPIError):
    """Raised when request validation fails (422)."""
    pass


class RateLimitError(OpennoteAPIError):
    """Raised when rate limit is exceeded (429)."""
    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(OpennoteAPIError):
    """Raised when server encounters an error (500)."""
    pass


class BaseClient:
    """Base client with common functionality for sync and async clients."""
    
    def __init__(
        self,
        api_key: str,
        base_url: str = OPENNOTE_BASE_URL,
        timeout: float = 30.0,
        max_retries: int = 3,
        default_headers: Optional[Dict[str, str]] = None,
        default_body: Optional[Dict[str, Any]] = None,
    ):
        if not api_key:
            api_key = getenv("OPENNOTE_API_KEY")
            if not api_key:
                raise ValueError("OPENNOTE_API_KEY is not set")

        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.default_headers = default_headers or {}
        self.default_body = default_body or {}
        
    def _get_headers(self, extra_headers: Optional[Dict[str, str]] = None) -> Dict[str, str]:
        """Get common headers for all requests."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        headers.update(self.default_headers)
        if extra_headers:
            headers.update(extra_headers)
        return headers
    
    def _merge_body(self, body: Dict[str, Any], extra_body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Merge request body with default and extra body parameters."""
        merged = {}
        merged.update(self.default_body)
        merged.update(body)
        if extra_body:
            merged.update(extra_body)
        return merged
    
    def _handle_response_errors(self, response: Response) -> None:
        """Handle HTTP errors and raise appropriate exceptions."""
        if response.status_code == 401:
            raise AuthenticationError(
                "Invalid API key or unauthorized access",
                status_code=401,
                response=response
            )
        elif response.status_code == 402:
            raise InsufficientCreditsError(
                "Insufficient credits",
                status_code=402,
                response=response
            )
        elif response.status_code == 422:
            try:
                error_detail = response.json()
                message = f"Validation error: {error_detail}"
            except:
                message = "Validation error"
            raise ValidationError(
                message,
                status_code=422,
                response=response
            )
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            retry_after_int = int(retry_after) if retry_after else None
            raise RateLimitError(
                "Rate limit exceeded",
                retry_after=retry_after_int,
                status_code=429,
                response=response
            )
        elif response.status_code == 500:
            raise ServerError(
                "Internal server error",
                status_code=500,
                response=response
            )
        elif response.status_code >= 400:
            raise OpennoteAPIError(
                f"API error: {response.status_code}",
                status_code=response.status_code,
                response=response
            )
    
    def _process_response(self, response: Response) -> Dict[str, Any]:
        """Process response and handle errors."""
        try:
            response.raise_for_status()
        except HTTPStatusError:
            self._handle_response_errors(response)
        
        return response.json()