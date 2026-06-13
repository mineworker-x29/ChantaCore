"""v0.40.0 controlled multi-iteration mission loop boundary metadata.

This module can describe, simulate, deny, and guide a future repair mission
loop. It cannot execute, invoke, submit, delegate, mutate, persist, or certify.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0400_VERSION = "v0.40.0"
V0400_RELEASE_NAME = "v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation"
V040_TRACK_NAME = "Controlled Multi-Iteration Mission Loop with Execution-Test Ladder and Subagent Verification Boundary"


class IterationStatus(StrEnum):
    DRAFTED = "drafted"
    DRY_RUN_SIMULATED = "dry_run_simulated"
    CHECKPOINT_REQUIRED = "checkpoint_required"
    BLOCKED = "blocked"
    STOPPED = "stopped"
    ELIGIBLE_FOR_NEXT_ITERATION = "eligible_for_next_iteration"


class LoopDecisionKind(StrEnum):
    CONTINUE_AS_DRAFT = "continue_as_draft"
    REQUEST_HUMAN_CHECKPOINT = "request_human_checkpoint"
    REQUEST_VERIFIER_DRAFT = "request_verifier_draft"
    STOP = "stop"
    DO_NOTHING = "do_nothing"
    BLOCK = "block"


class RuntimeActionType(StrEnum):
    MODEL_PROVIDER_INVOCATION = "model_provider_invocation"
    PROMPT_SUBMISSION = "prompt_submission"
    SUBAGENT_INVOCATION = "subagent_invocation"
    EXTERNAL_AGENT_EXECUTION = "external_agent_execution"
    AUTOMATIC_REPAIR = "automatic_repair"
    RETRY_LOOP = "retry_loop"
    MULTI_CYCLE_LOOP = "multi_cycle_loop"
    LIVE_WORKSPACE_APPLY = "live_workspace_apply"
    DOMINION_RUNTIME = "dominion_runtime"
    PRODUCTION_CERTIFICATION = "production_certification"


class SafeAlternative(StrEnum):
    DRY_RUN = "dry_run"
    REQUEST_HUMAN_CHECKPOINT = "request_human_checkpoint"
    CREATE_DRAFT = "create_draft"
    SIMULATE = "simulate"
    DO_NOTHING = "do_nothing"
    STOP = "stop"


REQUIRED_STOP_SIGNALS: tuple[str, ...] = (
    "budget_exhausted",
    "human_checkpoint_missing",
    "unsafe_runtime_requested",
    "model_invocation_without_gate",
    "prompt_submission_without_gate",
    "subagent_invocation_without_gate",
    "live_workspace_apply_requested",
    "automatic_repair_requested",
    "retry_loop_requested",
    "dominion_runtime_requested",
    "production_certification_claimed",
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
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_dominion_runtime",
    "production_certified",
)


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0400_VERSION not in version:
        raise ValueError("version must include v0.40.0")


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


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


@dataclass(frozen=True)
class MissionLoopEnvelope:
    loop_id: str
    mission_id: str
    source_handoff_ref: str | None = None
    source_process_state_ref: str | None = None
    current_iteration_index: int = 0
    max_iteration_count: int = 1
    status: str = "drafted"
    human_checkpoint_required: bool = True
    autonomous_continuation_allowed: bool = False
    dry_run_only: bool = True
    sandbox_rehearsal_allowed: bool = False
    production_certified: bool = False
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_id", self.loop_id)
        _require_non_blank("mission_id", self.mission_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.current_iteration_index != 0:
            raise ValueError("current_iteration_index must be 0 for v0.40.0")
        if self.max_iteration_count != 1:
            raise ValueError("max_iteration_count must be 1 for v0.40.0")
        if self.human_checkpoint_required is not True:
            raise ValueError("human_checkpoint_required must be True")
        if self.dry_run_only is not True:
            raise ValueError("dry_run_only must be True")
        _validate_false(
            self,
            (
                "autonomous_continuation_allowed",
                "sandbox_rehearsal_allowed",
                "production_certified",
            ),
        )


@dataclass(frozen=True)
class IterationState:
    loop_id: str
    iteration_index: int
    input_refs: tuple[str, ...] = ()
    process_state_refs: tuple[str, ...] = ()
    comparison_refs: tuple[str, ...] = ()
    next_action_draft_refs: tuple[str, ...] = ()
    verifier_request_draft_refs: tuple[str, ...] = ()
    denied_runtime_action_refs: tuple[str, ...] = ()
    status: str = IterationStatus.DRAFTED.value
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_id", self.loop_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        for name in (
            "input_refs",
            "process_state_refs",
            "comparison_refs",
            "next_action_draft_refs",
            "verifier_request_draft_refs",
            "denied_runtime_action_refs",
        ):
            _validate_tuple(name, getattr(self, name))
        if self.iteration_index < 0:
            raise ValueError("iteration_index must be >= 0")
        if self.status not in {item.value for item in IterationStatus}:
            raise ValueError("invalid iteration status")

    @property
    def grants_execution_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class StopConditionContract:
    contract_id: str
    loop_id: str
    stop_signals: tuple[str, ...] = REQUIRED_STOP_SIGNALS
    active_stop_signals: tuple[str, ...] = ()
    continuation_requires_stop_condition_check: bool = True
    unsafe_runtime_requested: bool = False
    decision_if_triggered: str = LoopDecisionKind.STOP.value
    do_nothing_allowed: bool = True
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("contract_id", self.contract_id)
        _require_non_blank("loop_id", self.loop_id)
        _validate_version(self.version)
        _validate_tuple("stop_signals", self.stop_signals)
        _validate_tuple("active_stop_signals", self.active_stop_signals)
        _validate_dict("metadata", self.metadata)
        missing = set(REQUIRED_STOP_SIGNALS).difference(self.stop_signals)
        if missing:
            raise ValueError(f"missing required stop signals: {sorted(missing)}")
        if self.continuation_requires_stop_condition_check is not True:
            raise ValueError("continuation requires stop condition check")
        if self.unsafe_runtime_requested and self.decision_if_triggered not in {
            LoopDecisionKind.BLOCK.value,
            LoopDecisionKind.STOP.value,
        }:
            raise ValueError("unsafe runtime must block or stop")
        if self.do_nothing_allowed is not True:
            raise ValueError("do_nothing must remain a valid loop decision")


@dataclass(frozen=True)
class LoopBudgetGate:
    loop_id: str
    max_iterations: int
    used_iterations: int
    max_prompt_drafts: int
    used_prompt_drafts: int
    max_verifier_request_drafts: int
    used_verifier_request_drafts: int
    max_estimated_tokens: int | None
    used_estimated_tokens: int | None
    budget_status: str
    unknown_token_budget_requires_checkpoint: bool
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_id", self.loop_id)
        _require_non_blank("budget_status", self.budget_status)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        for name in ("max_iterations", "max_prompt_drafts", "max_verifier_request_drafts"):
            if getattr(self, name) <= 0:
                raise ValueError(f"{name} must be > 0")
        for name in ("used_iterations", "used_prompt_drafts", "used_verifier_request_drafts"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        if self.max_estimated_tokens is None:
            if self.unknown_token_budget_requires_checkpoint is not True:
                raise ValueError("unknown token budget requires checkpoint")
            if self.budget_status == "unlimited":
                raise ValueError("unknown token budget is not unlimited")
        if self.max_estimated_tokens is not None and self.max_estimated_tokens <= 0:
            raise ValueError("max_estimated_tokens must be > 0 when provided")
        if self.used_estimated_tokens is not None and self.used_estimated_tokens < 0:
            raise ValueError("used_estimated_tokens must be >= 0 when provided")


@dataclass(frozen=True)
class HumanCheckpointGate:
    checkpoint_id: str
    loop_id: str
    iteration_index: int
    required: bool
    reason: str
    required_review_refs: tuple[str, ...]
    decision_options: tuple[str, ...]
    default_decision: str
    approval_grants_runtime_authority: bool
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("checkpoint_id", "loop_id", "reason", "default_decision"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("required_review_refs", self.required_review_refs)
        _validate_tuple("decision_options", self.decision_options)
        _validate_dict("metadata", self.metadata)
        if self.iteration_index < 0:
            raise ValueError("iteration_index must be >= 0")
        if self.required is not True:
            raise ValueError("checkpoint must be required")
        if self.default_decision != LoopDecisionKind.STOP.value:
            raise ValueError("default_decision must be stop")
        if LoopDecisionKind.STOP.value not in self.decision_options:
            raise ValueError("stop must be a decision option")
        _validate_false(self, ("approval_grants_runtime_authority",))


@dataclass(frozen=True)
class LoopDecisionRecord:
    decision_id: str
    loop_id: str
    iteration_index: int
    decision_kind: str
    reason: str
    requires_human_checkpoint: bool
    grants_runtime_authority: bool
    safe_alternative: str | None
    evidence_refs: tuple[str, ...]
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "loop_id", "decision_kind", "reason"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.iteration_index < 0:
            raise ValueError("iteration_index must be >= 0")
        if self.decision_kind not in {item.value for item in LoopDecisionKind}:
            raise ValueError("invalid loop decision kind")
        _validate_false(self, ("grants_runtime_authority",))


@dataclass(frozen=True)
class DeniedRuntimeActionMetadata:
    denied_action_id: str
    loop_id: str
    iteration_index: int
    requested_action_type: str
    denial_reason: str
    safety_boundary: str
    suggested_safe_alternative: str
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in (
            "denied_action_id",
            "loop_id",
            "requested_action_type",
            "denial_reason",
            "safety_boundary",
            "suggested_safe_alternative",
        ):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.iteration_index < 0:
            raise ValueError("iteration_index must be >= 0")
        if self.requested_action_type not in {item.value for item in RuntimeActionType}:
            raise ValueError("invalid requested action type")
        if self.suggested_safe_alternative not in {item.value for item in SafeAlternative}:
            raise ValueError("invalid safe alternative")


@dataclass(frozen=True)
class ProviderBoundaryGate:
    boundary_id: str
    loop_id: str
    provider_ref: str | None = None
    model_ref: str | None = None
    prompt_draft_ref: str | None = None
    invocation_requested: bool = False
    invocation_allowed: bool = False
    dispatch_mode: str = "metadata_only"
    output_quarantine_required: bool = True
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _require_non_blank("loop_id", self.loop_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.dispatch_mode != "metadata_only":
            raise ValueError("dispatch_mode must be metadata_only")
        if self.output_quarantine_required is not True:
            raise ValueError("output_quarantine_required must be True")
        _validate_false(self, ("invocation_allowed",))


@dataclass(frozen=True)
class PromptSubmissionBoundary:
    boundary_id: str
    loop_id: str
    prompt_draft_ref: str | None = None
    submission_requested: bool = False
    submission_allowed: bool = False
    submitted_to_model: bool = False
    human_checkpoint_required: bool = True
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _require_non_blank("loop_id", self.loop_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.human_checkpoint_required is not True:
            raise ValueError("human_checkpoint_required must be True")
        _validate_false(self, ("submission_allowed", "submitted_to_model"))


@dataclass(frozen=True)
class VerifierSubagentBoundary:
    boundary_id: str
    loop_id: str
    verifier_role: str
    input_refs: tuple[str, ...]
    evidence_requirements: tuple[str, ...]
    invocation_requested: bool = False
    invocation_allowed: bool = False
    subagent_invoked: bool = False
    parent_context_shared: bool = False
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("boundary_id", "loop_id", "verifier_role"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("input_refs", self.input_refs)
        _validate_tuple("evidence_requirements", self.evidence_requirements)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, ("invocation_allowed", "subagent_invoked", "parent_context_shared"))


@dataclass(frozen=True)
class SimulatedMultiIterationLoopPacket:
    packet_id: str
    loop_envelope: MissionLoopEnvelope
    iteration_states: tuple[IterationState, ...]
    loop_decision: LoopDecisionRecord
    denied_actions: tuple[DeniedRuntimeActionMetadata, ...] = ()
    executed: bool = False
    mutated_files: bool = False
    invoked_model: bool = False
    invoked_subagent: bool = False
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("packet_id", self.packet_id)
        _validate_version(self.version)
        _validate_tuple("iteration_states", self.iteration_states)
        _validate_tuple("denied_actions", self.denied_actions)
        _validate_dict("metadata", self.metadata)
        if not isinstance(self.loop_envelope, MissionLoopEnvelope):
            raise TypeError("loop_envelope must be MissionLoopEnvelope")
        if not isinstance(self.loop_decision, LoopDecisionRecord):
            raise TypeError("loop_decision must be LoopDecisionRecord")
        if not self.iteration_states:
            raise ValueError("iteration_states must not be empty")
        _validate_false(self, ("executed", "mutated_files", "invoked_model", "invoked_subagent"))


@dataclass(frozen=True)
class V040ReadinessReport:
    report_id: str
    release_name: str = V0400_RELEASE_NAME
    track_name: str = V040_TRACK_NAME
    controlled_multi_iteration_boundary_defined: bool = True
    dry_run_simulation_ready: bool = True
    negative_runtime_gate_test_ready: bool = True
    default_personal_user_guide_ready: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_live_workspace_apply: bool = False
    ready_for_prompt_submission_to_model: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_dominion_runtime: bool = False
    production_certified: bool = False
    report_summary: str = "v0.40.0 can describe, simulate, deny, and guide; it cannot execute, invoke, submit, delegate, mutate, persist, or certify."
    version: str = V0400_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "release_name", "track_name", "report_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        for name in (
            "controlled_multi_iteration_boundary_defined",
            "dry_run_simulation_ready",
            "negative_runtime_gate_test_ready",
            "default_personal_user_guide_ready",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_false(self, UNSAFE_READINESS_FLAGS)


def create_default_mission_loop_envelope(**overrides: Any) -> MissionLoopEnvelope:
    defaults = {
        "loop_id": "v0400-loop",
        "mission_id": "v0400-mission",
        "source_handoff_ref": "v0399-handoff",
        "source_process_state_ref": "v0396-process-state",
    }
    return MissionLoopEnvelope(**_with_overrides(defaults, overrides))


def create_initial_iteration_state(**overrides: Any) -> IterationState:
    defaults = {
        "loop_id": "v0400-loop",
        "iteration_index": 0,
        "input_refs": ("v0399-handoff",),
        "process_state_refs": ("v0396-process-state",),
        "comparison_refs": ("v0395-comparison",),
        "next_action_draft_refs": ("v0397-next-action-draft",),
        "verifier_request_draft_refs": ("v0397-verifier-request-draft",),
        "status": IterationStatus.DRAFTED.value,
    }
    return IterationState(**_with_overrides(defaults, overrides))


def evaluate_stop_conditions(
    *,
    loop_id: str = "v0400-loop",
    active_stop_signals: tuple[str, ...] = (),
    unsafe_runtime_requested: bool = False,
    **overrides: Any,
) -> StopConditionContract:
    decision = LoopDecisionKind.BLOCK.value if unsafe_runtime_requested else LoopDecisionKind.STOP.value
    defaults = {
        "contract_id": "v0400-stop-condition",
        "loop_id": loop_id,
        "active_stop_signals": active_stop_signals,
        "unsafe_runtime_requested": unsafe_runtime_requested,
        "decision_if_triggered": decision,
    }
    return StopConditionContract(**_with_overrides(defaults, overrides))


def evaluate_loop_budget(**overrides: Any) -> LoopBudgetGate:
    max_tokens = overrides.get("max_estimated_tokens", None)
    defaults = {
        "loop_id": "v0400-loop",
        "max_iterations": 1,
        "used_iterations": 0,
        "max_prompt_drafts": 2,
        "used_prompt_drafts": 0,
        "max_verifier_request_drafts": 1,
        "used_verifier_request_drafts": 0,
        "max_estimated_tokens": max_tokens,
        "used_estimated_tokens": None,
        "budget_status": "checkpoint_required" if max_tokens is None else "within_budget",
        "unknown_token_budget_requires_checkpoint": max_tokens is None,
    }
    return LoopBudgetGate(**_with_overrides(defaults, overrides))


def require_human_checkpoint_for_second_iteration(
    iteration_state: IterationState | None = None,
    **overrides: Any,
) -> HumanCheckpointGate:
    index = iteration_state.iteration_index if iteration_state is not None else 1
    defaults = {
        "checkpoint_id": f"v0400-human-checkpoint-{index}",
        "loop_id": iteration_state.loop_id if iteration_state is not None else "v0400-loop",
        "iteration_index": index,
        "required": True,
        "reason": "Second iteration requires human checkpoint metadata before any continuation.",
        "required_review_refs": ("loop-decision", "stop-condition", "budget-gate"),
        "decision_options": (
            LoopDecisionKind.STOP.value,
            LoopDecisionKind.DO_NOTHING.value,
            LoopDecisionKind.CONTINUE_AS_DRAFT.value,
        ),
        "default_decision": LoopDecisionKind.STOP.value,
        "approval_grants_runtime_authority": False,
    }
    return HumanCheckpointGate(**_with_overrides(defaults, overrides))


def create_denied_runtime_action(**overrides: Any) -> DeniedRuntimeActionMetadata:
    defaults = {
        "denied_action_id": "v0400-denied-runtime-action",
        "loop_id": "v0400-loop",
        "iteration_index": 0,
        "requested_action_type": RuntimeActionType.MODEL_PROVIDER_INVOCATION.value,
        "denial_reason": "v0.40.0 is boundary and dry-run only.",
        "safety_boundary": "Controlled Multi-Iteration Mission Loop Boundary",
        "suggested_safe_alternative": SafeAlternative.CREATE_DRAFT.value,
    }
    return DeniedRuntimeActionMetadata(**_with_overrides(defaults, overrides))


def create_provider_boundary_gate(**overrides: Any) -> ProviderBoundaryGate:
    defaults = {
        "boundary_id": "v0400-provider-boundary",
        "loop_id": "v0400-loop",
        "provider_ref": None,
        "model_ref": None,
        "prompt_draft_ref": "v0397-self-prompt-draft",
        "invocation_requested": False,
        "invocation_allowed": False,
        "dispatch_mode": "metadata_only",
        "output_quarantine_required": True,
    }
    return ProviderBoundaryGate(**_with_overrides(defaults, overrides))


def create_prompt_submission_boundary(**overrides: Any) -> PromptSubmissionBoundary:
    defaults = {
        "boundary_id": "v0400-prompt-submission-boundary",
        "loop_id": "v0400-loop",
        "prompt_draft_ref": "v0397-self-prompt-draft",
        "submission_requested": False,
        "submission_allowed": False,
        "submitted_to_model": False,
        "human_checkpoint_required": True,
    }
    return PromptSubmissionBoundary(**_with_overrides(defaults, overrides))


def create_verifier_subagent_boundary(**overrides: Any) -> VerifierSubagentBoundary:
    defaults = {
        "boundary_id": "v0400-verifier-boundary",
        "loop_id": "v0400-loop",
        "verifier_role": "verifier-subagent-boundary-metadata",
        "input_refs": ("v0397-verifier-request-draft",),
        "evidence_requirements": ("process-state-ref", "comparison-ref", "human-checkpoint-ref"),
        "invocation_requested": False,
        "invocation_allowed": False,
        "subagent_invoked": False,
        "parent_context_shared": False,
    }
    return VerifierSubagentBoundary(**_with_overrides(defaults, overrides))


def simulate_multi_iteration_loop_dry_run(**overrides: Any) -> SimulatedMultiIterationLoopPacket:
    envelope = overrides.pop("loop_envelope", create_default_mission_loop_envelope())
    first_iteration = create_initial_iteration_state(loop_id=envelope.loop_id)
    checkpoint = require_human_checkpoint_for_second_iteration(
        IterationState(
            loop_id=envelope.loop_id,
            iteration_index=1,
            status=IterationStatus.CHECKPOINT_REQUIRED.value,
        )
    )
    decision = LoopDecisionRecord(
        decision_id="v0400-loop-decision",
        loop_id=envelope.loop_id,
        iteration_index=0,
        decision_kind=LoopDecisionKind.REQUEST_HUMAN_CHECKPOINT.value,
        reason="Dry-run simulation stops before any second iteration until human checkpoint metadata is reviewed.",
        requires_human_checkpoint=True,
        grants_runtime_authority=False,
        safe_alternative=SafeAlternative.REQUEST_HUMAN_CHECKPOINT.value,
        evidence_refs=(checkpoint.checkpoint_id,),
    )
    second_iteration_marker = IterationState(
        loop_id=envelope.loop_id,
        iteration_index=1,
        input_refs=(checkpoint.checkpoint_id,),
        status=IterationStatus.CHECKPOINT_REQUIRED.value,
    )
    defaults = {
        "packet_id": "v0400-simulated-loop-packet",
        "loop_envelope": envelope,
        "iteration_states": (first_iteration, second_iteration_marker),
        "loop_decision": decision,
        "denied_actions": (),
    }
    return SimulatedMultiIterationLoopPacket(**_with_overrides(defaults, overrides))


def create_v040_readiness_report(**overrides: Any) -> V040ReadinessReport:
    defaults = {
        "report_id": "v0400-readiness-report",
    }
    return V040ReadinessReport(**_with_overrides(defaults, overrides))


def iteration_state_is_not_execution_permission(iteration_state: IterationState) -> bool:
    return iteration_state.grants_execution_permission is False


def provider_boundary_gate_is_not_invocation(gate: ProviderBoundaryGate) -> bool:
    return gate.invocation_allowed is False and gate.dispatch_mode == "metadata_only"


def prompt_submission_boundary_is_not_submission(boundary: PromptSubmissionBoundary) -> bool:
    return boundary.submission_allowed is False and boundary.submitted_to_model is False


def verifier_subagent_boundary_is_not_invocation(boundary: VerifierSubagentBoundary) -> bool:
    return (
        boundary.invocation_allowed is False
        and boundary.subagent_invoked is False
        and boundary.parent_context_shared is False
    )


def simulated_packet_is_dry_run_only(packet: SimulatedMultiIterationLoopPacket) -> bool:
    return (
        packet.executed is False
        and packet.mutated_files is False
        and packet.invoked_model is False
        and packet.invoked_subagent is False
    )


def v040_readiness_report_preserves_no_execution(report: V040ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_READINESS_FLAGS)
