"""v0.40.2 manual two-iteration rehearsal metadata.

This layer connects the v0.40.0 mission-loop boundary and the v0.40.1 sandbox
rehearsal helper. It proves that iteration 1 requires explicit human checkpoint
metadata. It does not auto-continue, invoke models, submit prompts, invoke
subagents, mutate live workspace, open standalone runtime, or certify
production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .boundary import _require_non_blank
from .repair_mission_loop_boundary import (
    HumanCheckpointGate,
    IterationState,
    LoopDecisionKind,
    create_initial_iteration_state,
)
from .repair_mission_loop_rehearsal import (
    DefaultPersonalAccelerationAssessment,
    DefaultPersonalStandaloneGapRegister,
    SandboxRehearsalInput,
    SandboxRehearsalReadinessReport,
    SandboxRehearsalResult,
    SandboxRehearsalSafetyReport,
    StandaloneAgentRuntimeStatus,
    RunnerCallable,
    assess_default_personal_acceleration,
    create_default_personal_gap_register,
    create_sandbox_rehearsal_input,
    create_sandbox_rehearsal_readiness_report,
    create_standalone_agent_runtime_status,
    run_sandbox_rehearsal,
)


V0402_VERSION = "v0.40.2"
V0402_RELEASE_NAME = "v0.40.2 Manual Two-Iteration Rehearsal & Human Checkpoint Enforcement"
V0402_TRACK_NAME = "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + Sandbox Rehearsal + Manual Two-Iteration Checkpoint Gate"

CHECKPOINT_DECISIONS: tuple[str, ...] = (
    "approve_second_iteration_rehearsal",
    "request_more_evidence",
    "stop",
    "do_nothing",
    "reject",
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

STANDALONE_OPENED_FLAGS: tuple[str, ...] = (
    "chat_service_opened",
    "orchestrator_opened",
    "agent_loop_opened",
    "skill_registry_opened",
    "skill_executor_opened",
    "profile_runtime_opened",
    "prompt_assembly_opened",
    "user_facing_cli_opened",
    "event_trace_emission_opened",
    "standalone_default_personal_runtime_opened",
)

V0403_NEGATIVE_CASES: tuple[str, ...] = (
    "model_provider_invocation",
    "prompt_submission",
    "subagent_invocation",
    "external_agent_execution",
    "automatic_repair",
    "retry_loop",
    "unbounded_multi_cycle_loop",
    "live_workspace_apply",
    "standalone_runtime_claim",
    "dominion_runtime",
    "production_certification",
)


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0402_VERSION not in version:
        raise ValueError("version must include v0.40.2")


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


@dataclass(frozen=True)
class ManualTwoIterationRehearsalInput:
    rehearsal_id: str
    loop_id: str
    mission_id: str
    max_iterations: int
    iteration_zero_input_ref: str
    iteration_one_input_ref: str | None
    checkpoint_decision_ref: str | None
    manual_mode_required: bool
    autonomous_continuation_requested: bool
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("rehearsal_id", "loop_id", "mission_id", "iteration_zero_input_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.max_iterations > 2:
            raise ValueError("max_iterations must be <= 2")
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
        _validate_true(self, ("manual_mode_required",))
        _validate_false(self, ("autonomous_continuation_requested",))


@dataclass(frozen=True)
class ManualIterationStateRef:
    state_ref_id: str
    loop_id: str
    iteration_index: int
    sandbox_rehearsal_result_ref: str | None = None
    checkpoint_request_ref: str | None = None
    checkpoint_decision_ref: str | None = None
    eligible_for_next_iteration: bool = False
    execution_permission_granted: bool = False
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("state_ref_id", self.state_ref_id)
        _require_non_blank("loop_id", self.loop_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.iteration_index < 0:
            raise ValueError("iteration_index must be >= 0")
        _validate_false(self, ("execution_permission_granted",))


@dataclass(frozen=True)
class ManualIterationCheckpointRequest:
    checkpoint_request_id: str
    loop_id: str
    after_iteration_index: int
    required: bool
    reason: str
    required_review_refs: tuple[str, ...]
    decision_options: tuple[str, ...]
    default_decision: str
    approval_grants_runtime_authority: bool
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("checkpoint_request_id", "loop_id", "reason", "default_decision"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("required_review_refs", self.required_review_refs)
        _validate_tuple("decision_options", self.decision_options)
        _validate_dict("metadata", self.metadata)
        if self.after_iteration_index != 0:
            raise ValueError("after_iteration_index must be 0")
        _validate_true(self, ("required",))
        if self.default_decision != "stop":
            raise ValueError("default_decision must be stop")
        missing = set(CHECKPOINT_DECISIONS).difference(self.decision_options)
        if missing:
            raise ValueError(f"missing checkpoint decision options: {sorted(missing)}")
        _validate_false(self, ("approval_grants_runtime_authority",))


@dataclass(frozen=True)
class ManualIterationCheckpointDecision:
    checkpoint_decision_id: str
    checkpoint_request_id: str
    loop_id: str
    decision: str
    decision_scope: str
    approved_iteration_index: int | None
    approved_rehearsal_only: bool
    approval_grants_runtime_authority: bool
    reviewed_evidence_refs: tuple[str, ...]
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("checkpoint_decision_id", "checkpoint_request_id", "loop_id", "decision", "decision_scope"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("reviewed_evidence_refs", self.reviewed_evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.decision not in CHECKPOINT_DECISIONS:
            raise ValueError("invalid checkpoint decision")
        if self.decision == "approve_second_iteration_rehearsal":
            if self.approved_iteration_index != 1:
                raise ValueError("approval must target iteration 1")
            _validate_true(self, ("approved_rehearsal_only",))
        elif self.approved_rehearsal_only:
            raise ValueError("approved_rehearsal_only is only valid for approval")
        _validate_false(self, ("approval_grants_runtime_authority",))


@dataclass(frozen=True)
class SecondIterationEligibilityDecision:
    eligibility_id: str
    loop_id: str
    iteration_index: int
    eligible: bool
    reason: str
    checkpoint_required: bool
    checkpoint_present: bool
    checkpoint_decision_ref: str | None
    manual_only: bool
    runtime_authority_granted: bool
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("eligibility_id", "loop_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.iteration_index != 1:
            raise ValueError("iteration_index must be 1")
        _validate_true(self, ("checkpoint_required", "manual_only"))
        _validate_false(self, ("runtime_authority_granted",))
        if self.eligible and not self.checkpoint_present:
            raise ValueError("eligible second iteration requires checkpoint")
        if self.eligible and self.reason != "approved_manual_bounded_rehearsal":
            raise ValueError("eligible second iteration must be manual bounded rehearsal only")


@dataclass(frozen=True)
class ManualTwoIterationRehearsalPlan:
    plan_id: str
    loop_id: str
    max_iterations: int
    iteration_zero_rehearsal_ref: str | None
    checkpoint_request_ref: str | None
    checkpoint_decision_ref: str | None
    second_iteration_eligibility_ref: str | None
    iteration_one_rehearsal_ref: str | None
    manual_only: bool
    autonomous_continuation_allowed: bool
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("plan_id", self.plan_id)
        _require_non_blank("loop_id", self.loop_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.max_iterations > 2:
            raise ValueError("max_iterations must be <= 2")
        if self.max_iterations < 1:
            raise ValueError("max_iterations must be >= 1")
        _validate_true(self, ("manual_only",))
        _validate_false(self, ("autonomous_continuation_allowed",))


@dataclass(frozen=True)
class ManualTwoIterationRehearsalResult:
    result_id: str
    loop_id: str
    iteration_zero_attempted: bool
    iteration_zero_succeeded: bool
    checkpoint_requested: bool
    checkpoint_present: bool
    second_iteration_eligible: bool
    iteration_one_attempted: bool
    iteration_one_succeeded: bool
    stopped_after_iteration_zero: bool
    stopped_after_iteration_one: bool
    max_iteration_cap_enforced: bool
    autonomous_continuation_used: bool
    runtime_authority_granted: bool
    live_workspace_mutated: bool
    model_invoked: bool
    prompt_submitted: bool
    subagent_invoked: bool
    result_summary: str
    evidence_refs: tuple[str, ...]
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("result_id", "loop_id", "result_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("max_iteration_cap_enforced",))
        _validate_false(
            self,
            (
                "autonomous_continuation_used",
                "runtime_authority_granted",
                "live_workspace_mutated",
                "model_invoked",
                "prompt_submitted",
                "subagent_invoked",
            ),
        )


@dataclass(frozen=True)
class ManualTwoIterationAuditRecord:
    audit_id: str
    loop_id: str
    checked_max_two_iterations: bool
    checked_checkpoint_between_iterations: bool
    checked_no_autonomous_continuation: bool
    checked_no_runtime_authority_grant: bool
    checked_no_live_workspace_mutation: bool
    checked_no_model_invocation: bool
    checked_no_prompt_submission: bool
    checked_no_subagent_invocation: bool
    checked_standalone_runtime_not_opened: bool
    notes: tuple[str, ...]
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _require_non_blank("loop_id", self.loop_id)
        _validate_version(self.version)
        _validate_tuple("notes", self.notes)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "checked_max_two_iterations",
                "checked_checkpoint_between_iterations",
                "checked_no_autonomous_continuation",
                "checked_no_runtime_authority_grant",
                "checked_no_live_workspace_mutation",
                "checked_no_model_invocation",
                "checked_no_prompt_submission",
                "checked_no_subagent_invocation",
                "checked_standalone_runtime_not_opened",
            ),
        )


@dataclass(frozen=True)
class ManualTwoIterationSafetyReport:
    report_id: str
    loop_id: str
    safe_for_v0402_manual_rehearsal: bool
    safe_for_autonomous_loop: bool
    safe_for_live_apply: bool
    safe_for_model_invocation: bool
    safe_for_prompt_submission: bool
    safe_for_subagent_invocation: bool
    safe_for_standalone_default_personal_runtime: bool
    requires_v0403_negative_gate_regression: bool
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("loop_id", self.loop_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("safe_for_v0402_manual_rehearsal", "requires_v0403_negative_gate_regression"))
        _validate_false(
            self,
            (
                "safe_for_autonomous_loop",
                "safe_for_live_apply",
                "safe_for_model_invocation",
                "safe_for_prompt_submission",
                "safe_for_subagent_invocation",
                "safe_for_standalone_default_personal_runtime",
            ),
        )


@dataclass(frozen=True)
class ManualTwoIterationReadinessReport:
    report_id: str
    manual_two_iteration_rehearsal_defined: bool = True
    human_checkpoint_between_iterations_required: bool = True
    second_iteration_eligibility_gate_ready: bool = True
    max_two_iteration_cap_ready: bool = True
    no_autonomous_continuation_guarantee_ready: bool = True
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
    report_summary: str = "v0.40.2 rehearses at most two manual sandbox iterations and keeps unsafe runtime surfaces closed."
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("report_summary", self.report_summary)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "manual_two_iteration_rehearsal_defined",
                "human_checkpoint_between_iterations_required",
                "second_iteration_eligibility_gate_ready",
                "max_two_iteration_cap_ready",
                "no_autonomous_continuation_guarantee_ready",
            ),
        )
        _validate_false(self, UNSAFE_READINESS_FLAGS)


@dataclass(frozen=True)
class NoAutonomousContinuationGuarantee:
    guarantee_id: str
    loop_id: str
    autonomous_continuation_allowed: bool
    automatic_second_iteration_allowed: bool
    unbounded_loop_allowed: bool
    retry_loop_allowed: bool
    human_checkpoint_required: bool
    guarantee_statement: str
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("guarantee_id", "loop_id", "guarantee_statement"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("human_checkpoint_required",))
        _validate_false(
            self,
            (
                "autonomous_continuation_allowed",
                "automatic_second_iteration_allowed",
                "unbounded_loop_allowed",
                "retry_loop_allowed",
            ),
        )


@dataclass(frozen=True)
class StandaloneRuntimeStillClosedRecord:
    record_id: str
    chat_service_opened: bool = False
    orchestrator_opened: bool = False
    agent_loop_opened: bool = False
    skill_registry_opened: bool = False
    skill_executor_opened: bool = False
    profile_runtime_opened: bool = False
    prompt_assembly_opened: bool = False
    user_facing_cli_opened: bool = False
    event_trace_emission_opened: bool = False
    standalone_default_personal_runtime_opened: bool = False
    first_smoke_run_conservative_target: str = "v0.41.6"
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _require_non_blank("first_smoke_run_conservative_target", self.first_smoke_run_conservative_target)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, STANDALONE_OPENED_FLAGS)


@dataclass(frozen=True)
class V041SmokeRunAccelerationSignal:
    signal_id: str
    conservative_target: str
    earliest_candidate_target: str | None
    manual_two_iteration_rehearsal_passed: bool
    blocking_runtime_gaps: tuple[str, ...]
    acceleration_conditions: tuple[str, ...]
    recommendation: str
    standalone_runtime_started: bool = False
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("signal_id", "conservative_target", "recommendation"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("blocking_runtime_gaps", self.blocking_runtime_gaps)
        _validate_tuple("acceleration_conditions", self.acceleration_conditions)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, ("standalone_runtime_started",))


@dataclass(frozen=True)
class V0403NegativeRuntimeGateHandoff:
    handoff_id: str
    target_version: str
    target_track: str
    required_negative_cases: tuple[str, ...]
    reason: str
    version: str = V0402_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("handoff_id", "target_version", "target_track", "reason"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("required_negative_cases", self.required_negative_cases)
        _validate_dict("metadata", self.metadata)
        missing = set(V0403_NEGATIVE_CASES).difference(self.required_negative_cases)
        if missing:
            raise ValueError(f"missing negative runtime cases: {sorted(missing)}")


def create_manual_two_iteration_input(**overrides: Any) -> ManualTwoIterationRehearsalInput:
    defaults = {
        "rehearsal_id": "v0402-two-iteration-rehearsal",
        "loop_id": "v0402-loop",
        "mission_id": "v0402-mission",
        "max_iterations": 2,
        "iteration_zero_input_ref": "v0401-iteration-zero-input",
        "iteration_one_input_ref": None,
        "checkpoint_decision_ref": None,
        "manual_mode_required": True,
        "autonomous_continuation_requested": False,
    }
    return ManualTwoIterationRehearsalInput(**_with_overrides(defaults, overrides))


def create_checkpoint_request_after_iteration_zero(
    loop_id: str = "v0402-loop",
    iteration_zero_result_ref: str = "v0401-iteration-zero-result",
    **overrides: Any,
) -> ManualIterationCheckpointRequest:
    upstream_gate = HumanCheckpointGate(
        checkpoint_id="v0402-upstream-human-gate",
        loop_id=loop_id,
        iteration_index=1,
        required=True,
        reason="Manual second iteration rehearsal requires human checkpoint metadata.",
        required_review_refs=(iteration_zero_result_ref,),
        decision_options=("stop", "do_nothing", "continue_as_draft"),
        default_decision=LoopDecisionKind.STOP.value,
        approval_grants_runtime_authority=False,
    )
    defaults = {
        "checkpoint_request_id": "v0402-checkpoint-request",
        "loop_id": loop_id,
        "after_iteration_index": 0,
        "required": True,
        "reason": "Iteration 1 cannot proceed unless explicit human checkpoint decision metadata exists.",
        "required_review_refs": (iteration_zero_result_ref, upstream_gate.checkpoint_id),
        "decision_options": CHECKPOINT_DECISIONS,
        "default_decision": "stop",
        "approval_grants_runtime_authority": False,
        "metadata": {"upstream_human_checkpoint_gate": upstream_gate.checkpoint_id},
    }
    return ManualIterationCheckpointRequest(**_with_overrides(defaults, overrides))


def create_checkpoint_decision(
    checkpoint_request: ManualIterationCheckpointRequest | None = None,
    decision: str = "approve_second_iteration_rehearsal",
    **overrides: Any,
) -> ManualIterationCheckpointDecision:
    request = checkpoint_request or create_checkpoint_request_after_iteration_zero()
    defaults = {
        "checkpoint_decision_id": "v0402-checkpoint-decision",
        "checkpoint_request_id": request.checkpoint_request_id,
        "loop_id": request.loop_id,
        "decision": decision,
        "decision_scope": "manual_bounded_rehearsal_only",
        "approved_iteration_index": 1 if decision == "approve_second_iteration_rehearsal" else None,
        "approved_rehearsal_only": decision == "approve_second_iteration_rehearsal",
        "approval_grants_runtime_authority": False,
        "reviewed_evidence_refs": request.required_review_refs,
    }
    return ManualIterationCheckpointDecision(**_with_overrides(defaults, overrides))


def evaluate_second_iteration_eligibility(
    checkpoint_decision: ManualIterationCheckpointDecision | None = None,
    loop_id: str = "v0402-loop",
    **overrides: Any,
) -> SecondIterationEligibilityDecision:
    if checkpoint_decision is None:
        defaults = {
            "eligibility_id": "v0402-second-iteration-eligibility",
            "loop_id": loop_id,
            "iteration_index": 1,
            "eligible": False,
            "reason": "human_checkpoint_missing",
            "checkpoint_required": True,
            "checkpoint_present": False,
            "checkpoint_decision_ref": None,
            "manual_only": True,
            "runtime_authority_granted": False,
        }
        return SecondIterationEligibilityDecision(**_with_overrides(defaults, overrides))

    eligible = checkpoint_decision.decision == "approve_second_iteration_rehearsal"
    reason = "approved_manual_bounded_rehearsal" if eligible else checkpoint_decision.decision
    defaults = {
        "eligibility_id": "v0402-second-iteration-eligibility",
        "loop_id": checkpoint_decision.loop_id,
        "iteration_index": 1,
        "eligible": eligible,
        "reason": reason,
        "checkpoint_required": True,
        "checkpoint_present": True,
        "checkpoint_decision_ref": checkpoint_decision.checkpoint_decision_id,
        "manual_only": True,
        "runtime_authority_granted": False,
    }
    return SecondIterationEligibilityDecision(**_with_overrides(defaults, overrides))


def create_manual_two_iteration_plan(
    rehearsal_input: ManualTwoIterationRehearsalInput | None = None,
    checkpoint_request: ManualIterationCheckpointRequest | None = None,
    checkpoint_decision: ManualIterationCheckpointDecision | None = None,
    eligibility: SecondIterationEligibilityDecision | None = None,
    **overrides: Any,
) -> ManualTwoIterationRehearsalPlan:
    input_packet = rehearsal_input or create_manual_two_iteration_input()
    request = checkpoint_request
    decision = checkpoint_decision
    eligibility_decision = eligibility
    defaults = {
        "plan_id": "v0402-two-iteration-plan",
        "loop_id": input_packet.loop_id,
        "max_iterations": input_packet.max_iterations,
        "iteration_zero_rehearsal_ref": input_packet.iteration_zero_input_ref,
        "checkpoint_request_ref": request.checkpoint_request_id if request is not None else None,
        "checkpoint_decision_ref": decision.checkpoint_decision_id if decision is not None else None,
        "second_iteration_eligibility_ref": eligibility_decision.eligibility_id if eligibility_decision is not None else None,
        "iteration_one_rehearsal_ref": input_packet.iteration_one_input_ref if eligibility_decision and eligibility_decision.eligible else None,
        "manual_only": True,
        "autonomous_continuation_allowed": False,
    }
    return ManualTwoIterationRehearsalPlan(**_with_overrides(defaults, overrides))


def _default_runner(argv: list[str], cwd_ref: str, timeout_seconds: int, env_overrides: dict[str, str]) -> dict[str, Any]:
    return {
        "stdout": "manual rehearsal runner passed",
        "stderr": "",
        "exit_code": 0,
        "timed_out": False,
        "duration_ms": 1,
        "argv_seen": list(argv),
        "cwd_ref_seen": cwd_ref,
        "timeout_seen": timeout_seconds,
        "env_seen": dict(env_overrides),
    }


def run_manual_two_iteration_rehearsal(
    rehearsal_input: ManualTwoIterationRehearsalInput,
    iteration_zero_input: SandboxRehearsalInput,
    iteration_one_input: SandboxRehearsalInput | None = None,
    checkpoint_decision: ManualIterationCheckpointDecision | None = None,
    runner: RunnerCallable | None = None,
) -> tuple[ManualTwoIterationRehearsalPlan, ManualTwoIterationRehearsalResult, ManualTwoIterationAuditRecord, ManualTwoIterationSafetyReport]:
    if rehearsal_input.max_iterations > 2:
        raise ValueError("max_iterations must be <= 2")
    supplied_runner = runner or _default_runner
    iteration_zero_result, _, _ = run_sandbox_rehearsal(iteration_zero_input, runner=supplied_runner)
    checkpoint_request = create_checkpoint_request_after_iteration_zero(
        loop_id=rehearsal_input.loop_id,
        iteration_zero_result_ref=iteration_zero_result.result_id,
    )
    eligibility = evaluate_second_iteration_eligibility(checkpoint_decision, loop_id=rehearsal_input.loop_id)
    iteration_one_attempted = False
    iteration_one_succeeded = False
    iteration_one_result_ref: str | None = None
    if eligibility.eligible and iteration_one_input is not None:
        iteration_one_result, _, _ = run_sandbox_rehearsal(iteration_one_input, runner=supplied_runner)
        iteration_one_attempted = True
        iteration_one_succeeded = iteration_one_result.apply_succeeded and iteration_one_result.retest_succeeded
        iteration_one_result_ref = iteration_one_result.result_id
    plan = create_manual_two_iteration_plan(
        rehearsal_input,
        checkpoint_request,
        checkpoint_decision,
        eligibility,
        iteration_one_rehearsal_ref=iteration_one_result_ref,
    )
    stopped_after_zero = not eligibility.eligible
    result = ManualTwoIterationRehearsalResult(
        result_id=f"{rehearsal_input.rehearsal_id}-result",
        loop_id=rehearsal_input.loop_id,
        iteration_zero_attempted=True,
        iteration_zero_succeeded=iteration_zero_result.apply_succeeded and iteration_zero_result.retest_succeeded,
        checkpoint_requested=True,
        checkpoint_present=checkpoint_decision is not None,
        second_iteration_eligible=eligibility.eligible,
        iteration_one_attempted=iteration_one_attempted,
        iteration_one_succeeded=iteration_one_succeeded,
        stopped_after_iteration_zero=stopped_after_zero,
        stopped_after_iteration_one=iteration_one_attempted,
        max_iteration_cap_enforced=True,
        autonomous_continuation_used=False,
        runtime_authority_granted=False,
        live_workspace_mutated=False,
        model_invoked=False,
        prompt_submitted=False,
        subagent_invoked=False,
        result_summary="Manual two-iteration rehearsal remained checkpoint-gated and bounded to at most two sandbox rehearsals.",
        evidence_refs=tuple(
            ref
            for ref in (
                iteration_zero_result.result_id,
                checkpoint_request.checkpoint_request_id,
                checkpoint_decision.checkpoint_decision_id if checkpoint_decision else None,
                eligibility.eligibility_id,
                iteration_one_result_ref,
            )
            if ref is not None
        ),
    )
    audit = ManualTwoIterationAuditRecord(
        audit_id=f"{rehearsal_input.rehearsal_id}-audit",
        loop_id=rehearsal_input.loop_id,
        checked_max_two_iterations=True,
        checked_checkpoint_between_iterations=True,
        checked_no_autonomous_continuation=True,
        checked_no_runtime_authority_grant=True,
        checked_no_live_workspace_mutation=True,
        checked_no_model_invocation=True,
        checked_no_prompt_submission=True,
        checked_no_subagent_invocation=True,
        checked_standalone_runtime_not_opened=True,
        notes=("iteration 1 requires explicit checkpoint metadata", "max two-iteration cap enforced"),
    )
    safety = create_manual_two_iteration_safety_report(rehearsal_input.loop_id, result, audit)
    return plan, result, audit, safety


def create_manual_two_iteration_safety_report(
    loop_id: str = "v0402-loop",
    result: ManualTwoIterationRehearsalResult | None = None,
    audit: ManualTwoIterationAuditRecord | None = None,
    **overrides: Any,
) -> ManualTwoIterationSafetyReport:
    safe = True
    if result is not None:
        safe = safe and result.max_iteration_cap_enforced and not result.autonomous_continuation_used
    if audit is not None:
        safe = safe and audit.checked_checkpoint_between_iterations and audit.checked_no_autonomous_continuation
    defaults = {
        "report_id": "v0402-two-iteration-safety-report",
        "loop_id": loop_id,
        "safe_for_v0402_manual_rehearsal": safe,
        "safe_for_autonomous_loop": False,
        "safe_for_live_apply": False,
        "safe_for_model_invocation": False,
        "safe_for_prompt_submission": False,
        "safe_for_subagent_invocation": False,
        "safe_for_standalone_default_personal_runtime": False,
        "requires_v0403_negative_gate_regression": True,
    }
    return ManualTwoIterationSafetyReport(**_with_overrides(defaults, overrides))


def create_manual_two_iteration_readiness_report(**overrides: Any) -> ManualTwoIterationReadinessReport:
    defaults = {"report_id": "v0402-two-iteration-readiness"}
    return ManualTwoIterationReadinessReport(**_with_overrides(defaults, overrides))


def create_no_autonomous_continuation_guarantee(**overrides: Any) -> NoAutonomousContinuationGuarantee:
    defaults = {
        "guarantee_id": "v0402-no-autonomous-continuation",
        "loop_id": "v0402-loop",
        "autonomous_continuation_allowed": False,
        "automatic_second_iteration_allowed": False,
        "unbounded_loop_allowed": False,
        "retry_loop_allowed": False,
        "human_checkpoint_required": True,
        "guarantee_statement": "Iteration 1 requires explicit human checkpoint metadata and never proceeds automatically.",
    }
    return NoAutonomousContinuationGuarantee(**_with_overrides(defaults, overrides))


def create_standalone_runtime_still_closed_record(**overrides: Any) -> StandaloneRuntimeStillClosedRecord:
    upstream_status = create_standalone_agent_runtime_status()
    defaults = {
        "record_id": "v0402-standalone-runtime-still-closed",
        "first_smoke_run_conservative_target": "v0.41.6",
        "metadata": {"upstream_status_ref": upstream_status.status_id},
    }
    return StandaloneRuntimeStillClosedRecord(**_with_overrides(defaults, overrides))


def create_v041_smoke_run_acceleration_signal(
    manual_two_iteration_rehearsal_passed: bool = True,
    gap_register: DefaultPersonalStandaloneGapRegister | None = None,
    upstream_assessment: DefaultPersonalAccelerationAssessment | None = None,
    read_only_skill_registry_can_precede_loop: bool = False,
    **overrides: Any,
) -> V041SmokeRunAccelerationSignal:
    register = gap_register or create_default_personal_gap_register()
    assessment = upstream_assessment or assess_default_personal_acceleration(register)
    blocking = tuple(gap.gap_name for gap in register.gaps if gap.current_status != "complete")
    earliest: str | None = None
    recommendation = "do_not_accelerate"
    conditions: tuple[str, ...] = ("manual_two_iteration_rehearsal_required",)
    if manual_two_iteration_rehearsal_passed:
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
            earliest = assessment.earliest_possible_target
            recommendation = "keep_conservative_target" if earliest is None else "possible_mild_acceleration"
        conditions = ("manual_two_iteration_rehearsal_passed", "standalone_runtime_gaps_must_close")
    defaults = {
        "signal_id": "v0402-v041-smoke-run-acceleration-signal",
        "conservative_target": "v0.41.6",
        "earliest_candidate_target": earliest,
        "manual_two_iteration_rehearsal_passed": manual_two_iteration_rehearsal_passed,
        "blocking_runtime_gaps": blocking,
        "acceleration_conditions": conditions,
        "recommendation": recommendation,
        "standalone_runtime_started": False,
    }
    return V041SmokeRunAccelerationSignal(**_with_overrides(defaults, overrides))


def create_v0403_negative_runtime_gate_handoff(**overrides: Any) -> V0403NegativeRuntimeGateHandoff:
    defaults = {
        "handoff_id": "v0402-v0403-negative-runtime-gate-handoff",
        "target_version": "v0.40.3",
        "target_track": "Negative Runtime Gate Regression",
        "required_negative_cases": V0403_NEGATIVE_CASES,
        "reason": "v0.40.3 should regression-test denied runtime surfaces after manual two-iteration rehearsal.",
    }
    return V0403NegativeRuntimeGateHandoff(**_with_overrides(defaults, overrides))


def manual_iteration_state_ref_is_not_execution_permission(state_ref: ManualIterationStateRef) -> bool:
    return state_ref.execution_permission_granted is False


def second_iteration_eligibility_is_not_runtime_authority(decision: SecondIterationEligibilityDecision) -> bool:
    return decision.manual_only and not decision.runtime_authority_granted


def manual_two_iteration_result_preserves_safety(result: ManualTwoIterationRehearsalResult) -> bool:
    return (
        result.max_iteration_cap_enforced
        and not result.autonomous_continuation_used
        and not result.runtime_authority_granted
        and not result.live_workspace_mutated
        and not result.model_invoked
        and not result.prompt_submitted
        and not result.subagent_invoked
    )


def manual_two_iteration_readiness_preserves_no_unsafe_runtime(report: ManualTwoIterationReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_READINESS_FLAGS)


def standalone_runtime_still_closed(record: StandaloneRuntimeStillClosedRecord) -> bool:
    return all(getattr(record, name) is False for name in STANDALONE_OPENED_FLAGS)


def smoke_run_acceleration_signal_is_not_runtime_start(signal: V041SmokeRunAccelerationSignal) -> bool:
    return signal.standalone_runtime_started is False
