from __future__ import annotations

import os
from dataclasses import dataclass

@dataclass(frozen=True)
class LLMProviderSettings:
    provider: str
    base_url: str
    api_key: str
    model: str

def load_llm_settings(provider: str | None = None) -> LLMProviderSettings:
    selected = provider or os.getenv("CHANTA_LLM_PROVIDER", "lm_studio")

    if selected == "lm_studio":
        return LLMProviderSettings(
            provider="lm_studio",
            base_url=os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1"),
            api_key=os.getenv("LM_STUDIO_API_KEY", "lm-studio"),
            model=os.getenv("LM_STUDIO_MODEL", ""),
        )

    if selected == "ollama":
        return LLMProviderSettings(
            provider="ollama",
            base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
            api_key=os.getenv("OLLAMA_API_KEY", "ollama"),
            model=os.getenv("OLLAMA_MODEL", ""),
        )

    raise ValueError(f"Unsupported LLM provider: {selected}")