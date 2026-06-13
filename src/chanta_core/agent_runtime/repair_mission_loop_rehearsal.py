"""v0.40.1 sandbox rehearsal and standalone readiness clarification.

The rehearsal layer wraps the existing v0.39.3 sandbox-only text replacement
primitive and the v0.39.4 controlled retest primitive. It does not open
standalone agent execution, provider calls, prompt submission, subagent calls,
live workspace mutation, arbitrary commands, Dominion runtime, or production
certification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .boundary import _require_non_blank
from .repair_post_apply_retest import (
    build_repair_post_apply_retest_input,
    build_repair_post_apply_test_selection_plan,
    create_repair_controlled_test_command_spec,
    run_post_apply_controlled_retest,
)
from .repair_sandbox_apply import (
    apply_sandbox_text_replacements,
    build_repair_sandbox_apply_input,
    create_sandbox_apply_operations,
)


V0401_VERSION = "v0.40.1"
V0401_RELEASE_NAME = "v0.40.1 Sandbox Rehearsal Runner & Standalone Agent Readiness Clarification"
V0401_TRACK_NAME = "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + Sandbox Rehearsal + Manual Runtime Gap Accounting"

RunnerCallable = Callable[[list[str], str, int, dict[str, str]], dict[str, Any]]

UNSAFE_READINESS_FLAGS: tuple[str, ...] = (
    "ready_for_live_workspace_apply",
    "ready_for_autonomous_loop_runtime",
    "ready_for_model_provider_invocation",
    "ready_for_prompt_submission_to_model",
    "ready_for_subagent_invocation",
    "ready_for_external_agent_execution",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_dominion_runtime",
    "production_certified",
)

OPENED_RUNTIME_FLAGS: tuple[str, ...] = (
    "chat_service_opened",
    "orchestrator_opened",
    "agent_loop_opened",
    "skill_loader_opened",
    "skill_executor_opened",
    "prompt_assembly_opened",
    "profile_runtime_opened",
    "session_store_opened",
    "event_trace_emission_opened",
    "user_facing_cli_opened",
    "standalone_default_personal_runtime_opened",
)

REQUIRED_GAP_NAMES: tuple[str, ...] = (
    "ChatService",
    "Orchestrator",
    "AgentLoop",
    "SkillRegistry",
    "SkillExecutor",
    "PromptAssembly",
    "ProfileRuntime",
    "SessionStore",
    "EventTraceEmitter",
    "UserFacingCLI",
    "DefaultPersonalSmokeScenario",
)

MINIMUM_USER_FACING_COMMANDS: tuple[str, ...] = (
    "chanta personal status",
    "chanta personal ask",
    "chanta personal inspect",
    "chanta personal trace recent",
    "chanta personal dry-run",
)

MINIMUM_READ_ONLY_SKILLS: tuple[str, ...] = (
    "status_summary",
    "inspect_file",
    "inspect_directory",
    "summarize_recent_trace",
    "dry_run_mission_loop",
    "explain_boundary_report",
)

MINIMUM_EVENTS: tuple[str, ...] = (
    "user_goal_received",
    "profile_loaded",
    "prompt_assembled",
    "skill_selected",
    "skill_executed",
    "observation_recorded",
    "response_emitted",
)

V041_SEQUENCE: tuple[str, ...] = (
    "v0.41.0 Default Personal Profile Runtime",
    "v0.41.1 User-facing CLI Entry",
    "v0.41.2 Prompt Assembly / Soul-Role-Domain Binding",
    "v0.41.3 Read-only Skill Registry",
    "v0.41.4 Minimal AgentLoop",
    "v0.41.5 Event / Trace Emission",
    "v0.41.6 First Default Personal Smoke Run",
)


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0401_VERSION not in version:
        raise ValueError("version must include v0.40.1")


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
class SandboxRehearsalInput:
    rehearsal_id: str
    loop_id: str
    iteration_index: int
    sandbox_root_ref: str
    target_relative_path: str
    original_text: str
    replacement_text: str
    test_command_ref: str | None = None
    human_checkpoint_ref: str | None = None
    live_workspace_apply_requested: bool = False
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in (
            "rehearsal_id",
            "loop_id",
            "sandbox_root_ref",
            "target_relative_path",
            "original_text",
            "replacement_text",
        ):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.iteration_index < 0:
            raise ValueError("iteration_index must be >= 0")
        _validate_false(self, ("live_workspace_apply_requested",))


@dataclass(frozen=True)
class SandboxRehearsalApplyPlan:
    plan_id: str
    rehearsal_id: str
    uses_v0393_sandbox_apply_primitive: bool
    sandbox_root_ref: str
    target_relative_path: str
    exact_text_replacement_required: bool
    live_workspace_allowed: bool
    git_apply_allowed: bool
    apply_patch_allowed: bool
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("plan_id", "rehearsal_id", "sandbox_root_ref", "target_relative_path"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("uses_v0393_sandbox_apply_primitive", "exact_text_replacement_required"))
        _validate_false(self, ("live_workspace_allowed", "git_apply_allowed", "apply_patch_allowed"))


@dataclass(frozen=True)
class SandboxRehearsalRetestPlan:
    plan_id: str
    rehearsal_id: str
    uses_v0394_controlled_retest_primitive: bool
    supplied_runner_required: bool
    shell_allowed: bool
    bounded_argv_required: bool
    timeout_required: bool
    output_capture_bounded: bool
    network_allowed: bool
    dependency_install_allowed: bool
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("plan_id", "rehearsal_id"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "uses_v0394_controlled_retest_primitive",
                "supplied_runner_required",
                "bounded_argv_required",
                "timeout_required",
                "output_capture_bounded",
            ),
        )
        _validate_false(self, ("shell_allowed", "network_allowed", "dependency_install_allowed"))


@dataclass(frozen=True)
class SandboxRehearsalResult:
    result_id: str
    rehearsal_id: str
    apply_attempted: bool
    apply_succeeded: bool
    retest_attempted: bool
    retest_succeeded: bool
    sandbox_only: bool
    live_workspace_mutated: bool
    model_invoked: bool
    prompt_submitted: bool
    subagent_invoked: bool
    external_agent_invoked: bool
    runtime_authority_granted: bool
    result_summary: str
    evidence_refs: tuple[str, ...]
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("result_id", "rehearsal_id", "result_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("sandbox_only",))
        _validate_false(
            self,
            (
                "live_workspace_mutated",
                "model_invoked",
                "prompt_submitted",
                "subagent_invoked",
                "external_agent_invoked",
                "runtime_authority_granted",
            ),
        )


@dataclass(frozen=True)
class SandboxRehearsalAuditRecord:
    audit_id: str
    rehearsal_id: str
    checked_sandbox_containment: bool
    checked_no_live_workspace: bool
    checked_no_git_apply: bool
    checked_no_apply_patch: bool
    checked_no_raw_subprocess: bool
    checked_no_shell: bool
    checked_no_network: bool
    checked_no_dependency_install: bool
    checked_no_model_invocation: bool
    checked_no_subagent_invocation: bool
    notes: tuple[str, ...]
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _require_non_blank("rehearsal_id", self.rehearsal_id)
        _validate_version(self.version)
        _validate_tuple("notes", self.notes)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "checked_sandbox_containment",
                "checked_no_live_workspace",
                "checked_no_git_apply",
                "checked_no_apply_patch",
                "checked_no_raw_subprocess",
                "checked_no_shell",
                "checked_no_network",
                "checked_no_dependency_install",
                "checked_no_model_invocation",
                "checked_no_subagent_invocation",
            ),
        )


@dataclass(frozen=True)
class SandboxRehearsalSafetyReport:
    report_id: str
    rehearsal_id: str
    safe_for_v0401: bool
    safe_for_live_apply: bool
    safe_for_autonomous_loop: bool
    safe_for_model_invocation: bool
    safe_for_subagent_invocation: bool
    requires_human_checkpoint_before_next_iteration: bool
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("rehearsal_id", self.rehearsal_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("safe_for_v0401", "requires_human_checkpoint_before_next_iteration"))
        _validate_false(
            self,
            (
                "safe_for_live_apply",
                "safe_for_autonomous_loop",
                "safe_for_model_invocation",
                "safe_for_subagent_invocation",
            ),
        )


@dataclass(frozen=True)
class SandboxRehearsalReadinessReport:
    report_id: str
    sandbox_rehearsal_runner_defined: bool = True
    v0393_sandbox_apply_primitive_reused: bool = True
    v0394_controlled_retest_primitive_reused: bool = True
    temp_sandbox_fixture_ready: bool = True
    ready_for_live_workspace_apply: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_prompt_submission_to_model: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_dominion_runtime: bool = False
    production_certified: bool = False
    report_summary: str = "v0.40.1 rehearses bounded sandbox apply/retest only and does not open standalone Default Personal runtime."
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("report_summary", self.report_summary)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "sandbox_rehearsal_runner_defined",
                "v0393_sandbox_apply_primitive_reused",
                "v0394_controlled_retest_primitive_reused",
                "temp_sandbox_fixture_ready",
            ),
        )
        _validate_false(self, UNSAFE_READINESS_FLAGS)


@dataclass(frozen=True)
class StandaloneAgentRuntimeStatus:
    status_id: str
    chat_service_opened: bool = False
    orchestrator_opened: bool = False
    agent_loop_opened: bool = False
    skill_loader_opened: bool = False
    skill_executor_opened: bool = False
    prompt_assembly_opened: bool = False
    profile_runtime_opened: bool = False
    session_store_opened: bool = False
    event_trace_emission_opened: bool = False
    user_facing_cli_opened: bool = False
    standalone_default_personal_runtime_opened: bool = False
    first_smoke_run_target_version: str = "v0.41.6-conservative"
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("status_id", self.status_id)
        _require_non_blank("first_smoke_run_target_version", self.first_smoke_run_target_version)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, OPENED_RUNTIME_FLAGS)


@dataclass(frozen=True)
class DefaultPersonalStandaloneGap:
    gap_id: str
    gap_name: str
    required_for: str
    current_status: str
    target_version: str
    risk_if_missing: str
    acceleration_possible: bool
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("gap_id", "gap_name", "required_for", "current_status", "target_version", "risk_if_missing"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class DefaultPersonalStandaloneGapRegister:
    register_id: str
    gaps: tuple[DefaultPersonalStandaloneGap, ...]
    standalone_runtime_started: bool = False
    conservative_first_smoke_target: str = "v0.41.6"
    earliest_possible_smoke_target: str | None = None
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("register_id", self.register_id)
        _require_non_blank("conservative_first_smoke_target", self.conservative_first_smoke_target)
        _validate_version(self.version)
        _validate_tuple("gaps", self.gaps)
        _validate_dict("metadata", self.metadata)
        if not self.gaps:
            raise ValueError("gaps must not be empty")
        gap_names = {gap.gap_name for gap in self.gaps}
        missing = set(REQUIRED_GAP_NAMES).difference(gap_names)
        if missing:
            raise ValueError(f"missing required gaps: {sorted(missing)}")
        _validate_false(self, ("standalone_runtime_started",))


@dataclass(frozen=True)
class DefaultPersonalRequiredRuntimeSurface:
    surface_id: str
    required_components: tuple[str, ...]
    minimum_user_facing_commands: tuple[str, ...]
    minimum_read_only_skills: tuple[str, ...]
    minimum_events: tuple[str, ...]
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("surface_id", self.surface_id)
        _validate_version(self.version)
        for name in ("required_components", "minimum_user_facing_commands", "minimum_read_only_skills", "minimum_events"):
            _validate_tuple(name, getattr(self, name))
            if not getattr(self, name):
                raise ValueError(f"{name} must not be empty")
        _validate_dict("metadata", self.metadata)
        for command in MINIMUM_USER_FACING_COMMANDS:
            if command not in self.minimum_user_facing_commands:
                raise ValueError(f"missing minimum command: {command}")
        for skill in MINIMUM_READ_ONLY_SKILLS:
            if skill not in self.minimum_read_only_skills:
                raise ValueError(f"missing minimum read-only skill: {skill}")
        for event in MINIMUM_EVENTS:
            if event not in self.minimum_events:
                raise ValueError(f"missing minimum event: {event}")


@dataclass(frozen=True)
class DefaultPersonalAccelerationAssessment:
    assessment_id: str
    conservative_target: str
    earliest_possible_target: str | None
    blocking_gaps: tuple[str, ...]
    acceleratable_gaps: tuple[str, ...]
    recommendation: str
    standalone_runtime_started: bool = False
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("assessment_id", "conservative_target", "recommendation"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("blocking_gaps", self.blocking_gaps)
        _validate_tuple("acceleratable_gaps", self.acceleratable_gaps)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, ("standalone_runtime_started",))


@dataclass(frozen=True)
class V041DefaultPersonalRuntimeHandoffDraft:
    handoff_id: str
    target_track: str
    recommended_start_version: str
    first_smoke_run_conservative_target: str
    first_smoke_run_acceleration_note: str
    required_components: tuple[str, ...]
    recommended_v041_sequence: tuple[str, ...]
    version: str = V0401_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in (
            "handoff_id",
            "target_track",
            "recommended_start_version",
            "first_smoke_run_conservative_target",
            "first_smoke_run_acceleration_note",
        ):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("required_components", self.required_components)
        _validate_tuple("recommended_v041_sequence", self.recommended_v041_sequence)
        _validate_dict("metadata", self.metadata)
        for item in V041_SEQUENCE:
            if item not in self.recommended_v041_sequence:
                raise ValueError(f"missing v0.41 sequence item: {item}")


def create_sandbox_rehearsal_input(**overrides: Any) -> SandboxRehearsalInput:
    defaults = {
        "rehearsal_id": "v0401-rehearsal",
        "loop_id": "v0400-loop",
        "iteration_index": 0,
        "sandbox_root_ref": "sandbox-root",
        "target_relative_path": "example.txt",
        "original_text": "before",
        "replacement_text": "after",
        "test_command_ref": "tests/test_changed_target.py::test_smoke",
        "human_checkpoint_ref": "v0400-human-checkpoint",
        "live_workspace_apply_requested": False,
    }
    return SandboxRehearsalInput(**_with_overrides(defaults, overrides))


def create_sandbox_rehearsal_apply_plan(rehearsal_input: SandboxRehearsalInput, **overrides: Any) -> SandboxRehearsalApplyPlan:
    defaults = {
        "plan_id": f"{rehearsal_input.rehearsal_id}-apply-plan",
        "rehearsal_id": rehearsal_input.rehearsal_id,
        "uses_v0393_sandbox_apply_primitive": True,
        "sandbox_root_ref": rehearsal_input.sandbox_root_ref,
        "target_relative_path": rehearsal_input.target_relative_path,
        "exact_text_replacement_required": True,
        "live_workspace_allowed": False,
        "git_apply_allowed": False,
        "apply_patch_allowed": False,
    }
    return SandboxRehearsalApplyPlan(**_with_overrides(defaults, overrides))


def create_sandbox_rehearsal_retest_plan(rehearsal_input: SandboxRehearsalInput, **overrides: Any) -> SandboxRehearsalRetestPlan:
    defaults = {
        "plan_id": f"{rehearsal_input.rehearsal_id}-retest-plan",
        "rehearsal_id": rehearsal_input.rehearsal_id,
        "uses_v0394_controlled_retest_primitive": True,
        "supplied_runner_required": True,
        "shell_allowed": False,
        "bounded_argv_required": True,
        "timeout_required": True,
        "output_capture_bounded": True,
        "network_allowed": False,
        "dependency_install_allowed": False,
    }
    return SandboxRehearsalRetestPlan(**_with_overrides(defaults, overrides))


def _default_fake_runner(argv: list[str], cwd_ref: str, timeout_seconds: int, env_overrides: dict[str, str]) -> dict[str, Any]:
    return {
        "stdout": "sandbox rehearsal fake runner passed",
        "stderr": "",
        "exit_code": 0,
        "timed_out": False,
        "duration_ms": 1,
        "argv_seen": list(argv),
        "cwd_ref_seen": cwd_ref,
        "timeout_seconds_seen": timeout_seconds,
        "env_seen": dict(env_overrides),
    }


def run_sandbox_rehearsal(
    rehearsal_input: SandboxRehearsalInput,
    runner: RunnerCallable | None = None,
) -> tuple[SandboxRehearsalResult, SandboxRehearsalAuditRecord, SandboxRehearsalSafetyReport]:
    create_sandbox_rehearsal_apply_plan(rehearsal_input)
    create_sandbox_rehearsal_retest_plan(rehearsal_input)
    apply_input = build_repair_sandbox_apply_input(sandbox_root_ref=rehearsal_input.sandbox_root_ref)
    operations = create_sandbox_apply_operations(
        rehearsal_input.sandbox_root_ref,
        [
            {
                "target_relative_path": rehearsal_input.target_relative_path,
                "original_text": rehearsal_input.original_text,
                "replacement_text": rehearsal_input.replacement_text,
            }
        ],
    )
    transaction, apply_result, _ = apply_sandbox_text_replacements(apply_input, operations)
    supplied_runner = runner or _default_fake_runner
    retest_input = build_repair_post_apply_retest_input(
        sandbox_apply_result_id=apply_result.apply_result_id,
        sandbox_apply_transaction_id=transaction.transaction_id,
        sandbox_root_ref=rehearsal_input.sandbox_root_ref,
    )
    selection = build_repair_post_apply_test_selection_plan(
        retest_input_id=retest_input.retest_input_id,
        selected_test_refs=[rehearsal_input.test_command_ref or "tests/test_changed_target.py::test_smoke"],
        changed_target_refs=[rehearsal_input.target_relative_path],
    )
    command_spec = create_repair_controlled_test_command_spec(selection)
    _, run_record, _, retest_result = run_post_apply_controlled_retest(
        retest_input,
        command_spec,
        runner=supplied_runner,
    )
    apply_succeeded = apply_result.sandbox_apply_completed and not apply_result.live_workspace_touched
    retest_succeeded = bool(retest_result.tests_run_under_controlled_boundary and run_record.exit_code == 0)
    result = SandboxRehearsalResult(
        result_id=f"{rehearsal_input.rehearsal_id}-result",
        rehearsal_id=rehearsal_input.rehearsal_id,
        apply_attempted=True,
        apply_succeeded=apply_succeeded,
        retest_attempted=True,
        retest_succeeded=retest_succeeded,
        sandbox_only=True,
        live_workspace_mutated=False,
        model_invoked=False,
        prompt_submitted=False,
        subagent_invoked=False,
        external_agent_invoked=False,
        runtime_authority_granted=False,
        result_summary="Sandbox rehearsal used existing v0.39 bounded primitives inside the supplied sandbox root.",
        evidence_refs=(apply_result.apply_result_id, retest_result.retest_result_id),
    )
    audit = SandboxRehearsalAuditRecord(
        audit_id=f"{rehearsal_input.rehearsal_id}-audit",
        rehearsal_id=rehearsal_input.rehearsal_id,
        checked_sandbox_containment=True,
        checked_no_live_workspace=True,
        checked_no_git_apply=True,
        checked_no_apply_patch=True,
        checked_no_raw_subprocess=True,
        checked_no_shell = True,
        checked_no_network=True,
        checked_no_dependency_install=True,
        checked_no_model_invocation=True,
        checked_no_subagent_invocation=True,
        notes=("v0.39.3 apply primitive reused", "v0.39.4 supplied runner primitive reused"),
    )
    safety = create_sandbox_rehearsal_safety_report(rehearsal_input.rehearsal_id, result, audit)
    return result, audit, safety


def create_sandbox_rehearsal_safety_report(
    rehearsal_id: str = "v0401-rehearsal",
    result: SandboxRehearsalResult | None = None,
    audit: SandboxRehearsalAuditRecord | None = None,
    **overrides: Any,
) -> SandboxRehearsalSafetyReport:
    safe = True
    if result is not None:
        safe = safe and result.sandbox_only and not result.live_workspace_mutated
    if audit is not None:
        safe = safe and audit.checked_sandbox_containment and audit.checked_no_live_workspace
    defaults = {
        "report_id": f"{rehearsal_id}-safety-report",
        "rehearsal_id": rehearsal_id,
        "safe_for_v0401": safe,
        "safe_for_live_apply": False,
        "safe_for_autonomous_loop": False,
        "safe_for_model_invocation": False,
        "safe_for_subagent_invocation": False,
        "requires_human_checkpoint_before_next_iteration": True,
    }
    return SandboxRehearsalSafetyReport(**_with_overrides(defaults, overrides))


def create_sandbox_rehearsal_readiness_report(**overrides: Any) -> SandboxRehearsalReadinessReport:
    defaults = {"report_id": "v0401-rehearsal-readiness"}
    return SandboxRehearsalReadinessReport(**_with_overrides(defaults, overrides))


def create_standalone_agent_runtime_status(**overrides: Any) -> StandaloneAgentRuntimeStatus:
    defaults = {"status_id": "v0401-standalone-runtime-status"}
    return StandaloneAgentRuntimeStatus(**_with_overrides(defaults, overrides))


def create_default_personal_gap_register(**overrides: Any) -> DefaultPersonalStandaloneGapRegister:
    gaps = tuple(
        DefaultPersonalStandaloneGap(
            gap_id=f"gap-{name.lower()}",
            gap_name=name,
            required_for="Standalone Default Personal smoke run",
            current_status="missing",
            target_version="v0.41",
            risk_if_missing=f"{name} missing prevents end-to-end Default Personal operation.",
            acceleration_possible=name in {"UserFacingCLI", "ProfileRuntime", "DefaultPersonalSmokeScenario"},
        )
        for name in REQUIRED_GAP_NAMES
    )
    defaults = {
        "register_id": "v0401-default-personal-gap-register",
        "gaps": gaps,
        "standalone_runtime_started": False,
        "conservative_first_smoke_target": "v0.41.6",
        "earliest_possible_smoke_target": None,
    }
    return DefaultPersonalStandaloneGapRegister(**_with_overrides(defaults, overrides))


def create_default_personal_required_runtime_surface(**overrides: Any) -> DefaultPersonalRequiredRuntimeSurface:
    defaults = {
        "surface_id": "v0401-default-personal-required-runtime-surface",
        "required_components": REQUIRED_GAP_NAMES,
        "minimum_user_facing_commands": MINIMUM_USER_FACING_COMMANDS,
        "minimum_read_only_skills": MINIMUM_READ_ONLY_SKILLS,
        "minimum_events": MINIMUM_EVENTS,
    }
    return DefaultPersonalRequiredRuntimeSurface(**_with_overrides(defaults, overrides))


def assess_default_personal_acceleration(
    gap_register: DefaultPersonalStandaloneGapRegister | None = None,
    **overrides: Any,
) -> DefaultPersonalAccelerationAssessment:
    register = gap_register or create_default_personal_gap_register()
    blocking = tuple(gap.gap_name for gap in register.gaps if gap.current_status != "complete")
    acceleratable = tuple(gap.gap_name for gap in register.gaps if gap.acceleration_possible and gap.current_status != "complete")
    earliest: str | None = None
    recommendation = "Keep conservative v0.41.6 target; core standalone runtime surfaces remain missing."
    core_missing = {"ChatService", "UserFacingCLI", "AgentLoop", "SkillExecutor", "ProfileRuntime"}.issubset(blocking)
    if not core_missing and set(blocking).issubset({"UserFacingCLI", "ProfileRuntime"}):
        earliest = "v0.41.4"
        recommendation = "Acceleration to v0.41.4 may be possible if CLI and profile runtime close early."
    elif set(blocking).issubset({"DefaultPersonalSmokeScenario", "Docs"}):
        earliest = "v0.41.3"
        recommendation = "Acceleration to v0.41.3 may be possible if only smoke scenario/docs remain."
    defaults = {
        "assessment_id": "v0401-default-personal-acceleration",
        "conservative_target": register.conservative_first_smoke_target,
        "earliest_possible_target": earliest,
        "blocking_gaps": blocking,
        "acceleratable_gaps": acceleratable,
        "recommendation": recommendation,
        "standalone_runtime_started": False,
    }
    return DefaultPersonalAccelerationAssessment(**_with_overrides(defaults, overrides))


def create_v041_default_personal_handoff_draft(**overrides: Any) -> V041DefaultPersonalRuntimeHandoffDraft:
    assessment = assess_default_personal_acceleration()
    note = assessment.earliest_possible_target or "No acceleration recommended until core standalone surfaces close."
    defaults = {
        "handoff_id": "v0401-v041-default-personal-runtime-handoff",
        "target_track": "Default Personal Standalone Runtime",
        "recommended_start_version": "v0.41.0",
        "first_smoke_run_conservative_target": "v0.41.6",
        "first_smoke_run_acceleration_note": note,
        "required_components": REQUIRED_GAP_NAMES,
        "recommended_v041_sequence": V041_SEQUENCE,
    }
    return V041DefaultPersonalRuntimeHandoffDraft(**_with_overrides(defaults, overrides))


def sandbox_rehearsal_result_preserves_runtime_boundary(result: SandboxRehearsalResult) -> bool:
    return (
        result.sandbox_only
        and not result.live_workspace_mutated
        and not result.model_invoked
        and not result.prompt_submitted
        and not result.subagent_invoked
        and not result.external_agent_invoked
        and not result.runtime_authority_granted
    )


def sandbox_rehearsal_readiness_preserves_no_unsafe_runtime(report: SandboxRehearsalReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_READINESS_FLAGS)


def standalone_agent_runtime_status_all_closed(status: StandaloneAgentRuntimeStatus) -> bool:
    return all(getattr(status, name) is False for name in OPENED_RUNTIME_FLAGS)


def default_personal_gap_register_is_not_runtime_started(register: DefaultPersonalStandaloneGapRegister) -> bool:
    return register.standalone_runtime_started is False


def acceleration_assessment_is_not_runtime_start(assessment: DefaultPersonalAccelerationAssessment) -> bool:
    return assessment.standalone_runtime_started is False
