from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SessionContextProjection:
    projection_id: str
    session_id: str
    policy_id: str | None
    source_turn_ids: list[str]
    source_message_ids: list[str]
    rendered_messages: list[dict[str, Any]]
    total_messages: int
    total_chars: int
    truncated: bool
    truncation_reason: str | None
    created_at: str
    projection_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_id": self.projection_id,
            "session_id": self.session_id,
            "policy_id": self.policy_id,
            "source_turn_ids": list(self.source_turn_ids),
            "source_message_ids": list(self.source_message_ids),
            "rendered_messages": [dict(message) for message in self.rendered_messages],
            "total_messages": self.total_messages,
            "total_chars": self.total_chars,
            "truncated": self.truncated,
            "truncation_reason": self.truncation_reason,
            "created_at": self.created_at,
            "projection_attrs": {"canonical": False, **dict(self.projection_attrs)},
        }


@dataclass(frozen=True)
class SessionPromptRenderResult:
    render_id: str
    projection_id: str
    messages: list[dict[str, Any]]
    system_prompt_included: bool
    capability_profile_included: bool
    created_at: str
    render_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "render_id": self.render_id,
            "projection_id": self.projection_id,
            "messages": [dict(message) for message in self.messages],
            "system_prompt_included": self.system_prompt_included,
            "capability_profile_included": self.capability_profile_included,
            "created_at": self.created_at,
            "render_attrs": dict(self.render_attrs),
        }
