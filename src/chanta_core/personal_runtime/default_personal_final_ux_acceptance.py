"""v0.42.10 final business UX acceptance gate.

This module is acceptance and handoff metadata only. It does not add provider
tool calling, function calling, shell execution, subagents, retries, memory
mutation, or production certification.
"""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass, is_dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_business_ux import (
    V0429_CLOSED_CAPABILITIES,
    main as _v0429_main,
)


V04210_VERSION = "v0.42.10"
V04210_RELEASE_NAME = "v0.42.10 Final Business UX Acceptance & Operation Pilot Gate"
V04210_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.10_final_business_ux_acceptance_restore.md"


class V04210AcceptanceStatus(StrEnum):
    PASS = "pass"
    PASS_WITH_NOTES = "pass_with_notes"
    WARNING = "warning"
    FAIL = "fail"
    NOT_TESTED = "not_tested"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class V04210AcceptanceSeverity(StrEnum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKER = "blocker"
    UNKNOWN = "unknown"


class V04210AcceptanceArea(StrEnum):
    DEFAULT_RUN_OUTPUT = "default_run_output"
    DEBUG_RUN_OUTPUT = "debug_run_output"
    CONFIGURED_PROVIDER = "configured_provider"
    MOCK_PROVIDER = "mock_provider"
    CHAT_OUTPUT = "chat_output"
    PROVIDER_STATUS = "provider_status"
    COMMAND_GUIDE = "command_guide"
    RUNTIME_IDENTITY = "runtime_identity"
    EMPTY_RESPONSE = "empty_response"
    DIAGNOSTICS = "diagnostics"
    PROCESS_INTELLIGENCE_REVIEW = "process_intelligence_review"
    SAFETY_BOUNDARY = "safety_boundary"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V04210ManualAcceptanceScenario:
    scenario_id: str
    title: str
    purpose: str
    commands: tuple[str, ...]
    expected_user_experience: str
    acceptance_area: str
    blocks_v043_if_failed: bool


@dataclass(frozen=True)
class V04210ManualAcceptanceStep:
    step_id: str
    order_index: int
    command_text: str
    expected_result: str
    failure_signal: str
    area: str


@dataclass(frozen=True)
class V04210ManualAcceptanceCriterion:
    criterion_id: str
    area: str
    description: str
    pass_condition: str
    fail_condition: str
    severity_if_failed: str
    blocks_v043: bool


@dataclass(frozen=True)
class V04210ConfiguredProviderAcceptance:
    acceptance_id: str
    provider_config_required: bool
    connectivity_required: bool
    actual_completion_required: bool
    default_output_clean_required: bool
    runtime_identity_required: bool
    empty_response_must_not_complete_success: bool
    debug_output_available_required: bool
    status: str
    blocks_v043: bool


@dataclass(frozen=True)
class V04210MockProviderAcceptance:
    acceptance_id: str
    mock_run_required: bool
    mock_chat_required: bool
    duplicate_output_absent_required: bool
    debug_available_required: bool
    status: str


@dataclass(frozen=True)
class V04210RunUXAcceptance:
    acceptance_id: str
    default_output_hides_raw_trace: bool
    default_output_shows_assistant_response: bool
    compact_footer_ok: bool
    debug_output_exposes_details: bool
    json_output_preserved: bool
    status: str
    blocking_findings: tuple[str, ...]


@dataclass(frozen=True)
class V04210DebugUXAcceptance:
    acceptance_id: str
    debug_flag_supported: bool
    verbose_or_json_available: bool
    run_id_visible: bool
    session_id_visible: bool
    provider_visible: bool
    parse_status_visible: bool
    safety_flags_visible: bool
    status: str


@dataclass(frozen=True)
class V04210ChatUXAcceptance:
    acceptance_id: str
    clean_banner: bool
    grouped_help: bool
    readable_status: bool
    readable_provider_view: bool
    no_duplicate_response: bool
    internal_commands_safe: bool
    status: str
    blocking_findings: tuple[str, ...]


@dataclass(frozen=True)
class V04210ProviderUXAcceptance:
    acceptance_id: str
    status_readable: bool
    connectivity_readable: bool
    next_action_clear: bool
    secrets_hidden: bool
    mock_and_configured_readiness_clear: bool
    status: str


@dataclass(frozen=True)
class V04210CommandGuideAcceptance:
    acceptance_id: str
    guide_command_available: bool
    sections_present: tuple[str, ...]
    hides_internal_artifact_names: bool
    business_user_friendly: bool
    status: str


@dataclass(frozen=True)
class V04210RuntimeIdentityAcceptance:
    acceptance_id: str
    primary_identity: str
    provider_identity_treatment: str
    base_model_identity_primary_allowed: bool
    korean_polite_language_expected: bool
    business_agent_positioning: bool
    status: str
    sample_expected_answer: str


@dataclass(frozen=True)
class V04210EmptyResponseAcceptance:
    acceptance_id: str
    empty_response_must_fail_or_completed_empty: bool
    empty_response_completed_success_allowed: bool
    plain_language_guidance_required: bool
    run_report_parse_fields_required: bool
    status: str


@dataclass(frozen=True)
class V04210DiagnosticAcceptance:
    acceptance_id: str
    report_bundle_available: bool
    copy_paste_available: bool
    redaction_required: bool
    includes_provider_run_trace_feedback_safety: bool
    status: str


@dataclass(frozen=True)
class V04210PIReviewAvailabilityAcceptance:
    acceptance_id: str
    trace_timeline_available: bool
    run_report_available: bool
    run_history_available: bool
    report_bundle_available: bool
    feedback_available: bool
    process_evidence_preserved: bool
    status: str


@dataclass(frozen=True)
class V04210SafetyBoundaryAcceptance:
    acceptance_id: str
    provider_doctor_completion_closed: bool
    provider_tool_calling_closed: bool
    function_calling_closed: bool
    shell_execution_closed: bool
    file_edit_closed: bool
    patch_apply_closed: bool
    arbitrary_file_read_closed: bool
    broad_scan_closed: bool
    repo_search_closed: bool
    subagent_closed: bool
    general_agent_loop_closed: bool
    dominion_closed: bool
    production_certified: bool
    status: str


@dataclass(frozen=True)
class V04210FinalUXFinding:
    finding_id: str
    area: str
    severity: str
    description: str
    user_impact: str
    fix_applied_in_v04210: bool
    deferred_to_v04211: bool
    blocks_v043: bool
    recommended_action: str


@dataclass(frozen=True)
class V04210FinalUXAcceptanceReport:
    report_id: str
    configured_provider_acceptance: V04210ConfiguredProviderAcceptance
    mock_provider_acceptance: V04210MockProviderAcceptance
    run_ux_acceptance: V04210RunUXAcceptance
    debug_ux_acceptance: V04210DebugUXAcceptance
    chat_ux_acceptance: V04210ChatUXAcceptance
    provider_ux_acceptance: V04210ProviderUXAcceptance
    command_guide_acceptance: V04210CommandGuideAcceptance
    runtime_identity_acceptance: V04210RuntimeIdentityAcceptance
    empty_response_acceptance: V04210EmptyResponseAcceptance
    diagnostic_acceptance: V04210DiagnosticAcceptance
    pi_review_acceptance: V04210PIReviewAvailabilityAcceptance
    safety_acceptance: V04210SafetyBoundaryAcceptance
    findings: tuple[V04210FinalUXFinding, ...]
    blocker_count: int
    warning_count: int
    pass_count: int
    ready_for_v043: bool
    recommends_v04211: bool
    production_certified: bool


@dataclass(frozen=True)
class V04210PilotGateDecision:
    decision_id: str
    decision: str
    reason: str
    ready_for_v043: bool
    continue_v04211: bool
    required_before_v043: tuple[str, ...]
    recommended_next_track: str


@dataclass(frozen=True)
class V04210ReadinessReport:
    final_business_ux_acceptance_ready: bool
    configured_provider_acceptance_defined: bool
    mock_provider_acceptance_defined: bool
    run_ux_acceptance_ready: bool
    chat_ux_acceptance_ready: bool
    provider_ux_acceptance_ready: bool
    command_guide_acceptance_ready: bool
    runtime_identity_acceptance_ready: bool
    empty_response_acceptance_ready: bool
    diagnostic_acceptance_ready: bool
    pi_review_availability_ready: bool
    safety_boundary_acceptance_ready: bool
    pilot_gate_decision_ready: bool
    integrated_restore_document_ready: bool
    ready_for_v043_user_operation_pilot: bool
    recommends_v04211_final_polish: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_arbitrary_file_read: bool
    ready_for_broad_filesystem_scan: bool
    ready_for_repo_search: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V04211PolishContinuationHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V043UserOperationPilotHandoffFinal:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04210IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V04210IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str


@dataclass(frozen=True)
class V04210IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V04210IntegratedRestoreContextSnapshot
    sections: tuple[V04210IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V04210IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool


REQUIRED_V04210_DOC_SECTIONS: tuple[str, ...] = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "Project Context for New Codex Session",
    "User UX Direction",
    "v0.42.9 Result Summary",
    "Final Business UX Acceptance Scope",
    "Configured Provider Acceptance",
    "Mock Provider Acceptance",
    "Default Run UX Acceptance",
    "Debug UX Acceptance",
    "Chat UX Acceptance",
    "Provider UX Acceptance",
    "Command Guide Acceptance",
    "Runtime Identity Acceptance",
    "Empty Response Acceptance",
    "Diagnostic Acceptance",
    "Process Intelligence Review Availability",
    "Safety Boundary Acceptance",
    "Final UX Findings",
    "Pilot Gate Decision",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Manual Acceptance Commands",
    "Withdrawal Conditions",
    "v0.42.11 or v0.43 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)

REQUIRED_COMMAND_GUIDE_SECTIONS: tuple[str, ...] = (
    "Start",
    "Talk",
    "Provider",
    "Review",
    "Skills",
    "Diagnostics",
    "Safety",
)


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _json_ready(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    return value


def create_v04210_manual_acceptance_step(
    command_text: str = 'chanta-cli run --provider mock "hello"',
    expected_result: str = "Clean business-facing output.",
    failure_signal: str = "Raw trace banner or missing assistant response.",
    area: str = V04210AcceptanceArea.DEFAULT_RUN_OUTPUT.value,
    order_index: int = 1,
    **overrides: Any,
) -> V04210ManualAcceptanceStep:
    defaults = {
        "step_id": f"v04210-step-{order_index}",
        "order_index": order_index,
        "command_text": command_text,
        "expected_result": expected_result,
        "failure_signal": failure_signal,
        "area": area,
    }
    return V04210ManualAcceptanceStep(**_merge(defaults, overrides))


def create_v04210_manual_acceptance_criterion(
    area: str = V04210AcceptanceArea.DEFAULT_RUN_OUTPUT.value,
    description: str = "Default output is business-user-facing.",
    pass_condition: str = "Assistant response is visible and raw trace banner is hidden.",
    fail_condition: str = "Default output is raw trace or hides the answer.",
    severity_if_failed: str = V04210AcceptanceSeverity.BLOCKER.value,
    blocks_v043: bool = True,
    **overrides: Any,
) -> V04210ManualAcceptanceCriterion:
    defaults = {
        "criterion_id": f"v04210-criterion-{area}",
        "area": area,
        "description": description,
        "pass_condition": pass_condition,
        "fail_condition": fail_condition,
        "severity_if_failed": severity_if_failed,
        "blocks_v043": blocks_v043,
    }
    return V04210ManualAcceptanceCriterion(**_merge(defaults, overrides))


def create_v04210_manual_acceptance_scenario(
    scenario_id: str = "configured-provider-default-run",
    title: str = "configured provider default run",
    purpose: str = "Verify live configured provider UX.",
    commands: tuple[str, ...] = ('chanta-cli run --profile default-personal --provider configured --timeout 120 "넌 누구야?"',),
    expected_user_experience: str = "Clean answer or plain-language failure card.",
    acceptance_area: str = V04210AcceptanceArea.CONFIGURED_PROVIDER.value,
    blocks_v043_if_failed: bool = True,
    **overrides: Any,
) -> V04210ManualAcceptanceScenario:
    defaults = {
        "scenario_id": scenario_id,
        "title": title,
        "purpose": purpose,
        "commands": commands,
        "expected_user_experience": expected_user_experience,
        "acceptance_area": acceptance_area,
        "blocks_v043_if_failed": blocks_v043_if_failed,
    }
    return V04210ManualAcceptanceScenario(**_merge(defaults, overrides))


def create_v04210_configured_provider_acceptance(
    live_tested: bool = False,
    status: str | None = None,
    **overrides: Any,
) -> V04210ConfiguredProviderAcceptance:
    resolved_status = status or (V04210AcceptanceStatus.PASS_WITH_NOTES.value if live_tested else V04210AcceptanceStatus.NOT_TESTED.value)
    defaults = {
        "acceptance_id": "v04210-configured-provider-acceptance",
        "provider_config_required": True,
        "connectivity_required": True,
        "actual_completion_required": True,
        "default_output_clean_required": True,
        "runtime_identity_required": True,
        "empty_response_must_not_complete_success": True,
        "debug_output_available_required": True,
        "status": resolved_status,
        "blocks_v043": resolved_status not in {V04210AcceptanceStatus.PASS.value, V04210AcceptanceStatus.PASS_WITH_NOTES.value},
    }
    return V04210ConfiguredProviderAcceptance(**_merge(defaults, overrides))


def create_v04210_mock_provider_acceptance(**overrides: Any) -> V04210MockProviderAcceptance:
    defaults = {
        "acceptance_id": "v04210-mock-provider-acceptance",
        "mock_run_required": True,
        "mock_chat_required": True,
        "duplicate_output_absent_required": True,
        "debug_available_required": True,
        "status": V04210AcceptanceStatus.PASS.value,
    }
    return V04210MockProviderAcceptance(**_merge(defaults, overrides))


def create_v04210_run_ux_acceptance(**overrides: Any) -> V04210RunUXAcceptance:
    defaults = {
        "acceptance_id": "v04210-run-ux-acceptance",
        "default_output_hides_raw_trace": True,
        "default_output_shows_assistant_response": True,
        "compact_footer_ok": True,
        "debug_output_exposes_details": True,
        "json_output_preserved": True,
        "status": V04210AcceptanceStatus.PASS.value,
        "blocking_findings": (),
    }
    return V04210RunUXAcceptance(**_merge(defaults, overrides))


def create_v04210_debug_ux_acceptance(**overrides: Any) -> V04210DebugUXAcceptance:
    defaults = {
        "acceptance_id": "v04210-debug-ux-acceptance",
        "debug_flag_supported": True,
        "verbose_or_json_available": True,
        "run_id_visible": True,
        "session_id_visible": True,
        "provider_visible": True,
        "parse_status_visible": True,
        "safety_flags_visible": True,
        "status": V04210AcceptanceStatus.PASS.value,
    }
    return V04210DebugUXAcceptance(**_merge(defaults, overrides))


def create_v04210_chat_ux_acceptance(**overrides: Any) -> V04210ChatUXAcceptance:
    defaults = {
        "acceptance_id": "v04210-chat-ux-acceptance",
        "clean_banner": True,
        "grouped_help": True,
        "readable_status": True,
        "readable_provider_view": True,
        "no_duplicate_response": True,
        "internal_commands_safe": True,
        "status": V04210AcceptanceStatus.PASS.value,
        "blocking_findings": (),
    }
    return V04210ChatUXAcceptance(**_merge(defaults, overrides))


def create_v04210_provider_ux_acceptance(**overrides: Any) -> V04210ProviderUXAcceptance:
    defaults = {
        "acceptance_id": "v04210-provider-ux-acceptance",
        "status_readable": True,
        "connectivity_readable": True,
        "next_action_clear": True,
        "secrets_hidden": True,
        "mock_and_configured_readiness_clear": True,
        "status": V04210AcceptanceStatus.PASS.value,
    }
    return V04210ProviderUXAcceptance(**_merge(defaults, overrides))


def create_v04210_command_guide_acceptance(**overrides: Any) -> V04210CommandGuideAcceptance:
    defaults = {
        "acceptance_id": "v04210-command-guide-acceptance",
        "guide_command_available": True,
        "sections_present": REQUIRED_COMMAND_GUIDE_SECTIONS,
        "hides_internal_artifact_names": True,
        "business_user_friendly": True,
        "status": V04210AcceptanceStatus.PASS.value,
    }
    return V04210CommandGuideAcceptance(**_merge(defaults, overrides))


def create_v04210_runtime_identity_acceptance(**overrides: Any) -> V04210RuntimeIdentityAcceptance:
    defaults = {
        "acceptance_id": "v04210-runtime-identity-acceptance",
        "primary_identity": "ChantaCore default-personal work assistant",
        "provider_identity_treatment": "provider model is implementation detail",
        "base_model_identity_primary_allowed": False,
        "korean_polite_language_expected": True,
        "business_agent_positioning": True,
        "status": V04210AcceptanceStatus.PASS_WITH_NOTES.value,
        "sample_expected_answer": (
            "\uc800\ub294 ChantaCore default-personal runtime\uc5d0\uc11c \ub3d9\uc791\ud558\ub294 "
            "\uc5c5\ubb34 \ubcf4\uc870 \uc5d0\uc774\uc804\ud2b8\uc785\ub2c8\ub2e4. "
            "\ud604\uc7ac \uc751\ub2f5 \uc0dd\uc131\uc5d0\ub294 \ub85c\uceec OpenAI-compatible provider\uac00 "
            "\uc0ac\uc6a9\ub418\uba70, provider \ubaa8\ub378\uc740 \uad6c\ud604 \uc138\ubd80\uc0ac\ud56d\uc785\ub2c8\ub2e4."
        ),
    }
    return V04210RuntimeIdentityAcceptance(**_merge(defaults, overrides))


def create_v04210_empty_response_acceptance(**overrides: Any) -> V04210EmptyResponseAcceptance:
    defaults = {
        "acceptance_id": "v04210-empty-response-acceptance",
        "empty_response_must_fail_or_completed_empty": True,
        "empty_response_completed_success_allowed": False,
        "plain_language_guidance_required": True,
        "run_report_parse_fields_required": True,
        "status": V04210AcceptanceStatus.PASS.value,
    }
    return V04210EmptyResponseAcceptance(**_merge(defaults, overrides))


def create_v04210_diagnostic_acceptance(**overrides: Any) -> V04210DiagnosticAcceptance:
    defaults = {
        "acceptance_id": "v04210-diagnostic-acceptance",
        "report_bundle_available": True,
        "copy_paste_available": True,
        "redaction_required": True,
        "includes_provider_run_trace_feedback_safety": True,
        "status": V04210AcceptanceStatus.PASS.value,
    }
    return V04210DiagnosticAcceptance(**_merge(defaults, overrides))


def create_v04210_pi_review_availability_acceptance(**overrides: Any) -> V04210PIReviewAvailabilityAcceptance:
    defaults = {
        "acceptance_id": "v04210-pi-review-availability-acceptance",
        "trace_timeline_available": True,
        "run_report_available": True,
        "run_history_available": True,
        "report_bundle_available": True,
        "feedback_available": True,
        "process_evidence_preserved": True,
        "status": V04210AcceptanceStatus.PASS.value,
    }
    return V04210PIReviewAvailabilityAcceptance(**_merge(defaults, overrides))


def create_v04210_safety_boundary_acceptance(**overrides: Any) -> V04210SafetyBoundaryAcceptance:
    defaults = {
        "acceptance_id": "v04210-safety-boundary-acceptance",
        "provider_doctor_completion_closed": True,
        "provider_tool_calling_closed": True,
        "function_calling_closed": True,
        "shell_execution_closed": True,
        "file_edit_closed": True,
        "patch_apply_closed": True,
        "arbitrary_file_read_closed": True,
        "broad_scan_closed": True,
        "repo_search_closed": True,
        "subagent_closed": True,
        "general_agent_loop_closed": True,
        "dominion_closed": True,
        "production_certified": False,
        "status": V04210AcceptanceStatus.PASS.value,
    }
    return V04210SafetyBoundaryAcceptance(**_merge(defaults, overrides))


def create_v04210_final_ux_finding(
    finding_id: str = "configured-live-provider-manual-acceptance",
    area: str = V04210AcceptanceArea.CONFIGURED_PROVIDER.value,
    severity: str = V04210AcceptanceSeverity.LOW.value,
    description: str = "Configured provider live acceptance depends on the user's local provider state.",
    user_impact: str = "v0.43 should begin only after live configured output is acceptable or safely handled.",
    fix_applied_in_v04210: bool = False,
    deferred_to_v04211: bool = False,
    blocks_v043: bool = False,
    recommended_action: str = "Run manual configured provider acceptance on the real ChantaCore home.",
    **overrides: Any,
) -> V04210FinalUXFinding:
    defaults = {
        "finding_id": finding_id,
        "area": area,
        "severity": severity,
        "description": description,
        "user_impact": user_impact,
        "fix_applied_in_v04210": fix_applied_in_v04210,
        "deferred_to_v04211": deferred_to_v04211,
        "blocks_v043": blocks_v043,
        "recommended_action": recommended_action,
    }
    return V04210FinalUXFinding(**_merge(defaults, overrides))


def create_v04210_final_ux_acceptance_report(
    configured_live_tested: bool = False,
    configured_status: str | None = None,
    findings: tuple[V04210FinalUXFinding, ...] | None = None,
    **overrides: Any,
) -> V04210FinalUXAcceptanceReport:
    configured = create_v04210_configured_provider_acceptance(configured_live_tested, configured_status)
    findings = findings if findings is not None else (() if configured.status in {V04210AcceptanceStatus.PASS.value, V04210AcceptanceStatus.PASS_WITH_NOTES.value} else (create_v04210_final_ux_finding(blocks_v043=True, severity=V04210AcceptanceSeverity.BLOCKER.value),))
    acceptances = (
        configured.status,
        create_v04210_mock_provider_acceptance().status,
        create_v04210_run_ux_acceptance().status,
        create_v04210_debug_ux_acceptance().status,
        create_v04210_chat_ux_acceptance().status,
        create_v04210_provider_ux_acceptance().status,
        create_v04210_command_guide_acceptance().status,
        create_v04210_runtime_identity_acceptance().status,
        create_v04210_empty_response_acceptance().status,
        create_v04210_diagnostic_acceptance().status,
        create_v04210_pi_review_availability_acceptance().status,
        create_v04210_safety_boundary_acceptance().status,
    )
    blocker_count = sum(1 for item in findings if item.blocks_v043 or item.severity == V04210AcceptanceSeverity.BLOCKER.value)
    warning_count = sum(1 for item in findings if item.severity in {V04210AcceptanceSeverity.LOW.value, V04210AcceptanceSeverity.MEDIUM.value, V04210AcceptanceSeverity.HIGH.value} and not item.blocks_v043)
    pass_count = sum(1 for status in acceptances if status in {V04210AcceptanceStatus.PASS.value, V04210AcceptanceStatus.PASS_WITH_NOTES.value})
    ready = blocker_count == 0 and configured.status in {V04210AcceptanceStatus.PASS.value, V04210AcceptanceStatus.PASS_WITH_NOTES.value}
    defaults = {
        "report_id": "v04210-final-ux-acceptance-report",
        "configured_provider_acceptance": configured,
        "mock_provider_acceptance": create_v04210_mock_provider_acceptance(),
        "run_ux_acceptance": create_v04210_run_ux_acceptance(),
        "debug_ux_acceptance": create_v04210_debug_ux_acceptance(),
        "chat_ux_acceptance": create_v04210_chat_ux_acceptance(),
        "provider_ux_acceptance": create_v04210_provider_ux_acceptance(),
        "command_guide_acceptance": create_v04210_command_guide_acceptance(),
        "runtime_identity_acceptance": create_v04210_runtime_identity_acceptance(),
        "empty_response_acceptance": create_v04210_empty_response_acceptance(),
        "diagnostic_acceptance": create_v04210_diagnostic_acceptance(),
        "pi_review_acceptance": create_v04210_pi_review_availability_acceptance(),
        "safety_acceptance": create_v04210_safety_boundary_acceptance(),
        "findings": findings,
        "blocker_count": blocker_count,
        "warning_count": warning_count,
        "pass_count": pass_count,
        "ready_for_v043": ready,
        "recommends_v04211": any(item.deferred_to_v04211 for item in findings),
        "production_certified": False,
    }
    return V04210FinalUXAcceptanceReport(**_merge(defaults, overrides))


def create_v04210_pilot_gate_decision(
    report: V04210FinalUXAcceptanceReport | None = None,
    **overrides: Any,
) -> V04210PilotGateDecision:
    report = report or create_v04210_final_ux_acceptance_report(configured_live_tested=True)
    if report.ready_for_v043:
        decision = "proceed_to_v043"
        reason = "Final business UX acceptance has no v0.43 blockers."
        required = ()
        next_track = "v0.43 User Operation Pilot & Process Intelligence Review Loop"
    elif report.recommends_v04211:
        decision = "continue_v04211"
        reason = "User-facing polish remains but no unsafe capability is required."
        required = tuple(item.recommended_action for item in report.findings if item.blocks_v043)
        next_track = "v0.42.11 Final Polish Continuation"
    else:
        decision = "blocked"
        reason = "Configured provider live acceptance or another blocker is not satisfied."
        required = tuple(item.recommended_action for item in report.findings if item.blocks_v043)
        next_track = "v0.42.10 manual acceptance retry"
    defaults = {
        "decision_id": "v04210-pilot-gate-decision",
        "decision": decision,
        "reason": reason,
        "ready_for_v043": report.ready_for_v043,
        "continue_v04211": decision == "continue_v04211",
        "required_before_v043": required,
        "recommended_next_track": next_track,
    }
    return V04210PilotGateDecision(**_merge(defaults, overrides))


def create_v04210_readiness_report(**overrides: Any) -> V04210ReadinessReport:
    decision = create_v04210_pilot_gate_decision()
    defaults = {
        "final_business_ux_acceptance_ready": True,
        "configured_provider_acceptance_defined": True,
        "mock_provider_acceptance_defined": True,
        "run_ux_acceptance_ready": True,
        "chat_ux_acceptance_ready": True,
        "provider_ux_acceptance_ready": True,
        "command_guide_acceptance_ready": True,
        "runtime_identity_acceptance_ready": True,
        "empty_response_acceptance_ready": True,
        "diagnostic_acceptance_ready": True,
        "pi_review_availability_ready": True,
        "safety_boundary_acceptance_ready": True,
        "pilot_gate_decision_ready": True,
        "integrated_restore_document_ready": True,
        "ready_for_v043_user_operation_pilot": decision.ready_for_v043,
        "recommends_v04211_final_polish": decision.continue_v04211,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_broad_filesystem_scan": False,
        "ready_for_repo_search": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_multi_step_agent_loop": False,
        "ready_for_autonomous_retry_loop": False,
        "ready_for_dominion_runtime": False,
        "production_certified": False,
    }
    return V04210ReadinessReport(**_merge(defaults, overrides))


def create_v04211_polish_continuation_handoff(**overrides: Any) -> V04211PolishContinuationHandoff:
    defaults = {
        "handoff_id": "v04211-polish-continuation-handoff",
        "target_version": "v0.42.11 Final Polish Continuation",
        "recommended_focus": (
            "only address remaining user-facing rough edges found in v0.42.10",
            "no new runtime capability",
            "no high-risk feature",
            "no shell/edit/apply/subagent",
            "no provider tool/function calling",
            "no production certification",
        ),
        "must_not_open": V0429_CLOSED_CAPABILITIES,
        "production_certified": False,
    }
    return V04211PolishContinuationHandoff(**_merge(defaults, overrides))


def create_v043_user_operation_pilot_handoff_final(**overrides: Any) -> V043UserOperationPilotHandoffFinal:
    defaults = {
        "handoff_id": "v043-user-operation-pilot-handoff-final",
        "target_version": "v0.43 User Operation Pilot & Process Intelligence Review Loop",
        "recommended_focus": (
            "begin real user operation pilot",
            "use ChantaCore for actual daily/work-like questions",
            "collect feedback notes",
            "collect report bundles",
            "review traces after real usage",
            "evaluate ChantaCore as work-agent runtime",
            "determine Schumpeter split readiness from runtime contract, provider stability, trace evidence, and security boundary",
            "no production certification",
        ),
        "must_not_open": V0429_CLOSED_CAPABILITIES,
        "production_certified": False,
    }
    return V043UserOperationPilotHandoffFinal(**_merge(defaults, overrides))


def create_v04210_integrated_restore_context_snapshot(**overrides: Any) -> V04210IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v04210-integrated-restore-context-snapshot",
        "current_version": V04210_RELEASE_NAME,
        "current_track": V04210_TRACK_NAME,
        "open_capabilities": (
            "final_business_ux_acceptance_model",
            "live_configured_provider_acceptance_checklist",
            "mock_provider_acceptance_checklist",
            "runtime_identity_acceptance",
            "empty_response_acceptance",
            "diagnostic_acceptance",
            "process_intelligence_review_acceptance",
            "safety_boundary_acceptance",
            "v043_pilot_gate_decision",
            "v04211_or_v043_handoff",
            "integrated_restore_document",
        ),
        "closed_capabilities": V0429_CLOSED_CAPABILITIES,
        "integrated_doc_path": INTEGRATED_DOC_PATH,
    }
    return V04210IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v04210_integrated_restore_packet(**overrides: Any) -> V04210IntegratedRestorePacket:
    sections = tuple(
        V04210IntegratedRestoreSection(section.lower().replace(" ", "_").replace("-", "_"), section, True)
        for section in REQUIRED_V04210_DOC_SECTIONS
    )
    defaults = {
        "packet_id": "v04210-integrated-restore-packet",
        "context_snapshot": create_v04210_integrated_restore_context_snapshot(),
        "sections": sections,
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V04210IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v04210_integrated_restore_document_manifest(**overrides: Any) -> V04210IntegratedRestoreDocumentManifest:
    path = Path(INTEGRATED_DOC_PATH)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    forbidden = (
        Path("docs/versions/v0.42/v0.42.10_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.10_acceptance.md"),
        Path("docs/versions/v0.42/v0.42.10_business_ux.md"),
        Path("docs/versions/v0.42/v0.42.10_final_ux.md"),
    )
    defaults = {
        "manifest_id": "v04210-integrated-restore-document-manifest",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": any(item.exists() for item in forbidden),
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": bool(text) and all(f"## {section}" in text for section in REQUIRED_V04210_DOC_SECTIONS),
    }
    return V04210IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def create_v04210_manual_acceptance_scenarios() -> tuple[V04210ManualAcceptanceScenario, ...]:
    return (
        create_v04210_manual_acceptance_scenario("configured-provider-default-run", "configured provider default run", commands=('chanta-cli run --profile default-personal --provider configured --timeout 120 "넌 누구야?"',)),
        create_v04210_manual_acceptance_scenario("configured-provider-debug-run", "configured provider debug run", commands=('chanta-cli run --profile default-personal --provider configured --timeout 120 --debug "넌 누구야?"',), acceptance_area=V04210AcceptanceArea.DEBUG_RUN_OUTPUT.value),
        create_v04210_manual_acceptance_scenario("mock-provider-default-run", "mock provider default run", commands=('chanta-cli run --profile default-personal --provider mock "넌 누구야?"',), acceptance_area=V04210AcceptanceArea.MOCK_PROVIDER.value),
        create_v04210_manual_acceptance_scenario("chat-configured-provider", "chat configured provider", commands=("chanta-cli chat --provider configured --timeout 120", "/help", "/status", "/provider", "넌 누구야", "/run last", "/exit"), acceptance_area=V04210AcceptanceArea.CHAT_OUTPUT.value),
        create_v04210_manual_acceptance_scenario("chat-mock-provider", "chat mock provider", commands=("chanta-cli chat --provider mock", "/help", "/status", "/provider", "넌 누구야", "/history", "/trace", "/handoff", "/exit"), acceptance_area=V04210AcceptanceArea.CHAT_OUTPUT.value),
        create_v04210_manual_acceptance_scenario("provider-status-connectivity", "provider status/connectivity", commands=("chanta-cli provider status", "chanta-cli provider connectivity"), acceptance_area=V04210AcceptanceArea.PROVIDER_STATUS.value),
        create_v04210_manual_acceptance_scenario("command-guide", "command guide", commands=("chanta-cli commands",), acceptance_area=V04210AcceptanceArea.COMMAND_GUIDE.value),
        create_v04210_manual_acceptance_scenario("report-bundle-copy-paste", "report bundle copy-paste", commands=("chanta-cli report bundle --copy-paste",), acceptance_area=V04210AcceptanceArea.DIAGNOSTICS.value),
        create_v04210_manual_acceptance_scenario("empty-response-handling", "empty response handling", commands=("simulate configured provider empty final answer", "chanta-cli run-report last"), acceptance_area=V04210AcceptanceArea.EMPTY_RESPONSE.value),
        create_v04210_manual_acceptance_scenario("runtime-identity-answer", "runtime identity answer", commands=('chanta-cli run --provider configured "넌 누구야?"',), acceptance_area=V04210AcceptanceArea.RUNTIME_IDENTITY.value),
        create_v04210_manual_acceptance_scenario("safety-boundary-check", "safety boundary check", commands=('chanta-cli safety check-command --command "rm -rf ."',), acceptance_area=V04210AcceptanceArea.SAFETY_BOUNDARY.value),
    )


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V04210_VERSION}; {V04210_RELEASE_NAME})")
        return 0
    return _v0429_main(args)


__all__ = [
    name
    for name in globals()
    if name.startswith("V042")
    or name.startswith("V043")
    or name.startswith("create_v042")
    or name.startswith("create_v043")
    or name == "main"
]
