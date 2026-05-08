from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.capabilities.errors import (
    CapabilityDecisionError,
    CapabilityDecisionEvidenceError,
    CapabilityRequestIntentError,
    CapabilityRequirementError,
)


REQUESTED_OPERATIONS = {
    "chat",
    "workspace_file_read",
    "workspace_file_write",
    "shell_execution",
    "network_access",
    "mcp_connection",
    "plugin_loading",
    "external_capability_use",
    "external_ocel_import",
    "runtime_registry_update",
    "session_context",
    "unknown",
    "other",
}

CAPABILITY_CATEGORIES = {
    "llm_chat",
    "workspace",
    "filesystem",
    "shell",
    "network",
    "mcp",
    "plugin",
    "tool_dispatch",
    "external_capability",
    "external_ocel",
    "permission",
    "sandbox",
    "memory",
    "session_context",
    "unknown",
    "other",
}

AVAILABILITIES = {
    "available_now",
    "metadata_only",
    "disabled_candidate",
    "requires_review",
    "requires_permission",
    "requires_explicit_skill",
    "not_implemented",
    "unknown",
}

AGENT_MODES = {
    "answer_with_llm",
    "state_limitation",
    "ask_for_pasted_content",
    "requires_explicit_skill",
    "requires_review",
    "requires_permission",
    "cannot_fulfill",
    "unknown",
}


@dataclass(frozen=True)
class CapabilityRequestIntent:
    intent_id: str
    session_id: str | None
    turn_id: str | None
    message_id: str | None
    user_prompt_preview: str
    requested_operation: str
    target_refs: list[dict[str, Any]]
    inferred_requirement_ids: list[str]
    created_at: str
    intent_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.requested_operation not in REQUESTED_OPERATIONS:
            raise CapabilityRequestIntentError(
                f"Unsupported requested_operation: {self.requested_operation}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "message_id": self.message_id,
            "user_prompt_preview": self.user_prompt_preview,
            "requested_operation": self.requested_operation,
            "target_refs": [dict(item) for item in self.target_refs],
            "inferred_requirement_ids": list(self.inferred_requirement_ids),
            "created_at": self.created_at,
            "intent_attrs": dict(self.intent_attrs),
        }


@dataclass(frozen=True)
class CapabilityRequirement:
    requirement_id: str
    requirement_type: str
    capability_name: str
    capability_category: str
    target_type: str | None
    target_ref: str | None
    required_now: bool
    reason: str | None
    created_at: str
    requirement_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.capability_category not in CAPABILITY_CATEGORIES:
            raise CapabilityRequirementError(
                f"Unsupported capability_category: {self.capability_category}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "requirement_type": self.requirement_type,
            "capability_name": self.capability_name,
            "capability_category": self.capability_category,
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "required_now": self.required_now,
            "reason": self.reason,
            "created_at": self.created_at,
            "requirement_attrs": dict(self.requirement_attrs),
        }


@dataclass(frozen=True)
class CapabilityDecision:
    decision_id: str
    intent_id: str
    requirement_id: str | None
    capability_name: str
    availability: str
    can_execute_now: bool
    requires_review: bool
    requires_permission: bool
    reason: str | None
    recommended_response: str | None
    evidence_ids: list[str]
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.availability not in AVAILABILITIES:
            raise CapabilityDecisionError(
                f"Unsupported availability: {self.availability}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "intent_id": self.intent_id,
            "requirement_id": self.requirement_id,
            "capability_name": self.capability_name,
            "availability": self.availability,
            "can_execute_now": self.can_execute_now,
            "requires_review": self.requires_review,
            "requires_permission": self.requires_permission,
            "reason": self.reason,
            "recommended_response": self.recommended_response,
            "evidence_ids": list(self.evidence_ids),
            "created_at": self.created_at,
            "decision_attrs": dict(self.decision_attrs),
        }


@dataclass(frozen=True)
class CapabilityDecisionSurface:
    surface_id: str
    session_id: str | None
    turn_id: str | None
    message_id: str | None
    capability_snapshot_id: str | None
    intent_id: str
    decision_ids: list[str]
    overall_availability: str
    can_fulfill_now: bool
    recommended_agent_mode: str
    limitation_summary: str | None
    created_at: str
    surface_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.overall_availability not in AVAILABILITIES:
            raise CapabilityDecisionError(
                f"Unsupported overall_availability: {self.overall_availability}"
            )
        if self.recommended_agent_mode not in AGENT_MODES:
            raise CapabilityDecisionError(
                f"Unsupported recommended_agent_mode: {self.recommended_agent_mode}"
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "surface_id": self.surface_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "message_id": self.message_id,
            "capability_snapshot_id": self.capability_snapshot_id,
            "intent_id": self.intent_id,
            "decision_ids": list(self.decision_ids),
            "overall_availability": self.overall_availability,
            "can_fulfill_now": self.can_fulfill_now,
            "recommended_agent_mode": self.recommended_agent_mode,
            "limitation_summary": self.limitation_summary,
            "created_at": self.created_at,
            "surface_attrs": dict(self.surface_attrs),
        }


@dataclass(frozen=True)
class CapabilityDecisionEvidence:
    evidence_id: str
    decision_id: str | None
    evidence_type: str
    source_kind: str | None
    source_ref: str | None
    content: str
    created_at: str
    evidence_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.content:
            raise CapabilityDecisionEvidenceError("Evidence content is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "decision_id": self.decision_id,
            "evidence_type": self.evidence_type,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "content": self.content,
            "created_at": self.created_at,
            "evidence_attrs": dict(self.evidence_attrs),
        }
