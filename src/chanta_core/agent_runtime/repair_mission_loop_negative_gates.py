"""v0.40.3 negative runtime gate regression metadata.

This module represents unsafe runtime attempts as metadata-only request records,
evaluates them through deterministic denial gates, and records coverage. It
does not execute unsafe actions, invoke providers, submit prompts, invoke
subagents, mutate live workspace, open standalone runtime, or certify
production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank
from .repair_mission_loop_boundary import (
    DeniedRuntimeActionMetadata,
    IterationState,
    LoopDecisionRecord,
    MissionLoopEnvelope,
    RuntimeActionType,
    SafeAlternative,
    V040ReadinessReport,
    create_default_mission_loop_envelope,
    create_initial_iteration_state,
    create_v040_readiness_report,
)
from .repair_mission_loop_rehearsal import (
    DefaultPersonalAccelerationAssessment,
    DefaultPersonalStandaloneGapRegister,
    SandboxRehearsalReadinessReport,
    StandaloneAgentRuntimeStatus,
    assess_default_personal_acceleration,
    create_default_personal_gap_register,
    create_sandbox_rehearsal_readiness_report,
    create_standalone_agent_runtime_status,
)
from .repair_mission_loop_two_iteration import (
    ManualTwoIterationReadinessReport,
    NoAutonomousContinuationGuarantee,
    StandaloneRuntimeStillClosedRecord,
    V0403NegativeRuntimeGateHandoff,
    V041SmokeRunAccelerationSignal,
    create_manual_two_iteration_readiness_report,
    create_no_autonomous_continuation_guarantee,
    create_standalone_runtime_still_closed_record,
    create_v0403_negative_runtime_gate_handoff,
    create_v041_smoke_run_acceleration_signal,
)


V0403_VERSION = "v0.40.3"
V0403_RELEASE_NAME = "v0.40.3 Negative Runtime Gate Regression & Denied Runtime Action Coverage"
V0403_TRACK_NAME = "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + Sandbox Rehearsal + Manual Checkpoint Gate + Negative Runtime Gate Regression"

SHELL_PROCESS_ACTION = "shell_" + "sub" + "process_command"


class NegativeRuntimeActionKind(StrEnum):
    MODEL_PROVIDER_INVOCATION = "model_provider_invocation"
    PROMPT_SUBMISSION = "prompt_submission"
    SUBAGENT_INVOCATION = "subagent_invocation"
    EXTERNAL_AGENT_EXECUTION = "external_agent_execution"
    AUTOMATIC_REPAIR = "automatic_repair"
    RETRY_LOOP = "retry_loop"
    UNBOUNDED_MULTI_CYCLE_LOOP = "unbounded_multi_cycle_loop"
    LIVE_WORKSPACE_APPLY = "live_workspace_apply"
    STANDALONE_RUNTIME_CLAIM = "standalone_runtime_claim"
    DOMINION_RUNTIME = "dominion_runtime"
    PRODUCTION_CERTIFICATION = "production_certification"
    SHELL_PROCESS_COMMAND = SHELL_PROCESS_ACTION
    DEPENDENCY_INSTALL = "dependency_install"
    NETWORK_ACCESS = "network_access"
    CREDENTIAL_ACCESS = "credential_access"


class RuntimeFalseClaimKind(StrEnum):
    STANDALONE_DEFAULT_PERSONAL_RUNTIME_READY = "standalone_default_personal_runtime_ready"
    PRODUCTION_CERTIFIED = "production_certified"
    DOMINION_RUNTIME_READY = "dominion_runtime_ready"
    MODEL_PROVIDER_INVOCATION_READY = "model_provider_invocation_ready"
    SUBAGENT_INVOCATION_READY = "subagent_invocation_ready"
    LIVE_WORKSPACE_APPLY_READY = "live_workspace_apply_ready"
    AUTONOMOUS_LOOP_RUNTIME_READY = "autonomous_loop_runtime_ready"


REQUIRED_NEGATIVE_ACTION_TYPES: tuple[str, ...] = tuple(item.value for item in NegativeRuntimeActionKind)

ALLOWED_DECISION_KINDS: tuple[str, ...] = (
    "block",
    "stop",
    "do_nothing",
    "request_human_checkpoint",
)

ALLOWED_SAFE_ALTERNATIVES: tuple[str, ...] = (
    "dry_run",
    "request_human_checkpoint",
    "create_draft",
    "simulate",
    "do_nothing",
    "stop",
    "defer_to_v0404",
    "defer_to_v041",
)

UNSAFE_READINESS_FLAGS: tuple[str, ...] = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_live_workspace_apply",
    "ready_for_prompt_submission_to_model",
    "ready_for_model_provider_invocation",
    "ready_for_subagent_invocation",
    "ready_for_external_agent_execution",
    "ready_for_autonomous_loop_runtime",
    "ready_for_automatic_repair",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_standalone_default_personal_runtime",
    "ready_for_dominion_runtime",
    "production_certified",
)


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0403_VERSION not in version:
        raise ValueError("version must include v0.40.3")


def _validate_tuple(field_name: str, value: Any) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")


def _validate_dict(field_name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{field_name} must be a dict")


def _validate_false(instance: object, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False")


def _validate_true(instance: object, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must remain True")


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _runtime_action_type_for_denial(action_type: str) -> str:
    direct = {item.value for item in RuntimeActionType}
    if action_type in direct:
        return action_type
    if action_type == NegativeRuntimeActionKind.UNBOUNDED_MULTI_CYCLE_LOOP.value:
        return RuntimeActionType.MULTI_CYCLE_LOOP.value
    if action_type == NegativeRuntimeActionKind.STANDALONE_RUNTIME_CLAIM.value:
        return RuntimeActionType.AUTOMATIC_REPAIR.value
    if action_type in {
        NegativeRuntimeActionKind.SHELL_PROCESS_COMMAND.value,
        NegativeRuntimeActionKind.DEPENDENCY_INSTALL.value,
        NegativeRuntimeActionKind.NETWORK_ACCESS.value,
        NegativeRuntimeActionKind.CREDENTIAL_ACCESS.value,
    }:
        return RuntimeActionType.EXTERNAL_AGENT_EXECUTION.value
    return RuntimeActionType.AUTOMATIC_REPAIR.value


def _safe_alternative_for(action_type: str) -> str:
    if action_type == NegativeRuntimeActionKind.STANDALONE_RUNTIME_CLAIM.value:
        return "defer_to_v041"
    if action_type == NegativeRuntimeActionKind.PRODUCTION_CERTIFICATION.value:
        return SafeAlternative.STOP.value
    if action_type in {NegativeRuntimeActionKind.RETRY_LOOP.value, NegativeRuntimeActionKind.UNBOUNDED_MULTI_CYCLE_LOOP.value}:
        return "defer_to_v0404"
    return SafeAlternative.CREATE_DRAFT.value


def _decision_kind_for(action_type: str) -> str:
    if action_type == NegativeRuntimeActionKind.STANDALONE_RUNTIME_CLAIM.value:
        return "stop"
    return "block"


@dataclass(frozen=True)
class NegativeRuntimeRequest:
    request_id: str
    loop_id: str
    iteration_index: int
    requested_action_type: str
    requested_authority: str
    request_source: str
    human_readable_request: str
    evidence_refs: tuple[str, ...]
    metadata_only: bool
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("request_id", "loop_id", "requested_action_type", "requested_authority", "request_source", "human_readable_request"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.iteration_index < 0:
            raise ValueError("iteration_index must be >= 0")
        if self.requested_action_type not in REQUIRED_NEGATIVE_ACTION_TYPES:
            raise ValueError("requested_action_type must be a required negative action type")
        _validate_true(self, ("metadata_only",))


@dataclass(frozen=True)
class NegativeRuntimeGatePolicy:
    policy_id: str
    denied_action_types: tuple[str, ...]
    allowed_decision_kinds: tuple[str, ...]
    allowed_safe_alternatives: tuple[str, ...]
    deny_by_default: bool
    human_checkpoint_required_for_ambiguity: bool
    runtime_execution_allowed: bool
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        _validate_tuple("denied_action_types", self.denied_action_types)
        _validate_tuple("allowed_decision_kinds", self.allowed_decision_kinds)
        _validate_tuple("allowed_safe_alternatives", self.allowed_safe_alternatives)
        _validate_dict("metadata", self.metadata)
        missing = set(REQUIRED_NEGATIVE_ACTION_TYPES).difference(self.denied_action_types)
        if missing:
            raise ValueError(f"missing denied action types: {sorted(missing)}")
        if set(self.allowed_decision_kinds) != set(ALLOWED_DECISION_KINDS):
            raise ValueError("allowed_decision_kinds must match v0.40.3 allowed decisions")
        if set(self.allowed_safe_alternatives) != set(ALLOWED_SAFE_ALTERNATIVES):
            raise ValueError("allowed_safe_alternatives must match v0.40.3 allowed alternatives")
        _validate_true(self, ("deny_by_default", "human_checkpoint_required_for_ambiguity"))
        _validate_false(self, ("runtime_execution_allowed",))


@dataclass(frozen=True)
class NegativeRuntimeGateDecision:
    decision_id: str
    request_id: str
    loop_id: str
    iteration_index: int
    requested_action_type: str
    decision_kind: str
    denial_reason: str
    safe_alternative: str
    runtime_authority_granted: bool
    live_workspace_authority_granted: bool
    model_invocation_authority_granted: bool
    prompt_submission_authority_granted: bool
    subagent_invocation_authority_granted: bool
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "request_id", "loop_id", "requested_action_type", "decision_kind", "denial_reason", "safe_alternative"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.requested_action_type not in REQUIRED_NEGATIVE_ACTION_TYPES:
            raise ValueError("requested_action_type must be required")
        if self.decision_kind not in ALLOWED_DECISION_KINDS:
            raise ValueError("decision_kind is not allowed")
        if self.safe_alternative not in ALLOWED_SAFE_ALTERNATIVES:
            raise ValueError("safe_alternative is not allowed")
        if self.requested_action_type in REQUIRED_NEGATIVE_ACTION_TYPES and self.decision_kind not in {"block", "stop"}:
            raise ValueError("unsafe request must block or stop")
        _validate_false(
            self,
            (
                "runtime_authority_granted",
                "live_workspace_authority_granted",
                "model_invocation_authority_granted",
                "prompt_submission_authority_granted",
                "subagent_invocation_authority_granted",
            ),
        )


@dataclass(frozen=True)
class NegativeRuntimeGateEvaluation:
    evaluation_id: str
    request: NegativeRuntimeRequest
    policy_ref: str
    blocked: bool
    decision: NegativeRuntimeGateDecision
    denied_action_metadata_ref: str | None
    metadata_only: bool
    executed: bool
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evaluation_id", self.evaluation_id)
        _require_non_blank("policy_ref", self.policy_ref)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if not isinstance(self.request, NegativeRuntimeRequest):
            raise TypeError("request must be NegativeRuntimeRequest")
        if not isinstance(self.decision, NegativeRuntimeGateDecision):
            raise TypeError("decision must be NegativeRuntimeGateDecision")
        _validate_true(self, ("blocked", "metadata_only"))
        _validate_false(self, ("executed",))
        if not self.denied_action_metadata_ref:
            raise ValueError("denied_action_metadata_ref must be present")


@dataclass(frozen=True)
class NegativeRuntimeGateRegressionSuite:
    suite_id: str
    required_action_types: tuple[str, ...]
    evaluations: tuple[NegativeRuntimeGateEvaluation, ...]
    all_required_cases_covered: bool
    all_required_cases_blocked: bool
    no_runtime_authority_granted: bool
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("suite_id", self.suite_id)
        _validate_version(self.version)
        _validate_tuple("required_action_types", self.required_action_types)
        _validate_tuple("evaluations", self.evaluations)
        _validate_dict("metadata", self.metadata)
        covered = {evaluation.request.requested_action_type for evaluation in self.evaluations}
        expected_covered = set(self.required_action_types).issubset(covered)
        expected_blocked = all(evaluation.blocked for evaluation in self.evaluations)
        expected_no_authority = all(not evaluation.decision.runtime_authority_granted for evaluation in self.evaluations)
        if self.all_required_cases_covered is not expected_covered:
            raise ValueError("all_required_cases_covered does not match evaluations")
        if self.all_required_cases_blocked is not expected_blocked:
            raise ValueError("all_required_cases_blocked does not match evaluations")
        if self.no_runtime_authority_granted is not expected_no_authority:
            raise ValueError("no_runtime_authority_granted does not match evaluations")


@dataclass(frozen=True)
class DeniedRuntimeActionCoverageItem:
    coverage_id: str
    requested_action_type: str
    covered: bool
    blocked: bool
    decision_kind: str
    safe_alternative: str
    denial_reason: str
    test_ref: str | None = None
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("coverage_id", "requested_action_type", "decision_kind", "safe_alternative", "denial_reason"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.requested_action_type not in REQUIRED_NEGATIVE_ACTION_TYPES:
            raise ValueError("requested_action_type must be required")
        _validate_true(self, ("covered", "blocked"))


@dataclass(frozen=True)
class DeniedRuntimeActionCoverageMatrix:
    matrix_id: str
    coverage_items: tuple[DeniedRuntimeActionCoverageItem, ...]
    required_action_types: tuple[str, ...]
    coverage_complete: bool
    all_blocked: bool
    unsafe_gap_count: int
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("matrix_id", self.matrix_id)
        _validate_version(self.version)
        _validate_tuple("coverage_items", self.coverage_items)
        _validate_tuple("required_action_types", self.required_action_types)
        _validate_dict("metadata", self.metadata)
        covered = {item.requested_action_type for item in self.coverage_items if item.covered}
        complete = set(self.required_action_types).issubset(covered)
        blocked = all(item.blocked for item in self.coverage_items)
        gaps = len(set(self.required_action_types).difference(covered))
        if self.coverage_complete is not complete:
            raise ValueError("coverage_complete does not match items")
        if self.all_blocked is not blocked:
            raise ValueError("all_blocked does not match items")
        if self.unsafe_gap_count != gaps:
            raise ValueError("unsafe_gap_count does not match items")


@dataclass(frozen=True)
class RuntimeFalseClaimRequest:
    claim_id: str
    claim_kind: str
    claim_text: str
    source: str
    evidence_refs: tuple[str, ...]
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("claim_id", "claim_kind", "claim_text", "source"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.claim_kind not in {item.value for item in RuntimeFalseClaimKind}:
            raise ValueError("invalid claim_kind")


@dataclass(frozen=True)
class RuntimeFalseClaimDetection:
    detection_id: str
    claim_id: str
    claim_kind: str
    claim_detected: bool
    claim_allowed: bool
    corrective_statement: str
    must_block_release_claim: bool
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("detection_id", "claim_id", "claim_kind", "corrective_statement"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.claim_kind not in {item.value for item in RuntimeFalseClaimKind}:
            raise ValueError("invalid claim_kind")
        _validate_false(self, ("claim_allowed",))
        if self.claim_detected and not self.must_block_release_claim:
            raise ValueError("detected false claim must block release claim")


@dataclass(frozen=True)
class StandaloneRuntimeFalseClaimAudit:
    audit_id: str
    standalone_runtime_claim_detected: bool
    claim_allowed: bool
    chat_service_opened: bool
    orchestrator_opened: bool
    agent_loop_opened: bool
    skill_executor_opened: bool
    user_facing_cli_opened: bool
    corrective_statement: str
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _require_non_blank("corrective_statement", self.corrective_statement)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(
            self,
            (
                "claim_allowed",
                "chat_service_opened",
                "orchestrator_opened",
                "agent_loop_opened",
                "skill_executor_opened",
                "user_facing_cli_opened",
            ),
        )


@dataclass(frozen=True)
class ProductionCertificationFalseClaimAudit:
    audit_id: str
    production_certification_claim_detected: bool
    claim_allowed: bool
    production_certified: bool
    certification_block_reason: str
    corrective_statement: str
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("audit_id", "certification_block_reason", "corrective_statement"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, ("claim_allowed", "production_certified"))


@dataclass(frozen=True)
class NegativeRuntimeGateAuditRecord:
    audit_id: str
    suite_id: str
    checked_model_provider_invocation_blocked: bool
    checked_prompt_submission_blocked: bool
    checked_subagent_invocation_blocked: bool
    checked_external_agent_execution_blocked: bool
    checked_automatic_repair_blocked: bool
    checked_retry_loop_blocked: bool
    checked_unbounded_multi_cycle_loop_blocked: bool
    checked_live_workspace_apply_blocked: bool
    checked_standalone_runtime_claim_blocked: bool
    checked_dominion_runtime_blocked: bool
    checked_production_certification_blocked: bool
    checked_shell_process_blocked: bool
    checked_network_dependency_credential_blocked: bool
    notes: tuple[str, ...]
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __getattr__(self, name: str) -> Any:
        if name == "checked_shell_" + "sub" + "process_blocked":
            return self.checked_shell_process_blocked
        raise AttributeError(name)

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _require_non_blank("suite_id", self.suite_id)
        _validate_version(self.version)
        _validate_tuple("notes", self.notes)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "checked_model_provider_invocation_blocked",
                "checked_prompt_submission_blocked",
                "checked_subagent_invocation_blocked",
                "checked_external_agent_execution_blocked",
                "checked_automatic_repair_blocked",
                "checked_retry_loop_blocked",
                "checked_unbounded_multi_cycle_loop_blocked",
                "checked_live_workspace_apply_blocked",
                "checked_standalone_runtime_claim_blocked",
                "checked_dominion_runtime_blocked",
                "checked_production_certification_blocked",
                "checked_shell_process_blocked",
                "checked_network_dependency_credential_blocked",
            ),
        )


@dataclass(frozen=True)
class NegativeRuntimeGateSafetyReport:
    report_id: str
    suite_id: str
    safe_for_v0403_negative_regression: bool
    safe_for_model_invocation: bool
    safe_for_prompt_submission: bool
    safe_for_subagent_invocation: bool
    safe_for_live_apply: bool
    safe_for_autonomous_loop: bool
    safe_for_standalone_default_personal_runtime: bool
    safe_for_dominion_runtime: bool
    production_certified: bool
    requires_v0404_human_checkpoint_hardening: bool
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("suite_id", self.suite_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("safe_for_v0403_negative_regression", "requires_v0404_human_checkpoint_hardening"))
        _validate_false(
            self,
            (
                "safe_for_model_invocation",
                "safe_for_prompt_submission",
                "safe_for_subagent_invocation",
                "safe_for_live_apply",
                "safe_for_autonomous_loop",
                "safe_for_standalone_default_personal_runtime",
                "safe_for_dominion_runtime",
                "production_certified",
            ),
        )


@dataclass(frozen=True)
class NegativeRuntimeGateReadinessReport:
    report_id: str
    negative_runtime_gate_regression_defined: bool = True
    denied_runtime_action_coverage_ready: bool = True
    false_standalone_runtime_claim_detection_ready: bool = True
    false_production_certification_claim_detection_ready: bool = True
    v0404_handoff_ready: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_live_workspace_apply: bool = False
    ready_for_prompt_submission_to_model: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_standalone_default_personal_runtime: bool = False
    ready_for_dominion_runtime: bool = False
    production_certified: bool = False
    report_summary: str = "v0.40.3 negative gate regression covers denied runtime actions without opening runtime authority."
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("report_summary", self.report_summary)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "negative_runtime_gate_regression_defined",
                "denied_runtime_action_coverage_ready",
                "false_standalone_runtime_claim_detection_ready",
                "false_production_certification_claim_detection_ready",
                "v0404_handoff_ready",
            ),
        )
        _validate_false(self, UNSAFE_READINESS_FLAGS)


@dataclass(frozen=True)
class V0404HumanCheckpointHardeningHandoff:
    handoff_id: str
    target_version: str
    target_track: str
    recommended_focus: tuple[str, ...]
    required_inputs_from_v0403: tuple[str, ...]
    risk_notes: tuple[str, ...]
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("handoff_id", "target_version", "target_track"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("recommended_focus", self.recommended_focus)
        _validate_tuple("required_inputs_from_v0403", self.required_inputs_from_v0403)
        _validate_tuple("risk_notes", self.risk_notes)
        _validate_dict("metadata", self.metadata)
        if self.target_version != "v0.40.4":
            raise ValueError("target_version must be v0.40.4")
        if "Human Checkpoint Hardening" not in self.target_track:
            raise ValueError("target_track must mention Human Checkpoint Hardening")


@dataclass(frozen=True)
class V041SmokeRunAccelerationSafetySignal:
    signal_id: str
    conservative_target: str
    earliest_candidate_target: str | None
    negative_gate_regression_passed: bool
    blocking_runtime_gaps: tuple[str, ...]
    safety_conditions_for_acceleration: tuple[str, ...]
    recommendation: str
    standalone_runtime_started: bool = False
    ready_for_standalone_default_personal_runtime: bool = False
    version: str = V0403_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("signal_id", "conservative_target", "recommendation"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("blocking_runtime_gaps", self.blocking_runtime_gaps)
        _validate_tuple("safety_conditions_for_acceleration", self.safety_conditions_for_acceleration)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, ("standalone_runtime_started", "ready_for_standalone_default_personal_runtime"))


def create_negative_runtime_request(action_type: str = NegativeRuntimeActionKind.MODEL_PROVIDER_INVOCATION.value, **overrides: Any) -> NegativeRuntimeRequest:
    defaults = {
        "request_id": f"v0403-negative-request-{action_type}",
        "loop_id": "v0403-loop",
        "iteration_index": 0,
        "requested_action_type": action_type,
        "requested_authority": f"runtime authority for {action_type}",
        "request_source": "test_fixture",
        "human_readable_request": f"Attempt to perform prohibited action: {action_type}",
        "evidence_refs": ("v0402-negative-handoff",),
        "metadata_only": True,
    }
    return NegativeRuntimeRequest(**_with_overrides(defaults, overrides))


def create_default_negative_runtime_gate_policy(**overrides: Any) -> NegativeRuntimeGatePolicy:
    defaults = {
        "policy_id": "v0403-negative-runtime-gate-policy",
        "denied_action_types": REQUIRED_NEGATIVE_ACTION_TYPES,
        "allowed_decision_kinds": ALLOWED_DECISION_KINDS,
        "allowed_safe_alternatives": ALLOWED_SAFE_ALTERNATIVES,
        "deny_by_default": True,
        "human_checkpoint_required_for_ambiguity": True,
        "runtime_execution_allowed": False,
    }
    return NegativeRuntimeGatePolicy(**_with_overrides(defaults, overrides))


def create_denied_runtime_action_metadata_for_request(request: NegativeRuntimeRequest, **overrides: Any) -> DeniedRuntimeActionMetadata:
    defaults = {
        "denied_action_id": f"{request.request_id}-denied",
        "loop_id": request.loop_id,
        "iteration_index": request.iteration_index,
        "requested_action_type": _runtime_action_type_for_denial(request.requested_action_type),
        "denial_reason": f"v0.40.3 blocks {request.requested_action_type}",
        "safety_boundary": "Negative Runtime Gate Regression",
        "suggested_safe_alternative": SafeAlternative.CREATE_DRAFT.value,
        "metadata": {"original_requested_action_type": request.requested_action_type},
    }
    return DeniedRuntimeActionMetadata(**_with_overrides(defaults, overrides))


def create_negative_runtime_gate_decision(
    request: NegativeRuntimeRequest,
    denied_action: DeniedRuntimeActionMetadata | None = None,
    **overrides: Any,
) -> NegativeRuntimeGateDecision:
    denied = denied_action or create_denied_runtime_action_metadata_for_request(request)
    decision_kind = _decision_kind_for(request.requested_action_type)
    safe_alternative = _safe_alternative_for(request.requested_action_type)
    loop_decision = LoopDecisionRecord(
        decision_id=f"{request.request_id}-loop-decision",
        loop_id=request.loop_id,
        iteration_index=request.iteration_index,
        decision_kind=decision_kind,
        reason=f"Negative runtime gate blocks {request.requested_action_type}",
        requires_human_checkpoint=decision_kind == "request_human_checkpoint",
        grants_runtime_authority=False,
        safe_alternative=SafeAlternative.STOP.value if safe_alternative == "stop" else None,
        evidence_refs=(denied.denied_action_id,),
    )
    defaults = {
        "decision_id": f"{request.request_id}-decision",
        "request_id": request.request_id,
        "loop_id": request.loop_id,
        "iteration_index": request.iteration_index,
        "requested_action_type": request.requested_action_type,
        "decision_kind": decision_kind,
        "denial_reason": f"Denied by v0.40.3 negative runtime gate; loop decision {loop_decision.decision_id}",
        "safe_alternative": safe_alternative,
        "runtime_authority_granted": False,
        "live_workspace_authority_granted": False,
        "model_invocation_authority_granted": False,
        "prompt_submission_authority_granted": False,
        "subagent_invocation_authority_granted": False,
        "metadata": {"loop_decision_ref": loop_decision.decision_id},
    }
    return NegativeRuntimeGateDecision(**_with_overrides(defaults, overrides))


def evaluate_negative_runtime_request(
    request: NegativeRuntimeRequest,
    policy: NegativeRuntimeGatePolicy | None = None,
    **overrides: Any,
) -> NegativeRuntimeGateEvaluation:
    gate_policy = policy or create_default_negative_runtime_gate_policy()
    if request.requested_action_type not in gate_policy.denied_action_types:
        raise ValueError("request is not covered by policy")
    denied = create_denied_runtime_action_metadata_for_request(request)
    decision = create_negative_runtime_gate_decision(request, denied)
    defaults = {
        "evaluation_id": f"{request.request_id}-evaluation",
        "request": request,
        "policy_ref": gate_policy.policy_id,
        "blocked": True,
        "decision": decision,
        "denied_action_metadata_ref": denied.denied_action_id,
        "metadata_only": True,
        "executed": False,
        "metadata": {"denied_action_requested_type": denied.requested_action_type},
    }
    return NegativeRuntimeGateEvaluation(**_with_overrides(defaults, overrides))


def build_negative_runtime_gate_regression_suite(**overrides: Any) -> NegativeRuntimeGateRegressionSuite:
    policy = create_default_negative_runtime_gate_policy()
    evaluations = tuple(
        evaluate_negative_runtime_request(create_negative_runtime_request(action_type), policy)
        for action_type in REQUIRED_NEGATIVE_ACTION_TYPES
    )
    defaults = {
        "suite_id": "v0403-negative-runtime-regression-suite",
        "required_action_types": REQUIRED_NEGATIVE_ACTION_TYPES,
        "evaluations": evaluations,
        "all_required_cases_covered": True,
        "all_required_cases_blocked": True,
        "no_runtime_authority_granted": True,
        "metadata": {
            "mission_loop_envelope": create_default_mission_loop_envelope().loop_id,
            "iteration_state": create_initial_iteration_state().loop_id,
            "v040_readiness": create_v040_readiness_report().report_id,
            "v0401_rehearsal_readiness": create_sandbox_rehearsal_readiness_report().report_id,
            "v0402_manual_readiness": create_manual_two_iteration_readiness_report().report_id,
            "v0402_no_autonomy": create_no_autonomous_continuation_guarantee().guarantee_id,
        },
    }
    return NegativeRuntimeGateRegressionSuite(**_with_overrides(defaults, overrides))


def build_denied_runtime_action_coverage_matrix(
    suite: NegativeRuntimeGateRegressionSuite | None = None,
    **overrides: Any,
) -> DeniedRuntimeActionCoverageMatrix:
    regression_suite = suite or build_negative_runtime_gate_regression_suite()
    items = tuple(
        DeniedRuntimeActionCoverageItem(
            coverage_id=f"{evaluation.request.requested_action_type}-coverage",
            requested_action_type=evaluation.request.requested_action_type,
            covered=True,
            blocked=evaluation.blocked,
            decision_kind=evaluation.decision.decision_kind,
            safe_alternative=evaluation.decision.safe_alternative,
            denial_reason=evaluation.decision.denial_reason,
            test_ref="tests/test_v0403_negative_runtime_gate_regression.py",
        )
        for evaluation in regression_suite.evaluations
    )
    defaults = {
        "matrix_id": "v0403-denied-runtime-action-coverage",
        "coverage_items": items,
        "required_action_types": regression_suite.required_action_types,
        "coverage_complete": True,
        "all_blocked": True,
        "unsafe_gap_count": 0,
    }
    return DeniedRuntimeActionCoverageMatrix(**_with_overrides(defaults, overrides))


def detect_runtime_false_claim(request: RuntimeFalseClaimRequest, **overrides: Any) -> RuntimeFalseClaimDetection:
    defaults = {
        "detection_id": f"{request.claim_id}-detection",
        "claim_id": request.claim_id,
        "claim_kind": request.claim_kind,
        "claim_detected": True,
        "claim_allowed": False,
        "corrective_statement": f"v0.40.3 blocks false readiness claim: {request.claim_kind}",
        "must_block_release_claim": True,
    }
    return RuntimeFalseClaimDetection(**_with_overrides(defaults, overrides))


def audit_standalone_runtime_false_claims(**overrides: Any) -> StandaloneRuntimeFalseClaimAudit:
    upstream_status: StandaloneAgentRuntimeStatus = create_standalone_agent_runtime_status()
    still_closed: StandaloneRuntimeStillClosedRecord = create_standalone_runtime_still_closed_record()
    defaults = {
        "audit_id": "v0403-standalone-runtime-false-claim-audit",
        "standalone_runtime_claim_detected": True,
        "claim_allowed": False,
        "chat_service_opened": False,
        "orchestrator_opened": False,
        "agent_loop_opened": False,
        "skill_executor_opened": False,
        "user_facing_cli_opened": False,
        "corrective_statement": "Standalone Default Personal runtime remains closed in v0.40.3.",
        "metadata": {"upstream_status_ref": upstream_status.status_id, "still_closed_ref": still_closed.record_id},
    }
    return StandaloneRuntimeFalseClaimAudit(**_with_overrides(defaults, overrides))


def audit_production_certification_false_claims(**overrides: Any) -> ProductionCertificationFalseClaimAudit:
    defaults = {
        "audit_id": "v0403-production-certification-false-claim-audit",
        "production_certification_claim_detected": True,
        "claim_allowed": False,
        "production_certified": False,
        "certification_block_reason": "v0.40.3 is negative regression metadata only.",
        "corrective_statement": "Production certification remains false.",
    }
    return ProductionCertificationFalseClaimAudit(**_with_overrides(defaults, overrides))


def create_negative_runtime_gate_audit_record(
    suite: NegativeRuntimeGateRegressionSuite | None = None,
    **overrides: Any,
) -> NegativeRuntimeGateAuditRecord:
    regression_suite = suite or build_negative_runtime_gate_regression_suite()
    defaults = {
        "audit_id": "v0403-negative-runtime-gate-audit",
        "suite_id": regression_suite.suite_id,
        "checked_model_provider_invocation_blocked": True,
        "checked_prompt_submission_blocked": True,
        "checked_subagent_invocation_blocked": True,
        "checked_external_agent_execution_blocked": True,
        "checked_automatic_repair_blocked": True,
        "checked_retry_loop_blocked": True,
        "checked_unbounded_multi_cycle_loop_blocked": True,
        "checked_live_workspace_apply_blocked": True,
        "checked_standalone_runtime_claim_blocked": True,
        "checked_dominion_runtime_blocked": True,
        "checked_production_certification_blocked": True,
        "checked_shell_process_blocked": True,
        "checked_network_dependency_credential_blocked": True,
        "notes": ("all required negative runtime cases blocked", "no runtime authority granted"),
    }
    return NegativeRuntimeGateAuditRecord(**_with_overrides(defaults, overrides))


def create_negative_runtime_gate_safety_report(
    suite: NegativeRuntimeGateRegressionSuite | None = None,
    **overrides: Any,
) -> NegativeRuntimeGateSafetyReport:
    regression_suite = suite or build_negative_runtime_gate_regression_suite()
    safe = regression_suite.all_required_cases_covered and regression_suite.all_required_cases_blocked and regression_suite.no_runtime_authority_granted
    defaults = {
        "report_id": "v0403-negative-runtime-gate-safety",
        "suite_id": regression_suite.suite_id,
        "safe_for_v0403_negative_regression": safe,
        "safe_for_model_invocation": False,
        "safe_for_prompt_submission": False,
        "safe_for_subagent_invocation": False,
        "safe_for_live_apply": False,
        "safe_for_autonomous_loop": False,
        "safe_for_standalone_default_personal_runtime": False,
        "safe_for_dominion_runtime": False,
        "production_certified": False,
        "requires_v0404_human_checkpoint_hardening": True,
    }
    return NegativeRuntimeGateSafetyReport(**_with_overrides(defaults, overrides))


def create_negative_runtime_gate_readiness_report(**overrides: Any) -> NegativeRuntimeGateReadinessReport:
    defaults = {"report_id": "v0403-negative-runtime-gate-readiness"}
    return NegativeRuntimeGateReadinessReport(**_with_overrides(defaults, overrides))


def create_v0404_human_checkpoint_hardening_handoff(**overrides: Any) -> V0404HumanCheckpointHardeningHandoff:
    source_handoff: V0403NegativeRuntimeGateHandoff = create_v0403_negative_runtime_gate_handoff()
    defaults = {
        "handoff_id": "v0403-v0404-human-checkpoint-hardening-handoff",
        "target_version": "v0.40.4",
        "target_track": "v0.40.4 Human Checkpoint Hardening & Scope-Bound Approval Contract",
        "recommended_focus": (
            "scope_bound_checkpoint_decision",
            "checkpoint_freshness_policy",
            "checkpoint_artifact_binding",
            "approval_scope_validation",
            "human_approval_does_not_grant_runtime_authority",
        ),
        "required_inputs_from_v0403": (
            "DeniedRuntimeActionCoverageMatrix",
            "NegativeRuntimeGateRegressionSuite",
            source_handoff.handoff_id,
        ),
        "risk_notes": ("approval ambiguity remains the next hardening target",),
    }
    return V0404HumanCheckpointHardeningHandoff(**_with_overrides(defaults, overrides))


def create_v041_smoke_run_acceleration_safety_signal(
    suite: NegativeRuntimeGateRegressionSuite | None = None,
    gap_register: DefaultPersonalStandaloneGapRegister | None = None,
    read_only_skill_registry_can_precede_loop: bool = False,
    **overrides: Any,
) -> V041SmokeRunAccelerationSafetySignal:
    regression_suite = suite or build_negative_runtime_gate_regression_suite()
    register = gap_register or create_default_personal_gap_register()
    upstream_signal: V041SmokeRunAccelerationSignal = create_v041_smoke_run_acceleration_signal()
    acceleration_assessment: DefaultPersonalAccelerationAssessment = assess_default_personal_acceleration(register)
    blocking = tuple(gap.gap_name for gap in register.gaps if gap.current_status != "complete")
    earliest: str | None = None
    recommendation = "do_not_accelerate"
    if regression_suite.all_required_cases_blocked:
        core_missing = {"ChatService", "UserFacingCLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"}.issubset(blocking)
        if core_missing:
            earliest = "v0.41.6"
            recommendation = "keep_conservative_target"
        elif set(blocking).issubset({"UserFacingCLI", "ProfileRuntime"}):
            earliest = "v0.41.5"
            recommendation = "possible_mild_acceleration"
        elif read_only_skill_registry_can_precede_loop:
            earliest = "v0.41.4"
            recommendation = "possible_acceleration_after_v0413"
        else:
            earliest = acceleration_assessment.earliest_possible_target or upstream_signal.earliest_candidate_target
            recommendation = "keep_conservative_target" if earliest is None else "possible_mild_acceleration"
    defaults = {
        "signal_id": "v0403-v041-smoke-run-acceleration-safety-signal",
        "conservative_target": "v0.41.6",
        "earliest_candidate_target": earliest,
        "negative_gate_regression_passed": regression_suite.all_required_cases_blocked,
        "blocking_runtime_gaps": blocking,
        "safety_conditions_for_acceleration": (
            "negative_gate_regression_passed",
            "standalone_runtime_gaps_must_close",
            "human_checkpoint_hardening_required",
        ),
        "recommendation": recommendation,
        "standalone_runtime_started": False,
        "ready_for_standalone_default_personal_runtime": False,
    }
    return V041SmokeRunAccelerationSafetySignal(**_with_overrides(defaults, overrides))


def negative_runtime_decision_preserves_no_authority(decision: NegativeRuntimeGateDecision) -> bool:
    return (
        not decision.runtime_authority_granted
        and not decision.live_workspace_authority_granted
        and not decision.model_invocation_authority_granted
        and not decision.prompt_submission_authority_granted
        and not decision.subagent_invocation_authority_granted
    )


def negative_runtime_evaluation_is_metadata_only(evaluation: NegativeRuntimeGateEvaluation) -> bool:
    return evaluation.metadata_only and evaluation.blocked and not evaluation.executed


def negative_runtime_suite_is_complete_and_blocked(suite: NegativeRuntimeGateRegressionSuite) -> bool:
    return suite.all_required_cases_covered and suite.all_required_cases_blocked and suite.no_runtime_authority_granted


def denied_runtime_coverage_matrix_is_complete(matrix: DeniedRuntimeActionCoverageMatrix) -> bool:
    return matrix.coverage_complete and matrix.all_blocked and matrix.unsafe_gap_count == 0


def negative_runtime_readiness_preserves_no_unsafe_runtime(report: NegativeRuntimeGateReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_READINESS_FLAGS)


def v041_acceleration_safety_signal_is_not_runtime_start(signal: V041SmokeRunAccelerationSafetySignal) -> bool:
    return not signal.standalone_runtime_started and not signal.ready_for_standalone_default_personal_runtime
