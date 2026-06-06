from __future__ import annotations

import inspect

import pytest

from chanta_core.internal_triad import (
    CapabilityClassification,
    DigestiblePatternSignal,
    DigestionBlocker,
    DigestionBlockerKind,
    DigestionEvidencePosture,
    DigestionFeasibilityPosture,
    DigestionFinding,
    DigestionFocusKind,
    DigestionRoute,
    DigestionRouteDecision,
    DigestionSignalKind,
    DigestionSkillFoundationReport,
    DigestionSkillInput,
    DigestionSkillNoOpDecision,
    DigestionSkillOutput,
    DigestionSkillRunPreview,
    DigestionSkillSourceKind,
    DigestionSourceRef,
    V0313ReadinessReport,
    build_capability_map_entry,
    build_digestible_pattern_signal,
    build_digestion_blocker,
    build_digestion_finding,
    build_digestion_no_op_decision,
    build_digestion_route_decision,
    build_digestion_run_preview,
    build_digestion_skill_foundation_report,
    build_digestion_skill_input,
    build_digestion_skill_output,
    build_digestion_source_ref,
    build_internal_capability_map,
    build_v0313_readiness_report,
    classify_digestion_focus_from_capability_entry,
    digestion_focus_kind_creates_internal_artifact,
    digestion_foundation_is_not_runtime_ready,
    digestion_input_preserves_no_execution,
    digestion_output_is_not_dominion,
    digestion_output_is_not_internalization,
    digestion_output_preserves_no_execution,
    digestion_run_preview_preserves_no_execution,
    digestion_source_kind_fetches,
    infer_digestion_route_from_capability_classification,
    normalize_digestion_blocker_kind,
    normalize_digestion_evidence_posture,
    normalize_digestion_feasibility_posture,
    normalize_digestion_focus_kind,
    normalize_digestion_route,
    normalize_digestion_signal_kind,
    normalize_digestion_source_kind,
)
from chanta_core.internal_triad import digestion


REQUIRED_V0313_GATE_ITEMS = {
    "external_scan",
    "source_ref_fetch",
    "internal_tool_execution",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "registry_mutation",
    "memory_mutation",
    "rollback",
    "retry",
    "active_internalization",
    "internal_candidate_creation",
    "internalization_plan_creation",
}


def test_digestion_taxonomies_are_complete_and_conservative() -> None:
    assert {kind.value for kind in DigestionSkillSourceKind} == {
        "internal_observation_report",
        "internal_capability_map",
        "observation_report_bundle",
        "capability_map_entry",
        "observation_gap_register",
        "observation_risk_map",
        "observation_evidence_table",
        "manual_digestive_review",
        "v0312_readiness_report",
        "unknown",
    }
    assert normalize_digestion_source_kind("unknown") is DigestionSkillSourceKind.UNKNOWN
    assert digestion_source_kind_fetches(DigestionSkillSourceKind.INTERNAL_CAPABILITY_MAP) is False

    assert {kind.value for kind in DigestionFocusKind} == {
        "tool_contract_pattern",
        "skill_manifest_pattern",
        "mission_manifest_pattern",
        "policy_rule_pattern",
        "memory_schema_pattern",
        "prompt_pattern",
        "profile_pattern",
        "trace_event_pattern",
        "result_envelope_pattern",
        "approval_boundary_pattern",
        "ocel_trace_pattern",
        "gateway_manifest_pattern",
        "provider_adapter_pattern",
        "delegation_packet_pattern",
        "unsafe_runtime_surface",
        "unknown",
    }
    assert normalize_digestion_focus_kind("provider_adapter_pattern") is DigestionFocusKind.PROVIDER_ADAPTER_PATTERN
    assert digestion_focus_kind_creates_internal_artifact(DigestionFocusKind.TOOL_CONTRACT_PATTERN) is False

    assert {kind.value for kind in DigestionSignalKind} == {
        "pattern_detected",
        "schema_extractable",
        "internalization_possible",
        "requires_internal_design",
        "requires_review",
        "insufficient_evidence",
        "unsafe_to_digest",
        "incompatible_with_ocel_spine",
        "dominion_required",
        "future_track_required",
        "blocked",
        "no_op_recommended",
        "unknown",
    }
    assert normalize_digestion_signal_kind("internalization_possible") is DigestionSignalKind.INTERNALIZATION_POSSIBLE

    assert {route.value for route in DigestionRoute} == {
        "internalization_candidate_signal",
        "defer",
        "reject",
        "dominion_required_signal",
        "blocked",
        "future_track",
        "no_op",
        "unknown",
    }
    assert normalize_digestion_route("dominion_required_signal") is DigestionRoute.DOMINION_REQUIRED_SIGNAL


def test_digestion_posture_and_blocker_taxonomies() -> None:
    assert {posture.value for posture in DigestionFeasibilityPosture} == {
        "unknown",
        "low",
        "medium",
        "high",
        "blocked",
        "future_track",
    }
    assert normalize_digestion_feasibility_posture("high") is DigestionFeasibilityPosture.HIGH

    assert {posture.value for posture in DigestionEvidencePosture} == {
        "unknown",
        "none",
        "weak",
        "partial",
        "sufficient_for_route_signal",
        "sufficient_for_v0314_review",
        "conflicting",
        "blocked",
    }
    assert normalize_digestion_evidence_posture("sufficient_for_route_signal") is DigestionEvidencePosture.SUFFICIENT_FOR_ROUTE_SIGNAL

    assert {kind.value for kind in DigestionBlockerKind} == {
        "insufficient_evidence",
        "missing_capability_map_entry",
        "missing_observation_report",
        "missing_evidence_table",
        "unsafe_network_surface",
        "unsafe_credential_surface",
        "unsafe_command_surface",
        "unsafe_provider_surface",
        "unsafe_browser_surface",
        "unsafe_rpa_surface",
        "unsafe_gateway_surface",
        "unsafe_delegation_surface",
        "raw_output_persistence_risk",
        "memory_contamination_risk",
        "incompatible_with_ocel_spine",
        "requires_dominion",
        "requires_future_gate",
        "unknown",
    }
    assert normalize_digestion_blocker_kind("requires_dominion") is DigestionBlockerKind.REQUIRES_DOMINION


def _sample_capability_map():
    digestion_entry = build_capability_map_entry(
        "capability_entry:digestion",
        "tool contract pattern",
        CapabilityClassification.DIGESTION_SIGNAL,
        target_id="target:1",
        capability_kind="tool contract",
        evidence_ref_ids=["evidence_ref:1"],
    )
    dominion_entry = build_capability_map_entry(
        "capability_entry:dominion",
        "provider adapter runtime surface",
        CapabilityClassification.DOMINION_SIGNAL,
        target_id="target:1",
        capability_kind="provider adapter",
        boundary_surfaces=["provider runtime"],
        evidence_ref_ids=["evidence_ref:1"],
    )
    blocked_entry = build_capability_map_entry(
        "capability_entry:blocked",
        "network credential command surface",
        CapabilityClassification.BLOCKED,
        target_id="target:1",
        capability_kind="unsafe runtime",
        boundary_surfaces=["network", "credential", "command"],
        blocked_reasons=["unsafe runtime surface"],
        evidence_ref_ids=["evidence_ref:1"],
    )
    capability_map = build_internal_capability_map(
        "internal_capability_map:v0.31.2",
        "internal_observation_report:v0.31.2",
        entries=[digestion_entry, dominion_entry, blocked_entry],
        digestion_signal_capability_ids=[digestion_entry.entry_id],
        dominion_signal_capability_ids=[dominion_entry.entry_id],
        blocked_capability_ids=[blocked_entry.entry_id],
        blocked_reasons=["blocked entry remains diagnostic"],
        evidence_ref_ids=["evidence_ref:1"],
    )
    return capability_map, digestion_entry, dominion_entry, blocked_entry


def test_source_ref_and_input_are_not_fetch_or_execution_request() -> None:
    capability_map, digestion_entry, _, _ = _sample_capability_map()
    source_ref = build_digestion_source_ref(
        "digestion_source_ref:1",
        DigestionSkillSourceKind.CAPABILITY_MAP_ENTRY,
        digestion_entry.entry_id,
        target_id=digestion_entry.target_id,
        capability_entry_id=digestion_entry.entry_id,
        evidence_ref_ids=["evidence_ref:1"],
    )
    digestion_input = build_digestion_skill_input(
        "digestion_input:v0.31.3",
        "Route v0.31.2 capability map entries for later design review.",
        "v0.31.3",
        source_refs=[source_ref],
        requested_focus=[DigestionFocusKind.TOOL_CONTRACT_PATTERN],
        capability_map=capability_map,
        evidence_refs=["evidence_ref:1"],
    )

    assert isinstance(source_ref, DigestionSourceRef)
    assert source_ref.fetches_source is False
    assert isinstance(digestion_input, DigestionSkillInput)
    assert digestion_input.is_execution_request is False
    assert "internal_capability_map:v0.31.2" in digestion_input.capability_map_refs
    assert digestion_input_preserves_no_execution(digestion_input) is True

    with pytest.raises(ValueError, match="source_ref_id"):
        build_digestion_source_ref("", DigestionSkillSourceKind.UNKNOWN, "source")
    with pytest.raises(ValueError, match="source_id"):
        build_digestion_source_ref("source_ref:bad", DigestionSkillSourceKind.UNKNOWN, "")
    with pytest.raises(ValueError, match="source fetch"):
        build_digestion_source_ref("source_ref:bad", DigestionSkillSourceKind.UNKNOWN, "source", metadata={"source_ref_fetch": True})
    with pytest.raises(ValueError, match="digestion_input_id"):
        build_digestion_skill_input("", "summary", "v0.31.3")
    with pytest.raises(ValueError, match="task_summary"):
        build_digestion_skill_input("input:bad", "", "v0.31.3")
    with pytest.raises(ValueError, match="source_version"):
        build_digestion_skill_input("input:bad", "summary", "")
    with pytest.raises(ValueError, match="execution"):
        build_digestion_skill_input("input:bad", "summary", "v0.31.3", metadata={"execution_request": True})


def test_capability_map_classification_routes_to_signals_only() -> None:
    _, digestion_entry, dominion_entry, blocked_entry = _sample_capability_map()

    assert classify_digestion_focus_from_capability_entry(digestion_entry) is DigestionFocusKind.TOOL_CONTRACT_PATTERN
    assert classify_digestion_focus_from_capability_entry(dominion_entry) is DigestionFocusKind.UNSAFE_RUNTIME_SURFACE
    assert infer_digestion_route_from_capability_classification(digestion_entry) is DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL
    assert infer_digestion_route_from_capability_classification(dominion_entry) is DigestionRoute.DOMINION_REQUIRED_SIGNAL
    assert infer_digestion_route_from_capability_classification(blocked_entry) is DigestionRoute.BLOCKED


def test_digestible_pattern_signal_is_not_internal_candidate_or_dominion_target() -> None:
    signal = build_digestible_pattern_signal(
        "digestion_signal:1",
        DigestionFocusKind.TOOL_CONTRACT_PATTERN,
        DigestionSignalKind.INTERNALIZATION_POSSIBLE,
        DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL,
        "Tool contract pattern may be reviewed later",
        "The pattern can be routed to v0.31.4 review without creating a candidate.",
        source_ref_id="source_ref:1",
        capability_entry_id="capability_entry:digestion",
        evidence_ref_ids=["evidence_ref:1"],
        feasibility_posture=DigestionFeasibilityPosture.HIGH,
        evidence_posture=DigestionEvidencePosture.SUFFICIENT_FOR_ROUTE_SIGNAL,
    )
    dominion_signal = build_digestible_pattern_signal(
        "digestion_signal:dominion",
        DigestionFocusKind.UNSAFE_RUNTIME_SURFACE,
        DigestionSignalKind.DOMINION_REQUIRED,
        DigestionRoute.DOMINION_REQUIRED_SIGNAL,
        "Dominion review signal",
        "The route signals later dominion review only.",
        evidence_ref_ids=["evidence_ref:1"],
    )

    assert isinstance(signal, DigestiblePatternSignal)
    assert signal.creates_internal_skill_candidate is False
    assert signal.creates_internalization_plan is False
    assert signal.is_internal_artifact is False
    assert dominion_signal.creates_dominion_target is False

    with pytest.raises(ValueError, match="signal_id"):
        build_digestible_pattern_signal("", DigestionFocusKind.UNKNOWN, DigestionSignalKind.UNKNOWN, DigestionRoute.UNKNOWN, "title", "summary")
    with pytest.raises(ValueError, match="title"):
        build_digestible_pattern_signal("signal:bad", DigestionFocusKind.UNKNOWN, DigestionSignalKind.UNKNOWN, DigestionRoute.UNKNOWN, "", "summary")
    with pytest.raises(ValueError, match="summary"):
        build_digestible_pattern_signal("signal:bad", DigestionFocusKind.UNKNOWN, DigestionSignalKind.UNKNOWN, DigestionRoute.UNKNOWN, "title", "")
    with pytest.raises(ValueError, match="blocked route"):
        build_digestible_pattern_signal("signal:bad", DigestionFocusKind.UNKNOWN, DigestionSignalKind.BLOCKED, DigestionRoute.BLOCKED, "title", "summary")
    with pytest.raises(ValueError, match="internal artifact"):
        build_digestible_pattern_signal(
            "signal:bad",
            DigestionFocusKind.TOOL_CONTRACT_PATTERN,
            DigestionSignalKind.INTERNALIZATION_POSSIBLE,
            DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL,
            "title",
            "summary",
            metadata={"internal_skill_candidate_creation": True},
        )


def test_finding_blocker_and_route_decision_are_not_implementation() -> None:
    finding = build_digestion_finding(
        "digestion_finding:1",
        "digestion_input:v0.31.3",
        DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL,
        "Route signal is available for v0.31.4 design review.",
        signal_ids=["digestion_signal:1"],
        feasibility_posture=DigestionFeasibilityPosture.HIGH,
        evidence_posture=DigestionEvidencePosture.SUFFICIENT_FOR_ROUTE_SIGNAL,
        evidence_ref_ids=["evidence_ref:1"],
    )
    blocker = build_digestion_blocker(
        "digestion_blocker:1",
        DigestionBlockerKind.UNSAFE_PROVIDER_SURFACE,
        "Provider runtime surface requires dominion review.",
        blocks_v0314=True,
        routes_to_dominion=True,
        evidence_ref_ids=["evidence_ref:1"],
    )
    route_decision = build_digestion_route_decision(
        "digestion_route_decision:1",
        "digestion_input:v0.31.3",
        DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL,
        "No blocking blockers are attached to this route signal.",
        signal_ids=["digestion_signal:1"],
        evidence_ref_ids=["evidence_ref:1"],
        ready_for_v0314_internalization_plan=True,
    )
    dominion_decision = build_digestion_route_decision(
        "digestion_route_decision:dominion",
        "digestion_input:v0.31.3",
        DigestionRoute.DOMINION_REQUIRED_SIGNAL,
        "Dominion review is required later.",
        signal_ids=["digestion_signal:dominion"],
        ready_for_v0315_dominion_skill_foundation=True,
    )

    assert isinstance(finding, DigestionFinding)
    assert finding.creates_v0314_artifact is False
    assert finding.creates_dominion_target is False
    assert isinstance(blocker, DigestionBlocker)
    assert blocker.executes_remediation is False
    assert isinstance(route_decision, DigestionRouteDecision)
    assert route_decision.ready_for_execution is False
    assert route_decision.ready_for_skill_activation is False
    assert route_decision.ready_for_internalization is False
    assert route_decision.is_implementation is False
    assert dominion_decision.ready_for_v0315_dominion_skill_foundation is True

    with pytest.raises(ValueError, match="finding_id"):
        build_digestion_finding("", "input", DigestionRoute.UNKNOWN, "summary")
    with pytest.raises(ValueError, match="digestion_input_id"):
        build_digestion_finding("finding:bad", "", DigestionRoute.UNKNOWN, "summary")
    with pytest.raises(ValueError, match="summary"):
        build_digestion_finding("finding:bad", "input", DigestionRoute.UNKNOWN, "")
    with pytest.raises(ValueError, match="later-stage artifacts"):
        build_digestion_finding("finding:bad", "input", DigestionRoute.UNKNOWN, "summary", metadata={"internalization_plan_creation": True})
    with pytest.raises(ValueError, match="blocker_id"):
        build_digestion_blocker("", DigestionBlockerKind.UNKNOWN, "description")
    with pytest.raises(ValueError, match="description"):
        build_digestion_blocker("blocker:bad", DigestionBlockerKind.UNKNOWN, "")
    with pytest.raises(TypeError, match="blocks_v0314"):
        DigestionBlocker("blocker:bad", DigestionBlockerKind.UNKNOWN, None, None, "description", "yes", False, False)
    with pytest.raises(ValueError, match="remediation"):
        build_digestion_blocker("blocker:bad", DigestionBlockerKind.UNKNOWN, "description", metadata={"automatic_remediation": True})
    with pytest.raises(ValueError, match="ready_for_execution"):
        DigestionRouteDecision("decision:bad", "input", DigestionRoute.UNKNOWN, [], [], "reason", ready_for_execution=True)
    with pytest.raises(ValueError, match="v0.31.4 readiness"):
        build_digestion_route_decision(
            "decision:bad",
            "input",
            DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL,
            "reason",
            blocker_ids=["blocker:1"],
            ready_for_v0314_internalization_plan=True,
        )
    with pytest.raises(ValueError, match="v0.31.5 readiness"):
        build_digestion_route_decision(
            "decision:bad",
            "input",
            DigestionRoute.DEFER,
            "reason",
            ready_for_v0315_dominion_skill_foundation=True,
        )


def test_digestion_skill_output_preserves_no_execution_internalization_or_registry_mutation() -> None:
    signal = build_digestible_pattern_signal(
        "digestion_signal:1",
        DigestionFocusKind.TOOL_CONTRACT_PATTERN,
        DigestionSignalKind.INTERNALIZATION_POSSIBLE,
        DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL,
        "Signal",
        "Route signal only.",
    )
    finding = build_digestion_finding("finding:1", "digestion_input:v0.31.3", DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL, "Finding.")
    decision = build_digestion_route_decision(
        "decision:1",
        "digestion_input:v0.31.3",
        DigestionRoute.INTERNALIZATION_CANDIDATE_SIGNAL,
        "Route to next design review only.",
        signal_ids=[signal.signal_id],
        ready_for_v0314_internalization_plan=True,
    )
    output = build_digestion_skill_output(
        "digestion_output:v0.31.3",
        "digestion_input:v0.31.3",
        "route_ready",
        pattern_signals=[signal],
        findings=[finding],
        route_decisions=[decision],
        internalization_signal_ids=[signal.signal_id],
        ready_for_v0314_internalization_plan=True,
    )

    assert isinstance(output, DigestionSkillOutput)
    assert output.ready_for_execution is False
    assert output.ready_for_skill_activation is False
    assert output.ready_for_internalization is False
    assert output.ready_for_registry_mutation is False
    assert output.creates_internal_skill_candidate is False
    assert output.creates_internalization_plan is False
    assert output.creates_dominion_target is False
    assert output.active_artifact_registration is False
    assert digestion_output_preserves_no_execution(output) is True
    assert digestion_output_is_not_internalization(output) is True
    assert digestion_output_is_not_dominion(output) is True

    with pytest.raises(ValueError, match="digestion_output_id"):
        build_digestion_skill_output("", "input", "status")
    with pytest.raises(ValueError, match="digestion_input_id"):
        build_digestion_skill_output("output:bad", "", "status")
    with pytest.raises(ValueError, match="status"):
        build_digestion_skill_output("output:bad", "input", "")
    with pytest.raises(ValueError, match="ready_for_execution"):
        DigestionSkillOutput("output:bad", "input", None, "status", [], [], [], [], [], [], [], [], [], [], [], False, False, ready_for_execution=True)
    with pytest.raises(ValueError, match="ready_for_internalization"):
        DigestionSkillOutput("output:bad", "input", None, "status", [], [], [], [], [], [], [], [], [], [], [], False, False, ready_for_internalization=True)
    with pytest.raises(ValueError, match="ready_for_registry_mutation"):
        DigestionSkillOutput("output:bad", "input", None, "status", [], [], [], [], [], [], [], [], [], [], [], False, False, ready_for_registry_mutation=True)
    with pytest.raises(ValueError, match="registry"):
        build_digestion_skill_output("output:bad", "input", "status", metadata={"registry_mutation": True})


def test_no_op_run_preview_foundation_and_readiness_reports_are_non_runtime() -> None:
    no_op = build_digestion_no_op_decision(
        "digestion_noop:1",
        "digestion_input:v0.31.3",
        "No digestible route signal is available.",
        safe_alternatives=["defer"],
    )
    preview = build_digestion_run_preview("digestion_run_preview:1", "digestion_input:v0.31.3")
    foundation = build_digestion_skill_foundation_report()
    readiness = build_v0313_readiness_report(foundation)

    assert isinstance(no_op, DigestionSkillNoOpDecision)
    assert no_op.is_failure is False
    assert no_op.executes_anything is False
    assert isinstance(preview, DigestionSkillRunPreview)
    assert preview.no_execution_guarantee is True
    assert preview.no_external_scan_guarantee is True
    assert preview.no_tool_execution_guarantee is True
    assert preview.no_internalization_guarantee is True
    assert preview.no_candidate_creation_guarantee is True
    assert preview.no_registry_mutation_guarantee is True
    assert preview.no_memory_mutation_guarantee is True
    assert preview.executes_run is False
    assert digestion_run_preview_preserves_no_execution(preview) is True

    assert isinstance(foundation, DigestionSkillFoundationReport)
    assert "v0.31.3" in foundation.version
    assert foundation.ready_for_execution is False
    assert foundation.ready_for_skill_activation is False
    assert foundation.ready_for_internalization is False
    assert foundation.runtime_enablement is False
    assert digestion_foundation_is_not_runtime_ready(foundation) is True

    assert isinstance(readiness, V0313ReadinessReport)
    assert "v0.31.3" in readiness.version
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_skill_activation is False
    assert readiness.ready_for_internalization is False
    assert readiness.ready_for_registry_mutation is False
    assert readiness.runtime_enablement is False
    assert REQUIRED_V0313_GATE_ITEMS.issubset(set(readiness.prohibited_until_later_gate))
    assert digestion_foundation_is_not_runtime_ready(readiness) is True

    with pytest.raises(ValueError, match="no_op_id"):
        build_digestion_no_op_decision("", "input", "reason")
    with pytest.raises(ValueError, match="reason"):
        build_digestion_no_op_decision("noop:bad", "input", "")
    with pytest.raises(ValueError, match="run_preview_id"):
        build_digestion_run_preview("")
    with pytest.raises(ValueError, match="no_execution_guarantee"):
        DigestionSkillRunPreview("preview:bad", None, [], [], [], no_execution_guarantee=False)
    with pytest.raises(ValueError, match="v0.31.3"):
        DigestionSkillFoundationReport("foundation:bad", "v0.31.2", None, [], [], [], [], [], True, True, summary="summary")
    with pytest.raises(ValueError, match="ready_for_internalization"):
        V0313ReadinessReport("readiness:bad", "v0.31.3", "foundation:1", "summary", True, True, ready_for_internalization=True)


def test_helpers_are_pure_conservative_digestion_artifact_builders() -> None:
    helpers = [
        build_digestion_source_ref,
        build_digestion_skill_input,
        classify_digestion_focus_from_capability_entry,
        infer_digestion_route_from_capability_classification,
        build_digestible_pattern_signal,
        build_digestion_finding,
        build_digestion_blocker,
        build_digestion_route_decision,
        build_digestion_skill_output,
        build_digestion_no_op_decision,
        build_digestion_run_preview,
        build_digestion_skill_foundation_report,
        build_v0313_readiness_report,
        digestion_input_preserves_no_execution,
        digestion_output_preserves_no_execution,
        digestion_output_is_not_internalization,
        digestion_output_is_not_dominion,
        digestion_run_preview_preserves_no_execution,
        digestion_foundation_is_not_runtime_ready,
    ]

    for helper in helpers:
        source = inspect.getsource(helper)
        assert "ready_for_execution=True" not in source
        assert "ready_for_skill_activation=True" not in source
        assert "ready_for_internalization=True" not in source
        assert "ready_for_registry_mutation=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source

    implementation_source = inspect.getsource(digestion)
    assert "subprocess" not in implementation_source
    assert "os.system" not in implementation_source
    assert "shell=True" not in implementation_source
    assert "requests." not in implementation_source
    assert "httpx." not in implementation_source
    assert "urllib." not in implementation_source
    assert "aiohttp." not in implementation_source
    assert "socket." not in implementation_source
