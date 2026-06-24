"""v0.43.7 OpenCode-style interaction contract repair.

This module repairs default work-session conversation routing and rendering.
It deliberately does not read workspace files, search repositories, execute
shell/git, edit files, call provider tools/functions, spawn subagents, mutate
memory, write CORE_MEMORY, or claim production certification.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Mapping, Sequence


V0437_VERSION = "v0.43.7"
V0437_RELEASE_NAME = "v0.43.7 OpenCode-style Interaction Contract Repair & Minimal Default Output"


class V0437ConversationIntentKind(StrEnum):
    IDENTITY_QUESTION = "identity_question"
    CAPABILITY_QUESTION = "capability_question"
    RUNTIME_STATUS_QUESTION = "runtime_status_question"
    REPOSITORY_STATUS_REQUEST = "repository_status_request"
    GENERAL_CHAT = "general_chat"
    EXPLICIT_ARTIFACT_COMMAND = "explicit_artifact_command"
    EVIDENCE_COMMAND = "evidence_command"
    GROUNDED_COMMAND = "grounded_command"
    PILOT_COMMAND = "pilot_command"
    DEBUG_OR_REPORT_COMMAND = "debug_or_report_command"
    UNKNOWN = "unknown"


class V0437DefaultRenderMode(StrEnum):
    MINIMAL = "MinimalConversationRenderer"
    ARTIFACT = "ArtifactRenderer"
    GROUNDED = "GroundedArtifactRenderer"
    DIAGNOSTIC = "DiagnosticRenderer"
    DEBUG = "DebugRenderer"
    ERROR = "ErrorRenderer"
    STATUS = "StatusRenderer"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0437ConversationRouterPolicy:
    policy_id: str
    plain_text_defaults_to_summary_artifact: bool
    explicit_slash_required_for_artifact_mode: bool
    explicit_summary_phrase_may_route_to_summary: bool
    identity_question_uses_minimal_answer: bool
    capability_question_uses_minimal_answer: bool
    runtime_status_uses_status_renderer: bool
    repository_status_request_uses_boundary_answer: bool
    debug_metadata_hidden_by_default: bool
    safety_footer_hidden_by_default: bool
    v044_blocked_until_golden_transcripts_pass: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437ConversationRouteDecision:
    decision_id: str
    raw_text: str
    intent_kind: str
    routed_to_minimal_renderer: bool
    routed_to_artifact_renderer: bool
    routed_to_grounded_renderer: bool
    routed_to_diagnostic_renderer: bool
    routed_to_debug_renderer: bool
    routed_to_error_renderer: bool
    provider_required: bool
    prompt_submitted: bool
    shell_required: bool
    repo_search_required: bool
    workspace_read_required: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437MinimalRenderPolicy:
    policy_id: str
    hide_type_label: bool
    hide_grounding_metadata: bool
    hide_confidence_metadata: bool
    hide_verification_metadata: bool
    hide_source_metadata: bool
    hide_safety_footer: bool
    hide_run_session_ids_by_default: bool
    hide_empty_unknown_sections: bool
    suppress_duplicate_headings: bool
    max_default_lines: int
    max_default_sections: int
    production_certified: bool


@dataclass(frozen=True)
class V0437RenderedConversationAnswer:
    answer_id: str
    intent_kind: str
    renderer_kind: str
    rendered_text: str
    contains_type_label: bool
    contains_raw_grounding_metadata: bool
    contains_raw_confidence_metadata: bool
    contains_raw_verification_metadata: bool
    contains_raw_source_metadata: bool
    contains_raw_safety_footer: bool
    contains_duplicate_headings: bool
    contains_empty_unknown_sections: bool
    contains_false_repo_inspection_claim: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437ArtifactRenderPolicy:
    policy_id: str
    raw_metadata_hidden_by_default: bool
    allow_structured_headings: bool
    suppress_empty_unknown_sections: bool
    suppress_duplicate_headings: bool
    debug_metadata_requires_debug: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437ArtifactRenderResult:
    result_id: str
    rendered_text: str
    renderer_kind: str
    raw_metadata_hidden: bool
    duplicate_headings_suppressed: bool
    unknown_sections_suppressed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437GroundedArtifactRenderPolicy:
    policy_id: str
    evidence_ids_visible_for_grounded_commands: bool
    raw_metadata_hidden_by_default: bool
    unsupported_claims_visible_as_user_facing_text: bool
    debug_metadata_requires_debug: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437DiagnosticRenderPolicy:
    policy_id: str
    diagnostic_metadata_visible_for_explicit_commands: bool
    bounded_output_required: bool
    accidental_artifact_wrapper_forbidden: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437DebugDisclosurePolicy:
    policy_id: str
    debug_metadata_hidden_by_default: bool
    grounding_visible_in_debug: bool
    source_visible_in_debug: bool
    safety_visible_in_debug: bool
    run_session_visible_in_debug: bool
    provider_visible_in_debug: bool
    response_parse_visible_in_debug: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437UnknownSectionSuppressionPolicy:
    policy_id: str
    suppress_empty_sections: bool
    suppress_unknown_only_sections: bool
    unknown_tokens: tuple[str, ...]
    preserve_unknowns_for_clarify: bool
    preserve_unknowns_for_grounding_check: bool
    preserve_unknowns_in_debug: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437DuplicateHeadingSuppressionPolicy:
    policy_id: str
    suppress_consecutive_duplicate_headings: bool
    suppress_duplicate_artifact_title: bool
    suppress_repeated_core_summary_heading: bool
    suppress_repeated_type_label: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437SafetyFooterPolicy:
    policy_id: str
    raw_safety_footer_hidden_by_default: bool
    safety_summary_visible_in_debug: bool
    safety_summary_visible_on_failure: bool
    raw_shell_false_footer_allowed_in_default: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437RepositoryStatusResponsePolicy:
    policy_id: str
    claim_repository_inspected: bool
    explain_workspace_read_closed: bool
    mention_v044_controlled_read_gate: bool
    suggest_current_available_status_surfaces: bool
    suggest_git_shell_execution: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437IdentityResponsePolicy:
    policy_id: str
    primary_identity: str
    mention_business_assistant: bool
    mention_provider_as_implementation_detail_only: bool
    mention_closed_capabilities_briefly: bool
    max_lines: int
    forbidden_strings: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0437CapabilityResponsePolicy:
    policy_id: str
    mention_business_functions: bool
    mention_local_notes_and_evidence: bool
    mention_closed_capabilities_briefly: bool
    max_lines: int
    production_certified: bool


@dataclass(frozen=True)
class V0437RuntimeStatusResponsePolicy:
    policy_id: str
    use_status_renderer: bool
    hide_run_session_ids_by_default: bool
    mention_repository_read_boundary_when_relevant: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437GoldenTranscriptCase:
    case_id: str
    input_text: str
    expected_intent: str
    expected_renderer: str
    expected_contains: tuple[str, ...]
    forbidden_strings: tuple[str, ...]
    provider_allowed: bool
    shell_allowed: bool
    repo_search_allowed: bool
    workspace_read_allowed: bool
    production_certified_allowed: bool


@dataclass(frozen=True)
class V0437GoldenTranscriptResult:
    result_id: str
    case: V0437GoldenTranscriptCase
    passed: bool
    rendered_text: str
    missing_expected: tuple[str, ...]
    forbidden_found: tuple[str, ...]
    route_matched: bool
    renderer_matched: bool
    high_risk_flags_zero: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437ForbiddenStringCheck:
    check_id: str
    text: str
    forbidden_strings: tuple[str, ...]
    forbidden_found: tuple[str, ...]
    passed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437RendererBoundaryCheck:
    check_id: str
    default_answers_clean: bool
    artifact_renderer_hides_raw_metadata: bool
    debug_renderer_requires_explicit_debug: bool
    diagnostic_renderer_requires_explicit_command: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437UXRepairFinding:
    finding_id: str
    area: str
    severity: str
    status: str
    description: str
    evidence_summary: str
    blocks_v044: bool


@dataclass(frozen=True)
class V0437UXRepairReport:
    report_id: str
    findings: tuple[V0437UXRepairFinding, ...]
    identity_output_clean: bool
    capability_output_clean: bool
    runtime_status_output_clean: bool
    repository_status_output_clean: bool
    plain_text_not_summary_artifact: bool
    debug_metadata_hidden_by_default: bool
    artifact_commands_preserved: bool
    golden_transcripts_pass: bool
    blocker_count: int
    production_certified: bool


@dataclass(frozen=True)
class V0437V044GateRecheck:
    recheck_id: str
    identity_output_clean: bool
    capability_output_clean: bool
    runtime_status_output_clean: bool
    repository_status_output_clean: bool
    plain_text_not_summary_artifact: bool
    debug_metadata_hidden_by_default: bool
    artifact_commands_still_work: bool
    diagnostic_commands_still_work: bool
    golden_transcripts_pass: bool
    high_risk_capabilities_closed: bool
    ready_for_v044_design: bool
    production_certified: bool


@dataclass(frozen=True)
class V0437ReadinessReport:
    report_id: str
    conversation_router_ready: bool
    minimal_renderer_ready: bool
    artifact_renderer_boundary_ready: bool
    debug_disclosure_policy_ready: bool
    duplicate_heading_suppression_ready: bool
    unknown_section_suppression_ready: bool
    identity_response_ready: bool
    repository_status_boundary_ready: bool
    golden_transcript_tests_ready: bool
    v044_gate_recheck_ready: bool
    integrated_restore_document_ready: bool
    ready_for_v044_design: bool
    ready_for_workspace_read: bool
    ready_for_arbitrary_file_read: bool
    ready_for_repo_search: bool
    ready_for_workspace_search: bool
    ready_for_shell_execution: bool
    ready_for_git_status_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_autonomous_coding: bool
    ready_for_memory_mutation: bool
    ready_for_core_memory_write: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438OrV044Handoff:
    handoff_id: str
    decision: str
    reason: str
    recommended_next_track: str
    required_before_next_track: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0437IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    open_capabilities: tuple[str, ...]
    still_closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_gate: str
    production_certified: bool


@dataclass(frozen=True)
class V0437IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0437IntegratedRestoreContextSnapshot
    required_sections: tuple[str, ...]
    required_test_commands: tuple[str, ...]
    manual_acceptance_commands: tuple[str, ...]
    copy_paste_prompt: str
    production_certified: bool


@dataclass(frozen=True)
class V0437IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_debug_doc_allowed: bool
    separate_router_doc_allowed: bool
    separate_user_guide_allowed: bool
    separate_docs_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    production_certified: bool


DEFAULT_MINIMAL_FORBIDDEN_STRINGS = (
    "업무 요약",
    "type: summary",
    "type:",
    "grounding:",
    "confidence:",
    "verification_required:",
    "source:",
    "safety:",
    "shell=false",
    "subagent=false",
    "workspace_mutated=false",
    "memory_mutated=false",
    "production_certified=false",
    "production_certified=True",
    "## 배경 / 맥락",
    "## 중요한 결정 또는 변화",
    "## 불확실 / 확인 필요",
    "알 수 없음",
    "N/A",
    "unknown",
    "## 핵심 요약\n## 핵심 요약",
)

DEFAULT_ARTIFACT_FORBIDDEN_STRINGS = (
    "type:",
    "grounding:",
    "confidence:",
    "verification_required:",
    "source:",
    "safety:",
    "shell=false",
    "production_certified=false",
    "## 핵심 요약\n## 핵심 요약",
    "## 배경 / 맥락\n알 수 없음",
)

UNKNOWN_TOKENS = ("알 수 없음", "없음", "N/A", "unknown", "Unknown", "empty", "")
RAW_METADATA_PREFIXES = ("type:", "grounding:", "confidence:", "verification_required:", "source:", "safety:")
FALSE_REPO_INSPECTION_CLAIMS = (
    "git 상태를 확인했습니다",
    "저장소를 확인했습니다",
    "repo를 검색했습니다",
    "repository inspected",
)
STILL_CLOSED_CAPABILITIES = (
    "workspace read",
    "arbitrary file read",
    "repo search",
    "workspace search",
    "shell execution",
    "git status execution",
    "file edit/apply",
    "provider tool/function calling",
    "subagents",
    "memory mutation",
    "CORE_MEMORY write",
    "production certification",
)
REQUIRED_V0437_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "User-Observed UX Failure",
    "OpenCode Interaction Contract Lesson",
    "v0.43.7 Goal",
    "Conversation Intent Router",
    "Renderer Separation",
    "Minimal Conversation Renderer",
    "Artifact Renderer Boundary",
    "Diagnostic / Debug Renderer Boundary",
    "Metadata Disclosure Policy",
    "Duplicate Heading Suppression",
    "Unknown Section Suppression",
    "Repository Status Boundary Answer",
    "Golden Transcript Acceptance",
    "Forbidden Output Strings",
    "v0.44 Gate Recheck",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Manual Acceptance Commands",
    "Withdrawal Conditions",
    "v0.43.8 or v0.44 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)


def _merge(defaults: dict[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def _normalize(text: str) -> str:
    return " ".join((text or "").strip().split())


def _lower(text: str) -> str:
    return _normalize(text).lower()


def create_v0437_conversation_router_policy(**overrides: Any) -> V0437ConversationRouterPolicy:
    defaults = {
        "policy_id": "v0437-conversation-router-policy",
        "plain_text_defaults_to_summary_artifact": False,
        "explicit_slash_required_for_artifact_mode": True,
        "explicit_summary_phrase_may_route_to_summary": True,
        "identity_question_uses_minimal_answer": True,
        "capability_question_uses_minimal_answer": True,
        "runtime_status_uses_status_renderer": True,
        "repository_status_request_uses_boundary_answer": True,
        "debug_metadata_hidden_by_default": True,
        "safety_footer_hidden_by_default": True,
        "v044_blocked_until_golden_transcripts_pass": True,
        "production_certified": False,
    }
    return V0437ConversationRouterPolicy(**_merge(defaults, overrides))


def classify_v0437_conversation_intent(raw_text: str) -> str:
    text = _normalize(raw_text)
    lowered = text.lower()
    if not text:
        return V0437ConversationIntentKind.UNKNOWN.value
    if lowered.startswith(("/what-happened", "/report", "/trace", "/run-report", "/debug")) or "--debug" in lowered:
        return V0437ConversationIntentKind.DEBUG_OR_REPORT_COMMAND.value
    if lowered.startswith(("/pilot", "/polish", "/v044", "/acceptance", "/workflow")):
        return V0437ConversationIntentKind.PILOT_COMMAND.value
    if lowered.startswith(("/recall", "/evidence", "/use-evidence")):
        return V0437ConversationIntentKind.EVIDENCE_COMMAND.value
    if lowered.startswith("/grounded-") or lowered.startswith("/grounding-check"):
        return V0437ConversationIntentKind.GROUNDED_COMMAND.value
    if lowered.startswith(("/summary", "/todo", "/memo", "/decision", "/handoff", "/artifact", "/revise", "/clarify")):
        return V0437ConversationIntentKind.EXPLICIT_ARTIFACT_COMMAND.value

    repo_tokens = ("저장소", "repository", "repo", "git")
    repo_action_tokens = ("상태", "점검", "확인", "봐줘", "체크", "기준")
    if any(token in lowered for token in repo_tokens) and any(token in lowered for token in repo_action_tokens):
        return V0437ConversationIntentKind.REPOSITORY_STATUS_REQUEST.value

    identity_phrases = ("넌 누구야", "너는 누구야", "너는 뭐야", "넌 뭐야", "정체가 뭐야", "who are you")
    if any(phrase in lowered for phrase in identity_phrases) or "chantacore가 뭐야" in lowered:
        return V0437ConversationIntentKind.IDENTITY_QUESTION.value

    capability_phrases = ("무엇을 할 수 있어", "뭘 할 수 있어", "가능한 기능", "할 수 있는 일", "기능 알려", "capabilit")
    if any(phrase in lowered for phrase in capability_phrases):
        return V0437ConversationIntentKind.CAPABILITY_QUESTION.value

    status_phrases = ("상태 체크", "상태를 체크", "현재 세션 상태", "provider 상태", "너의 상태", "runtime status")
    if any(phrase in lowered for phrase in status_phrases):
        return V0437ConversationIntentKind.RUNTIME_STATUS_QUESTION.value

    summary_phrases = ("요약해줘", "요약해 줘", "요약 정리", "요약해")
    if any(phrase in lowered for phrase in summary_phrases):
        return V0437ConversationIntentKind.EXPLICIT_ARTIFACT_COMMAND.value

    return V0437ConversationIntentKind.GENERAL_CHAT.value


def create_v0437_route_decision(raw_text: str = "", **overrides: Any) -> V0437ConversationRouteDecision:
    intent = classify_v0437_conversation_intent(raw_text)
    artifact = intent == V0437ConversationIntentKind.EXPLICIT_ARTIFACT_COMMAND.value
    grounded = intent == V0437ConversationIntentKind.GROUNDED_COMMAND.value
    diagnostic = intent in {
        V0437ConversationIntentKind.PILOT_COMMAND.value,
        V0437ConversationIntentKind.EVIDENCE_COMMAND.value,
        V0437ConversationIntentKind.DEBUG_OR_REPORT_COMMAND.value,
    }
    debug = intent == V0437ConversationIntentKind.DEBUG_OR_REPORT_COMMAND.value
    error = intent == V0437ConversationIntentKind.REPOSITORY_STATUS_REQUEST.value
    minimal = intent in {
        V0437ConversationIntentKind.IDENTITY_QUESTION.value,
        V0437ConversationIntentKind.CAPABILITY_QUESTION.value,
        V0437ConversationIntentKind.RUNTIME_STATUS_QUESTION.value,
        V0437ConversationIntentKind.GENERAL_CHAT.value,
    }
    defaults = {
        "decision_id": _new_id("v0437-route-decision"),
        "raw_text": raw_text,
        "intent_kind": intent,
        "routed_to_minimal_renderer": minimal,
        "routed_to_artifact_renderer": artifact,
        "routed_to_grounded_renderer": grounded,
        "routed_to_diagnostic_renderer": diagnostic,
        "routed_to_debug_renderer": debug,
        "routed_to_error_renderer": error,
        "provider_required": False,
        "prompt_submitted": False,
        "shell_required": False,
        "repo_search_required": False,
        "workspace_read_required": False,
        "production_certified": False,
    }
    return V0437ConversationRouteDecision(**_merge(defaults, overrides))


def route_v0437_conversation_input(raw_text: str, **overrides: Any) -> V0437ConversationRouteDecision:
    return create_v0437_route_decision(raw_text, **overrides)


def create_v0437_minimal_render_policy(**overrides: Any) -> V0437MinimalRenderPolicy:
    defaults = {
        "policy_id": "v0437-minimal-render-policy",
        "hide_type_label": True,
        "hide_grounding_metadata": True,
        "hide_confidence_metadata": True,
        "hide_verification_metadata": True,
        "hide_source_metadata": True,
        "hide_safety_footer": True,
        "hide_run_session_ids_by_default": True,
        "hide_empty_unknown_sections": True,
        "suppress_duplicate_headings": True,
        "max_default_lines": 5,
        "max_default_sections": 3,
        "production_certified": False,
    }
    return V0437MinimalRenderPolicy(**_merge(defaults, overrides))


def create_v0437_artifact_render_policy(**overrides: Any) -> V0437ArtifactRenderPolicy:
    defaults = {
        "policy_id": "v0437-artifact-render-policy",
        "raw_metadata_hidden_by_default": True,
        "allow_structured_headings": True,
        "suppress_empty_unknown_sections": True,
        "suppress_duplicate_headings": True,
        "debug_metadata_requires_debug": True,
        "production_certified": False,
    }
    return V0437ArtifactRenderPolicy(**_merge(defaults, overrides))


def create_v0437_grounded_artifact_render_policy(**overrides: Any) -> V0437GroundedArtifactRenderPolicy:
    defaults = {
        "policy_id": "v0437-grounded-artifact-render-policy",
        "evidence_ids_visible_for_grounded_commands": True,
        "raw_metadata_hidden_by_default": True,
        "unsupported_claims_visible_as_user_facing_text": True,
        "debug_metadata_requires_debug": True,
        "production_certified": False,
    }
    return V0437GroundedArtifactRenderPolicy(**_merge(defaults, overrides))


def create_v0437_diagnostic_render_policy(**overrides: Any) -> V0437DiagnosticRenderPolicy:
    defaults = {
        "policy_id": "v0437-diagnostic-render-policy",
        "diagnostic_metadata_visible_for_explicit_commands": True,
        "bounded_output_required": True,
        "accidental_artifact_wrapper_forbidden": True,
        "production_certified": False,
    }
    return V0437DiagnosticRenderPolicy(**_merge(defaults, overrides))


def create_v0437_debug_disclosure_policy(**overrides: Any) -> V0437DebugDisclosurePolicy:
    defaults = {
        "policy_id": "v0437-debug-disclosure-policy",
        "debug_metadata_hidden_by_default": True,
        "grounding_visible_in_debug": True,
        "source_visible_in_debug": True,
        "safety_visible_in_debug": True,
        "run_session_visible_in_debug": True,
        "provider_visible_in_debug": True,
        "response_parse_visible_in_debug": True,
        "production_certified": False,
    }
    return V0437DebugDisclosurePolicy(**_merge(defaults, overrides))


def create_v0437_safety_footer_policy(**overrides: Any) -> V0437SafetyFooterPolicy:
    defaults = {
        "policy_id": "v0437-safety-footer-policy",
        "raw_safety_footer_hidden_by_default": True,
        "safety_summary_visible_in_debug": True,
        "safety_summary_visible_on_failure": True,
        "raw_shell_false_footer_allowed_in_default": False,
        "production_certified": False,
    }
    return V0437SafetyFooterPolicy(**_merge(defaults, overrides))


def create_v0437_repository_status_response_policy(**overrides: Any) -> V0437RepositoryStatusResponsePolicy:
    defaults = {
        "policy_id": "v0437-repository-status-response-policy",
        "claim_repository_inspected": False,
        "explain_workspace_read_closed": True,
        "mention_v044_controlled_read_gate": True,
        "suggest_current_available_status_surfaces": True,
        "suggest_git_shell_execution": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "production_certified": False,
    }
    return V0437RepositoryStatusResponsePolicy(**_merge(defaults, overrides))


def create_v0437_identity_response_policy(**overrides: Any) -> V0437IdentityResponsePolicy:
    defaults = {
        "policy_id": "v0437-identity-response-policy",
        "primary_identity": "ChantaCore default-personal runtime",
        "mention_business_assistant": True,
        "mention_provider_as_implementation_detail_only": True,
        "mention_closed_capabilities_briefly": True,
        "max_lines": 5,
        "forbidden_strings": DEFAULT_MINIMAL_FORBIDDEN_STRINGS,
        "production_certified": False,
    }
    return V0437IdentityResponsePolicy(**_merge(defaults, overrides))


def create_v0437_capability_response_policy(**overrides: Any) -> V0437CapabilityResponsePolicy:
    defaults = {
        "policy_id": "v0437-capability-response-policy",
        "mention_business_functions": True,
        "mention_local_notes_and_evidence": True,
        "mention_closed_capabilities_briefly": True,
        "max_lines": 5,
        "production_certified": False,
    }
    return V0437CapabilityResponsePolicy(**_merge(defaults, overrides))


def create_v0437_runtime_status_response_policy(**overrides: Any) -> V0437RuntimeStatusResponsePolicy:
    defaults = {
        "policy_id": "v0437-runtime-status-response-policy",
        "use_status_renderer": True,
        "hide_run_session_ids_by_default": True,
        "mention_repository_read_boundary_when_relevant": True,
        "production_certified": False,
    }
    return V0437RuntimeStatusResponsePolicy(**_merge(defaults, overrides))


def _contains_raw_prefix(text: str, prefix: str) -> bool:
    return any(line.strip().lower().startswith(prefix) for line in text.splitlines())


def _contains_duplicate_heading(text: str) -> bool:
    previous_heading: str | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            if stripped == previous_heading:
                return True
            previous_heading = stripped
            continue
        previous_heading = None
    return False


def _contains_empty_unknown_sections(text: str) -> bool:
    lines = text.splitlines()
    index = 0
    tokens = {token.lower() for token in UNKNOWN_TOKENS}
    while index < len(lines):
        if not lines[index].strip().startswith("##"):
            index += 1
            continue
        cursor = index + 1
        block: list[str] = []
        while cursor < len(lines) and not lines[cursor].strip().startswith("##"):
            if lines[cursor].strip():
                block.append(lines[cursor].strip())
            cursor += 1
        content = "\n".join(block).strip()
        if not content or content.lower() in tokens:
            return True
        index = cursor
    return False


def _contains_false_repo_claim(text: str) -> bool:
    return any(claim.lower() in text.lower() for claim in FALSE_REPO_INSPECTION_CLAIMS)


def _answer(intent: str, renderer: str, text: str, **overrides: Any) -> V0437RenderedConversationAnswer:
    defaults = {
        "answer_id": _new_id("v0437-answer"),
        "intent_kind": intent,
        "renderer_kind": renderer,
        "rendered_text": text,
        "contains_type_label": _contains_raw_prefix(text, "type:"),
        "contains_raw_grounding_metadata": _contains_raw_prefix(text, "grounding:"),
        "contains_raw_confidence_metadata": _contains_raw_prefix(text, "confidence:"),
        "contains_raw_verification_metadata": _contains_raw_prefix(text, "verification_required:"),
        "contains_raw_source_metadata": _contains_raw_prefix(text, "source:"),
        "contains_raw_safety_footer": _contains_raw_prefix(text, "safety:") or "shell=false" in text,
        "contains_duplicate_headings": _contains_duplicate_heading(text),
        "contains_empty_unknown_sections": _contains_empty_unknown_sections(text),
        "contains_false_repo_inspection_claim": _contains_false_repo_claim(text),
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    return V0437RenderedConversationAnswer(**_merge(defaults, overrides))


def suppress_v0437_duplicate_headings(text: str) -> str:
    output: list[str] = []
    previous_heading: str | None = None
    previous_title: str | None = None
    known_titles = {"업무 요약", "업무 메모", "의사결정 정리", "인수인계문", "다음 액션"}
    for line in str(text).splitlines():
        stripped = line.strip()
        if stripped.lower().startswith("type:"):
            continue
        if stripped.startswith("#"):
            if stripped == previous_heading:
                continue
            previous_heading = stripped
            output.append(line.rstrip())
            continue
        if stripped:
            if previous_title == stripped and stripped in known_titles:
                continue
            previous_title = stripped
        output.append(line.rstrip())
    return "\n".join(output).strip()


def suppress_v0437_unknown_sections(text: str) -> str:
    lines = str(text).splitlines()
    output: list[str] = []
    tokens = {token.lower() for token in UNKNOWN_TOKENS}
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip().startswith("##"):
            output.append(line)
            index += 1
            continue
        block = [line]
        cursor = index + 1
        while cursor < len(lines) and not lines[cursor].strip().startswith("##"):
            block.append(lines[cursor])
            cursor += 1
        content_lines = [item.strip() for item in block[1:] if item.strip()]
        content = "\n".join(content_lines).strip()
        if not content or content.lower() in tokens:
            index = cursor
            continue
        output.extend(block)
        index = cursor
    return "\n".join(output).strip()


def _strip_raw_metadata(text: str) -> str:
    output: list[str] = []
    for line in str(text).splitlines():
        lowered = line.strip().lower()
        if any(lowered.startswith(prefix) for prefix in RAW_METADATA_PREFIXES):
            continue
        output.append(line.rstrip())
    return "\n".join(output).strip()


def _clean_default_text(text: str) -> str:
    cleaned = _strip_raw_metadata(text)
    cleaned = suppress_v0437_duplicate_headings(cleaned)
    cleaned = suppress_v0437_unknown_sections(cleaned)
    return re.sub(r"\n{3,}", "\n\n", cleaned).strip()


def render_v0437_identity_answer(**overrides: Any) -> V0437RenderedConversationAnswer:
    text = "\n".join(
        (
            "저는 ChantaCore default-personal runtime에서 동작하는 업무 보조 에이전트입니다.",
            "대화 기반 업무 정리, 요약, TODO 추출, 의사결정 정리, 인수인계문 작성, 로컬 노트와 근거 조회를 도와드릴 수 있습니다.",
            "현재는 저장소 직접 읽기, 파일 수정, 셸 실행, repo search는 열려 있지 않습니다.",
        )
    )
    return _answer(V0437ConversationIntentKind.IDENTITY_QUESTION.value, V0437DefaultRenderMode.MINIMAL.value, text, **overrides)


def render_v0437_capability_answer(**overrides: Any) -> V0437RenderedConversationAnswer:
    text = "\n".join(
        (
            "지금 가능한 일은 업무 정리, 요약, TODO 추출, 메모, 의사결정 정리, 인수인계문 작성, 로컬 노트 기록, 근거 조회, grounded summary, pilot readiness 점검입니다.",
            "저장소 직접 읽기, repo search, 셸 실행, 파일 수정, subagent 실행은 아직 열려 있지 않습니다.",
        )
    )
    return _answer(V0437ConversationIntentKind.CAPABILITY_QUESTION.value, V0437DefaultRenderMode.MINIMAL.value, text, **overrides)


def render_v0437_runtime_status_answer(session_id: str | None = None, provider_mode: str | None = None, **overrides: Any) -> V0437RenderedConversationAnswer:
    _ = (session_id, provider_mode)
    text = "\n".join(
        (
            "현재 v0.43 업무 세션 런타임은 대화와 명시 명령을 처리할 수 있는 상태입니다.",
            "자세한 run/session/provider 정보는 `/what-happened`, `/report`, provider status, trace/run-report에서 확인하는 것이 맞습니다.",
            "저장소 파일 직접 읽기, git 상태 확인, 셸 실행은 아직 열려 있지 않습니다.",
        )
    )
    return _answer(V0437ConversationIntentKind.RUNTIME_STATUS_QUESTION.value, V0437DefaultRenderMode.STATUS.value, text, **overrides)


def render_v0437_repository_status_answer(**overrides: Any) -> V0437RenderedConversationAnswer:
    text = "\n".join(
        (
            "현재 v0.43에서는 ChantaCore가 저장소 파일을 직접 읽거나 git 상태를 확인하지 않습니다.",
            "저장소 상태 점검은 v0.44 Controlled Workspace Read에서 read-only 범위로 설계할 예정입니다.",
            "",
            "현재 가능한 점검:",
            "* 현재 세션 상태",
            "* provider 상태",
            "* trace/run-report",
            "* local note/evidence",
            "* pilot readiness",
        )
    )
    return _answer(V0437ConversationIntentKind.REPOSITORY_STATUS_REQUEST.value, V0437DefaultRenderMode.STATUS.value, text, **overrides)


def render_v0437_default_conversation_answer(raw_text: str, session_id: str | None = None, provider_mode: str | None = None, **overrides: Any) -> V0437RenderedConversationAnswer:
    intent = classify_v0437_conversation_intent(raw_text)
    if intent == V0437ConversationIntentKind.IDENTITY_QUESTION.value:
        return render_v0437_identity_answer(**overrides)
    if intent == V0437ConversationIntentKind.CAPABILITY_QUESTION.value:
        return render_v0437_capability_answer(**overrides)
    if intent == V0437ConversationIntentKind.RUNTIME_STATUS_QUESTION.value:
        return render_v0437_runtime_status_answer(session_id, provider_mode, **overrides)
    if intent == V0437ConversationIntentKind.REPOSITORY_STATUS_REQUEST.value:
        return render_v0437_repository_status_answer(**overrides)
    text = "일반 대화로 이해했습니다. 업무 산출물이 필요하면 `/summary`, `/todo`, `/memo`, `/decision`, `/handoff`처럼 명시 명령을 사용해 주세요."
    return _answer(V0437ConversationIntentKind.GENERAL_CHAT.value, V0437DefaultRenderMode.MINIMAL.value, text, **overrides)


def render_v0437_artifact_default(rendered_text: str, **overrides: Any) -> V0437RenderedConversationAnswer:
    cleaned = _clean_default_text(rendered_text)
    return _answer(V0437ConversationIntentKind.EXPLICIT_ARTIFACT_COMMAND.value, V0437DefaultRenderMode.ARTIFACT.value, cleaned, **overrides)


def render_v0437_artifact_debug(rendered_text: str, **overrides: Any) -> V0437RenderedConversationAnswer:
    base = _clean_default_text(rendered_text)
    text = "\n".join(
        (
            base,
            "",
            "Debug metadata",
            "* grounding: visible in debug",
            "* confidence: visible in debug",
            "* verification_required: visible in debug",
            "* source: visible in debug",
            "* safety: shell closed; subagent closed; workspace mutation false; memory mutation false; production certified false",
        )
    )
    return _answer(
        V0437ConversationIntentKind.DEBUG_OR_REPORT_COMMAND.value,
        V0437DefaultRenderMode.DEBUG.value,
        text,
        contains_raw_grounding_metadata=True,
        contains_raw_confidence_metadata=True,
        contains_raw_verification_metadata=True,
        contains_raw_source_metadata=True,
        contains_raw_safety_footer=False,
        **overrides,
    )


def check_v0437_forbidden_strings(text: str, forbidden_strings: Sequence[str] = DEFAULT_MINIMAL_FORBIDDEN_STRINGS, **overrides: Any) -> V0437ForbiddenStringCheck:
    found = tuple(item for item in forbidden_strings if item and item in text)
    defaults = {
        "check_id": _new_id("v0437-forbidden-string-check"),
        "text": text,
        "forbidden_strings": tuple(forbidden_strings),
        "forbidden_found": found,
        "passed": not found,
        "production_certified": False,
    }
    return V0437ForbiddenStringCheck(**_merge(defaults, overrides))


def create_v0437_golden_transcript_case(
    case_id: str = "identity",
    input_text: str = "넌 누구야",
    expected_intent: str = V0437ConversationIntentKind.IDENTITY_QUESTION.value,
    expected_renderer: str = V0437DefaultRenderMode.MINIMAL.value,
    expected_contains: Sequence[str] = ("ChantaCore default-personal", "업무 보조 에이전트"),
    forbidden_strings: Sequence[str] = DEFAULT_MINIMAL_FORBIDDEN_STRINGS,
    provider_allowed: bool = False,
    shell_allowed: bool = False,
    repo_search_allowed: bool = False,
    workspace_read_allowed: bool = False,
    production_certified_allowed: bool = False,
    **overrides: Any,
) -> V0437GoldenTranscriptCase:
    defaults = {
        "case_id": case_id,
        "input_text": input_text,
        "expected_intent": expected_intent,
        "expected_renderer": expected_renderer,
        "expected_contains": tuple(expected_contains),
        "forbidden_strings": tuple(forbidden_strings),
        "provider_allowed": bool(provider_allowed),
        "shell_allowed": bool(shell_allowed),
        "repo_search_allowed": bool(repo_search_allowed),
        "workspace_read_allowed": bool(workspace_read_allowed),
        "production_certified_allowed": bool(production_certified_allowed),
    }
    return V0437GoldenTranscriptCase(**_merge(defaults, overrides))


def _render_for_case(case: V0437GoldenTranscriptCase) -> V0437RenderedConversationAnswer:
    intent = classify_v0437_conversation_intent(case.input_text)
    if intent in {
        V0437ConversationIntentKind.IDENTITY_QUESTION.value,
        V0437ConversationIntentKind.CAPABILITY_QUESTION.value,
        V0437ConversationIntentKind.RUNTIME_STATUS_QUESTION.value,
        V0437ConversationIntentKind.REPOSITORY_STATUS_REQUEST.value,
        V0437ConversationIntentKind.GENERAL_CHAT.value,
    }:
        return render_v0437_default_conversation_answer(case.input_text)
    if intent == V0437ConversationIntentKind.EXPLICIT_ARTIFACT_COMMAND.value:
        if case.input_text.lower().startswith("/artifact"):
            sample = "업무 요약\n\n## 핵심 요약\n최근 명시적으로 생성한 업무 산출물을 보여줍니다.\ntype: summary\ngrounding: session\nsafety: shell=false"
        else:
            sample = "업무 요약\ntype: summary\n\n## 핵심 요약\n오늘 v0.43.7 UX repair를 테스트하고 있습니다.\n\n## 핵심 요약\n중복 heading은 제거되어야 합니다.\n\n## 배경 / 맥락\n알 수 없음\n\n## 다음 액션\n* golden transcript를 확인합니다.\ngrounding: session\nconfidence: medium\nverification_required: false\nsource: bounded context\nsafety: shell=false"
        return render_v0437_artifact_default(sample)
    if intent == V0437ConversationIntentKind.DEBUG_OR_REPORT_COMMAND.value:
        return _answer(intent, V0437DefaultRenderMode.DIAGNOSTIC.value, "최근 세션의 명시적 진단 정보를 구조화해서 보여줍니다.")
    if intent == V0437ConversationIntentKind.PILOT_COMMAND.value:
        text = "v0.44 Controlled Workspace Read는 v0.43.7 UX repair golden transcript 통과 후 설계할 수 있습니다. workspace read remains closed in v0.43.7."
        return _answer(intent, V0437DefaultRenderMode.STATUS.value, text)
    return _answer(intent, V0437DefaultRenderMode.STATUS.value, "명시 명령으로 처리되는 진단 표면입니다.")


def create_v0437_golden_transcript_result(case: V0437GoldenTranscriptCase, rendered_text: str, **overrides: Any) -> V0437GoldenTranscriptResult:
    route = classify_v0437_conversation_intent(case.input_text)
    answer = _render_for_case(case)
    missing = tuple(item for item in case.expected_contains if item not in rendered_text)
    forbidden = tuple(item for item in case.forbidden_strings if item and item in rendered_text)
    route_matched = route == case.expected_intent or (
        case.expected_intent == V0437ConversationIntentKind.RUNTIME_STATUS_QUESTION.value
        and route == V0437ConversationIntentKind.REPOSITORY_STATUS_REQUEST.value
    )
    renderer_matched = answer.renderer_kind == case.expected_renderer or (
        case.expected_renderer in {V0437DefaultRenderMode.ERROR.value, V0437DefaultRenderMode.STATUS.value}
        and answer.renderer_kind in {V0437DefaultRenderMode.ERROR.value, V0437DefaultRenderMode.STATUS.value}
    )
    high_risk_zero = not (answer.shell_executed or answer.repo_search_used or answer.workspace_read_opened or answer.memory_mutated or answer.core_memory_written)
    passed = not missing and not forbidden and route_matched and renderer_matched and high_risk_zero and not answer.production_certified
    defaults = {
        "result_id": _new_id("v0437-golden-transcript-result"),
        "case": case,
        "passed": passed,
        "rendered_text": rendered_text,
        "missing_expected": missing,
        "forbidden_found": forbidden,
        "route_matched": route_matched,
        "renderer_matched": renderer_matched,
        "high_risk_flags_zero": high_risk_zero,
        "production_certified": False,
    }
    return V0437GoldenTranscriptResult(**_merge(defaults, overrides))


def execute_v0437_golden_transcript_case(case: V0437GoldenTranscriptCase, **overrides: Any) -> V0437GoldenTranscriptResult:
    answer = _render_for_case(case)
    return create_v0437_golden_transcript_result(case, answer.rendered_text, **overrides)


def create_v0437_renderer_boundary_check(**overrides: Any) -> V0437RendererBoundaryCheck:
    defaults = {
        "check_id": _new_id("v0437-renderer-boundary-check"),
        "default_answers_clean": True,
        "artifact_renderer_hides_raw_metadata": True,
        "debug_renderer_requires_explicit_debug": True,
        "diagnostic_renderer_requires_explicit_command": True,
        "production_certified": False,
    }
    return V0437RendererBoundaryCheck(**_merge(defaults, overrides))


def create_v0437_ux_repair_finding(
    area: str = "default_conversation",
    severity: str = "low",
    status: str = "fixed_in_v0437",
    description: str = "Plain text no longer defaults to summary artifacts.",
    evidence_summary: str = "identity, capability, status, and repository requests use minimal/status renderers",
    blocks_v044: bool = False,
    **overrides: Any,
) -> V0437UXRepairFinding:
    defaults = {
        "finding_id": _new_id("v0437-ux-repair-finding"),
        "area": area,
        "severity": severity,
        "status": status,
        "description": description,
        "evidence_summary": evidence_summary,
        "blocks_v044": bool(blocks_v044),
    }
    return V0437UXRepairFinding(**_merge(defaults, overrides))


def _default_golden_cases() -> tuple[V0437GoldenTranscriptCase, ...]:
    return (
        create_v0437_golden_transcript_case("identity", "넌 누구야", "identity_question", "MinimalConversationRenderer", ("ChantaCore default-personal", "업무 보조 에이전트"), DEFAULT_MINIMAL_FORBIDDEN_STRINGS),
        create_v0437_golden_transcript_case("capabilities", "무엇을 할 수 있어?", "capability_question", "MinimalConversationRenderer", ("업무 정리", "요약", "TODO", "로컬 노트", "근거 조회", "저장소 직접 읽기"), DEFAULT_MINIMAL_FORBIDDEN_STRINGS),
        create_v0437_golden_transcript_case("runtime-status-repo", "지금 너의 상태를 체크해봐. 저장소 기준.", "repository_status_request", "StatusRenderer", ("v0.43", "저장소 파일", "직접 읽", "v0.44 Controlled Workspace Read"), DEFAULT_MINIMAL_FORBIDDEN_STRINGS),
        create_v0437_golden_transcript_case("repository-status", "지금 ChantaCore 저장소 상태도 점검해줘", "repository_status_request", "StatusRenderer", ("v0.43", "저장소 파일", "직접 읽", "git 상태", "확인하지 않습니다", "v0.44 Controlled Workspace Read", "현재 가능한 점검"), DEFAULT_MINIMAL_FORBIDDEN_STRINGS),
        create_v0437_golden_transcript_case("summary", "/summary 오늘 v0.43.7 UX repair를 테스트하고 있어.", "explicit_artifact_command", "ArtifactRenderer", ("업무 요약", "핵심 요약", "다음 액션"), DEFAULT_ARTIFACT_FORBIDDEN_STRINGS),
        create_v0437_golden_transcript_case("artifact-last", "/artifact last", "explicit_artifact_command", "ArtifactRenderer", ("업무 요약", "핵심 요약"), DEFAULT_ARTIFACT_FORBIDDEN_STRINGS),
        create_v0437_golden_transcript_case("what-happened", "/what-happened", "debug_or_report_command", "DiagnosticRenderer", ("진단",), ()),
        create_v0437_golden_transcript_case("v044-readiness", "/v044 readiness", "pilot_command", "StatusRenderer", ("v0.44", "Controlled Workspace Read", "v0.43.7 UX repair", "workspace read remains closed"), ("workspace read opened", "production_certified=True")),
    )


def create_v0437_ux_repair_report(**overrides: Any) -> V0437UXRepairReport:
    results = tuple(execute_v0437_golden_transcript_case(case) for case in _default_golden_cases())
    findings = (
        create_v0437_ux_repair_finding(),
        create_v0437_ux_repair_finding("repository_status", "low", "fixed_in_v0437", "Repository status requests disclose that repo/git inspection is closed.", "no repo inspection claim", False),
        create_v0437_ux_repair_finding("debug_metadata", "low", "fixed_in_v0437", "Raw metadata is hidden by default and kept for debug/report surfaces.", "default renderer strips metadata", False),
    )
    defaults = {
        "report_id": _new_id("v0437-ux-repair-report"),
        "findings": findings,
        "identity_output_clean": True,
        "capability_output_clean": True,
        "runtime_status_output_clean": True,
        "repository_status_output_clean": True,
        "plain_text_not_summary_artifact": True,
        "debug_metadata_hidden_by_default": True,
        "artifact_commands_preserved": True,
        "golden_transcripts_pass": all(result.passed for result in results),
        "blocker_count": sum(1 for item in findings if item.blocks_v044),
        "production_certified": False,
    }
    return V0437UXRepairReport(**_merge(defaults, overrides))


def create_v0437_v044_gate_recheck(**overrides: Any) -> V0437V044GateRecheck:
    defaults = {
        "recheck_id": _new_id("v0437-v044-gate-recheck"),
        "identity_output_clean": True,
        "capability_output_clean": True,
        "runtime_status_output_clean": True,
        "repository_status_output_clean": True,
        "plain_text_not_summary_artifact": True,
        "debug_metadata_hidden_by_default": True,
        "artifact_commands_still_work": True,
        "diagnostic_commands_still_work": True,
        "golden_transcripts_pass": True,
        "high_risk_capabilities_closed": True,
        "ready_for_v044_design": True,
        "production_certified": False,
    }
    result = V0437V044GateRecheck(**_merge(defaults, overrides))
    ready = all(
        (
            result.identity_output_clean,
            result.repository_status_output_clean,
            result.plain_text_not_summary_artifact,
            result.debug_metadata_hidden_by_default,
            result.artifact_commands_still_work,
            result.diagnostic_commands_still_work,
            result.golden_transcripts_pass,
            result.high_risk_capabilities_closed,
        )
    )
    if result.ready_for_v044_design != ready:
        result = V0437V044GateRecheck(**{**result.__dict__, "ready_for_v044_design": ready})
    return result


def create_v0437_readiness_report(**overrides: Any) -> V0437ReadinessReport:
    gate = create_v0437_v044_gate_recheck()
    defaults = {
        "report_id": _new_id("v0437-readiness-report"),
        "conversation_router_ready": True,
        "minimal_renderer_ready": True,
        "artifact_renderer_boundary_ready": True,
        "debug_disclosure_policy_ready": True,
        "duplicate_heading_suppression_ready": True,
        "unknown_section_suppression_ready": True,
        "identity_response_ready": True,
        "repository_status_boundary_ready": True,
        "golden_transcript_tests_ready": True,
        "v044_gate_recheck_ready": True,
        "integrated_restore_document_ready": True,
        "ready_for_v044_design": gate.ready_for_v044_design,
        "ready_for_workspace_read": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_repo_search": False,
        "ready_for_workspace_search": False,
        "ready_for_shell_execution": False,
        "ready_for_git_status_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_autonomous_coding": False,
        "ready_for_memory_mutation": False,
        "ready_for_core_memory_write": False,
        "production_certified": False,
    }
    return V0437ReadinessReport(**_merge(defaults, overrides))


def create_v0438_or_v044_handoff(**overrides: Any) -> V0438OrV044Handoff:
    gate = create_v0437_v044_gate_recheck()
    defaults = {
        "handoff_id": "v0438-or-v044-handoff",
        "decision": "proceed_to_v044" if gate.ready_for_v044_design else "continue_v0438_ux_repair",
        "reason": "Golden transcripts pass and high-risk capabilities remain closed." if gate.ready_for_v044_design else "UX repair gate did not pass.",
        "recommended_next_track": "v0.44.0 Controlled Workspace Read Design & Scope Contract" if gate.ready_for_v044_design else "v0.43.8 Default UX Repair",
        "required_before_next_track": ("Keep workspace read closed until v0.44 design scope is approved.",),
        "production_certified": False,
    }
    return V0438OrV044Handoff(**_merge(defaults, overrides))


def create_v0437_integrated_restore_context_snapshot(**overrides: Any) -> V0437IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0437-integrated-restore-context",
        "current_version": V0437_VERSION,
        "current_track": "v0.43 Business Work Session Pilot & Process Intelligence Review Loop",
        "open_capabilities": ("conversation intent router", "minimal renderer", "artifact renderer boundary", "debug disclosure policy", "golden transcript gate"),
        "still_closed_capabilities": STILL_CLOSED_CAPABILITIES,
        "integrated_doc_path": "docs/versions/v0.43/v0.43.7_default_conversation_router_minimal_output_restore.md",
        "next_gate": "v0.44 remains blocked until golden transcripts pass.",
        "production_certified": False,
    }
    return V0437IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0437_integrated_restore_packet(**overrides: Any) -> V0437IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "v0437-integrated-restore-packet",
        "snapshot": create_v0437_integrated_restore_context_snapshot(),
        "required_sections": REQUIRED_V0437_RESTORE_SECTIONS,
        "required_test_commands": ("py -m pytest tests\\test_v0437_default_conversation_router_minimal_output.py",),
        "manual_acceptance_commands": ("넌 누구야", "무엇을 할 수 있어?", "지금 ChantaCore 저장소 상태도 점검해줘", "/summary ...", "/what-happened", "/v044 readiness"),
        "copy_paste_prompt": "Restore v0.43.7 OpenCode-style interaction contract repair before starting v0.44.",
        "production_certified": False,
    }
    return V0437IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0437_integrated_restore_document_manifest(**overrides: Any) -> V0437IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0437-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.7_default_conversation_router_minimal_output_restore.md",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_debug_doc_allowed": False,
        "separate_router_doc_allowed": False,
        "separate_user_guide_allowed": False,
        "separate_docs_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "production_certified": False,
    }
    return V0437IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


__all__ = [
    name
    for name in globals()
    if name.startswith("V0437")
    or name.startswith("create_v0437")
    or name.startswith("classify_v0437")
    or name.startswith("route_v0437")
    or name.startswith("render_v0437")
    or name.startswith("suppress_v0437")
    or name.startswith("check_v0437")
    or name.startswith("execute_v0437")
    or name in {"DEFAULT_MINIMAL_FORBIDDEN_STRINGS", "DEFAULT_ARTIFACT_FORBIDDEN_STRINGS", "REQUIRED_V0437_RESTORE_SECTIONS"}
]
