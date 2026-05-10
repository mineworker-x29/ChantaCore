from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def _new_runtime_capability_snapshot_id() -> str:
    return f"runtime_capability_snapshot:{uuid4()}"


def _new_agent_capability_profile_id() -> str:
    return f"agent_capability_profile:{uuid4()}"


@dataclass(frozen=True)
class RuntimeCapabilitySnapshot:
    snapshot_id: str
    agent_id: str
    runtime_path: str
    available_now: list[str]
    metadata_only: list[str]
    disabled_candidates: list[str]
    requires_review: list[str]
    requires_permission: list[str]
    not_implemented: list[str]
    inspection_scopes: list[str]
    created_at: str
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "agent_id": self.agent_id,
            "runtime_path": self.runtime_path,
            "available_now": list(self.available_now),
            "metadata_only": list(self.metadata_only),
            "disabled_candidates": list(self.disabled_candidates),
            "requires_review": list(self.requires_review),
            "requires_permission": list(self.requires_permission),
            "not_implemented": list(self.not_implemented),
            "inspection_scopes": list(self.inspection_scopes),
            "created_at": self.created_at,
            "snapshot_attrs": dict(self.snapshot_attrs),
        }


@dataclass(frozen=True)
class AgentCapabilityProfile:
    profile_id: str
    agent_id: str
    identity_statement: str
    current_capability_statement: str
    limitation_statement: str
    soul_boundary_statement: str
    snapshot: RuntimeCapabilitySnapshot
    created_at: str
    profile_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "agent_id": self.agent_id,
            "identity_statement": self.identity_statement,
            "current_capability_statement": self.current_capability_statement,
            "limitation_statement": self.limitation_statement,
            "soul_boundary_statement": self.soul_boundary_statement,
            "snapshot": self.snapshot.to_dict(),
            "created_at": self.created_at,
            "profile_attrs": dict(self.profile_attrs),
        }

    def to_prompt_block(self) -> str:
        return "\n".join(
            [
                "Runtime capability contract:",
                f"- identity: {self.identity_statement}",
                f"- current capability: {self.current_capability_statement}",
                f"- limitation: {self.limitation_statement}",
                f"- Soul boundary: {self.soul_boundary_statement}",
                "- available_now: " + _join_items(self.snapshot.available_now),
                "- metadata_only: " + _join_items(self.snapshot.metadata_only),
                "- disabled_candidates: " + _join_items(self.snapshot.disabled_candidates),
                "- requires_review: " + _join_items(self.snapshot.requires_review),
                "- requires_permission: " + _join_items(self.snapshot.requires_permission),
                "- not_implemented: " + _join_items(self.snapshot.not_implemented),
                "- inspection_scopes: " + _join_items(self.snapshot.inspection_scopes),
                "- workspace_file_read: "
                + _workspace_read_capability_summary(self.snapshot.snapshot_attrs),
                (
                    "When asked what you can do, answer from this capability "
                    "contract. Do not claim capabilities listed as metadata_only, "
                    "disabled_candidates, requires_review, requires_permission, "
                    "or not_implemented as available_now."
                ),
            ]
        )


class RuntimeCapabilityIntrospectionService:
    """Builds a read-only capability contract for the current runtime path."""

    def build_default_agent_snapshot(
        self,
        *,
        agent_id: str = "chanta_core_default",
    ) -> RuntimeCapabilitySnapshot:
        return RuntimeCapabilitySnapshot(
            snapshot_id=_new_runtime_capability_snapshot_id(),
            agent_id=agent_id,
            runtime_path="default_agent_repl_llm_chat",
            available_now=[
                "configured local LLM chat",
                "immediate-prompt response",
                "OCEL/session/process event recording",
                "skill:llm_chat",
                "trace-aware local chat surface",
                "explicit limitation/refusal behavior",
            ],
            metadata_only=[
                "tool registry views",
                "tool policy views",
                "external capability descriptors",
                "external assimilation candidates",
                "external OCEL payload descriptors",
                "external OCEL import candidates",
                "external OCEL preview snapshots",
                "PIG/OCPX reports when present as read-models",
            ],
            disabled_candidates=[
                "external assimilation candidates with execution_enabled=False",
            ],
            requires_review=[
                "imported external capabilities",
                "MCP/plugin descriptors",
                "external OCEL import candidates",
            ],
            requires_permission=[
                "workspace file read explicit invocation gate",
                "workspace file write",
                "shell execution",
                "network access",
                "tool dispatch",
            ],
            not_implemented=[
                "arbitrary repository file read",
                "ambient Personal Directory inspection",
                "shell execution",
                "network calls",
                "MCP connection",
                "plugin loading",
                "active runtime registry updates",
                "canonical external OCEL merge",
                "active external OCEL ingestion",
                "full bounded REPL session history injection",
                "autonomous Soul behavior",
            ],
            inspection_scopes=[
                "recent_global",
                "persisted_store",
                "current_session not enabled by default",
                "current_process_instance not enabled by default",
            ],
            created_at=utc_now_iso(),
            snapshot_attrs={
                "canonical_runtime_state": "OCEL",
                "read_model_only": True,
                "adds_active_capabilities": False,
                "workspace_file_read": {
                    "ambient_access": False,
                    "available_via_explicit_skill": True,
                    "available_in_default_chat_path": False,
                    "explicit_skills": [
                        "skill:list_workspace_files",
                        "skill:read_workspace_text_file",
                        "skill:summarize_workspace_markdown",
                    ],
                },
            },
        )

    def build_default_agent_profile(
        self,
        *,
        agent_id: str = "chanta_core_default",
    ) -> AgentCapabilityProfile:
        snapshot = self.build_default_agent_snapshot(agent_id=agent_id)
        return AgentCapabilityProfile(
            profile_id=_new_agent_capability_profile_id(),
            agent_id=agent_id,
            identity_statement=(
                "ChantaCore Default Agent is a trace-aware local LLM chat "
                "endpoint with OCEL persistence."
            ),
            current_capability_statement=(
                "It can answer from the immediate prompt and assembled "
                "OCEL/PIG context through skill:llm_chat while recording "
                "session and process events."
            ),
            limitation_statement=(
                "It does not directly read files, execute shell commands, call "
                "network resources, connect MCP, load plugins, or mutate runtime "
                "registries in the default chat path. Workspace file read is "
                "available only through explicit root-constrained read-only skills."
            ),
            soul_boundary_statement=(
                "It is not yet an active Soul or workspace agent; active "
                "workspace operation requires future explicit reviewed skills, "
                "permissions, and safety/conformance layers."
            ),
            snapshot=snapshot,
            created_at=utc_now_iso(),
            profile_attrs={
                "generated_from_runtime_capability_snapshot": snapshot.snapshot_id,
                "self_report_source": "runtime_capability_contract",
            },
        )


def build_default_agent_capability_prompt_block() -> str:
    return RuntimeCapabilityIntrospectionService().build_default_agent_profile().to_prompt_block()


def _join_items(items: list[str]) -> str:
    return ", ".join(items) if items else "none"


def _workspace_read_capability_summary(attrs: dict[str, Any]) -> str:
    info = attrs.get("workspace_file_read")
    if not isinstance(info, dict):
        return "ambient_access=false, available_via_explicit_skill=false"
    explicit_skills = info.get("explicit_skills")
    if not isinstance(explicit_skills, list):
        explicit_skills = []
    return (
        f"ambient_access={str(bool(info.get('ambient_access'))).lower()}, "
        f"available_via_explicit_skill={str(bool(info.get('available_via_explicit_skill'))).lower()}, "
        f"available_in_default_chat_path={str(bool(info.get('available_in_default_chat_path'))).lower()}, "
        "explicit_skills=" + _join_items([str(item) for item in explicit_skills])
    )
