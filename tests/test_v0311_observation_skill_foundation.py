from __future__ import annotations

import inspect

import pytest

from chanta_core.internal_triad import (
    ObservationArtifactRef,
    ObservationEvidenceQuality,
    ObservationEvidenceRef,
    ObservationFinding,
    ObservationFindingKind,
    ObservationFocusKind,
    ObservationGap,
    ObservationGapKind,
    ObservationRiskPosture,
    ObservationRiskSignal,
    ObservationSkillFoundationReport,
    ObservationSkillInput,
    ObservationSkillNoOpDecision,
    ObservationSkillOutput,
    ObservationSkillRunPreview,
    ObservationSkillSourceKind,
    ObservationTargetRef,
    V0311ReadinessReport,
    build_observation_artifact_ref,
    build_observation_evidence_ref,
    build_observation_finding,
    build_observation_gap,
    build_observation_no_op_decision,
    build_observation_risk_signal,
    build_observation_run_preview,
    build_observation_skill_foundation_report,
    build_observation_skill_input,
    build_observation_skill_output,
    build_observation_target_ref,
    build_v0311_readiness_report,
    normalize_observation_evidence_quality,
    normalize_observation_finding_kind,
    normalize_observation_focus_kind,
    normalize_observation_gap_kind,
    normalize_observation_risk_posture,
    normalize_observation_source_kind,
    observation_finding_kind_is_certification,
    observation_focus_kind_creates_next_stage_artifact,
    observation_foundation_is_not_runtime_ready,
    observation_input_preserves_no_execution,
    observation_output_preserves_no_execution,
    observation_run_preview_preserves_no_execution,
    observation_source_kind_fetches,
)
from chanta_core.internal_triad import observation


REQUIRED_PROHIBITIONS = {
    "external_scan",
    "source_ref_fetch",
    "url_fetch",
    "internal_tool_execution",
    "read_only_tool_execution",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "active_registry_mutation",
    "active_memory_mutation",
    "rollback",
    "retry",
}


def test_observation_taxonomies_are_complete_and_conservative() -> None:
    assert {kind.value for kind in ObservationSkillSourceKind} == {
        "v030_handoff_packet",
        "external_target_record",
        "external_capability_observation_report",
        "digestion_feasibility_report",
        "dominion_authority_decision",
        "external_delegation_dry_run_report",
        "approval_audit_boundary",
        "certification_report",
        "preview_gate_report",
        "consolidation_report",
        "manual_evidence_ref",
        "unknown",
    }
    assert normalize_observation_source_kind("unknown") is ObservationSkillSourceKind.UNKNOWN
    assert observation_source_kind_fetches(ObservationSkillSourceKind.V030_HANDOFF_PACKET) is False

    assert {kind.value for kind in ObservationFocusKind} == {
        "target_identity",
        "target_trust_boundary",
        "capability_surface",
        "evidence_quality",
        "risk_surface",
        "effect_surface",
        "boundary_surface",
        "digestion_relevance",
        "dominion_relevance",
        "certification_coverage",
        "preview_gate_readiness",
        "ocel_trace_relevance",
        "gap_detection",
        "unknown",
    }
    assert normalize_observation_focus_kind("digestion_relevance") is ObservationFocusKind.DIGESTION_RELEVANCE
    assert observation_focus_kind_creates_next_stage_artifact(ObservationFocusKind.DOMINION_RELEVANCE) is False

    assert {kind.value for kind in ObservationFindingKind} == {
        "descriptive_summary",
        "capability_detected",
        "evidence_linked",
        "evidence_missing",
        "risk_signal_detected",
        "boundary_surface_detected",
        "effect_surface_detected",
        "trust_gap_detected",
        "digestion_possible_signal",
        "dominion_required_signal",
        "certification_gap_signal",
        "preview_gate_gap_signal",
        "ocel_trace_need_detected",
        "no_op_recommended",
        "unknown",
    }
    assert normalize_observation_finding_kind("dominion_required_signal") is ObservationFindingKind.DOMINION_REQUIRED_SIGNAL
    assert observation_finding_kind_is_certification(ObservationFindingKind.CERTIFICATION_GAP_SIGNAL) is False


def test_observation_gap_risk_and_evidence_taxonomies() -> None:
    assert {kind.value for kind in ObservationGapKind} == {
        "missing_target_identity",
        "missing_trust_boundary",
        "missing_capability_report",
        "missing_evidence_refs",
        "missing_risk_classification",
        "missing_boundary_classification",
        "missing_digestion_decision",
        "missing_dominion_decision",
        "missing_approval_boundary",
        "missing_audit_policy",
        "missing_result_boundary",
        "missing_rollback_or_no_op",
        "missing_certification_case",
        "missing_preview_gate_decision",
        "missing_ocel_trace_plan",
        "unknown",
    }
    assert normalize_observation_gap_kind("missing_ocel_trace_plan") is ObservationGapKind.MISSING_OCEL_TRACE_PLAN

    assert {posture.value for posture in ObservationRiskPosture} == {
        "unknown",
        "low",
        "medium",
        "high",
        "critical",
        "blocked",
        "future_track",
    }
    assert normalize_observation_risk_posture("future_track") is ObservationRiskPosture.FUTURE_TRACK

    assert {quality.value for quality in ObservationEvidenceQuality} == {
        "unknown",
        "none",
        "weak",
        "partial",
        "sufficient_for_observation",
        "sufficient_for_next_stage_review",
        "conflicting",
        "blocked",
    }
    assert normalize_observation_evidence_quality("sufficient_for_observation") is ObservationEvidenceQuality.SUFFICIENT_FOR_OBSERVATION


def test_observation_refs_are_references_not_fetch_or_access() -> None:
    target = build_observation_target_ref(
        target_ref_id="target_ref:1",
        target_id="external_target:1",
        target_kind="provider",
        source_kind=ObservationSkillSourceKind.EXTERNAL_TARGET_RECORD,
        source_ref="source_ref:target:1",
    )
    artifact = build_observation_artifact_ref(
        artifact_ref_id="artifact_ref:1",
        artifact_kind="v0309_handoff_packet",
        artifact_id="handoff:v0.30.9",
        source_kind=ObservationSkillSourceKind.V030_HANDOFF_PACKET,
        source_version="v0.30.9",
    )
    evidence = build_observation_evidence_ref(
        evidence_ref_id="evidence_ref:1",
        evidence_kind="test",
        evidence_id="tests:test_v0309",
        quality=ObservationEvidenceQuality.SUFFICIENT_FOR_OBSERVATION,
        source_artifact_ref_id=artifact.artifact_ref_id,
    )

    assert isinstance(target, ObservationTargetRef)
    assert target.accesses_target is False
    assert target.fetches_source_ref is False
    assert isinstance(artifact, ObservationArtifactRef)
    assert artifact.fetches_artifact is False
    assert isinstance(evidence, ObservationEvidenceRef)
    assert evidence.runtime_trust is False

    with pytest.raises(ValueError, match="target_ref_id"):
        build_observation_target_ref("", "target", ObservationSkillSourceKind.UNKNOWN)
    with pytest.raises(ValueError, match="target_id"):
        build_observation_target_ref("target_ref:bad", "", ObservationSkillSourceKind.UNKNOWN)
    with pytest.raises(ValueError, match="artifact_ref_id"):
        build_observation_artifact_ref("", "kind", "artifact", ObservationSkillSourceKind.UNKNOWN)
    with pytest.raises(ValueError, match="artifact_kind"):
        build_observation_artifact_ref("artifact_ref:bad", "", "artifact", ObservationSkillSourceKind.UNKNOWN)
    with pytest.raises(ValueError, match="artifact_id"):
        build_observation_artifact_ref("artifact_ref:bad", "kind", "", ObservationSkillSourceKind.UNKNOWN)
    with pytest.raises(ValueError, match="evidence_ref_id"):
        build_observation_evidence_ref("", "kind", "evidence", ObservationEvidenceQuality.WEAK)
    with pytest.raises(ValueError, match="evidence_kind"):
        build_observation_evidence_ref("evidence_ref:bad", "", "evidence", ObservationEvidenceQuality.WEAK)
    with pytest.raises(ValueError, match="evidence_id"):
        build_observation_evidence_ref("evidence_ref:bad", "kind", "", ObservationEvidenceQuality.WEAK)
    with pytest.raises(ValueError, match="conflict_notes"):
        build_observation_evidence_ref(
            "evidence_ref:conflict",
            "kind",
            "evidence",
            ObservationEvidenceQuality.CONFLICTING,
        )


def _sample_input() -> ObservationSkillInput:
    target = build_observation_target_ref("target_ref:1", "target:1", ObservationSkillSourceKind.EXTERNAL_TARGET_RECORD)
    artifact = build_observation_artifact_ref(
        "artifact_ref:1",
        "handoff_packet",
        "handoff:v0.30.9",
        ObservationSkillSourceKind.V030_HANDOFF_PACKET,
        "v0.30.9",
    )
    evidence = build_observation_evidence_ref(
        "evidence_ref:1",
        "test",
        "test:v0309",
        ObservationEvidenceQuality.SUFFICIENT_FOR_OBSERVATION,
        artifact.artifact_ref_id,
    )
    return build_observation_skill_input(
        observation_input_id="observation_input:v0.31.1",
        triad_input_id="triad_input:v0.31.0",
        requested_focus=[ObservationFocusKind.CAPABILITY_SURFACE, ObservationFocusKind.GAP_DETECTION],
        target_refs=[target],
        artifact_refs=[artifact],
        evidence_refs=[evidence],
        task_summary="Structure available v0.30.9 handoff refs for observation.",
        source_version="v0.31.1",
    )


def test_observation_skill_input_is_not_execution_request_or_external_scan() -> None:
    observation_input = _sample_input()

    assert observation_input.is_execution_request is False
    assert observation_input.triad_input_id == "triad_input:v0.31.0"
    assert REQUIRED_PROHIBITIONS.issubset(set(observation_input.prohibited_runtime_actions))
    assert observation_input_preserves_no_execution(observation_input) is True

    with pytest.raises(ValueError, match="observation_input_id"):
        build_observation_skill_input("", "summary", "v0.31.1")
    with pytest.raises(ValueError, match="task_summary"):
        build_observation_skill_input("input:bad", "", "v0.31.1")
    with pytest.raises(ValueError, match="source_version"):
        build_observation_skill_input("input:bad", "summary", "")
    with pytest.raises(TypeError, match="requested_focus"):
        ObservationSkillInput(
            observation_input_id="input:bad",
            triad_input_id=None,
            requested_focus="not-list",
            target_refs=[],
            artifact_refs=[],
            evidence_refs=[],
            task_summary="summary",
            source_version="v0.31.1",
        )
    with pytest.raises(ValueError, match="external scan"):
        build_observation_skill_input(
            "input:bad",
            "summary",
            "v0.31.1",
            metadata={"external_scan": True},
        )


def test_observation_finding_is_not_certification_digestion_or_dominion() -> None:
    finding = build_observation_finding(
        finding_id="finding:1",
        finding_kind=ObservationFindingKind.DIGESTION_POSSIBLE_SIGNAL,
        focus_kind=ObservationFocusKind.DIGESTION_RELEVANCE,
        target_id="target:1",
        artifact_ref_ids=["artifact_ref:1"],
        evidence_ref_ids=["evidence_ref:1"],
        summary="Available contract refs may be relevant to later digestion review.",
        risk_posture=ObservationRiskPosture.UNKNOWN,
        evidence_quality=ObservationEvidenceQuality.SUFFICIENT_FOR_OBSERVATION,
    )
    dominion_signal = build_observation_finding(
        finding_id="finding:dominion",
        finding_kind=ObservationFindingKind.DOMINION_REQUIRED_SIGNAL,
        focus_kind=ObservationFocusKind.DOMINION_RELEVANCE,
        target_id="target:1",
        artifact_ref_ids=["artifact_ref:1"],
        evidence_ref_ids=["evidence_ref:1"],
        summary="Available boundary refs may require later dominion review.",
        risk_posture=ObservationRiskPosture.MEDIUM,
        evidence_quality=ObservationEvidenceQuality.PARTIAL,
    )

    assert isinstance(finding, ObservationFinding)
    assert finding.is_certification is False
    assert finding.grants_permission is False
    assert finding.creates_digestion_or_dominion_artifact is False
    assert dominion_signal.creates_digestion_or_dominion_artifact is False

    with pytest.raises(ValueError, match="finding_id"):
        build_observation_finding("", ObservationFindingKind.UNKNOWN, ObservationFocusKind.UNKNOWN, "summary")
    with pytest.raises(ValueError, match="summary"):
        build_observation_finding("finding:bad", ObservationFindingKind.UNKNOWN, ObservationFocusKind.UNKNOWN, "")
    with pytest.raises(ValueError, match="evidence_quality"):
        build_observation_finding(
            "finding:bad",
            ObservationFindingKind.CAPABILITY_DETECTED,
            ObservationFocusKind.CAPABILITY_SURFACE,
            "summary",
            evidence_quality=ObservationEvidenceQuality.SUFFICIENT_FOR_OBSERVATION,
        )
    with pytest.raises(ValueError, match="risk_posture"):
        build_observation_finding(
            "finding:bad",
            ObservationFindingKind.RISK_SIGNAL_DETECTED,
            ObservationFocusKind.RISK_SURFACE,
            "summary",
            risk_posture=ObservationRiskPosture.HIGH,
            evidence_quality=ObservationEvidenceQuality.WEAK,
        )
    with pytest.raises(ValueError, match="digestion candidate"):
        build_observation_finding(
            "finding:bad",
            ObservationFindingKind.DIGESTION_POSSIBLE_SIGNAL,
            ObservationFocusKind.DIGESTION_RELEVANCE,
            "summary",
            metadata={"digestion_candidate": True},
        )


def test_observation_gap_and_risk_signal_are_diagnostic_not_authority() -> None:
    gap = build_observation_gap(
        gap_id="gap:1",
        gap_kind=ObservationGapKind.MISSING_OCEL_TRACE_PLAN,
        target_id="target:1",
        artifact_ref_ids=["artifact_ref:1"],
        description="OCEL trace plan ref is missing for next-stage observation report design.",
        blocks_v0312=True,
        recommended_followup="Add OCEL trace planning contract refs before v0.31.2 readiness.",
    )
    signal = build_observation_risk_signal(
        risk_signal_id="risk:1",
        target_id="target:1",
        signal_name="external-runtime-surface-present",
        posture=ObservationRiskPosture.HIGH,
        related_gap_ids=[gap.gap_id],
        recommended_boundary="Keep external runtime surfaces prohibited until later gate.",
    )

    assert isinstance(gap, ObservationGap)
    assert gap.executes_remediation is False
    assert gap.blocks_v0312 is True
    assert isinstance(signal, ObservationRiskSignal)
    assert signal.grants_authority is False

    with pytest.raises(ValueError, match="gap_id"):
        build_observation_gap("", ObservationGapKind.UNKNOWN, "description", False)
    with pytest.raises(ValueError, match="description"):
        build_observation_gap("gap:bad", ObservationGapKind.UNKNOWN, "", False)
    with pytest.raises(TypeError, match="blocks_v0312"):
        ObservationGap("gap:bad", ObservationGapKind.UNKNOWN, None, [], "description", "yes")
    with pytest.raises(ValueError, match="risk_signal_id"):
        build_observation_risk_signal("", "signal", ObservationRiskPosture.UNKNOWN)
    with pytest.raises(ValueError, match="signal_name"):
        build_observation_risk_signal("risk:bad", "", ObservationRiskPosture.UNKNOWN)
    with pytest.raises(ValueError, match="recommended_boundary"):
        build_observation_risk_signal("risk:bad", "critical-risk", ObservationRiskPosture.CRITICAL)


def test_observation_skill_output_preserves_no_execution_and_no_next_stage_artifacts() -> None:
    finding = build_observation_finding(
        "finding:1",
        ObservationFindingKind.EVIDENCE_LINKED,
        ObservationFocusKind.EVIDENCE_QUALITY,
        "Evidence refs are sufficient for observation.",
        evidence_ref_ids=["evidence_ref:1"],
        evidence_quality=ObservationEvidenceQuality.SUFFICIENT_FOR_OBSERVATION,
    )
    output = build_observation_skill_output(
        observation_output_id="observation_output:1",
        observation_input_id="observation_input:v0.31.1",
        skill_contract_id="internal_triad_skill_contract:observation:v0.31.0",
        status="result_ready",
        findings=[finding],
        gaps=[],
        risk_signals=[],
        observed_target_ref_ids=["target_ref:1"],
        observed_artifact_ref_ids=["artifact_ref:1"],
        evidence_ref_ids=["evidence_ref:1"],
        ready_for_v0312_observation_report=True,
    )

    assert isinstance(output, ObservationSkillOutput)
    assert output.ready_for_execution is False
    assert output.ready_for_skill_activation is False
    assert output.ready_for_external_scan is False
    assert output.ready_for_v0312_observation_report is True
    assert output.creates_digestion_candidate is False
    assert output.creates_dominion_target is False
    assert observation_output_preserves_no_execution(output) is True

    blocking_gap = build_observation_gap("gap:blocking", ObservationGapKind.MISSING_EVIDENCE_REFS, "missing evidence", True)
    with pytest.raises(ValueError, match="v0.31.2"):
        build_observation_skill_output(
            "output:bad",
            "input:1",
            "blocked",
            gaps=[blocking_gap],
            ready_for_v0312_observation_report=True,
        )
    with pytest.raises(ValueError, match="ready_for_execution"):
        ObservationSkillOutput("output:bad", "input", None, "status", [], [], [], ready_for_execution=True)
    with pytest.raises(ValueError, match="ready_for_skill_activation"):
        ObservationSkillOutput("output:bad", "input", None, "status", [], [], [], ready_for_skill_activation=True)
    with pytest.raises(ValueError, match="ready_for_external_scan"):
        ObservationSkillOutput("output:bad", "input", None, "status", [], [], [], ready_for_external_scan=True)
    with pytest.raises(ValueError, match="digestion candidate"):
        build_observation_skill_output("output:bad", "input", "status", metadata={"digestion_candidate": True})
    with pytest.raises(ValueError, match="dominion target"):
        build_observation_skill_output("output:bad", "input", "status", metadata={"dominion_target": True})


def test_no_op_and_run_preview_are_valid_non_execution_artifacts() -> None:
    no_op = build_observation_no_op_decision(
        no_op_id="noop:1",
        observation_input_id="observation_input:v0.31.1",
        reason="No available artifacts need observation structuring.",
        safe_alternatives=["defer to later evidence collection"],
    )
    preview = build_observation_run_preview(
        run_preview_id="run_preview:1",
        observation_input_id="observation_input:v0.31.1",
    )

    assert isinstance(no_op, ObservationSkillNoOpDecision)
    assert no_op.is_failure is False
    assert no_op.executes_anything is False
    assert isinstance(preview, ObservationSkillRunPreview)
    assert preview.no_execution_guarantee is True
    assert preview.no_external_scan_guarantee is True
    assert preview.no_tool_execution_guarantee is True
    assert preview.no_registry_mutation_guarantee is True
    assert preview.no_memory_mutation_guarantee is True
    assert preview.executes_run is False
    assert observation_run_preview_preserves_no_execution(preview) is True

    with pytest.raises(ValueError, match="no_op_id"):
        build_observation_no_op_decision("", "input", "reason")
    with pytest.raises(ValueError, match="observation_input_id"):
        build_observation_no_op_decision("noop:bad", "", "reason")
    with pytest.raises(ValueError, match="reason"):
        build_observation_no_op_decision("noop:bad", "input", "")
    with pytest.raises(ValueError, match="run_preview_id"):
        build_observation_run_preview("", "input")
    with pytest.raises(ValueError, match="observation_input_id"):
        build_observation_run_preview("preview:bad", "")
    with pytest.raises(ValueError, match="no_execution_guarantee"):
        ObservationSkillRunPreview("preview:bad", "input", [], [], [], no_execution_guarantee=False)
    with pytest.raises(ValueError, match="execution"):
        build_observation_run_preview("preview:bad", "input", metadata={"executes_run": True})


def test_foundation_and_readiness_reports_are_next_stage_only() -> None:
    foundation = build_observation_skill_foundation_report()
    readiness = build_v0311_readiness_report(foundation)

    assert isinstance(foundation, ObservationSkillFoundationReport)
    assert "v0.31.1" in foundation.version
    assert foundation.ready_for_v0312_observation_report_capability_map is True
    assert foundation.ready_for_execution is False
    assert foundation.ready_for_skill_activation is False
    assert foundation.ready_for_external_scan is False
    assert foundation.runtime_enablement is False
    assert REQUIRED_PROHIBITIONS.issubset(set(foundation.prohibited_runtime_actions))
    assert observation_foundation_is_not_runtime_ready(foundation) is True

    assert isinstance(readiness, V0311ReadinessReport)
    assert "v0.31.1" in readiness.version
    assert readiness.ready_for_v0312_observation_report_capability_map is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_skill_activation is False
    assert readiness.ready_for_external_scan is False
    assert readiness.runtime_enablement is False
    assert {
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
    }.issubset(set(readiness.prohibited_until_later_gate))
    assert observation_foundation_is_not_runtime_ready(readiness) is True

    with pytest.raises(ValueError, match="v0.31.1"):
        ObservationSkillFoundationReport(
            foundation_report_id="foundation:bad",
            version="v0.31.0",
            observation_contract_ref=None,
            supported_source_kinds=[],
            supported_focus_kinds=[],
            supported_output_artifact_kinds=[],
            prohibited_runtime_actions=list(observation.V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
            ready_for_v0312_observation_report_capability_map=True,
            summary="summary",
        )
    with pytest.raises(ValueError, match="ready_for_execution"):
        ObservationSkillFoundationReport(
            foundation_report_id="foundation:bad",
            version="v0.31.1",
            observation_contract_ref=None,
            supported_source_kinds=[],
            supported_focus_kinds=[],
            supported_output_artifact_kinds=[],
            prohibited_runtime_actions=list(observation.V0311_REQUIRED_PROHIBITED_RUNTIME_ACTIONS),
            ready_for_v0312_observation_report_capability_map=True,
            ready_for_execution=True,
            summary="summary",
        )
    with pytest.raises(ValueError, match="ready_for_external_scan"):
        V0311ReadinessReport(
            report_id="readiness:bad",
            version="v0.31.1",
            observation_foundation_report_id=foundation.foundation_report_id,
            summary="summary",
            ready_for_v0312_observation_report_capability_map=True,
            ready_for_external_scan=True,
        )


def test_helpers_are_pure_conservative_observation_artifact_builders() -> None:
    helpers = [
        build_observation_target_ref,
        build_observation_artifact_ref,
        build_observation_evidence_ref,
        build_observation_skill_input,
        build_observation_finding,
        build_observation_gap,
        build_observation_risk_signal,
        build_observation_skill_output,
        build_observation_no_op_decision,
        build_observation_run_preview,
        build_observation_skill_foundation_report,
        build_v0311_readiness_report,
        observation_input_preserves_no_execution,
        observation_output_preserves_no_execution,
        observation_run_preview_preserves_no_execution,
        observation_foundation_is_not_runtime_ready,
    ]

    for helper in helpers:
        source = inspect.getsource(helper)
        assert "ready_for_execution=True" not in source
        assert "ready_for_skill_activation=True" not in source
        assert "ready_for_external_scan=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source

    implementation_source = inspect.getsource(observation)
    assert "subprocess" not in implementation_source
    assert "os.system" not in implementation_source
    assert "shell=True" not in implementation_source
    assert "requests." not in implementation_source
    assert "httpx." not in implementation_source
    assert "urllib." not in implementation_source
    assert "aiohttp." not in implementation_source
    assert "socket." not in implementation_source

