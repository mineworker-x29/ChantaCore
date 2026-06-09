from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_diff_proposal import DiffProposalEnvelope
from .patch_plan import PatchPlan
from .patch_proposal_boundary import ReferenceHarnessPatternKind, ReferencePatternDigest, ReferencePatternDisposition
from .patch_review import PatchReviewPacket
from .patch_risk import PatchProposalRiskReport


V0357_VERSION = "v0.35.7"
V0357_RELEASE_NAME = "v0.35.7 Patch Proposal OCEL Trace Packet"
DEFAULT_V0357_DOC_PATH = "docs/versions/v0.35/v0.35.7_patch_proposal_ocel_trace_packet.md"
DEFAULT_V0356_REVIEW_DOC_REF = "docs/versions/v0.35/v0.35.6_human_review_packet_approval_gate_metadata.md"
DEFAULT_V0355_RISK_DOC_REF = "docs/versions/v0.35/v0.35.5_patch_risk_conformance_scanner.md"
DEFAULT_V0354_DIFF_DOC_REF = "docs/versions/v0.35/v0.35.4_diff_proposal_envelope.md"
DEFAULT_V0353_PLAN_DOC_REF = "docs/versions/v0.35/v0.35.3_reference_informed_patch_plan_change_set_graph.md"
DEFAULT_V0352_CONTEXT_DOC_REF = "docs/versions/v0.35/v0.35.2_readonly_patch_context_reference_corpus_collector.md"
DEFAULT_V0350_DIGEST_REF = "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md"
DEFAULT_MAX_TRACE_ATTRIBUTE_CHARS = 240

DEFAULT_PROHIBITED_PAYLOAD_PATTERNS = [
    "secret",
    "key",
    "token",
    "credential",
    "pem",
    "id_rsa",
    "id_ed25519",
]

DEFAULT_PROHIBITED_RUNTIME_ACTIONS = [
    "trace_persistence",
    "ocel_file_write",
    "jsonl_write",
    "log_write",
    "database_write",
    "patch_application",
    "workspace_write",
    "code_edit",
    "apply_patch",
    "git_apply",
    "shell_execution",
    "subprocess_execution",
    "command_execution",
    "test_execution",
    "dependency_install",
    "reference_execution",
    "reference_import",
    "external_agent_execution",
    "claude_code_invocation",
    "codex_cli_invocation",
    "dominion_runtime",
    "infinite_agent_loop",
    "provider_invocation",
    "direct_network_access",
    "credential_access",
    "secret_read",
]

UNSAFE_PATCH_PROPOSAL_TRACE_FLAG_NAMES = (
    "ready_for_execution",
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
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class PatchProposalTraceEventKind(StrEnum):
    PATCH_INTENT_CREATED = "patch_intent_created"
    PATCH_SCOPE_VALIDATED = "patch_scope_validated"
    PATCH_CONTEXT_COLLECTED = "patch_context_collected"
    REFERENCE_PATTERN_DIGEST_CONSUMED = "reference_pattern_digest_consumed"
    REFERENCE_PATTERN_ADAPTED = "reference_pattern_adapted"
    REFERENCE_PATTERN_REJECTED = "reference_pattern_rejected"
    PATCH_PLAN_CREATED = "patch_plan_created"
    CHANGE_SET_GRAPH_CREATED = "change_set_graph_created"
    DIFF_PROPOSAL_CREATED = "diff_proposal_created"
    STRUCTURED_PATCH_PROPOSAL_CREATED = "structured_patch_proposal_created"
    UNIFIED_DIFF_PROPOSAL_CREATED = "unified_diff_proposal_created"
    PATCH_RISK_SCANNED = "patch_risk_scanned"
    PATCH_CONFORMANCE_SCANNED = "patch_conformance_scanned"
    PATCH_SAFETY_REGRESSION_SCANNED = "patch_safety_regression_scanned"
    PATCH_SCOPE_VIOLATION_SCANNED = "patch_scope_violation_scanned"
    HUMAN_REVIEW_PACKET_CREATED = "human_review_packet_created"
    REVIEW_CHECKLIST_CREATED = "review_checklist_created"
    APPROVAL_GATE_METADATA_CREATED = "approval_gate_metadata_created"
    REVIEWER_DECISION_PLACEHOLDER_CREATED = "reviewer_decision_placeholder_created"
    REVIEWER_DECISION_RECORDED = "reviewer_decision_recorded"
    PATCH_PROPOSAL_READY_FOR_REVIEW = "patch_proposal_ready_for_review"
    PATCH_PROPOSAL_BLOCKED = "patch_proposal_blocked"
    PATCH_PROPOSAL_NEEDS_REVISION = "patch_proposal_needs_revision"
    PATCH_PROPOSAL_FUTURE_GATED = "patch_proposal_future_gated"
    DIGESTION_FIRST_POLICY_APPLIED = "digestion_first_policy_applied"
    EXTERNAL_AGENT_CONTROL_PATTERN_OBSERVED = "external_agent_control_pattern_observed"
    DOMINION_LIKE_LOOP_DETECTED = "dominion_like_loop_detected"
    DOMINION_ESCALATION_REJECTED = "dominion_escalation_rejected"
    DOMINION_ESCALATION_FUTURE_GATED = "dominion_escalation_future_gated"
    EXTERNAL_AGENT_EXECUTION_BLOCKED = "external_agent_execution_blocked"
    INFINITE_AGENT_LOOP_BLOCKED = "infinite_agent_loop_blocked"
    REFERENCE_HARNESS_EXECUTION_BLOCKED = "reference_harness_execution_blocked"
    UNKNOWN = "unknown"


class PatchProposalTraceObjectType(StrEnum):
    PATCH_INTENT_ENVELOPE = "patch_intent_envelope"
    PATCH_SCOPE_POLICY = "patch_scope_policy"
    PATCH_TARGET_SELECTOR = "patch_target_selector"
    REFERENCE_PATTERN_DIGEST = "reference_pattern_digest"
    REFERENCE_HARNESS_PATTERN = "reference_harness_pattern"
    PATCH_CONTEXT_SNAPSHOT = "patch_context_snapshot"
    PATCH_CONTEXT_EVIDENCE_BUNDLE = "patch_context_evidence_bundle"
    PATCH_PLAN = "patch_plan"
    PATCH_CHANGE_SET_GRAPH = "patch_change_set_graph"
    PATCH_CHANGE_NODE = "patch_change_node"
    PATCH_DEPENDENCY_EDGE = "patch_dependency_edge"
    DIFF_PROPOSAL_ENVELOPE = "diff_proposal_envelope"
    UNIFIED_DIFF_PROPOSAL = "unified_diff_proposal"
    STRUCTURED_PATCH_PROPOSAL = "structured_patch_proposal"
    PATCH_FILE_PROPOSAL = "patch_file_proposal"
    PATCH_HUNK_PROPOSAL = "patch_hunk_proposal"
    PATCH_RISK_SIGNAL = "patch_risk_signal"
    PATCH_PROPOSAL_RISK_REPORT = "patch_proposal_risk_report"
    PATCH_REVIEW_PACKET = "patch_review_packet"
    PATCH_REVIEW_CHECKLIST = "patch_review_checklist"
    PATCH_APPROVAL_GATE_METADATA = "patch_approval_gate_metadata"
    PATCH_REVIEWER_DECISION_PLACEHOLDER = "patch_reviewer_decision_placeholder"
    PATCH_REVIEWER_DECISION_RECORD = "patch_reviewer_decision_record"
    EXTERNAL_AGENT_CONTROL_PATTERN = "external_agent_control_pattern"
    DIGESTION_DOMINION_RECORD = "digestion_dominion_record"
    REFERENCE_CONTEXT = "reference_context"
    UNKNOWN = "unknown"


class PatchProposalTraceRelationType(StrEnum):
    INTENT_HAS_SCOPE = "intent_has_scope"
    SCOPE_SELECTS_TARGET = "scope_selects_target"
    DIGEST_INFORMS_INTENT = "digest_informs_intent"
    DIGEST_INFORMS_PLAN = "digest_informs_plan"
    CONTEXT_SUPPORTS_PLAN = "context_supports_plan"
    PLAN_CONTAINS_CHANGE_NODE = "plan_contains_change_node"
    PLAN_CONTAINS_DEPENDENCY_EDGE = "plan_contains_dependency_edge"
    CHANGE_NODE_TARGETS_FILE = "change_node_targets_file"
    GRAPH_PRODUCES_DIFF_ENVELOPE = "graph_produces_diff_envelope"
    DIFF_ENVELOPE_CONTAINS_STRUCTURED_PATCH = "diff_envelope_contains_structured_patch"
    DIFF_ENVELOPE_CONTAINS_UNIFIED_DIFF = "diff_envelope_contains_unified_diff"
    STRUCTURED_PATCH_CONTAINS_FILE_PROPOSAL = "structured_patch_contains_file_proposal"
    FILE_PROPOSAL_CONTAINS_HUNK = "file_proposal_contains_hunk"
    RISK_REPORT_SCANS_DIFF = "risk_report_scans_diff"
    RISK_SIGNAL_BLOCKS_PROPOSAL = "risk_signal_blocks_proposal"
    REVIEW_PACKET_SUMMARIZES_DIFF = "review_packet_summarizes_diff"
    REVIEW_PACKET_INCLUDES_RISK_REPORT = "review_packet_includes_risk_report"
    REVIEW_PACKET_HAS_CHECKLIST = "review_packet_has_checklist"
    REVIEW_PACKET_HAS_APPROVAL_GATE = "review_packet_has_approval_gate"
    REVIEW_DECISION_RECORDS_OUTCOME = "review_decision_records_outcome"
    TRACE_PACKET_CONTAINS_EVENT = "trace_packet_contains_event"
    TRACE_PACKET_CONTAINS_OBJECT = "trace_packet_contains_object"
    DIGESTION_PREFERS_PATTERN_ADAPTATION = "digestion_prefers_pattern_adaptation"
    DOMINION_PATTERN_FUTURE_GATED = "dominion_pattern_future_gated"
    EXTERNAL_AGENT_PATTERN_BLOCKED = "external_agent_pattern_blocked"
    UNKNOWN = "unknown"


class PatchProposalTraceAttributeKind(StrEnum):
    SUMMARY = "summary"
    STATUS = "status"
    READINESS_LEVEL = "readiness_level"
    DECISION_KIND = "decision_kind"
    OUTCOME_KIND = "outcome_kind"
    RISK_KIND = "risk_kind"
    SEVERITY = "severity"
    TARGET_PATH_REF = "target_path_ref"
    PROPOSAL_REF = "proposal_ref"
    REVIEW_STATUS = "review_status"
    APPROVAL_GATE_KIND = "approval_gate_kind"
    APPROVED_FOR_REVIEW = "approved_for_review"
    APPROVED_FOR_APPLY = "approved_for_apply"
    REDACTION_STATUS = "redaction_status"
    TRUNCATION_STATUS = "truncation_status"
    SOURCE_REF = "source_ref"
    EVIDENCE_REF = "evidence_ref"
    DIGEST_REF = "digest_ref"
    CONTEXT_SNAPSHOT_REF = "context_snapshot_ref"
    PATCH_PLAN_REF = "patch_plan_ref"
    DIFF_ENVELOPE_REF = "diff_envelope_ref"
    RISK_REPORT_REF = "risk_report_ref"
    REVIEW_PACKET_REF = "review_packet_ref"
    EXTERNAL_AGENT_PATTERN_KIND = "external_agent_pattern_kind"
    DIGESTION_DOMINION_DISPOSITION = "digestion_dominion_disposition"
    TIMESTAMP = "timestamp"
    UNKNOWN = "unknown"


class PatchProposalTraceSinkKind(StrEnum):
    RETURNED_TRACE_PACKET = "returned_trace_packet"
    IN_MEMORY_TEST_SINK = "in_memory_test_sink"
    DISABLED = "disabled"
    FUTURE_INTERNAL_OCEL_STORE = "future_internal_ocel_store"
    EXTERNAL_TRACE_SINK_BLOCKED = "external_trace_sink_blocked"
    UNKNOWN = "unknown"


class PatchProposalTraceStatus(StrEnum):
    UNKNOWN = "unknown"
    PLANNED = "planned"
    POLICY_CHECKED = "policy_checked"
    EMITTED_AS_PACKET = "emitted_as_packet"
    EMITTED_TO_IN_MEMORY_SINK = "emitted_to_in_memory_sink"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class PatchProposalTraceDecisionKind(StrEnum):
    ALLOW_TRACE_PACKET_CREATION = "allow_trace_packet_creation"
    ALLOW_IN_MEMORY_TEST_SINK = "allow_in_memory_test_sink"
    DENY = "deny"
    BLOCK = "block"
    SKIP = "skip"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class PatchProposalTraceRiskKind(StrEnum):
    RAW_DIFF_PERSISTENCE_RISK = "raw_diff_persistence_risk"
    RAW_SOURCE_PERSISTENCE_RISK = "raw_source_persistence_risk"
    RAW_REVIEW_PACKET_PERSISTENCE_RISK = "raw_review_packet_persistence_risk"
    SECRET_CONTENT_TRACE_RISK = "secret_content_trace_risk"
    CREDENTIAL_CONTENT_TRACE_RISK = "credential_content_trace_risk"
    TOKEN_CONTENT_TRACE_RISK = "token_content_trace_risk"
    UNBOUNDED_PAYLOAD_RISK = "unbounded_payload_risk"
    FULL_FILE_CONTENT_TRACE_RISK = "full_file_content_trace_risk"
    PATCH_APPLY_CONFUSION_RISK = "patch_apply_confusion_risk"
    WRITE_EDIT_CONFUSION_RISK = "write_edit_confusion_risk"
    APPROVAL_METADATA_CONFUSION_RISK = "approval_metadata_confusion_risk"
    EXTERNAL_AGENT_EXECUTION_CONFUSION_RISK = "external_agent_execution_confusion_risk"
    DOMINION_RUNTIME_CONFUSION_RISK = "dominion_runtime_confusion_risk"
    INFINITE_AGENT_LOOP_RISK = "infinite_agent_loop_risk"
    REFERENCE_EXECUTION_CONFUSION_RISK = "reference_execution_confusion_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    EXTERNAL_TRACE_SINK_RISK = "external_trace_sink_risk"
    UNKNOWN = "unknown"


class PatchProposalTraceSourceKind(StrEnum):
    V0356_PATCH_REVIEW_PACKET = "v0356_patch_review_packet"
    V0356_APPROVAL_GATE_METADATA = "v0356_approval_gate_metadata"
    V0356_REVIEWER_DECISION_RECORD = "v0356_reviewer_decision_record"
    V0355_PATCH_PROPOSAL_RISK_REPORT = "v0355_patch_proposal_risk_report"
    V0355_PATCH_RISK_SCAN_DECISION = "v0355_patch_risk_scan_decision"
    V0354_DIFF_PROPOSAL_ENVELOPE = "v0354_diff_proposal_envelope"
    V0354_UNIFIED_DIFF_PROPOSAL = "v0354_unified_diff_proposal"
    V0354_STRUCTURED_PATCH_PROPOSAL = "v0354_structured_patch_proposal"
    V0353_PATCH_PLAN = "v0353_patch_plan"
    V0353_CHANGE_SET_GRAPH = "v0353_change_set_graph"
    V0352_CONTEXT_SNAPSHOT = "v0352_context_snapshot"
    V0352_EVIDENCE_BUNDLE = "v0352_evidence_bundle"
    V0351_INTENT_SCOPE_BUNDLE = "v0351_intent_scope_bundle"
    V0350_REFERENCE_PATTERN_DIGEST = "v0350_reference_pattern_digest"
    EXTERNAL_AGENT_CONTROL_OBSERVATION = "external_agent_control_observation"
    DIGESTION_DOMINION_POLICY_NOTE = "digestion_dominion_policy_note"
    TEST_FIXTURE = "test_fixture"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    OPENCLAW_REFERENCE_CONTEXT_REF = "openclaw_reference_context_ref"
    UNKNOWN = "unknown"


class PatchProposalTraceReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    TRACE_CONTRACT_READY = "trace_contract_ready"
    TRACE_PACKET_READY = "trace_packet_ready"
    BOUNDED_PATCH_PROPOSAL_TRACE_READY = "bounded_patch_proposal_trace_ready"
    DIGESTION_DOMINION_TRACE_READY = "digestion_dominion_trace_ready"
    DESIGN_HANDOFF_READY_FOR_V0358 = "design_handoff_ready_for_v0358"
    DESIGN_HANDOFF_READY_FOR_V0359 = "design_handoff_ready_for_v0359"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ExternalAgentControlPatternKind(StrEnum):
    CODEX_TO_CLAUDE_CODE_LOOP = "codex_to_claude_code_loop"
    CODEX_TO_EXTERNAL_AGENT_CHAIN = "codex_to_external_agent_chain"
    CLAUDE_CODE_UNBOUNDED_LOOP = "claude_code_unbounded_loop"
    OPENCODE_EXECUTION_LOOP = "opencode_execution_loop"
    HERMES_EXECUTION_LOOP = "hermes_execution_loop"
    OPENCLAW_EXECUTION_LOOP = "openclaw_execution_loop"
    RECURSIVE_AGENT_SELF_INVOCATION = "recursive_agent_self_invocation"
    INFINITE_AGENT_LOOP = "infinite_agent_loop"
    HARNESS_ORCHESTRATION_PATTERN = "harness_orchestration_pattern"
    DOMINION_LIKE_EXTERNAL_CONTROL = "dominion_like_external_control"
    SAFE_STATIC_DIGEST_PATTERN = "safe_static_digest_pattern"
    NO_EXTERNAL_AGENT_CONTROL = "no_external_agent_control"
    UNKNOWN = "unknown"


class DigestionDominionDisposition(StrEnum):
    DIGESTION_FIRST = "digestion_first"
    SAFELY_DIGESTED = "safely_digested"
    ADAPTED_WITHOUT_EXECUTION = "adapted_without_execution"
    REJECTED_FOR_SAFETY = "rejected_for_safety"
    DOMINION_FUTURE_GATED = "dominion_future_gated"
    DOMINION_BLOCKED = "dominion_blocked"
    EXTERNAL_AGENT_EXECUTION_BLOCKED = "external_agent_execution_blocked"
    INFINITE_LOOP_BLOCKED = "infinite_loop_blocked"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNKNOWN = "unknown"


UNSAFE_EXTERNAL_AGENT_PATTERN_KINDS = {
    ExternalAgentControlPatternKind.CODEX_TO_CLAUDE_CODE_LOOP,
    ExternalAgentControlPatternKind.CODEX_TO_EXTERNAL_AGENT_CHAIN,
    ExternalAgentControlPatternKind.CLAUDE_CODE_UNBOUNDED_LOOP,
    ExternalAgentControlPatternKind.OPENCODE_EXECUTION_LOOP,
    ExternalAgentControlPatternKind.HERMES_EXECUTION_LOOP,
    ExternalAgentControlPatternKind.OPENCLAW_EXECUTION_LOOP,
    ExternalAgentControlPatternKind.RECURSIVE_AGENT_SELF_INVOCATION,
    ExternalAgentControlPatternKind.INFINITE_AGENT_LOOP,
    ExternalAgentControlPatternKind.HARNESS_ORCHESTRATION_PATTERN,
    ExternalAgentControlPatternKind.DOMINION_LIKE_EXTERNAL_CONTROL,
}


def _validate_version(value: str) -> None:
    _require_non_blank("version", value)
    if V0357_VERSION not in value:
        raise ValueError("version must include v0.35.7")


def _validate_list(name: str, values: list[Any]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be a list")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    _validate_list(name, values)
    for value in values:
        enum_type(value)


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.35.7")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a dict")
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret", "credential", "api_key", "token")):
            raise ValueError("metadata keys must not request credential or secret material")


def _contains_prohibited_payload(value: str, patterns: list[str]) -> bool:
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _validate_prohibited_patterns(patterns: list[str]) -> None:
    _validate_string_list("prohibited_payload_patterns", patterns)
    lowered = {pattern.lower() for pattern in patterns}
    for required in DEFAULT_PROHIBITED_PAYLOAD_PATTERNS:
        if required not in lowered:
            raise ValueError("prohibited_payload_patterns must include secret/key/token/credential/pem/id_rsa-like patterns")


def _bounded(value: str, limit: int, marker: str = "...[truncated]") -> tuple[str, bool]:
    if limit < 0:
        raise ValueError("limit must be >= 0")
    if len(value) <= limit:
        return value, False
    if limit <= len(marker):
        return value[:limit], True
    return value[: limit - len(marker)] + marker, True


def _object_id(prefix: str, source_id: str) -> str:
    return f"object:{prefix}:{source_id}"


@dataclass(frozen=True)
class PatchProposalTraceFlagSet:
    flag_set_id: str
    version: str
    patch_proposal_trace_layer_constructed: bool
    trace_packet_creation_available: bool
    trace_validation_available: bool
    digestion_dominion_trace_metadata_available: bool
    external_agent_control_pattern_trace_available: bool
    ready_for_v0358_cli_patch_proposal_surface: bool
    ready_for_v0359_consolidation: bool
    ready_for_patch_proposal_trace_packet_creation: bool
    ready_for_bounded_patch_proposal_ocel_trace_emission: bool
    ready_for_digestion_dominion_trace_metadata: bool
    ready_for_external_agent_control_pattern_trace: bool
    ready_for_execution: bool = False
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
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_PATCH_PROPOSAL_TRACE_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceSourceRef:
    source_ref_id: str
    source_kind: PatchProposalTraceSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        PatchProposalTraceSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTracePolicy:
    trace_policy_id: str
    version: str
    allowed_event_kinds: list[PatchProposalTraceEventKind | str]
    allowed_object_types: list[PatchProposalTraceObjectType | str]
    allowed_relation_types: list[PatchProposalTraceRelationType | str]
    allowed_sink_kinds: list[PatchProposalTraceSinkKind | str]
    prohibited_attribute_kinds: list[PatchProposalTraceAttributeKind | str]
    prohibited_payload_patterns: list[str]
    max_attribute_chars: int
    max_event_count: int
    max_object_count: int
    max_relation_count: int
    allow_raw_diff: bool = False
    allow_raw_source: bool = False
    allow_raw_review_packet: bool = False
    allow_secret_content: bool = False
    allow_credential_content: bool = False
    allow_token_content: bool = False
    allow_full_file_content: bool = False
    allow_persistent_write: bool = False
    allow_external_sink: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    allow_infinite_agent_loop: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_policy_id", self.trace_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_event_kinds", self.allowed_event_kinds, PatchProposalTraceEventKind)
        _validate_enum_list("allowed_object_types", self.allowed_object_types, PatchProposalTraceObjectType)
        _validate_enum_list("allowed_relation_types", self.allowed_relation_types, PatchProposalTraceRelationType)
        _validate_enum_list("allowed_sink_kinds", self.allowed_sink_kinds, PatchProposalTraceSinkKind)
        allowed_runtime_sinks = {
            PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET,
            PatchProposalTraceSinkKind.IN_MEMORY_TEST_SINK,
            PatchProposalTraceSinkKind.DISABLED,
        }
        if any(PatchProposalTraceSinkKind(sink) not in allowed_runtime_sinks for sink in self.allowed_sink_kinds):
            raise ValueError("trace policy cannot allow persistent or external trace sinks")
        _validate_enum_list("prohibited_attribute_kinds", self.prohibited_attribute_kinds, PatchProposalTraceAttributeKind)
        _validate_prohibited_patterns(self.prohibited_payload_patterns)
        for name in ("max_attribute_chars", "max_event_count", "max_object_count", "max_relation_count"):
            _validate_non_negative(name, getattr(self, name))
        _validate_false(
            self,
            (
                "allow_raw_diff",
                "allow_raw_source",
                "allow_raw_review_packet",
                "allow_secret_content",
                "allow_credential_content",
                "allow_token_content",
                "allow_full_file_content",
                "allow_persistent_write",
                "allow_external_sink",
                "allow_external_agent_execution",
                "allow_dominion_runtime",
                "allow_infinite_agent_loop",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceAttribute:
    attribute_id: str
    attribute_kind: PatchProposalTraceAttributeKind | str
    key: str
    value_preview: str
    redacted: bool
    truncated: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("attribute_id", self.attribute_id)
        PatchProposalTraceAttributeKind(self.attribute_kind)
        _require_non_blank("key", self.key)
        max_chars = int(self.metadata.get("max_attribute_chars", DEFAULT_MAX_TRACE_ATTRIBUTE_CHARS))
        if len(self.value_preview) > max_chars:
            raise ValueError("value_preview must be bounded")
        if _contains_prohibited_payload(self.value_preview, DEFAULT_PROHIBITED_PAYLOAD_PATTERNS) and not self.redacted:
            raise ValueError("secret-like trace attribute values must be redacted")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceObject:
    object_id: str
    object_type: PatchProposalTraceObjectType | str
    object_key: str
    object_summary: str
    attributes: list[PatchProposalTraceAttribute] = field(default_factory=list)
    source_refs: list[PatchProposalTraceSourceRef] = field(default_factory=list)
    redacted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("object_id", "object_key", "object_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchProposalTraceObjectType(self.object_type)
        _validate_list("attributes", self.attributes)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceEvent:
    event_id: str
    event_kind: PatchProposalTraceEventKind | str
    event_label: str
    event_summary: str
    related_object_ids: list[str] = field(default_factory=list)
    attributes: list[PatchProposalTraceAttribute] = field(default_factory=list)
    source_refs: list[PatchProposalTraceSourceRef] = field(default_factory=list)
    redacted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("event_id", "event_label", "event_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchProposalTraceEventKind(self.event_kind)
        _validate_string_list("related_object_ids", self.related_object_ids)
        _validate_list("attributes", self.attributes)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceRelation:
    relation_id: str
    relation_type: PatchProposalTraceRelationType | str
    source_object_id: str
    target_object_id: str
    relation_summary: str
    event_id: str | None = None
    attributes: list[PatchProposalTraceAttribute] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("relation_id", "source_object_id", "target_object_id", "relation_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchProposalTraceRelationType(self.relation_type)
        if self.event_id is not None:
            _require_non_blank("event_id", self.event_id)
        _validate_list("attributes", self.attributes)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ExternalAgentControlPatternRecord:
    pattern_record_id: str
    pattern_kind: ExternalAgentControlPatternKind | str
    disposition: DigestionDominionDisposition | str
    pattern_summary: str
    evidence_refs: list[str]
    risk_kinds: list[PatchProposalTraceRiskKind | str]
    rejected: bool
    future_gated: bool
    execution_allowed: bool = False
    dominion_runtime_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("pattern_record_id", self.pattern_record_id)
        pattern_kind = ExternalAgentControlPatternKind(self.pattern_kind)
        DigestionDominionDisposition(self.disposition)
        _require_non_blank("pattern_summary", self.pattern_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchProposalTraceRiskKind)
        _validate_false(self, ("execution_allowed", "dominion_runtime_allowed"))
        if pattern_kind in UNSAFE_EXTERNAL_AGENT_PATTERN_KINDS and not (self.rejected or self.future_gated):
            raise ValueError("unsafe external agent control patterns must be rejected or future_gated")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DigestionDominionTraceRecord:
    digestion_record_id: str
    disposition: DigestionDominionDisposition | str
    source_pattern_record_ids: list[str]
    digestion_summary: str
    chantacore_adaptation: str
    rejected_items: list[str]
    future_track_items: list[str]
    execution_allowed: bool = False
    dominion_runtime_allowed: bool = False
    infinite_loop_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("digestion_record_id", self.digestion_record_id)
        DigestionDominionDisposition(self.disposition)
        for name in ("source_pattern_record_ids", "rejected_items", "future_track_items"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("digestion_summary", self.digestion_summary)
        _require_non_blank("chantacore_adaptation", self.chantacore_adaptation)
        _validate_false(self, ("execution_allowed", "dominion_runtime_allowed", "infinite_loop_allowed"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTracePacket:
    trace_packet_id: str
    version: str
    sink_kind: PatchProposalTraceSinkKind | str
    objects: list[PatchProposalTraceObject]
    events: list[PatchProposalTraceEvent]
    relations: list[PatchProposalTraceRelation]
    attributes: list[PatchProposalTraceAttribute]
    external_agent_patterns: list[ExternalAgentControlPatternRecord]
    digestion_dominion_records: list[DigestionDominionTraceRecord]
    source_refs: list[PatchProposalTraceSourceRef]
    status: PatchProposalTraceStatus | str
    redaction_applied: bool
    truncated: bool
    summary: str
    ready_for_persistent_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_packet_id", self.trace_packet_id)
        _validate_version(self.version)
        sink_kind = PatchProposalTraceSinkKind(self.sink_kind)
        if sink_kind in {PatchProposalTraceSinkKind.FUTURE_INTERNAL_OCEL_STORE, PatchProposalTraceSinkKind.EXTERNAL_TRACE_SINK_BLOCKED, PatchProposalTraceSinkKind.UNKNOWN}:
            raise ValueError("trace packet sink must be returned/in-memory/disabled only")
        for name in ("objects", "events", "relations", "attributes", "external_agent_patterns", "digestion_dominion_records", "source_refs"):
            _validate_list(name, getattr(self, name))
        PatchProposalTraceStatus(self.status)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_persistent_write", "ready_for_external_sink", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceEmissionInput:
    emission_input_id: str
    version: str
    requested_sink_kind: PatchProposalTraceSinkKind | str
    review_packet_id: str | None
    proposal_risk_report_id: str | None
    diff_envelope_id: str | None
    patch_plan_id: str | None
    reference_digest_id: str | None
    task_summary: str
    source_refs: list[PatchProposalTraceSourceRef]
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_RUNTIME_ACTIONS))
    allow_raw_diff: bool = False
    allow_raw_source: bool = False
    allow_raw_review_packet: bool = False
    allow_secret_content: bool = False
    allow_credential_content: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    allow_persistent_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emission_input_id", self.emission_input_id)
        _validate_version(self.version)
        PatchProposalTraceSinkKind(self.requested_sink_kind)
        for name in ("review_packet_id", "proposal_risk_report_id", "diff_envelope_id", "patch_plan_id", "reference_digest_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"trace_persistence", "patch_application", "workspace_write", "external_agent_execution", "dominion_runtime", "credential_access"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include persistence/apply/write/external-agent/dominion/credential actions")
        _validate_false(
            self,
            (
                "allow_raw_diff",
                "allow_raw_source",
                "allow_raw_review_packet",
                "allow_secret_content",
                "allow_credential_content",
                "allow_external_agent_execution",
                "allow_dominion_runtime",
                "allow_persistent_write",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceEmissionDecision:
    decision_id: str
    emission_input_id: str
    decision_kind: PatchProposalTraceDecisionKind | str
    decision_summary: str
    allowed_sink_kind: PatchProposalTraceSinkKind | str | None
    risk_kinds: list[PatchProposalTraceRiskKind | str]
    persistent_write_allowed: bool = False
    external_sink_allowed: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "emission_input_id", "decision_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchProposalTraceDecisionKind(self.decision_kind)
        if self.allowed_sink_kind is not None:
            sink_kind = PatchProposalTraceSinkKind(self.allowed_sink_kind)
            if sink_kind not in {PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET, PatchProposalTraceSinkKind.IN_MEMORY_TEST_SINK, PatchProposalTraceSinkKind.DISABLED}:
                raise ValueError("allowed_sink_kind cannot be persistent or external")
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchProposalTraceRiskKind)
        _validate_false(self, ("persistent_write_allowed", "external_sink_allowed", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceValidationReport:
    validation_report_id: str
    version: str
    trace_packet_id: str | None
    blocked_items: list[str]
    warning_items: list[str]
    valid: bool
    summary: str
    ready_for_persistent_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        if self.trace_packet_id is not None:
            _require_non_blank("trace_packet_id", self.trace_packet_id)
        _validate_string_list("blocked_items", self.blocked_items)
        _validate_string_list("warning_items", self.warning_items)
        if self.blocked_items and self.valid:
            raise ValueError("validation report cannot be valid when blocked_items exist")
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_persistent_write", "ready_for_external_sink", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceEmissionReport:
    emission_report_id: str
    version: str
    emission_input_id: str
    decision_id: str
    trace_packet_id: str | None
    summary: str
    packet_returned: bool
    emitted_to_in_memory_sink: bool
    persistent_write_performed: bool = False
    external_sink_used: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("emission_report_id", "emission_input_id", "decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.trace_packet_id is not None:
            _require_non_blank("trace_packet_id", self.trace_packet_id)
        _validate_false(self, ("persistent_write_performed", "external_sink_used", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceEmitter:
    emitter_id: str
    version: str
    trace_policy: PatchProposalTracePolicy
    supported_sink_kinds: list[PatchProposalTraceSinkKind | str]
    ready_for_persistent_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emitter_id", self.emitter_id)
        _validate_version(self.version)
        if not isinstance(self.trace_policy, PatchProposalTracePolicy):
            raise TypeError("trace_policy must be PatchProposalTracePolicy")
        _validate_enum_list("supported_sink_kinds", self.supported_sink_kinds, PatchProposalTraceSinkKind)
        if any(PatchProposalTraceSinkKind(kind) not in {PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET, PatchProposalTraceSinkKind.IN_MEMORY_TEST_SINK, PatchProposalTraceSinkKind.DISABLED} for kind in self.supported_sink_kinds):
            raise ValueError("emitter cannot support persistent or external sinks")
        _validate_false(self, ("ready_for_persistent_write", "ready_for_external_sink", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceRunPreview:
    run_preview_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_trace_persistence_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_external_agent_execution_guarantee: bool = True
    no_dominion_runtime_guarantee: bool = True
    no_infinite_agent_loop_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalTraceNoPersistenceGuarantee:
    guarantee_id: str
    version: str
    no_trace_persistence: bool = True
    no_ocel_file_write: bool = True
    no_jsonl_write: bool = True
    no_log_write: bool = True
    no_database_write: bool = True
    no_patch_application: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_apply_patch_runtime_call: bool = True
    no_git_apply_runtime_call: bool = True
    no_shell_execution: bool = True
    no_test_execution: bool = True
    no_dependency_install: bool = True
    no_reference_execution: bool = True
    no_reference_import: bool = True
    no_external_agent_execution: bool = True
    no_claude_code_invocation: bool = True
    no_codex_cli_invocation: bool = True
    no_dominion_runtime: bool = True
    no_infinite_agent_loop: bool = True
    no_provider_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_ui_runtime: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0357ReadinessReport:
    report_id: str
    version: str
    trace_packet_id: str | None
    summary: str
    completed_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0358_cli_patch_proposal_surface: bool = True
    ready_for_v0359_consolidation: bool = True
    ready_for_patch_proposal_trace_packet_creation: bool = True
    ready_for_bounded_patch_proposal_ocel_trace_emission: bool = True
    ready_for_digestion_dominion_trace_metadata: bool = True
    ready_for_external_agent_control_pattern_trace: bool = True
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        if self.trace_packet_id is not None:
            _require_non_blank("trace_packet_id", self.trace_packet_id)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        unsafe_names = tuple(name for name in UNSAFE_PATCH_PROPOSAL_TRACE_FLAG_NAMES if hasattr(self, name))
        _validate_false(self, unsafe_names)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


def default_patch_proposal_trace_policy(**kwargs: Any) -> PatchProposalTracePolicy:
    return build_patch_proposal_trace_policy(**kwargs)


def build_patch_proposal_trace_flags(flag_set_id: str = "patch_proposal_trace_flags:v0.35.7", **kwargs: Any) -> PatchProposalTraceFlagSet:
    return PatchProposalTraceFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0357_VERSION),
        patch_proposal_trace_layer_constructed=kwargs.pop("patch_proposal_trace_layer_constructed", True),
        trace_packet_creation_available=kwargs.pop("trace_packet_creation_available", True),
        trace_validation_available=kwargs.pop("trace_validation_available", True),
        digestion_dominion_trace_metadata_available=kwargs.pop("digestion_dominion_trace_metadata_available", True),
        external_agent_control_pattern_trace_available=kwargs.pop("external_agent_control_pattern_trace_available", True),
        ready_for_v0358_cli_patch_proposal_surface=kwargs.pop("ready_for_v0358_cli_patch_proposal_surface", True),
        ready_for_v0359_consolidation=kwargs.pop("ready_for_v0359_consolidation", True),
        ready_for_patch_proposal_trace_packet_creation=kwargs.pop("ready_for_patch_proposal_trace_packet_creation", True),
        ready_for_bounded_patch_proposal_ocel_trace_emission=kwargs.pop("ready_for_bounded_patch_proposal_ocel_trace_emission", True),
        ready_for_digestion_dominion_trace_metadata=kwargs.pop("ready_for_digestion_dominion_trace_metadata", True),
        ready_for_external_agent_control_pattern_trace=kwargs.pop("ready_for_external_agent_control_pattern_trace", True),
        **kwargs,
    )


def build_patch_proposal_trace_source_ref(source_ref_id: str = "patch_trace_source:v0.35.7:review", **kwargs: Any) -> PatchProposalTraceSourceRef:
    return PatchProposalTraceSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", PatchProposalTraceSourceKind.V0356_PATCH_REVIEW_PACKET),
        source_id=kwargs.pop("source_id", "review_packet:v0.35.6"),
        source_summary=kwargs.pop("source_summary", "Supplied review packet metadata source; no execution or file access."),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0356_REVIEW_DOC_REF]),
        **kwargs,
    )


def build_patch_proposal_trace_policy(trace_policy_id: str = "patch_trace_policy:v0.35.7", **kwargs: Any) -> PatchProposalTracePolicy:
    return PatchProposalTracePolicy(
        trace_policy_id=trace_policy_id,
        version=kwargs.pop("version", V0357_VERSION),
        allowed_event_kinds=kwargs.pop("allowed_event_kinds", list(PatchProposalTraceEventKind)),
        allowed_object_types=kwargs.pop("allowed_object_types", list(PatchProposalTraceObjectType)),
        allowed_relation_types=kwargs.pop("allowed_relation_types", list(PatchProposalTraceRelationType)),
        allowed_sink_kinds=kwargs.pop("allowed_sink_kinds", [PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET, PatchProposalTraceSinkKind.IN_MEMORY_TEST_SINK, PatchProposalTraceSinkKind.DISABLED]),
        prohibited_attribute_kinds=kwargs.pop("prohibited_attribute_kinds", []),
        prohibited_payload_patterns=kwargs.pop("prohibited_payload_patterns", list(DEFAULT_PROHIBITED_PAYLOAD_PATTERNS)),
        max_attribute_chars=kwargs.pop("max_attribute_chars", DEFAULT_MAX_TRACE_ATTRIBUTE_CHARS),
        max_event_count=kwargs.pop("max_event_count", 200),
        max_object_count=kwargs.pop("max_object_count", 200),
        max_relation_count=kwargs.pop("max_relation_count", 300),
        **kwargs,
    )


def sanitize_patch_proposal_trace_attribute_value(value: Any, policy: PatchProposalTracePolicy | None = None) -> PatchProposalTraceAttribute:
    policy = policy or default_patch_proposal_trace_policy()
    preview = "" if value is None else str(value)
    redacted = False
    if _contains_prohibited_payload(preview, policy.prohibited_payload_patterns):
        preview = "[redacted]"
        redacted = True
    preview, truncated = _bounded(preview, policy.max_attribute_chars)
    return build_patch_proposal_trace_attribute(
        attribute_id="patch_trace_attribute:v0.35.7:sanitized",
        value_preview=preview,
        redacted=redacted,
        truncated=truncated,
        metadata={"max_attribute_chars": policy.max_attribute_chars},
    )


def build_patch_proposal_trace_attribute(attribute_id: str = "patch_trace_attribute:v0.35.7:summary", **kwargs: Any) -> PatchProposalTraceAttribute:
    policy = kwargs.pop("policy", None) or default_patch_proposal_trace_policy()
    value = kwargs.pop("value", None)
    if value is not None and "value_preview" not in kwargs:
        preview = str(value)
        redacted = _contains_prohibited_payload(preview, policy.prohibited_payload_patterns)
        if redacted:
            preview = "[redacted]"
        preview, truncated = _bounded(preview, policy.max_attribute_chars)
        kwargs.setdefault("redacted", redacted)
        kwargs.setdefault("truncated", truncated)
        kwargs.setdefault("value_preview", preview)
    return PatchProposalTraceAttribute(
        attribute_id=attribute_id,
        attribute_kind=kwargs.pop("attribute_kind", PatchProposalTraceAttributeKind.SUMMARY),
        key=kwargs.pop("key", "summary"),
        value_preview=kwargs.pop("value_preview", "bounded patch proposal trace metadata"),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", False),
        metadata=kwargs.pop("metadata", {"max_attribute_chars": policy.max_attribute_chars}),
        **kwargs,
    )


def build_patch_proposal_trace_object(object_id: str = "patch_trace_object:v0.35.7:review", **kwargs: Any) -> PatchProposalTraceObject:
    return PatchProposalTraceObject(
        object_id=object_id,
        object_type=kwargs.pop("object_type", PatchProposalTraceObjectType.PATCH_REVIEW_PACKET),
        object_key=kwargs.pop("object_key", "review_packet:v0.35.6"),
        object_summary=kwargs.pop("object_summary", "Trace object is bounded metadata, not registry mutation."),
        attributes=kwargs.pop("attributes", [build_patch_proposal_trace_attribute()]),
        source_refs=kwargs.pop("source_refs", [build_patch_proposal_trace_source_ref()]),
        redacted=kwargs.pop("redacted", False),
        **kwargs,
    )


def build_patch_proposal_trace_event(event_id: str = "patch_trace_event:v0.35.7:review_packet_created", **kwargs: Any) -> PatchProposalTraceEvent:
    return PatchProposalTraceEvent(
        event_id=event_id,
        event_kind=kwargs.pop("event_kind", PatchProposalTraceEventKind.HUMAN_REVIEW_PACKET_CREATED),
        event_label=kwargs.pop("event_label", "Human review packet traced"),
        event_summary=kwargs.pop("event_summary", "Trace event is metadata only and performs no execution."),
        related_object_ids=kwargs.pop("related_object_ids", ["patch_trace_object:v0.35.7:review"]),
        attributes=kwargs.pop("attributes", [build_patch_proposal_trace_attribute()]),
        source_refs=kwargs.pop("source_refs", [build_patch_proposal_trace_source_ref()]),
        redacted=kwargs.pop("redacted", False),
        **kwargs,
    )


def build_patch_proposal_trace_relation(relation_id: str = "patch_trace_relation:v0.35.7:packet_contains_object", **kwargs: Any) -> PatchProposalTraceRelation:
    return PatchProposalTraceRelation(
        relation_id=relation_id,
        relation_type=kwargs.pop("relation_type", PatchProposalTraceRelationType.TRACE_PACKET_CONTAINS_OBJECT),
        source_object_id=kwargs.pop("source_object_id", "trace_packet:v0.35.7"),
        target_object_id=kwargs.pop("target_object_id", "patch_trace_object:v0.35.7:review"),
        relation_summary=kwargs.pop("relation_summary", "Trace relation is metadata only, not execution."),
        event_id=kwargs.pop("event_id", None),
        attributes=kwargs.pop("attributes", []),
        **kwargs,
    )


def build_external_agent_control_pattern_record(pattern_record_id: str = "external_agent_pattern:v0.35.7:codex_claude_loop", **kwargs: Any) -> ExternalAgentControlPatternRecord:
    pattern_kind = ExternalAgentControlPatternKind(kwargs.pop("pattern_kind", ExternalAgentControlPatternKind.CODEX_TO_CLAUDE_CODE_LOOP))
    unsafe = pattern_kind in UNSAFE_EXTERNAL_AGENT_PATTERN_KINDS
    return ExternalAgentControlPatternRecord(
        pattern_record_id=pattern_record_id,
        pattern_kind=pattern_kind,
        disposition=kwargs.pop("disposition", DigestionDominionDisposition.DOMINION_FUTURE_GATED if unsafe else DigestionDominionDisposition.SAFELY_DIGESTED),
        pattern_summary=kwargs.pop("pattern_summary", "External agent control pattern is traced as blocked/future-gated metadata only."),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0357_DOC_PATH]),
        risk_kinds=kwargs.pop("risk_kinds", [PatchProposalTraceRiskKind.EXTERNAL_AGENT_EXECUTION_CONFUSION_RISK, PatchProposalTraceRiskKind.INFINITE_AGENT_LOOP_RISK] if unsafe else []),
        rejected=kwargs.pop("rejected", unsafe),
        future_gated=kwargs.pop("future_gated", unsafe),
        **kwargs,
    )


def build_digestion_dominion_trace_record(digestion_record_id: str = "digestion_dominion:v0.35.7", **kwargs: Any) -> DigestionDominionTraceRecord:
    return DigestionDominionTraceRecord(
        digestion_record_id=digestion_record_id,
        disposition=kwargs.pop("disposition", DigestionDominionDisposition.DIGESTION_FIRST),
        source_pattern_record_ids=kwargs.pop("source_pattern_record_ids", ["external_agent_pattern:v0.35.7:codex_claude_loop"]),
        digestion_summary=kwargs.pop("digestion_summary", "Digestion-first policy is traced; Dominion escalation remains blocked/future-gated."),
        chantacore_adaptation=kwargs.pop("chantacore_adaptation", "Represent external agent control patterns as metadata only."),
        rejected_items=kwargs.pop("rejected_items", ["external agent execution", "infinite agent loop", "Dominion runtime"]),
        future_track_items=kwargs.pop("future_track_items", ["future gated Dominion review only"]),
        **kwargs,
    )


def build_patch_proposal_trace_packet(trace_packet_id: str = "trace_packet:v0.35.7", **kwargs: Any) -> PatchProposalTracePacket:
    return PatchProposalTracePacket(
        trace_packet_id=trace_packet_id,
        version=kwargs.pop("version", V0357_VERSION),
        sink_kind=kwargs.pop("sink_kind", PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET),
        objects=kwargs.pop("objects", [build_patch_proposal_trace_object()]),
        events=kwargs.pop("events", [build_patch_proposal_trace_event()]),
        relations=kwargs.pop("relations", [build_patch_proposal_trace_relation()]),
        attributes=kwargs.pop("attributes", [build_patch_proposal_trace_attribute()]),
        external_agent_patterns=kwargs.pop("external_agent_patterns", [build_external_agent_control_pattern_record()]),
        digestion_dominion_records=kwargs.pop("digestion_dominion_records", [build_digestion_dominion_trace_record()]),
        source_refs=kwargs.pop("source_refs", [build_patch_proposal_trace_source_ref()]),
        status=kwargs.pop("status", PatchProposalTraceStatus.EMITTED_AS_PACKET),
        redaction_applied=kwargs.pop("redaction_applied", False),
        truncated=kwargs.pop("truncated", False),
        summary=kwargs.pop("summary", "Patch proposal trace packet is returned/in-memory metadata, not persistent storage."),
        **kwargs,
    )


def build_patch_proposal_trace_emission_input(emission_input_id: str = "patch_trace_emission_input:v0.35.7", **kwargs: Any) -> PatchProposalTraceEmissionInput:
    return PatchProposalTraceEmissionInput(
        emission_input_id=emission_input_id,
        version=kwargs.pop("version", V0357_VERSION),
        requested_sink_kind=kwargs.pop("requested_sink_kind", PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET),
        review_packet_id=kwargs.pop("review_packet_id", "review_packet:v0.35.6"),
        proposal_risk_report_id=kwargs.pop("proposal_risk_report_id", "proposal_risk_report:v0.35.5"),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:v0.35.4"),
        patch_plan_id=kwargs.pop("patch_plan_id", "patch_plan:v0.35.3"),
        reference_digest_id=kwargs.pop("reference_digest_id", "reference_pattern_digest:v0.35.0"),
        task_summary=kwargs.pop("task_summary", "Create returned patch proposal trace packet metadata only."),
        source_refs=kwargs.pop("source_refs", [build_patch_proposal_trace_source_ref()]),
        **kwargs,
    )


def build_patch_proposal_trace_emission_decision(decision_id: str = "patch_trace_decision:v0.35.7", **kwargs: Any) -> PatchProposalTraceEmissionDecision:
    return PatchProposalTraceEmissionDecision(
        decision_id=decision_id,
        emission_input_id=kwargs.pop("emission_input_id", "patch_trace_emission_input:v0.35.7"),
        decision_kind=kwargs.pop("decision_kind", PatchProposalTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION),
        decision_summary=kwargs.pop("decision_summary", "Returned trace packet creation is allowed; persistence is not allowed."),
        allowed_sink_kind=kwargs.pop("allowed_sink_kind", PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET),
        risk_kinds=kwargs.pop("risk_kinds", []),
        **kwargs,
    )


def build_patch_proposal_trace_validation_report(validation_report_id: str = "patch_trace_validation:v0.35.7", **kwargs: Any) -> PatchProposalTraceValidationReport:
    blocked_items = kwargs.pop("blocked_items", [])
    return PatchProposalTraceValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0357_VERSION),
        trace_packet_id=kwargs.pop("trace_packet_id", "trace_packet:v0.35.7"),
        blocked_items=blocked_items,
        warning_items=kwargs.pop("warning_items", []),
        valid=kwargs.pop("valid", not blocked_items),
        summary=kwargs.pop("summary", "Trace validation checks bounded returned metadata only."),
        **kwargs,
    )


def build_patch_proposal_trace_emission_report(emission_report_id: str = "patch_trace_emission_report:v0.35.7", **kwargs: Any) -> PatchProposalTraceEmissionReport:
    return PatchProposalTraceEmissionReport(
        emission_report_id=emission_report_id,
        version=kwargs.pop("version", V0357_VERSION),
        emission_input_id=kwargs.pop("emission_input_id", "patch_trace_emission_input:v0.35.7"),
        decision_id=kwargs.pop("decision_id", "patch_trace_decision:v0.35.7"),
        trace_packet_id=kwargs.pop("trace_packet_id", "trace_packet:v0.35.7"),
        summary=kwargs.pop("summary", "Trace packet returned without persistent write or external sink."),
        packet_returned=kwargs.pop("packet_returned", True),
        emitted_to_in_memory_sink=kwargs.pop("emitted_to_in_memory_sink", False),
        **kwargs,
    )


def build_patch_proposal_trace_emitter(emitter_id: str = "patch_trace_emitter:v0.35.7", **kwargs: Any) -> PatchProposalTraceEmitter:
    return PatchProposalTraceEmitter(
        emitter_id=emitter_id,
        version=kwargs.pop("version", V0357_VERSION),
        trace_policy=kwargs.pop("trace_policy", default_patch_proposal_trace_policy()),
        supported_sink_kinds=kwargs.pop("supported_sink_kinds", [PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET, PatchProposalTraceSinkKind.IN_MEMORY_TEST_SINK, PatchProposalTraceSinkKind.DISABLED]),
        **kwargs,
    )


def build_patch_proposal_trace_run_preview(run_preview_id: str = "patch_trace_run_preview:v0.35.7", **kwargs: Any) -> PatchProposalTraceRunPreview:
    return PatchProposalTraceRunPreview(
        run_preview_id=run_preview_id,
        planned_steps=kwargs.pop("planned_steps", ["summarize supplied artifacts", "create trace objects/events/relations", "record digestion/dominion metadata", "return trace packet"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["PatchProposalTracePacket", "PatchProposalTraceValidationReport", "V0357ReadinessReport"]),
        explicitly_not_performed=kwargs.pop("explicitly_not_performed", ["trace persistence", "OCEL file write", "patch application", "external agent execution", "Dominion runtime"]),
        **kwargs,
    )


def build_patch_proposal_trace_no_persistence_guarantee(guarantee_id: str = "patch_trace_no_persistence:v0.35.7", **kwargs: Any) -> PatchProposalTraceNoPersistenceGuarantee:
    return PatchProposalTraceNoPersistenceGuarantee(
        guarantee_id=guarantee_id,
        version=kwargs.pop("version", V0357_VERSION),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0357_DOC_PATH]),
        **kwargs,
    )


def build_v0357_readiness_report(report_id: str = "readiness:v0.35.7", **kwargs: Any) -> V0357ReadinessReport:
    return V0357ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0357_VERSION),
        trace_packet_id=kwargs.pop("trace_packet_id", "trace_packet:v0.35.7"),
        summary=kwargs.pop("summary", "v0.35.7 is ready for v0.35.8/v0.35.9 design-stage handoff only."),
        completed_items=kwargs.pop("completed_items", ["PatchProposalTracePacket", "PatchProposalTraceEvent", "PatchProposalTraceObject", "DigestionDominionTraceRecord"]),
        blocked_items=kwargs.pop("blocked_items", ["trace persistence", "patch application", "external agent execution", "Dominion runtime", "infinite agent loop"]),
        future_track_items=kwargs.pop("future_track_items", ["v0.35.8 CLI Patch Proposal Surface", "v0.35.9 Controlled Patch Proposal Layer Consolidation"]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0357_DOC_PATH, DEFAULT_V0356_REVIEW_DOC_REF, DEFAULT_V0355_RISK_DOC_REF, DEFAULT_V0354_DIFF_DOC_REF, DEFAULT_V0353_PLAN_DOC_REF, DEFAULT_V0352_CONTEXT_DOC_REF, DEFAULT_V0350_DIGEST_REF]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["Any trace persistence, apply/write/edit, external agent, Dominion runtime, or infinite-loop path is introduced."]),
        **kwargs,
    )


def _packet_with(
    trace_packet_id: str,
    source_ref: PatchProposalTraceSourceRef,
    object_type: PatchProposalTraceObjectType,
    object_key: str,
    object_summary: str,
    event_kind: PatchProposalTraceEventKind,
    event_label: str,
    event_summary: str,
    attributes: list[PatchProposalTraceAttribute] | None = None,
    relations: list[PatchProposalTraceRelation] | None = None,
    **kwargs: Any,
) -> PatchProposalTracePacket:
    obj = build_patch_proposal_trace_object(
        object_id=_object_id(str(object_type), object_key),
        object_type=object_type,
        object_key=object_key,
        object_summary=object_summary,
        attributes=attributes or [build_patch_proposal_trace_attribute(value=object_summary)],
        source_refs=[source_ref],
    )
    event = build_patch_proposal_trace_event(
        event_id=f"event:{trace_packet_id}:{event_kind}",
        event_kind=event_kind,
        event_label=event_label,
        event_summary=event_summary,
        related_object_ids=[obj.object_id],
        source_refs=[source_ref],
    )
    return build_patch_proposal_trace_packet(
        trace_packet_id=trace_packet_id,
        objects=[obj],
        events=[event],
        relations=relations or [],
        attributes=attributes or [],
        source_refs=[source_ref],
        redaction_applied=any(attribute.redacted for attribute in (attributes or [])),
        truncated=any(attribute.truncated for attribute in (attributes or [])),
        summary=event_summary,
        **kwargs,
    )


def build_patch_proposal_trace_packet_from_review_packet(review_packet: PatchReviewPacket | None = None, policy: PatchProposalTracePolicy | None = None) -> PatchProposalTracePacket:
    policy = policy or default_patch_proposal_trace_policy()
    if review_packet is None:
        return build_patch_proposal_trace_packet(
            trace_packet_id="trace_packet:v0.35.7:missing_review",
            objects=[],
            events=[],
            relations=[],
            attributes=[sanitize_patch_proposal_trace_attribute_value("missing review packet", policy)],
            status=PatchProposalTraceStatus.BLOCKED,
            summary="Trace packet blocked because review packet metadata is missing.",
        )
    source_ref = build_patch_proposal_trace_source_ref(source_id=review_packet.review_packet_id, source_summary="Supplied v0.35.6 review packet metadata.")
    attributes = [
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.REVIEW_PACKET_REF, key="review_packet_id", value=review_packet.review_packet_id, policy=policy),
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.REVIEW_STATUS, key="status", value=str(review_packet.status), policy=policy),
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.APPROVED_FOR_REVIEW, key="approved_for_review", value=str(review_packet.approved_for_review), policy=policy),
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.APPROVED_FOR_APPLY, key="approved_for_apply", value=str(review_packet.approved_for_apply), policy=policy),
    ]
    packet = _packet_with(
        "trace_packet:v0.35.7:review",
        source_ref,
        PatchProposalTraceObjectType.PATCH_REVIEW_PACKET,
        review_packet.review_packet_id,
        review_packet.summary,
        PatchProposalTraceEventKind.HUMAN_REVIEW_PACKET_CREATED,
        "Human review packet traced",
        "PatchReviewPacket metadata traced without apply permission or persistence.",
        attributes=attributes,
    )
    approval_obj = build_patch_proposal_trace_object(
        object_id=_object_id("approval_gate", review_packet.approval_gate_metadata.approval_gate_id),
        object_type=PatchProposalTraceObjectType.PATCH_APPROVAL_GATE_METADATA,
        object_key=review_packet.approval_gate_metadata.approval_gate_id,
        object_summary=review_packet.approval_gate_metadata.gate_summary,
        source_refs=[source_ref],
    )
    return build_patch_proposal_trace_packet(
        trace_packet_id=packet.trace_packet_id,
        objects=packet.objects + [approval_obj],
        events=packet.events,
        relations=[
            build_patch_proposal_trace_relation(
                relation_id="relation:v0.35.7:review_has_gate",
                relation_type=PatchProposalTraceRelationType.REVIEW_PACKET_HAS_APPROVAL_GATE,
                source_object_id=packet.objects[0].object_id,
                target_object_id=approval_obj.object_id,
            )
        ],
        attributes=attributes,
        source_refs=[source_ref],
        redaction_applied=packet.redaction_applied,
        truncated=packet.truncated,
        summary=packet.summary,
    )


def build_patch_proposal_trace_packet_from_risk_report(risk_report: PatchProposalRiskReport | None = None, policy: PatchProposalTracePolicy | None = None) -> PatchProposalTracePacket:
    policy = policy or default_patch_proposal_trace_policy()
    if risk_report is None:
        return build_patch_proposal_trace_packet(trace_packet_id="trace_packet:v0.35.7:missing_risk", status=PatchProposalTraceStatus.BLOCKED, summary="Trace packet blocked because risk report metadata is missing.")
    source_ref = build_patch_proposal_trace_source_ref(source_kind=PatchProposalTraceSourceKind.V0355_PATCH_PROPOSAL_RISK_REPORT, source_id=risk_report.proposal_risk_report_id, source_summary="Supplied v0.35.5 risk report metadata.")
    attributes = [
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.RISK_REPORT_REF, key="risk_report_id", value=risk_report.proposal_risk_report_id, policy=policy),
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.DECISION_KIND, key="overall_decision", value=str(risk_report.overall_decision), policy=policy),
    ]
    return _packet_with("trace_packet:v0.35.7:risk", source_ref, PatchProposalTraceObjectType.PATCH_PROPOSAL_RISK_REPORT, risk_report.proposal_risk_report_id, risk_report.summary, PatchProposalTraceEventKind.PATCH_RISK_SCANNED, "Patch risk report traced", "PatchProposalRiskReport metadata traced as review input, not approval.", attributes=attributes)


def build_patch_proposal_trace_packet_from_diff_envelope(diff_envelope: DiffProposalEnvelope | None = None, policy: PatchProposalTracePolicy | None = None) -> PatchProposalTracePacket:
    policy = policy or default_patch_proposal_trace_policy()
    if diff_envelope is None:
        return build_patch_proposal_trace_packet(trace_packet_id="trace_packet:v0.35.7:missing_diff", status=PatchProposalTraceStatus.BLOCKED, summary="Trace packet blocked because diff envelope metadata is missing.")
    source_ref = build_patch_proposal_trace_source_ref(source_kind=PatchProposalTraceSourceKind.V0354_DIFF_PROPOSAL_ENVELOPE, source_id=diff_envelope.diff_envelope_id, source_summary="Supplied v0.35.4 diff envelope metadata.")
    attributes = [
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.DIFF_ENVELOPE_REF, key="diff_envelope_id", value=diff_envelope.diff_envelope_id, policy=policy),
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.STATUS, key="status", value=str(diff_envelope.status), policy=policy),
    ]
    packet = _packet_with("trace_packet:v0.35.7:diff", source_ref, PatchProposalTraceObjectType.DIFF_PROPOSAL_ENVELOPE, diff_envelope.diff_envelope_id, diff_envelope.summary, PatchProposalTraceEventKind.DIFF_PROPOSAL_CREATED, "Diff proposal envelope traced", "DiffProposalEnvelope metadata traced without applying or persisting diff text.", attributes=attributes)
    objects = list(packet.objects)
    relations: list[PatchProposalTraceRelation] = []
    if diff_envelope.structured_patch is not None:
        structured_obj = build_patch_proposal_trace_object(
            object_id=_object_id("structured_patch", diff_envelope.structured_patch.structured_patch_id),
            object_type=PatchProposalTraceObjectType.STRUCTURED_PATCH_PROPOSAL,
            object_key=diff_envelope.structured_patch.structured_patch_id,
            object_summary=diff_envelope.structured_patch.proposal_summary,
            source_refs=[source_ref],
        )
        objects.append(structured_obj)
        relations.append(build_patch_proposal_trace_relation(relation_id="relation:v0.35.7:diff_structured", relation_type=PatchProposalTraceRelationType.DIFF_ENVELOPE_CONTAINS_STRUCTURED_PATCH, source_object_id=packet.objects[0].object_id, target_object_id=structured_obj.object_id))
    if diff_envelope.unified_diff is not None:
        unified_obj = build_patch_proposal_trace_object(
            object_id=_object_id("unified_diff", diff_envelope.unified_diff.unified_diff_id),
            object_type=PatchProposalTraceObjectType.UNIFIED_DIFF_PROPOSAL,
            object_key=diff_envelope.unified_diff.unified_diff_id,
            object_summary=diff_envelope.unified_diff.diff_summary,
            source_refs=[source_ref],
        )
        objects.append(unified_obj)
        relations.append(build_patch_proposal_trace_relation(relation_id="relation:v0.35.7:diff_unified", relation_type=PatchProposalTraceRelationType.DIFF_ENVELOPE_CONTAINS_UNIFIED_DIFF, source_object_id=packet.objects[0].object_id, target_object_id=unified_obj.object_id))
    return build_patch_proposal_trace_packet(trace_packet_id=packet.trace_packet_id, objects=objects, events=packet.events, relations=relations, attributes=attributes, source_refs=[source_ref], summary=packet.summary)


def build_patch_proposal_trace_packet_from_patch_plan(patch_plan: PatchPlan | None = None, policy: PatchProposalTracePolicy | None = None) -> PatchProposalTracePacket:
    policy = policy or default_patch_proposal_trace_policy()
    if patch_plan is None:
        return build_patch_proposal_trace_packet(trace_packet_id="trace_packet:v0.35.7:missing_plan", status=PatchProposalTraceStatus.BLOCKED, summary="Trace packet blocked because patch plan metadata is missing.")
    source_ref = build_patch_proposal_trace_source_ref(source_kind=PatchProposalTraceSourceKind.V0353_PATCH_PLAN, source_id=patch_plan.patch_plan_id, source_summary="Supplied v0.35.3 patch plan metadata.")
    attributes = [
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.PATCH_PLAN_REF, key="patch_plan_id", value=patch_plan.patch_plan_id, policy=policy),
        build_patch_proposal_trace_attribute(attribute_kind=PatchProposalTraceAttributeKind.STATUS, key="status", value=str(patch_plan.status), policy=policy),
    ]
    return _packet_with("trace_packet:v0.35.7:plan", source_ref, PatchProposalTraceObjectType.PATCH_PLAN, patch_plan.patch_plan_id, patch_plan.plan_summary, PatchProposalTraceEventKind.PATCH_PLAN_CREATED, "Patch plan traced", "PatchPlan metadata traced without creating or applying patches.", attributes=attributes)


def build_external_agent_pattern_records_from_metadata(metadata: dict[str, Any] | None = None) -> list[ExternalAgentControlPatternRecord]:
    metadata = metadata or {}
    patterns = metadata.get("external_agent_patterns", [ExternalAgentControlPatternKind.CODEX_TO_CLAUDE_CODE_LOOP])
    records: list[ExternalAgentControlPatternRecord] = []
    for index, pattern in enumerate(patterns):
        pattern_kind = ExternalAgentControlPatternKind(pattern)
        records.append(
            build_external_agent_control_pattern_record(
                pattern_record_id=f"external_agent_pattern:v0.35.7:{index}",
                pattern_kind=pattern_kind,
                pattern_summary=f"{pattern_kind.value} traced as blocked/future-gated metadata only.",
            )
        )
    return records


def build_digestion_dominion_records_from_reference_digest(reference_digest: ReferencePatternDigest | None = None) -> list[DigestionDominionTraceRecord]:
    if reference_digest is None:
        return [
            build_digestion_dominion_trace_record(
                digestion_record_id="digestion_dominion:v0.35.7:missing_digest",
                disposition=DigestionDominionDisposition.INSUFFICIENT_EVIDENCE,
                source_pattern_record_ids=[],
                digestion_summary="ReferencePatternDigest metadata missing; trace remains blocked/future-gated.",
                chantacore_adaptation="Record gap instead of executing or importing references.",
                rejected_items=["reference execution", "reference import"],
                future_track_items=["supply digest metadata"],
            )
        ]
    records: list[DigestionDominionTraceRecord] = []
    for index, pattern in enumerate(reference_digest.patterns):
        disposition = DigestionDominionDisposition.SAFELY_DIGESTED
        rejected_items: list[str] = []
        future_items: list[str] = []
        if pattern.pattern_kind == ReferenceHarnessPatternKind.AGENT_LOOP_PATTERN:
            disposition = DigestionDominionDisposition.DOMINION_FUTURE_GATED
            rejected_items.append("external agent execution loop")
            future_items.append("future gated Dominion review")
        if pattern.disposition == ReferencePatternDisposition.REJECTED_FOR_SAFETY:
            disposition = DigestionDominionDisposition.REJECTED_FOR_SAFETY
            rejected_items.append(pattern.rejection_reason or "rejected reference pattern")
        if pattern.disposition == ReferencePatternDisposition.FUTURE_TRACK:
            disposition = DigestionDominionDisposition.DOMINION_FUTURE_GATED
            future_items.append(pattern.future_track_note or "future-track reference pattern")
        records.append(
            build_digestion_dominion_trace_record(
                digestion_record_id=f"digestion_dominion:v0.35.7:{index}",
                disposition=disposition,
                source_pattern_record_ids=[pattern.pattern_id],
                digestion_summary=pattern.pattern_summary,
                chantacore_adaptation=pattern.chantacore_adaptation or "Static pattern digested without execution.",
                rejected_items=rejected_items,
                future_track_items=future_items,
            )
        )
    if not records:
        records.append(build_digestion_dominion_trace_record())
    return records


def validate_patch_proposal_trace_packet(packet: PatchProposalTracePacket, policy: PatchProposalTracePolicy | None = None) -> PatchProposalTraceValidationReport:
    policy = policy or default_patch_proposal_trace_policy()
    blocked_items: list[str] = []
    if not patch_proposal_trace_packet_is_not_persistence(packet):
        blocked_items.append("persistent/external/execution readiness")
    if len(packet.events) > policy.max_event_count:
        blocked_items.append("too many trace events")
    if len(packet.objects) > policy.max_object_count:
        blocked_items.append("too many trace objects")
    if len(packet.relations) > policy.max_relation_count:
        blocked_items.append("too many trace relations")
    for attribute in packet.attributes:
        if _contains_prohibited_payload(attribute.value_preview, policy.prohibited_payload_patterns) and not attribute.redacted:
            blocked_items.append("unredacted secret-like attribute")
            break
    return build_patch_proposal_trace_validation_report(trace_packet_id=packet.trace_packet_id, blocked_items=blocked_items)


def decide_patch_proposal_trace_emission(emission_input: PatchProposalTraceEmissionInput, policy: PatchProposalTracePolicy | None = None) -> PatchProposalTraceEmissionDecision:
    policy = policy or default_patch_proposal_trace_policy()
    sink_kind = PatchProposalTraceSinkKind(emission_input.requested_sink_kind)
    if sink_kind == PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET and sink_kind in set(policy.allowed_sink_kinds):
        return build_patch_proposal_trace_emission_decision(emission_input_id=emission_input.emission_input_id, allowed_sink_kind=sink_kind)
    if sink_kind == PatchProposalTraceSinkKind.IN_MEMORY_TEST_SINK and sink_kind in set(policy.allowed_sink_kinds):
        return build_patch_proposal_trace_emission_decision(
            emission_input_id=emission_input.emission_input_id,
            decision_kind=PatchProposalTraceDecisionKind.ALLOW_IN_MEMORY_TEST_SINK,
            decision_summary="In-memory test sink is allowed only as non-persistent returned metadata.",
            allowed_sink_kind=sink_kind,
        )
    return build_patch_proposal_trace_emission_decision(
        emission_input_id=emission_input.emission_input_id,
        decision_kind=PatchProposalTraceDecisionKind.BLOCK,
        decision_summary="Requested trace sink is persistent, external, unknown, or blocked.",
        allowed_sink_kind=None,
        risk_kinds=[PatchProposalTraceRiskKind.PERSISTENT_TRACE_WRITE_RISK, PatchProposalTraceRiskKind.EXTERNAL_TRACE_SINK_RISK],
    )


def emit_patch_proposal_trace_packet(emission_input: PatchProposalTraceEmissionInput, emitter: PatchProposalTraceEmitter, supplied_packet: PatchProposalTracePacket | None = None) -> PatchProposalTracePacket:
    decision = decide_patch_proposal_trace_emission(emission_input, emitter.trace_policy)
    if PatchProposalTraceDecisionKind(decision.decision_kind) not in {
        PatchProposalTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION,
        PatchProposalTraceDecisionKind.ALLOW_IN_MEMORY_TEST_SINK,
    }:
        return build_patch_proposal_trace_packet(trace_packet_id=f"trace_packet:{emission_input.emission_input_id}:blocked", status=PatchProposalTraceStatus.BLOCKED, summary="Trace emission blocked; no persistence or external sink occurred.")
    packet = supplied_packet or build_patch_proposal_trace_packet(trace_packet_id=f"trace_packet:{emission_input.emission_input_id}")
    validation = validate_patch_proposal_trace_packet(packet, emitter.trace_policy)
    if not validation.valid:
        return build_patch_proposal_trace_packet(trace_packet_id=f"trace_packet:{emission_input.emission_input_id}:validation_blocked", status=PatchProposalTraceStatus.BLOCKED, summary="Trace packet failed validation and was returned as blocked metadata.")
    return packet


def patch_proposal_trace_flags_preserve_unsafe_false(flags: PatchProposalTraceFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PATCH_PROPOSAL_TRACE_FLAG_NAMES) and flags.production_certified is False


def patch_proposal_trace_policy_blocks_persistence(policy: PatchProposalTracePolicy) -> bool:
    return (
        policy.allow_raw_diff is False
        and policy.allow_raw_source is False
        and policy.allow_raw_review_packet is False
        and policy.allow_secret_content is False
        and policy.allow_credential_content is False
        and policy.allow_token_content is False
        and policy.allow_full_file_content is False
        and policy.allow_persistent_write is False
        and policy.allow_external_sink is False
        and policy.allow_external_agent_execution is False
        and policy.allow_dominion_runtime is False
        and policy.allow_infinite_agent_loop is False
    )


def patch_proposal_trace_packet_is_not_persistence(packet: PatchProposalTracePacket) -> bool:
    return (
        packet.ready_for_persistent_write is False
        and packet.ready_for_external_sink is False
        and packet.ready_for_execution is False
        and PatchProposalTraceSinkKind(packet.sink_kind)
        in {PatchProposalTraceSinkKind.RETURNED_TRACE_PACKET, PatchProposalTraceSinkKind.IN_MEMORY_TEST_SINK, PatchProposalTraceSinkKind.DISABLED}
    )


def digestion_dominion_record_is_not_runtime(record: DigestionDominionTraceRecord) -> bool:
    return record.execution_allowed is False and record.dominion_runtime_allowed is False and record.infinite_loop_allowed is False


def external_agent_pattern_record_is_not_execution(record: ExternalAgentControlPatternRecord) -> bool:
    return record.execution_allowed is False and record.dominion_runtime_allowed is False


def v0357_readiness_report_is_not_execution_ready(report: V0357ReadinessReport) -> bool:
    unsafe_names = tuple(name for name in UNSAFE_PATCH_PROPOSAL_TRACE_FLAG_NAMES if hasattr(report, name))
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
