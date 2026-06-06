from __future__ import annotations

import inspect

import pytest

from chanta_core.internal_triad import (
    CapabilityClassification,
    CapabilityMapEntry,
    CapabilityMapStatus,
    InternalCapabilityMap,
    InternalObservationReport,
    ObservationEvidenceQuality,
    ObservationEvidenceTable,
    ObservationFindingKind,
    ObservationFocusKind,
    ObservationGapKind,
    ObservationGapRegister,
    ObservationReportBundle,
    ObservationReportRunPreview,
    ObservationReportStatus,
    ObservationRiskMap,
    ObservationRiskPosture,
    ObservedTargetSummary,
    V0312ReadinessReport,
    build_capability_map_entry,
    build_internal_capability_map,
    build_internal_observation_report,
    build_observation_evidence_table,
    build_observation_finding,
    build_observation_gap,
    build_observation_gap_register,
    build_observation_report_bundle,
    build_observation_report_run_preview,
    build_observation_risk_map,
    build_observation_risk_signal,
    build_observation_skill_output,
    build_observed_target_summary,
    build_v0312_readiness_report,
    capability_map_preserves_no_activation,
    classify_capability_from_observation_finding,
    normalize_capability_classification,
    normalize_capability_map_status,
    normalize_observation_report_status,
    observation_bundle_preserves_no_runtime,
    observation_report_is_not_digestion_or_dominion,
    observation_report_preserves_no_execution,
)
from chanta_core.internal_triad import observation_reports


REQUIRED_V0312_GATE_ITEMS = {
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
    "digestion_candidate_creation",
    "dominion_target_creation",
}


def test_observation_report_taxonomies_are_complete_and_conservative() -> None:
    assert {status.value for status in ObservationReportStatus} == {
        "unknown",
        "draft",
        "report_ready",
        "report_ready_with_gaps",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert normalize_observation_report_status("report_ready") is ObservationReportStatus.REPORT_READY

    assert {classification.value for classification in CapabilityClassification} == {
        "unknown",
        "descriptive_only",
        "safe_descriptive",
        "digestion_signal",
        "dominion_signal",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert normalize_capability_classification("safe_descriptive") is CapabilityClassification.SAFE_DESCRIPTIVE

    assert {status.value for status in CapabilityMapStatus} == {
        "unknown",
        "map_ready",
        "map_ready_with_gaps",
        "incomplete",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert normalize_capability_map_status("map_ready") is CapabilityMapStatus.MAP_READY


def _sample_findings():
    descriptive = build_observation_finding(
        finding_id="finding:capability",
        finding_kind=ObservationFindingKind.CAPABILITY_DETECTED,
        focus_kind=ObservationFocusKind.CAPABILITY_SURFACE,
        target_id="target:1",
        artifact_ref_ids=["artifact_ref:handoff"],
        evidence_ref_ids=["evidence_ref:test"],
        summary="Available handoff refs describe a capability surface.",
        risk_posture=ObservationRiskPosture.UNKNOWN,
        evidence_quality=ObservationEvidenceQuality.SUFFICIENT_FOR_OBSERVATION,
    )
    digestion = build_observation_finding(
        finding_id="finding:digestion",
        finding_kind=ObservationFindingKind.DIGESTION_POSSIBLE_SIGNAL,
        focus_kind=ObservationFocusKind.DIGESTION_RELEVANCE,
        target_id="target:1",
        artifact_ref_ids=["artifact_ref:handoff"],
        evidence_ref_ids=["evidence_ref:test"],
        summary="A later digestion review may be useful.",
        risk_posture=ObservationRiskPosture.UNKNOWN,
        evidence_quality=ObservationEvidenceQuality.PARTIAL,
    )
    dominion = build_observation_finding(
        finding_id="finding:dominion",
        finding_kind=ObservationFindingKind.DOMINION_REQUIRED_SIGNAL,
        focus_kind=ObservationFocusKind.DOMINION_RELEVANCE,
        target_id="target:1",
        artifact_ref_ids=["artifact_ref:handoff"],
        evidence_ref_ids=["evidence_ref:test"],
        summary="A later dominion boundary review may be useful.",
        risk_posture=ObservationRiskPosture.MEDIUM,
        evidence_quality=ObservationEvidenceQuality.PARTIAL,
    )
    return descriptive, digestion, dominion


def test_capability_classification_from_observation_finding_is_signal_only() -> None:
    descriptive, digestion, dominion = _sample_findings()

    assert classify_capability_from_observation_finding(descriptive) is CapabilityClassification.SAFE_DESCRIPTIVE
    assert classify_capability_from_observation_finding(digestion) is CapabilityClassification.DIGESTION_SIGNAL
    assert classify_capability_from_observation_finding(dominion) is CapabilityClassification.DOMINION_SIGNAL


def test_capability_map_entry_is_not_permission_or_next_stage_object() -> None:
    entry = build_capability_map_entry(
        entry_id="capability_entry:1",
        target_id="target:1",
        capability_name="contract-observable capability",
        capability_kind="descriptive",
        classification=CapabilityClassification.DIGESTION_SIGNAL,
        source_finding_ids=["finding:digestion"],
        evidence_ref_ids=["evidence_ref:test"],
        risk_posture="unknown",
        evidence_quality="partial",
        boundary_surfaces=["no-execution"],
        effect_surfaces=["report-only"],
        recommended_next_stage="v0.31.3 design review",
    )

    assert isinstance(entry, CapabilityMapEntry)
    assert entry.classification == CapabilityClassification.DIGESTION_SIGNAL
    assert entry.grants_permission is False
    assert entry.activates_capability is False
    assert entry.creates_digestion_candidate is False
    assert entry.creates_dominion_target is False

    dominion_entry = build_capability_map_entry(
        "capability_entry:dominion",
        "contract-observable dominion signal",
        CapabilityClassification.DOMINION_SIGNAL,
        source_finding_ids=["finding:dominion"],
        evidence_ref_ids=["evidence_ref:test"],
    )
    assert dominion_entry.creates_dominion_target is False

    with pytest.raises(ValueError, match="entry_id"):
        build_capability_map_entry("", "capability", CapabilityClassification.UNKNOWN)
    with pytest.raises(ValueError, match="capability_name"):
        build_capability_map_entry("entry:bad", "", CapabilityClassification.UNKNOWN)
    with pytest.raises(ValueError, match="blocked_reasons"):
        build_capability_map_entry("entry:blocked", "blocked capability", CapabilityClassification.BLOCKED)
    with pytest.raises(ValueError, match="permission"):
        build_capability_map_entry(
            "entry:bad",
            "bad capability",
            CapabilityClassification.SAFE_DESCRIPTIVE,
            metadata={"permission_grant": True},
        )


def test_observed_target_summary_is_not_target_access() -> None:
    summary = build_observed_target_summary(
        target_summary_id="target_summary:1",
        target_id="target:1",
        display_name="External target one",
        source_target_ref_ids=["target_ref:1"],
        observed_capability_entry_ids=["capability_entry:1"],
        gap_ids=[],
        risk_signal_ids=[],
        evidence_ref_ids=["evidence_ref:test"],
        summary="Target is represented only by available refs.",
        risk_posture="unknown",
        evidence_quality="partial",
        ready_for_capability_map=True,
    )

    assert isinstance(summary, ObservedTargetSummary)
    assert summary.ready_for_execution is False
    assert summary.accesses_target is False

    with pytest.raises(ValueError, match="target_summary_id"):
        build_observed_target_summary("", "target:1", "summary")
    with pytest.raises(ValueError, match="target_id"):
        build_observed_target_summary("target_summary:bad", "", "summary")
    with pytest.raises(ValueError, match="summary"):
        build_observed_target_summary("target_summary:bad", "target:1", "")
    with pytest.raises(ValueError, match="ready_for_execution"):
        ObservedTargetSummary("target_summary:bad", "target:1", None, [], [], [], [], [], "summary", "unknown", "unknown", True, True)


def _sample_report_and_map():
    descriptive, digestion, dominion = _sample_findings()
    risk = build_observation_risk_signal(
        risk_signal_id="risk:dominion",
        target_id="target:1",
        signal_name="later-dominion-boundary-needed",
        posture=ObservationRiskPosture.HIGH,
        related_finding_ids=[dominion.finding_id],
        evidence_ref_ids=["evidence_ref:test"],
        recommended_boundary="Keep runtime controls disabled.",
    )
    gap = build_observation_gap(
        gap_id="gap:nonblocking",
        gap_kind=ObservationGapKind.MISSING_OCEL_TRACE_PLAN,
        target_id="target:1",
        artifact_ref_ids=["artifact_ref:handoff"],
        description="OCEL trace plan should be completed before later activation stages.",
        blocks_v0312=False,
        evidence_ref_ids=["evidence_ref:test"],
    )
    output = build_observation_skill_output(
        observation_output_id="observation_output:v0.31.1",
        observation_input_id="observation_input:v0.31.1",
        status="result_ready",
        findings=[descriptive, digestion, dominion],
        gaps=[gap],
        risk_signals=[risk],
        evidence_ref_ids=["evidence_ref:test"],
        ready_for_v0312_observation_report=True,
    )
    entries = [
        build_capability_map_entry(
            "capability_entry:safe",
            "descriptive capability",
            CapabilityClassification.SAFE_DESCRIPTIVE,
            target_id="target:1",
            source_finding_ids=[descriptive.finding_id],
            evidence_ref_ids=["evidence_ref:test"],
            evidence_quality="sufficient_for_observation",
        ),
        build_capability_map_entry(
            "capability_entry:digestion",
            "digestion signal capability",
            CapabilityClassification.DIGESTION_SIGNAL,
            target_id="target:1",
            source_finding_ids=[digestion.finding_id],
            evidence_ref_ids=["evidence_ref:test"],
            evidence_quality="partial",
        ),
        build_capability_map_entry(
            "capability_entry:dominion",
            "dominion signal capability",
            CapabilityClassification.DOMINION_SIGNAL,
            target_id="target:1",
            source_finding_ids=[dominion.finding_id],
            source_risk_signal_ids=[risk.risk_signal_id],
            evidence_ref_ids=["evidence_ref:test"],
            evidence_quality="partial",
        ),
    ]
    target_summary = build_observed_target_summary(
        "target_summary:1",
        "target:1",
        "Target can be summarized from available observation output only.",
        source_target_ref_ids=["target_ref:1"],
        observed_capability_entry_ids=[entry.entry_id for entry in entries],
        gap_ids=[gap.gap_id],
        risk_signal_ids=[risk.risk_signal_id],
        evidence_ref_ids=["evidence_ref:test"],
        ready_for_capability_map=True,
    )
    report = build_internal_observation_report(
        report_id="internal_observation_report:v0.31.2",
        observation_output=output,
        target_summaries=[target_summary],
        status=ObservationReportStatus.REPORT_READY_WITH_GAPS,
        summary="Internal observation report structures available v0.31.1 output.",
        report_gaps=[gap.gap_id],
        ready_for_v0313_digestion_skill_foundation=True,
        ready_for_v0315_dominion_skill_foundation=True,
    )
    capability_map = build_internal_capability_map(
        capability_map_id="internal_capability_map:v0.31.2",
        observation_report_id=report.report_id,
        target_id="target:1",
        entries=entries,
        safe_descriptive_capability_ids=["capability_entry:safe"],
        digestion_signal_capability_ids=["capability_entry:digestion"],
        dominion_signal_capability_ids=["capability_entry:dominion"],
        status=CapabilityMapStatus.MAP_READY_WITH_GAPS,
        evidence_ref_ids=["evidence_ref:test"],
        map_gaps=[gap.gap_id],
        ready_for_v0313_digestion_skill_foundation=True,
        ready_for_v0315_dominion_skill_foundation=True,
    )
    return report, capability_map, gap, risk


def test_internal_observation_report_preserves_no_execution_scan_or_next_stage_creation() -> None:
    report, _, _, _ = _sample_report_and_map()

    assert isinstance(report, InternalObservationReport)
    assert report.ready_for_execution is False
    assert report.ready_for_skill_activation is False
    assert report.ready_for_external_scan is False
    assert report.creates_digestion_candidate is False
    assert report.creates_dominion_target is False
    assert observation_report_preserves_no_execution(report) is True

    with pytest.raises(ValueError, match="report_id"):
        build_internal_observation_report("", "summary", ObservationReportStatus.DRAFT)
    with pytest.raises(ValueError, match="summary"):
        build_internal_observation_report("report:bad", "", ObservationReportStatus.DRAFT)
    with pytest.raises(ValueError, match="ready_for_execution"):
        InternalObservationReport("report:bad", None, None, [], [], [], [], [], ObservationReportStatus.DRAFT, "summary", ready_for_execution=True)
    with pytest.raises(ValueError, match="ready_for_external_scan"):
        InternalObservationReport("report:bad", None, None, [], [], [], [], [], ObservationReportStatus.DRAFT, "summary", ready_for_external_scan=True)
    with pytest.raises(ValueError, match="v0.31.3"):
        build_internal_observation_report(
            "report:bad",
            "blocked summary",
            ObservationReportStatus.BLOCKED,
            ready_for_v0313_digestion_skill_foundation=True,
        )
    with pytest.raises(ValueError, match="digestion"):
        build_internal_observation_report(
            "report:bad",
            "summary",
            ObservationReportStatus.DRAFT,
            metadata={"digestion_candidate_creation": True},
        )


def test_internal_capability_map_is_not_permission_or_activation_map() -> None:
    _, capability_map, _, _ = _sample_report_and_map()

    assert isinstance(capability_map, InternalCapabilityMap)
    assert capability_map.ready_for_execution is False
    assert capability_map.ready_for_skill_activation is False
    assert capability_map.grants_permission is False
    assert capability_map.activates_capabilities is False
    assert capability_map_preserves_no_activation(capability_map) is True

    with pytest.raises(ValueError, match="capability_map_id"):
        build_internal_capability_map("", "report:1")
    with pytest.raises(ValueError, match="observation_report_id"):
        build_internal_capability_map("map:bad", "")
    with pytest.raises(ValueError, match="ready_for_execution"):
        InternalCapabilityMap("map:bad", "report:1", None, [], [], [], [], [], [], [], CapabilityMapStatus.UNKNOWN, ready_for_execution=True)
    with pytest.raises(ValueError, match="activate capabilities"):
        build_internal_capability_map("map:bad", "report:1", metadata={"activate_capabilities": True})
    with pytest.raises(ValueError, match="blocked_reasons"):
        build_internal_capability_map(
            "map:bad",
            "report:1",
            entries=[build_capability_map_entry("entry:blocked", "blocked", CapabilityClassification.BLOCKED, blocked_reasons=["blocked"])],
            blocked_capability_ids=["entry:blocked"],
            status=CapabilityMapStatus.BLOCKED,
        )


def test_gap_register_risk_map_and_evidence_table_are_diagnostic_only() -> None:
    report, _, gap, risk = _sample_report_and_map()
    gap_register = build_observation_gap_register(
        "gap_register:v0.31.2",
        report.report_id,
        "Gap register preserves blocking and non-blocking diagnostic refs.",
        gap_ids=[gap.gap_id],
        blocking_gap_ids=["gap:blocking"],
        non_blocking_gap_ids=[gap.gap_id],
        evidence_ref_ids=["evidence_ref:test"],
    )
    risk_map = build_observation_risk_map(
        "risk_map:v0.31.2",
        report.report_id,
        "Risk map preserves advisory risk signals.",
        risk_signal_ids=[risk.risk_signal_id],
        high_risk_signal_ids=[risk.risk_signal_id],
        risk_surfaces=["external-runtime"],
        recommended_boundaries=["no-runtime"],
        evidence_ref_ids=["evidence_ref:test"],
    )
    evidence_table = build_observation_evidence_table(
        "evidence_table:v0.31.2",
        report.report_id,
        "Evidence table preserves evidence quality without runtime trust.",
        evidence_ref_ids=["evidence_ref:test"],
        strong_evidence_ref_ids=["evidence_ref:test"],
        weak_evidence_ref_ids=[],
        missing_evidence_items=["live scan evidence intentionally absent"],
        conflicting_evidence_ref_ids=["evidence_ref:conflicting"],
    )

    assert isinstance(gap_register, ObservationGapRegister)
    assert gap_register.blocks_next_stage is True
    assert gap_register.executes_remediation is False
    assert isinstance(risk_map, ObservationRiskMap)
    assert risk_map.grants_authority is False
    assert risk_map.creates_dominion_target is False
    assert isinstance(evidence_table, ObservationEvidenceTable)
    assert evidence_table.runtime_trust is False
    assert evidence_table.conflicting_evidence_ref_ids == ["evidence_ref:conflicting"]

    with pytest.raises(ValueError, match="remediation"):
        build_observation_gap_register("gap_register:bad", report.report_id, "summary", metadata={"automatic_remediation": True})
    with pytest.raises(ValueError, match="grant authority"):
        build_observation_risk_map("risk_map:bad", report.report_id, "summary", metadata={"authority_grant": True})
    with pytest.raises(ValueError, match="runtime trust"):
        build_observation_evidence_table("evidence_table:bad", report.report_id, "summary", metadata={"runtime_trust": True})


def test_observation_report_bundle_is_not_active_artifact_registration() -> None:
    report, capability_map, gap, risk = _sample_report_and_map()
    gap_register = build_observation_gap_register("gap_register:v0.31.2", report.report_id, "Gap register.", gap_ids=[gap.gap_id])
    risk_map = build_observation_risk_map("risk_map:v0.31.2", report.report_id, "Risk map.", risk_signal_ids=[risk.risk_signal_id])
    evidence_table = build_observation_evidence_table("evidence_table:v0.31.2", report.report_id, "Evidence table.", ["evidence_ref:test"])
    bundle = build_observation_report_bundle(
        "observation_report_bundle:v0.31.2",
        report,
        capability_map,
        gap_register,
        risk_map,
        evidence_table,
        ObservationReportStatus.REPORT_READY_WITH_GAPS,
        ready_for_v0313_digestion_skill_foundation=True,
        ready_for_v0315_dominion_skill_foundation=True,
        evidence_refs=["evidence_ref:test"],
    )

    assert isinstance(bundle, ObservationReportBundle)
    assert bundle.ready_for_execution is False
    assert bundle.ready_for_skill_activation is False
    assert bundle.ready_for_external_scan is False
    assert bundle.active_artifact_registration is False
    assert observation_bundle_preserves_no_runtime(bundle) is True
    assert observation_report_is_not_digestion_or_dominion(bundle) is True

    mismatched_gap_register = build_observation_gap_register("gap_register:mismatch", "other_report", "summary")
    with pytest.raises(ValueError, match="gap_register"):
        build_observation_report_bundle(
            "bundle:bad",
            report,
            capability_map,
            mismatched_gap_register,
            risk_map,
            evidence_table,
            ObservationReportStatus.DRAFT,
        )
    with pytest.raises(ValueError, match="ready_for_skill_activation"):
        ObservationReportBundle(
            "bundle:bad",
            report,
            capability_map,
            gap_register,
            risk_map,
            evidence_table,
            ObservationReportStatus.DRAFT,
            ready_for_skill_activation=True,
        )
    with pytest.raises(ValueError, match="active artifact registration"):
        build_observation_report_bundle(
            "bundle:bad",
            report,
            capability_map,
            gap_register,
            risk_map,
            evidence_table,
            ObservationReportStatus.DRAFT,
            metadata={"active_artifact_registration": True},
        )


def test_run_preview_and_readiness_report_are_not_runtime_enablement() -> None:
    report, capability_map, gap, risk = _sample_report_and_map()
    gap_register = build_observation_gap_register("gap_register:v0.31.2", report.report_id, "Gap register.", gap_ids=[gap.gap_id])
    risk_map = build_observation_risk_map("risk_map:v0.31.2", report.report_id, "Risk map.", risk_signal_ids=[risk.risk_signal_id])
    evidence_table = build_observation_evidence_table("evidence_table:v0.31.2", report.report_id, "Evidence table.")
    bundle = build_observation_report_bundle(
        "observation_report_bundle:v0.31.2",
        report,
        capability_map,
        gap_register,
        risk_map,
        evidence_table,
        ObservationReportStatus.REPORT_READY_WITH_GAPS,
        ready_for_v0313_digestion_skill_foundation=True,
        ready_for_v0315_dominion_skill_foundation=True,
    )
    preview = build_observation_report_run_preview("run_preview:v0.31.2", observation_output_id=report.observation_output_id)
    readiness = build_v0312_readiness_report(bundle)

    assert isinstance(preview, ObservationReportRunPreview)
    assert preview.no_execution_guarantee is True
    assert preview.no_external_scan_guarantee is True
    assert preview.no_tool_execution_guarantee is True
    assert preview.no_digestion_candidate_creation_guarantee is True
    assert preview.no_dominion_target_creation_guarantee is True
    assert preview.no_registry_mutation_guarantee is True
    assert preview.no_memory_mutation_guarantee is True
    assert preview.executes_run is False

    assert isinstance(readiness, V0312ReadinessReport)
    assert "v0.31.2" in readiness.version
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_skill_activation is False
    assert readiness.ready_for_external_scan is False
    assert readiness.runtime_enablement is False
    assert REQUIRED_V0312_GATE_ITEMS.issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError, match="run_preview_id"):
        build_observation_report_run_preview("")
    with pytest.raises(ValueError, match="no_execution_guarantee"):
        ObservationReportRunPreview("preview:bad", None, [], [], [], no_execution_guarantee=False)
    with pytest.raises(ValueError, match="v0.31.2"):
        V0312ReadinessReport("readiness:bad", "v0.31.1", None, "summary", False, False)
    with pytest.raises(ValueError, match="ready_for_external_scan"):
        V0312ReadinessReport("readiness:bad", "v0.31.2", None, "summary", False, False, ready_for_external_scan=True)
    with pytest.raises(ValueError, match="runtime readiness"):
        V0312ReadinessReport("readiness:bad", "v0.31.2", None, "summary", False, False, metadata={"runtime_enablement": True})


def test_helpers_are_pure_conservative_observation_report_builders() -> None:
    helpers = [
        classify_capability_from_observation_finding,
        build_capability_map_entry,
        build_observed_target_summary,
        build_internal_observation_report,
        build_internal_capability_map,
        build_observation_gap_register,
        build_observation_risk_map,
        build_observation_evidence_table,
        build_observation_report_bundle,
        build_observation_report_run_preview,
        build_v0312_readiness_report,
        observation_report_preserves_no_execution,
        capability_map_preserves_no_activation,
        observation_bundle_preserves_no_runtime,
        observation_report_is_not_digestion_or_dominion,
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

    implementation_source = inspect.getsource(observation_reports)
    assert "subprocess" not in implementation_source
    assert "os.system" not in implementation_source
    assert "shell=True" not in implementation_source
    assert "requests." not in implementation_source
    assert "httpx." not in implementation_source
    assert "urllib." not in implementation_source
    assert "aiohttp." not in implementation_source
    assert "socket." not in implementation_source
