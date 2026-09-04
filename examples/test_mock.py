import asyncio
from callaider import AsyncCallaider, Callaider, Webhooks

MOCK_SERVER_URL = "http://127.0.0.1:4010"
API_KEY = "test_token"


def test_sync():
    print("=== Testing Sync Client ===")
    client = Callaider(api_key=API_KEY, base_url=MOCK_SERVER_URL)

    # 1. Health
    health = client.health()
    print("Health:", health.status)

    # 2. Campaigns
    campaigns = client.ringing.list_campaigns()
    print("Campaigns count:", len(campaigns))

    # 3. Assistants message
    assistant_reply = client.assistants.send_message(
        assistant_id=1,
        external_conversation_id="telegram_chat_987654",
        message="Hello AI, this is a test message!",
    )
    print("Assistant Full Response:", assistant_reply)
    print("Assistant Text Reply:", assistant_reply.text)


async def test_async():
    print("\n=== Testing Async Client ===")
    async with AsyncCallaider(api_key=API_KEY, base_url=MOCK_SERVER_URL) as client:
        health = await client.health()
        print("Async Health:", health.status)


def test_webhooks():
    print("\n=== Testing Webhooks Parser ===")
    raw_payload = """
    {
        "event": "call.completed",
        "timestamp": "2026-09-04T12:00:00Z",
        "data": {
            "call_id": 12345,
            "phone": "+380501234567",
            "duration_seconds": 45,
            "recording_url": "https://storage.callaider.ai/recordings/12345.mp3"
        }
    }
    """
    event = Webhooks.construct_event(raw_payload)
    print(f"Parsed Event: {event.event} for call #{event.data.call_id}")


if __name__ == "__main__":
    test_sync()
    asyncio.run(test_async())
    test_webhooks()
