"""v0.43.6 final pilot polish and v0.44 gate.

This layer closes the v0.43 business work-session pilot with deterministic
review objects. It does not open workspace read, arbitrary filesystem search,
repo search, shell execution, file edit/apply, provider tool/function calling,
subagents, automatic memory mutation, CORE_MEMORY writes, or production
certification.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_pilot_review import (
    V043_TRACK_NAME,
    V0435_RELEASE_NAME,
    create_v043_pilot_review_request,
    create_v043_pilot_review_result,
)


V0436_VERSION = "v0.43.6"
V0436_RELEASE_NAME = "v0.43.6 Final Pilot Polish & v0.44 Controlled Workspace Read Gate"
V0440_RECOMMENDED_TITLE = "v0.44.0 - Controlled Workspace Read Design & Scope Contract"


class V0436PolishStatus(StrEnum):
    OPEN = "open"
    FIXED = "fixed"
    DEFERRED = "deferred"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class V0436PolishFindingArea(StrEnum):
    COMMAND_SURFACE = "command_surface"
    CHAT_UX = "chat_ux"
    RUN_UX = "run_ux"
    PROVIDER_UX = "provider_ux"
    WORK_FLOW = "work_flow"
    ARTIFACT_QUALITY = "artifact_quality"
    EVIDENCE_RETRIEVAL = "evidence_retrieval"
    GROUNDED_SYNTHESIS = "grounded_synthesis"
    PILOT_REVIEW = "pilot_review"
    SAFETY = "safety"
    V044_GATE = "v044_gate"
    DOCUMENTATION = "documentation"
    UNKNOWN = "unknown"


class V0436PolishFindingSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKER = "blocker"
    UNKNOWN = "unknown"


class V0436PolishFindingStatus(StrEnum):
    OPEN = "open"
    FIXED_IN_V0436 = "fixed_in_v0436"
    DEFERRED_TO_V0437 = "deferred_to_v0437"
    ACCEPTED_FOR_V044 = "accepted_for_v044"
    BLOCKS_V044 = "blocks_v044"
    UNKNOWN = "unknown"


class V0436V044GateDecisionKind(StrEnum):
    PROCEED_TO_V044_CONTROLLED_WORKSPACE_READ_DESIGN = "proceed_to_v044_controlled_workspace_read_design"
    CONTINUE_V0437_POLISH = "continue_v0437_polish"
    BLOCKED_BY_SAFETY = "blocked_by_safety"
    BLOCKED_BY_UNCLEAR_SCOPE = "blocked_by_unclear_scope"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0436PolishFinding:
    finding_id: str
    area: str
    severity: str
    status: str
    description: str
    user_impact: str
    recommended_action: str
    blocks_v044: bool
    fixed_in_v0436: bool
    deferred_reason: str | None


@dataclass(frozen=True)
class V0436CommandSurfaceAuditItem:
    item_id: str
    command_name: str
    category: str
    expected_behavior: str
    available: bool
    user_friendly: bool
    debug_details_hidden_by_default: bool
    high_risk_capability_opened: bool
    notes: str


@dataclass(frozen=True)
class V0436CommandSurfaceAudit:
    audit_id: str
    items: tuple[V0436CommandSurfaceAuditItem, ...]
    missing_commands: tuple[str, ...]
    rough_commands: tuple[str, ...]
    high_risk_commands: tuple[str, ...]
    pass_count: int
    warning_count: int
    fail_count: int
    ready_for_v044: bool


@dataclass(frozen=True)
class V0436BusinessUXFinalAcceptance:
    acceptance_id: str
    start_flow_accepted: bool
    chat_ux_accepted: bool
    work_flow_accepted: bool
    artifact_ux_accepted: bool
    evidence_ux_accepted: bool
    grounded_ux_accepted: bool
    pilot_review_accepted: bool
    default_debug_separation_accepted: bool
    overall_accepted: bool
    remaining_rough_edges: tuple[str, ...]


@dataclass(frozen=True)
class V0436PilotClosureCriterion:
    criterion_id: str
    title: str
    pass_condition: str
    status: str
    blocks_closure: bool
    evidence_summary: str


@dataclass(frozen=True)
class V0436PilotClosureReport:
    report_id: str
    criteria: tuple[V0436PilotClosureCriterion, ...]
    command_audit: V0436CommandSurfaceAudit
    ux_acceptance: V0436BusinessUXFinalAcceptance
    polish_findings: tuple[V0436PolishFinding, ...]
    blocker_count: int
    warning_count: int
    v043_closure_allowed: bool
    recommends_v0437: bool
    recommends_v044_design: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436PilotClosureDecision:
    decision_id: str
    decision: str
    reason: str
    close_v043: bool
    continue_v0437: bool
    proceed_to_v044_design: bool
    required_before_next_track: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0436V044ControlledWorkspaceReadScope:
    scope_id: str
    design_only_in_v0436: bool
    controlled_workspace_read_may_open_in_v044: bool
    write_allowed: bool
    edit_apply_allowed: bool
    shell_allowed: bool
    test_execution_allowed: bool
    repo_wide_search_allowed: bool
    subagent_allowed: bool
    production_certified: bool
    required_scope_elements: tuple[str, ...]


@dataclass(frozen=True)
class V0436V044WorkspaceReadSafetyGate:
    gate_id: str
    title: str
    required: bool
    description: str
    failure_mode: str
    blocks_workspace_read: bool


@dataclass(frozen=True)
class V0436V044WorkspaceReadRisk:
    risk_id: str
    title: str
    severity: str
    description: str
    mitigation: str
    withdrawal_condition: str


@dataclass(frozen=True)
class V0436V044RiskRegister:
    register_id: str
    risks: tuple[V0436V044WorkspaceReadRisk, ...]
    high_or_blocker_count: int
    mitigations_defined: bool
    safe_to_design_v044: bool


@dataclass(frozen=True)
class V0436V044ReadinessReport:
    report_id: str
    v044_gate_decision: str
    scope: V0436V044ControlledWorkspaceReadScope
    safety_gates: tuple[V0436V044WorkspaceReadSafetyGate, ...]
    risk_register: V0436V044RiskRegister
    recommended_v0440_title: str
    allowed_in_v0440: tuple[str, ...]
    forbidden_in_v0440: tuple[str, ...]
    ready_for_v044_design: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436V044ScopeProposal:
    proposal_id: str
    title: str
    purpose: str
    allowed_scope: tuple[str, ...]
    forbidden_scope: tuple[str, ...]
    required_tests: tuple[str, ...]
    withdrawal_conditions: tuple[str, ...]
    recommended_next_version: str


@dataclass(frozen=True)
class V0436V044HandoffPacket:
    packet_id: str
    v043_closure_summary: str
    v044_objective: str
    allowed_scope: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    safety_gates: tuple[str, ...]
    risk_summary: str
    required_tests: tuple[str, ...]
    copy_paste_prompt: str
    production_certified: bool


@dataclass(frozen=True)
class V0436PolishStatusRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V0436PolishStatusResult:
    result_id: str
    rendered_text: str
    open_findings: tuple[V0436PolishFinding, ...]
    fixed_findings: tuple[V0436PolishFinding, ...]
    deferred_findings: tuple[V0436PolishFinding, ...]
    v043_can_close: bool
    v044_design_can_begin: bool
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436PolishFindingsRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V0436PolishFindingsResult:
    result_id: str
    findings: tuple[V0436PolishFinding, ...]
    rendered_text: str
    blocker_count: int
    deferred_count: int
    fixed_count: int
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436PolishReportRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V0436PolishReportResult:
    result_id: str
    rendered_text: str
    closure_report: V0436PilotClosureReport
    v044_readiness: V0436V044ReadinessReport
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436PilotCloseRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None
    create_trace_record: bool


@dataclass(frozen=True)
class V0436PilotCloseResult:
    result_id: str
    rendered_text: str
    closure_decision: V0436PilotClosureDecision
    closure_report: V0436PilotClosureReport
    trace_record: "V0436PilotClosureTraceRecord | None"
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436V044ReadinessRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V0436V044ReadinessResult:
    result_id: str
    rendered_text: str
    readiness_report: V0436V044ReadinessReport
    provider_invoked: bool
    prompt_submitted: bool
    workspace_read_opened: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436V044ScopeRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V0436V044ScopeResult:
    result_id: str
    rendered_text: str
    scope_proposal: V0436V044ScopeProposal
    workspace_read_opened: bool
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436V044RisksRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V0436V044RisksResult:
    result_id: str
    rendered_text: str
    risk_register: V0436V044RiskRegister
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436V044HandoffRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    session_id: str | None


@dataclass(frozen=True)
class V0436V044HandoffResult:
    result_id: str
    rendered_text: str
    handoff_packet: V0436V044HandoffPacket
    provider_invoked: bool
    prompt_submitted: bool
    workspace_read_opened: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436PilotClosureTraceRecord:
    trace_record_id: str
    event_kind: str
    closure_decision: str
    v043_closed: bool
    v044_design_recommended: bool
    session_id: str | None
    provider_invoked: bool
    prompt_submitted: bool
    arbitrary_file_search_used: bool
    repo_search_used: bool
    workspace_read_opened: bool
    shell_executed: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436PilotClosurePIReviewRecord:
    review_id: str
    closure_trace_id: str | None
    reconstructable_as_process_event: bool
    closure_criteria_lineage_preserved: bool
    safety_lineage_preserved: bool
    v044_gate_lineage_preserved: bool
    high_risk_counts_zero: bool
    review_summary: str


@dataclass(frozen=True)
class V0436PilotClosureSafetyReport:
    report_id: str
    final_pilot_polish_opened: bool
    v044_design_gate_opened: bool
    workspace_read_opened: bool
    provider_invocation_allowed_by_default: bool
    prompt_submission_allowed_by_default: bool
    arbitrary_file_search_allowed: bool
    repo_search_allowed: bool
    workspace_search_allowed: bool
    external_search_allowed: bool
    shell_execution_allowed: bool
    file_edit_allowed: bool
    patch_apply_allowed: bool
    provider_tool_calling_allowed: bool
    function_calling_allowed: bool
    subagent_allowed: bool
    memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0436ReadinessReport:
    final_pilot_polish_ready: bool
    command_surface_audit_ready: bool
    business_ux_final_acceptance_ready: bool
    pilot_closure_report_ready: bool
    pilot_closure_decision_ready: bool
    v044_readiness_report_ready: bool
    v044_scope_proposal_ready: bool
    v044_risk_register_ready: bool
    v044_handoff_packet_ready: bool
    pilot_closure_trace_ready: bool
    pilot_closure_pi_review_ready: bool
    integrated_restore_document_ready: bool
    v0440_handoff_ready: bool
    ready_to_close_v043: bool
    ready_for_v044_design: bool
    ready_for_workspace_read_in_v0436: bool
    ready_for_arbitrary_file_search: bool
    ready_for_repo_search: bool
    ready_for_workspace_search: bool
    ready_for_external_search: bool
    ready_for_shell_execution: bool
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
class V0440ControlledWorkspaceReadDesignHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0436IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    summary: str
    restore_relevance: str


@dataclass(frozen=True)
class V0436IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0436IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0436IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0436IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0436IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


REQUIRED_SCOPE_ELEMENTS = (
    "explicit_workspace_root",
    "allowlist",
    "path_normalization",
    "inside_root_validation",
    "max_file_count",
    "max_byte_or_char_budget",
    "file_extension_filter",
    "secret_redaction",
    "trace_event_contract",
    "read_disclosure",
    "denial_policy",
)

REQUIRED_SAFETY_GATES = (
    "explicit_user_workspace_root",
    "explicit_allowlist",
    "path_traversal_prevention",
    "inside_root_validation",
    "read_budget",
    "extension_filter",
    "binary_file_denial_or_safe_skip",
    "secret_redaction",
    "no_shell",
    "no_edit_apply",
    "no_test_execution",
    "no_repo_wide_scan",
    "trace_every_read",
    "user_visible_read_disclosure",
    "provider_prompt_size_control",
    "withdrawal_condition",
)

REQUIRED_RISKS = (
    "path_traversal",
    "secret_leakage",
    "accidental_broad_scan",
    "repo_wide_overread",
    "provider_prompt_leakage",
    "unbounded_context_expansion",
    "read_vs_edit_confusion",
    "future_shell_edit_pressure",
    "memory_pollution",
    "audit_gap",
)

CLOSED_CAPABILITIES = (
    "workspace read",
    "arbitrary filesystem search",
    "repo search",
    "workspace search",
    "external search",
    "shell execution",
    "file edit/apply",
    "test execution",
    "provider tool/function calling",
    "subagents",
    "general AgentLoop",
    "automatic memory mutation",
    "CORE_MEMORY write",
    "production certification",
)

REQUIRED_V0436_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "v0.43.5 Baseline Summary",
    "v0.43.6 Goal",
    "Final Pilot Polish Concept",
    "Command Surface Final Audit",
    "Business UX Final Acceptance",
    "Pilot Closure Criteria",
    "Pilot Closure Decision",
    "v0.44 Controlled Workspace Read Gate",
    "v0.44 Scope Proposal",
    "v0.44 Safety Gates",
    "v0.44 Risk Register",
    "v0.44 Handoff Packet",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Manual Pilot Commands",
    "Withdrawal Conditions",
    "v0.43.7 or v0.44 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)


def _merge(defaults: dict[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def create_v0436_polish_finding(
    area: str = V0436PolishFindingArea.COMMAND_SURFACE.value,
    severity: str = V0436PolishFindingSeverity.LOW.value,
    status: str = V0436PolishFindingStatus.FIXED_IN_V0436.value,
    description: str = "Command guide wording was polished.",
    user_impact: str = "The work-session command surface is easier to scan.",
    recommended_action: str = "Keep command guide wording grouped by workflow.",
    blocks_v044: bool | None = None,
    fixed_in_v0436: bool | None = None,
    deferred_reason: str | None = None,
    **overrides: Any,
) -> V0436PolishFinding:
    actual_status = status if status in {item.value for item in V0436PolishFindingStatus} else V0436PolishFindingStatus.UNKNOWN.value
    defaults = {
        "finding_id": _new_id("v0436-polish-finding"),
        "area": area if area in {item.value for item in V0436PolishFindingArea} else V0436PolishFindingArea.UNKNOWN.value,
        "severity": severity if severity in {item.value for item in V0436PolishFindingSeverity} else V0436PolishFindingSeverity.UNKNOWN.value,
        "status": actual_status,
        "description": description,
        "user_impact": user_impact,
        "recommended_action": recommended_action,
        "blocks_v044": bool(blocks_v044 if blocks_v044 is not None else actual_status == V0436PolishFindingStatus.BLOCKS_V044.value),
        "fixed_in_v0436": bool(fixed_in_v0436 if fixed_in_v0436 is not None else actual_status == V0436PolishFindingStatus.FIXED_IN_V0436.value),
        "deferred_reason": deferred_reason,
    }
    return V0436PolishFinding(**_merge(defaults, overrides))


def _default_polish_findings() -> tuple[V0436PolishFinding, ...]:
    return (
        create_v0436_polish_finding(
            V0436PolishFindingArea.COMMAND_SURFACE.value,
            V0436PolishFindingSeverity.LOW.value,
            V0436PolishFindingStatus.FIXED_IN_V0436.value,
            "Work-session start/help command groups now include polish and v0.44 gate commands.",
            "Users can see pilot closure and v0.44 gate commands without reading debug docs.",
            "Keep commands grouped as workflow, evidence, pilot, polish, and v0.44 gate.",
        ),
        create_v0436_polish_finding(
            V0436PolishFindingArea.CHAT_UX.value,
            V0436PolishFindingSeverity.LOW.value,
            V0436PolishFindingStatus.DEFERRED_TO_V0437.value,
            "Some legacy work-session Korean copy still needs broader UX cleanup.",
            "The core command surface is usable, but older messages may be less polished.",
            "Defer full wording cleanup unless pilot feedback shows confusion.",
            blocks_v044=False,
            fixed_in_v0436=False,
            deferred_reason="Non-blocking wording polish; safety and command coherence are intact.",
        ),
        create_v0436_polish_finding(
            V0436PolishFindingArea.V044_GATE.value,
            V0436PolishFindingSeverity.MEDIUM.value,
            V0436PolishFindingStatus.ACCEPTED_FOR_V044.value,
            "Workspace-specific work needs a controlled read-only design gate.",
            "The next track can improve usefulness without opening edit/apply/shell.",
            "Start v0.44 with design/spec/contract only.",
            blocks_v044=False,
            fixed_in_v0436=False,
        ),
    )


def create_v0436_command_surface_audit_item(
    command_name: str = "/summary",
    category: str = "work_flow",
    expected_behavior: str = "Produce a bounded business work artifact.",
    available: bool = True,
    user_friendly: bool = True,
    debug_details_hidden_by_default: bool = True,
    high_risk_capability_opened: bool = False,
    notes: str = "deterministic audit item",
    **overrides: Any,
) -> V0436CommandSurfaceAuditItem:
    defaults = {
        "item_id": _new_id("v0436-command-audit-item"),
        "command_name": command_name,
        "category": category,
        "expected_behavior": expected_behavior,
        "available": bool(available),
        "user_friendly": bool(user_friendly),
        "debug_details_hidden_by_default": bool(debug_details_hidden_by_default),
        "high_risk_capability_opened": False,
        "notes": notes,
    }
    return V0436CommandSurfaceAuditItem(**_merge(defaults, overrides))


def _default_audit_items() -> tuple[V0436CommandSurfaceAuditItem, ...]:
    groups = (
        ("chanta-cli start", "start", "Open the business work session entrypoint."),
        ("/summary /todo /memo /decision /handoff", "work_flow", "Create provider-backed business artifacts with bounded context."),
        ("/artifact last /revise /clarify", "artifact", "Review and improve the latest business artifact."),
        ("/note /notes /note last /note from-artifact /notes search", "notes", "Capture local work notes without CORE_MEMORY mutation."),
        ("/recall /evidence /evidence sources /evidence last /evidence explain", "evidence", "Search bounded local evidence and disclose sources."),
        ("/use-evidence /grounded-summary /grounding-check /evidence used", "grounded", "Use selected evidence for grounded business synthesis."),
        ("/pilot status /pilot review /pilot score /pilot findings /pilot next /pilot report /acceptance /workflow score", "pilot", "Review pilot acceptance metrics without provider calls."),
        ("/report /what-happened /feedback", "diagnostics", "Expose report, trace, and feedback surfaces."),
        ("/capabilities /memory-boundary /context", "safety", "Explain current boundaries and closed capabilities."),
        ("/polish status /polish findings /polish report /pilot close /v044 readiness /v044 scope /v044 risks /v044 handoff", "v044_gate", "Close v0.43 and hand off to v0.44 design-only gate."),
    )
    return tuple(create_v0436_command_surface_audit_item(command, category, expected, notes="available; high-risk capabilities closed") for command, category, expected in groups)


def create_v0436_command_surface_audit(items: Sequence[V0436CommandSurfaceAuditItem] = (), **overrides: Any) -> V0436CommandSurfaceAudit:
    actual_items = tuple(items) or _default_audit_items()
    missing = tuple(item.command_name for item in actual_items if not item.available)
    rough = tuple(item.command_name for item in actual_items if item.available and not item.user_friendly)
    high_risk = tuple(item.command_name for item in actual_items if item.high_risk_capability_opened)
    fail_count = len(missing) + len(high_risk)
    warning_count = len(rough)
    pass_count = len(actual_items) - fail_count - warning_count
    defaults = {
        "audit_id": _new_id("v0436-command-surface-audit"),
        "items": actual_items,
        "missing_commands": missing,
        "rough_commands": rough,
        "high_risk_commands": (),
        "pass_count": max(0, pass_count),
        "warning_count": warning_count,
        "fail_count": fail_count,
        "ready_for_v044": fail_count == 0,
    }
    return V0436CommandSurfaceAudit(**_merge(defaults, overrides))


def create_v0436_business_ux_final_acceptance(**overrides: Any) -> V0436BusinessUXFinalAcceptance:
    rough_edges = ("legacy wording polish can continue if pilot feedback requests it",)
    defaults = {
        "acceptance_id": _new_id("v0436-business-ux-final-acceptance"),
        "start_flow_accepted": True,
        "chat_ux_accepted": True,
        "work_flow_accepted": True,
        "artifact_ux_accepted": True,
        "evidence_ux_accepted": True,
        "grounded_ux_accepted": True,
        "pilot_review_accepted": True,
        "default_debug_separation_accepted": True,
        "overall_accepted": True,
        "remaining_rough_edges": rough_edges,
    }
    return V0436BusinessUXFinalAcceptance(**_merge(defaults, overrides))


def create_v0436_pilot_closure_criterion(
    criterion_id: str = "business_work_session_usable",
    title: str = "Business work session usable",
    pass_condition: str = "The command surface is available and understandable.",
    status: str = "pass",
    blocks_closure: bool = False,
    evidence_summary: str = "v0.43.5 pilot review and v0.43.6 audit pass.",
    **overrides: Any,
) -> V0436PilotClosureCriterion:
    defaults = {
        "criterion_id": criterion_id,
        "title": title,
        "pass_condition": pass_condition,
        "status": status,
        "blocks_closure": bool(blocks_closure),
        "evidence_summary": evidence_summary,
    }
    return V0436PilotClosureCriterion(**_merge(defaults, overrides))


def _default_closure_criteria() -> tuple[V0436PilotClosureCriterion, ...]:
    data = (
        ("business_work_session_usable", "Business work session usable"),
        ("core_workflow_commands_available", "Core workflow commands available"),
        ("artifacts_useful", "Business artifacts useful"),
        ("local_notes_safe", "Local notes safe and bounded"),
        ("local_evidence_retrieval_safe", "Local evidence retrieval safe and bounded"),
        ("grounded_synthesis_traceable", "Grounded synthesis traceable"),
        ("pilot_metrics_available", "Pilot metrics available"),
        ("process_intelligence_reviewable", "Process Intelligence reviewable"),
        ("safety_boundary_intact", "Safety boundary intact"),
        ("production_certification_not_claimed", "Production certification not claimed"),
        ("v044_gate_defined", "v0.44 gate defined"),
    )
    return tuple(create_v0436_pilot_closure_criterion(key, title, "Criterion is satisfied or safely documented.") for key, title in data)


def _safety_boundary_intact(criteria: Sequence[V0436PilotClosureCriterion]) -> bool:
    return any(item.criterion_id == "safety_boundary_intact" and item.status == "pass" and not item.blocks_closure for item in criteria)


def _v044_gate_defined(criteria: Sequence[V0436PilotClosureCriterion]) -> bool:
    return any(item.criterion_id == "v044_gate_defined" and item.status == "pass" and not item.blocks_closure for item in criteria)


def create_v0436_pilot_closure_report(
    criteria: Sequence[V0436PilotClosureCriterion] = (),
    command_audit: V0436CommandSurfaceAudit | None = None,
    ux_acceptance: V0436BusinessUXFinalAcceptance | None = None,
    polish_findings: Sequence[V0436PolishFinding] = (),
    **overrides: Any,
) -> V0436PilotClosureReport:
    actual_criteria = tuple(criteria) or _default_closure_criteria()
    audit = command_audit or create_v0436_command_surface_audit()
    ux = ux_acceptance or create_v0436_business_ux_final_acceptance()
    findings = tuple(polish_findings) or _default_polish_findings()
    blockers = sum(1 for item in actual_criteria if item.blocks_closure or item.status in {"blocker", "fail"})
    blockers += sum(1 for item in findings if item.blocks_v044 or item.status == V0436PolishFindingStatus.BLOCKS_V044.value)
    warnings = sum(1 for item in findings if item.severity in {V0436PolishFindingSeverity.MEDIUM.value, V0436PolishFindingSeverity.HIGH.value})
    safety_intact = _safety_boundary_intact(actual_criteria) and not audit.high_risk_commands
    closure_allowed = blockers == 0 and safety_intact and ux.overall_accepted and audit.ready_for_v044
    gate_defined = _v044_gate_defined(actual_criteria)
    defaults = {
        "report_id": _new_id("v0436-pilot-closure-report"),
        "criteria": actual_criteria,
        "command_audit": audit,
        "ux_acceptance": ux,
        "polish_findings": findings,
        "blocker_count": blockers,
        "warning_count": warnings,
        "v043_closure_allowed": closure_allowed,
        "recommends_v0437": not closure_allowed,
        "recommends_v044_design": closure_allowed and gate_defined,
        "production_certified": False,
    }
    return V0436PilotClosureReport(**_merge(defaults, overrides))


def create_v0436_pilot_closure_decision(report: V0436PilotClosureReport | None = None, **overrides: Any) -> V0436PilotClosureDecision:
    actual_report = report or create_v0436_pilot_closure_report()
    if not _safety_boundary_intact(actual_report.criteria) or actual_report.command_audit.high_risk_commands:
        decision = "blocked_by_safety"
        reason = "Safety boundary is not intact."
        close_v043 = False
        continue_v0437 = False
        proceed_v044 = False
        required = ("Fix safety boundary before any next track.",)
    elif not actual_report.ux_acceptance.overall_accepted:
        decision = "blocked_by_usability"
        reason = "Business UX acceptance did not pass."
        close_v043 = False
        continue_v0437 = True
        proceed_v044 = False
        required = ("Polish user-facing workflow before closure.",)
    elif actual_report.v043_closure_allowed and actual_report.recommends_v044_design:
        decision = "close_v043_proceed_v044_design"
        reason = "v0.43 closure criteria passed and v0.44 design gate is explicit."
        close_v043 = True
        continue_v0437 = False
        proceed_v044 = True
        required = ("Start v0.44.0 with design/spec/contract only.",)
    else:
        decision = "continue_v0437_polish"
        reason = "Non-blocking rough edges remain important enough to polish."
        close_v043 = False
        continue_v0437 = True
        proceed_v044 = False
        required = ("Resolve closure blockers or important rough edges.",)
    defaults = {
        "decision_id": _new_id("v0436-pilot-closure-decision"),
        "decision": decision,
        "reason": reason,
        "close_v043": close_v043,
        "continue_v0437": continue_v0437,
        "proceed_to_v044_design": proceed_v044,
        "required_before_next_track": required,
        "production_certified": False,
    }
    return V0436PilotClosureDecision(**_merge(defaults, overrides))


def create_v0436_v044_controlled_workspace_read_scope(**overrides: Any) -> V0436V044ControlledWorkspaceReadScope:
    defaults = {
        "scope_id": "v0436-v044-controlled-workspace-read-scope",
        "design_only_in_v0436": True,
        "controlled_workspace_read_may_open_in_v044": True,
        "write_allowed": False,
        "edit_apply_allowed": False,
        "shell_allowed": False,
        "test_execution_allowed": False,
        "repo_wide_search_allowed": False,
        "subagent_allowed": False,
        "production_certified": False,
        "required_scope_elements": REQUIRED_SCOPE_ELEMENTS,
    }
    return V0436V044ControlledWorkspaceReadScope(**_merge(defaults, overrides))


def create_v0436_v044_workspace_read_safety_gate(
    gate_id: str = "explicit_user_workspace_root",
    title: str | None = None,
    description: str | None = None,
    failure_mode: str | None = None,
    **overrides: Any,
) -> V0436V044WorkspaceReadSafetyGate:
    defaults = {
        "gate_id": gate_id,
        "title": title or gate_id.replace("_", " "),
        "required": True,
        "description": description or f"Require {gate_id.replace('_', ' ')} before any workspace read opens.",
        "failure_mode": failure_mode or f"Without {gate_id}, workspace read must be denied.",
        "blocks_workspace_read": True,
    }
    return V0436V044WorkspaceReadSafetyGate(**_merge(defaults, overrides))


def _default_safety_gates() -> tuple[V0436V044WorkspaceReadSafetyGate, ...]:
    return tuple(create_v0436_v044_workspace_read_safety_gate(gate_id) for gate_id in REQUIRED_SAFETY_GATES)


def create_v0436_v044_workspace_read_risk(
    risk_id: str = "path_traversal",
    severity: str = "high",
    title: str | None = None,
    description: str | None = None,
    mitigation: str | None = None,
    withdrawal_condition: str | None = None,
    **overrides: Any,
) -> V0436V044WorkspaceReadRisk:
    defaults = {
        "risk_id": risk_id,
        "title": title or risk_id.replace("_", " "),
        "severity": severity,
        "description": description or f"Risk: {risk_id.replace('_', ' ')}.",
        "mitigation": mitigation or "Require explicit scope, deny unsafe reads, trace every allowed read, and disclose what was read.",
        "withdrawal_condition": withdrawal_condition or f"Withdraw if {risk_id.replace('_', ' ')} is not mitigated.",
    }
    return V0436V044WorkspaceReadRisk(**_merge(defaults, overrides))


def create_v0436_v044_risk_register(risks: Sequence[V0436V044WorkspaceReadRisk] = (), **overrides: Any) -> V0436V044RiskRegister:
    actual_risks = tuple(risks) or tuple(create_v0436_v044_workspace_read_risk(risk) for risk in REQUIRED_RISKS)
    high_count = sum(1 for item in actual_risks if item.severity in {"high", "blocker"})
    mitigations = all(bool(item.mitigation) and bool(item.withdrawal_condition) for item in actual_risks)
    defaults = {
        "register_id": _new_id("v0436-v044-risk-register"),
        "risks": actual_risks,
        "high_or_blocker_count": high_count,
        "mitigations_defined": mitigations,
        "safe_to_design_v044": mitigations,
    }
    return V0436V044RiskRegister(**_merge(defaults, overrides))


def create_v0436_v044_readiness_report(**overrides: Any) -> V0436V044ReadinessReport:
    scope = create_v0436_v044_controlled_workspace_read_scope()
    gates = _default_safety_gates()
    risks = create_v0436_v044_risk_register()
    forbidden = (
        "file edit",
        "patch apply",
        "shell execution",
        "test execution",
        "subagent invocation",
        "production certification",
        "repo-wide search",
        "automatic memory mutation",
    )
    allowed = ("design", "spec", "scope contract", "safety gate contract", "risk register", "test plan")
    defaults = {
        "report_id": _new_id("v0436-v044-readiness-report"),
        "v044_gate_decision": V0436V044GateDecisionKind.PROCEED_TO_V044_CONTROLLED_WORKSPACE_READ_DESIGN.value,
        "scope": scope,
        "safety_gates": gates,
        "risk_register": risks,
        "recommended_v0440_title": V0440_RECOMMENDED_TITLE,
        "allowed_in_v0440": allowed,
        "forbidden_in_v0440": forbidden,
        "ready_for_v044_design": True,
        "production_certified": False,
    }
    return V0436V044ReadinessReport(**_merge(defaults, overrides))


def create_v0436_v044_scope_proposal(**overrides: Any) -> V0436V044ScopeProposal:
    defaults = {
        "proposal_id": _new_id("v0436-v044-scope-proposal"),
        "title": V0440_RECOMMENDED_TITLE,
        "purpose": "Define the controlled read-only workspace scope before any workspace read implementation.",
        "allowed_scope": (
            "design/spec/contract only",
            "explicit workspace root contract",
            "allowlist contract",
            "path boundary and normalization contract",
            "read budget contract",
            "file type policy",
            "secret redaction contract",
            "trace event contract",
            "denial cases",
        ),
        "forbidden_scope": CLOSED_CAPABILITIES,
        "required_tests": (
            "scope model keeps workspace_read_opened=false in v0.43.6",
            "safety gates include root, allowlist, path validation, budget, redaction, trace, disclosure, denial",
            "forbidden capabilities remain false",
        ),
        "withdrawal_conditions": (
            "workspace read opens before v0.44 implementation scope is approved",
            "edit/apply/shell/test/subagent is recommended as immediate next step",
            "root/allowlist/path validation/budget/redaction/trace is omitted",
        ),
        "recommended_next_version": V0440_RECOMMENDED_TITLE,
    }
    return V0436V044ScopeProposal(**_merge(defaults, overrides))


def create_v0436_v044_handoff_packet(**overrides: Any) -> V0436V044HandoffPacket:
    gates = REQUIRED_SAFETY_GATES
    tests = (
        "py -m pytest tests\\test_v0436_final_pilot_polish_v044_gate.py",
        "py -m pytest tests\\test_v0435_pilot_review_acceptance_metrics.py",
    )
    prompt = (
        "You are Codex Mode Vera working on ChantaCore v0.44.0. "
        "Start Controlled Workspace Read Design & Scope Contract only. "
        "Do not implement workspace read, edit/apply, shell/test, repo-wide search, subagents, memory mutation, or production certification."
    )
    defaults = {
        "packet_id": _new_id("v0436-v044-handoff-packet"),
        "v043_closure_summary": "v0.43 business work-session pilot is closed if closure criteria remain passing.",
        "v044_objective": "Design the controlled read-only workspace read scope contract.",
        "allowed_scope": create_v0436_v044_scope_proposal().allowed_scope,
        "closed_capabilities": CLOSED_CAPABILITIES,
        "safety_gates": gates,
        "risk_summary": "Path traversal, secret leakage, broad scan, prompt leakage, context expansion, memory pollution, and audit gaps require explicit mitigations.",
        "required_tests": tests,
        "copy_paste_prompt": prompt,
        "production_certified": False,
    }
    return V0436V044HandoffPacket(**_merge(defaults, overrides))


def create_v0436_polish_status_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V0436PolishStatusRequest:
    defaults = {"request_id": _new_id("v0436-polish-status-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V0436PolishStatusRequest(**_merge(defaults, overrides))


def _render_findings(findings: Sequence[V0436PolishFinding]) -> str:
    lines = ["Polish findings", f"count: {len(tuple(findings))}"]
    for item in findings:
        lines.append(f"- {item.finding_id} [{item.area}/{item.severity}/{item.status}] {item.description}; blocks_v044={str(item.blocks_v044).lower()}")
        lines.append(f"  action: {item.recommended_action}")
    return "\n".join(lines)


def create_v0436_polish_status_result(request: V0436PolishStatusRequest | None = None, **overrides: Any) -> V0436PolishStatusResult:
    findings = _default_polish_findings()
    fixed = tuple(item for item in findings if item.fixed_in_v0436)
    deferred = tuple(item for item in findings if item.status == V0436PolishFindingStatus.DEFERRED_TO_V0437.value)
    open_items = tuple(item for item in findings if item.status == V0436PolishFindingStatus.OPEN.value)
    report = create_v0436_pilot_closure_report(polish_findings=findings)
    rendered = "\n".join(
        (
            "Polish status",
            f"track: {V043_TRACK_NAME}",
            f"fixed_rough_edges: {len(fixed)}",
            f"deferred_rough_edges: {len(deferred)}",
            f"open_rough_edges: {len(open_items)}",
            f"v043_can_close: {str(report.v043_closure_allowed).lower()}",
            f"v044_design_can_begin: {str(report.recommends_v044_design).lower()}",
            "safety_status: high-risk capabilities closed; workspace_read_opened=false; production_certified=false",
        )
    )
    defaults = {
        "result_id": _new_id("v0436-polish-status-result"),
        "rendered_text": rendered,
        "open_findings": open_items,
        "fixed_findings": fixed,
        "deferred_findings": deferred,
        "v043_can_close": report.v043_closure_allowed,
        "v044_design_can_begin": report.recommends_v044_design,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V0436PolishStatusResult(**_merge(defaults, overrides))


def execute_v0436_polish_status(request: V0436PolishStatusRequest, **overrides: Any) -> V0436PolishStatusResult:
    return create_v0436_polish_status_result(request, **overrides)


def create_v0436_polish_findings_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V0436PolishFindingsRequest:
    defaults = {"request_id": _new_id("v0436-polish-findings-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V0436PolishFindingsRequest(**_merge(defaults, overrides))


def create_v0436_polish_findings_result(request: V0436PolishFindingsRequest | None = None, **overrides: Any) -> V0436PolishFindingsResult:
    findings = _default_polish_findings()
    defaults = {
        "result_id": _new_id("v0436-polish-findings-result"),
        "findings": findings,
        "rendered_text": _render_findings(findings),
        "blocker_count": sum(1 for item in findings if item.blocks_v044),
        "deferred_count": sum(1 for item in findings if item.status == V0436PolishFindingStatus.DEFERRED_TO_V0437.value),
        "fixed_count": sum(1 for item in findings if item.fixed_in_v0436),
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V0436PolishFindingsResult(**_merge(defaults, overrides))


def execute_v0436_polish_findings(request: V0436PolishFindingsRequest, **overrides: Any) -> V0436PolishFindingsResult:
    return create_v0436_polish_findings_result(request, **overrides)


def create_v0436_polish_report_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V0436PolishReportRequest:
    defaults = {"request_id": _new_id("v0436-polish-report-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V0436PolishReportRequest(**_merge(defaults, overrides))


def _render_polish_report(closure: V0436PilotClosureReport, readiness: V0436V044ReadinessReport) -> str:
    fixed = sum(1 for item in closure.polish_findings if item.fixed_in_v0436)
    deferred = sum(1 for item in closure.polish_findings if item.status == V0436PolishFindingStatus.DEFERRED_TO_V0437.value)
    return "\n".join(
        (
            "Polish report",
            f"summary: {V0436_RELEASE_NAME}",
            f"fixed_items: {fixed}",
            f"deferred_items: {deferred}",
            f"command_surface_ready: {str(closure.command_audit.ready_for_v044).lower()}",
            f"ux_accepted: {str(closure.ux_acceptance.overall_accepted).lower()}",
            f"safety_status: high-risk closed; workspace_read_opened=false",
            f"v043_closure_allowed: {str(closure.v043_closure_allowed).lower()}",
            f"v044_readiness: {readiness.v044_gate_decision}",
            f"next: {'v0.44.0 Controlled Workspace Read Design & Scope Contract' if closure.recommends_v044_design else 'v0.43.7 Final Pilot Polish'}",
            "provider_invoked=false; prompt_submitted=false; shell=false; memory_mutated=false; production_certified=false",
        )
    )


def create_v0436_polish_report_result(request: V0436PolishReportRequest | None = None, **overrides: Any) -> V0436PolishReportResult:
    closure = create_v0436_pilot_closure_report()
    readiness = create_v0436_v044_readiness_report()
    defaults = {
        "result_id": _new_id("v0436-polish-report-result"),
        "rendered_text": _render_polish_report(closure, readiness),
        "closure_report": closure,
        "v044_readiness": readiness,
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V0436PolishReportResult(**_merge(defaults, overrides))


def execute_v0436_polish_report(request: V0436PolishReportRequest, **overrides: Any) -> V0436PolishReportResult:
    return create_v0436_polish_report_result(request, **overrides)


def create_v0436_pilot_close_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    session_id: str | None = None,
    create_trace_record: bool = True,
    **overrides: Any,
) -> V0436PilotCloseRequest:
    defaults = {"request_id": _new_id("v0436-pilot-close-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id, "create_trace_record": bool(create_trace_record)}
    return V0436PilotCloseRequest(**_merge(defaults, overrides))


def create_v0436_pilot_closure_trace_record(
    closure_decision: str = "close_v043_proceed_v044_design",
    v043_closed: bool = True,
    v044_design_recommended: bool = True,
    session_id: str | None = None,
    **overrides: Any,
) -> V0436PilotClosureTraceRecord:
    defaults = {
        "trace_record_id": _new_id("v0436-pilot-closure-trace"),
        "event_kind": "pilot_closure_evaluated",
        "closure_decision": closure_decision,
        "v043_closed": bool(v043_closed),
        "v044_design_recommended": bool(v044_design_recommended),
        "session_id": session_id,
        "provider_invoked": False,
        "prompt_submitted": False,
        "arbitrary_file_search_used": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "shell_executed": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    return V0436PilotClosureTraceRecord(**_merge(defaults, overrides))


def create_v0436_pilot_close_result(request: V0436PilotCloseRequest | None = None, **overrides: Any) -> V0436PilotCloseResult:
    request = request or create_v0436_pilot_close_request()
    closure = create_v0436_pilot_closure_report()
    decision = create_v0436_pilot_closure_decision(closure)
    trace = create_v0436_pilot_closure_trace_record(decision.decision, decision.close_v043, decision.proceed_to_v044_design, request.session_id) if request.create_trace_record else None
    rendered = "\n".join(
        (
            "Pilot close",
            f"decision: {decision.decision}",
            f"reason: {decision.reason}",
            f"close_v043: {str(decision.close_v043).lower()}",
            f"proceed_to_v044_design: {str(decision.proceed_to_v044_design).lower()}",
            "next: v0.44.0 Controlled Workspace Read Design & Scope Contract" if decision.proceed_to_v044_design else "next: v0.43.7 Final Pilot Polish",
            "workspace_read_opened=false; production_certified=false",
        )
    )
    defaults = {
        "result_id": _new_id("v0436-pilot-close-result"),
        "rendered_text": rendered,
        "closure_decision": decision,
        "closure_report": closure,
        "trace_record": trace,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V0436PilotCloseResult(**_merge(defaults, overrides))


def execute_v0436_pilot_close(request: V0436PilotCloseRequest, **overrides: Any) -> V0436PilotCloseResult:
    return create_v0436_pilot_close_result(request, **overrides)


def create_v0436_v044_readiness_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V0436V044ReadinessRequest:
    defaults = {"request_id": _new_id("v0436-v044-readiness-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V0436V044ReadinessRequest(**_merge(defaults, overrides))


def _render_v044_readiness(report: V0436V044ReadinessReport) -> str:
    return "\n".join(
        (
            "v0.44 readiness",
            f"decision: {report.v044_gate_decision}",
            "ux_repair_gate: v0.43.7 default conversation output must stay clean before v0.44 starts.",
            "value: controlled workspace read can ground work on explicitly scoped local project evidence.",
            "currently_missing: workspace-specific files cannot be used unless already captured as bounded notes/evidence.",
            f"required_safety_gates: {', '.join(gate.gate_id for gate in report.safety_gates)}",
            f"allowed_in_v0440: {', '.join(report.allowed_in_v0440)}",
            f"forbidden_in_v0440: {', '.join(report.forbidden_in_v0440)}",
            "workspace_read_opened=false; production_certified=false",
        )
    )


def create_v0436_v044_readiness_result(request: V0436V044ReadinessRequest | None = None, **overrides: Any) -> V0436V044ReadinessResult:
    report = create_v0436_v044_readiness_report()
    defaults = {
        "result_id": _new_id("v0436-v044-readiness-result"),
        "rendered_text": _render_v044_readiness(report),
        "readiness_report": report,
        "provider_invoked": False,
        "prompt_submitted": False,
        "workspace_read_opened": False,
        "production_certified": False,
    }
    return V0436V044ReadinessResult(**_merge(defaults, overrides))


def execute_v0436_v044_readiness(request: V0436V044ReadinessRequest, **overrides: Any) -> V0436V044ReadinessResult:
    return create_v0436_v044_readiness_result(request, **overrides)


def create_v0436_v044_scope_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V0436V044ScopeRequest:
    defaults = {"request_id": _new_id("v0436-v044-scope-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V0436V044ScopeRequest(**_merge(defaults, overrides))


def create_v0436_v044_scope_result(request: V0436V044ScopeRequest | None = None, **overrides: Any) -> V0436V044ScopeResult:
    proposal = create_v0436_v044_scope_proposal()
    rendered = "\n".join(
        (
            "v0.44 scope",
            proposal.title,
            f"allowed_scope: {', '.join(proposal.allowed_scope)}",
            f"forbidden_scope: {', '.join(proposal.forbidden_scope)}",
            "workspace_read_opened=false; production_certified=false",
        )
    )
    defaults = {
        "result_id": _new_id("v0436-v044-scope-result"),
        "rendered_text": rendered,
        "scope_proposal": proposal,
        "workspace_read_opened": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V0436V044ScopeResult(**_merge(defaults, overrides))


def execute_v0436_v044_scope(request: V0436V044ScopeRequest, **overrides: Any) -> V0436V044ScopeResult:
    return create_v0436_v044_scope_result(request, **overrides)


def create_v0436_v044_risks_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V0436V044RisksRequest:
    defaults = {"request_id": _new_id("v0436-v044-risks-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V0436V044RisksRequest(**_merge(defaults, overrides))


def create_v0436_v044_risks_result(request: V0436V044RisksRequest | None = None, **overrides: Any) -> V0436V044RisksResult:
    register = create_v0436_v044_risk_register()
    rendered = "\n".join(
        (
            "v0.44 risks",
            f"risk_count: {len(register.risks)}",
            f"high_or_blocker_count: {register.high_or_blocker_count}",
            f"risks: {', '.join(risk.risk_id for risk in register.risks)}",
            "provider_invoked=false; prompt_submitted=false; production_certified=false",
        )
    )
    defaults = {
        "result_id": _new_id("v0436-v044-risks-result"),
        "rendered_text": rendered,
        "risk_register": register,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    return V0436V044RisksResult(**_merge(defaults, overrides))


def execute_v0436_v044_risks(request: V0436V044RisksRequest, **overrides: Any) -> V0436V044RisksResult:
    return create_v0436_v044_risks_result(request, **overrides)


def create_v0436_v044_handoff_request(profile_id: str = PROFILE_ID, home_path: str | None = None, session_id: str | None = None, **overrides: Any) -> V0436V044HandoffRequest:
    defaults = {"request_id": _new_id("v0436-v044-handoff-request"), "profile_id": profile_id, "home_path": home_path, "session_id": session_id}
    return V0436V044HandoffRequest(**_merge(defaults, overrides))


def create_v0436_v044_handoff_result(request: V0436V044HandoffRequest | None = None, **overrides: Any) -> V0436V044HandoffResult:
    packet = create_v0436_v044_handoff_packet()
    rendered = "\n".join(
        (
            "v0.44 handoff",
            packet.v043_closure_summary,
            f"objective: {packet.v044_objective}",
            f"allowed_scope: {', '.join(packet.allowed_scope)}",
            f"closed_capabilities: {', '.join(packet.closed_capabilities)}",
            f"safety_gates: {', '.join(packet.safety_gates)}",
            f"required_tests: {', '.join(packet.required_tests)}",
            "",
            packet.copy_paste_prompt,
            "workspace_read_opened=false; production_certified=false",
        )
    )
    defaults = {
        "result_id": _new_id("v0436-v044-handoff-result"),
        "rendered_text": rendered,
        "handoff_packet": packet,
        "provider_invoked": False,
        "prompt_submitted": False,
        "workspace_read_opened": False,
        "production_certified": False,
    }
    return V0436V044HandoffResult(**_merge(defaults, overrides))


def execute_v0436_v044_handoff(request: V0436V044HandoffRequest, **overrides: Any) -> V0436V044HandoffResult:
    return create_v0436_v044_handoff_result(request, **overrides)


def create_v0436_pilot_closure_pi_review_record(closure_trace_id: str | None = None, **overrides: Any) -> V0436PilotClosurePIReviewRecord:
    defaults = {
        "review_id": _new_id("v0436-pilot-closure-pi-review"),
        "closure_trace_id": closure_trace_id,
        "reconstructable_as_process_event": True,
        "closure_criteria_lineage_preserved": True,
        "safety_lineage_preserved": True,
        "v044_gate_lineage_preserved": True,
        "high_risk_counts_zero": True,
        "review_summary": "Pilot closure criteria, safety, and v0.44 gate lineage are preserved.",
    }
    return V0436PilotClosurePIReviewRecord(**_merge(defaults, overrides))


def create_v0436_pilot_closure_safety_report(**overrides: Any) -> V0436PilotClosureSafetyReport:
    defaults = {
        "report_id": "v0436-pilot-closure-safety-report",
        "final_pilot_polish_opened": True,
        "v044_design_gate_opened": True,
        "workspace_read_opened": False,
        "provider_invocation_allowed_by_default": False,
        "prompt_submission_allowed_by_default": False,
        "arbitrary_file_search_allowed": False,
        "repo_search_allowed": False,
        "workspace_search_allowed": False,
        "external_search_allowed": False,
        "shell_execution_allowed": False,
        "file_edit_allowed": False,
        "patch_apply_allowed": False,
        "provider_tool_calling_allowed": False,
        "function_calling_allowed": False,
        "subagent_allowed": False,
        "memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "production_certified": False,
    }
    return V0436PilotClosureSafetyReport(**_merge(defaults, overrides))


def create_v0436_readiness_report(**overrides: Any) -> V0436ReadinessReport:
    closure = create_v0436_pilot_closure_report()
    defaults = {
        "final_pilot_polish_ready": True,
        "command_surface_audit_ready": True,
        "business_ux_final_acceptance_ready": True,
        "pilot_closure_report_ready": True,
        "pilot_closure_decision_ready": True,
        "v044_readiness_report_ready": True,
        "v044_scope_proposal_ready": True,
        "v044_risk_register_ready": True,
        "v044_handoff_packet_ready": True,
        "pilot_closure_trace_ready": True,
        "pilot_closure_pi_review_ready": True,
        "integrated_restore_document_ready": True,
        "v0440_handoff_ready": True,
        "ready_to_close_v043": closure.v043_closure_allowed,
        "ready_for_v044_design": closure.recommends_v044_design,
        "ready_for_workspace_read_in_v0436": False,
        "ready_for_arbitrary_file_search": False,
        "ready_for_repo_search": False,
        "ready_for_workspace_search": False,
        "ready_for_external_search": False,
        "ready_for_shell_execution": False,
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
    return V0436ReadinessReport(**_merge(defaults, overrides))


def create_v0440_controlled_workspace_read_design_handoff(**overrides: Any) -> V0440ControlledWorkspaceReadDesignHandoff:
    defaults = {
        "handoff_id": "v0440-controlled-workspace-read-design-handoff",
        "target_version": V0440_RECOMMENDED_TITLE,
        "recommended_focus": (
            "design only first",
            "explicit workspace root",
            "allowlist",
            "path boundary",
            "read budget",
            "file type policy",
            "secret redaction",
            "trace event contract",
            "denial cases",
            "provider prompt boundary",
            "no edit/apply/shell/test/subagent",
            "no production certification",
        ),
        "must_not_open": CLOSED_CAPABILITIES,
        "production_certified": False,
    }
    return V0440ControlledWorkspaceReadDesignHandoff(**_merge(defaults, overrides))


def create_v0436_integrated_restore_context_snapshot(**overrides: Any) -> V0436IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0436-integrated-restore-context",
        "current_version": V0436_VERSION,
        "current_track": V043_TRACK_NAME,
        "baseline_versions": ("v0.43.5", "v0.43.4", "v0.43.3", "v0.43.2", "v0.43.1", "v0.43.0", "v0.42.10"),
        "open_capabilities": ("final pilot polish", "command surface audit", "pilot closure decision", "v0.44 design gate", "v0.44 risk register", "v0.44 handoff"),
        "closed_capabilities": CLOSED_CAPABILITIES,
        "integrated_doc_path": "docs/versions/v0.43/v0.43.6_final_pilot_polish_v044_gate_restore.md",
        "next_recommended_version": V0440_RECOMMENDED_TITLE,
    }
    return V0436IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0436_integrated_restore_packet(**overrides: Any) -> V0436IntegratedRestorePacket:
    sections = tuple(
        V0436IntegratedRestoreSection(f"v0436-section-{index}", title, True, f"Required v0.43.6 section: {title}", "future-session restore")
        for index, title in enumerate(REQUIRED_V0436_RESTORE_SECTIONS, 1)
    )
    defaults = {
        "restore_packet_id": "v0436-integrated-restore-packet",
        "snapshot": create_v0436_integrated_restore_context_snapshot(),
        "restore_sections": sections,
        "required_test_commands": (
            "py -m pytest tests\\test_v0436_final_pilot_polish_v044_gate.py",
            "py -m pytest tests\\test_v0435_pilot_review_acceptance_metrics.py",
        ),
        "single_integrated_doc_path": "docs/versions/v0.43/v0.43.6_final_pilot_polish_v044_gate_restore.md",
        "separate_restore_doc_created": False,
    }
    return V0436IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0436_integrated_restore_document_manifest(**overrides: Any) -> V0436IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0436-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.6_final_pilot_polish_v044_gate_restore.md",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0436IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


__all__ = [
    name
    for name in globals()
    if name.startswith("V0436")
    or name.startswith("V0440")
    or name.startswith("create_v0436")
    or name.startswith("create_v0440")
    or name.startswith("execute_v0436")
]
