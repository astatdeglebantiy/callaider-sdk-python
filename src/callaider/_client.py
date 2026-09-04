import os
from typing import Mapping
from callaider._base_client import AsyncHttpxClientWrapper, SyncHttpxClientWrapper
from callaider.resources.assistants import AssistantsResource, AsyncAssistantsResource
from callaider._constants import DEFAULT_BASE_URL, DEFAULT_MAX_RETRIES, DEFAULT_TIMEOUT
from callaider._models import HealthResponse
from callaider.resources.ringing import AsyncRingingResource, RingingResource


class Callaider:
    """Synchronous client for the Callaider API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
    ) -> None:
        resolved_key = api_key or os.getenv("CALLAIDER_API_KEY")
        if not resolved_key:
            raise ValueError(
                "Missing API key. Pass `api_key` explicitly or set the `CALLAIDER_API_KEY` environment variable."
            )

        self._transport = SyncHttpxClientWrapper(
            base_url=base_url,
            api_key=resolved_key,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=default_headers,
        )

        # Resource namespaces
        self.ringing = RingingResource(self)
        self.assistants = AssistantsResource(self)

    def health(self) -> HealthResponse:
        """Check API service health status."""
        data = self._transport.request("GET", "/v1/health")
        return HealthResponse.model_validate(data or {})

    def close(self) -> None:
        """Close the active client session."""
        self._transport.close()

    def __enter__(self) -> "Callaider":
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


class AsyncCallaider:
    """Asynchronous client for the Callaider API."""

    def __init__(
        self,
        *,
        api_key: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
    ) -> None:
        resolved_key = api_key or os.getenv("CALLAIDER_API_KEY")
        if not resolved_key:
            raise ValueError(
                "Missing API key. Pass `api_key` explicitly or set the `CALLAIDER_API_KEY` environment variable."
            )

        self._transport = AsyncHttpxClientWrapper(
            base_url=base_url,
            api_key=resolved_key,
            timeout=timeout,
            max_retries=max_retries,
            custom_headers=default_headers,
        )

        # Resource namespaces
        self.ringing = AsyncRingingResource(self)
        self.assistants = AsyncAssistantsResource(self)

    async def health(self) -> HealthResponse:
        """Check API service health status asynchronously."""
        data = await self._transport.request("GET", "/v1/health")
        return HealthResponse.model_validate(data or {})

    async def close(self) -> None:
        """Close the active client session asynchronously."""
        await self._transport.close()

    async def __aenter__(self) -> "AsyncCallaider":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()
