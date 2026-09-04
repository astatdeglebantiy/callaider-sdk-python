from typing import Any
import httpx


class CallaiderError(Exception):
    """Base exception for all Callaider SDK errors."""
    pass


class APIError(CallaiderError):
    """Raised when the API returns an error response."""

    def __init__(
        self,
        message: str,
        *,
        request: httpx.Request | None = None,
        response: httpx.Response | None = None,
        body: Any | None = None,
    ) -> None:
        super().__init__(message)
        self.request = request
        self.response = response
        self.status_code = response.status_code if response else None
        self.body = body


class APIStatusError(APIError):
    """Raised for non-2xx HTTP status codes."""
    pass


class AuthenticationError(APIStatusError):
    """Raised for 401 Unauthorized and 403 Forbidden errors."""
    pass


class NotFoundError(APIStatusError):
    """Raised for 404 Not Found errors."""
    pass


class RateLimitError(APIStatusError):
    """Raised for 429 Too Many Requests errors."""
    pass


class InternalServerError(APIStatusError):
    """Raised for 5xx Server Errors."""
    pass


class APIConnectionError(APIError):
    """Raised when a network connection error occurs (DNS, timeout, connection drop)."""
    pass