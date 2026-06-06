from __future__ import annotations

import inspect

import pytest

from chanta_core.internal_triad import (
    DominionBlocker,
    DominionBlockerKind,
    DominionBoundaryPosture,
    DominionControlBoundarySignal,
    DominionFeasibilityPosture,
    DominionFocusKind,
    DominionGovernanceFinding,
    DominionRiskPosture,
    DominionRoute,
    DominionRouteDecision,
    DominionSignalKind,
    DominionSkillFoundationReport,
    DominionSkillInput,
    DominionSkillNoOpDecision,
    DominionSkillOutput,
    DominionSkillRunPreview,
    DominionSkillSourceKind,
    DominionSkillSourceRef,
    V0315ReadinessReport,
    build_dominion_blocker,
    build_dominion_control_boundary_signal,
    build_dominion_governance_finding,
    build_dominion_no_op_decision,
    build_dominion_route_decision,
    build_dominion_run_preview,
    build_dominion_skill_foundation_report,
    build_dominion_skill_input,
    build_dominion_skill_output,
    build_dominion_source_ref,
    build_internal_candidate_set,
    build_internalization_plan,
    build_v0315_readiness_report,
    classify_dominion_focus_from_source,
    dominion_focus_kind_creates_target,
    dominion_foundation_is_not_runtime_ready,
    dominion_input_preserves_no_execution,
    dominion_output_grants_no_authority,
    dominion_output_is_not_target_or_decision,
    dominion_output_preserves_no_execution,
    dominion_run_preview_preserves_no_execution,
    dominion_source_kind_fetches,
    infer_dominion_route_from_source_or_signal,
    normalize_dominion_blocker_kind,
    normalize_dominion_boundary_posture,
    normalize_dominion_feasibility_posture,
    normalize_dominion_focus_kind,
    normalize_dominion_risk_posture,
    normalize_dominion_route,
    normalize_dominion_signal_kind,
    normalize_dominion_source_kind,
)
from chanta_core.internal_triad import dominion


REQUIRED_PROHIBITIONS = {
    "external_control",
    "authority_grant",
    "dominion_target_creation",
    "dominion_decision_creation",
    "external_execution",
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
}


def test_dominion_taxonomies_are_complete_and_conservative() -> None:
    assert {kind.value for kind in DominionSkillSourceKind} == {
        "internal_candidate_set",
        "internalization_plan",
        "internalization_no_op_decision",
        "v0314_readiness_report",
        "digestion_skill_output",
        "digestion_route_decision",
        "digestible_pattern_signal",
        "observation_risk_map",
        "observation_gap_register",
        "capability_map_entry",
        "external_dominion_authority_decision",
        "external_certification_report",
        "external_preview_gate_report",
        "manual_dominion_review",
        "unknown",
    }
    assert normalize_dominion_source_kind("unknown") is DominionSkillSourceKind.UNKNOWN
    assert dominion_source_kind_fetches(DominionSkillSourceKind.INTERNAL_CANDIDATE_SET) is False

    assert {kind.value for kind in DominionFocusKind} == {
        "external_runtime_boundary",
        "provider_boundary",
        "network_boundary",
        "credential_boundary",
        "command_boundary",
        "browser_boundary",
        "rpa_boundary",
        "gateway_boundary",
        "delegation_boundary",
        "memory_boundary",
        "raw_output_boundary",
        "registry_boundary",
        "policy_boundary",
        "approval_boundary",
        "audit_boundary",
        "rollback_no_op_boundary",
        "future_gate_boundary",
        "ocel_trace_boundary",
        "unknown",
    }
    assert normalize_dominion_focus_kind("network_boundary") is DominionFocusKind.NETWORK_BOUNDARY
    assert dominion_focus_kind_creates_target(DominionFocusKind.PROVIDER_BOUNDARY) is False

    assert {kind.value for kind in DominionSignalKind} == {
        "dominion_required",
        "external_control_risk_detected",
        "runtime_boundary_needed",
        "authority_boundary_needed",
        "approval_boundary_needed",
        "audit_boundary_needed",
        "result_boundary_needed",
        "rollback_no_op_needed",
        "future_gate_needed",
        "no_op_recommended",
        "blocked_by_policy",
        "insufficient_evidence",
        "unsafe_to_control",
        "incompatible_with_ocel_spine",
        "unknown",
    }
    assert normalize_dominion_signal_kind("dominion_required") is DominionSignalKind.DOMINION_REQUIRED

    assert {route.value for route in DominionRoute} == {
        "dominion_target_signal",
        "dominion_decision_signal",
        "future_gate_signal",
        "review_required",
        "defer",
        "reject",
        "blocked",
        "no_op",
        "unknown",
    }
    assert normalize_dominion_route("dominion_target_signal") is DominionRoute.DOMINION_TARGET_SIGNAL

    assert {posture.value for posture in DominionFeasibilityPosture} == {
        "unknown",
        "low",
        "medium",
        "high",
        "blocked",
        "future_track",
    }
    assert normalize_dominion_feasibility_posture("high") is DominionFeasibilityPosture.HIGH

    assert {posture.value for posture in DominionBoundaryPosture} == {
        "unknown",
        "descriptive_only",
        "observation_only",
        "plan_only",
        "simulate_only",
        "blocked",
        "future_track",
    }
    assert normalize_dominion_boundary_posture("simulate_only") is DominionBoundaryPosture.SIMULATE_ONLY

    assert {posture.value for posture in DominionRiskPosture} == {
        "unknown",
        "low",
        "medium",
        "high",
        "critical",
        "blocked",
        "future_track",
    }
    assert normalize_dominion_risk_posture("critical") is DominionRiskPosture.CRITICAL

    assert {kind.value for kind in DominionBlockerKind} == {
        "insufficient_evidence",
        "missing_internalization_context",
        "missing_boundary_classification",
        "missing_risk_map",
        "missing_approval_boundary",
        "missing_audit_boundary",
        "missing_result_boundary",
        "missing_rollback_no_op",
        "unsafe_network_surface",
        "unsafe_credential_surface",
        "unsafe_command_surface",
        "unsafe_provider_surface",
        "unsafe_browser_surface",
        "unsafe_rpa_surface",
        "unsafe_gateway_surface",
        "unsafe_delegation_surface",
        "memory_contamination_risk",
        "raw_output_persistence_risk",
        "registry_mutation_risk",
        "policy_activation_risk",
        "requires_future_gate",
        "incompatible_with_ocel_spine",
        "unknown",
    }
    assert normalize_dominion_blocker_kind("requires_future_gate") is DominionBlockerKind.REQUIRES_FUTURE_GATE


def _source_ref() -> DominionSkillSourceRef:
    return build_dominion_source_ref(
        "dominion_source_ref:1",
        DominionSkillSourceKind.INTERNAL_CANDIDATE_SET,
        "candidate_set:v0.31.4",
        candidate_id="candidate:1",
        internal_candidate_id="candidate:1",
        evidence_ref_ids=["evidence:1"],
    )


def test_source_ref_and_input_are_not_fetch_or_execution_request() -> None:
    source_ref = _source_ref()
    candidate_set = build_internal_candidate_set(
        "candidate_set:v0.31.4",
        dominion_required_source_refs=["digestion_signal:dominion"],
    )
    plan = build_internalization_plan(
        "internalization_plan:v0.31.4",
        candidate_set.candidate_set_id,
        "plan_ready",
        "Plan remains design only.",
        blocked_candidate_ids=["candidate:block"],
    )
    dominion_input = build_dominion_skill_input(
        "dominion_input:1",
        "Classify dominion-required internalization sources.",
        "v0.31.4",
        source_refs=[source_ref],
        candidate_set=candidate_set,
        internalization_plan=plan,
        requested_focus=[DominionFocusKind.NETWORK_BOUNDARY],
        evidence_refs=["evidence:1"],
    )

    assert source_ref.fetches_source is False
    assert isinstance(dominion_input, DominionSkillInput)
    assert dominion_input.is_execution_request is False
    assert REQUIRED_PROHIBITIONS.issubset(set(dominion_input.prohibited_runtime_actions))
    assert dominion_input_preserves_no_execution(dominion_input) is True
    assert classify_dominion_focus_from_source(build_dominion_source_ref("source:network", "manual_dominion_review", "network")) is DominionFocusKind.NETWORK_BOUNDARY

    with pytest.raises(ValueError, match="source_ref_id"):
        build_dominion_source_ref("", DominionSkillSourceKind.UNKNOWN, "source")
    with pytest.raises(ValueError, match="source_id"):
        build_dominion_source_ref("source:bad", DominionSkillSourceKind.UNKNOWN, "")
    with pytest.raises(ValueError, match="source fetch"):
        build_dominion_source_ref("source:bad", "unknown", "source", metadata={"source_ref_fetch": True})
    with pytest.raises(ValueError, match="dominion_input_id"):
        build_dominion_skill_input("", "summary", "v0.31.4")
    with pytest.raises(ValueError, match="execution"):
        build_dominion_skill_input("input:bad", "summary", "v0.31.4", metadata={"execution_request": True})


def test_boundary_signal_finding_blocker_and_route_decision_are_signal_only() -> None:
    signal = build_dominion_control_boundary_signal(
        "dominion_signal:1",
        DominionFocusKind.PROVIDER_BOUNDARY,
        DominionSignalKind.DOMINION_REQUIRED,
        DominionRoute.DOMINION_TARGET_SIGNAL,
        "Provider boundary signal",
        "Provider control should remain a future target signal.",
        source_ref_id="dominion_source_ref:1",
        risk_posture=DominionRiskPosture.HIGH,
        boundary_posture=DominionBoundaryPosture.PLAN_ONLY,
        feasibility_posture=DominionFeasibilityPosture.MEDIUM,
        evidence_ref_ids=["evidence:1"],
        blocker_ids=["blocker:1"],
    )
    finding = build_dominion_governance_finding(
        "dominion_finding:1",
        "dominion_input:1",
        DominionRoute.DOMINION_TARGET_SIGNAL,
        "Boundary finding remains governance-only.",
        signal_ids=[signal.signal_id],
        risk_posture=DominionRiskPosture.HIGH,
        boundary_posture=DominionBoundaryPosture.PLAN_ONLY,
        feasibility_posture=DominionFeasibilityPosture.MEDIUM,
    )
    blocker = build_dominion_blocker(
        "blocker:1",
        DominionBlockerKind.UNSAFE_PROVIDER_SURFACE,
        "Provider boundary requires later gate.",
        blocks_v0316=True,
        routes_to_future_gate=True,
    )
    decision = build_dominion_route_decision(
        "dominion_route_decision:1",
        "dominion_input:1",
        DominionRoute.DOMINION_TARGET_SIGNAL,
        "Route as future design signal only.",
        signal_ids=[signal.signal_id],
        ready_for_v0316_dominion_target_decision=True,
    )

    assert isinstance(signal, DominionControlBoundarySignal)
    assert signal.creates_dominion_target is False
    assert signal.creates_dominion_decision is False
    assert signal.grants_authority is False
    assert infer_dominion_route_from_source_or_signal(signal) is DominionRoute.DOMINION_TARGET_SIGNAL
    assert isinstance(finding, DominionGovernanceFinding)
    assert finding.creates_v0316_artifact is False
    assert finding.grants_authority is False
    assert isinstance(blocker, DominionBlocker)
    assert blocker.executes_remediation is False
    assert isinstance(decision, DominionRouteDecision)
    assert decision.ready_for_execution is False
    assert decision.ready_for_external_control is False
    assert decision.ready_for_authority_grant is False
    assert decision.ready_for_dominion_target_creation is False
    assert decision.ready_for_dominion_decision_creation is False
    assert decision.grants_authority is False
    assert decision.is_implementation is False

    with pytest.raises(ValueError, match="high, critical, or blocked risk"):
        build_dominion_control_boundary_signal(
            "dominion_signal:bad",
            DominionFocusKind.NETWORK_BOUNDARY,
            DominionSignalKind.EXTERNAL_CONTROL_RISK_DETECTED,
            DominionRoute.DOMINION_TARGET_SIGNAL,
            "Network boundary",
            "High risk requires conservative routing evidence.",
            risk_posture=DominionRiskPosture.CRITICAL,
        )
    with pytest.raises(ValueError, match="signal-only"):
        build_dominion_control_boundary_signal(
            "dominion_signal:bad",
            DominionFocusKind.NETWORK_BOUNDARY,
            DominionSignalKind.DOMINION_REQUIRED,
            DominionRoute.DOMINION_DECISION_SIGNAL,
            "Network boundary",
            "Signal only.",
            metadata={"dominion_decision_creation": True},
        )
    with pytest.raises(ValueError, match="later-stage"):
        build_dominion_governance_finding(
            "finding:bad",
            "dominion_input:1",
            DominionRoute.DOMINION_DECISION_SIGNAL,
            "Finding.",
            metadata={"v0316_artifact_creation": True},
        )
    with pytest.raises(ValueError, match="remediation"):
        build_dominion_blocker("blocker:bad", DominionBlockerKind.UNKNOWN, "description", metadata={"remediation_execution": True})
    with pytest.raises(ValueError, match="ready_for_external_control"):
        DominionRouteDecision(
            "decision:bad",
            "dominion_input:1",
            DominionRoute.DOMINION_TARGET_SIGNAL,
            [],
            [],
            "reason",
            ready_for_external_control=True,
        )
    with pytest.raises(ValueError, match="v0.31.6 readiness"):
        build_dominion_route_decision(
            "decision:bad",
            "dominion_input:1",
            DominionRoute.DOMINION_TARGET_SIGNAL,
            "reason",
            blocker_ids=["blocker:1"],
            ready_for_v0316_dominion_target_decision=True,
        )


def _output_parts():
    signal = build_dominion_control_boundary_signal(
        "dominion_signal:1",
        DominionFocusKind.APPROVAL_BOUNDARY,
        DominionSignalKind.AUTHORITY_BOUNDARY_NEEDED,
        DominionRoute.DOMINION_DECISION_SIGNAL,
        "Authority boundary signal",
        "Authority boundary remains a decision signal only.",
        risk_posture=DominionRiskPosture.MEDIUM,
    )
    finding = build_dominion_governance_finding(
        "dominion_finding:1",
        "dominion_input:1",
        DominionRoute.DOMINION_DECISION_SIGNAL,
        "Governance finding only.",
        signal_ids=[signal.signal_id],
        risk_posture=DominionRiskPosture.MEDIUM,
        boundary_posture=DominionBoundaryPosture.PLAN_ONLY,
        feasibility_posture=DominionFeasibilityPosture.HIGH,
    )
    decision = build_dominion_route_decision(
        "dominion_route_decision:1",
        "dominion_input:1",
        DominionRoute.DOMINION_DECISION_SIGNAL,
        "Decision signal for v0.31.6 modeling only.",
        signal_ids=[signal.signal_id],
        ready_for_v0316_dominion_target_decision=True,
    )
    return signal, finding, decision


def test_output_no_op_run_preview_foundation_and_readiness_are_non_runtime() -> None:
    signal, finding, decision = _output_parts()
    output = build_dominion_skill_output(
        "dominion_output:1",
        "dominion_input:1",
        "route_ready",
        boundary_signals=[signal],
        findings=[finding],
        route_decisions=[decision],
        dominion_decision_signal_ids=[signal.signal_id],
        ready_for_v0316_dominion_target_decision=True,
    )
    no_op = build_dominion_no_op_decision("dominion_noop:1", "dominion_input:1", "No external control should occur.")
    preview = build_dominion_run_preview("dominion_preview:1", "dominion_input:1")
    foundation = build_dominion_skill_foundation_report()
    readiness = build_v0315_readiness_report(foundation)

    assert isinstance(output, DominionSkillOutput)
    assert output.ready_for_execution is False
    assert output.ready_for_skill_activation is False
    assert output.ready_for_external_control is False
    assert output.ready_for_authority_grant is False
    assert output.ready_for_dominion_runtime is False
    assert output.creates_dominion_target is False
    assert output.creates_dominion_decision is False
    assert output.grants_authority is False
    assert output.active_artifact_registration is False
    assert dominion_output_preserves_no_execution(output) is True
    assert dominion_output_is_not_target_or_decision(output) is True
    assert dominion_output_grants_no_authority(output) is True

    assert isinstance(no_op, DominionSkillNoOpDecision)
    assert no_op.is_failure is False
    assert no_op.executes_anything is False
    assert isinstance(preview, DominionSkillRunPreview)
    assert preview.no_execution_guarantee is True
    assert preview.no_external_control_guarantee is True
    assert preview.no_authority_grant_guarantee is True
    assert preview.no_dominion_target_creation_guarantee is True
    assert preview.no_dominion_decision_creation_guarantee is True
    assert preview.no_registry_mutation_guarantee is True
    assert preview.no_memory_mutation_guarantee is True
    assert preview.executes_run is False
    assert dominion_run_preview_preserves_no_execution(preview) is True

    assert isinstance(foundation, DominionSkillFoundationReport)
    assert "v0.31.5" in foundation.version
    assert foundation.ready_for_execution is False
    assert foundation.ready_for_skill_activation is False
    assert foundation.ready_for_external_control is False
    assert foundation.ready_for_authority_grant is False
    assert foundation.runtime_enablement is False
    assert dominion_foundation_is_not_runtime_ready(foundation) is True

    assert isinstance(readiness, V0315ReadinessReport)
    assert "v0.31.5" in readiness.version
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_skill_activation is False
    assert readiness.ready_for_external_control is False
    assert readiness.ready_for_authority_grant is False
    assert readiness.ready_for_dominion_runtime is False
    assert readiness.runtime_enablement is False
    assert REQUIRED_PROHIBITIONS.issubset(set(readiness.prohibited_until_later_gate))
    assert dominion_foundation_is_not_runtime_ready(readiness) is True

    with pytest.raises(ValueError, match="ready_for_execution"):
        build_dominion_skill_output("output:bad", "dominion_input:1", "status", metadata={"external_control": False}, ready_for_v0316_dominion_target_decision=False).__class__(
            "output:bad",
            "dominion_input:1",
            None,
            "status",
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            [],
            ready_for_execution=True,
        )
    with pytest.raises(ValueError, match="ready_for_authority_grant"):
        DominionSkillOutput("output:bad", "dominion_input:1", None, "status", [], [], [], [], [], [], [], [], [], [], [], ready_for_authority_grant=True)
    with pytest.raises(ValueError, match="foundation artifact"):
        build_dominion_skill_output("output:bad", "dominion_input:1", "status", metadata={"authority_grant": True})
    with pytest.raises(ValueError, match="no_op_id"):
        build_dominion_no_op_decision("", "dominion_input:1", "reason")
    with pytest.raises(ValueError, match="reason"):
        build_dominion_no_op_decision("noop:bad", "dominion_input:1", "")
    with pytest.raises(ValueError, match="no_execution_guarantee"):
        DominionSkillRunPreview("preview:bad", no_execution_guarantee=False)
    with pytest.raises(ValueError, match="v0.31.5"):
        V0315ReadinessReport("readiness:bad", "v0.31.4", "foundation", "summary", True)
    with pytest.raises(ValueError, match="ready_for_external_control"):
        V0315ReadinessReport("readiness:bad", "v0.31.5", "foundation", "summary", True, ready_for_external_control=True)


def test_helpers_are_pure_conservative_foundation_builders() -> None:
    helpers = [
        build_dominion_source_ref,
        build_dominion_skill_input,
        classify_dominion_focus_from_source,
        infer_dominion_route_from_source_or_signal,
        build_dominion_control_boundary_signal,
        build_dominion_governance_finding,
        build_dominion_blocker,
        build_dominion_route_decision,
        build_dominion_skill_output,
        build_dominion_no_op_decision,
        build_dominion_run_preview,
        build_dominion_skill_foundation_report,
        build_v0315_readiness_report,
        dominion_input_preserves_no_execution,
        dominion_output_preserves_no_execution,
        dominion_output_is_not_target_or_decision,
        dominion_output_grants_no_authority,
        dominion_run_preview_preserves_no_execution,
        dominion_foundation_is_not_runtime_ready,
    ]

    for helper in helpers:
        source = inspect.getsource(helper)
        assert "ready_for_execution=True" not in source
        assert "ready_for_external_control=True" not in source
        assert "ready_for_authority_grant=True" not in source
        assert "ready_for_dominion_runtime=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source

    implementation_source = inspect.getsource(dominion)
    assert "subprocess" not in implementation_source
    assert "os.system" not in implementation_source
    assert "shell=True" not in implementation_source
    assert "requests." not in implementation_source
    assert "httpx." not in implementation_source
    assert "urllib." not in implementation_source
    assert "aiohttp." not in implementation_source
    assert "socket." not in implementation_source
    assert "DominionTarget" not in implementation_source
    assert "DominionDecision" not in implementation_source
