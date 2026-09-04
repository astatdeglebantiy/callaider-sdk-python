import pytest
from callaider import AsyncCallaider, Callaider

TEST_BASE_URL = "https://api.callaider.ai"
TEST_API_KEY = "test_api_key_12345"


@pytest.fixture
def client() -> Callaider:
    """Fixture providing a synchronous Callaider client instance."""
    return Callaider(api_key=TEST_API_KEY, base_url=TEST_BASE_URL)


@pytest.fixture
def async_client() -> AsyncCallaider:
    """Fixture providing an asynchronous Callaider client instance."""
    return AsyncCallaider(api_key=TEST_API_KEY, base_url=TEST_BASE_URL)
