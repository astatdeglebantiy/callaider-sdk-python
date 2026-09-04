import pytest
import respx
from httpx import Response
from callaider import AuthenticationError, Callaider, NotFoundError, RateLimitError


@respx.mock
def test_unauthorized_error(client: Callaider) -> None:
    """Test 401 Unauthorized maps to AuthenticationError."""
    respx.get("https://api.callaider.ai/v1/health").mock(
        return_value=Response(401, json={"message": "Invalid API key provided"})
    )

    with pytest.raises(AuthenticationError) as exc_info:
        client.health()

    assert exc_info.value.status_code == 401
    assert "Invalid API key" in str(exc_info.value)


@respx.mock
def test_not_found_error(client: Callaider) -> None:
    """Test 404 Not Found maps to NotFoundError."""
    respx.get("https://api.callaider.ai/v1/ringing/campaigns/999").mock(
        return_value=Response(404, json={"message": "Campaign not found"})
    )

    with pytest.raises(NotFoundError) as exc_info:
        client.ringing.get_campaign(999)

    assert exc_info.value.status_code == 404


@respx.mock
def test_rate_limit_error(client: Callaider) -> None:
    """Test 429 Too Many Requests maps to RateLimitError."""
    # Temporarily set max_retries to 0 to test immediate error raising
    client._transport.max_retries = 0
    respx.get("https://api.callaider.ai/v1/health").mock(
        return_value=Response(429, json={"message": "Rate limit exceeded"})
    )

    with pytest.raises(RateLimitError) as exc_info:
        client.health()

    assert exc_info.value.status_code == 429
