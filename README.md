# Callaider Python SDK

[![PyPI version](https://img.shields.io/pypi/v/callaider.svg)](https://pypi.org/project/callaider/)
[![Python versions](https://img.shields.io/pypi/pyversions/callaider.svg)](https://pypi.org/project/callaider/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The official Python client library for the [Callaider](https://callaider.ai) AI voice calling and conversational platform.

Built on top of the [Callaider OpenAPI 3.0.3 specification](https://github.com/NBM-Labs/callaider_openapi).

---

## Features

- ⚡ **Sync & Async clients** built on modern `httpx`.
- 🛡️ **Fully typed** request/response models with Pydantic v2.
- 🔄 **Automatic retries** with exponential backoff on 429/5xx errors.
- 📞 **Complete Ringing API support**: Campaigns, batch calls, recordings, and statistics.
- 🤖 **External Conversation Bridge**: Direct AI assistant messaging integration (ideal for Telegram bots).
- 🪝 **Built-in Webhooks parser**: Typed events parsing for callback handling.

---

## Installation

```bash
pip install callaider
```

Or using `uv`:

```bash
uv add callaider
```

---

## Quickstart

### Synchronous Usage

```python
from callaider import Callaider

client = Callaider(api_key="your_api_key_here")

# 1. Check API status
health = client.health()
print(f"API status: {health.status}")

# 2. Create an automated call campaign
campaign = client.ringing.create_campaign(
    assistant_id="asst_sales_01",
    recipients=[
        {"phone": "+380501234567", "name": "Alex"}
    ],
    name="VIP Outreach Campaign"
)
print(f"Created campaign #{campaign.id} with status: {campaign.status}")

# 3. Launch the campaign
client.ringing.launch_campaign(campaign.id)
```

### Asynchronous Usage (FastAPI, Asyncio, Telegram Bots)

```python
import asyncio
from callaider import AsyncCallaider

async def main():
    async with AsyncCallaider(api_key="your_api_key_here") as client:
        # Send a message to AI assistant bridge
        response = await client.assistants.send_message(
            assistant_id="asst_support_01",
            external_conversation_id="telegram_user_12345",
            message="Hello! I need help with my order."
        )
        print("AI Response:", response.text)

asyncio.run(main())
```

---

## Webhooks Handling

Easily parse incoming Callaider webhook payloads in FastAPI or Flask:

```python
from fastapi import FastAPI, Request
from callaider import Webhooks

app = FastAPI()

@app.post("/webhooks/callaider")
async def handle_webhook(request: Request):
    payload = await request.body()
    event = Webhooks.construct_event(payload)

    if event.event == "call.completed":
        print(f"Call {event.data.call_id} finished. Duration: {event.data.duration_seconds}s")
        print(f"Audio recording: {event.data.recording_url}")

    return {"status": "ok"}
```

---

## Development & Testing

```bash
# Clone the repository
git clone https://github.com/astatdeglebantiy/callaider-python.git
cd callaider-python

# Install dependencies with uv
uv sync --all-extras

# Run unit tests
uv run pytest
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.