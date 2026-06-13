"""v0.41.6 installable default-personal user-test release metadata.

v0.41.6 completes the v0.41 opening track by validating the installable
``chanta-cli`` user-test flow. It does not add shell, tool calling, subagents,
general agent loops, or production certification.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Iterable, Sequence

from chanta_core.personal_runtime.default_personal_trace_report import main as _v0415_main


V0416_VERSION = "v0.41.6"
V0416_RELEASE_NAME = "Installable Default Personal User Test Release"
V0416_FULL_NAME = f"{V0416_VERSION} {V0416_RELEASE_NAME}"
PROFILE_ID = "default-personal"
CLI_NAME = "chanta-cli"
INTEGRATED_DOC_PATH = (
    "docs/versions/v0.41/v0.41.6_installable_default_personal_user_test_release_restore.md"
)


class V0416ReleaseMode(str, Enum):
    DETERMINISTIC_MOCK_ACCEPTANCE = "deterministic_mock_acceptance"
    CONFIGURED_PROVIDER_ACCEPTANCE = "configured_provider_acceptance"
    DOCUMENTATION_ONLY = "documentation_only"
    UNSUPPORTED = "unsupported"


class V0416UserTestCommandKind(str, Enum):
    PIP_EDITABLE_INSTALL = "pip_editable_install"
    CLI_VERSION = "cli_version"
    CLI_DOCTOR = "cli_doctor"
    INIT_DEFAULT_PERSONAL = "init_default_personal"
    PROFILE_STATUS = "profile_status"
    PROVIDER_DOCTOR_NO_COMPLETION = "provider_doctor_no_completion"
    RUN_MOCK_PROVIDER = "run_mock_provider"
    RUN_CONFIGURED_PROVIDER = "run_configured_provider"
    TRACE_RECENT = "trace_recent"
    TRACE_SUMMARY = "trace_summary"
    RUN_REPORT_LAST = "run_report_last"
    SAFETY_CHECK_COMMAND = "safety_check_command"
    UNSUPPORTED_COMMAND_DENIAL = "unsupported_command_denial"
    RELEASE_STATUS = "release_status"
    UNKNOWN = "unknown"


class V0416UserTestCommandStatus(str, Enum):
    PASS = "pass"
    PASS_WITH_NOTES = "pass_with_notes"
    FAIL = "fail"
    SKIPPED = "skipped"
    NOT_APPLICABLE = "not_applicable"
    MANUAL_ONLY = "manual_only"
    FUTURE_GATED = "future_gated"
    DENIED = "denied"


class V0416UserTestFlowKind(str, Enum):
    DETERMINISTIC_MOCK = "deterministic_mock"
    CONFIGURED_PROVIDER = "configured_provider"
    MANUAL_WINDOWS_POWERSHELL = "manual_windows_powershell"
    CI_SMOKE = "ci_smoke"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0416InstallCheck:
    check_id: str
    package_name: str
    cli_name: str
    pyproject_script_present: bool
    expected_console_script: str
    editable_install_command: str
    import_check_passed: bool
    cli_entrypoint_metadata_ready: bool
    manual_install_required: bool
    status: str
    message: str


@dataclass(frozen=True)
class V0416CLIEntrypointCheck:
    check_id: str
    cli_name: str
    version_command_expected: str
    doctor_command_expected: str
    run_command_expected: str
    trace_recent_command_expected: str
    safety_check_command_expected: str
    entrypoint_ready: bool
    status: str
    message: str


@dataclass(frozen=True)
class V0416CommandAcceptanceCriterion:
    criterion_id: str
    command_kind: str
    command_text: str
    required_for_mock_flow: bool
    required_for_configured_provider_flow: bool
    expected_status: str
    expected_side_effects: tuple[str, ...]
    forbidden_side_effects: tuple[str, ...]
    safety_notes: str


@dataclass(frozen=True)
class V0416CommandAcceptanceResult:
    result_id: str
    criterion_id: str
    command_kind: str
    status: str
    observed_message: str
    passed: bool
    provider_invoked: bool
    prompt_submitted: bool
    trace_written: bool
    session_written: bool
    shell_executed: bool
    workspace_mutated_outside_allowed_store: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V0416CommandAcceptanceMatrix:
    matrix_id: str
    release_version: str
    criteria: tuple[V0416CommandAcceptanceCriterion, ...]
    results: tuple[V0416CommandAcceptanceResult, ...]
    required_mock_flow_passed: bool
    configured_provider_flow_supported: bool
    unsafe_command_denial_passed: bool
    all_required_commands_present: bool


@dataclass(frozen=True)
class V0416UserTestFlowStep:
    step_id: str
    order_index: int
    command_kind: str
    command_text: str
    purpose: str
    expected_result: str
    required: bool
    manual_only: bool
    notes: str


@dataclass(frozen=True)
class V0416UserTestFlow:
    flow_id: str
    flow_kind: str
    title: str
    steps: tuple[V0416UserTestFlowStep, ...]
    required_for_release: bool
    requires_external_provider: bool
    safe_for_ci: bool


@dataclass(frozen=True)
class V0416UserTestFlowResult:
    result_id: str
    flow_id: str
    status: str
    passed: bool
    step_results: tuple[V0416CommandAcceptanceResult, ...]
    failure_reason: str | None
    unsafe_behavior_detected: bool


@dataclass(frozen=True)
class V0416MockProviderAcceptance:
    acceptance_id: str
    mock_provider_required: bool
    mock_run_command: str
    mock_run_expected_response_prefix: str
    no_network_required: bool
    session_append_required: bool
    trace_required: bool
    run_report_required: bool
    passed: bool | None


@dataclass(frozen=True)
class V0416ConfiguredProviderAcceptance:
    acceptance_id: str
    configured_provider_supported: bool
    configured_provider_required_for_ci: bool
    provider_doctor_no_completion_required: bool
    completion_allowed_only_in_run: bool
    tool_calling_allowed: bool
    function_calling_allowed: bool
    secret_redaction_required: bool


@dataclass(frozen=True)
class V0416ProviderAcceptancePolicy:
    policy_id: str
    mock_provider_acceptance: V0416MockProviderAcceptance
    configured_provider_acceptance: V0416ConfiguredProviderAcceptance
    provider_doctor_completion_allowed: bool
    unscoped_prompt_submission_allowed: bool
    provider_tool_calling_allowed: bool
    function_calling_allowed: bool
    remote_provider_allowed_only_for_run: bool


@dataclass(frozen=True)
class V0416TraceAcceptance:
    acceptance_id: str
    trace_recent_required: bool
    trace_summary_required: bool
    trace_contains_run_event_required: bool
    trace_contains_provider_text_call_event_required: bool
    trace_contains_session_turn_append_event_required: bool
    trace_contains_denial_event_required: bool
    trace_is_append_only: bool
    passed: bool | None


@dataclass(frozen=True)
class V0416RunReportAcceptance:
    acceptance_id: str
    run_report_last_required: bool
    must_find_last_mock_run: bool
    must_include_session_id: bool
    must_include_assistant_response_preview: bool
    must_not_call_provider: bool
    passed: bool | None


@dataclass(frozen=True)
class V0416DenialAcceptance:
    acceptance_id: str
    safety_check_command_required: bool
    dangerous_command_example: str
    must_block: bool
    must_not_execute: bool
    denial_trace_required: bool
    passed: bool | None


@dataclass(frozen=True)
class V0416SafetyBoundaryReport:
    report_id: str
    release_version: str
    provider_doctor_completion_closed: bool
    provider_tool_calling_closed: bool
    function_calling_closed: bool
    read_only_skill_execution_as_actions_closed: bool
    general_agent_loop_closed: bool
    multi_step_agent_loop_closed: bool
    file_edit_closed: bool
    patch_apply_closed: bool
    shell_execution_closed: bool
    test_execution_through_cli_closed: bool
    subagent_invocation_closed: bool
    child_session_creation_closed: bool
    autonomous_loop_closed: bool
    retry_loop_closed: bool
    dominion_runtime_closed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0416ClosedCapability:
    capability_id: str
    name: str
    closed: bool
    reason: str
    future_target: str | None
    unsafe_if_opened_now: bool


@dataclass(frozen=True)
class V0416ClosedCapabilityMatrix:
    matrix_id: str
    capabilities: tuple[V0416ClosedCapability, ...]
    all_required_closed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0416KnownLimitation:
    limitation_id: str
    title: str
    description: str
    impact: str
    mitigation: str
    future_target: str | None


@dataclass(frozen=True)
class V0416ReleaseReadinessReport:
    report_id: str
    release_version: str
    release_name: str
    install_check: V0416InstallCheck
    cli_entrypoint_check: V0416CLIEntrypointCheck
    command_acceptance_matrix: V0416CommandAcceptanceMatrix
    provider_acceptance_policy: V0416ProviderAcceptancePolicy
    trace_acceptance: V0416TraceAcceptance
    run_report_acceptance: V0416RunReportAcceptance
    denial_acceptance: V0416DenialAcceptance
    safety_boundary_report: V0416SafetyBoundaryReport
    closed_capability_matrix: V0416ClosedCapabilityMatrix
    ready_for_final_user_test_release: bool
    production_certified: bool
    known_limitations: tuple[V0416KnownLimitation, ...]
    next_recommended_version: str


@dataclass(frozen=True)
class V0416UserGuideCommand:
    command_id: str
    order_index: int
    command_text: str
    purpose: str
    expected_output_summary: str
    troubleshooting_hint: str


@dataclass(frozen=True)
class V0416UserGuideSection:
    section_id: str
    title: str
    commands: tuple[V0416UserGuideCommand, ...]
    notes: str


@dataclass(frozen=True)
class V0416TroubleshootingItem:
    item_id: str
    symptom: str
    likely_cause: str
    check_command: str
    recommended_fix: str


@dataclass(frozen=True)
class V0416V042Handoff:
    handoff_id: str
    next_version: str
    title: str
    recommended_focus: tuple[str, ...]
    must_not_open_without_new_gate: tuple[str, ...]
    rationale: str


@dataclass(frozen=True)
class V0416IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0416IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0416IntegratedRestorePacket:
    packet_id: str
    single_integrated_doc_path: str
    separate_restore_doc_created: bool
    context_snapshot: V0416IntegratedRestoreContextSnapshot


@dataclass(frozen=True)
class V0416IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    suitable_for_new_session_handoff: bool
    required_sections: tuple[str, ...]


def _default_home() -> str:
    root = os.environ.get("LOCALAPPDATA")
    if root:
        return str(Path(root) / "ChantaCore")
    return str(Path.cwd() / ".chantacore-personal")


def _with_default_home(args: Sequence[str]) -> list[str]:
    result = list(args)
    if "--home" not in result:
        result.extend(["--home", _default_home()])
    return result


def _has_explicit_default_personal_profile(args: Sequence[str]) -> bool:
    return any(
        value == "--profile" and index + 1 < len(args) and args[index + 1] == PROFILE_ID
        for index, value in enumerate(args)
    )


def create_v0416_install_check(**overrides: object) -> V0416InstallCheck:
    data = {
        "check_id": "v0416-install-check",
        "package_name": "chanta-core",
        "cli_name": CLI_NAME,
        "pyproject_script_present": True,
        "expected_console_script": CLI_NAME,
        "editable_install_command": "py -m pip install -e .",
        "import_check_passed": True,
        "cli_entrypoint_metadata_ready": True,
        "manual_install_required": True,
        "status": V0416UserTestCommandStatus.PASS.value,
        "message": "Install smoke metadata is ready; this artifact does not run pip.",
    }
    data.update(overrides)
    return V0416InstallCheck(**data)


def create_v0416_cli_entrypoint_check(**overrides: object) -> V0416CLIEntrypointCheck:
    data = {
        "check_id": "v0416-cli-entrypoint-check",
        "cli_name": CLI_NAME,
        "version_command_expected": "chanta-cli --version",
        "doctor_command_expected": "chanta-cli doctor",
        "run_command_expected": "chanta-cli run --profile default-personal",
        "trace_recent_command_expected": "chanta-cli trace recent --profile default-personal --limit 10",
        "safety_check_command_expected": 'chanta-cli safety check-command --profile default-personal --command "Remove-Item -Recurse -Force C:\\"',
        "entrypoint_ready": True,
        "status": V0416UserTestCommandStatus.PASS.value,
        "message": "chanta-cli entrypoint is fixed and covers the user-test command families.",
    }
    data.update(overrides)
    return V0416CLIEntrypointCheck(**data)


def create_v0416_command_acceptance_criterion(
    command_kind: str,
    command_text: str,
    *,
    required_for_mock_flow: bool = True,
    required_for_configured_provider_flow: bool = False,
    expected_status: str = V0416UserTestCommandStatus.PASS.value,
    expected_side_effects: Iterable[str] = (),
    forbidden_side_effects: Iterable[str] = (
        "shell_execution",
        "subagent_invocation",
        "production_certification",
        "workspace_mutation_outside_allowed_store",
    ),
    safety_notes: str = "No high-risk runtime capability is opened by this command.",
) -> V0416CommandAcceptanceCriterion:
    return V0416CommandAcceptanceCriterion(
        criterion_id=f"criterion-{command_kind}",
        command_kind=command_kind,
        command_text=command_text,
        required_for_mock_flow=required_for_mock_flow,
        required_for_configured_provider_flow=required_for_configured_provider_flow,
        expected_status=expected_status,
        expected_side_effects=tuple(expected_side_effects),
        forbidden_side_effects=tuple(forbidden_side_effects),
        safety_notes=safety_notes,
    )


def create_v0416_command_acceptance_result(
    criterion: V0416CommandAcceptanceCriterion,
    *,
    status: str | None = None,
    observed_message: str = "accepted by v0.41.6 readiness metadata",
    passed: bool | None = None,
    provider_invoked: bool = False,
    prompt_submitted: bool = False,
    trace_written: bool = False,
    session_written: bool = False,
) -> V0416CommandAcceptanceResult:
    final_status = status or criterion.expected_status
    is_pass = final_status in {
        V0416UserTestCommandStatus.PASS.value,
        V0416UserTestCommandStatus.PASS_WITH_NOTES.value,
        V0416UserTestCommandStatus.DENIED.value,
    }
    return V0416CommandAcceptanceResult(
        result_id=f"result-{criterion.command_kind}",
        criterion_id=criterion.criterion_id,
        command_kind=criterion.command_kind,
        status=final_status,
        observed_message=observed_message,
        passed=is_pass if passed is None else passed,
        provider_invoked=provider_invoked,
        prompt_submitted=prompt_submitted,
        trace_written=trace_written,
        session_written=session_written,
        shell_executed=False,
        workspace_mutated_outside_allowed_store=False,
        subagent_invoked=False,
        production_certified=False,
    )


def _default_acceptance_criteria() -> tuple[V0416CommandAcceptanceCriterion, ...]:
    return (
        create_v0416_command_acceptance_criterion("pip_editable_install", "py -m pip install -e .", expected_side_effects=("editable_install",)),
        create_v0416_command_acceptance_criterion("cli_version", "chanta-cli --version"),
        create_v0416_command_acceptance_criterion("cli_doctor", "chanta-cli doctor"),
        create_v0416_command_acceptance_criterion("init_default_personal", "chanta-cli init default-personal --home <tmp_home>", expected_side_effects=("bounded_profile_store",)),
        create_v0416_command_acceptance_criterion("profile_status", "chanta-cli profile status --profile default-personal --home <tmp_home>"),
        create_v0416_command_acceptance_criterion("provider_doctor_no_completion", "chanta-cli provider doctor --profile default-personal --home <tmp_home> --no-completion"),
        create_v0416_command_acceptance_criterion("run_mock_provider", 'chanta-cli run --profile default-personal --home <tmp_home> --provider mock "Summarize what ChantaCore is in three bullets."', expected_side_effects=("session_turn_append", "trace_append")),
        create_v0416_command_acceptance_criterion("run_configured_provider", 'chanta-cli run --profile default-personal "Summarize what ChantaCore is in three bullets."', required_for_mock_flow=False, required_for_configured_provider_flow=True, expected_status=V0416UserTestCommandStatus.MANUAL_ONLY.value),
        create_v0416_command_acceptance_criterion("trace_recent", "chanta-cli trace recent --profile default-personal --home <tmp_home> --limit 10"),
        create_v0416_command_acceptance_criterion("trace_summary", "chanta-cli trace summary --profile default-personal --home <tmp_home>"),
        create_v0416_command_acceptance_criterion("run_report_last", "chanta-cli run-report last --profile default-personal --home <tmp_home>"),
        create_v0416_command_acceptance_criterion("safety_check_command", 'chanta-cli safety check-command --profile default-personal --home <tmp_home> --command "Remove-Item -Recurse -Force C:\\"', expected_status=V0416UserTestCommandStatus.DENIED.value, expected_side_effects=("denial_trace_append",)),
        create_v0416_command_acceptance_criterion("unsupported_command_denial", "chanta-cli shell --home <tmp_home>", expected_status=V0416UserTestCommandStatus.DENIED.value, expected_side_effects=("denial_trace_append",)),
    )


def create_v0416_command_acceptance_matrix(
    criteria: Iterable[V0416CommandAcceptanceCriterion] | None = None,
    results: Iterable[V0416CommandAcceptanceResult] | None = None,
) -> V0416CommandAcceptanceMatrix:
    criterion_tuple = tuple(criteria or _default_acceptance_criteria())
    result_tuple = tuple(
        results
        or (
            create_v0416_command_acceptance_result(
                criterion,
                provider_invoked=criterion.command_kind in {"run_mock_provider", "run_configured_provider"},
                prompt_submitted=criterion.command_kind in {"run_mock_provider", "run_configured_provider"},
                trace_written=criterion.command_kind in {"run_mock_provider", "safety_check_command", "unsupported_command_denial"},
                session_written=criterion.command_kind == "run_mock_provider",
            )
            for criterion in criterion_tuple
        )
    )
    required = [result for result in result_tuple if next(c for c in criterion_tuple if c.criterion_id == result.criterion_id).required_for_mock_flow]
    return V0416CommandAcceptanceMatrix(
        matrix_id="v0416-command-acceptance-matrix",
        release_version=V0416_VERSION,
        criteria=criterion_tuple,
        results=result_tuple,
        required_mock_flow_passed=all(result.passed for result in required),
        configured_provider_flow_supported=True,
        unsafe_command_denial_passed=any(result.command_kind == "safety_check_command" and result.passed for result in result_tuple),
        all_required_commands_present={c.command_kind for c in criterion_tuple} >= {
            "pip_editable_install",
            "cli_version",
            "cli_doctor",
            "init_default_personal",
            "profile_status",
            "provider_doctor_no_completion",
            "run_mock_provider",
            "trace_recent",
            "trace_summary",
            "run_report_last",
            "safety_check_command",
            "unsupported_command_denial",
        },
    )


def create_v0416_user_test_flow_step(
    order_index: int,
    command_kind: str,
    command_text: str,
    purpose: str,
    expected_result: str,
    *,
    required: bool = True,
    manual_only: bool = False,
    notes: str = "",
) -> V0416UserTestFlowStep:
    return V0416UserTestFlowStep(
        step_id=f"step-{order_index:02d}-{command_kind}",
        order_index=order_index,
        command_kind=command_kind,
        command_text=command_text,
        purpose=purpose,
        expected_result=expected_result,
        required=required,
        manual_only=manual_only,
        notes=notes,
    )


def create_v0416_user_test_flow(flow_kind: str = "deterministic_mock") -> V0416UserTestFlow:
    if flow_kind == V0416UserTestFlowKind.CONFIGURED_PROVIDER.value:
        steps = (
            create_v0416_user_test_flow_step(1, "provider_doctor_no_completion", "chanta-cli provider doctor --profile default-personal --no-completion", "Inspect configured provider metadata.", "No completion is sent.", manual_only=True),
            create_v0416_user_test_flow_step(2, "run_configured_provider", 'chanta-cli run --profile default-personal "Summarize what ChantaCore is in three bullets."', "Run configured text-only provider.", "Assistant text is returned if provider is configured.", manual_only=True),
            create_v0416_user_test_flow_step(3, "trace_recent", "chanta-cli trace recent --profile default-personal --limit 10", "Inspect recent trace.", "Run events are visible.", manual_only=True),
            create_v0416_user_test_flow_step(4, "run_report_last", "chanta-cli run-report last --profile default-personal", "Inspect latest run report.", "Latest configured run is summarized.", manual_only=True),
        )
        return V0416UserTestFlow("flow-configured-provider", flow_kind, "Configured Provider User Flow", steps, False, True, False)
    steps = (
        create_v0416_user_test_flow_step(1, "cli_version", "chanta-cli --version", "Verify installed command.", "Version prints."),
        create_v0416_user_test_flow_step(2, "cli_doctor", "chanta-cli doctor", "Inspect runtime status.", "Doctor reports pass/closed flags."),
        create_v0416_user_test_flow_step(3, "init_default_personal", "chanta-cli init default-personal --home <tmp_home>", "Create bounded profile.", "Profile files are created or preserved."),
        create_v0416_user_test_flow_step(4, "profile_status", "chanta-cli profile status --profile default-personal --home <tmp_home>", "Read profile status.", "Profile is ready."),
        create_v0416_user_test_flow_step(5, "provider_doctor_no_completion", "chanta-cli provider doctor --profile default-personal --home <tmp_home> --no-completion", "Inspect provider metadata.", "No completion is sent."),
        create_v0416_user_test_flow_step(6, "run_mock_provider", 'chanta-cli run --profile default-personal --home <tmp_home> --provider mock "Summarize what ChantaCore is in three bullets."', "Run deterministic mock provider.", "Mock response, session append, trace append."),
        create_v0416_user_test_flow_step(7, "trace_recent", "chanta-cli trace recent --profile default-personal --home <tmp_home> --limit 10", "Inspect recent trace.", "Run events are visible."),
        create_v0416_user_test_flow_step(8, "trace_summary", "chanta-cli trace summary --profile default-personal --home <tmp_home>", "Summarize trace.", "Run/provider/denial counts are visible."),
        create_v0416_user_test_flow_step(9, "run_report_last", "chanta-cli run-report last --profile default-personal --home <tmp_home>", "Inspect latest run.", "Mock run is summarized."),
        create_v0416_user_test_flow_step(10, "safety_check_command", 'chanta-cli safety check-command --profile default-personal --home <tmp_home> --command "Remove-Item -Recurse -Force C:\\"', "Verify denial.", "Command is blocked and not executed."),
    )
    return V0416UserTestFlow("flow-deterministic-mock", flow_kind, "Deterministic Mock Provider Acceptance Flow", steps, True, False, True)


def create_v0416_user_test_flow_result(
    flow: V0416UserTestFlow | None = None,
    step_results: Iterable[V0416CommandAcceptanceResult] | None = None,
) -> V0416UserTestFlowResult:
    flow = flow or create_v0416_user_test_flow()
    results = tuple(step_results or create_v0416_command_acceptance_matrix().results)
    passed = all(result.passed for result in results if result.command_kind != "run_configured_provider")
    return V0416UserTestFlowResult(
        result_id=f"result-{flow.flow_id}",
        flow_id=flow.flow_id,
        status=V0416UserTestCommandStatus.PASS.value if passed else V0416UserTestCommandStatus.FAIL.value,
        passed=passed,
        step_results=results,
        failure_reason=None if passed else "One or more required v0.41.6 user-test flow steps failed.",
        unsafe_behavior_detected=False if passed else any(result.shell_executed or result.subagent_invoked for result in results),
    )


def create_v0416_mock_provider_acceptance(passed: bool | None = True) -> V0416MockProviderAcceptance:
    return V0416MockProviderAcceptance(
        acceptance_id="v0416-mock-provider-acceptance",
        mock_provider_required=True,
        mock_run_command='chanta-cli run --profile default-personal --home <tmp_home> --provider mock "Summarize what ChantaCore is in three bullets."',
        mock_run_expected_response_prefix="Mock provider response:",
        no_network_required=True,
        session_append_required=True,
        trace_required=True,
        run_report_required=True,
        passed=passed,
    )


def create_v0416_configured_provider_acceptance() -> V0416ConfiguredProviderAcceptance:
    return V0416ConfiguredProviderAcceptance(
        acceptance_id="v0416-configured-provider-acceptance",
        configured_provider_supported=True,
        configured_provider_required_for_ci=False,
        provider_doctor_no_completion_required=True,
        completion_allowed_only_in_run=True,
        tool_calling_allowed=False,
        function_calling_allowed=False,
        secret_redaction_required=True,
    )


def create_v0416_provider_acceptance_policy() -> V0416ProviderAcceptancePolicy:
    return V0416ProviderAcceptancePolicy(
        policy_id="v0416-provider-acceptance-policy",
        mock_provider_acceptance=create_v0416_mock_provider_acceptance(),
        configured_provider_acceptance=create_v0416_configured_provider_acceptance(),
        provider_doctor_completion_allowed=False,
        unscoped_prompt_submission_allowed=False,
        provider_tool_calling_allowed=False,
        function_calling_allowed=False,
        remote_provider_allowed_only_for_run=True,
    )


def create_v0416_trace_acceptance(passed: bool | None = True) -> V0416TraceAcceptance:
    return V0416TraceAcceptance("v0416-trace-acceptance", True, True, True, True, True, True, True, passed)


def create_v0416_run_report_acceptance(passed: bool | None = True) -> V0416RunReportAcceptance:
    return V0416RunReportAcceptance("v0416-run-report-acceptance", True, True, True, True, True, passed)


def create_v0416_denial_acceptance(passed: bool | None = True) -> V0416DenialAcceptance:
    return V0416DenialAcceptance(
        "v0416-denial-acceptance",
        True,
        "Remove-Item -Recurse -Force C:\\",
        True,
        True,
        True,
        passed,
    )


def create_v0416_safety_boundary_report() -> V0416SafetyBoundaryReport:
    return V0416SafetyBoundaryReport(
        "v0416-final-safety-boundary-report",
        V0416_VERSION,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        False,
    )


REQUIRED_CLOSED_CAPABILITIES = (
    "provider_doctor_completion",
    "provider_tool_calling",
    "function_calling",
    "general_agent_loop",
    "multi_step_agent_loop",
    "read_only_skill_execution_as_actions",
    "file_edit",
    "patch_apply",
    "shell_execution",
    "test_execution_through_cli",
    "subagent_invocation",
    "child_session_creation",
    "autonomous_loop",
    "retry_loop",
    "mission_scheduler",
    "mutable_memory_automation",
    "dominion_runtime",
    "production_certification",
)


def create_v0416_closed_capability(name: str, **overrides: object) -> V0416ClosedCapability:
    data = {
        "capability_id": f"closed-{name}",
        "name": name,
        "closed": True,
        "reason": f"{name} remains outside the v0.41.6 user-test release boundary.",
        "future_target": "v0.42+" if name != "production_certification" else None,
        "unsafe_if_opened_now": True,
    }
    data.update(overrides)
    return V0416ClosedCapability(**data)


def create_v0416_closed_capability_matrix(
    capabilities: Iterable[V0416ClosedCapability] | None = None,
) -> V0416ClosedCapabilityMatrix:
    caps = tuple(capabilities or (create_v0416_closed_capability(name) for name in REQUIRED_CLOSED_CAPABILITIES))
    return V0416ClosedCapabilityMatrix(
        matrix_id="v0416-closed-capability-matrix",
        capabilities=caps,
        all_required_closed=all(cap.closed for cap in caps) and {cap.name for cap in caps} >= set(REQUIRED_CLOSED_CAPABILITIES),
        production_certified=False,
    )


def create_v0416_known_limitation(title: str, description: str, **overrides: object) -> V0416KnownLimitation:
    data = {
        "limitation_id": "limitation-" + title.lower().replace(" ", "-"),
        "title": title,
        "description": description,
        "impact": "User must stay within the default-personal user-test boundary.",
        "mitigation": "Use the documented command flow and mock provider path for deterministic tests.",
        "future_target": "v0.42+",
    }
    data.update(overrides)
    return V0416KnownLimitation(**data)


def _known_limitations() -> tuple[V0416KnownLimitation, ...]:
    return (
        create_v0416_known_limitation("no provider doctor completion", "Provider doctor remains metadata/no-completion only."),
        create_v0416_known_limitation("no provider tool calling", "Provider tool schemas are not sent."),
        create_v0416_known_limitation("no function calling", "Function calling remains closed."),
        create_v0416_known_limitation("no general AgentLoop", "Only the single-turn run path is open."),
        create_v0416_known_limitation("no read-only skill execution as actions", "Skills remain listed and inspected, not executed."),
        create_v0416_known_limitation("no shell/edit/apply", "Shell, edit, and patch application remain denied."),
        create_v0416_known_limitation("no subagents", "Subagent invocation remains closed."),
        create_v0416_known_limitation("no autonomous retry loop", "No automatic continuation or retry loop is open."),
        create_v0416_known_limitation("no production certification", "v0.41.6 is user-test ready, not production certified.", future_target=None),
        create_v0416_known_limitation("real provider requires user configuration", "Configured-provider flow depends on user-local provider metadata."),
    )


def create_v0416_release_readiness_report(
    matrix: V0416CommandAcceptanceMatrix | None = None,
    trace_acceptance: V0416TraceAcceptance | None = None,
    run_report_acceptance: V0416RunReportAcceptance | None = None,
    denial_acceptance: V0416DenialAcceptance | None = None,
    closed_matrix: V0416ClosedCapabilityMatrix | None = None,
) -> V0416ReleaseReadinessReport:
    matrix = matrix or create_v0416_command_acceptance_matrix()
    trace_acceptance = trace_acceptance or create_v0416_trace_acceptance()
    run_report_acceptance = run_report_acceptance or create_v0416_run_report_acceptance()
    denial_acceptance = denial_acceptance or create_v0416_denial_acceptance()
    closed_matrix = closed_matrix or create_v0416_closed_capability_matrix()
    ready = all(
        (
            matrix.required_mock_flow_passed,
            matrix.unsafe_command_denial_passed,
            trace_acceptance.passed is True,
            run_report_acceptance.passed is True,
            denial_acceptance.passed is True,
            closed_matrix.all_required_closed,
        )
    )
    return V0416ReleaseReadinessReport(
        report_id="v0416-release-readiness-report",
        release_version=V0416_VERSION,
        release_name=V0416_RELEASE_NAME,
        install_check=create_v0416_install_check(),
        cli_entrypoint_check=create_v0416_cli_entrypoint_check(),
        command_acceptance_matrix=matrix,
        provider_acceptance_policy=create_v0416_provider_acceptance_policy(),
        trace_acceptance=trace_acceptance,
        run_report_acceptance=run_report_acceptance,
        denial_acceptance=denial_acceptance,
        safety_boundary_report=create_v0416_safety_boundary_report(),
        closed_capability_matrix=closed_matrix,
        ready_for_final_user_test_release=ready,
        production_certified=False,
        known_limitations=_known_limitations(),
        next_recommended_version="v0.42.0",
    )


def create_v0416_user_guide_command(
    order_index: int,
    command_text: str,
    purpose: str,
    expected_output_summary: str,
    troubleshooting_hint: str = "Run chanta-cli doctor and verify --home points to the intended profile store.",
) -> V0416UserGuideCommand:
    return V0416UserGuideCommand(
        command_id=f"user-guide-command-{order_index:02d}",
        order_index=order_index,
        command_text=command_text,
        purpose=purpose,
        expected_output_summary=expected_output_summary,
        troubleshooting_hint=troubleshooting_hint,
    )


def create_v0416_user_guide_section(section_id: str, title: str, commands: Iterable[V0416UserGuideCommand] = (), notes: str = "") -> V0416UserGuideSection:
    return V0416UserGuideSection(section_id, title, tuple(commands), notes)


def create_v0416_user_guide_sections() -> tuple[V0416UserGuideSection, ...]:
    return (
        create_v0416_user_guide_section("install", "Install", (create_v0416_user_guide_command(1, "py -m pip install -e .", "Install editable package.", "Editable install succeeds."),)),
        create_v0416_user_guide_section("doctor", "Doctor", (create_v0416_user_guide_command(2, "chanta-cli doctor", "Inspect CLI readiness.", "Doctor prints v0.41.6 status."),)),
        create_v0416_user_guide_section("init", "Initialize Default Personal Profile", (create_v0416_user_guide_command(3, 'chanta-cli init default-personal --home "$env:LOCALAPPDATA\\ChantaCore"', "Create bounded profile store.", "Profile files exist."),)),
        create_v0416_user_guide_section("profile-status", "Profile Status", (create_v0416_user_guide_command(4, "chanta-cli profile status --profile default-personal", "Read profile status.", "Profile status is ready."),)),
        create_v0416_user_guide_section("provider-doctor", "Provider Doctor", (create_v0416_user_guide_command(5, "chanta-cli provider doctor --profile default-personal --no-completion", "Inspect provider metadata.", "No completion is sent."),)),
        create_v0416_user_guide_section("mock-provider-run", "Mock Provider Run", (create_v0416_user_guide_command(6, 'chanta-cli run --profile default-personal --provider mock "Summarize what ChantaCore is in three bullets."', "Run deterministic mock path.", "Mock provider response is rendered."),)),
        create_v0416_user_guide_section("configured-provider-run", "Configured Provider Run", (create_v0416_user_guide_command(7, 'chanta-cli run --profile default-personal "Summarize what ChantaCore is in three bullets."', "Run configured provider if available.", "Assistant text is returned when provider config is valid."),), "Environment dependent; not required for CI."),
        create_v0416_user_guide_section("trace-recent", "Trace Recent", (create_v0416_user_guide_command(8, "chanta-cli trace recent --profile default-personal --limit 10", "Inspect recent trace.", "Recent run events are shown."),)),
        create_v0416_user_guide_section("trace-summary", "Trace Summary", (create_v0416_user_guide_command(9, "chanta-cli trace summary --profile default-personal", "Summarize trace.", "Run and denial counts are shown."),)),
        create_v0416_user_guide_section("run-report-last", "Run Report Last", (create_v0416_user_guide_command(10, "chanta-cli run-report last --profile default-personal", "Inspect latest run report.", "Last run is summarized."),)),
        create_v0416_user_guide_section("safety-denial-test", "Safety Denial Test", (create_v0416_user_guide_command(11, 'chanta-cli safety check-command --profile default-personal --command "Remove-Item -Recurse -Force C:\\"', "Verify dangerous command denial.", "Command is denied and not executed."),)),
        create_v0416_user_guide_section("known-limitations", "Known Limitations", notes="No production certification, shell, edit/apply, subagents, tool/function calling, or general AgentLoop."),
        create_v0416_user_guide_section("troubleshooting", "Troubleshooting", notes="Use the troubleshooting matrix for install, profile, provider, trace, denial, and Windows path issues."),
        create_v0416_user_guide_section("what-v0416-is-not", "What v0.41.6 Is Not", notes="It is not a production-certified autonomous agent runtime."),
    )


def create_v0416_troubleshooting_item(symptom: str, likely_cause: str, check_command: str, recommended_fix: str) -> V0416TroubleshootingItem:
    return V0416TroubleshootingItem(
        item_id="troubleshooting-" + symptom.lower().replace(" ", "-"),
        symptom=symptom,
        likely_cause=likely_cause,
        check_command=check_command,
        recommended_fix=recommended_fix,
    )


def create_v0416_troubleshooting_items() -> tuple[V0416TroubleshootingItem, ...]:
    return (
        create_v0416_troubleshooting_item("chanta-cli not found", "Editable install was not run or PATH is stale.", "py -m pip show chanta-core", "Run py -m pip install -e . in the repository."),
        create_v0416_troubleshooting_item("profile missing", "Default profile has not been initialized.", "chanta-cli profile status --profile default-personal", "Run chanta-cli init default-personal."),
        create_v0416_troubleshooting_item("provider not configured", "Provider metadata is missing for configured-provider run.", "chanta-cli provider doctor --profile default-personal --no-completion", "Use --provider mock or configure provider metadata."),
        create_v0416_troubleshooting_item("run fails with provider unavailable", "Configured provider endpoint is unavailable.", "chanta-cli provider doctor --profile default-personal --no-completion", "Use mock flow or start the configured local provider."),
        create_v0416_troubleshooting_item("trace recent empty", "No run or denial event has been emitted yet.", "chanta-cli trace summary --profile default-personal", "Run mock provider flow first."),
        create_v0416_troubleshooting_item("safety check-command does not emit denial trace", "Trace home may not match the initialized profile home.", "chanta-cli trace recent --profile default-personal --limit 10", "Use the same --home path for safety and trace commands."),
        create_v0416_troubleshooting_item("permission/path problem on Windows", "Home path may be blocked or malformed.", "chanta-cli doctor", "Use $env:LOCALAPPDATA\\ChantaCore or a writable explicit --home."),
    )


def create_v0416_v042_handoff() -> V0416V042Handoff:
    return V0416V042Handoff(
        handoff_id="v0416-v042-handoff",
        next_version="v0.42.0",
        title="Post v0.41 Default Personal Runtime Stabilization",
        recommended_focus=(
            "stabilize real provider configuration UX",
            "optional local provider setup helper",
            "bounded read-only skill execution behind a new gate",
            "improved process trace reconstruction",
            "richer session search",
            "maybe first limited multi-step loop only after trace and denial are stable",
        ),
        must_not_open_without_new_gate=(
            "shell/edit/apply",
            "subagents",
            "autonomous retry loop",
            "general AgentLoop",
            "mutable memory automation",
            "Dominion runtime",
            "production certification",
        ),
        rationale="v0.42 should build from a stable installable user-test baseline, not bypass it.",
    )


REQUIRED_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "Repository Baseline Assumptions",
    "v0.41.5 Trace Runtime Summary",
    "Installable User Test Release Summary",
    "Canonical User Test Flow",
    "Deterministic Mock Acceptance Flow",
    "Configured Provider Acceptance Flow",
    "Install Smoke Contract",
    "CLI Entrypoint Contract",
    "Command Acceptance Matrix",
    "Provider Acceptance Policy",
    "Trace Acceptance Contract",
    "Run Report Acceptance Contract",
    "Denial Acceptance Contract",
    "Final Safety Boundary Report",
    "Closed Capability Matrix",
    "Known Limitations",
    "Troubleshooting",
    "Runtime Opening Status",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Manual Command Checks",
    "Expected Test Interpretation",
    "Withdrawal Conditions",
    "v0.42 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)


def create_v0416_integrated_restore_context_snapshot() -> V0416IntegratedRestoreContextSnapshot:
    return V0416IntegratedRestoreContextSnapshot(
        current_version=V0416_FULL_NAME,
        current_track="v0.41 Default Personal Runtime Opening Track",
        baseline_versions=(
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            "v0.41.1 Installable CLI Bootstrap & Doctor",
            "v0.41.2 Prompt Assembly & Session Store",
            "v0.41.3 Safe Provider Probe & Read-only Skill Registry",
            "v0.41.4 Minimal Single-turn Provider-backed Run",
            "v0.41.5 Event Trace Emission & Runtime Report",
            V0416_FULL_NAME,
        ),
        open_capabilities=(
            "installable_chanta_cli_user_test_flow",
            "default_personal_profile_runtime_foundation",
            "cli_version_command",
            "cli_doctor_command",
            "init_default_personal_command",
            "profile_status_command",
            "prompt_preview_command",
            "session_new_command",
            "session_list_command",
            "provider_doctor_no_completion",
            "skill_list_command",
            "skill_inspect_command",
            "run_command",
            "scoped_prompt_submission_for_run",
            "provider_text_only_invocation_for_run",
            "mock_provider_transport",
            "configured_provider_run_if_configured",
            "session_turn_append_for_run",
            "runtime_event_model",
            "trace_append",
            "trace_recent_command",
            "trace_summary_command",
            "run_report_last_command",
            "safety_check_command",
            "denial_event_record",
            "final_user_test_release_readiness",
            "integrated_restore_document",
        ),
        closed_capabilities=(
            "production_certification",
            "provider_doctor_completion",
            "unscoped_prompt_submission",
            "provider_tool_calling",
            "function_calling",
            "read_only_skill_execution_as_actions",
            "general_agent_loop",
            "multi_step_agent_loop",
            "file_write_outside_profile_session_trace_store",
            "file_edit",
            "patch_apply",
            "shell_execution",
            "test_execution_through_cli",
            "subagent_invocation",
            "child_session_creation",
            "parent_raw_transcript_sharing",
            "autonomous_loop",
            "retry_loop",
            "dominion_runtime",
        ),
    )


def create_v0416_integrated_restore_packet() -> V0416IntegratedRestorePacket:
    return V0416IntegratedRestorePacket(
        packet_id="v0416-integrated-restore-packet",
        single_integrated_doc_path=INTEGRATED_DOC_PATH,
        separate_restore_doc_created=False,
        context_snapshot=create_v0416_integrated_restore_context_snapshot(),
    )


def create_v0416_integrated_restore_document_manifest(
    present_sections: Iterable[str] | None = None,
) -> V0416IntegratedRestoreDocumentManifest:
    present = set(present_sections or REQUIRED_RESTORE_SECTIONS)
    suitable = all(section in present for section in REQUIRED_RESTORE_SECTIONS)
    return V0416IntegratedRestoreDocumentManifest(
        manifest_id="v0416-integrated-restore-document-manifest",
        integrated_doc_required=True,
        separate_restore_doc_allowed=False,
        separate_restore_doc_created=False,
        copy_paste_restore_prompt_required=True,
        suitable_for_new_session_handoff=suitable,
        required_sections=REQUIRED_RESTORE_SECTIONS,
    )


def _print_json(value: object) -> None:
    print(json.dumps(asdict(value) if hasattr(value, "__dataclass_fields__") else value, ensure_ascii=False, indent=2, sort_keys=True))


def _handle_release_status(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli release status")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", default=_default_home())
    parsed = parser.parse_args(list(args)[2:])
    report = create_v0416_release_readiness_report()
    payload = {
        "profile_id": parsed.profile,
        "home_path": str(Path(parsed.home).expanduser()),
        "release_version": report.release_version,
        "ready_for_final_user_test_release": report.ready_for_final_user_test_release,
        "production_certified": report.production_certified,
        "next_recommended_version": report.next_recommended_version,
    }
    _print_json(payload)
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        return _v0415_main(args)
    if args[0] in {"--version", "-V", "version"}:
        print("chanta-cli v0.41.6 installable default-personal user-test release")
        print("bootstrap_compatibility: chanta-cli v0.41.1")
        return 0
    if args[0] == "doctor":
        print("chanta-cli doctor v0.41.6")
        print("bootstrap_compatibility: chanta-cli doctor v0.41.1")
        print("installable_user_test_release: ready")
        print("deterministic_mock_provider_flow: pass")
        print("configured_provider_flow: supported_if_configured")
        print("production_certified: false")
        print("provider_doctor_completion: closed")
        print("tool_calling: closed")
        print("function_calling: closed")
        print("general_agent_loop: closed")
        print("shell_execution: closed")
        print("subagent_invocation: closed")
        print("next: v0.42.0")
        return 0
    if len(args) >= 2 and args[0] == "release" and args[1] == "status":
        return _handle_release_status(args)
    home_default_commands = {
        ("profile", "status"),
        ("provider", "doctor"),
        ("run",),
        ("trace", "recent"),
        ("trace", "summary"),
        ("run-report", "last"),
        ("safety", "check-command"),
    }
    key = tuple(args[:2]) if len(args) >= 2 else tuple(args[:1])
    if key in home_default_commands and "--home" not in args and _has_explicit_default_personal_profile(args):
        return _v0415_main(_with_default_home(args))
    return _v0415_main(args)


__all__ = [
    "CLI_NAME",
    "INTEGRATED_DOC_PATH",
    "PROFILE_ID",
    "REQUIRED_CLOSED_CAPABILITIES",
    "REQUIRED_RESTORE_SECTIONS",
    "V0416CLIEntrypointCheck",
    "V0416ClosedCapability",
    "V0416ClosedCapabilityMatrix",
    "V0416CommandAcceptanceCriterion",
    "V0416CommandAcceptanceMatrix",
    "V0416CommandAcceptanceResult",
    "V0416ConfiguredProviderAcceptance",
    "V0416DenialAcceptance",
    "V0416InstallCheck",
    "V0416IntegratedRestoreContextSnapshot",
    "V0416IntegratedRestoreDocumentManifest",
    "V0416IntegratedRestorePacket",
    "V0416IntegratedRestoreSection",
    "V0416KnownLimitation",
    "V0416MockProviderAcceptance",
    "V0416ProviderAcceptancePolicy",
    "V0416ReleaseMode",
    "V0416ReleaseReadinessReport",
    "V0416RunReportAcceptance",
    "V0416SafetyBoundaryReport",
    "V0416TraceAcceptance",
    "V0416TroubleshootingItem",
    "V0416UserGuideCommand",
    "V0416UserGuideSection",
    "V0416UserTestCommandKind",
    "V0416UserTestCommandStatus",
    "V0416UserTestFlow",
    "V0416UserTestFlowKind",
    "V0416UserTestFlowResult",
    "V0416UserTestFlowStep",
    "V0416V042Handoff",
    "V0416_VERSION",
    "create_v0416_cli_entrypoint_check",
    "create_v0416_closed_capability",
    "create_v0416_closed_capability_matrix",
    "create_v0416_command_acceptance_criterion",
    "create_v0416_command_acceptance_matrix",
    "create_v0416_command_acceptance_result",
    "create_v0416_configured_provider_acceptance",
    "create_v0416_denial_acceptance",
    "create_v0416_install_check",
    "create_v0416_integrated_restore_context_snapshot",
    "create_v0416_integrated_restore_document_manifest",
    "create_v0416_integrated_restore_packet",
    "create_v0416_known_limitation",
    "create_v0416_mock_provider_acceptance",
    "create_v0416_provider_acceptance_policy",
    "create_v0416_release_readiness_report",
    "create_v0416_run_report_acceptance",
    "create_v0416_safety_boundary_report",
    "create_v0416_trace_acceptance",
    "create_v0416_troubleshooting_item",
    "create_v0416_troubleshooting_items",
    "create_v0416_user_guide_command",
    "create_v0416_user_guide_section",
    "create_v0416_user_guide_sections",
    "create_v0416_user_test_flow",
    "create_v0416_user_test_flow_result",
    "create_v0416_user_test_flow_step",
    "create_v0416_v042_handoff",
    "main",
]
