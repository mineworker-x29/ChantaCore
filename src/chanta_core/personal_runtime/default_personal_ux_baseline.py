"""v0.42.0 Default Personal Runtime UX baseline metadata.

This module records the v0.42 UX hardening baseline as pure metadata. It does
not change CLI behavior, resolve a default home, call providers, submit prompts,
execute skills, or open any new runtime capability.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable


V0420_VERSION = "v0.42.0"
V042_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
V0420_RELEASE_NAME = "Default Personal Runtime UX Baseline & User Journey Contract"
V0420_FULL_NAME = f"{V0420_VERSION} {V0420_RELEASE_NAME}"
V0416_BASELINE_VERSION = "v0.41.6"
V0416_TRACK_NAME = "v0.41 Default Personal Runtime Opening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.0_default_personal_runtime_ux_baseline_restore.md"


class V042UXPainPointKind(str, Enum):
    DEFAULT_HOME_FRICTION = "default_home_friction"
    PROVIDER_SETUP_FRICTION = "provider_setup_friction"
    JSON_TRACE_READABILITY = "json_trace_readability"
    RUN_HISTORY_VISIBILITY = "run_history_visibility"
    SESSION_VISIBILITY = "session_visibility"
    DIAGNOSTIC_HANDOFF_GAP = "diagnostic_handoff_gap"
    VERSION_METADATA_MISMATCH = "version_metadata_mismatch"
    PROVIDER_COUNT_SEMANTICS = "provider_count_semantics"
    USER_COMMAND_DISCOVERABILITY = "user_command_discoverability"
    UNKNOWN = "unknown"


class V042UserReviewMode(str, Enum):
    USER_FLOW_REVIEW = "user_flow_review"
    COMMAND_OUTPUT_REVIEW = "command_output_review"
    PROCESS_TRACE_REVIEW = "process_trace_review"
    RUN_REPORT_REVIEW = "run_report_review"
    DENIAL_EVIDENCE_REVIEW = "denial_evidence_review"
    CODE_LEVEL_REVIEW_LIMITED = "code_level_review_limited"
    UNKNOWN = "unknown"


class V042UserJourneyStepKind(str, Enum):
    INSTALL = "install"
    FIRST_DOCTOR = "first_doctor"
    QUICKSTART = "quickstart"
    PROFILE_INIT = "profile_init"
    PROFILE_STATUS = "profile_status"
    PROVIDER_STATUS = "provider_status"
    MOCK_RUN = "mock_run"
    CONFIGURED_PROVIDER_RUN = "configured_provider_run"
    TRACE_REVIEW = "trace_review"
    RUN_HISTORY_REVIEW = "run_history_review"
    SESSION_REVIEW = "session_review"
    DENIAL_TEST = "denial_test"
    DIAGNOSTIC_BUNDLE = "diagnostic_bundle"
    FEEDBACK_NOTE = "feedback_note"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V042TrackIdentity:
    track_id: str
    version: str
    track_name: str
    track_goal: str
    previous_track: str
    starting_baseline_version: str
    primary_user_review_mode: str
    process_intelligence_review_required: bool
    high_risk_capability_expansion_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0416UserTestEvidence:
    evidence_id: str
    evidence_source: str
    test_home_kind: str
    fresh_home_used: bool
    init_passed: bool
    profile_status_passed: bool
    provider_doctor_no_completion_passed: bool
    mock_run_passed: bool
    trace_recent_passed: bool
    trace_summary_passed: bool
    run_report_last_passed: bool
    safety_denial_passed: bool
    run_count: int
    denial_count: int
    provider_call_count_observed: int
    provider_call_count_semantics: str
    shell_execution_count: int
    skill_execution_count: int
    subagent_invocation_count: int
    production_certification_count: int
    total_events: int
    deterministic_mock_flow_passed: bool
    configured_provider_flow_verified: bool


@dataclass(frozen=True)
class V0416UserTestEvidenceInterpretation:
    interpretation_id: str
    evidence: V0416UserTestEvidence
    v0416_passed: bool
    v041_track_can_close: bool
    ready_for_v042_ux_hardening: bool
    blockers: tuple[str, ...]
    non_blocking_notes: tuple[str, ...]
    recommended_next_track: str


@dataclass(frozen=True)
class V0416KnownNote:
    note_id: str
    title: str
    description: str
    severity: str
    blocks_v0420: bool
    recommended_target_version: str
    recommendation: str


@dataclass(frozen=True)
class V042UXPainPoint:
    pain_point_id: str
    kind: str
    title: str
    observed_in_v0416: bool
    user_impact: str
    process_intelligence_impact: str
    recommended_target_version: str
    recommended_resolution: str
    high_risk_capability_required: bool


@dataclass(frozen=True)
class V042UserPersona:
    persona_id: str
    name: str
    review_strength: str
    review_limit: str
    needs_from_v042: tuple[str, ...]


@dataclass(frozen=True)
class V042UserJourneyStep:
    step_id: str
    order_index: int
    step_kind: str
    current_v0416_command: str
    desired_v042_command: str
    current_friction: str
    target_user_experience: str
    process_intelligence_review_need: str
    target_version: str
    opens_high_risk_capability: bool


@dataclass(frozen=True)
class V042UserJourneyContract:
    contract_id: str
    title: str
    baseline_version: str
    steps: tuple[V042UserJourneyStep, ...]
    user_can_review_without_code: bool
    process_trace_review_required: bool
    high_risk_capabilities_remain_closed: bool


@dataclass(frozen=True)
class V042CommandSurfaceReviewItem:
    item_id: str
    command_name: str
    current_state: str
    desired_state: str
    user_friction: str
    process_intelligence_value: str
    target_version: str
    should_remain_closed: bool


@dataclass(frozen=True)
class V042CommandSurfaceReview:
    review_id: str
    items: tuple[V042CommandSurfaceReviewItem, ...]
    default_home_required: bool
    human_readable_outputs_required: bool
    closed_capabilities_visible_to_user: bool


@dataclass(frozen=True)
class V042DefaultHomeUXDecision:
    decision_id: str
    current_state: str
    desired_state: str
    default_home_path: str
    home_resolution_order: tuple[str, ...]
    should_support_explicit_home: bool
    should_support_env_override: bool
    should_auto_create_home: bool
    target_version: str
    safety_notes: str


@dataclass(frozen=True)
class V042ProviderUXDecision:
    decision_id: str
    current_state: str
    desired_state: str
    provider_modes: tuple[str, ...]
    setup_command_target: str
    doctor_behavior_target: str
    completion_allowed_only_in_run: bool
    provider_doctor_completion_allowed: bool
    tool_calling_allowed: bool
    function_calling_allowed: bool
    secret_redaction_required: bool
    target_version: str


@dataclass(frozen=True)
class V042TraceUXDecision:
    decision_id: str
    current_state: str
    desired_state: str
    json_trace_stays_available: bool
    human_readable_timeline_required: bool
    run_history_required: bool
    provider_call_event_vs_transaction_count_must_be_clarified: bool
    target_version: str
    process_intelligence_notes: str


@dataclass(frozen=True)
class V042HumanReadableOutputNeed:
    need_id: str
    output_surface: str
    current_format: str
    desired_format: str
    target_user_value: str
    process_intelligence_value: str
    target_version: str


@dataclass(frozen=True)
class V042ProcessIntelligenceReviewCriterion:
    criterion_id: str
    title: str
    question: str
    expected_evidence: str
    applies_to: str
    target_version: str


@dataclass(frozen=True)
class V042ProcessIntelligenceReviewContract:
    contract_id: str
    criteria: tuple[V042ProcessIntelligenceReviewCriterion, ...]
    process_trace_review_required: bool
    reviewer_persona: str
    high_priority_findings_target: str


@dataclass(frozen=True)
class V042UserOperabilityRisk:
    risk_id: str
    title: str
    risk_class: str
    severity: str
    description: str
    mitigation: str
    target_version: str
    blocks_v0420: bool


@dataclass(frozen=True)
class V042UserOperabilityRiskRegister:
    register_id: str
    risks: tuple[V042UserOperabilityRisk, ...]
    high_risk_count: int
    blocks_v0420: bool


@dataclass(frozen=True)
class V042ClosedCapability:
    capability_id: str
    name: str
    closed: bool
    reason: str
    may_reopen_in_v042: bool
    required_gate_before_opening: str | None


@dataclass(frozen=True)
class V042ClosedCapabilityMatrix:
    matrix_id: str
    capabilities: tuple[V042ClosedCapability, ...]
    all_required_closed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042RoadmapItem:
    item_id: str
    version: str
    title: str
    user_value: str
    process_intelligence_value: str
    implementation_scope: str
    must_not_open: tuple[str, ...]
    exit_criteria: tuple[str, ...]
    depends_on: tuple[str, ...]


@dataclass(frozen=True)
class V042Roadmap:
    roadmap_id: str
    track_name: str
    items: tuple[V042RoadmapItem, ...]
    high_risk_expansion_deferred: bool
    user_operability_priority: bool
    process_intelligence_review_priority: bool


@dataclass(frozen=True)
class V0420ReadinessReport:
    v0416_user_test_evidence_captured: bool
    v0416_deterministic_mock_flow_interpreted: bool
    v042_track_identity_defined: bool
    v042_ux_pain_point_register_ready: bool
    v042_user_journey_contract_ready: bool
    v042_command_surface_review_ready: bool
    v042_default_home_decision_ready: bool
    v042_provider_ux_decision_ready: bool
    v042_trace_ux_decision_ready: bool
    v042_process_intelligence_review_contract_ready: bool
    v042_roadmap_ready: bool
    v0421_handoff_ready: bool
    integrated_restore_document_ready: bool
    ready_for_default_home_resolver_implementation: bool
    ready_for_quickstart_command: bool
    ready_for_provider_setup_command: bool
    ready_for_trace_timeline_command: bool
    ready_for_interactive_chat_shell: bool
    ready_for_read_only_skill_execution_as_actions: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_subagent_invocation: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V0421DefaultHomeQuickstartHandoff:
    handoff_id: str
    target_version: str
    title: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    exit_criteria: tuple[str, ...]


@dataclass(frozen=True)
class V0420IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0420IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0420IntegratedRestorePacket:
    packet_id: str
    single_integrated_doc_path: str
    separate_restore_doc_created: bool
    context_snapshot: V0420IntegratedRestoreContextSnapshot


@dataclass(frozen=True)
class V0420IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    suitable_for_new_session_handoff: bool
    required_sections: tuple[str, ...]


def create_v042_track_identity(**overrides: object) -> V042TrackIdentity:
    data = {
        "track_id": "v042-default-personal-runtime-ux-hardening",
        "version": V0420_VERSION,
        "track_name": V042_TRACK_NAME,
        "track_goal": "Make the Default Personal Runtime easier to use, inspect, diagnose, and improve from a user and Process Intelligence perspective.",
        "previous_track": V0416_TRACK_NAME,
        "starting_baseline_version": V0416_BASELINE_VERSION,
        "primary_user_review_mode": V042UserReviewMode.USER_FLOW_REVIEW.value,
        "process_intelligence_review_required": True,
        "high_risk_capability_expansion_allowed": False,
        "production_certified": False,
    }
    data.update(overrides)
    return V042TrackIdentity(**data)


def create_v0416_user_test_evidence(**overrides: object) -> V0416UserTestEvidence:
    data = {
        "evidence_id": "v0416-clean-home-deterministic-mock-user-test",
        "evidence_source": "user-reported clean-home v0.41.6 deterministic mock-provider flow",
        "test_home_kind": "fresh_temp_home",
        "fresh_home_used": True,
        "init_passed": True,
        "profile_status_passed": True,
        "provider_doctor_no_completion_passed": True,
        "mock_run_passed": True,
        "trace_recent_passed": True,
        "trace_summary_passed": True,
        "run_report_last_passed": True,
        "safety_denial_passed": True,
        "run_count": 1,
        "denial_count": 1,
        "provider_call_count_observed": 2,
        "provider_call_count_semantics": "event_count_not_transaction_count",
        "shell_execution_count": 0,
        "skill_execution_count": 0,
        "subagent_invocation_count": 0,
        "production_certification_count": 0,
        "total_events": 12,
        "deterministic_mock_flow_passed": True,
        "configured_provider_flow_verified": False,
    }
    data.update(overrides)
    return V0416UserTestEvidence(**data)


def interpret_v0416_user_test_evidence(
    evidence: V0416UserTestEvidence | None = None,
) -> V0416UserTestEvidenceInterpretation:
    evidence = evidence or create_v0416_user_test_evidence()
    unsafe_counts_zero = all(
        count == 0
        for count in (
            evidence.shell_execution_count,
            evidence.skill_execution_count,
            evidence.subagent_invocation_count,
            evidence.production_certification_count,
        )
    )
    passed = evidence.deterministic_mock_flow_passed and unsafe_counts_zero
    notes = (
        "configured provider flow remains supported by design but not manually verified",
        "provider_call_count currently counts provider call events, not transactions",
        "v0.42 should harden UX and reviewability before opening new capability",
    )
    return V0416UserTestEvidenceInterpretation(
        interpretation_id="v0416-clean-home-evidence-interpretation",
        evidence=evidence,
        v0416_passed=passed,
        v041_track_can_close=passed,
        ready_for_v042_ux_hardening=passed,
        blockers=() if passed else ("v0.41.6 deterministic mock flow did not pass",),
        non_blocking_notes=notes,
        recommended_next_track="v0.42 Default Personal Runtime UX Hardening Track",
    )


def create_v0416_known_note(
    note_id: str,
    title: str,
    description: str,
    *,
    severity: str = "medium",
    blocks_v0420: bool = False,
    recommended_target_version: str = "v0.42.1",
    recommendation: str = "",
) -> V0416KnownNote:
    return V0416KnownNote(
        note_id=note_id,
        title=title,
        description=description,
        severity=severity,
        blocks_v0420=blocks_v0420,
        recommended_target_version=recommended_target_version,
        recommendation=recommendation,
    )


def build_v0416_known_notes() -> tuple[V0416KnownNote, ...]:
    return (
        create_v0416_known_note(
            "explicit-home-required",
            "Explicit --home required in user flow",
            "run currently needs explicit --home in the clean-home flow; default-home UX should be improved.",
            recommended_target_version="v0.42.1",
            recommendation="Add resolver and quickstart while keeping explicit --home supported.",
        ),
        create_v0416_known_note(
            "provider-call-count-semantics",
            "Provider call count uses event-count semantics",
            "provider_call_count currently counts provider call events, not provider call transactions.",
            recommended_target_version="v0.42.3",
            recommendation="Clarify trace summary labels and human-readable trace output.",
        ),
        create_v0416_known_note(
            "configured-provider-not-manually-verified",
            "Configured real provider flow not manually verified",
            "The mock flow passed; configured real provider flow remains environment-dependent.",
            recommended_target_version="v0.42.2",
            recommendation="Add provider setup/status UX before asking users to test configured providers.",
        ),
        create_v0416_known_note(
            "package-version-metadata-mismatch",
            "Package metadata version may lag CLI runtime version",
            "pyproject metadata can show an older package version than the CLI runtime track.",
            recommended_target_version="v0.42.6",
            recommendation="Add version hygiene to diagnostic bundle and release review.",
        ),
        create_v0416_known_note(
            "json-trace-readability",
            "JSON trace output is hard to review repeatedly",
            "Raw JSON trace data is useful but not comfortable as the primary repeated review surface.",
            recommended_target_version="v0.42.3",
            recommendation="Keep JSON available and add a human-readable timeline.",
        ),
        create_v0416_known_note(
            "diagnostic-bundle-gap",
            "Diagnostic bundle gap",
            "When something goes wrong, the user needs one bundle/report suitable for GPT/Codex handoff.",
            recommended_target_version="v0.42.6",
            recommendation="Add a non-executing report bundle and feedback note surface.",
        ),
    )


def create_v042_ux_pain_point(
    kind: str,
    title: str,
    user_impact: str,
    process_intelligence_impact: str,
    recommended_target_version: str,
    recommended_resolution: str,
    *,
    pain_point_id: str | None = None,
    observed_in_v0416: bool = True,
) -> V042UXPainPoint:
    return V042UXPainPoint(
        pain_point_id=pain_point_id or f"pain-{kind}",
        kind=kind,
        title=title,
        observed_in_v0416=observed_in_v0416,
        user_impact=user_impact,
        process_intelligence_impact=process_intelligence_impact,
        recommended_target_version=recommended_target_version,
        recommended_resolution=recommended_resolution,
        high_risk_capability_required=False,
    )


def build_v042_ux_pain_point_register() -> tuple[V042UXPainPoint, ...]:
    return (
        create_v042_ux_pain_point(
            V042UXPainPointKind.DEFAULT_HOME_FRICTION.value,
            "Default home friction",
            "User must repeat --home across the flow.",
            "Process evidence can split across homes when commands are inconsistent.",
            "v0.42.1",
            "Define explicit/env/platform resolution and quickstart-owned creation.",
        ),
        create_v042_ux_pain_point(
            V042UXPainPointKind.PROVIDER_SETUP_FRICTION.value,
            "Provider setup friction",
            "Configured-provider path is hard to prepare and diagnose.",
            "Provider objects and provider status are difficult to review before a run.",
            "v0.42.2",
            "Add provider setup/status UX without allowing doctor completion.",
        ),
        create_v042_ux_pain_point(
            V042UXPainPointKind.PROVIDER_COUNT_SEMANTICS.value,
            "Provider count semantics",
            "User may misread event counts as provider transactions.",
            "Trace summary needs event-vs-transaction clarity.",
            "v0.42.3",
            "Clarify labels and timeline grouping.",
        ),
        create_v042_ux_pain_point(
            V042UXPainPointKind.VERSION_METADATA_MISMATCH.value,
            "Version metadata mismatch",
            "Package metadata may not match runtime release language.",
            "Diagnostic evidence can become confusing during handoff.",
            "v0.42.6",
            "Include package/runtime version comparison in diagnostic bundle.",
        ),
        create_v042_ux_pain_point(
            V042UXPainPointKind.JSON_TRACE_READABILITY.value,
            "JSON trace readability",
            "Raw trace JSON is too dense for repeated review.",
            "Process reconstruction is possible but not ergonomic.",
            "v0.42.3",
            "Add human-readable trace timeline while keeping JSON available.",
        ),
        create_v042_ux_pain_point(
            V042UXPainPointKind.DIAGNOSTIC_HANDOFF_GAP.value,
            "Diagnostic handoff gap",
            "User lacks one safe report to hand to GPT/Codex when debugging.",
            "Failure evidence can be incomplete or scattered.",
            "v0.42.6",
            "Add report bundle and feedback note surfaces.",
        ),
        create_v042_ux_pain_point(
            V042UXPainPointKind.RUN_HISTORY_VISIBILITY.value,
            "Run history visibility",
            "User cannot comfortably compare recent runs.",
            "Run process instances need a review surface.",
            "v0.42.3",
            "Add run history and run show surfaces.",
        ),
        create_v042_ux_pain_point(
            V042UXPainPointKind.SESSION_VISIBILITY.value,
            "Session visibility",
            "User cannot inspect the latest session in a compact way.",
            "Session/run linkage needs user-facing evidence.",
            "v0.42.3",
            "Add session show last after trace/run surfaces are stable.",
        ),
        create_v042_ux_pain_point(
            V042UXPainPointKind.USER_COMMAND_DISCOVERABILITY.value,
            "Command discoverability",
            "User has to remember a long sequence of commands.",
            "Review workflows are harder to repeat consistently.",
            "v0.42.1",
            "Add quickstart guidance before adding provider setup or trace timeline.",
        ),
    )


def create_v042_user_persona(
    persona_id: str,
    name: str,
    review_strength: str,
    review_limit: str,
    needs_from_v042: Iterable[str],
) -> V042UserPersona:
    return V042UserPersona(
        persona_id=persona_id,
        name=name,
        review_strength=review_strength,
        review_limit=review_limit,
        needs_from_v042=tuple(needs_from_v042),
    )


def build_v042_user_personas() -> tuple[V042UserPersona, ...]:
    return (
        create_v042_user_persona(
            "primary_user_operator",
            "Primary User Operator",
            "Runs ChantaCore locally and reviews behavior.",
            "Cannot reasonably review every code path directly.",
            ("short setup path", "human-readable command output", "safe diagnostic handoff"),
        ),
        create_v042_user_persona(
            "process_intelligence_reviewer",
            "Process Intelligence Reviewer",
            "Evaluates event, trace, object, session, provider, and denial semantics.",
            "Needs reconstructed evidence, not raw implementation details alone.",
            ("process instance clarity", "object linkage", "event/transaction semantics"),
        ),
        create_v042_user_persona(
            "codex_implementer",
            "Codex Implementer",
            "Implements internals and tests.",
            "May over-focus on code correctness without user-operability evidence.",
            ("bounded scope", "clear contracts", "regression tests"),
        ),
        create_v042_user_persona(
            "gpt_design_synthesizer",
            "GPT Mode Vera Design Synthesizer",
            "Synthesizes design direction from user test results.",
            "Cannot inspect repo state unless evidence is supplied.",
            ("handoff bundle", "restore prompt", "known pain points"),
        ),
    )


def create_v042_user_journey_step(
    order_index: int,
    step_kind: str,
    current_v0416_command: str,
    desired_v042_command: str,
    current_friction: str,
    target_user_experience: str,
    process_intelligence_review_need: str,
    target_version: str,
) -> V042UserJourneyStep:
    return V042UserJourneyStep(
        step_id=f"journey-{order_index:02d}-{step_kind}",
        order_index=order_index,
        step_kind=step_kind,
        current_v0416_command=current_v0416_command,
        desired_v042_command=desired_v042_command,
        current_friction=current_friction,
        target_user_experience=target_user_experience,
        process_intelligence_review_need=process_intelligence_review_need,
        target_version=target_version,
        opens_high_risk_capability=False,
    )


def build_v042_user_journey_contract() -> V042UserJourneyContract:
    steps = (
        create_v042_user_journey_step(1, "install", "py -m pip install -e .", "py -m pip install -e .", "Install is manual but acceptable.", "User can install and confirm CLI exists.", "Install step is distinct from runtime process evidence.", "v0.42.0"),
        create_v042_user_journey_step(2, "first_doctor", "chanta-cli doctor", "chanta-cli doctor", "Doctor output is useful but not full journey guidance.", "User sees runtime status and closed capabilities.", "Doctor evidence should identify runtime state without executing providers.", "v0.42.1"),
        create_v042_user_journey_step(3, "quickstart", "chanta-cli init default-personal --home <home>", "chanta-cli quickstart", "Default home and command order are manual.", "User can initialize and run mock flow with guided defaults.", "Home resolution should make process evidence land in one store.", "v0.42.1"),
        create_v042_user_journey_step(4, "profile_status", "chanta-cli profile status --profile default-personal --home <home>", "chanta-cli profile status", "Needs repeated --home.", "User can inspect profile readiness from default home.", "Profile object should be visible in the review path.", "v0.42.1"),
        create_v042_user_journey_step(5, "provider_status", "chanta-cli provider doctor --profile default-personal --home <home> --no-completion", "chanta-cli provider status", "Provider setup is not user-friendly.", "User can see mock/configured provider readiness without completion.", "Provider config object and redaction status should be reviewable.", "v0.42.2"),
        create_v042_user_journey_step(6, "mock_run", "chanta-cli run --profile default-personal --home <home> --provider mock <prompt>", "chanta-cli run --provider mock <prompt>", "Works but carries home friction.", "User can run deterministic mock path after quickstart.", "Mock run should create a clear run process instance.", "v0.42.1"),
        create_v042_user_journey_step(7, "configured_provider_run", "chanta-cli run --profile default-personal --home <home> <prompt>", "chanta-cli run <prompt>", "Configured provider readiness is hard to diagnose.", "User can knowingly run configured provider only after status/setup.", "Provider text must be marked untrusted and linked to run.", "v0.42.2"),
        create_v042_user_journey_step(8, "trace_review", "chanta-cli trace recent --profile default-personal --home <home>", "chanta-cli trace timeline", "JSON/recent trace output is dense.", "User can read a timeline of run/provider/session/denial events.", "Trace must support process reconstruction.", "v0.42.3"),
        create_v042_user_journey_step(9, "run_history_review", "chanta-cli run-report last --profile default-personal --home <home>", "chanta-cli run history", "Only last run report exists.", "User can compare recent runs.", "Run objects should be listable as process instances.", "v0.42.3"),
        create_v042_user_journey_step(10, "session_review", "chanta-cli session list --profile default-personal --home <home>", "chanta-cli session show last", "Session visibility is shallow.", "User can inspect latest session linkage.", "Session/run linkage should be explicit.", "v0.42.3"),
        create_v042_user_journey_step(11, "denial_test", "chanta-cli safety check-command --profile default-personal --home <home> --command <dangerous>", "chanta-cli safety check-command --command <dangerous>", "Works but review output is not yet a full denial narrative.", "User can prove dangerous command text was not executed.", "Denial evidence must prove non-execution.", "v0.42.3"),
        create_v042_user_journey_step(12, "diagnostic_bundle", "manual collection", "chanta-cli report bundle", "Evidence is scattered when debugging.", "User can hand one report to GPT/Codex.", "Bundle should preserve trace/process evidence and safety counts.", "v0.42.6"),
        create_v042_user_journey_step(13, "feedback_note", "manual note", "chanta-cli feedback note", "User feedback is not attached to runtime evidence.", "User can record review notes without opening automation.", "Feedback note should become review context, not autonomous instruction.", "v0.42.6"),
    )
    return V042UserJourneyContract(
        contract_id="v042-user-journey-contract",
        title="Default Personal Runtime User Journey Contract",
        baseline_version=V0416_BASELINE_VERSION,
        steps=steps,
        user_can_review_without_code=True,
        process_trace_review_required=True,
        high_risk_capabilities_remain_closed=True,
    )


def create_v042_command_surface_review_item(
    item_id: str,
    command_name: str,
    current_state: str,
    desired_state: str,
    user_friction: str,
    process_intelligence_value: str,
    target_version: str,
    *,
    should_remain_closed: bool = False,
) -> V042CommandSurfaceReviewItem:
    return V042CommandSurfaceReviewItem(
        item_id=item_id,
        command_name=command_name,
        current_state=current_state,
        desired_state=desired_state,
        user_friction=user_friction,
        process_intelligence_value=process_intelligence_value,
        target_version=target_version,
        should_remain_closed=should_remain_closed,
    )


def build_v042_command_surface_review() -> V042CommandSurfaceReview:
    items = (
        create_v042_command_surface_review_item("quickstart", "chanta-cli quickstart", "not implemented", "guided default-home mock flow", "User repeats command sequence manually.", "Creates a consistent journey start.", "v0.42.1"),
        create_v042_command_surface_review_item("doctor", "chanta-cli doctor", "available", "journey-aware status", "Does not yet guide next step enough.", "Shows closed capabilities and runtime state.", "v0.42.1"),
        create_v042_command_surface_review_item("provider-setup", "chanta-cli provider setup", "not implemented", "safe setup helper", "Provider configuration is hard to start.", "Creates reviewable provider config state.", "v0.42.2"),
        create_v042_command_surface_review_item("provider-status", "chanta-cli provider status", "doctor exists with --no-completion", "readable status view", "Doctor language is not enough for setup review.", "Makes provider object state clear.", "v0.42.2"),
        create_v042_command_surface_review_item("run", "chanta-cli run", "available", "default-home-aware single-turn run", "Needs --home in clean flow.", "Creates run/provider/session events.", "v0.42.1"),
        create_v042_command_surface_review_item("trace-timeline", "chanta-cli trace timeline", "not implemented", "human-readable event timeline", "Trace JSON is dense.", "Supports process reconstruction.", "v0.42.3"),
        create_v042_command_surface_review_item("run-history", "chanta-cli run history", "not implemented", "recent run list", "Only last report is available.", "Run process instances become inspectable.", "v0.42.3"),
        create_v042_command_surface_review_item("run-show-last", "chanta-cli run show last", "run-report last exists", "readable last-run view", "Command naming is not yet user-obvious.", "Links latest run evidence.", "v0.42.3"),
        create_v042_command_surface_review_item("session-show-last", "chanta-cli session show last", "not implemented", "latest session detail", "Session store is not easy to review.", "Links session and run objects.", "v0.42.3"),
        create_v042_command_surface_review_item("report-bundle", "chanta-cli report bundle", "not implemented", "safe diagnostic bundle", "Debug evidence is scattered.", "Creates handoff evidence.", "v0.42.6"),
        create_v042_command_surface_review_item("feedback-note", "chanta-cli feedback note", "not implemented", "manual feedback record", "User notes are outside runtime review.", "Adds review note as evidence, not instruction.", "v0.42.6"),
        create_v042_command_surface_review_item("shell", "shell/edit/apply/subagent commands", "denied/closed", "remain closed", "Unsafe if opened without new gate.", "Closed capability visibility is itself review evidence.", "not_in_v0.42.0", should_remain_closed=True),
    )
    return V042CommandSurfaceReview(
        review_id="v042-command-surface-review",
        items=items,
        default_home_required=True,
        human_readable_outputs_required=True,
        closed_capabilities_visible_to_user=True,
    )


def create_v042_default_home_ux_decision() -> V042DefaultHomeUXDecision:
    return V042DefaultHomeUXDecision(
        decision_id="v042-default-home-ux-decision",
        current_state="User flow commonly requires explicit --home to keep evidence in one store.",
        desired_state="Resolve home through explicit flag, environment override, then platform default.",
        default_home_path="%LOCALAPPDATA%\\ChantaCore",
        home_resolution_order=("explicit --home", "CHANTACORE_HOME", "platform default local app data"),
        should_support_explicit_home=True,
        should_support_env_override=True,
        should_auto_create_home=False,
        target_version="v0.42.1",
        safety_notes="Auto-create should occur only through quickstart/init, never silently from every command.",
    )


def create_v042_provider_ux_decision() -> V042ProviderUXDecision:
    return V042ProviderUXDecision(
        decision_id="v042-provider-ux-decision",
        current_state="Mock path works; configured provider flow is supported but hard to set up and manually unverified.",
        desired_state="Expose provider setup/status UX while keeping doctor no-completion.",
        provider_modes=("mock", "local_openai_compatible", "configured_provider"),
        setup_command_target="chanta-cli provider setup",
        doctor_behavior_target="doctor/status may inspect metadata and safe reachability only; no completion",
        completion_allowed_only_in_run=True,
        provider_doctor_completion_allowed=False,
        tool_calling_allowed=False,
        function_calling_allowed=False,
        secret_redaction_required=True,
        target_version="v0.42.2",
    )


def create_v042_trace_ux_decision() -> V042TraceUXDecision:
    return V042TraceUXDecision(
        decision_id="v042-trace-ux-decision",
        current_state="JSON trace and summary exist, but repeated human review is difficult.",
        desired_state="Keep JSON and add human-readable timeline plus run history.",
        json_trace_stays_available=True,
        human_readable_timeline_required=True,
        run_history_required=True,
        provider_call_event_vs_transaction_count_must_be_clarified=True,
        target_version="v0.42.3",
        process_intelligence_notes="Provider call event count must be distinguished from provider call transaction count.",
    )


def create_v042_human_readable_output_need(
    need_id: str,
    output_surface: str,
    current_format: str,
    desired_format: str,
    target_user_value: str,
    process_intelligence_value: str,
    target_version: str,
) -> V042HumanReadableOutputNeed:
    return V042HumanReadableOutputNeed(
        need_id=need_id,
        output_surface=output_surface,
        current_format=current_format,
        desired_format=desired_format,
        target_user_value=target_user_value,
        process_intelligence_value=process_intelligence_value,
        target_version=target_version,
    )


def build_v042_human_readable_output_needs() -> tuple[V042HumanReadableOutputNeed, ...]:
    return (
        create_v042_human_readable_output_need("trace-timeline", "trace timeline", "JSON/recent event list", "ordered narrative event timeline", "Review runtime behavior quickly.", "Reconstruct process instance flow.", "v0.42.3"),
        create_v042_human_readable_output_need("run-history", "run history", "last report only", "recent run table", "Compare runs without reading raw stores.", "Review run objects as process instances.", "v0.42.3"),
        create_v042_human_readable_output_need("run-show-last", "run show last", "run-report last", "clear last-run detail view", "Inspect latest prompt/response summary safely.", "Link run/provider/session evidence.", "v0.42.3"),
        create_v042_human_readable_output_need("session-show-last", "session show last", "session list", "latest session detail", "Understand what was appended.", "Review session/run object linkage.", "v0.42.3"),
        create_v042_human_readable_output_need("provider-status", "provider status", "provider doctor JSON", "readable provider readiness summary", "Know whether mock/configured provider is ready.", "Review provider object status.", "v0.42.2"),
        create_v042_human_readable_output_need("diagnostic-bundle", "diagnostic bundle", "manual evidence collection", "single safe handoff report", "Share one report for debugging.", "Preserve trace, status, denial, and version evidence.", "v0.42.6"),
    )


def create_v042_process_intelligence_review_criterion(
    criterion_id: str,
    title: str,
    question: str,
    expected_evidence: str,
    applies_to: str,
    target_version: str,
) -> V042ProcessIntelligenceReviewCriterion:
    return V042ProcessIntelligenceReviewCriterion(
        criterion_id=criterion_id,
        title=title,
        question=question,
        expected_evidence=expected_evidence,
        applies_to=applies_to,
        target_version=target_version,
    )


def build_v042_process_intelligence_review_contract() -> V042ProcessIntelligenceReviewContract:
    criteria = (
        create_v042_process_intelligence_review_criterion("run-process-instance", "Run as process instance", "Can a run be reconstructed as a process instance?", "run id, started/completed events, provider/session refs", "run/trace", "v0.42.3"),
        create_v042_process_intelligence_review_criterion("object-links", "Object links", "Are run/session/provider/denial objects linked clearly?", "object refs for run, session, provider request/response, denial", "trace/report", "v0.42.3"),
        create_v042_process_intelligence_review_criterion("semantic-event-names", "Semantic event names", "Are event names semantically meaningful?", "event names describe user-visible runtime steps", "trace", "v0.42.3"),
        create_v042_process_intelligence_review_criterion("event-vs-transaction-count", "Event count vs transaction count", "Are event count and transaction count distinguished?", "provider call event-count labels and transaction grouping notes", "trace summary", "v0.42.3"),
        create_v042_process_intelligence_review_criterion("denial-non-execution", "Denial proves non-execution", "Does denial evidence prove non-execution?", "denial record with blocked true and executed false", "safety denial", "v0.42.3"),
        create_v042_process_intelligence_review_criterion("provider-text-untrusted", "Provider text remains untrusted", "Is provider text clearly marked untrusted?", "run report/timeline labels provider text as untrusted text output", "run/provider", "v0.42.3"),
        create_v042_process_intelligence_review_criterion("unsafe-counts-visible", "Unsafe counts visible", "Can trace summary reveal unsafe capability counts?", "shell, skill, subagent, production counts shown as zero", "trace summary", "v0.42.3"),
        create_v042_process_intelligence_review_criterion("diagnostic-handoff", "Diagnostic handoff evidence", "Can the user hand off enough evidence to GPT/Codex for debugging?", "bundle includes version, home, trace summary, last run, denials, provider status", "diagnostic bundle", "v0.42.6"),
    )
    return V042ProcessIntelligenceReviewContract(
        contract_id="v042-process-intelligence-review-contract",
        criteria=criteria,
        process_trace_review_required=True,
        reviewer_persona="process_intelligence_reviewer",
        high_priority_findings_target="v0.42.x UX hardening backlog",
    )


def create_v042_user_operability_risk(
    risk_id: str,
    title: str,
    risk_class: str,
    severity: str,
    description: str,
    mitigation: str,
    target_version: str,
    *,
    blocks_v0420: bool = False,
) -> V042UserOperabilityRisk:
    return V042UserOperabilityRisk(
        risk_id=risk_id,
        title=title,
        risk_class=risk_class,
        severity=severity,
        description=description,
        mitigation=mitigation,
        target_version=target_version,
        blocks_v0420=blocks_v0420,
    )


def build_v042_user_operability_risk_register() -> V042UserOperabilityRiskRegister:
    risks = (
        create_v042_user_operability_risk("risk-usability-home", "Default home flow confusion", "usability", "medium", "Repeated --home makes first-run flow error-prone.", "Add default home resolver and quickstart.", "v0.42.1"),
        create_v042_user_operability_risk("risk-provider-config", "Configured provider setup confusion", "provider_config", "medium", "Real provider setup can fail without clear status.", "Add provider setup/status UX while keeping completion closed in doctor.", "v0.42.2"),
        create_v042_user_operability_risk("risk-trace-semantics", "Trace semantics misread", "trace_semantics", "medium", "Provider call event count can be mistaken for transaction count.", "Clarify timeline and summary wording.", "v0.42.3"),
        create_v042_user_operability_risk("risk-safety-boundary", "UX work accidentally opens capability", "safety_boundary", "high", "Usability changes can accidentally turn into runtime expansion.", "Closed capability matrix and readiness false flags stay explicit.", "v0.42.0"),
        create_v042_user_operability_risk("risk-version-hygiene", "Version metadata mismatch", "version_hygiene", "low", "Package metadata may lag CLI/runtime release labels.", "Add diagnostic version comparison.", "v0.42.6"),
        create_v042_user_operability_risk("risk-user-diagnostic", "Incomplete handoff evidence", "user_diagnostic", "medium", "User may not gather enough evidence for GPT/Codex debugging.", "Create diagnostic bundle and feedback note.", "v0.42.6"),
        create_v042_user_operability_risk("risk-scope-creep", "Scope creep into unsafe runtime", "scope_creep", "high", "Roadmap items may be misread as permission to open shell/edit/apply/loops.", "Mark roadmap as contract-only until each gate is separately implemented.", "v0.42.0"),
    )
    return V042UserOperabilityRiskRegister(
        register_id="v042-user-operability-risk-register",
        risks=risks,
        high_risk_count=sum(1 for risk in risks if risk.severity == "high"),
        blocks_v0420=any(risk.blocks_v0420 for risk in risks),
    )


REQUIRED_CLOSED_CAPABILITIES = (
    "provider_doctor_completion",
    "provider_tool_calling",
    "function_calling",
    "general_agent_loop",
    "multi_step_agent_loop",
    "shell_execution",
    "file_edit",
    "patch_apply",
    "test_execution_through_cli",
    "subagent_invocation",
    "child_session_creation",
    "autonomous_retry_loop",
    "mission_scheduler",
    "mutable_memory_automation",
    "dominion_runtime",
    "production_certification",
)


def create_v042_closed_capability(
    capability_id: str,
    name: str | None = None,
    *,
    may_reopen_in_v042: bool = False,
    required_gate_before_opening: str | None = None,
) -> V042ClosedCapability:
    return V042ClosedCapability(
        capability_id=capability_id,
        name=name or capability_id,
        closed=True,
        reason="v0.42.0 is metadata/contract/roadmap only and does not open this capability.",
        may_reopen_in_v042=may_reopen_in_v042,
        required_gate_before_opening=required_gate_before_opening,
    )


def build_v042_closed_capability_matrix() -> V042ClosedCapabilityMatrix:
    may_consider_later = {
        "provider_doctor_completion": False,
        "provider_tool_calling": False,
        "function_calling": False,
        "general_agent_loop": False,
        "multi_step_agent_loop": False,
        "shell_execution": False,
        "file_edit": False,
        "patch_apply": False,
        "test_execution_through_cli": False,
        "subagent_invocation": False,
        "child_session_creation": False,
        "autonomous_retry_loop": False,
        "mission_scheduler": False,
        "mutable_memory_automation": False,
        "dominion_runtime": False,
        "production_certification": False,
    }
    capabilities = tuple(
        create_v042_closed_capability(
            capability,
            may_reopen_in_v042=may_consider_later[capability],
            required_gate_before_opening=None,
        )
        for capability in REQUIRED_CLOSED_CAPABILITIES
    )
    return V042ClosedCapabilityMatrix(
        matrix_id="v042-closed-capability-matrix",
        capabilities=capabilities,
        all_required_closed=all(capability.closed for capability in capabilities),
        production_certified=False,
    )


def create_v042_roadmap_item(
    version: str,
    title: str,
    user_value: str,
    process_intelligence_value: str,
    implementation_scope: str,
    must_not_open: Iterable[str],
    exit_criteria: Iterable[str],
    depends_on: Iterable[str] = (),
) -> V042RoadmapItem:
    return V042RoadmapItem(
        item_id=f"roadmap-{version.replace('.', '').replace('v', 'v')}",
        version=version,
        title=title,
        user_value=user_value,
        process_intelligence_value=process_intelligence_value,
        implementation_scope=implementation_scope,
        must_not_open=tuple(must_not_open),
        exit_criteria=tuple(exit_criteria),
        depends_on=tuple(depends_on),
    )


def build_v042_roadmap() -> V042Roadmap:
    common_closed = ("shell_execution", "file_edit", "patch_apply", "subagent_invocation", "general_agent_loop", "dominion_runtime", "production_certification")
    items = (
        create_v042_roadmap_item("v0.42.0", "UX Baseline & User Journey Contract", "Defines the user-operability baseline.", "Defines PI review criteria and closed capability matrix.", "Metadata, contracts, roadmap, and integrated restore document only.", common_closed, ("v0.41.6 evidence recorded", "single integrated document exists")),
        create_v042_roadmap_item("v0.42.1", "Default Home Resolver & Quickstart", "Removes repeated --home friction.", "Keeps process evidence in a consistent home.", "Implement resolver and quickstart-owned initialization.", common_closed + ("provider_setup_command",), ("explicit/env/platform resolution works", "quickstart guides mock flow"), ("v0.42.0",)),
        create_v042_roadmap_item("v0.42.2", "Provider Setup UX", "Makes provider preparation understandable.", "Makes provider config/status reviewable.", "Add provider setup/status without doctor completion.", common_closed + ("provider_doctor_completion", "provider_tool_calling", "function_calling"), ("mock/local/configured provider status is readable", "secrets remain redacted"), ("v0.42.1",)),
        create_v042_roadmap_item("v0.42.3", "Human-readable Trace / Run History", "Makes runtime review repeatable.", "Improves run/session/provider/denial process reconstruction.", "Add timeline, run history, run show, and session show surfaces.", common_closed, ("timeline clarifies event-vs-transaction counts", "run history links process objects"), ("v0.42.2",)),
        create_v042_roadmap_item("v0.42.4", "Interactive Manual Chat Shell", "Allows manual multi-turn conversation without autonomous loop.", "Each user turn remains a single process instance.", "Manual loop only: user input -> single-turn run -> response -> trace -> next user input.", common_closed + ("multi_step_agent_loop", "autonomous_retry_loop"), ("no autonomous continuation", "each turn is traceable"), ("v0.42.3",)),
        create_v042_roadmap_item("v0.42.5", "Bounded Read-only Skill Execution", "Allows safe local metadata/status/report skill actions first.", "Adds skill execution evidence under a bounded gate.", "Only bounded read-only metadata/status/report skills; no broad scan, shell, edit, or apply.", common_closed + ("broad_filesystem_scan",), ("gate exists", "safe local read-only skills only"), ("v0.42.4",)),
        create_v042_roadmap_item("v0.42.6", "Diagnostic Bundle & User Feedback Loop", "Creates one handoff artifact when something fails.", "Bundles trace, version, provider, denial, run, and user feedback evidence.", "Add non-executing report bundle and manual feedback note.", common_closed, ("bundle contains required evidence", "feedback note does not become autonomous instruction"), ("v0.42.5",)),
    )
    return V042Roadmap(
        roadmap_id="v042-roadmap",
        track_name=V042_TRACK_NAME,
        items=items,
        high_risk_expansion_deferred=True,
        user_operability_priority=True,
        process_intelligence_review_priority=True,
    )


def create_v0420_readiness_report() -> V0420ReadinessReport:
    return V0420ReadinessReport(
        v0416_user_test_evidence_captured=True,
        v0416_deterministic_mock_flow_interpreted=True,
        v042_track_identity_defined=True,
        v042_ux_pain_point_register_ready=True,
        v042_user_journey_contract_ready=True,
        v042_command_surface_review_ready=True,
        v042_default_home_decision_ready=True,
        v042_provider_ux_decision_ready=True,
        v042_trace_ux_decision_ready=True,
        v042_process_intelligence_review_contract_ready=True,
        v042_roadmap_ready=True,
        v0421_handoff_ready=True,
        integrated_restore_document_ready=True,
        ready_for_default_home_resolver_implementation=False,
        ready_for_quickstart_command=False,
        ready_for_provider_setup_command=False,
        ready_for_trace_timeline_command=False,
        ready_for_interactive_chat_shell=False,
        ready_for_read_only_skill_execution_as_actions=False,
        ready_for_provider_doctor_completion=False,
        ready_for_provider_tool_calling=False,
        ready_for_function_calling=False,
        ready_for_general_agent_loop=False,
        ready_for_multi_step_agent_loop=False,
        ready_for_shell_execution=False,
        ready_for_file_edit=False,
        ready_for_patch_apply=False,
        ready_for_subagent_invocation=False,
        ready_for_autonomous_retry_loop=False,
        ready_for_dominion_runtime=False,
        production_certified=False,
    )


def create_v0421_default_home_quickstart_handoff() -> V0421DefaultHomeQuickstartHandoff:
    return V0421DefaultHomeQuickstartHandoff(
        handoff_id="v0421-default-home-quickstart-handoff",
        target_version="v0.42.1",
        title="Default Home Resolver & Quickstart",
        recommended_focus=(
            "default home resolver",
            "CHANTACORE_HOME environment override",
            "explicit --home remains supported",
            "platform default %LOCALAPPDATA%\\ChantaCore",
            "chanta-cli quickstart",
            "quickstart guides init/profile/provider/mock run",
        ),
        must_not_open=(
            "provider setup wizard",
            "provider doctor completion",
            "tool calling",
            "function calling",
            "general AgentLoop",
            "shell/edit/apply/subagent",
        ),
        exit_criteria=(
            "commands can use explicit/env/platform home consistently",
            "quickstart initializes only through approved init path",
            "mock flow remains deterministic",
            "all v0.41.6 safety boundaries remain closed",
        ),
    )


REQUIRED_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "Project Context for New Codex Session",
    "v0.41.6 User Test Evidence",
    "v0.41.6 Final Interpretation",
    "Known Notes from v0.41.6",
    "v0.42 Track Goal",
    "v0.42 User Personas",
    "v0.42 User Journey Contract",
    "v0.42 Command Surface Review",
    "Default Home UX Decision",
    "Provider UX Decision",
    "Trace UX Decision",
    "Human-readable Output Needs",
    "Process Intelligence Review Contract",
    "User Operability Risk Register",
    "Closed Capability Matrix",
    "v0.42 Roadmap",
    "Runtime Opening Status",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Expected Test Interpretation",
    "Withdrawal Conditions",
    "v0.42.1 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)

_RESTORE_SECTION_IDS = {
    "Restore Purpose": "restore_purpose",
    "One-Screen Restore Summary": "one_screen_restore_summary",
    "Current Version and Track Identity": "current_version_and_track",
    "Project Context for New Codex Session": "project_context_for_new_codex_session",
    "v0.41.6 User Test Evidence": "v0416_user_test_evidence",
    "v0.41.6 Final Interpretation": "v0416_final_interpretation",
    "Known Notes from v0.41.6": "known_notes_from_v0416",
    "v0.42 Track Goal": "v042_track_goal",
    "v0.42 User Personas": "v042_user_personas",
    "v0.42 User Journey Contract": "v042_user_journey_contract",
    "v0.42 Command Surface Review": "v042_command_surface_review",
    "Default Home UX Decision": "default_home_ux_decision",
    "Provider UX Decision": "provider_ux_decision",
    "Trace UX Decision": "trace_ux_decision",
    "Human-readable Output Needs": "human_readable_output_needs",
    "Process Intelligence Review Contract": "process_intelligence_review_contract",
    "User Operability Risk Register": "user_operability_risk_register",
    "Closed Capability Matrix": "closed_capability_matrix",
    "v0.42 Roadmap": "v042_roadmap",
    "Runtime Opening Status": "runtime_opening_status",
    "Still-Closed Capabilities": "still_closed_capabilities",
    "Required Test Commands": "required_test_commands",
    "Expected Test Interpretation": "expected_test_interpretation",
    "Withdrawal Conditions": "withdrawal_conditions",
    "v0.42.1 Recommended Next Step": "v0421_handoff",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session": "copy_paste_restore_prompt",
}


def create_v0420_integrated_restore_sections() -> tuple[V0420IntegratedRestoreSection, ...]:
    return tuple(
        V0420IntegratedRestoreSection(
            section_id=_RESTORE_SECTION_IDS[section],
            title=section,
            required=True,
        )
        for section in REQUIRED_RESTORE_SECTIONS
    )


def create_v0420_integrated_restore_context_snapshot() -> V0420IntegratedRestoreContextSnapshot:
    return V0420IntegratedRestoreContextSnapshot(
        current_version="v0.42.0 Default Personal Runtime UX Baseline & User Journey Contract",
        current_track="v0.42 Default Personal Runtime UX Hardening Track",
        baseline_versions=(
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            "v0.41.1 Installable CLI Bootstrap & Doctor",
            "v0.41.2 Prompt Assembly & Session Store",
            "v0.41.3 Safe Provider Probe & Read-only Skill Registry",
            "v0.41.4 Minimal Single-turn Provider-backed Run",
            "v0.41.5 Event Trace Emission & Runtime Report",
            "v0.41.6 Installable Default Personal User Test Release",
            "v0.42.0 Default Personal Runtime UX Baseline & User Journey Contract",
        ),
        open_capabilities=(
            "v0416_user_test_evidence_record",
            "v042_track_identity",
            "v042_ux_pain_point_register",
            "v042_user_journey_contract",
            "v042_command_surface_review",
            "default_home_ux_decision_record",
            "provider_ux_decision_record",
            "trace_ux_decision_record",
            "process_intelligence_review_contract",
            "user_operability_risk_register",
            "closed_capability_matrix",
            "v042_roadmap",
            "v0421_handoff",
            "integrated_restore_document",
        ),
        closed_capabilities=(
            "default_home_resolver_implementation",
            "quickstart_command",
            "provider_setup_command",
            "trace_timeline_command",
            "run_history_command",
            "interactive_chat_shell",
            "read_only_skill_execution_as_actions",
            "provider_doctor_completion",
            "provider_tool_calling",
            "function_calling",
            "general_agent_loop",
            "multi_step_agent_loop",
            "shell_execution",
            "file_edit",
            "patch_apply",
            "test_execution_through_cli",
            "subagent_invocation",
            "child_session_creation",
            "autonomous_retry_loop",
            "dominion_runtime",
            "production_certification",
        ),
    )


def create_v0420_integrated_restore_packet() -> V0420IntegratedRestorePacket:
    return V0420IntegratedRestorePacket(
        packet_id="v0420-integrated-restore-packet",
        single_integrated_doc_path=INTEGRATED_DOC_PATH,
        separate_restore_doc_created=False,
        context_snapshot=create_v0420_integrated_restore_context_snapshot(),
    )


def create_v0420_integrated_restore_document_manifest(
    present_sections: Iterable[str] | None = None,
) -> V0420IntegratedRestoreDocumentManifest:
    present = set(present_sections or REQUIRED_RESTORE_SECTIONS)
    suitable = all(section in present for section in REQUIRED_RESTORE_SECTIONS)
    return V0420IntegratedRestoreDocumentManifest(
        manifest_id="v0420-integrated-restore-document-manifest",
        integrated_doc_required=True,
        separate_restore_doc_allowed=False,
        separate_restore_doc_created=False,
        copy_paste_restore_prompt_required=True,
        suitable_for_new_session_handoff=suitable,
        required_sections=REQUIRED_RESTORE_SECTIONS,
    )


__all__ = [
    "INTEGRATED_DOC_PATH",
    "REQUIRED_CLOSED_CAPABILITIES",
    "REQUIRED_RESTORE_SECTIONS",
    "V0416UserTestEvidence",
    "V0416UserTestEvidenceInterpretation",
    "V0416KnownNote",
    "V0420_FULL_NAME",
    "V0420_VERSION",
    "V0420IntegratedRestoreContextSnapshot",
    "V0420IntegratedRestoreDocumentManifest",
    "V0420IntegratedRestorePacket",
    "V0420IntegratedRestoreSection",
    "V0420ReadinessReport",
    "V0421DefaultHomeQuickstartHandoff",
    "V042ClosedCapability",
    "V042ClosedCapabilityMatrix",
    "V042CommandSurfaceReview",
    "V042CommandSurfaceReviewItem",
    "V042DefaultHomeUXDecision",
    "V042HumanReadableOutputNeed",
    "V042ProcessIntelligenceReviewContract",
    "V042ProcessIntelligenceReviewCriterion",
    "V042ProviderUXDecision",
    "V042Roadmap",
    "V042RoadmapItem",
    "V042TraceUXDecision",
    "V042TrackIdentity",
    "V042UXPainPoint",
    "V042UXPainPointKind",
    "V042UserJourneyContract",
    "V042UserJourneyStep",
    "V042UserJourneyStepKind",
    "V042UserOperabilityRisk",
    "V042UserOperabilityRiskRegister",
    "V042UserPersona",
    "V042UserReviewMode",
    "build_v0416_known_notes",
    "build_v042_closed_capability_matrix",
    "build_v042_command_surface_review",
    "build_v042_human_readable_output_needs",
    "build_v042_process_intelligence_review_contract",
    "build_v042_roadmap",
    "build_v042_user_journey_contract",
    "build_v042_user_operability_risk_register",
    "build_v042_user_personas",
    "build_v042_ux_pain_point_register",
    "create_v0416_known_note",
    "create_v0416_user_test_evidence",
    "create_v0420_integrated_restore_context_snapshot",
    "create_v0420_integrated_restore_document_manifest",
    "create_v0420_integrated_restore_packet",
    "create_v0420_integrated_restore_sections",
    "create_v0420_readiness_report",
    "create_v0421_default_home_quickstart_handoff",
    "create_v042_closed_capability",
    "create_v042_command_surface_review_item",
    "create_v042_default_home_ux_decision",
    "create_v042_human_readable_output_need",
    "create_v042_process_intelligence_review_criterion",
    "create_v042_provider_ux_decision",
    "create_v042_roadmap_item",
    "create_v042_trace_ux_decision",
    "create_v042_track_identity",
    "create_v042_user_journey_step",
    "create_v042_user_operability_risk",
    "create_v042_user_persona",
    "create_v042_ux_pain_point",
    "interpret_v0416_user_test_evidence",
]
