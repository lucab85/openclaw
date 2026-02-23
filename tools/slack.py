import os
import requests
from pydantic import Field

class Tools:
    def __init__(self):
        pass

    def slack_prepare_message(
        self,
        title: str = Field(..., description="Short title for the Slack message."),
        body: str = Field(..., description="Main content of the message (plain text)."),
    ) -> str:
        """
        Prepare (but DO NOT send) a Slack message for the private channel.
        Use this to draft the message, then ask the user for confirmation before sending.
        """
        msg = f"*{title}*\n{body}"
        return (
            "Draft Slack message prepared for #openclaw-private.\n\n"
            f"{msg}\n\n"
            "Reply with: CONFIRM to post, or REVISE with changes."
        )

    def slack_post_private(
        self,
        text: str = Field(..., description="The exact text to post to the private Slack channel."),
        confirm: bool = Field(False, description="Must be True to actually post to Slack."),
    ) -> str:
        """
        Post a message to Slack via Incoming Webhook.
        SAFETY: Posts ONLY if confirm=True, otherwise returns a draft and asks for confirmation.
        """
        if not confirm:
            return (
                "Not posting yet (confirmation required).\n\n"
                "Draft message for #openclaw-private:\n"
                f"{text}\n\n"
                "Reply with: CONFIRM to post."
            )

        webhook = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook:
            return "SLACK_WEBHOOK_URL is not set. Add it to your container environment and restart."

        payload = {"text": text}

        try:
            r = requests.post(webhook, json=payload, timeout=10)
            if r.status_code != 200:
                return f"Slack webhook error: HTTP {r.status_code} - {r.text}"
            return "✅ Posted to #openclaw-private."
        except Exception as e:
            return f"Slack request failed: {str(e)}"
