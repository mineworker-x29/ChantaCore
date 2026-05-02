from __future__ import annotations

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class LLMSettings:
    provider: str
    base_url: str
    api_key: str
    model: str
    timeout_seconds: float = 60.0


LLMProviderSettings = LLMSettings


def _read_timeout_seconds() -> float:
    raw_value = os.getenv("CHANTA_LLM_TIMEOUT_SECONDS", "60")
    try:
        return float(raw_value)
    except ValueError:
        return 60.0


def load_llm_settings(provider: str | None = None) -> LLMSettings:
    selected = provider or os.getenv("CHANTA_LLM_PROVIDER", "lm_studio")
    timeout_seconds = _read_timeout_seconds()

    if selected == "lm_studio":
        return LLMSettings(
            provider="lm_studio",
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
            model=os.getenv("LM_STUDIO_MODEL", ""),
            timeout_seconds=timeout_seconds,
        )

    if selected == "ollama":
        return LLMSettings(
            provider="ollama",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
            model=os.getenv("OLLAMA_MODEL", ""),
            timeout_seconds=timeout_seconds,
        )

    raise ValueError(f"Unsupported LLM provider: {selected}")
