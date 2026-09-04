from typing import Any, TYPE_CHECKING
from callaider._models import (
    ExternalConversationMessageRequest,
    ExternalConversationMessageResponse,
)

if TYPE_CHECKING:
    from callaider._client import AsyncCallaider, Callaider


class AssistantsResource:
    """Synchronous interface for conversational assistants and bridge integrations."""

    def __init__(self, client: "Callaider") -> None:
        self._client = client

    def send_message(
        self,
        assistant_id: str | int,
        *,
        message: str,
        external_conversation_id: str = "conv_default_123",
        metadata: dict[str, Any] | None = None,
    ) -> ExternalConversationMessageResponse:
        """Send a message to an AI assistant and receive a contextual response.

        :param assistant_id: Unique identifier of the assistant.
        :param message: Text prompt/message from the user.
        :param external_conversation_id: External session ID for conversation state.
        :param metadata: Optional metadata dictionary.
        """
        request_model = ExternalConversationMessageRequest(
            message=message,
            externalConversationId=external_conversation_id,
            metadata=metadata or {},
        )

        data = self._client._transport.request(
            "POST",
            f"/v1/assistants/{assistant_id}/external-conversations/messages",
            json_data=request_model.model_dump(by_alias=True, exclude_none=True),
        )
        return ExternalConversationMessageResponse.model_validate(data)

    def get_conversation_state(
        self,
        assistant_id: str | int,
        external_conversation_id: str,
    ) -> dict[str, Any]:
        """Retrieve conversation state by external conversation ID."""
        data = self._client._transport.request(
            "GET",
            f"/v1/assistants/{assistant_id}/external-conversations/{external_conversation_id}/state",
        )
        return data or {}


class AsyncAssistantsResource:
    """Asynchronous interface for conversational assistants and bridge integrations."""

    def __init__(self, client: "AsyncCallaider") -> None:
        self._client = client

    async def send_message(
        self,
        assistant_id: str | int,
        *,
        message: str,
        external_conversation_id: str = "conv_default_123",
        metadata: dict[str, Any] | None = None,
    ) -> ExternalConversationMessageResponse:
        """Send a message to an AI assistant asynchronously."""
        request_model = ExternalConversationMessageRequest(
            message=message,
            externalConversationId=external_conversation_id,
            metadata=metadata or {},
        )

        data = await self._client._transport.request(
            "POST",
            f"/v1/assistants/{assistant_id}/external-conversations/messages",
            json_data=request_model.model_dump(by_alias=True, exclude_none=True),
        )
        return ExternalConversationMessageResponse.model_validate(data)

    async def get_conversation_state(
        self,
        assistant_id: str | int,
        external_conversation_id: str,
    ) -> dict[str, Any]:
        """Retrieve conversation state asynchronously."""
        data = await self._client._transport.request(
            "GET",
            f"/v1/assistants/{assistant_id}/external-conversations/{external_conversation_id}/state",
        )
        return data or {}
