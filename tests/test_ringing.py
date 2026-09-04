import respx
from httpx import Response
from callaider import Callaider
from callaider._models import CampaignRecipient


@respx.mock
def test_list_campaigns(client: Callaider) -> None:
    """Test fetching campaign list."""
    mock_payload = [
        {"id": 1, "name": "Spring 2026 Campaign", "status": "created", "total_recipients": 10}
    ]
    respx.get("https://api.callaider.ai/v1/ringing/campaigns").mock(
        return_value=Response(200, json=mock_payload)
    )

    campaigns = client.ringing.list_campaigns()
    assert len(campaigns) == 1
    assert campaigns[0].id == 1
    assert campaigns[0].name == "Spring 2026 Campaign"


@respx.mock
def test_create_campaign(client: Callaider) -> None:
    """Test campaign creation."""
    respx.post("https://api.callaider.ai/v1/ringing/campaigns").mock(
        return_value=Response(
            201,
            json={"id": 42, "name": "VIP Outreach", "status": "created", "total_recipients": 1},
        )
    )

    recipients = [CampaignRecipient(phone="+380501234567", name="Alex")]
    campaign = client.ringing.create_campaign(
        assistant_id="asst_sales_01",
        recipients=recipients,
        name="VIP Outreach",
    )
    assert campaign.id == 42
    assert campaign.status == "created"
