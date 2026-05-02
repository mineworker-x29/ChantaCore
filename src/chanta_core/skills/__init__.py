"""Skill package exports.

Imports are resolved lazily so canonical OCEL modules can import
``chanta_core.skills.skill`` without pulling in runtime dispatch dependencies.
"""

from __future__ import annotations

from importlib import import_module
from typing import Any

__all__ = [
    "Skill",
    "SkillExecutionContext",
    "SkillExecutionResult",
    "SkillExecutionPolicy",
    "SkillExecutor",
    "SkillRegistryError",
    "SkillValidationError",
    "SkillRegistry",
    "builtin_llm_chat_skill",
    "create_echo_skill",
    "create_inspect_ocel_recent_skill",
    "create_llm_chat_skill",
    "create_summarize_process_trace_skill",
    "create_summarize_text_skill",
]


def __getattr__(name: str) -> Any:
    if name == "Skill":
        return import_module("chanta_core.skills.skill").Skill
    if name == "SkillExecutionContext":
        return import_module("chanta_core.skills.context").SkillExecutionContext
    if name == "SkillExecutionResult":
        return import_module("chanta_core.skills.result").SkillExecutionResult
    if name == "SkillExecutionPolicy":
        return import_module("chanta_core.skills.executor").SkillExecutionPolicy
    if name == "SkillExecutor":
        return import_module("chanta_core.skills.executor").SkillExecutor
    if name in {"SkillRegistryError", "SkillValidationError"}:
        errors = import_module("chanta_core.skills.errors")
        return getattr(errors, name)
    if name == "SkillRegistry":
        return import_module("chanta_core.skills.registry").SkillRegistry
    if name in {
        "builtin_llm_chat_skill",
        "create_echo_skill",
        "create_inspect_ocel_recent_skill",
        "create_llm_chat_skill",
        "create_summarize_process_trace_skill",
        "create_summarize_text_skill",
    }:
        builtin = import_module("chanta_core.skills.builtin")
        return getattr(builtin, name)
    raise AttributeError(name)
