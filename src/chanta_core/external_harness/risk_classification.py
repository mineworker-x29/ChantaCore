from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .manifest_extraction import (
    ExternalManifestCandidateBase,
    ExternalManifestRiskSurfaceKind,
)
from .profiles import _metadata_flag_true, _require_non_blank, _validate_object_list, _validate_string_list


V0325_VERSION = "v0.32.5"
V0325_RELEASE_NAME = "v0.32.5 External Capability Risk Classification"

DEFAULT_RISK_PROHIBITED_RUNTIME_ACTIONS = [
    "capability permission",
    "runtime certification",
    "harness execution",
    "reference code execution",
    "install",
    "import runtime",
    "plugin loading",
    "external plugin loading",
    "tool registration",
    "tool invocation",
    "mission installation",
    "mission execution",
    "gateway connection",
    "provider invocation",
    "network",
    "credential",
    "secret file read",
    "command",
    "digestion candidate creation",
    "internal candidate creation",
    "dominion target creation",
    "dominion decision creation",
    "registry mutation",
    "memory mutation",
    "OCEL emission",
]


class ExternalCapabilityRiskClass(StrEnum):
    SAFE_DESCRIPTIVE = "safe_descriptive"
    DIGESTIBLE_PATTERN = "digestible_pattern"
    REQUIRES_REVIEW = "requires_review"
    DOMINION_REQUIRED = "dominion_required"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class ExternalCapabilityRiskSeverity(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ExternalCapabilityRiskRoute(StrEnum):
    DESCRIBE_ONLY = "describe_only"
    SEND_TO_V0326_DIGESTION_GENERATOR = "send_to_v0326_digestion_generator"
    SEND_TO_V0328_DOMINION_EMITTER = "send_to_v0328_dominion_emitter"
    REQUIRE_REVIEW = "require_review"
    REQUIRE_FUTURE_GATE = "require_future_gate"
    REJECT = "reject"
    BLOCK = "block"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class ExternalCapabilityBoundaryKind(StrEnum):
    NO_EXECUTION = "no_execution"
    NO_REFERENCE_CODE_EXECUTION = "no_reference_code_execution"
    NO_RUNTIME_IMPORT = "no_runtime_import"
    NO_DEPENDENCY_INSTALL = "no_dependency_install"
    NO_PLUGIN_LOADING = "no_plugin_loading"
    NO_TOOL_REGISTRATION = "no_tool_registration"
    NO_TOOL_INVOCATION = "no_tool_invocation"
    NO_MISSION_INSTALLATION = "no_mission_installation"
    NO_MISSION_EXECUTION = "no_mission_execution"
    NO_PROVIDER_INVOCATION = "no_provider_invocation"
    NO_GATEWAY_CONNECTION = "no_gateway_connection"
    NO_CHANNEL_ACCESS = "no_channel_access"
    NO_MESSAGE_SEND = "no_message_send"
    NO_WEBHOOK_CALL = "no_webhook_call"
    NO_WORKSPACE_WRITE = "no_workspace_write"
    NO_CODE_EDIT = "no_code_edit"
    NO_PATCH_APPLICATION = "no_patch_application"
    NO_NETWORK_ACCESS = "no_network_access"
    NO_CREDENTIAL_ACCESS = "no_credential_access"
    NO_SECRET_FILE_READ = "no_secret_file_read"
    NO_COMMAND_EXECUTION = "no_command_execution"
    NO_BROWSER_AUTOMATION = "no_browser_automation"
    NO_RPA_CONTROL = "no_rpa_control"
    NO_REGISTRY_MUTATION = "no_registry_mutation"
    NO_MEMORY_MUTATION = "no_memory_mutation"
    NO_PRIVATE_DATA_ACCESS = "no_private_data_access"
    NO_RAW_OUTPUT_PERSISTENCE = "no_raw_output_persistence"
    NO_OCEL_EMISSION = "no_ocel_emission"
    APPROVAL_REQUIRED = "approval_required"
    AUDIT_REQUIRED = "audit_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ExternalCapabilityReviewRequirementKind(StrEnum):
    EVIDENCE_REVIEW = "evidence_review"
    BOUNDARY_REVIEW = "boundary_review"
    SECURITY_REVIEW = "security_review"
    PRIVACY_REVIEW = "privacy_review"
    CREDENTIAL_REVIEW = "credential_review"
    NETWORK_REVIEW = "network_review"
    COMMAND_REVIEW = "command_review"
    PROVIDER_REVIEW = "provider_review"
    PLUGIN_REVIEW = "plugin_review"
    GATEWAY_REVIEW = "gateway_review"
    MEMORY_REVIEW = "memory_review"
    REGISTRY_REVIEW = "registry_review"
    OCEL_TRACE_REVIEW = "ocel_trace_review"
    HUMAN_REVIEW = "human_review"
    FUTURE_GATE_REVIEW = "future_gate_review"
    UNKNOWN = "unknown"


class ExternalCapabilityRiskClassificationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    CLASSIFIED = "classified"
    CLASSIFIED_WITH_GAPS = "classified_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    REJECTED = "rejected"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalCapabilityRiskEvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    NONE = "none"
    WEAK = "weak"
    PARTIAL = "partial"
    SUFFICIENT_FOR_RISK_CLASSIFICATION = "sufficient_for_risk_classification"
    SUFFICIENT_FOR_V0326_REVIEW = "sufficient_for_v0326_review"
    SUFFICIENT_FOR_V0328_REVIEW = "sufficient_for_v0328_review"
    CONFLICTING = "conflicting"
    BLOCKED = "blocked"


class ExternalCapabilityRiskSourceKind(StrEnum):
    EXTERNAL_MANIFEST_CANDIDATE = "external_manifest_candidate"
    EXTERNAL_MANIFEST_CANDIDATE_SET = "external_manifest_candidate_set"
    EXTERNAL_MANIFEST_EXTRACTION_REPORT = "external_manifest_extraction_report"
    OPENCODE_OBSERVATION_OUTPUT = "opencode_observation_output"
    OPENCLAW_OBSERVATION_OUTPUT = "openclaw_observation_output"
    HERMES_OBSERVATION_OUTPUT = "hermes_observation_output"
    REFERENCE_FILE_INVENTORY = "reference_file_inventory"
    REFERENCE_CORPUS_SNAPSHOT = "reference_corpus_snapshot"
    MANUAL_RISK_REVIEW = "manual_risk_review"
    SANITIZED_RISK_MANIFEST = "sanitized_risk_manifest"
    UNKNOWN = "unknown"


def _validate_version_includes_v0325(version: str) -> None:
    _require_non_blank("version", version)
    if V0325_VERSION not in version:
        raise ValueError("version must include v0.32.5")


def _validate_kind_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_default_prohibitions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_RISK_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.32.5 prohibitions: {sorted(missing)}")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.32.5")


def _has_blocking_boundary(boundaries: list["ExternalCapabilityBoundaryRequirement"]) -> bool:
    return any(
        boundary.blocks_execution or boundary.blocks_activation or boundary.blocks_runtime_registration
        for boundary in boundaries
    )


@dataclass(frozen=True)
class ExternalCapabilityRiskSourceRef:
    source_ref_id: str
    source_kind: ExternalCapabilityRiskSourceKind | str
    source_id: str
    manifest_candidate_id: str | None = None
    harness_kind: str | None = None
    reference_entry_ids: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ExternalCapabilityRiskSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _validate_string_list("reference_entry_ids", self.reference_entry_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"source_fetch", "execution", "live_scan"}):
            raise ValueError("ExternalCapabilityRiskSourceRef is not source fetch, execution, or live scan")

    @property
    def source_fetch(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityRiskFactor:
    risk_factor_id: str
    risk_surface: str
    risk_class: ExternalCapabilityRiskClass | str
    severity: ExternalCapabilityRiskSeverity | str
    summary: str
    source_ref_ids: list[str] = field(default_factory=list)
    boundary_kinds: list[ExternalCapabilityBoundaryKind | str] = field(default_factory=list)
    review_requirements: list[ExternalCapabilityReviewRequirementKind | str] = field(default_factory=list)
    evidence_quality: ExternalCapabilityRiskEvidenceQuality | str = ExternalCapabilityRiskEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_factor_id", self.risk_factor_id)
        _require_non_blank("risk_surface", self.risk_surface)
        ExternalCapabilityRiskClass(self.risk_class)
        severity = ExternalCapabilityRiskSeverity(self.severity)
        _require_non_blank("summary", self.summary)
        for name in ("source_ref_ids", "evidence_refs", "assumptions", "limitations"):
            _validate_string_list(name, getattr(self, name))
        _validate_kind_list("boundary_kinds", self.boundary_kinds, ExternalCapabilityBoundaryKind)
        _validate_kind_list("review_requirements", self.review_requirements, ExternalCapabilityReviewRequirementKind)
        ExternalCapabilityRiskEvidenceQuality(self.evidence_quality)
        if severity in {
            ExternalCapabilityRiskSeverity.HIGH,
            ExternalCapabilityRiskSeverity.CRITICAL,
            ExternalCapabilityRiskSeverity.BLOCKED,
        } and not self.boundary_kinds and not self.review_requirements:
            raise ValueError("high, critical, and blocked severity require boundary kind or review requirement")
        if _metadata_flag_true(self.metadata, {"proof_of_exploitability", "permission"}):
            raise ValueError("ExternalCapabilityRiskFactor is not proof of exploitability or permission")

    @property
    def proof_of_exploitability(self) -> bool:
        return False

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityBoundaryRequirement:
    boundary_requirement_id: str
    boundary_kind: ExternalCapabilityBoundaryKind | str
    target_risk_factor_ids: list[str] = field(default_factory=list)
    target_manifest_candidate_ids: list[str] = field(default_factory=list)
    reason: str = "Runtime boundary required for static risk classification."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_RISK_PROHIBITED_RUNTIME_ACTIONS))
    required_reviews: list[ExternalCapabilityReviewRequirementKind | str] = field(default_factory=list)
    blocks_execution: bool = True
    blocks_activation: bool = True
    blocks_runtime_registration: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_requirement_id", self.boundary_requirement_id)
        ExternalCapabilityBoundaryKind(self.boundary_kind)
        _require_non_blank("reason", self.reason)
        for name in ("target_risk_factor_ids", "target_manifest_candidate_ids"):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_kind_list("required_reviews", self.required_reviews, ExternalCapabilityReviewRequirementKind)
        if self.blocks_execution is not True:
            raise ValueError("blocks_execution must default True in v0.32.5")
        if self.blocks_activation is not True:
            raise ValueError("blocks_activation must default True in v0.32.5")
        if self.blocks_runtime_registration is not True:
            raise ValueError("blocks_runtime_registration must default True in v0.32.5")
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "permission"}):
            raise ValueError("ExternalCapabilityBoundaryRequirement is not runtime enforcement")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityReviewRequirement:
    review_requirement_id: str
    requirement_kind: ExternalCapabilityReviewRequirementKind | str
    target_risk_factor_ids: list[str] = field(default_factory=list)
    target_manifest_candidate_ids: list[str] = field(default_factory=list)
    reason: str = "Review required for static risk classification."
    required_evidence_refs: list[str] = field(default_factory=list)
    required_reviewer_refs: list[str] = field(default_factory=list)
    approval_granted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_requirement_id", self.review_requirement_id)
        ExternalCapabilityReviewRequirementKind(self.requirement_kind)
        _require_non_blank("reason", self.reason)
        for name in (
            "target_risk_factor_ids",
            "target_manifest_candidate_ids",
            "required_evidence_refs",
            "required_reviewer_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.approval_granted is not False:
            raise ValueError("approval_granted must always be False in v0.32.5")
        if _metadata_flag_true(self.metadata, {"approval", "approval_granted"}):
            raise ValueError("ExternalCapabilityReviewRequirement is not approval")

    @property
    def approval(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityRiskClassification:
    classification_id: str
    source_refs: list[ExternalCapabilityRiskSourceRef] = field(default_factory=list)
    target_manifest_candidate_id: str | None = None
    risk_class: ExternalCapabilityRiskClass | str = ExternalCapabilityRiskClass.UNKNOWN
    route: ExternalCapabilityRiskRoute | str = ExternalCapabilityRiskRoute.UNKNOWN
    severity: ExternalCapabilityRiskSeverity | str = ExternalCapabilityRiskSeverity.UNKNOWN
    status: ExternalCapabilityRiskClassificationStatus | str = ExternalCapabilityRiskClassificationStatus.CLASSIFIED_WITH_GAPS
    risk_factors: list[ExternalCapabilityRiskFactor] = field(default_factory=list)
    boundary_requirements: list[ExternalCapabilityBoundaryRequirement] = field(default_factory=list)
    review_requirements: list[ExternalCapabilityReviewRequirement] = field(default_factory=list)
    evidence_quality: ExternalCapabilityRiskEvidenceQuality | str = ExternalCapabilityRiskEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0326_digestion_candidate_generation: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_capability_permission: bool = False
    ready_for_runtime_certification: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("classification_id", self.classification_id)
        risk_class = ExternalCapabilityRiskClass(self.risk_class)
        route = ExternalCapabilityRiskRoute(self.route)
        ExternalCapabilityRiskSeverity(self.severity)
        ExternalCapabilityRiskClassificationStatus(self.status)
        _validate_object_list("source_refs", self.source_refs, ExternalCapabilityRiskSourceRef)
        _validate_object_list("risk_factors", self.risk_factors, ExternalCapabilityRiskFactor)
        _validate_object_list("boundary_requirements", self.boundary_requirements, ExternalCapabilityBoundaryRequirement)
        _validate_object_list("review_requirements", self.review_requirements, ExternalCapabilityReviewRequirement)
        ExternalCapabilityRiskEvidenceQuality(self.evidence_quality)
        for name in ("evidence_refs", "assumptions", "limitations", "gaps"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            ("ready_for_capability_permission", "ready_for_runtime_certification", "ready_for_execution"),
        )
        if self.ready_for_v0326_digestion_candidate_generation:
            if risk_class != ExternalCapabilityRiskClass.DIGESTIBLE_PATTERN:
                raise ValueError("v0.32.6 handoff requires digestible_pattern risk class")
            if route != ExternalCapabilityRiskRoute.SEND_TO_V0326_DIGESTION_GENERATOR:
                raise ValueError("v0.32.6 handoff requires send_to_v0326 route")
            if _has_blocking_boundary(self.boundary_requirements):
                raise ValueError("v0.32.6 handoff is not allowed with blocking boundary requirements")
        if self.ready_for_v0328_dominion_candidate_emitter:
            allowed = (
                risk_class == ExternalCapabilityRiskClass.DOMINION_REQUIRED
                and route == ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER
            ) or route in {
                ExternalCapabilityRiskRoute.REQUIRE_REVIEW,
                ExternalCapabilityRiskRoute.REQUIRE_FUTURE_GATE,
                ExternalCapabilityRiskRoute.BLOCK,
            }
            if not allowed:
                raise ValueError("v0.32.8 handoff requires dominion_required or conservative route")
        if _metadata_flag_true(
            self.metadata,
            {
                "permission",
                "runtime_certification",
                "digestion_candidate",
                "internal_skill_candidate",
                "dominion_target",
                "dominion_decision",
            },
        ):
            raise ValueError("ExternalCapabilityRiskClassification is not permission or active candidate/control artifact")

    @property
    def permission(self) -> bool:
        return False

    @property
    def digestion_candidate(self) -> bool:
        return False

    @property
    def dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityRiskMap:
    risk_map_id: str
    version: str = V0325_VERSION
    classification_ids: list[str] = field(default_factory=list)
    safe_descriptive_classification_ids: list[str] = field(default_factory=list)
    digestible_pattern_classification_ids: list[str] = field(default_factory=list)
    review_required_classification_ids: list[str] = field(default_factory=list)
    dominion_required_classification_ids: list[str] = field(default_factory=list)
    blocked_classification_ids: list[str] = field(default_factory=list)
    future_track_classification_ids: list[str] = field(default_factory=list)
    no_op_classification_ids: list[str] = field(default_factory=list)
    high_risk_factor_ids: list[str] = field(default_factory=list)
    critical_risk_factor_ids: list[str] = field(default_factory=list)
    blocked_risk_factor_ids: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0326_digestion_candidate_generation: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_map_id", self.risk_map_id)
        _validate_version_includes_v0325(self.version)
        for name in (
            "classification_ids",
            "safe_descriptive_classification_ids",
            "digestible_pattern_classification_ids",
            "review_required_classification_ids",
            "dominion_required_classification_ids",
            "blocked_classification_ids",
            "future_track_classification_ids",
            "no_op_classification_ids",
            "high_risk_factor_ids",
            "critical_risk_factor_ids",
            "blocked_risk_factor_ids",
            "evidence_refs",
            "gaps",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution",))
        if _metadata_flag_true(self.metadata, {"permission_map", "execution_ready"}):
            raise ValueError("ExternalCapabilityRiskMap is not permission map")

    @property
    def permission_map(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityBoundaryMap:
    boundary_map_id: str
    version: str = V0325_VERSION
    boundary_requirements: list[ExternalCapabilityBoundaryRequirement] = field(default_factory=list)
    review_requirements: list[ExternalCapabilityReviewRequirement] = field(default_factory=list)
    prohibited_runtime_surfaces: list[str] = field(default_factory=list)
    future_gate_required_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_execution: bool = False
    ready_for_runtime_enforcement: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_map_id", self.boundary_map_id)
        _validate_version_includes_v0325(self.version)
        _validate_object_list("boundary_requirements", self.boundary_requirements, ExternalCapabilityBoundaryRequirement)
        _validate_object_list("review_requirements", self.review_requirements, ExternalCapabilityReviewRequirement)
        for name in ("prohibited_runtime_surfaces", "future_gate_required_items", "blocked_items", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution", "ready_for_runtime_enforcement"))
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "execution_ready"}):
            raise ValueError("ExternalCapabilityBoundaryMap is not runtime enforcement")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityNoOpRecommendation:
    no_op_id: str
    target_manifest_candidate_id: str | None = None
    reason: str = "No runtime action recommended for this external capability surface."
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_id", self.no_op_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("ready_for_execution",))
        if _metadata_flag_true(self.metadata, {"failure", "execution"}):
            raise ValueError("ExternalCapabilityNoOpRecommendation is valid no-op metadata only")

    @property
    def failure(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityFutureGateItem:
    future_gate_id: str
    gate_kind: str
    target_manifest_candidate_id: str | None = None
    reason: str = "Future gate required before any later-stage work."
    required_artifacts: list[str] = field(default_factory=list)
    required_reviews: list[ExternalCapabilityReviewRequirementKind | str] = field(default_factory=list)
    prohibited_until_satisfied: list[str] = field(default_factory=lambda: list(DEFAULT_RISK_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    ready_now: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("future_gate_id", self.future_gate_id)
        _require_non_blank("gate_kind", self.gate_kind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("required_artifacts", self.required_artifacts)
        _validate_kind_list("required_reviews", self.required_reviews, ExternalCapabilityReviewRequirementKind)
        _validate_default_prohibitions("prohibited_until_satisfied", self.prohibited_until_satisfied)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("ready_now", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"readiness", "execution_ready"}):
            raise ValueError("ExternalCapabilityFutureGateItem is not readiness")

    @property
    def readiness(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityRiskClassificationInput:
    classification_input_id: str
    source_version: str = V0325_VERSION
    manifest_candidate_set_ids: list[str] = field(default_factory=list)
    manifest_extraction_report_ids: list[str] = field(default_factory=list)
    opencode_output_ids: list[str] = field(default_factory=list)
    openclaw_output_ids: list[str] = field(default_factory=list)
    hermes_output_ids: list[str] = field(default_factory=list)
    reference_inventory_ids: list[str] = field(default_factory=list)
    reference_corpus_snapshot_ids: list[str] = field(default_factory=list)
    source_refs: list[ExternalCapabilityRiskSourceRef] = field(default_factory=list)
    requested_risk_classes: list[ExternalCapabilityRiskClass | str] = field(default_factory=list)
    task_summary: str = "Classify external capability risk from static contract metadata."
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_RISK_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("classification_input_id", self.classification_input_id)
        _require_non_blank("source_version", self.source_version)
        for name in (
            "manifest_candidate_set_ids",
            "manifest_extraction_report_ids",
            "opencode_output_ids",
            "openclaw_output_ids",
            "hermes_output_ids",
            "reference_inventory_ids",
            "reference_corpus_snapshot_ids",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_object_list("source_refs", self.source_refs, ExternalCapabilityRiskSourceRef)
        _validate_kind_list("requested_risk_classes", self.requested_risk_classes, ExternalCapabilityRiskClass)
        _require_non_blank("task_summary", self.task_summary)
        _validate_default_prohibitions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        if _metadata_flag_true(self.metadata, {"execution_request", "permission_request"}):
            raise ValueError("ExternalCapabilityRiskClassificationInput is not execution request")

    @property
    def execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityRiskClassificationFinding:
    finding_id: str
    classification_input_id: str
    source_ref_ids: list[str]
    target_manifest_candidate_id: str | None
    risk_class: ExternalCapabilityRiskClass | str
    route: ExternalCapabilityRiskRoute | str
    severity: ExternalCapabilityRiskSeverity | str
    summary: str
    risk_factor_ids: list[str] = field(default_factory=list)
    boundary_requirement_ids: list[str] = field(default_factory=list)
    review_requirement_ids: list[str] = field(default_factory=list)
    evidence_quality: ExternalCapabilityRiskEvidenceQuality | str = ExternalCapabilityRiskEvidenceQuality.UNKNOWN
    evidence_refs: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("classification_input_id", self.classification_input_id)
        _validate_string_list("source_ref_ids", self.source_ref_ids)
        ExternalCapabilityRiskClass(self.risk_class)
        ExternalCapabilityRiskRoute(self.route)
        ExternalCapabilityRiskSeverity(self.severity)
        _require_non_blank("summary", self.summary)
        for name in (
            "risk_factor_ids",
            "boundary_requirement_ids",
            "review_requirement_ids",
            "evidence_refs",
            "assumptions",
            "limitations",
        ):
            _validate_string_list(name, getattr(self, name))
        ExternalCapabilityRiskEvidenceQuality(self.evidence_quality)
        if _metadata_flag_true(self.metadata, {"certification", "permission"}):
            raise ValueError("ExternalCapabilityRiskClassificationFinding is not certification or permission")

    @property
    def certification(self) -> bool:
        return False

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityRiskClassificationReport:
    report_id: str
    version: str
    classification_input_id: str
    risk_map_id: str | None = None
    boundary_map_id: str | None = None
    classifications: list[ExternalCapabilityRiskClassification] = field(default_factory=list)
    findings: list[ExternalCapabilityRiskClassificationFinding] = field(default_factory=list)
    no_op_recommendations: list[ExternalCapabilityNoOpRecommendation] = field(default_factory=list)
    future_gate_items: list[ExternalCapabilityFutureGateItem] = field(default_factory=list)
    status: ExternalCapabilityRiskClassificationStatus | str = ExternalCapabilityRiskClassificationStatus.CLASSIFIED_WITH_GAPS
    summary: str = "External capability risk classification contract report."
    classified_count: int = 0
    blocked_items: list[str] = field(default_factory=list)
    deferred_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0326_digestion_candidate_generation: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0325(self.version)
        _require_non_blank("classification_input_id", self.classification_input_id)
        _validate_object_list("classifications", self.classifications, ExternalCapabilityRiskClassification)
        _validate_object_list("findings", self.findings, ExternalCapabilityRiskClassificationFinding)
        _validate_object_list("no_op_recommendations", self.no_op_recommendations, ExternalCapabilityNoOpRecommendation)
        _validate_object_list("future_gate_items", self.future_gate_items, ExternalCapabilityFutureGateItem)
        ExternalCapabilityRiskClassificationStatus(self.status)
        _require_non_blank("summary", self.summary)
        if self.classified_count < 0:
            raise ValueError("classified_count must be >= 0")
        for name in ("blocked_items", "deferred_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution",))
        if _metadata_flag_true(self.metadata, {"runtime_classification", "execution_ready"}):
            raise ValueError("ExternalCapabilityRiskClassificationReport is not runtime classification")

    @property
    def runtime_classification(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityRiskClassificationRunPreview:
    run_preview_id: str
    classification_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_harness_execution_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_install_guarantee: bool = True
    no_import_runtime_guarantee: bool = True
    no_plugin_loading_guarantee: bool = True
    no_tool_registration_guarantee: bool = True
    no_tool_invocation_guarantee: bool = True
    no_mission_installation_guarantee: bool = True
    no_mission_execution_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_gateway_connection_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_secret_file_read_guarantee: bool = True
    no_digestion_candidate_creation_guarantee: bool = True
    no_dominion_target_creation_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        guarantee_names = tuple(name for name in self.__dataclass_fields__ if name.startswith("no_"))
        for name in guarantee_names:
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must always be True in v0.32.5")
        if _metadata_flag_true(self.metadata, {"execution"}):
            raise ValueError("ExternalCapabilityRiskClassificationRunPreview is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalCapabilityRiskNoRuntimeGuarantee:
    guarantee_id: str
    version: str
    no_capability_permission: bool = True
    no_runtime_certification: bool = True
    no_harness_execution: bool = True
    no_reference_code_execution: bool = True
    no_dependency_install: bool = True
    no_import_runtime: bool = True
    no_plugin_loading: bool = True
    no_external_plugin_loading: bool = True
    no_tool_registration: bool = True
    no_tool_invocation: bool = True
    no_mission_installation: bool = True
    no_mission_execution: bool = True
    no_gateway_connection: bool = True
    no_provider_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_file_read: bool = True
    no_command_execution: bool = True
    no_digestion_candidate_creation: bool = True
    no_internal_candidate_creation: bool = True
    no_dominion_target_creation: bool = True
    no_dominion_decision_creation: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0325(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must always be True in v0.32.5")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0325ReadinessReport:
    report_id: str
    version: str
    classification_report_id: str | None = None
    risk_map_id: str | None = None
    boundary_map_id: str | None = None
    summary: str = "v0.32.5 readiness is limited to design-stage handoff."
    ready_for_v0326_digestion_candidate_generation: bool = False
    ready_for_v0328_dominion_candidate_emitter: bool = False
    ready_for_execution: bool = False
    ready_for_capability_permission: bool = False
    ready_for_runtime_certification: bool = False
    ready_for_digestion_candidate_creation: bool = False
    ready_for_internal_candidate_creation: bool = False
    ready_for_dominion_target_creation: bool = False
    ready_for_dominion_decision_creation: bool = False
    ready_for_plugin_loading: bool = False
    ready_for_tool_registration: bool = False
    ready_for_tool_invocation: bool = False
    ready_for_mission_installation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_gateway_connection: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_RISK_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0325(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_capability_permission",
                "ready_for_runtime_certification",
                "ready_for_digestion_candidate_creation",
                "ready_for_internal_candidate_creation",
                "ready_for_dominion_target_creation",
                "ready_for_dominion_decision_creation",
                "ready_for_plugin_loading",
                "ready_for_tool_registration",
                "ready_for_tool_invocation",
                "ready_for_mission_installation",
                "ready_for_provider_invocation",
                "ready_for_gateway_connection",
                "ready_for_network_access",
                "ready_for_credential_access",
                "ready_for_command_execution",
            ),
        )
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_default_prohibitions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "permission", "runtime_certification"}):
            raise ValueError("V0325ReadinessReport is not runtime enablement")


def build_external_capability_risk_source_ref(
    source_ref_id: str,
    source_kind: ExternalCapabilityRiskSourceKind | str,
    source_id: str,
    **kwargs: Any,
) -> ExternalCapabilityRiskSourceRef:
    return ExternalCapabilityRiskSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, **kwargs)


def build_external_capability_risk_factor(
    risk_factor_id: str,
    risk_surface: str,
    risk_class: ExternalCapabilityRiskClass | str,
    severity: ExternalCapabilityRiskSeverity | str,
    summary: str,
    **kwargs: Any,
) -> ExternalCapabilityRiskFactor:
    return ExternalCapabilityRiskFactor(
        risk_factor_id=risk_factor_id,
        risk_surface=risk_surface,
        risk_class=risk_class,
        severity=severity,
        summary=summary,
        **kwargs,
    )


def build_external_capability_boundary_requirement(
    boundary_requirement_id: str,
    boundary_kind: ExternalCapabilityBoundaryKind | str,
    **kwargs: Any,
) -> ExternalCapabilityBoundaryRequirement:
    return ExternalCapabilityBoundaryRequirement(
        boundary_requirement_id=boundary_requirement_id,
        boundary_kind=boundary_kind,
        **kwargs,
    )


def build_external_capability_review_requirement(
    review_requirement_id: str,
    requirement_kind: ExternalCapabilityReviewRequirementKind | str,
    **kwargs: Any,
) -> ExternalCapabilityReviewRequirement:
    return ExternalCapabilityReviewRequirement(
        review_requirement_id=review_requirement_id,
        requirement_kind=requirement_kind,
        **kwargs,
    )


def build_external_capability_risk_classification(classification_id: str, **kwargs: Any) -> ExternalCapabilityRiskClassification:
    if "route" not in kwargs:
        kwargs["route"] = infer_risk_route_from_class_and_surfaces(
            kwargs.get("risk_class", ExternalCapabilityRiskClass.UNKNOWN),
            [factor.risk_surface for factor in kwargs.get("risk_factors", [])],
        )
    return ExternalCapabilityRiskClassification(classification_id=classification_id, **kwargs)


def build_external_capability_risk_map(risk_map_id: str, **kwargs: Any) -> ExternalCapabilityRiskMap:
    return ExternalCapabilityRiskMap(risk_map_id=risk_map_id, version=V0325_VERSION, **kwargs)


def build_external_capability_boundary_map(boundary_map_id: str, **kwargs: Any) -> ExternalCapabilityBoundaryMap:
    return ExternalCapabilityBoundaryMap(boundary_map_id=boundary_map_id, version=V0325_VERSION, **kwargs)


def build_external_capability_no_op_recommendation(no_op_id: str, **kwargs: Any) -> ExternalCapabilityNoOpRecommendation:
    return ExternalCapabilityNoOpRecommendation(no_op_id=no_op_id, **kwargs)


def build_external_capability_future_gate_item(
    future_gate_id: str,
    gate_kind: str,
    **kwargs: Any,
) -> ExternalCapabilityFutureGateItem:
    return ExternalCapabilityFutureGateItem(future_gate_id=future_gate_id, gate_kind=gate_kind, **kwargs)


def build_external_capability_risk_classification_input(
    classification_input_id: str,
    **kwargs: Any,
) -> ExternalCapabilityRiskClassificationInput:
    return ExternalCapabilityRiskClassificationInput(classification_input_id=classification_input_id, **kwargs)


def build_external_capability_risk_classification_finding(
    finding_id: str,
    classification_input_id: str,
    source_ref_ids: list[str],
    target_manifest_candidate_id: str | None,
    risk_class: ExternalCapabilityRiskClass | str,
    route: ExternalCapabilityRiskRoute | str,
    severity: ExternalCapabilityRiskSeverity | str,
    summary: str,
    **kwargs: Any,
) -> ExternalCapabilityRiskClassificationFinding:
    return ExternalCapabilityRiskClassificationFinding(
        finding_id=finding_id,
        classification_input_id=classification_input_id,
        source_ref_ids=list(source_ref_ids),
        target_manifest_candidate_id=target_manifest_candidate_id,
        risk_class=risk_class,
        route=route,
        severity=severity,
        summary=summary,
        **kwargs,
    )


def build_external_capability_risk_classification_report(
    report_id: str,
    classification_input_id: str,
    **kwargs: Any,
) -> ExternalCapabilityRiskClassificationReport:
    return ExternalCapabilityRiskClassificationReport(
        report_id=report_id,
        version=V0325_VERSION,
        classification_input_id=classification_input_id,
        **kwargs,
    )


def build_external_capability_risk_classification_run_preview(
    run_preview_id: str = "external_capability_risk_classification_run_preview:v0.32.5",
    **kwargs: Any,
) -> ExternalCapabilityRiskClassificationRunPreview:
    return ExternalCapabilityRiskClassificationRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_external_capability_risk_no_runtime_guarantee(
    guarantee_id: str = "external_capability_risk_no_runtime_guarantee:v0.32.5",
    evidence_refs: list[str] | None = None,
    metadata: dict[str, Any] | None = None,
) -> ExternalCapabilityRiskNoRuntimeGuarantee:
    return ExternalCapabilityRiskNoRuntimeGuarantee(
        guarantee_id=guarantee_id,
        version=V0325_VERSION,
        evidence_refs=list(evidence_refs or []),
        metadata=dict(metadata or {}),
    )


def build_v0325_readiness_report(
    report_id: str = "v0325_readiness_report",
    classification_report_id: str | None = None,
    risk_map_id: str | None = None,
    boundary_map_id: str | None = None,
    **kwargs: Any,
) -> V0325ReadinessReport:
    return V0325ReadinessReport(
        report_id=report_id,
        version=V0325_VERSION,
        classification_report_id=classification_report_id,
        risk_map_id=risk_map_id,
        boundary_map_id=boundary_map_id,
        **kwargs,
    )


def classify_manifest_candidate_risk(candidate: ExternalManifestCandidateBase) -> ExternalCapabilityRiskClass:
    surfaces = {ExternalManifestRiskSurfaceKind(value) for value in candidate.risk_surfaces}
    if not surfaces:
        return ExternalCapabilityRiskClass.SAFE_DESCRIPTIVE
    if surfaces <= {ExternalManifestRiskSurfaceKind.UNKNOWN}:
        return ExternalCapabilityRiskClass.NO_OP
    if surfaces & {
        ExternalManifestRiskSurfaceKind.REFERENCE_CODE_EXECUTION,
        ExternalManifestRiskSurfaceKind.SECRET_FILE_READ,
        ExternalManifestRiskSurfaceKind.COMMAND_EXECUTION,
        ExternalManifestRiskSurfaceKind.DEPENDENCY_INSTALL,
        ExternalManifestRiskSurfaceKind.RUNTIME_IMPORT,
    }:
        return ExternalCapabilityRiskClass.BLOCKED
    if surfaces & {
        ExternalManifestRiskSurfaceKind.PROVIDER_INVOCATION,
        ExternalManifestRiskSurfaceKind.GATEWAY_CONNECTION,
        ExternalManifestRiskSurfaceKind.CHANNEL_ACCESS,
        ExternalManifestRiskSurfaceKind.MESSAGE_SEND,
        ExternalManifestRiskSurfaceKind.WEBHOOK_CALL,
        ExternalManifestRiskSurfaceKind.NETWORK_ACCESS,
        ExternalManifestRiskSurfaceKind.CREDENTIAL_ACCESS,
        ExternalManifestRiskSurfaceKind.BROWSER_AUTOMATION,
        ExternalManifestRiskSurfaceKind.RPA_CONTROL,
    }:
        return ExternalCapabilityRiskClass.DOMINION_REQUIRED
    if surfaces & {
        ExternalManifestRiskSurfaceKind.PLUGIN_LOADING,
        ExternalManifestRiskSurfaceKind.EXTERNAL_PLUGIN_LOADING,
        ExternalManifestRiskSurfaceKind.TOOL_REGISTRATION,
        ExternalManifestRiskSurfaceKind.TOOL_INVOCATION,
        ExternalManifestRiskSurfaceKind.MISSION_INSTALLATION,
        ExternalManifestRiskSurfaceKind.MISSION_EXECUTION,
        ExternalManifestRiskSurfaceKind.REGISTRY_MUTATION,
        ExternalManifestRiskSurfaceKind.MEMORY_MUTATION,
        ExternalManifestRiskSurfaceKind.PRIVATE_DATA_EXPOSURE,
        ExternalManifestRiskSurfaceKind.RAW_OUTPUT_PERSISTENCE,
        ExternalManifestRiskSurfaceKind.OCEL_EMISSION,
    }:
        return ExternalCapabilityRiskClass.REQUIRES_REVIEW
    return ExternalCapabilityRiskClass.SAFE_DESCRIPTIVE


def infer_risk_route_from_class_and_surfaces(
    risk_class: ExternalCapabilityRiskClass | str,
    risk_surfaces: list[ExternalManifestRiskSurfaceKind | str] | list[str],
) -> ExternalCapabilityRiskRoute:
    risk_class = ExternalCapabilityRiskClass(risk_class)
    if risk_class == ExternalCapabilityRiskClass.SAFE_DESCRIPTIVE:
        return ExternalCapabilityRiskRoute.DESCRIBE_ONLY
    if risk_class == ExternalCapabilityRiskClass.DIGESTIBLE_PATTERN:
        return ExternalCapabilityRiskRoute.SEND_TO_V0326_DIGESTION_GENERATOR
    if risk_class == ExternalCapabilityRiskClass.DOMINION_REQUIRED:
        return ExternalCapabilityRiskRoute.SEND_TO_V0328_DOMINION_EMITTER
    if risk_class == ExternalCapabilityRiskClass.REQUIRES_REVIEW:
        return ExternalCapabilityRiskRoute.REQUIRE_REVIEW
    if risk_class == ExternalCapabilityRiskClass.BLOCKED:
        return ExternalCapabilityRiskRoute.BLOCK
    if risk_class == ExternalCapabilityRiskClass.FUTURE_TRACK:
        return ExternalCapabilityRiskRoute.REQUIRE_FUTURE_GATE
    if risk_class == ExternalCapabilityRiskClass.NO_OP:
        return ExternalCapabilityRiskRoute.NO_OP
    return ExternalCapabilityRiskRoute.REQUIRE_REVIEW if risk_surfaces else ExternalCapabilityRiskRoute.UNKNOWN


def infer_boundary_kinds_from_risk_surfaces(
    risk_surfaces: list[ExternalManifestRiskSurfaceKind | str] | list[str],
) -> list[ExternalCapabilityBoundaryKind]:
    mapping = {
        ExternalManifestRiskSurfaceKind.REFERENCE_CODE_EXECUTION: ExternalCapabilityBoundaryKind.NO_REFERENCE_CODE_EXECUTION,
        ExternalManifestRiskSurfaceKind.DEPENDENCY_INSTALL: ExternalCapabilityBoundaryKind.NO_DEPENDENCY_INSTALL,
        ExternalManifestRiskSurfaceKind.RUNTIME_IMPORT: ExternalCapabilityBoundaryKind.NO_RUNTIME_IMPORT,
        ExternalManifestRiskSurfaceKind.PLUGIN_LOADING: ExternalCapabilityBoundaryKind.NO_PLUGIN_LOADING,
        ExternalManifestRiskSurfaceKind.EXTERNAL_PLUGIN_LOADING: ExternalCapabilityBoundaryKind.NO_PLUGIN_LOADING,
        ExternalManifestRiskSurfaceKind.TOOL_REGISTRATION: ExternalCapabilityBoundaryKind.NO_TOOL_REGISTRATION,
        ExternalManifestRiskSurfaceKind.TOOL_INVOCATION: ExternalCapabilityBoundaryKind.NO_TOOL_INVOCATION,
        ExternalManifestRiskSurfaceKind.MISSION_INSTALLATION: ExternalCapabilityBoundaryKind.NO_MISSION_INSTALLATION,
        ExternalManifestRiskSurfaceKind.MISSION_EXECUTION: ExternalCapabilityBoundaryKind.NO_MISSION_EXECUTION,
        ExternalManifestRiskSurfaceKind.PROVIDER_INVOCATION: ExternalCapabilityBoundaryKind.NO_PROVIDER_INVOCATION,
        ExternalManifestRiskSurfaceKind.GATEWAY_CONNECTION: ExternalCapabilityBoundaryKind.NO_GATEWAY_CONNECTION,
        ExternalManifestRiskSurfaceKind.CHANNEL_ACCESS: ExternalCapabilityBoundaryKind.NO_CHANNEL_ACCESS,
        ExternalManifestRiskSurfaceKind.MESSAGE_SEND: ExternalCapabilityBoundaryKind.NO_MESSAGE_SEND,
        ExternalManifestRiskSurfaceKind.WEBHOOK_CALL: ExternalCapabilityBoundaryKind.NO_WEBHOOK_CALL,
        ExternalManifestRiskSurfaceKind.NETWORK_ACCESS: ExternalCapabilityBoundaryKind.NO_NETWORK_ACCESS,
        ExternalManifestRiskSurfaceKind.CREDENTIAL_ACCESS: ExternalCapabilityBoundaryKind.NO_CREDENTIAL_ACCESS,
        ExternalManifestRiskSurfaceKind.SECRET_FILE_READ: ExternalCapabilityBoundaryKind.NO_SECRET_FILE_READ,
        ExternalManifestRiskSurfaceKind.COMMAND_EXECUTION: ExternalCapabilityBoundaryKind.NO_COMMAND_EXECUTION,
        ExternalManifestRiskSurfaceKind.BROWSER_AUTOMATION: ExternalCapabilityBoundaryKind.NO_BROWSER_AUTOMATION,
        ExternalManifestRiskSurfaceKind.RPA_CONTROL: ExternalCapabilityBoundaryKind.NO_RPA_CONTROL,
        ExternalManifestRiskSurfaceKind.MEMORY_MUTATION: ExternalCapabilityBoundaryKind.NO_MEMORY_MUTATION,
        ExternalManifestRiskSurfaceKind.REGISTRY_MUTATION: ExternalCapabilityBoundaryKind.NO_REGISTRY_MUTATION,
        ExternalManifestRiskSurfaceKind.PRIVATE_DATA_EXPOSURE: ExternalCapabilityBoundaryKind.NO_PRIVATE_DATA_ACCESS,
        ExternalManifestRiskSurfaceKind.RAW_OUTPUT_PERSISTENCE: ExternalCapabilityBoundaryKind.NO_RAW_OUTPUT_PERSISTENCE,
        ExternalManifestRiskSurfaceKind.OCEL_EMISSION: ExternalCapabilityBoundaryKind.NO_OCEL_EMISSION,
        ExternalManifestRiskSurfaceKind.UNKNOWN: ExternalCapabilityBoundaryKind.UNKNOWN,
    }
    output: list[ExternalCapabilityBoundaryKind] = [ExternalCapabilityBoundaryKind.NO_EXECUTION]
    for surface in risk_surfaces:
        boundary = mapping.get(ExternalManifestRiskSurfaceKind(surface), ExternalCapabilityBoundaryKind.UNKNOWN)
        if boundary not in output:
            output.append(boundary)
    return output


def infer_review_requirements_from_risk_surfaces(
    risk_surfaces: list[ExternalManifestRiskSurfaceKind | str] | list[str],
) -> list[ExternalCapabilityReviewRequirementKind]:
    mapping = {
        ExternalManifestRiskSurfaceKind.CREDENTIAL_ACCESS: ExternalCapabilityReviewRequirementKind.CREDENTIAL_REVIEW,
        ExternalManifestRiskSurfaceKind.NETWORK_ACCESS: ExternalCapabilityReviewRequirementKind.NETWORK_REVIEW,
        ExternalManifestRiskSurfaceKind.COMMAND_EXECUTION: ExternalCapabilityReviewRequirementKind.COMMAND_REVIEW,
        ExternalManifestRiskSurfaceKind.PROVIDER_INVOCATION: ExternalCapabilityReviewRequirementKind.PROVIDER_REVIEW,
        ExternalManifestRiskSurfaceKind.PLUGIN_LOADING: ExternalCapabilityReviewRequirementKind.PLUGIN_REVIEW,
        ExternalManifestRiskSurfaceKind.EXTERNAL_PLUGIN_LOADING: ExternalCapabilityReviewRequirementKind.PLUGIN_REVIEW,
        ExternalManifestRiskSurfaceKind.GATEWAY_CONNECTION: ExternalCapabilityReviewRequirementKind.GATEWAY_REVIEW,
        ExternalManifestRiskSurfaceKind.CHANNEL_ACCESS: ExternalCapabilityReviewRequirementKind.GATEWAY_REVIEW,
        ExternalManifestRiskSurfaceKind.MESSAGE_SEND: ExternalCapabilityReviewRequirementKind.GATEWAY_REVIEW,
        ExternalManifestRiskSurfaceKind.WEBHOOK_CALL: ExternalCapabilityReviewRequirementKind.GATEWAY_REVIEW,
        ExternalManifestRiskSurfaceKind.MEMORY_MUTATION: ExternalCapabilityReviewRequirementKind.MEMORY_REVIEW,
        ExternalManifestRiskSurfaceKind.PRIVATE_DATA_EXPOSURE: ExternalCapabilityReviewRequirementKind.PRIVACY_REVIEW,
        ExternalManifestRiskSurfaceKind.REGISTRY_MUTATION: ExternalCapabilityReviewRequirementKind.REGISTRY_REVIEW,
        ExternalManifestRiskSurfaceKind.TOOL_REGISTRATION: ExternalCapabilityReviewRequirementKind.REGISTRY_REVIEW,
        ExternalManifestRiskSurfaceKind.OCEL_EMISSION: ExternalCapabilityReviewRequirementKind.OCEL_TRACE_REVIEW,
        ExternalManifestRiskSurfaceKind.RAW_OUTPUT_PERSISTENCE: ExternalCapabilityReviewRequirementKind.EVIDENCE_REVIEW,
        ExternalManifestRiskSurfaceKind.UNKNOWN: ExternalCapabilityReviewRequirementKind.EVIDENCE_REVIEW,
    }
    output: list[ExternalCapabilityReviewRequirementKind] = []
    for surface in risk_surfaces:
        review = mapping.get(ExternalManifestRiskSurfaceKind(surface), ExternalCapabilityReviewRequirementKind.SECURITY_REVIEW)
        if review not in output:
            output.append(review)
    return output


def capability_classification_is_not_permission(classification: ExternalCapabilityRiskClassification) -> bool:
    return (
        classification.ready_for_capability_permission is False
        and classification.ready_for_runtime_certification is False
        and classification.ready_for_execution is False
        and classification.permission is False
        and classification.digestion_candidate is False
        and classification.dominion_target is False
    )


def risk_map_is_not_permission_map(risk_map: ExternalCapabilityRiskMap) -> bool:
    return risk_map.ready_for_execution is False and risk_map.permission_map is False


def boundary_map_is_not_runtime_enforcement(boundary_map: ExternalCapabilityBoundaryMap) -> bool:
    return (
        boundary_map.ready_for_execution is False
        and boundary_map.ready_for_runtime_enforcement is False
        and boundary_map.runtime_enforcement is False
    )


def v0325_readiness_report_is_not_runtime_ready(report: V0325ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_capability_permission is False
        and report.ready_for_runtime_certification is False
        and report.ready_for_digestion_candidate_creation is False
        and report.ready_for_internal_candidate_creation is False
        and report.ready_for_dominion_target_creation is False
        and report.ready_for_dominion_decision_creation is False
        and report.ready_for_plugin_loading is False
        and report.ready_for_tool_registration is False
        and report.ready_for_tool_invocation is False
        and report.ready_for_mission_installation is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_gateway_connection is False
        and report.ready_for_network_access is False
        and report.ready_for_credential_access is False
        and report.ready_for_command_execution is False
    )
