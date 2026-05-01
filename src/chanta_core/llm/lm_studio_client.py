from __future__ import annotations

import json
import urllib.error
import urllib.request

from chanta_core.llm.types import ChatRequest, ChatResponse
from chanta_core.settings.llm_settings import LLMSettings


class OpenAICompatibleClient:
    def __init__(self, settings: LLMSettings) -> None:
        if not settings.model:
            raise ValueError("LM_STUDIO_MODEL must be set")
        self._settings = settings

    def chat(self, request: ChatRequest) -> ChatResponse:
        payload = request.as_payload(model=self._settings.model)
        url = f"{self._settings.base_url.rstrip('/')}/chat/completions"
        raw_request = urllib.request.Request(
            url=url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._settings.api_key}",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(raw_request, timeout=self._settings.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            details = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"request failed with status {exc.code}: {details}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"failed to reach endpoint {url}: {exc.reason}") from exc

        parsed = json.loads(body)
        return ChatResponse(text=self._extract_text(parsed), raw=parsed)

    @staticmethod
    def _extract_text(payload: dict) -> str:
        choices = payload.get("choices")
        if not choices:
            raise RuntimeError("response did not contain choices")

        message = choices[0].get("message", {})
        content = message.get("content")
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            text_parts: list[str] = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(str(item.get("text", "")))
            combined = "".join(text_parts).strip()
            if combined:
                return combined
        raise RuntimeError("response did not contain text content")
