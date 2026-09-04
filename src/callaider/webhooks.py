import json
from typing import Any, Union
from callaider._models import WebhookEvent
from callaider.exceptions import CallaiderError


class WebhookParsingError(CallaiderError):
    """Raised when an incoming webhook payload cannot be parsed."""
    pass


class Webhooks:
    """Helper utilities for parsing and verifying Callaider webhooks."""

    @staticmethod
    def construct_event(
        payload: Union[str, bytes, dict[str, Any]],
        *,
        secret: str | None = None,  # Reserved for signature verification if HMAC is used
    ) -> WebhookEvent:
        """Parse raw incoming HTTP payload into a strongly-typed WebhookEvent.

        :param payload: Raw request body (bytes, str or parsed dict).
        :param secret: Optional webhook signing secret.
        :raises WebhookParsingError: If payload is invalid JSON or does not match schema.
        :return: Validated WebhookEvent object.
        """
        try:
            if isinstance(payload, (bytes, bytearray)):
                data = json.loads(payload.decode("utf-8"))
            elif isinstance(payload, str):
                data = json.loads(payload)
            elif isinstance(payload, dict):
                data = payload
            else:
                raise WebhookParsingError(f"Unsupported payload type: {type(payload)}")

            return WebhookEvent.model_validate(data)
        except Exception as exc:
            raise WebhookParsingError(f"Failed to parse webhook event: {exc}") from exc
