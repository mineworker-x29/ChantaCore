from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any

from chanta_core.hooks.errors import HookPolicyError, HookResultError


FORBIDDEN_HOOK_OUTCOMES = {
    "allow",
    "deny",
    "ask",
    "block",
    "rewrite",
    "mutate_input",
    "mutate_output",
}


def hash_payload(payload: Any) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def summarize_payload(payload: Any, max_chars: int = 240) -> str:
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, default=str)
    marker = "...[hook payload truncated]..."
    if len(raw) <= max_chars:
        return raw
    if len(marker) >= max_chars:
        return marker[:max_chars]
    return f"{raw[: max_chars - len(marker)]}{marker}"


@dataclass(frozen=True)
class HookDefinition:
    hook_id: str
    hook_name: str
    hook_type: str
    lifecycle_stage: str
    description: str | None
    status: str
    priority: int | None
    scope: str | None
    source_kind: str | None
    handler_ref: str | None
    created_at: str
    updated_at: str
    hook_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "hook_id": self.hook_id,
            "hook_name": self.hook_name,
            "hook_type": self.hook_type,
            "lifecycle_stage": self.lifecycle_stage,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "scope": self.scope,
            "source_kind": self.source_kind,
            "handler_ref": self.handler_ref,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "hook_attrs": self.hook_attrs,
        }


@dataclass(frozen=True)
class HookInvocation:
    invocation_id: str
    hook_id: str
    lifecycle_stage: str
    status: str
    started_at: str
    completed_at: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    triggering_event_id: str | None
    input_summary: str | None
    input_hash: str | None
    invocation_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "invocation_id": self.invocation_id,
            "hook_id": self.hook_id,
            "lifecycle_stage": self.lifecycle_stage,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "triggering_event_id": self.triggering_event_id,
            "input_summary": self.input_summary,
            "input_hash": self.input_hash,
            "invocation_attrs": self.invocation_attrs,
        }


@dataclass(frozen=True)
class HookResult:
    result_id: str
    invocation_id: str
    hook_id: str
    status: str
    result_kind: str
    output_summary: str | None
    output_hash: str | None
    error_message: str | None
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.result_kind in FORBIDDEN_HOOK_OUTCOMES:
            raise HookResultError(f"Forbidden hook result kind: {self.result_kind}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "invocation_id": self.invocation_id,
            "hook_id": self.hook_id,
            "status": self.status,
            "result_kind": self.result_kind,
            "output_summary": self.output_summary,
            "output_hash": self.output_hash,
            "error_message": self.error_message,
            "created_at": self.created_at,
            "result_attrs": self.result_attrs,
        }


@dataclass(frozen=True)
class HookPolicy:
    policy_id: str
    hook_id: str
    policy_kind: str
    status: str
    scope: str | None
    created_at: str
    updated_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.policy_kind in FORBIDDEN_HOOK_OUTCOMES:
            raise HookPolicyError(f"Forbidden hook policy kind: {self.policy_kind}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "hook_id": self.hook_id,
            "policy_kind": self.policy_kind,
            "status": self.status,
            "scope": self.scope,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "policy_attrs": self.policy_attrs,
        }
