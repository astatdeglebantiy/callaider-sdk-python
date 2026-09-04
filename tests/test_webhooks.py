import pytest
from callaider import WebhookParsingError, Webhooks


def test_parse_valid_webhook() -> None:
    """Test valid JSON payload parsing."""
    raw_payload = """
    {
        "event": "call.completed",
        "timestamp": "2026-09-04T12:00:00Z",
        "data": {
            "call_id": 999,
            "phone": "+380501112233",
            "duration_seconds": 120,
            "recording_url": "https://storage.callaider.ai/rec.mp3"
        }
    }
    """
    event = Webhooks.construct_event(raw_payload)
    assert event.event == "call.completed"
    assert event.data.call_id == 999
    assert event.data.duration_seconds == 120


def test_parse_invalid_webhook_json() -> None:
    """Test malformed JSON raises WebhookParsingError."""
    invalid_json = "NOT_A_JSON_STRING"

    with pytest.raises(WebhookParsingError):
        Webhooks.construct_event(invalid_json)
