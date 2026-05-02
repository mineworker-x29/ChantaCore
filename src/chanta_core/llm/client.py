from openai import OpenAI

from chanta_core.llm.messages import build_messages
from chanta_core.llm.types import ChatMessage
from chanta_core.settings.llm_settings import LLMProviderSettings, load_llm_settings


class LLMClient:
    def __init__(self, settings: LLMProviderSettings | None = None):
        self.settings = settings or load_llm_settings()

        if not self.settings.model:
            raise ValueError(
                f"Model is not configured for provider: {self.settings.provider}"
            )

        self.client = OpenAI(
            base_url=self.settings.base_url,
            api_key=self.settings.api_key,
            timeout=self.settings.timeout_seconds,
        )

    def chat(
        self,
        user_message: str,
        system_message: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        return self.chat_messages(
            messages=build_messages(
                user_message=user_message,
                system_message=system_message,
            ),
            temperature=temperature,
            max_tokens=max_tokens,
        )

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        response = self.client.chat.completions.create(
            model=self.settings.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )

        return response.choices[0].message.content or ""


def create_llm_client(settings: LLMProviderSettings | None = None) -> LLMClient:
    return LLMClient(settings=settings)
