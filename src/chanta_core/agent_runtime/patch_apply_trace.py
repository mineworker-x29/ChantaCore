from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .agentic_operation_cycle import AgenticOperationRunPacket
from .boundary import _require_non_blank, _validate_string_list
from .patch_apply_candidate import ApplyCandidateEnvelope
from .patch_apply_dry_run import DryRunApplySimulationResult
from .patch_apply_engine import SandboxPatchApplyResult
from .patch_apply_validation import SandboxPostApplyValidationReport


V0367_VERSION = "v0.36.7"
V0367_RELEASE_NAME = "v0.36.7 Patch Apply Sandbox OCEL Trace Packet"
MAX_TRACE_ATTRIBUTE_CHARS = 240

PROHIBITED_PAYLOAD_PATTERNS = (
    "secret",
    "key",
    "token",
    "credential",
    "pem",
    "id_rsa",
    "id_ed25519",
)

PROHIBITED_RUNTIME_ACTIONS = (
    "trace_persistence",
    "ocel_file_write",
    "jsonl_write",
    "log_write",
    "database_write",
    "sandbox_file_write",
    "live_workspace_write",
    "patch_application",
    "apply_patch",
    "git_apply",
    "shell_execution",
    "test_execution",
    "dependency_install",
    "reference_execution",
    "reference_import",
    "external_agent_execution",
    "claude_code_invocation",
    "codex_cli_invocation",
    "dominion_runtime",
    "provider_invocation",
    "network_access",
    "credential_access",
    "secret_read",
)

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ocel_file_write",
    "ready_for_jsonl_trace_write",
    "ready_for_log_write",
    "ready_for_database_write",
    "ready_for_sandbox_file_write",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_test_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_reference_execution",
    "ready_for_reference_import",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_dominion_runtime",
    "ready_for_infinite_agent_loop",
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_independent_agent_runtime",
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)


class PatchApplyTraceEventKind(StrEnum):
    APPLY_CANDIDATE_CREATED = "apply_candidate_created"
    HUMAN_APPROVAL_CONTRACT_ATTACHED = "human_approval_contract_attached"
    HUMAN_APPROVAL_CONTRACT_VALIDATED = "human_approval_contract_validated"
    DRY_RUN_SIMULATION_STARTED = "dry_run_simulation_started"
    DRY_RUN_SIMULATION_COMPLETED = "dry_run_simulation_completed"
    DRY_RUN_CONFLICT_DETECTED = "dry_run_conflict_detected"
    SANDBOX_WORKSPACE_POLICY_CREATED = "sandbox_workspace_policy_created"
    SANDBOX_MANIFEST_CREATED = "sandbox_manifest_created"
    SANDBOX_WORKSPACE_MATERIALIZATION_PLANNED = "sandbox_workspace_materialization_planned"
    SANDBOX_WORKSPACE_MATERIALIZED = "sandbox_workspace_materialized"
    SANDBOX_FILE_WRITE_RECORDED = "sandbox_file_write_recorded"
    SANDBOX_PATCH_APPLY_STARTED = "sandbox_patch_apply_started"
    SANDBOX_PATCH_APPLY_COMPLETED = "sandbox_patch_apply_completed"
    SANDBOX_PATCH_APPLY_BLOCKED = "sandbox_patch_apply_blocked"
    POST_APPLY_VALIDATION_STARTED = "post_apply_validation_started"
    POST_APPLY_VALIDATION_COMPLETED = "post_apply_validation_completed"
    RECONCILIATION_REPORT_CREATED = "reconciliation_report_created"
    SAFETY_REGRESSION_SCAN_COMPLETED = "safety_regression_scan_completed"
    SCOPE_VALIDATION_COMPLETED = "scope_validation_completed"
    AGENTIC_OPERATION_CYCLE_STARTED = "agentic_operation_cycle_started"
    AGENTIC_OPERATION_STEP_RECORDED = "agentic_operation_step_recorded"
    AGENTIC_OPERATION_CYCLE_COMPLETED = "agentic_operation_cycle_completed"
    AGENTIC_OPERATION_CYCLE_STOPPED = "agentic_operation_cycle_stopped"
    HUMAN_HANDOFF_REQUIRED = "human_handoff_required"
    LIVE_WORKSPACE_WRITE_BLOCKED = "live_workspace_write_blocked"
    EXTERNAL_AGENT_EXECUTION_BLOCKED = "external_agent_execution_blocked"
    DOMINION_RUNTIME_BLOCKED = "dominion_runtime_blocked"
    INFINITE_AGENT_LOOP_BLOCKED = "infinite_agent_loop_blocked"
    AUTOMATIC_REPAIR_LOOP_BLOCKED = "automatic_repair_loop_blocked"
    TRACE_PACKET_CREATED = "trace_packet_created"
    TRACE_EMISSION_BLOCKED = "trace_emission_blocked"
    NO_OP_EVENT = "no_op_event"
    UNKNOWN = "unknown"


class PatchApplyTraceObjectType(StrEnum):
    PATCH_APPLY_SANDBOX_BOUNDARY = "patch_apply_sandbox_boundary"
    APPLY_CANDIDATE_ENVELOPE = "apply_candidate_envelope"
    HUMAN_APPROVAL_CONTRACT = "human_approval_contract"
    DRY_RUN_APPLY_SIMULATION_RESULT = "dry_run_apply_simulation_result"
    DRY_RUN_CONFLICT = "dry_run_conflict"
    SANDBOX_WORKSPACE_MANIFEST = "sandbox_workspace_manifest"
    SANDBOX_WORKSPACE_PLAN = "sandbox_workspace_plan"
    SANDBOX_OVERLAY_ENTRY = "sandbox_overlay_entry"
    SANDBOX_FILE_MAP_ENTRY = "sandbox_file_map_entry"
    SANDBOX_PATCH_APPLY_INPUT = "sandbox_patch_apply_input"
    SANDBOX_PATCH_APPLY_RESULT = "sandbox_patch_apply_result"
    SANDBOX_FILE_WRITE_RECORD = "sandbox_file_write_record"
    SANDBOX_ENGINE_FILE_RESULT = "sandbox_engine_file_result"
    SANDBOX_POST_APPLY_VALIDATION_REPORT = "sandbox_post_apply_validation_report"
    SANDBOX_RECONCILIATION_REPORT = "sandbox_reconciliation_report"
    SANDBOX_SAFETY_REGRESSION_REPORT = "sandbox_safety_regression_report"
    SANDBOX_SCOPE_VALIDATION_REPORT = "sandbox_scope_validation_report"
    AGENTIC_OPERATION_INTENT = "agentic_operation_intent"
    AGENTIC_OPERATION_RUN_PACKET = "agentic_operation_run_packet"
    AGENTIC_OPERATION_STEP_RECORD = "agentic_operation_step_record"
    AGENTIC_OPERATION_RESULT = "agentic_operation_result"
    AGENTIC_OPERATION_STOP_REASON = "agentic_operation_stop_reason"
    DIGESTION_DOMINION_RECORD = "digestion_dominion_record"
    EXTERNAL_AGENT_BLOCK_RECORD = "external_agent_block_record"
    TRACE_PACKET = "trace_packet"
    UNKNOWN = "unknown"


class PatchApplyTraceRelationType(StrEnum):
    CANDIDATE_USES_APPROVAL_CONTRACT = "candidate_uses_approval_contract"
    CANDIDATE_USES_DIFF_PROPOSAL = "candidate_uses_diff_proposal"
    DRY_RUN_USES_CANDIDATE = "dry_run_uses_candidate"
    DRY_RUN_PRODUCES_SIMULATED_DELTA = "dry_run_produces_simulated_delta"
    DRY_RUN_DETECTS_CONFLICT = "dry_run_detects_conflict"
    MANIFEST_USES_DRY_RUN_RESULT = "manifest_uses_dry_run_result"
    MANIFEST_MAPS_TARGET_FILE = "manifest_maps_target_file"
    OVERLAY_ENTRY_USES_SIMULATED_DELTA = "overlay_entry_uses_simulated_delta"
    SANDBOX_APPLY_USES_MANIFEST = "sandbox_apply_uses_manifest"
    SANDBOX_APPLY_WRITES_SANDBOX_FILE = "sandbox_apply_writes_sandbox_file"
    SANDBOX_APPLY_PRODUCES_WRITE_RECORD = "sandbox_apply_produces_write_record"
    VALIDATION_USES_SANDBOX_APPLY_RESULT = "validation_uses_sandbox_apply_result"
    VALIDATION_READS_SANDBOX_FILE = "validation_reads_sandbox_file"
    RECONCILIATION_COMPARES_EXPECTED_ACTUAL = "reconciliation_compares_expected_actual"
    SAFETY_SCAN_CHECKS_VALIDATION_RESULT = "safety_scan_checks_validation_result"
    AGENTIC_CYCLE_USES_VALIDATION_REPORT = "agentic_cycle_uses_validation_report"
    AGENTIC_CYCLE_RECORDS_STEP = "agentic_cycle_records_step"
    AGENTIC_CYCLE_PRODUCES_RESULT = "agentic_cycle_produces_result"
    RESULT_HAS_STOP_REASON = "result_has_stop_reason"
    TRACE_PACKET_CONTAINS_EVENT = "trace_packet_contains_event"
    TRACE_PACKET_CONTAINS_OBJECT = "trace_packet_contains_object"
    TRACE_PACKET_CONTAINS_RELATION = "trace_packet_contains_relation"
    DIGESTION_POLICY_BLOCKS_DOMINION = "digestion_policy_blocks_dominion"
    EXTERNAL_AGENT_PATTERN_BLOCKED = "external_agent_pattern_blocked"
    LIVE_WRITE_BLOCKED_BY_BOUNDARY = "live_write_blocked_by_boundary"
    UNKNOWN = "unknown"


class PatchApplyTraceAttributeKind(StrEnum):
    SUMMARY = "summary"
    STATUS = "status"
    READINESS_LEVEL = "readiness_level"
    DECISION_KIND = "decision_kind"
    RISK_KIND = "risk_kind"
    SEVERITY = "severity"
    PHASE = "phase"
    TARGET_PATH_REF = "target_path_ref"
    SANDBOX_ROOT_REF = "sandbox_root_ref"
    SANDBOX_PATH_REF = "sandbox_path_ref"
    WRITE_RECORD_REF = "write_record_ref"
    APPLY_RESULT_REF = "apply_result_ref"
    VALIDATION_REPORT_REF = "validation_report_ref"
    RECONCILIATION_REPORT_REF = "reconciliation_report_ref"
    AGENTIC_RUN_PACKET_REF = "agentic_run_packet_ref"
    STOP_REASON_REF = "stop_reason_ref"
    HUMAN_HANDOFF_REQUIRED = "human_handoff_required"
    PRODUCTION_CERTIFIED = "production_certified"
    READY_FOR_EXECUTION = "ready_for_execution"
    LIVE_WRITE_PERFORMED = "live_write_performed"
    USED_APPLY_PATCH = "used_apply_patch"
    USED_GIT_APPLY = "used_git_apply"
    USED_SHELL = "used_shell"
    REDACTION_STATUS = "redaction_status"
    TRUNCATION_STATUS = "truncation_status"
    SOURCE_REF = "source_ref"
    EVIDENCE_REF = "evidence_ref"
    TIMESTAMP = "timestamp"
    UNKNOWN = "unknown"


class PatchApplyTraceSinkKind(StrEnum):
    RETURNED_TRACE_PACKET = "returned_trace_packet"
    IN_MEMORY_TEST_SINK = "in_memory_test_sink"
    DISABLED = "disabled"
    FUTURE_INTERNAL_OCEL_STORE = "future_internal_ocel_store"
    EXTERNAL_TRACE_SINK_BLOCKED = "external_trace_sink_blocked"
    UNKNOWN = "unknown"


class PatchApplyTraceStatus(StrEnum):
    UNKNOWN = "unknown"
    PLANNED = "planned"
    POLICY_CHECKED = "policy_checked"
    EMITTED_AS_PACKET = "emitted_as_packet"
    EMITTED_TO_IN_MEMORY_SINK = "emitted_to_in_memory_sink"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class PatchApplyTraceDecisionKind(StrEnum):
    ALLOW_TRACE_PACKET_CREATION = "allow_trace_packet_creation"
    ALLOW_IN_MEMORY_TEST_SINK = "allow_in_memory_test_sink"
    DENY = "deny"
    BLOCK = "block"
    SKIP = "skip"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class PatchApplyTraceRiskKind(StrEnum):
    RAW_DIFF_PERSISTENCE_RISK = "raw_diff_persistence_risk"
    RAW_SOURCE_PERSISTENCE_RISK = "raw_source_persistence_risk"
    RAW_SANDBOX_FILE_PERSISTENCE_RISK = "raw_sandbox_file_persistence_risk"
    RAW_VALIDATION_REPORT_PERSISTENCE_RISK = "raw_validation_report_persistence_risk"
    SECRET_CONTENT_TRACE_RISK = "secret_content_trace_risk"
    CREDENTIAL_CONTENT_TRACE_RISK = "credential_content_trace_risk"
    TOKEN_CONTENT_TRACE_RISK = "token_content_trace_risk"
    UNBOUNDED_PAYLOAD_RISK = "unbounded_payload_risk"
    FULL_FILE_CONTENT_TRACE_RISK = "full_file_content_trace_risk"
    PATCH_APPLY_CONFUSION_RISK = "patch_apply_confusion_risk"
    LIVE_WRITE_CONFUSION_RISK = "live_write_confusion_risk"
    SANDBOX_WRITE_CONFUSION_RISK = "sandbox_write_confusion_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    EXTERNAL_AGENT_EXECUTION_CONFUSION_RISK = "external_agent_execution_confusion_risk"
    DOMINION_RUNTIME_CONFUSION_RISK = "dominion_runtime_confusion_risk"
    INFINITE_AGENT_LOOP_RISK = "infinite_agent_loop_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    EXTERNAL_TRACE_SINK_RISK = "external_trace_sink_risk"
    UNKNOWN = "unknown"


class PatchApplyTraceSourceKind(StrEnum):
    V0366_AGENTIC_OPERATION_RUN_PACKET = "v0366_agentic_operation_run_packet"
    V0366_AGENTIC_OPERATION_RESULT = "v0366_agentic_operation_result"
    V0366_AGENTIC_OPERATION_STEP_RECORD = "v0366_agentic_operation_step_record"
    V0365_POST_APPLY_VALIDATION_REPORT = "v0365_post_apply_validation_report"
    V0365_RECONCILIATION_REPORT = "v0365_reconciliation_report"
    V0365_SAFETY_REGRESSION_REPORT = "v0365_safety_regression_report"
    V0365_SCOPE_VALIDATION_REPORT = "v0365_scope_validation_report"
    V0364_SANDBOX_PATCH_APPLY_RESULT = "v0364_sandbox_patch_apply_result"
    V0364_SANDBOX_FILE_WRITE_RECORD = "v0364_sandbox_file_write_record"
    V0363_SANDBOX_WORKSPACE_MANIFEST = "v0363_sandbox_workspace_manifest"
    V0363_SANDBOX_WORKSPACE_PLAN = "v0363_sandbox_workspace_plan"
    V0362_DRY_RUN_APPLY_SIMULATION_RESULT = "v0362_dry_run_apply_simulation_result"
    V0361_APPLY_CANDIDATE_ENVELOPE = "v0361_apply_candidate_envelope"
    V0361_HUMAN_APPROVAL_CONTRACT = "v0361_human_approval_contract"
    V0360_PATCH_APPLY_SANDBOX_BOUNDARY = "v0360_patch_apply_sandbox_boundary"
    V0359_CONTROLLED_PATCH_PROPOSAL_CONSOLIDATION = "v0359_controlled_patch_proposal_consolidation"
    DIGESTION_DOMINION_POLICY_NOTE = "digestion_dominion_policy_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class PatchApplyTraceReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    TRACE_CONTRACT_READY = "trace_contract_ready"
    TRACE_PACKET_READY = "trace_packet_ready"
    SANDBOX_LIFECYCLE_TRACE_READY = "sandbox_lifecycle_trace_ready"
    AGENTIC_OPERATION_TRACE_READY = "agentic_operation_trace_ready"
    DESIGN_HANDOFF_READY_FOR_V0368 = "design_handoff_ready_for_v0368"
    DESIGN_HANDOFF_READY_FOR_V0369 = "design_handoff_ready_for_v0369"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchApplyTraceLifecyclePhase(StrEnum):
    PROPOSAL_REVIEW = "proposal_review"
    APPLY_CANDIDATE = "apply_candidate"
    HUMAN_APPROVAL = "human_approval"
    DRY_RUN = "dry_run"
    SANDBOX_WORKSPACE = "sandbox_workspace"
    SANDBOX_APPLY = "sandbox_apply"
    POST_APPLY_VALIDATION = "post_apply_validation"
    BOUNDED_AGENTIC_OPERATION = "bounded_agentic_operation"
    HUMAN_HANDOFF = "human_handoff"
    DIGESTION_DOMINION_BOUNDARY = "digestion_dominion_boundary"
    TRACE_EMISSION = "trace_emission"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0367_VERSION not in version:
        raise ValueError("version must include v0.36.7")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.7")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


def _safe_artifact_id(artifact: Any, *names: str, fallback: str = "missing") -> str | None:
    if artifact is None:
        return None
    for name in names:
        value = getattr(artifact, name, None)
        if value:
            return str(value)
    return fallback


def _artifact_bool(artifact: Any, name: str, default: bool = False) -> bool:
    if artifact is None:
        return default
    value = getattr(artifact, name, default)
    return bool(value)


def _artifact_summary(artifact: Any, fallback: str) -> str:
    if artifact is None:
        return fallback
    return str(getattr(artifact, "summary", fallback) or fallback)


def sanitize_patch_apply_trace_attribute_value(value: Any, max_chars: int = MAX_TRACE_ATTRIBUTE_CHARS) -> str:
    if max_chars < 0:
        raise ValueError("max_chars must be >= 0")
    text = str(value)
    redacted = text
    for token in PROHIBITED_PAYLOAD_PATTERNS:
        for variant in (token, token.upper(), token.capitalize()):
            redacted = redacted.replace(variant, "[redacted]")
    if len(redacted) > max_chars:
        return redacted[:max_chars]
    return redacted


def _contains_prohibited_payload(value: str) -> bool:
    lowered = value.lower()
    return any(token in lowered for token in PROHIBITED_PAYLOAD_PATTERNS)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceFlagSet:
    flag_set_id: str
    version: str
    patch_apply_trace_layer_constructed: bool
    trace_packet_creation_available: bool
    sandbox_lifecycle_trace_available: bool
    agentic_operation_trace_available: bool
    digestion_dominion_trace_metadata_available: bool
    trace_validation_available: bool
    ready_for_v0368_cli_sandbox_apply_agentic_surface: bool
    ready_for_v0369_patch_apply_sandbox_consolidation: bool
    ready_for_patch_apply_sandbox_trace_packet_creation: bool
    ready_for_bounded_patch_apply_ocel_trace_emission: bool
    ready_for_sandbox_apply_lifecycle_trace: bool
    ready_for_agentic_operation_lifecycle_trace: bool
    ready_for_digestion_dominion_trace_metadata: bool
    ready_for_future_cli_trace_preview_input: bool
    ready_for_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_jsonl_trace_write: bool = False
    ready_for_log_write: bool = False
    ready_for_database_write: bool = False
    ready_for_sandbox_file_write: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceSourceRef:
    source_ref_id: str
    source_kind: PatchApplyTraceSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyTraceSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTracePolicy:
    trace_policy_id: str
    version: str
    allowed_event_kinds: list[PatchApplyTraceEventKind | str]
    allowed_object_types: list[PatchApplyTraceObjectType | str]
    allowed_relation_types: list[PatchApplyTraceRelationType | str]
    allowed_sink_kinds: list[PatchApplyTraceSinkKind | str]
    prohibited_attribute_kinds: list[PatchApplyTraceAttributeKind | str]
    prohibited_payload_patterns: list[str]
    max_attribute_chars: int
    max_event_count: int
    max_object_count: int
    max_relation_count: int
    allow_raw_diff: bool = False
    allow_raw_source: bool = False
    allow_raw_sandbox_file_content: bool = False
    allow_raw_validation_report: bool = False
    allow_secret_content: bool = False
    allow_credential_content: bool = False
    allow_token_content: bool = False
    allow_full_file_content: bool = False
    allow_persistent_write: bool = False
    allow_external_sink: bool = False
    allow_ocel_file_write: bool = False
    allow_jsonl_write: bool = False
    allow_log_write: bool = False
    allow_database_write: bool = False
    allow_sandbox_file_write: bool = False
    allow_live_workspace_write: bool = False
    allow_patch_application: bool = False
    allow_test_execution: bool = False
    allow_shell: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_policy_id", self.trace_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_event_kinds", self.allowed_event_kinds, PatchApplyTraceEventKind)
        _validate_enum_list("allowed_object_types", self.allowed_object_types, PatchApplyTraceObjectType)
        _validate_enum_list("allowed_relation_types", self.allowed_relation_types, PatchApplyTraceRelationType)
        _validate_enum_list("allowed_sink_kinds", self.allowed_sink_kinds, PatchApplyTraceSinkKind)
        _validate_enum_list("prohibited_attribute_kinds", self.prohibited_attribute_kinds, PatchApplyTraceAttributeKind)
        _validate_string_list("prohibited_payload_patterns", self.prohibited_payload_patterns)
        lowered_patterns = {pattern.lower() for pattern in self.prohibited_payload_patterns}
        for pattern in PROHIBITED_PAYLOAD_PATTERNS:
            if pattern not in lowered_patterns:
                raise ValueError("prohibited_payload_patterns must include secret/key/token/credential/pem/id_rsa-like patterns")
        for name in ("max_attribute_chars", "max_event_count", "max_object_count", "max_relation_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(
            self,
            (
                "allow_raw_diff",
                "allow_raw_source",
                "allow_raw_sandbox_file_content",
                "allow_raw_validation_report",
                "allow_secret_content",
                "allow_credential_content",
                "allow_token_content",
                "allow_full_file_content",
                "allow_persistent_write",
                "allow_external_sink",
                "allow_ocel_file_write",
                "allow_jsonl_write",
                "allow_log_write",
                "allow_database_write",
                "allow_sandbox_file_write",
                "allow_live_workspace_write",
                "allow_patch_application",
                "allow_test_execution",
                "allow_shell",
                "allow_external_agent_execution",
                "allow_dominion_runtime",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceAttribute:
    attribute_id: str
    attribute_kind: PatchApplyTraceAttributeKind | str
    value: str
    value_summary: str
    redacted: bool
    truncated: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("attribute_id", "value_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyTraceAttributeKind(self.attribute_kind)
        if not isinstance(self.value, str):
            raise TypeError("value must be str")
        if len(self.value) > MAX_TRACE_ATTRIBUTE_CHARS:
            raise ValueError("trace attribute value must be bounded")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceObject:
    object_id: str
    object_type: PatchApplyTraceObjectType | str
    object_label: str
    object_summary: str
    attributes: list[PatchApplyTraceAttribute]
    source_refs: list[PatchApplyTraceSourceRef]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("object_id", "object_label", "object_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyTraceObjectType(self.object_type)
        _validate_list("attributes", self.attributes)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceEvent:
    event_id: str
    event_kind: PatchApplyTraceEventKind | str
    lifecycle_phase: PatchApplyTraceLifecyclePhase | str
    event_summary: str
    related_object_ids: list[str]
    attributes: list[PatchApplyTraceAttribute]
    source_refs: list[PatchApplyTraceSourceRef]
    executed_runtime_action: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("event_id", "event_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyTraceEventKind(self.event_kind)
        PatchApplyTraceLifecyclePhase(self.lifecycle_phase)
        _validate_string_list("related_object_ids", self.related_object_ids)
        _validate_list("attributes", self.attributes)
        _validate_list("source_refs", self.source_refs)
        _validate_false(self, ("executed_runtime_action",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceRelation:
    relation_id: str
    relation_type: PatchApplyTraceRelationType | str
    source_object_id: str
    target_object_id: str
    relation_summary: str
    attributes: list[PatchApplyTraceAttribute]
    source_refs: list[PatchApplyTraceSourceRef]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("relation_id", "source_object_id", "target_object_id", "relation_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyTraceRelationType(self.relation_type)
        _validate_list("attributes", self.attributes)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxApplyLifecycleTraceRecord:
    lifecycle_record_id: str
    version: str
    apply_candidate_id: str | None
    human_approval_contract_id: str | None
    dry_run_result_id: str | None
    sandbox_manifest_id: str | None
    sandbox_apply_result_id: str | None
    post_apply_validation_report_id: str | None
    lifecycle_phases: list[PatchApplyTraceLifecyclePhase | str]
    lifecycle_summary: str
    sandbox_apply_successful: bool
    post_apply_validation_successful: bool
    live_write_performed: bool = False
    patch_application_performed: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("lifecycle_record_id", "lifecycle_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_enum_list("lifecycle_phases", self.lifecycle_phases, PatchApplyTraceLifecyclePhase)
        _validate_false(self, ("live_write_performed", "patch_application_performed", "production_certified"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticTaskLifecycleTraceRecord:
    agentic_lifecycle_record_id: str
    version: str
    agentic_run_packet_id: str | None
    operation_result_id: str | None
    stop_reason_id: str | None
    step_record_ids: list[str]
    lifecycle_summary: str
    single_cycle_only: bool
    human_handoff_required: bool
    automatic_retry_allowed: bool = False
    automatic_repair_allowed: bool = False
    independent_agent_runtime: bool = False
    multi_cycle_loop: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("agentic_lifecycle_record_id", "lifecycle_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_string_list("step_record_ids", self.step_record_ids)
        if self.single_cycle_only is not True:
            raise ValueError("single_cycle_only must be True in v0.36.7 trace metadata")
        if self.human_handoff_required is not True:
            raise ValueError("human_handoff_required must be True in v0.36.7 trace metadata")
        _validate_false(
            self,
            ("automatic_retry_allowed", "automatic_repair_allowed", "independent_agent_runtime", "multi_cycle_loop"),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class DigestionDominionApplyTraceRecord:
    digestion_trace_record_id: str
    version: str
    digestion_first_policy_applied: bool
    dominion_runtime_blocked: bool
    external_agent_execution_blocked: bool
    infinite_agent_loop_blocked: bool
    automatic_repair_loop_blocked: bool
    recursive_self_invocation_blocked: bool
    bounded_agentic_task_only: bool
    summary: str
    future_track_items: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("digestion_trace_record_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in (
            "digestion_first_policy_applied",
            "dominion_runtime_blocked",
            "external_agent_execution_blocked",
            "infinite_agent_loop_blocked",
            "automatic_repair_loop_blocked",
            "recursive_self_invocation_blocked",
            "bounded_agentic_task_only",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.7 trace metadata")
        _validate_string_list("future_track_items", self.future_track_items)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxTracePacket:
    trace_packet_id: str
    version: str
    sink_kind: PatchApplyTraceSinkKind | str
    objects: list[PatchApplyTraceObject]
    events: list[PatchApplyTraceEvent]
    relations: list[PatchApplyTraceRelation]
    attributes: list[PatchApplyTraceAttribute]
    sandbox_lifecycle_record: SandboxApplyLifecycleTraceRecord | None
    agentic_task_lifecycle_record: AgenticTaskLifecycleTraceRecord | None
    digestion_dominion_record: DigestionDominionApplyTraceRecord | None
    source_refs: list[PatchApplyTraceSourceRef]
    status: PatchApplyTraceStatus | str
    redaction_applied: bool
    truncated: bool
    summary: str
    ready_for_persistent_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_jsonl_write: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("trace_packet_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchApplyTraceSinkKind(self.sink_kind)
        PatchApplyTraceStatus(self.status)
        _validate_list("objects", self.objects)
        _validate_list("events", self.events)
        _validate_list("relations", self.relations)
        _validate_list("attributes", self.attributes)
        _validate_list("source_refs", self.source_refs)
        _validate_false(
            self,
            (
                "ready_for_persistent_write",
                "ready_for_external_sink",
                "ready_for_ocel_file_write",
                "ready_for_jsonl_write",
                "ready_for_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceEmissionInput:
    emission_input_id: str
    version: str
    requested_sink_kind: PatchApplyTraceSinkKind | str
    trace_packet: PatchApplySandboxTracePacket | None
    source_refs: list[PatchApplyTraceSourceRef]
    prohibited_runtime_actions: list[str]
    summary: str
    include_raw_diff: bool = False
    include_raw_source: bool = False
    include_raw_sandbox_file_content: bool = False
    include_raw_validation_report: bool = False
    include_secret_content: bool = False
    include_credential_content: bool = False
    include_token_content: bool = False
    allow_persistence: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("emission_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchApplyTraceSinkKind(self.requested_sink_kind)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [action for action in PROHIBITED_RUNTIME_ACTIONS if action not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing {missing}")
        _validate_false(
            self,
            (
                "include_raw_diff",
                "include_raw_source",
                "include_raw_sandbox_file_content",
                "include_raw_validation_report",
                "include_secret_content",
                "include_credential_content",
                "include_token_content",
                "allow_persistence",
                "allow_external_agent_execution",
                "allow_dominion_runtime",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceEmissionDecision:
    decision_id: str
    decision_kind: PatchApplyTraceDecisionKind | str
    status: PatchApplyTraceStatus | str
    summary: str
    allow_trace_packet_creation: bool
    allow_in_memory_test_sink: bool
    allow_persistent_write: bool = False
    allow_external_sink: bool = False
    allow_ocel_file_write: bool = False
    allow_jsonl_write: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyTraceDecisionKind(self.decision_kind)
        PatchApplyTraceStatus(self.status)
        _validate_false(
            self,
            ("allow_persistent_write", "allow_external_sink", "allow_ocel_file_write", "allow_jsonl_write", "ready_for_execution"),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceValidationFinding:
    validation_finding_id: str
    risk_kind: PatchApplyTraceRiskKind | str
    decision_kind: PatchApplyTraceDecisionKind | str
    severity: str
    summary: str
    evidence_preview: str
    blocked: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_finding_id", "severity", "summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyTraceRiskKind(self.risk_kind)
        PatchApplyTraceDecisionKind(self.decision_kind)
        if sanitize_patch_apply_trace_attribute_value(self.evidence_preview) != self.evidence_preview:
            raise ValueError("evidence_preview must be sanitized and bounded")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceValidationReport:
    validation_report_id: str
    version: str
    findings: list[PatchApplyTraceValidationFinding]
    summary: str
    validation_successful: bool
    blocked: bool
    requires_review: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("findings", self.findings)
        if any(finding.blocked for finding in self.findings) and self.validation_successful:
            raise ValueError("validation_successful cannot be true with blocked findings")
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceEmissionReport:
    emission_report_id: str
    version: str
    emission_input_id: str
    decision: PatchApplyTraceEmissionDecision
    trace_packet: PatchApplySandboxTracePacket | None
    validation_report: PatchApplyTraceValidationReport
    summary: str
    emitted: bool
    persisted: bool = False
    wrote_ocel_file: bool = False
    wrote_jsonl_file: bool = False
    wrote_log_or_database: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("emission_report_id", "emission_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_false(
            self,
            ("persisted", "wrote_ocel_file", "wrote_jsonl_file", "wrote_log_or_database", "ready_for_execution"),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceEmitter:
    emitter_id: str
    version: str
    allowed_sink_kinds: list[PatchApplyTraceSinkKind | str]
    emitter_summary: str
    persistent_write_enabled: bool = False
    external_sink_enabled: bool = False
    ocel_file_write_enabled: bool = False
    jsonl_write_enabled: bool = False
    log_database_write_enabled: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("emitter_id", "emitter_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_enum_list("allowed_sink_kinds", self.allowed_sink_kinds, PatchApplyTraceSinkKind)
        blocked_sinks = {
            PatchApplyTraceSinkKind.FUTURE_INTERNAL_OCEL_STORE,
            PatchApplyTraceSinkKind.EXTERNAL_TRACE_SINK_BLOCKED,
            PatchApplyTraceSinkKind.UNKNOWN,
        }
        if any(PatchApplyTraceSinkKind(kind) in blocked_sinks for kind in self.allowed_sink_kinds):
            raise ValueError("emitter may only allow returned packet, in-memory test sink, or disabled sink")
        _validate_false(
            self,
            (
                "persistent_write_enabled",
                "external_sink_enabled",
                "ocel_file_write_enabled",
                "jsonl_write_enabled",
                "log_database_write_enabled",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceRunPreview:
    run_preview_id: str
    emission_input_id: str
    preview_summary: str
    planned_trace_actions: list[str]
    prohibited_runtime_actions: list[str]
    ready_for_patch_apply_sandbox_trace_packet_creation: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "emission_input_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("planned_trace_actions", self.planned_trace_actions)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceNoPersistenceGuarantee:
    guarantee_id: str
    version: str
    no_trace_persistence: bool
    no_ocel_file_write: bool
    no_jsonl_write: bool
    no_log_write: bool
    no_database_write: bool
    no_external_trace_sink: bool
    no_sandbox_file_write: bool
    no_live_workspace_write: bool
    no_live_code_edit: bool
    no_additional_patch_application: bool
    no_apply_patch: bool
    no_git_apply: bool
    no_shell_execution: bool
    no_subprocess_execution: bool
    no_command_execution: bool
    no_test_execution: bool
    no_dependency_install: bool
    no_reference_execution: bool
    no_reference_import: bool
    no_external_agent_execution: bool
    no_claude_code_invocation: bool
    no_codex_cli_invocation: bool
    no_dominion_runtime: bool
    no_infinite_agent_loop: bool
    no_provider_invocation: bool
    no_network_access: bool
    no_credential_access: bool
    no_secret_read: bool
    no_autonomous_runtime: bool
    no_general_tool_execution: bool
    no_ui_runtime: bool
    no_authority_grant: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name, value in self.__dict__.items():
            if name.startswith("no_") and value is not True:
                raise ValueError(f"{name} must be True in v0.36.7")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0367ReadinessReport:
    readiness_report_id: str
    version: str
    release_name: str
    status: PatchApplyTraceStatus | str
    readiness_level: PatchApplyTraceReadinessLevel | str
    ready_for_v0368_cli_sandbox_apply_agentic_surface: bool
    ready_for_v0369_patch_apply_sandbox_consolidation: bool
    ready_for_patch_apply_sandbox_trace_packet_creation: bool
    ready_for_bounded_patch_apply_ocel_trace_emission: bool
    ready_for_sandbox_apply_lifecycle_trace: bool
    ready_for_agentic_operation_lifecycle_trace: bool
    ready_for_digestion_dominion_trace_metadata: bool
    ready_for_future_cli_trace_preview_input: bool
    ready_for_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_jsonl_trace_write: bool = False
    ready_for_log_write: bool = False
    ready_for_database_write: bool = False
    ready_for_sandbox_file_write: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    summary: str = "v0.36.7 trace packet layer is returned/in-memory metadata only"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchApplyTraceStatus(self.status)
        PatchApplyTraceReadinessLevel(self.readiness_level)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


def build_patch_apply_trace_flags(**kwargs: Any) -> PatchApplyTraceFlagSet:
    return PatchApplyTraceFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "patch_apply_trace_flags:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        patch_apply_trace_layer_constructed=kwargs.pop("patch_apply_trace_layer_constructed", True),
        trace_packet_creation_available=kwargs.pop("trace_packet_creation_available", True),
        sandbox_lifecycle_trace_available=kwargs.pop("sandbox_lifecycle_trace_available", True),
        agentic_operation_trace_available=kwargs.pop("agentic_operation_trace_available", True),
        digestion_dominion_trace_metadata_available=kwargs.pop("digestion_dominion_trace_metadata_available", True),
        trace_validation_available=kwargs.pop("trace_validation_available", True),
        ready_for_v0368_cli_sandbox_apply_agentic_surface=kwargs.pop("ready_for_v0368_cli_sandbox_apply_agentic_surface", True),
        ready_for_v0369_patch_apply_sandbox_consolidation=kwargs.pop("ready_for_v0369_patch_apply_sandbox_consolidation", True),
        ready_for_patch_apply_sandbox_trace_packet_creation=kwargs.pop("ready_for_patch_apply_sandbox_trace_packet_creation", True),
        ready_for_bounded_patch_apply_ocel_trace_emission=kwargs.pop("ready_for_bounded_patch_apply_ocel_trace_emission", True),
        ready_for_sandbox_apply_lifecycle_trace=kwargs.pop("ready_for_sandbox_apply_lifecycle_trace", True),
        ready_for_agentic_operation_lifecycle_trace=kwargs.pop("ready_for_agentic_operation_lifecycle_trace", True),
        ready_for_digestion_dominion_trace_metadata=kwargs.pop("ready_for_digestion_dominion_trace_metadata", True),
        ready_for_future_cli_trace_preview_input=kwargs.pop("ready_for_future_cli_trace_preview_input", True),
        **kwargs,
    )


def build_patch_apply_trace_source_ref(**kwargs: Any) -> PatchApplyTraceSourceRef:
    return PatchApplyTraceSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "patch_apply_trace_source_ref:v0.36.7"),
        source_kind=kwargs.pop("source_kind", PatchApplyTraceSourceKind.TEST_FIXTURE),
        source_id=kwargs.pop("source_id", "source:v0.36.7"),
        source_summary=kwargs.pop("source_summary", "patch apply trace source metadata; not execution or file access"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        **kwargs,
    )


def build_patch_apply_trace_policy(**kwargs: Any) -> PatchApplyTracePolicy:
    return PatchApplyTracePolicy(
        trace_policy_id=kwargs.pop("trace_policy_id", "patch_apply_trace_policy:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        allowed_event_kinds=kwargs.pop("allowed_event_kinds", list(PatchApplyTraceEventKind)),
        allowed_object_types=kwargs.pop("allowed_object_types", list(PatchApplyTraceObjectType)),
        allowed_relation_types=kwargs.pop("allowed_relation_types", list(PatchApplyTraceRelationType)),
        allowed_sink_kinds=kwargs.pop(
            "allowed_sink_kinds",
            [PatchApplyTraceSinkKind.RETURNED_TRACE_PACKET, PatchApplyTraceSinkKind.IN_MEMORY_TEST_SINK, PatchApplyTraceSinkKind.DISABLED],
        ),
        prohibited_attribute_kinds=kwargs.pop("prohibited_attribute_kinds", [PatchApplyTraceAttributeKind.UNKNOWN]),
        prohibited_payload_patterns=kwargs.pop("prohibited_payload_patterns", list(PROHIBITED_PAYLOAD_PATTERNS)),
        max_attribute_chars=kwargs.pop("max_attribute_chars", MAX_TRACE_ATTRIBUTE_CHARS),
        max_event_count=kwargs.pop("max_event_count", 500),
        max_object_count=kwargs.pop("max_object_count", 500),
        max_relation_count=kwargs.pop("max_relation_count", 1000),
        **kwargs,
    )


def default_patch_apply_trace_policy(**kwargs: Any) -> PatchApplyTracePolicy:
    return build_patch_apply_trace_policy(**kwargs)


def build_patch_apply_trace_attribute(**kwargs: Any) -> PatchApplyTraceAttribute:
    raw_value = kwargs.pop("value", "trace metadata only")
    max_chars = kwargs.pop("max_chars", MAX_TRACE_ATTRIBUTE_CHARS)
    sanitized = sanitize_patch_apply_trace_attribute_value(raw_value, max_chars=max_chars)
    return PatchApplyTraceAttribute(
        attribute_id=kwargs.pop("attribute_id", "patch_apply_trace_attribute:v0.36.7"),
        attribute_kind=kwargs.pop("attribute_kind", PatchApplyTraceAttributeKind.SUMMARY),
        value=sanitized,
        value_summary=kwargs.pop("value_summary", "bounded trace attribute; no raw source or secret payload"),
        redacted=kwargs.pop("redacted", sanitized != str(raw_value) and _contains_prohibited_payload(str(raw_value))),
        truncated=kwargs.pop("truncated", len(sanitized) < len(str(raw_value))),
        **kwargs,
    )


def build_patch_apply_trace_object(**kwargs: Any) -> PatchApplyTraceObject:
    return PatchApplyTraceObject(
        object_id=kwargs.pop("object_id", "patch_apply_trace_object:v0.36.7"),
        object_type=kwargs.pop("object_type", PatchApplyTraceObjectType.TRACE_PACKET),
        object_label=kwargs.pop("object_label", "trace object"),
        object_summary=kwargs.pop("object_summary", "OCEL-style trace object metadata; not registry mutation"),
        attributes=kwargs.pop("attributes", []),
        source_refs=kwargs.pop("source_refs", [build_patch_apply_trace_source_ref()]),
        **kwargs,
    )


def build_patch_apply_trace_event(**kwargs: Any) -> PatchApplyTraceEvent:
    return PatchApplyTraceEvent(
        event_id=kwargs.pop("event_id", "patch_apply_trace_event:v0.36.7"),
        event_kind=kwargs.pop("event_kind", PatchApplyTraceEventKind.TRACE_PACKET_CREATED),
        lifecycle_phase=kwargs.pop("lifecycle_phase", PatchApplyTraceLifecyclePhase.TRACE_EMISSION),
        event_summary=kwargs.pop("event_summary", "OCEL-style trace event metadata; not runtime execution"),
        related_object_ids=kwargs.pop("related_object_ids", []),
        attributes=kwargs.pop("attributes", []),
        source_refs=kwargs.pop("source_refs", [build_patch_apply_trace_source_ref()]),
        **kwargs,
    )


def build_patch_apply_trace_relation(**kwargs: Any) -> PatchApplyTraceRelation:
    return PatchApplyTraceRelation(
        relation_id=kwargs.pop("relation_id", "patch_apply_trace_relation:v0.36.7"),
        relation_type=kwargs.pop("relation_type", PatchApplyTraceRelationType.TRACE_PACKET_CONTAINS_OBJECT),
        source_object_id=kwargs.pop("source_object_id", "trace_packet:v0.36.7"),
        target_object_id=kwargs.pop("target_object_id", "patch_apply_trace_object:v0.36.7"),
        relation_summary=kwargs.pop("relation_summary", "OCEL-style trace relation metadata; not runtime control"),
        attributes=kwargs.pop("attributes", []),
        source_refs=kwargs.pop("source_refs", [build_patch_apply_trace_source_ref()]),
        **kwargs,
    )


def build_sandbox_apply_lifecycle_trace_record(**kwargs: Any) -> SandboxApplyLifecycleTraceRecord:
    return SandboxApplyLifecycleTraceRecord(
        lifecycle_record_id=kwargs.pop("lifecycle_record_id", "sandbox_apply_lifecycle_trace_record:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        apply_candidate_id=kwargs.pop("apply_candidate_id", None),
        human_approval_contract_id=kwargs.pop("human_approval_contract_id", None),
        dry_run_result_id=kwargs.pop("dry_run_result_id", None),
        sandbox_manifest_id=kwargs.pop("sandbox_manifest_id", None),
        sandbox_apply_result_id=kwargs.pop("sandbox_apply_result_id", None),
        post_apply_validation_report_id=kwargs.pop("post_apply_validation_report_id", None),
        lifecycle_phases=kwargs.pop(
            "lifecycle_phases",
            [
                PatchApplyTraceLifecyclePhase.APPLY_CANDIDATE,
                PatchApplyTraceLifecyclePhase.HUMAN_APPROVAL,
                PatchApplyTraceLifecyclePhase.DRY_RUN,
                PatchApplyTraceLifecyclePhase.SANDBOX_WORKSPACE,
                PatchApplyTraceLifecyclePhase.SANDBOX_APPLY,
                PatchApplyTraceLifecyclePhase.POST_APPLY_VALIDATION,
            ],
        ),
        lifecycle_summary=kwargs.pop("lifecycle_summary", "sandbox apply lifecycle trace metadata; not live apply"),
        sandbox_apply_successful=kwargs.pop("sandbox_apply_successful", False),
        post_apply_validation_successful=kwargs.pop("post_apply_validation_successful", False),
        **kwargs,
    )


def build_agentic_task_lifecycle_trace_record(**kwargs: Any) -> AgenticTaskLifecycleTraceRecord:
    return AgenticTaskLifecycleTraceRecord(
        agentic_lifecycle_record_id=kwargs.pop("agentic_lifecycle_record_id", "agentic_task_lifecycle_trace_record:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        agentic_run_packet_id=kwargs.pop("agentic_run_packet_id", None),
        operation_result_id=kwargs.pop("operation_result_id", None),
        stop_reason_id=kwargs.pop("stop_reason_id", None),
        step_record_ids=kwargs.pop("step_record_ids", []),
        lifecycle_summary=kwargs.pop("lifecycle_summary", "bounded agentic task lifecycle trace metadata; not autonomous runtime"),
        single_cycle_only=kwargs.pop("single_cycle_only", True),
        human_handoff_required=kwargs.pop("human_handoff_required", True),
        **kwargs,
    )


def build_digestion_dominion_apply_trace_record(**kwargs: Any) -> DigestionDominionApplyTraceRecord:
    return DigestionDominionApplyTraceRecord(
        digestion_trace_record_id=kwargs.pop("digestion_trace_record_id", "digestion_dominion_apply_trace_record:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        digestion_first_policy_applied=kwargs.pop("digestion_first_policy_applied", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        external_agent_execution_blocked=kwargs.pop("external_agent_execution_blocked", True),
        infinite_agent_loop_blocked=kwargs.pop("infinite_agent_loop_blocked", True),
        automatic_repair_loop_blocked=kwargs.pop("automatic_repair_loop_blocked", True),
        recursive_self_invocation_blocked=kwargs.pop("recursive_self_invocation_blocked", True),
        bounded_agentic_task_only=kwargs.pop("bounded_agentic_task_only", True),
        summary=kwargs.pop("summary", "Digestion-first and Dominion-fallback boundaries are trace metadata only"),
        future_track_items=kwargs.pop(
            "future_track_items",
            ["Dominion requires explicit future gate", "external agent execution remains blocked"],
        ),
        **kwargs,
    )


def build_patch_apply_sandbox_trace_packet(**kwargs: Any) -> PatchApplySandboxTracePacket:
    objects = kwargs.pop("objects", [])
    events = kwargs.pop("events", [])
    relations = kwargs.pop("relations", [])
    attributes = kwargs.pop("attributes", [])
    return PatchApplySandboxTracePacket(
        trace_packet_id=kwargs.pop("trace_packet_id", "patch_apply_sandbox_trace_packet:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        sink_kind=kwargs.pop("sink_kind", PatchApplyTraceSinkKind.RETURNED_TRACE_PACKET),
        objects=objects,
        events=events,
        relations=relations,
        attributes=attributes,
        sandbox_lifecycle_record=kwargs.pop("sandbox_lifecycle_record", None),
        agentic_task_lifecycle_record=kwargs.pop("agentic_task_lifecycle_record", None),
        digestion_dominion_record=kwargs.pop("digestion_dominion_record", build_digestion_dominion_apply_trace_record()),
        source_refs=kwargs.pop("source_refs", [build_patch_apply_trace_source_ref()]),
        status=kwargs.pop("status", PatchApplyTraceStatus.EMITTED_AS_PACKET),
        redaction_applied=kwargs.pop("redaction_applied", any(attribute.redacted for attribute in attributes)),
        truncated=kwargs.pop("truncated", any(attribute.truncated for attribute in attributes)),
        summary=kwargs.pop("summary", "returned/in-memory patch apply sandbox trace packet; not persistent storage"),
        **kwargs,
    )


def build_patch_apply_trace_emission_input(**kwargs: Any) -> PatchApplyTraceEmissionInput:
    return PatchApplyTraceEmissionInput(
        emission_input_id=kwargs.pop("emission_input_id", "patch_apply_trace_emission_input:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        requested_sink_kind=kwargs.pop("requested_sink_kind", PatchApplyTraceSinkKind.RETURNED_TRACE_PACKET),
        trace_packet=kwargs.pop("trace_packet", None),
        source_refs=kwargs.pop("source_refs", [build_patch_apply_trace_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        summary=kwargs.pop("summary", "trace emission input for returned/in-memory packet only"),
        **kwargs,
    )


def build_patch_apply_trace_emission_decision(**kwargs: Any) -> PatchApplyTraceEmissionDecision:
    return PatchApplyTraceEmissionDecision(
        decision_id=kwargs.pop("decision_id", "patch_apply_trace_emission_decision:v0.36.7"),
        decision_kind=kwargs.pop("decision_kind", PatchApplyTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION),
        status=kwargs.pop("status", PatchApplyTraceStatus.POLICY_CHECKED),
        summary=kwargs.pop("summary", "trace packet creation allowed without persistence"),
        allow_trace_packet_creation=kwargs.pop("allow_trace_packet_creation", True),
        allow_in_memory_test_sink=kwargs.pop("allow_in_memory_test_sink", False),
        **kwargs,
    )


def build_patch_apply_trace_validation_finding(**kwargs: Any) -> PatchApplyTraceValidationFinding:
    return PatchApplyTraceValidationFinding(
        validation_finding_id=kwargs.pop("validation_finding_id", "patch_apply_trace_validation_finding:v0.36.7"),
        risk_kind=kwargs.pop("risk_kind", PatchApplyTraceRiskKind.PERSISTENT_TRACE_WRITE_RISK),
        decision_kind=kwargs.pop("decision_kind", PatchApplyTraceDecisionKind.BLOCK),
        severity=kwargs.pop("severity", "blocked"),
        summary=kwargs.pop("summary", "trace validation finding"),
        evidence_preview=kwargs.pop("evidence_preview", ""),
        blocked=kwargs.pop("blocked", True),
        requires_review=kwargs.pop("requires_review", True),
        **kwargs,
    )


def build_patch_apply_trace_validation_report(**kwargs: Any) -> PatchApplyTraceValidationReport:
    findings = kwargs.pop("findings", [])
    blocked = kwargs.pop("blocked", any(finding.blocked for finding in findings))
    return PatchApplyTraceValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "patch_apply_trace_validation_report:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        findings=findings,
        summary=kwargs.pop("summary", "trace packet validation report; no test execution or persistence"),
        validation_successful=kwargs.pop("validation_successful", not blocked),
        blocked=blocked,
        requires_review=kwargs.pop("requires_review", any(finding.requires_review for finding in findings)),
        **kwargs,
    )


def build_patch_apply_trace_emission_report(**kwargs: Any) -> PatchApplyTraceEmissionReport:
    decision = kwargs.pop("decision", build_patch_apply_trace_emission_decision())
    validation_report = kwargs.pop("validation_report", build_patch_apply_trace_validation_report())
    packet = kwargs.pop("trace_packet", None)
    emitted = kwargs.pop(
        "emitted",
        decision.allow_trace_packet_creation and not validation_report.blocked and packet is not None,
    )
    return PatchApplyTraceEmissionReport(
        emission_report_id=kwargs.pop("emission_report_id", "patch_apply_trace_emission_report:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        emission_input_id=kwargs.pop("emission_input_id", "patch_apply_trace_emission_input:v0.36.7"),
        decision=decision,
        trace_packet=packet,
        validation_report=validation_report,
        summary=kwargs.pop("summary", "trace emission report; returned packet only, no persistence"),
        emitted=emitted,
        **kwargs,
    )


def build_patch_apply_trace_emitter(**kwargs: Any) -> PatchApplyTraceEmitter:
    return PatchApplyTraceEmitter(
        emitter_id=kwargs.pop("emitter_id", "patch_apply_trace_emitter:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        allowed_sink_kinds=kwargs.pop(
            "allowed_sink_kinds",
            [PatchApplyTraceSinkKind.RETURNED_TRACE_PACKET, PatchApplyTraceSinkKind.IN_MEMORY_TEST_SINK, PatchApplyTraceSinkKind.DISABLED],
        ),
        emitter_summary=kwargs.pop("emitter_summary", "returned/in-memory trace packet emitter only"),
        **kwargs,
    )


def build_patch_apply_trace_run_preview(**kwargs: Any) -> PatchApplyTraceRunPreview:
    return PatchApplyTraceRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "patch_apply_trace_run_preview:v0.36.7"),
        emission_input_id=kwargs.pop("emission_input_id", "patch_apply_trace_emission_input:v0.36.7"),
        preview_summary=kwargs.pop("preview_summary", "preview returned/in-memory trace packet creation"),
        planned_trace_actions=kwargs.pop(
            "planned_trace_actions",
            ["convert supplied metadata to trace objects", "create trace packet", "validate no persistence"],
        ),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        ready_for_patch_apply_sandbox_trace_packet_creation=kwargs.pop("ready_for_patch_apply_sandbox_trace_packet_creation", True),
        **kwargs,
    )


def build_patch_apply_trace_no_persistence_guarantee(**kwargs: Any) -> PatchApplyTraceNoPersistenceGuarantee:
    return PatchApplyTraceNoPersistenceGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "patch_apply_trace_no_persistence_guarantee:v0.36.7"),
        version=kwargs.pop("version", V0367_VERSION),
        no_trace_persistence=kwargs.pop("no_trace_persistence", True),
        no_ocel_file_write=kwargs.pop("no_ocel_file_write", True),
        no_jsonl_write=kwargs.pop("no_jsonl_write", True),
        no_log_write=kwargs.pop("no_log_write", True),
        no_database_write=kwargs.pop("no_database_write", True),
        no_external_trace_sink=kwargs.pop("no_external_trace_sink", True),
        no_sandbox_file_write=kwargs.pop("no_sandbox_file_write", True),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
        no_live_code_edit=kwargs.pop("no_live_code_edit", True),
        no_additional_patch_application=kwargs.pop("no_additional_patch_application", True),
        no_apply_patch=kwargs.pop("no_apply_patch", True),
        no_git_apply=kwargs.pop("no_git_apply", True),
        no_shell_execution=kwargs.pop("no_shell_execution", True),
        no_subprocess_execution=kwargs.pop("no_subprocess_execution", True),
        no_command_execution=kwargs.pop("no_command_execution", True),
        no_test_execution=kwargs.pop("no_test_execution", True),
        no_dependency_install=kwargs.pop("no_dependency_install", True),
        no_reference_execution=kwargs.pop("no_reference_execution", True),
        no_reference_import=kwargs.pop("no_reference_import", True),
        no_external_agent_execution=kwargs.pop("no_external_agent_execution", True),
        no_claude_code_invocation=kwargs.pop("no_claude_code_invocation", True),
        no_codex_cli_invocation=kwargs.pop("no_codex_cli_invocation", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        no_infinite_agent_loop=kwargs.pop("no_infinite_agent_loop", True),
        no_provider_invocation=kwargs.pop("no_provider_invocation", True),
        no_network_access=kwargs.pop("no_network_access", True),
        no_credential_access=kwargs.pop("no_credential_access", True),
        no_secret_read=kwargs.pop("no_secret_read", True),
        no_autonomous_runtime=kwargs.pop("no_autonomous_runtime", True),
        no_general_tool_execution=kwargs.pop("no_general_tool_execution", True),
        no_ui_runtime=kwargs.pop("no_ui_runtime", True),
        no_authority_grant=kwargs.pop("no_authority_grant", True),
        **kwargs,
    )


def build_v0367_readiness_report(**kwargs: Any) -> V0367ReadinessReport:
    return V0367ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0367_readiness_report"),
        version=kwargs.pop("version", V0367_VERSION),
        release_name=kwargs.pop("release_name", V0367_RELEASE_NAME),
        status=kwargs.pop("status", PatchApplyTraceStatus.EMITTED_AS_PACKET),
        readiness_level=kwargs.pop("readiness_level", PatchApplyTraceReadinessLevel.TRACE_PACKET_READY),
        ready_for_v0368_cli_sandbox_apply_agentic_surface=kwargs.pop("ready_for_v0368_cli_sandbox_apply_agentic_surface", True),
        ready_for_v0369_patch_apply_sandbox_consolidation=kwargs.pop("ready_for_v0369_patch_apply_sandbox_consolidation", True),
        ready_for_patch_apply_sandbox_trace_packet_creation=kwargs.pop("ready_for_patch_apply_sandbox_trace_packet_creation", True),
        ready_for_bounded_patch_apply_ocel_trace_emission=kwargs.pop("ready_for_bounded_patch_apply_ocel_trace_emission", True),
        ready_for_sandbox_apply_lifecycle_trace=kwargs.pop("ready_for_sandbox_apply_lifecycle_trace", True),
        ready_for_agentic_operation_lifecycle_trace=kwargs.pop("ready_for_agentic_operation_lifecycle_trace", True),
        ready_for_digestion_dominion_trace_metadata=kwargs.pop("ready_for_digestion_dominion_trace_metadata", True),
        ready_for_future_cli_trace_preview_input=kwargs.pop("ready_for_future_cli_trace_preview_input", True),
        **kwargs,
    )


def build_sandbox_apply_lifecycle_record_from_artifacts(
    *,
    apply_candidate: Any = None,
    human_approval_contract: Any = None,
    dry_run_result: Any = None,
    sandbox_manifest: Any = None,
    sandbox_apply_result: SandboxPatchApplyResult | None = None,
    post_apply_validation_report: SandboxPostApplyValidationReport | None = None,
    **kwargs: Any,
) -> SandboxApplyLifecycleTraceRecord:
    return build_sandbox_apply_lifecycle_trace_record(
        apply_candidate_id=_safe_artifact_id(apply_candidate, "candidate_id", "apply_candidate_id"),
        human_approval_contract_id=_safe_artifact_id(human_approval_contract, "approval_contract_id", "human_approval_contract_id", "contract_id"),
        dry_run_result_id=_safe_artifact_id(dry_run_result, "dry_run_result_id", "simulation_result_id"),
        sandbox_manifest_id=_safe_artifact_id(sandbox_manifest, "manifest_id", "sandbox_manifest_id"),
        sandbox_apply_result_id=_safe_artifact_id(sandbox_apply_result, "sandbox_apply_result_id"),
        post_apply_validation_report_id=_safe_artifact_id(post_apply_validation_report, "validation_report_id"),
        sandbox_apply_successful=_artifact_bool(sandbox_apply_result, "sandbox_apply_successful", False),
        post_apply_validation_successful=_artifact_bool(post_apply_validation_report, "validation_successful", False),
        **kwargs,
    )


def build_agentic_task_lifecycle_record_from_run_packet(
    run_packet: AgenticOperationRunPacket | None,
    **kwargs: Any,
) -> AgenticTaskLifecycleTraceRecord:
    result = getattr(run_packet, "result", None)
    step_sequence = getattr(result, "step_sequence", None)
    step_records = getattr(step_sequence, "step_records", []) if step_sequence else []
    stop_reason = getattr(result, "stop_reason", None)
    return build_agentic_task_lifecycle_trace_record(
        agentic_run_packet_id=_safe_artifact_id(run_packet, "run_packet_id"),
        operation_result_id=_safe_artifact_id(result, "operation_result_id"),
        stop_reason_id=_safe_artifact_id(stop_reason, "stop_reason_id"),
        step_record_ids=[str(getattr(step, "step_record_id", "missing")) for step in step_records],
        single_cycle_only=True,
        human_handoff_required=True,
        **kwargs,
    )


def build_digestion_dominion_trace_record_from_policy_metadata(**kwargs: Any) -> DigestionDominionApplyTraceRecord:
    return build_digestion_dominion_apply_trace_record(**kwargs)


def _trace_packet_with_single_object(
    *,
    object_id: str,
    object_type: PatchApplyTraceObjectType,
    object_label: str,
    object_summary: str,
    event_kind: PatchApplyTraceEventKind,
    phase: PatchApplyTraceLifecyclePhase,
    source_kind: PatchApplyTraceSourceKind,
    source_id: str,
    event_summary: str,
    summary: str,
    sandbox_lifecycle_record: SandboxApplyLifecycleTraceRecord | None = None,
    agentic_lifecycle_record: AgenticTaskLifecycleTraceRecord | None = None,
) -> PatchApplySandboxTracePacket:
    source_ref = build_patch_apply_trace_source_ref(source_kind=source_kind, source_id=source_id)
    trace_object = build_patch_apply_trace_object(
        object_id=object_id,
        object_type=object_type,
        object_label=object_label,
        object_summary=object_summary,
        source_refs=[source_ref],
        attributes=[build_patch_apply_trace_attribute(value=object_summary)],
    )
    trace_event = build_patch_apply_trace_event(
        event_id=f"{event_kind.value}:v0.36.7",
        event_kind=event_kind,
        lifecycle_phase=phase,
        event_summary=event_summary,
        related_object_ids=[object_id],
        source_refs=[source_ref],
    )
    trace_packet_object = build_patch_apply_trace_object(
        object_id="trace_packet:v0.36.7",
        object_type=PatchApplyTraceObjectType.TRACE_PACKET,
        object_label="trace packet",
        object_summary="returned trace packet metadata",
        source_refs=[source_ref],
    )
    relation = build_patch_apply_trace_relation(
        relation_id=f"trace_packet_contains:{object_id}",
        relation_type=PatchApplyTraceRelationType.TRACE_PACKET_CONTAINS_OBJECT,
        source_object_id=trace_packet_object.object_id,
        target_object_id=object_id,
        source_refs=[source_ref],
    )
    return build_patch_apply_sandbox_trace_packet(
        objects=[trace_packet_object, trace_object],
        events=[trace_event],
        relations=[relation],
        source_refs=[source_ref],
        sandbox_lifecycle_record=sandbox_lifecycle_record,
        agentic_task_lifecycle_record=agentic_lifecycle_record,
        summary=summary,
    )


def build_trace_packet_from_agentic_operation_run_packet(run_packet: AgenticOperationRunPacket) -> PatchApplySandboxTracePacket:
    lifecycle = build_agentic_task_lifecycle_record_from_run_packet(run_packet)
    source_ref = build_patch_apply_trace_source_ref(
        source_kind=PatchApplyTraceSourceKind.V0366_AGENTIC_OPERATION_RUN_PACKET,
        source_id=run_packet.run_packet_id,
    )
    objects: list[PatchApplyTraceObject] = [
        build_patch_apply_trace_object(
            object_id="trace_packet:v0.36.7",
            object_type=PatchApplyTraceObjectType.TRACE_PACKET,
            object_label="trace packet",
            object_summary="returned trace packet metadata",
            source_refs=[source_ref],
        ),
        build_patch_apply_trace_object(
            object_id=run_packet.run_packet_id,
            object_type=PatchApplyTraceObjectType.AGENTIC_OPERATION_RUN_PACKET,
            object_label="agentic operation run packet",
            object_summary=run_packet.summary,
            source_refs=[source_ref],
            attributes=[
                build_patch_apply_trace_attribute(
                    attribute_kind=PatchApplyTraceAttributeKind.AGENTIC_RUN_PACKET_REF,
                    value=run_packet.run_packet_id,
                )
            ],
        ),
        build_patch_apply_trace_object(
            object_id=run_packet.result.operation_result_id,
            object_type=PatchApplyTraceObjectType.AGENTIC_OPERATION_RESULT,
            object_label="agentic operation result",
            object_summary=run_packet.result.result_summary,
            source_refs=[source_ref],
        ),
        build_patch_apply_trace_object(
            object_id=run_packet.result.stop_reason.stop_reason_id,
            object_type=PatchApplyTraceObjectType.AGENTIC_OPERATION_STOP_REASON,
            object_label="agentic operation stop reason",
            object_summary=run_packet.result.stop_reason.stop_summary,
            source_refs=[source_ref],
        ),
    ]
    for step in run_packet.result.step_sequence.step_records:
        objects.append(
            build_patch_apply_trace_object(
                object_id=step.step_record_id,
                object_type=PatchApplyTraceObjectType.AGENTIC_OPERATION_STEP_RECORD,
                object_label="agentic operation step record",
                object_summary=step.step_summary,
                source_refs=[source_ref],
            )
        )
    events = [
        build_patch_apply_trace_event(
            event_id="agentic_operation_cycle_started:v0.36.7",
            event_kind=PatchApplyTraceEventKind.AGENTIC_OPERATION_CYCLE_STARTED,
            lifecycle_phase=PatchApplyTraceLifecyclePhase.BOUNDED_AGENTIC_OPERATION,
            event_summary="bounded agentic operation cycle traced; not started by trace layer",
            related_object_ids=[run_packet.run_packet_id],
            source_refs=[source_ref],
        ),
        build_patch_apply_trace_event(
            event_id="agentic_operation_cycle_completed:v0.36.7",
            event_kind=PatchApplyTraceEventKind.AGENTIC_OPERATION_CYCLE_COMPLETED
            if run_packet.result.completed_successfully
            else PatchApplyTraceEventKind.AGENTIC_OPERATION_CYCLE_STOPPED,
            lifecycle_phase=PatchApplyTraceLifecyclePhase.HUMAN_HANDOFF,
            event_summary="bounded single cycle traced with mandatory human handoff",
            related_object_ids=[run_packet.result.operation_result_id, run_packet.result.stop_reason.stop_reason_id],
            source_refs=[source_ref],
        ),
        build_patch_apply_trace_event(
            event_id="human_handoff_required:v0.36.7",
            event_kind=PatchApplyTraceEventKind.HUMAN_HANDOFF_REQUIRED,
            lifecycle_phase=PatchApplyTraceLifecyclePhase.HUMAN_HANDOFF,
            event_summary="human handoff required after one bounded cycle",
            related_object_ids=[run_packet.result.stop_reason.stop_reason_id],
            source_refs=[source_ref],
        ),
    ]
    for step in run_packet.result.step_sequence.step_records:
        events.append(
            build_patch_apply_trace_event(
                event_id=f"agentic_step_recorded:v0.36.7:{step.step_index}",
                event_kind=PatchApplyTraceEventKind.AGENTIC_OPERATION_STEP_RECORDED,
                lifecycle_phase=PatchApplyTraceLifecyclePhase.BOUNDED_AGENTIC_OPERATION,
                event_summary=step.step_summary,
                related_object_ids=[step.step_record_id],
                source_refs=[source_ref],
            )
        )
    relations = [
        build_patch_apply_trace_relation(
            relation_id="agentic_cycle_produces_result:v0.36.7",
            relation_type=PatchApplyTraceRelationType.AGENTIC_CYCLE_PRODUCES_RESULT,
            source_object_id=run_packet.run_packet_id,
            target_object_id=run_packet.result.operation_result_id,
            source_refs=[source_ref],
        ),
        build_patch_apply_trace_relation(
            relation_id="result_has_stop_reason:v0.36.7",
            relation_type=PatchApplyTraceRelationType.RESULT_HAS_STOP_REASON,
            source_object_id=run_packet.result.operation_result_id,
            target_object_id=run_packet.result.stop_reason.stop_reason_id,
            source_refs=[source_ref],
        ),
    ]
    for step in run_packet.result.step_sequence.step_records:
        relations.append(
            build_patch_apply_trace_relation(
                relation_id=f"agentic_cycle_records_step:v0.36.7:{step.step_index}",
                relation_type=PatchApplyTraceRelationType.AGENTIC_CYCLE_RECORDS_STEP,
                source_object_id=run_packet.run_packet_id,
                target_object_id=step.step_record_id,
                source_refs=[source_ref],
            )
        )
    return build_patch_apply_sandbox_trace_packet(
        objects=objects,
        events=events,
        relations=relations,
        agentic_task_lifecycle_record=lifecycle,
        source_refs=[source_ref],
        summary="trace packet from bounded agentic operation run packet; not autonomous runtime",
    )


def build_trace_packet_from_post_apply_validation_report(
    report: SandboxPostApplyValidationReport,
) -> PatchApplySandboxTracePacket:
    lifecycle = build_sandbox_apply_lifecycle_record_from_artifacts(post_apply_validation_report=report)
    return _trace_packet_with_single_object(
        object_id=report.validation_report_id,
        object_type=PatchApplyTraceObjectType.SANDBOX_POST_APPLY_VALIDATION_REPORT,
        object_label="sandbox post-apply validation report",
        object_summary=report.summary,
        event_kind=PatchApplyTraceEventKind.POST_APPLY_VALIDATION_COMPLETED,
        phase=PatchApplyTraceLifecyclePhase.POST_APPLY_VALIDATION,
        source_kind=PatchApplyTraceSourceKind.V0365_POST_APPLY_VALIDATION_REPORT,
        source_id=report.validation_report_id,
        event_summary="sandbox post-apply validation traced; not test execution",
        summary="trace packet from sandbox post-apply validation report",
        sandbox_lifecycle_record=lifecycle,
    )


def build_trace_packet_from_sandbox_apply_result(result: SandboxPatchApplyResult) -> PatchApplySandboxTracePacket:
    lifecycle = build_sandbox_apply_lifecycle_record_from_artifacts(sandbox_apply_result=result)
    source_ref = build_patch_apply_trace_source_ref(
        source_kind=PatchApplyTraceSourceKind.V0364_SANDBOX_PATCH_APPLY_RESULT,
        source_id=result.sandbox_apply_result_id,
    )
    objects = [
        build_patch_apply_trace_object(
            object_id="trace_packet:v0.36.7",
            object_type=PatchApplyTraceObjectType.TRACE_PACKET,
            object_label="trace packet",
            object_summary="returned trace packet metadata",
            source_refs=[source_ref],
        ),
        build_patch_apply_trace_object(
            object_id=result.sandbox_apply_result_id,
            object_type=PatchApplyTraceObjectType.SANDBOX_PATCH_APPLY_RESULT,
            object_label="sandbox patch apply result",
            object_summary=result.summary,
            source_refs=[source_ref],
        ),
    ]
    events = [
        build_patch_apply_trace_event(
            event_id="sandbox_patch_apply_completed:v0.36.7",
            event_kind=PatchApplyTraceEventKind.SANDBOX_PATCH_APPLY_COMPLETED
            if result.sandbox_apply_successful
            else PatchApplyTraceEventKind.SANDBOX_PATCH_APPLY_BLOCKED,
            lifecycle_phase=PatchApplyTraceLifecyclePhase.SANDBOX_APPLY,
            event_summary="sandbox patch apply result traced; not live apply permission",
            related_object_ids=[result.sandbox_apply_result_id],
            source_refs=[source_ref],
        )
    ]
    relations: list[PatchApplyTraceRelation] = []
    for index, record in enumerate(result.write_records, start=1):
        objects.append(
            build_patch_apply_trace_object(
                object_id=record.write_record_id,
                object_type=PatchApplyTraceObjectType.SANDBOX_FILE_WRITE_RECORD,
                object_label="sandbox file write record",
                object_summary=record.write_summary,
                source_refs=[
                    build_patch_apply_trace_source_ref(
                        source_kind=PatchApplyTraceSourceKind.V0364_SANDBOX_FILE_WRITE_RECORD,
                        source_id=record.write_record_id,
                    )
                ],
            )
        )
        events.append(
            build_patch_apply_trace_event(
                event_id=f"sandbox_file_write_recorded:v0.36.7:{index}",
                event_kind=PatchApplyTraceEventKind.SANDBOX_FILE_WRITE_RECORDED,
                lifecycle_phase=PatchApplyTraceLifecyclePhase.SANDBOX_APPLY,
                event_summary="sandbox file write record traced; no write performed by trace layer",
                related_object_ids=[record.write_record_id],
                source_refs=[source_ref],
            )
        )
        relations.append(
            build_patch_apply_trace_relation(
                relation_id=f"sandbox_apply_produces_write_record:v0.36.7:{index}",
                relation_type=PatchApplyTraceRelationType.SANDBOX_APPLY_PRODUCES_WRITE_RECORD,
                source_object_id=result.sandbox_apply_result_id,
                target_object_id=record.write_record_id,
                source_refs=[source_ref],
            )
        )
    return build_patch_apply_sandbox_trace_packet(
        objects=objects,
        events=events,
        relations=relations,
        sandbox_lifecycle_record=lifecycle,
        source_refs=[source_ref],
        summary="trace packet from sandbox patch apply result; not live apply",
    )


def build_trace_packet_from_dry_run_result(result: DryRunApplySimulationResult) -> PatchApplySandboxTracePacket:
    result_id = _safe_artifact_id(result, "dry_run_result_id", "simulation_result_id", fallback="dry_run_result:v0.36.2")
    return _trace_packet_with_single_object(
        object_id=str(result_id),
        object_type=PatchApplyTraceObjectType.DRY_RUN_APPLY_SIMULATION_RESULT,
        object_label="dry-run apply simulation result",
        object_summary=_artifact_summary(result, "dry-run result metadata"),
        event_kind=PatchApplyTraceEventKind.DRY_RUN_SIMULATION_COMPLETED,
        phase=PatchApplyTraceLifecyclePhase.DRY_RUN,
        source_kind=PatchApplyTraceSourceKind.V0362_DRY_RUN_APPLY_SIMULATION_RESULT,
        source_id=str(result_id),
        event_summary="dry-run simulation result traced; not patch application",
        summary="trace packet from dry-run apply simulation result",
        sandbox_lifecycle_record=build_sandbox_apply_lifecycle_record_from_artifacts(dry_run_result=result),
    )


def build_trace_packet_from_apply_candidate(candidate: ApplyCandidateEnvelope) -> PatchApplySandboxTracePacket:
    candidate_id = _safe_artifact_id(candidate, "candidate_id", "apply_candidate_id", fallback="apply_candidate:v0.36.1")
    return _trace_packet_with_single_object(
        object_id=str(candidate_id),
        object_type=PatchApplyTraceObjectType.APPLY_CANDIDATE_ENVELOPE,
        object_label="apply candidate envelope",
        object_summary=_artifact_summary(candidate, "apply candidate metadata"),
        event_kind=PatchApplyTraceEventKind.APPLY_CANDIDATE_CREATED,
        phase=PatchApplyTraceLifecyclePhase.APPLY_CANDIDATE,
        source_kind=PatchApplyTraceSourceKind.V0361_APPLY_CANDIDATE_ENVELOPE,
        source_id=str(candidate_id),
        event_summary="apply candidate traced; not apply permission",
        summary="trace packet from apply candidate envelope",
        sandbox_lifecycle_record=build_sandbox_apply_lifecycle_record_from_artifacts(apply_candidate=candidate),
    )


def validate_patch_apply_sandbox_trace_packet(
    packet: PatchApplySandboxTracePacket,
    policy: PatchApplyTracePolicy | None = None,
) -> PatchApplyTraceValidationReport:
    active_policy = policy or default_patch_apply_trace_policy()
    findings: list[PatchApplyTraceValidationFinding] = []
    sink = PatchApplyTraceSinkKind(packet.sink_kind)
    if sink not in {PatchApplyTraceSinkKind.RETURNED_TRACE_PACKET, PatchApplyTraceSinkKind.IN_MEMORY_TEST_SINK, PatchApplyTraceSinkKind.DISABLED}:
        findings.append(
            build_patch_apply_trace_validation_finding(
                risk_kind=PatchApplyTraceRiskKind.EXTERNAL_TRACE_SINK_RISK,
                summary="trace packet requested a blocked persistent or external sink",
            )
        )
    if len(packet.events) > active_policy.max_event_count:
        findings.append(
            build_patch_apply_trace_validation_finding(
                risk_kind=PatchApplyTraceRiskKind.UNBOUNDED_PAYLOAD_RISK,
                summary="trace packet event count exceeds policy bound",
            )
        )
    if len(packet.objects) > active_policy.max_object_count:
        findings.append(
            build_patch_apply_trace_validation_finding(
                risk_kind=PatchApplyTraceRiskKind.UNBOUNDED_PAYLOAD_RISK,
                summary="trace packet object count exceeds policy bound",
            )
        )
    if len(packet.relations) > active_policy.max_relation_count:
        findings.append(
            build_patch_apply_trace_validation_finding(
                risk_kind=PatchApplyTraceRiskKind.UNBOUNDED_PAYLOAD_RISK,
                summary="trace packet relation count exceeds policy bound",
            )
        )
    for attribute in packet.attributes + [attr for obj in packet.objects for attr in obj.attributes] + [attr for event in packet.events for attr in event.attributes]:
        if len(attribute.value) > active_policy.max_attribute_chars or _contains_prohibited_payload(attribute.value):
            findings.append(
                build_patch_apply_trace_validation_finding(
                    risk_kind=PatchApplyTraceRiskKind.SECRET_CONTENT_TRACE_RISK,
                    summary="trace attribute contains blocked or unbounded payload",
                    evidence_preview=sanitize_patch_apply_trace_attribute_value(attribute.value),
                )
            )
    return build_patch_apply_trace_validation_report(findings=findings)


def decide_patch_apply_trace_emission(
    emission_input: PatchApplyTraceEmissionInput,
    policy: PatchApplyTracePolicy | None = None,
) -> PatchApplyTraceEmissionDecision:
    active_policy = policy or default_patch_apply_trace_policy()
    requested_sink = PatchApplyTraceSinkKind(emission_input.requested_sink_kind)
    if requested_sink not in {PatchApplyTraceSinkKind(kind) for kind in active_policy.allowed_sink_kinds}:
        return build_patch_apply_trace_emission_decision(
            decision_kind=PatchApplyTraceDecisionKind.BLOCK,
            status=PatchApplyTraceStatus.BLOCKED,
            summary="trace sink blocked by policy",
            allow_trace_packet_creation=False,
            allow_in_memory_test_sink=False,
        )
    if requested_sink == PatchApplyTraceSinkKind.IN_MEMORY_TEST_SINK:
        return build_patch_apply_trace_emission_decision(
            decision_kind=PatchApplyTraceDecisionKind.ALLOW_IN_MEMORY_TEST_SINK,
            status=PatchApplyTraceStatus.POLICY_CHECKED,
            summary="in-memory test sink allowed; no persistence",
            allow_trace_packet_creation=True,
            allow_in_memory_test_sink=True,
        )
    if requested_sink == PatchApplyTraceSinkKind.DISABLED:
        return build_patch_apply_trace_emission_decision(
            decision_kind=PatchApplyTraceDecisionKind.SKIP,
            status=PatchApplyTraceStatus.SKIPPED,
            summary="trace emission disabled by request",
            allow_trace_packet_creation=False,
            allow_in_memory_test_sink=False,
        )
    return build_patch_apply_trace_emission_decision()


def emit_patch_apply_trace_packet(
    emission_input: PatchApplyTraceEmissionInput,
    emitter: PatchApplyTraceEmitter | None = None,
    policy: PatchApplyTracePolicy | None = None,
) -> PatchApplyTraceEmissionReport:
    active_emitter = emitter or build_patch_apply_trace_emitter()
    if PatchApplyTraceSinkKind(emission_input.requested_sink_kind) not in {PatchApplyTraceSinkKind(kind) for kind in active_emitter.allowed_sink_kinds}:
        decision = build_patch_apply_trace_emission_decision(
            decision_kind=PatchApplyTraceDecisionKind.BLOCK,
            status=PatchApplyTraceStatus.BLOCKED,
            summary="trace sink blocked by emitter",
            allow_trace_packet_creation=False,
            allow_in_memory_test_sink=False,
        )
        validation = build_patch_apply_trace_validation_report(
            findings=[
                build_patch_apply_trace_validation_finding(
                    risk_kind=PatchApplyTraceRiskKind.EXTERNAL_TRACE_SINK_RISK,
                    summary="emitter blocks requested sink",
                )
            ]
        )
        return build_patch_apply_trace_emission_report(
            emission_input_id=emission_input.emission_input_id,
            decision=decision,
            validation_report=validation,
            trace_packet=None,
            emitted=False,
        )
    decision = decide_patch_apply_trace_emission(emission_input, policy=policy)
    validation = (
        validate_patch_apply_sandbox_trace_packet(emission_input.trace_packet, policy=policy)
        if emission_input.trace_packet is not None
        else build_patch_apply_trace_validation_report(
            findings=[
                build_patch_apply_trace_validation_finding(
                    risk_kind=PatchApplyTraceRiskKind.UNBOUNDED_PAYLOAD_RISK,
                    summary="missing trace packet",
                )
            ]
        )
    )
    return build_patch_apply_trace_emission_report(
        emission_input_id=emission_input.emission_input_id,
        decision=decision,
        validation_report=validation,
        trace_packet=emission_input.trace_packet if decision.allow_trace_packet_creation and not validation.blocked else None,
    )


def patch_apply_trace_flags_preserve_no_persistence(flags: PatchApplyTraceFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def patch_apply_trace_policy_blocks_persistence(policy: PatchApplyTracePolicy) -> bool:
    blocked_names = (
        "allow_raw_diff",
        "allow_raw_source",
        "allow_raw_sandbox_file_content",
        "allow_raw_validation_report",
        "allow_secret_content",
        "allow_credential_content",
        "allow_token_content",
        "allow_full_file_content",
        "allow_persistent_write",
        "allow_external_sink",
        "allow_ocel_file_write",
        "allow_jsonl_write",
        "allow_log_write",
        "allow_database_write",
        "allow_sandbox_file_write",
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_test_execution",
        "allow_shell",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    )
    return all(getattr(policy, name) is False for name in blocked_names)


def patch_apply_trace_packet_is_not_persistence(packet: PatchApplySandboxTracePacket) -> bool:
    return (
        packet.ready_for_persistent_write is False
        and packet.ready_for_external_sink is False
        and packet.ready_for_ocel_file_write is False
        and packet.ready_for_jsonl_write is False
        and packet.ready_for_execution is False
        and PatchApplyTraceSinkKind(packet.sink_kind)
        in {PatchApplyTraceSinkKind.RETURNED_TRACE_PACKET, PatchApplyTraceSinkKind.IN_MEMORY_TEST_SINK, PatchApplyTraceSinkKind.DISABLED}
    )


def sandbox_apply_lifecycle_record_is_not_live_apply(record: SandboxApplyLifecycleTraceRecord) -> bool:
    return (
        record.live_write_performed is False
        and record.patch_application_performed is False
        and record.production_certified is False
    )


def agentic_task_lifecycle_record_is_not_runtime(record: AgenticTaskLifecycleTraceRecord) -> bool:
    return (
        record.single_cycle_only is True
        and record.human_handoff_required is True
        and record.automatic_retry_allowed is False
        and record.automatic_repair_allowed is False
        and record.independent_agent_runtime is False
        and record.multi_cycle_loop is False
    )


def digestion_dominion_apply_trace_record_is_not_runtime(record: DigestionDominionApplyTraceRecord) -> bool:
    return (
        record.digestion_first_policy_applied is True
        and record.dominion_runtime_blocked is True
        and record.external_agent_execution_blocked is True
        and record.infinite_agent_loop_blocked is True
        and record.automatic_repair_loop_blocked is True
        and record.recursive_self_invocation_blocked is True
        and record.bounded_agentic_task_only is True
    )


def v0367_readiness_report_is_not_execution_ready(report: V0367ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)
