from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from chanta_core.settings.llm_settings import LLMSettings, load_llm_settings


@dataclass(frozen=True)
class AppSettings:
    env_file: str | None
    llm: LLMSettings


def load_app_settings() -> AppSettings:
    env_file = _load_env_file()
    return AppSettings(
        env_file=str(env_file) if env_file else None,
        llm=load_llm_settings(),
    )


def _load_env_file() -> Path | None:
    for candidate in (Path.cwd() / ".env", Path.cwd() / ".env.local"):
        if candidate.is_file():
            _apply_env_file(candidate)
            return candidate
    return None


def _apply_env_file(path: Path) -> None:
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
