from enum import Enum
from typing import Any
from pydantic import BaseModel, ConfigDict, Field


class BaseModelStrict(BaseModel):
    """Base Pydantic model with extra field tolerance and alias support."""
    model_config = ConfigDict(extra="ignore", populate_by_name=True)


class HealthResponse(BaseModelStrict):
    """API health status response."""
    status: str = Field(default="ok")
    timestamp: str | None = None


# --- Ringing Enums & Sub-models ---

class CampaignStatus(str, Enum):
    DRAFT = "draft"
    CREATED = "created"
    IN_PROGRESS = "in_progress"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class CampaignRecipient(BaseModelStrict):
    """Single recipient details."""
    phone: str
    name: str | None = None
    variables: dict[str, Any] = Field(default_factory=dict)


class Campaign(BaseModelStrict):
    """Full campaign object representation."""
    id: str | int
    name: str | None = None
    status: str | CampaignStatus
    assistant_id: str | None = None
    total_recipients: int | None = 0
    created_at: str | None = None
    updated_at: str | None = None


class CampaignStatistics(BaseModelStrict):
    """Aggregated campaign performance statistics."""
    campaign_id: str | int
    total_calls: int = 0
    completed_calls: int = 0
    successful_calls: int = 0
    failed_calls: int = 0
    average_duration_seconds: float | None = None


class CallRecord(BaseModelStrict):
    """Single call details and outcome."""
    id: str | int
    campaign_id: str | int | None = None
    phone: str
    status: str
    duration_seconds: int | None = 0
    recording_url: str | None = None
    transcript: str | None = None
    post_analysis: dict[str, Any] | None = None
    created_at: str | None = None


class RecordingInfo(BaseModelStrict):
    """Call audio recording metadata."""
    call_id: str | int
    recording_url: str
    duration_seconds: int | None = None
    format: str = "mp3"


# --- Assistants / External Conversation Models ---

class MessageItem(BaseModelStrict):
    """Individual conversation message representation."""
    role: str = "assistant"
    content: str = ""
    timestamp: str | None = None


class ExternalConversationMessageRequest(BaseModelStrict):
    """Request payload for sending messages to an external assistant conversation."""
    message: str
    external_conversation_id: str = Field(alias="externalConversationId")
    metadata: dict[str, Any] = Field(default_factory=dict)


class ExternalConversationMessageResponse(BaseModelStrict):
    """Response returned by the AI assistant conversation bridge."""
    ok: bool = True
    status: str | None = None
    external_conversation_id: str | None = Field(default=None, alias="externalConversationId")
    reply: str | None = None
    messages: list[MessageItem] = Field(default_factory=list)
    state: dict[str, Any] = Field(default_factory=dict)

    @property
    def text(self) -> str:
        """Convenience helper to extract the main assistant reply text."""
        if self.reply:
            return self.reply
        if self.messages:
            # Return content of the latest assistant message
            for msg in reversed(self.messages):
                if msg.role == "assistant" and msg.content:
                    return msg.content
            return self.messages[-1].content
        return ""

# --- Webhook Event Models ---

class WebhookEventType(str, Enum):
    CALL_STARTED = "call.started"
    CALL_ANSWERED = "call.answered"
    CALL_COMPLETED = "call.completed"
    CALL_FAILED = "call.failed"
    CAMPAIGN_FINISHED = "campaign.finished"


class CallCompletedPayload(BaseModelStrict):
    """Payload delivered when a call is finished."""
    call_id: str | int
    campaign_id: str | int | None = None
    phone: str
    duration_seconds: int = 0
    recording_url: str | None = None
    transcript: str | None = None
    post_analysis: dict[str, Any] = Field(default_factory=dict)


class WebhookEvent(BaseModelStrict):
    """Generic incoming Callaider webhook event wrapper."""
    event: str | WebhookEventType
    timestamp: str | None = None
    data: CallCompletedPayload | dict[str, Any]
