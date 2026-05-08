from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.external.errors import (
    ExternalAssimilationCandidateError,
    ExternalCapabilityDescriptorError,
    ExternalCapabilityImportBatchError,
    ExternalCapabilityNormalizationError,
    ExternalCapabilityRiskNoteError,
    ExternalCapabilitySourceError,
)


SOURCE_TYPES = {
    "local_manifest",
    "provided_dict",
    "provided_json",
    "mcp_descriptor",
    "plugin_manifest",
    "skill_manifest",
    "tool_manifest",
    "manual",
    "other",
}
TRUST_LEVELS = {
    "unknown",
    "untrusted",
    "local_user_provided",
    "trusted_internal",
    "trusted_project",
    "other",
}
SOURCE_STATUSES = {"active", "draft", "deprecated", "archived", "withdrawn"}
CAPABILITY_TYPES = {
    "tool",
    "skill",
    "adapter",
    "connector",
    "mcp_server",
    "plugin",
    "agent",
    "workflow",
    "other",
}
DESCRIPTOR_STATUSES = {"imported", "normalized", "invalid", "deprecated", "archived"}
BATCH_STATUSES = {"started", "completed", "completed_with_errors", "failed", "skipped"}
NORMALIZATION_STATUSES = {"normalized", "invalid", "needs_review", "unsupported", "error"}
REVIEW_STATUSES = {"pending_review", "approved_for_design", "rejected", "needs_more_info", "archived"}
ACTIVATION_STATUSES = {"disabled", "design_only", "candidate", "active", "rejected"}
RISK_LEVELS = {"unknown", "low", "medium", "high", "critical"}
RISK_CATEGORIES = {
    "filesystem_read",
    "filesystem_write",
    "shell_execution",
    "network_access",
    "credential_access",
    "external_code_execution",
    "data_exfiltration",
    "permission_escalation",
    "unknown",
    "other",
}


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


@dataclass(frozen=True)
class ExternalCapabilitySource:
    source_id: str
    source_name: str
    source_type: str
    source_ref: str | None
    trust_level: str
    status: str
    created_at: str
    updated_at: str
    source_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source_name:
            raise ExternalCapabilitySourceError("source_name is required")
        _require_value(self.source_type, SOURCE_TYPES, ExternalCapabilitySourceError, "source_type")
        _require_value(self.trust_level, TRUST_LEVELS, ExternalCapabilitySourceError, "trust_level")
        _require_value(self.status, SOURCE_STATUSES, ExternalCapabilitySourceError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "source_ref": self.source_ref,
            "trust_level": self.trust_level,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "source_attrs": self.source_attrs,
        }


@dataclass(frozen=True)
class ExternalCapabilityDescriptor:
    descriptor_id: str
    source_id: str | None
    capability_name: str
    capability_type: str
    description: str | None
    provider: str | None
    version: str | None
    declared_inputs: dict[str, Any]
    declared_outputs: dict[str, Any]
    declared_permissions: list[str]
    declared_risks: list[str]
    declared_entrypoint: str | None
    raw_descriptor: dict[str, Any]
    normalized: bool
    status: str
    created_at: str
    descriptor_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.capability_name:
            raise ExternalCapabilityDescriptorError("capability_name is required")
        _require_value(self.capability_type, CAPABILITY_TYPES, ExternalCapabilityDescriptorError, "capability_type")
        _require_value(self.status, DESCRIPTOR_STATUSES, ExternalCapabilityDescriptorError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "descriptor_id": self.descriptor_id,
            "source_id": self.source_id,
            "capability_name": self.capability_name,
            "capability_type": self.capability_type,
            "description": self.description,
            "provider": self.provider,
            "version": self.version,
            "declared_inputs": self.declared_inputs,
            "declared_outputs": self.declared_outputs,
            "declared_permissions": self.declared_permissions,
            "declared_risks": self.declared_risks,
            "declared_entrypoint": self.declared_entrypoint,
            "raw_descriptor": self.raw_descriptor,
            "normalized": self.normalized,
            "status": self.status,
            "created_at": self.created_at,
            "descriptor_attrs": self.descriptor_attrs,
        }


@dataclass(frozen=True)
class ExternalCapabilityImportBatch:
    batch_id: str
    source_id: str | None
    batch_name: str | None
    imported_descriptor_ids: list[str]
    failed_descriptor_refs: list[str]
    status: str
    created_at: str
    batch_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, BATCH_STATUSES, ExternalCapabilityImportBatchError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "source_id": self.source_id,
            "batch_name": self.batch_name,
            "imported_descriptor_ids": self.imported_descriptor_ids,
            "failed_descriptor_refs": self.failed_descriptor_refs,
            "status": self.status,
            "created_at": self.created_at,
            "batch_attrs": self.batch_attrs,
        }


@dataclass(frozen=True)
class ExternalCapabilityNormalizationResult:
    normalization_id: str
    descriptor_id: str
    status: str
    normalized_capability_type: str | None
    normalized_name: str | None
    normalized_permissions: list[str]
    normalized_risk_categories: list[str]
    validation_messages: list[str]
    created_at: str
    normalization_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, NORMALIZATION_STATUSES, ExternalCapabilityNormalizationError, "status")
        if self.normalized_capability_type is not None:
            _require_value(
                self.normalized_capability_type,
                CAPABILITY_TYPES,
                ExternalCapabilityNormalizationError,
                "normalized_capability_type",
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "normalization_id": self.normalization_id,
            "descriptor_id": self.descriptor_id,
            "status": self.status,
            "normalized_capability_type": self.normalized_capability_type,
            "normalized_name": self.normalized_name,
            "normalized_permissions": self.normalized_permissions,
            "normalized_risk_categories": self.normalized_risk_categories,
            "validation_messages": self.validation_messages,
            "created_at": self.created_at,
            "normalization_attrs": self.normalization_attrs,
        }


@dataclass(frozen=True)
class ExternalAssimilationCandidate:
    candidate_id: str
    descriptor_id: str
    source_id: str | None
    candidate_type: str
    candidate_name: str
    review_status: str = "pending_review"
    activation_status: str = "disabled"
    execution_enabled: bool = False
    recommended_next_step: str | None = None
    linked_tool_descriptor_id: str | None = None
    linked_permission_scope_id: str | None = None
    linked_risk_note_ids: list[str] = field(default_factory=list)
    created_at: str = ""
    candidate_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.candidate_type, CAPABILITY_TYPES, ExternalAssimilationCandidateError, "candidate_type")
        _require_value(self.review_status, REVIEW_STATUSES, ExternalAssimilationCandidateError, "review_status")
        _require_value(self.activation_status, ACTIVATION_STATUSES, ExternalAssimilationCandidateError, "activation_status")
        if self.execution_enabled is not False:
            raise ExternalAssimilationCandidateError("execution_enabled must be False in v0.14.0")
        if self.activation_status == "active":
            raise ExternalAssimilationCandidateError("active external candidates must not be created in v0.14.0")

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "descriptor_id": self.descriptor_id,
            "source_id": self.source_id,
            "candidate_type": self.candidate_type,
            "candidate_name": self.candidate_name,
            "review_status": self.review_status,
            "activation_status": self.activation_status,
            "execution_enabled": self.execution_enabled,
            "recommended_next_step": self.recommended_next_step,
            "linked_tool_descriptor_id": self.linked_tool_descriptor_id,
            "linked_permission_scope_id": self.linked_permission_scope_id,
            "linked_risk_note_ids": self.linked_risk_note_ids,
            "created_at": self.created_at,
            "candidate_attrs": self.candidate_attrs,
        }


@dataclass(frozen=True)
class ExternalCapabilityRiskNote:
    risk_note_id: str
    descriptor_id: str | None
    candidate_id: str | None
    risk_level: str
    risk_categories: list[str]
    message: str
    review_required: bool
    source_kind: str | None
    created_at: str
    risk_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.risk_level, RISK_LEVELS, ExternalCapabilityRiskNoteError, "risk_level")
        for category in self.risk_categories:
            _require_value(category, RISK_CATEGORIES, ExternalCapabilityRiskNoteError, "risk_category")
        if not self.message:
            raise ExternalCapabilityRiskNoteError("message is required")

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_note_id": self.risk_note_id,
            "descriptor_id": self.descriptor_id,
            "candidate_id": self.candidate_id,
            "risk_level": self.risk_level,
            "risk_categories": self.risk_categories,
            "message": self.message,
            "review_required": self.review_required,
            "source_kind": self.source_kind,
            "created_at": self.created_at,
            "risk_attrs": self.risk_attrs,
        }
