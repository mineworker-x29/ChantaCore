from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SoulIdentity:
    soul_id: str
    soul_name: str
    soul_type: str
    description: str | None
    status: str
    created_at: str
    updated_at: str
    soul_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "soul_id": self.soul_id,
            "soul_name": self.soul_name,
            "soul_type": self.soul_type,
            "description": self.description,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "soul_attrs": dict(self.soul_attrs),
        }


@dataclass(frozen=True)
class PersonaProfile:
    profile_id: str
    soul_id: str
    profile_name: str
    identity_statement: str
    role_statement: str
    tone_guidance: list[str]
    behavioral_boundaries: list[str]
    capability_boundaries: list[str]
    safety_boundaries: list[str]
    status: str
    created_at: str
    updated_at: str
    profile_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "profile_id": self.profile_id,
            "soul_id": self.soul_id,
            "profile_name": self.profile_name,
            "identity_statement": self.identity_statement,
            "role_statement": self.role_statement,
            "tone_guidance": list(self.tone_guidance),
            "behavioral_boundaries": list(self.behavioral_boundaries),
            "capability_boundaries": list(self.capability_boundaries),
            "safety_boundaries": list(self.safety_boundaries),
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "profile_attrs": dict(self.profile_attrs),
        }


@dataclass(frozen=True)
class PersonaInstructionArtifact:
    artifact_id: str
    soul_id: str
    profile_id: str
    artifact_type: str
    title: str
    body: str
    body_preview: str
    body_hash: str
    source_kind: str
    source_ref: str | None
    status: str
    created_at: str
    artifact_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_id": self.artifact_id,
            "soul_id": self.soul_id,
            "profile_id": self.profile_id,
            "artifact_type": self.artifact_type,
            "title": self.title,
            "body": self.body,
            "body_preview": self.body_preview,
            "body_hash": self.body_hash,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "status": self.status,
            "created_at": self.created_at,
            "artifact_attrs": dict(self.artifact_attrs),
        }


@dataclass(frozen=True)
class AgentRoleBinding:
    binding_id: str
    soul_id: str
    profile_id: str
    agent_name: str
    runtime_path: str
    status: str
    created_at: str
    binding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "soul_id": self.soul_id,
            "profile_id": self.profile_id,
            "agent_name": self.agent_name,
            "runtime_path": self.runtime_path,
            "status": self.status,
            "created_at": self.created_at,
            "binding_attrs": dict(self.binding_attrs),
        }


@dataclass(frozen=True)
class PersonaLoadout:
    loadout_id: str
    soul_id: str
    profile_id: str
    binding_id: str | None
    artifact_ids: list[str]
    capability_snapshot_id: str | None
    created_at: str
    loadout_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "loadout_id": self.loadout_id,
            "soul_id": self.soul_id,
            "profile_id": self.profile_id,
            "binding_id": self.binding_id,
            "artifact_ids": list(self.artifact_ids),
            "capability_snapshot_id": self.capability_snapshot_id,
            "created_at": self.created_at,
            "loadout_attrs": dict(self.loadout_attrs),
        }


@dataclass(frozen=True)
class PersonaProjection:
    projection_id: str
    loadout_id: str
    soul_id: str
    profile_id: str
    projected_blocks: list[dict[str, Any]]
    total_chars: int
    truncated: bool
    created_at: str
    projection_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "projection_id": self.projection_id,
            "loadout_id": self.loadout_id,
            "soul_id": self.soul_id,
            "profile_id": self.profile_id,
            "projected_blocks": [dict(item) for item in self.projected_blocks],
            "total_chars": self.total_chars,
            "truncated": self.truncated,
            "created_at": self.created_at,
            "projection_attrs": dict(self.projection_attrs),
        }
