import asyncio
import logging
import time
from typing import Any, Mapping
import httpx

from callaider._constants import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT, RAW_USER_AGENT
from callaider.exceptions import (
    APIConnectionError,
    APIStatusError,
    AuthenticationError,
    InternalServerError,
    NotFoundError,
    RateLimitError,
)

logger = logging.getLogger("callaider")


def _make_status_error(
    response: httpx.Response,
    body: Any,
) -> APIStatusError:
    """Map HTTP status codes to specific exception types."""
    status_code = response.status_code
    message = f"Error code: {status_code}"
    if isinstance(body, dict):
        message = body.get("message") or body.get("detail") or str(body)
    elif isinstance(body, str) and body:
        message = body

    if status_code in (401, 403):
        return AuthenticationError(message, response=response, body=body)
    if status_code == 404:
        return NotFoundError(message, response=response, body=body)
    if status_code == 429:
        return RateLimitError(message, response=response, body=body)
    if status_code >= 500:
        return InternalServerError(message, response=response, body=body)
    return APIStatusError(message, response=response, body=body)


class SyncHttpxClientWrapper:
    """Synchronous HTTP transport layer with automatic retry logic."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        custom_headers: Mapping[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries

        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": RAW_USER_AGENT,
            "Accept": "application/json",
            **(custom_headers or {}),
        }
        self._client = httpx.Client(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_data: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        """Execute a synchronous HTTP request with exponential backoff retries."""
        retries = self.max_retries
        delay = 0.5

        for attempt in range(retries + 1):
            try:
                response = self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json_data,
                    headers=headers,
                )
                if response.is_success:
                    return response.json() if response.content else None

                # Attempt to parse response body for error messaging
                try:
                    body = response.json()
                except Exception:
                    body = response.text

                # Retry on rate limits, timeouts, and server errors
                if response.status_code in (408, 429, 500, 502, 503, 504) and attempt < retries:
                    logger.warning(
                        "Retrying request (%d/%d) due to status %d...",
                        attempt + 1,
                        retries,
                        response.status_code,
                    )
                    time.sleep(delay)
                    delay *= 2
                    continue

                raise _make_status_error(response, body)

            except httpx.RequestError as exc:
                if attempt < retries:
                    logger.warning(
                        "Retrying request (%d/%d) due to network error: %s",
                        attempt + 1,
                        retries,
                        exc,
                    )
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise APIConnectionError(f"Connection error: {exc}") from exc

    def close(self) -> None:
        """Close the underlying HTTP client session."""
        self._client.close()


class AsyncHttpxClientWrapper:
    """Asynchronous HTTP transport layer with automatic retry logic."""

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        api_key: str | None = None,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        custom_headers: Mapping[str, str] | None = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries

        headers = {
            "Authorization": f"Bearer {api_key}",
            "User-Agent": RAW_USER_AGENT,
            "Accept": "application/json",
            **(custom_headers or {}),
        }
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            headers=headers,
            timeout=timeout,
        )

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json_data: Any | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Any:
        """Execute an asynchronous HTTP request with exponential backoff retries."""
        retries = self.max_retries
        delay = 0.5

        for attempt in range(retries + 1):
            try:
                response = await self._client.request(
                    method=method,
                    url=path,
                    params=params,
                    json=json_data,
                    headers=headers,
                )
                if response.is_success:
                    return response.json() if response.content else None

                try:
                    body = response.json()
                except Exception:
                    body = response.text

                if response.status_code in (408, 429, 500, 502, 503, 504) and attempt < retries:
                    logger.warning(
                        "Retrying request (%d/%d) due to status %d...",
                        attempt + 1,
                        retries,
                        response.status_code,
                    )
                    await asyncio.sleep(delay)
                    delay *= 2
                    continue

                raise _make_status_error(response, body)

            except httpx.RequestError as exc:
                if attempt < retries:
                    logger.warning(
                        "Retrying request (%d/%d) due to network error: %s",
                        attempt + 1,
                        retries,
                        exc,
                    )
                    await asyncio.sleep(delay)
                    delay *= 2
                    continue
                raise APIConnectionError(f"Connection error: {exc}") from exc

    async def close(self) -> None:
        """Close the underlying async HTTP client session."""
        await self._client.aclose()
