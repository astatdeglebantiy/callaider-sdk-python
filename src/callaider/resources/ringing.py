from typing import Any, TYPE_CHECKING
from callaider._models import (
    Campaign,
    CampaignRecipient,
    CampaignStatistics,
    CallRecord,
    RecordingInfo,
)

if TYPE_CHECKING:
    from callaider._client import AsyncCallaider, Callaider


class RingingResource:
    """Synchronous client interface for the Ringing (outbound calls) module."""

    def __init__(self, client: "Callaider") -> None:
        self._client = client

    def list_campaigns(self) -> list[Campaign]:
        """Fetch all outbound campaigns."""
        data = self._client._transport.request("GET", "/v1/ringing/campaigns")
        items = data if isinstance(data, list) else data.get("data", [])
        return [Campaign.model_validate(c) for c in items]

    def create_campaign(
        self,
        *,
        assistant_id: str,
        recipients: list[CampaignRecipient | dict[str, Any]],
        name: str | None = None,
    ) -> Campaign:
        """Create a new outbound call campaign."""
        parsed_recipients = [
            r.model_dump() if isinstance(r, CampaignRecipient) else r
            for r in recipients
        ]
        payload: dict[str, Any] = {
            "assistant_id": assistant_id,
            "recipients": parsed_recipients,
        }
        if name:
            payload["name"] = name

        data = self._client._transport.request("POST", "/v1/ringing/campaigns", json_data=payload)
        return Campaign.model_validate(data)

    def get_campaign(self, campaign_id: str | int) -> Campaign:
        """Retrieve details of a specific campaign."""
        data = self._client._transport.request("GET", f"/v1/ringing/campaigns/{campaign_id}")
        return Campaign.model_validate(data)

    def delete_campaign(self, campaign_id: str | int) -> None:
        """Delete a campaign by ID."""
        self._client._transport.request("DELETE", f"/v1/ringing/campaigns/{campaign_id}")

    def launch_campaign(self, campaign_id: str | int) -> Campaign:
        """Start or schedule execution of a campaign."""
        data = self._client._transport.request("POST", f"/v1/ringing/campaigns/{campaign_id}/launch")
        return Campaign.model_validate(data)

    def pause_campaign(self, campaign_id: str | int) -> Campaign:
        """Pause an active campaign."""
        data = self._client._transport.request("POST", f"/v1/ringing/campaigns/{campaign_id}/pause")
        return Campaign.model_validate(data)

    def resume_campaign(self, campaign_id: str | int) -> Campaign:
        """Resume a paused campaign."""
        data = self._client._transport.request("POST", f"/v1/ringing/campaigns/{campaign_id}/resume")
        return Campaign.model_validate(data)

    def get_campaign_statistics(self, campaign_id: str | int) -> CampaignStatistics:
        """Retrieve aggregated statistics for a specific campaign."""
        data = self._client._transport.request("GET", f"/v1/ringing/campaigns/{campaign_id}/statistics")
        return CampaignStatistics.model_validate(data)

    def list_campaign_calls(self, campaign_id: str | int) -> list[CallRecord]:
        """Fetch all call records belonging to a campaign."""
        data = self._client._transport.request("GET", f"/v1/ringing/campaigns/{campaign_id}/calls")
        items = data if isinstance(data, list) else data.get("data", [])
        return [CallRecord.model_validate(item) for item in items]

    def get_call(self, call_id: str | int) -> CallRecord:
        """Retrieve details of an individual call record."""
        data = self._client._transport.request("GET", f"/v1/ringing/calls/{call_id}")
        return CallRecord.model_validate(data)

    def get_call_recording(self, call_id: str | int) -> RecordingInfo:
        """Retrieve the audio recording link and metadata for a specific call."""
        data = self._client._transport.request("GET", f"/v1/ringing/calls/{call_id}/recording")
        return RecordingInfo.model_validate(data)


class AsyncRingingResource:
    """Asynchronous client interface for the Ringing (outbound calls) module."""

    def __init__(self, client: "AsyncCallaider") -> None:
        self._client = client

    async def list_campaigns(self) -> list[Campaign]:
        """Fetch all outbound campaigns asynchronously."""
        data = await self._client._transport.request("GET", "/v1/ringing/campaigns")
        items = data if isinstance(data, list) else data.get("data", [])
        return [Campaign.model_validate(c) for c in items]

    async def create_campaign(
        self,
        *,
        assistant_id: str,
        recipients: list[CampaignRecipient | dict[str, Any]],
        name: str | None = None,
    ) -> Campaign:
        """Create a new outbound call campaign asynchronously."""
        parsed_recipients = [
            r.model_dump() if isinstance(r, CampaignRecipient) else r
            for r in recipients
        ]
        payload: dict[str, Any] = {
            "assistant_id": assistant_id,
            "recipients": parsed_recipients,
        }
        if name:
            payload["name"] = name

        data = await self._client._transport.request("POST", "/v1/ringing/campaigns", json_data=payload)
        return Campaign.model_validate(data)

    async def get_campaign(self, campaign_id: str | int) -> Campaign:
        """Retrieve details of a specific campaign asynchronously."""
        data = await self._client._transport.request("GET", f"/v1/ringing/campaigns/{campaign_id}")
        return Campaign.model_validate(data)

    async def delete_campaign(self, campaign_id: str | int) -> None:
        """Delete a campaign by ID asynchronously."""
        await self._client._transport.request("DELETE", f"/v1/ringing/campaigns/{campaign_id}")

    async def launch_campaign(self, campaign_id: str | int) -> Campaign:
        """Start or schedule execution of a campaign asynchronously."""
        data = await self._client._transport.request("POST", f"/v1/ringing/campaigns/{campaign_id}/launch")
        return Campaign.model_validate(data)

    async def pause_campaign(self, campaign_id: str | int) -> Campaign:
        """Pause an active campaign asynchronously."""
        data = await self._client._transport.request("POST", f"/v1/ringing/campaigns/{campaign_id}/pause")
        return Campaign.model_validate(data)

    async def resume_campaign(self, campaign_id: str | int) -> Campaign:
        """Resume a paused campaign asynchronously."""
        data = await self._client._transport.request("POST", f"/v1/ringing/campaigns/{campaign_id}/resume")
        return Campaign.model_validate(data)

    async def get_campaign_statistics(self, campaign_id: str | int) -> CampaignStatistics:
        """Retrieve aggregated statistics for a specific campaign asynchronously."""
        data = await self._client._transport.request("GET", f"/v1/ringing/campaigns/{campaign_id}/statistics")
        return CampaignStatistics.model_validate(data)

    async def list_campaign_calls(self, campaign_id: str | int) -> list[CallRecord]:
        """Fetch all call records belonging to a campaign asynchronously."""
        data = await self._client._transport.request("GET", f"/v1/ringing/campaigns/{campaign_id}/calls")
        items = data if isinstance(data, list) else data.get("data", [])
        return [CallRecord.model_validate(item) for item in items]

    async def get_call(self, call_id: str | int) -> CallRecord:
        """Retrieve details of an individual call record asynchronously."""
        data = await self._client._transport.request("GET", f"/v1/ringing/calls/{call_id}")
        return CallRecord.model_validate(data)

    async def get_call_recording(self, call_id: str | int) -> RecordingInfo:
        """Retrieve the audio recording link and metadata for a specific call asynchronously."""
        data = await self._client._transport.request("GET", f"/v1/ringing/calls/{call_id}/recording")
        return RecordingInfo.model_validate(data)
