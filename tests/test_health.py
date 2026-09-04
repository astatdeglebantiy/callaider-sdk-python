import pytest
import respx
from httpx import Response
from callaider import AsyncCallaider, Callaider


@respx.mock
def test_health_sync(client: Callaider) -> None:
    """Test synchronous health check endpoint."""
    respx.get("https://api.callaider.ai/v1/health").mock(
        return_value=Response(200, json={"status": "ok", "timestamp": "2026-09-04T12:00:00Z"})
    )

    response = client.health()
    assert response.status == "ok"
    assert response.timestamp == "2026-09-04T12:00:00Z"


@pytest.mark.asyncio
@respx.mock
async def test_health_async(async_client: AsyncCallaider) -> None:
    """Test asynchronous health check endpoint."""
    respx.get("https://api.callaider.ai/v1/health").mock(
        return_value=Response(200, json={"status": "ok", "timestamp": "2026-09-04T12:00:00Z"})
    )

    response = await async_client.health()
    assert response.status == "ok"
    await async_client.close()
