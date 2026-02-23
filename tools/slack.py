"""
title: Slack Message Sender
author: lucab85
version: 0.1.0
"""

import requests
from typing import Callable, Any

from pydantic import BaseModel, Field


class EventEmitter:
    def __init__(self, event_emitter: Callable[[dict], Any] = None):
        self.event_emitter = event_emitter

    async def emit(self, description="Unknown state", status="in_progress", done=False):
        if self.event_emitter:
            await self.event_emitter(
                {
                    "type": "status",
                    "data": {
                        "status": status,
                        "description": description,
                        "done": done,
                    },
                }
            )


class Tools:
    class Valves(BaseModel):
        SLACK_WEBHOOK_URL: str = Field(
            default="",
            description="Slack Incoming Webhook URL for the target channel.",
        )

    def __init__(self):
        self.valves = self.Valves()

    async def slack_prepare_message(
        self,
        title: str = Field(..., description="Short title for the Slack message."),
        body: str = Field(..., description="Main content of the message (plain text)."),
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Prepare (but DO NOT send) a Slack message for the private channel.
        Use this to draft the message, then ask the user for confirmation before sending.

        :param title: Short title for the Slack message.
        :param body: Main content of the message (plain text).
        :param __event_emitter__: An optional callback for emitting events during processing.
        :return: Draft message for user review.
        """
        emitter = EventEmitter(__event_emitter__)

        await emitter.emit(
            description="Preparing Slack message draft.",
            status="drafting",
            done=False,
        )

        msg = f"*{title}*\n{body}"

        await emitter.emit(
            description="Draft ready for review.",
            status="draft_ready",
            done=True,
        )

        return (
            "Draft Slack message prepared for the configured private channel.\n\n"
            f"{msg}\n\n"
            "Reply with: CONFIRM to post, or REVISE with changes."
        )

    async def slack_post_private(
        self,
        text: str = Field(..., description="The exact text to post to the private Slack channel."),
        confirm: bool = Field(default=False, description="Must be True to actually post to Slack."),
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Post a message to Slack via Incoming Webhook.
        SAFETY: Posts ONLY if confirm=True, otherwise returns a draft and asks for confirmation.

        :param text: The exact text to post to the private Slack channel.
        :param confirm: Must be True to actually post to Slack.
        :param __event_emitter__: An optional callback for emitting events during processing.
        :return: Response message indicating success or failure.
        """
        emitter = EventEmitter(__event_emitter__)

        if not confirm:
            await emitter.emit(
                description="Awaiting user confirmation to post.",
                status="awaiting_confirmation",
                done=True,
            )
            return (
                "Not posting yet (confirmation required).\n\n"
                "Draft message for the configured private channel:\n"
                f"{text}\n\n"
                "Reply with: CONFIRM to post."
            )

        if not self.valves.SLACK_WEBHOOK_URL:
            await emitter.emit(
                description="Slack webhook URL not configured.",
                status="missing_configuration",
                done=True,
            )
            return "SLACK_WEBHOOK_URL is not set. Configure it in the tool's Valves settings."

        await emitter.emit(
            description="Sending message to Slack.",
            status="sending_message",
            done=False,
        )

        payload = {"text": text}

        try:
            r = requests.post(self.valves.SLACK_WEBHOOK_URL, json=payload, timeout=10)

            if r.status_code != 200:
                await emitter.emit(
                    description=f"Slack webhook error: HTTP {r.status_code}.",
                    status="send_failed",
                    done=True,
                )
                return f"Slack webhook error: HTTP {r.status_code} - {r.text}"

            await emitter.emit(
                description="Message successfully posted to Slack.",
                status="message_sent",
                done=True,
            )
            return "✅ Posted to the configured private channel."

        except requests.exceptions.RequestException as e:
            await emitter.emit(
                description=f"Slack request failed: {e}",
                status="error",
                done=True,
            )
            return f"Slack request failed: {str(e)}"

    async def slack_private_channel(
        self,
        title: str = Field(..., description="Short title for the Slack message."),
        body: str = Field(..., description="Main content."),
        user_confirmation: str = Field(default="NO", description="Must be exactly CONFIRM to post. Otherwise NO."),
        __event_emitter__: Callable[[dict], Any] = None,
    ) -> str:
        """
        Single entrypoint: draft by default; post only when user_confirmation == 'CONFIRM'.

        :param title: Short title for the Slack message.
        :param body: Main content of the message.
        :param user_confirmation: Must be exactly CONFIRM to post. Otherwise NO.
        :param __event_emitter__: An optional callback for emitting events during processing.
        :return: Draft or post result.
        """
        emitter = EventEmitter(__event_emitter__)
        msg = f"*{title}*\n{body}"

        if user_confirmation.strip() != "CONFIRM":
            await emitter.emit(
                description="Drafting Slack message (not posting).",
                status="drafting",
                done=True,
            )
            return (
                "Draft Slack message for the configured private channel (NOT posted):\n\n"
                f"{msg}\n\n"
                "Reply with exactly: CONFIRM to post."
            )

        # If confirmed, post
        return await self.slack_post_private(
            text=msg, confirm=True, __event_emitter__=__event_emitter__
        )
