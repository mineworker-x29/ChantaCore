from __future__ import annotations

import inspect

import pytest

from chanta_core.external_dominion import DominionLevel
from chanta_core.internal_triad.consolidation import (
    DigestionSkillCoverage,
    DominionSkillCoverage,
    DominionTargetDecisionCoverage,
    InternalTriadConsolidationStatus,
    InternalTriadFoundationSnapshot,
    InternalTriadGapRegister,
    InternalTriadReadinessLevel,
    InternalTriadReleaseFlagSet,
    InternalTriadReleaseManifest,
    InternalTriadRiskRegister,
    InternalTriadV032HandoffPacket,
    InternalizationCoverage,
    ObservationReportCoverage,
    ObservationSkillCoverage,
    TriadOCELTraceCoverageSummary,
    TriadSkillContractCoverage,
    TriadWorkbenchCoverage,
    V031ConsolidationAuditTrail,
    V031ConsolidationReport,
    V0319_INCLUDED_VERSIONS,
    V0319_PROHIBITED_RUNTIME_SURFACES,
    build_internal_triad_foundation_snapshot,
    build_internal_triad_gap_register,
    build_internal_triad_release_manifest,
    build_internal_triad_risk_register,
    build_triad_coverage_matrix,
    build_v031_consolidation_audit_trail,
    build_v031_consolidation_report,
    build_v0319_release_flags,
    build_v032_handoff_packet,
    internal_triad_consolidation_preserves_no_execution,
    internal_triad_release_flags_preserve_runtime_false,
    v031_consolidation_report_is_not_runtime_ready,
    v032_handoff_packet_is_design_stage_only,
)


def test_v0319_status_and_readiness_taxonomies_are_conservative() -> None:
    assert {status.value for status in InternalTriadConsolidationStatus} == {
        "unknown",
        "not_started",
        "in_progress",
        "consolidated",
        "consolidated_with_gaps",
        "blocked",
        "future_track",
        "no_op",
    }
    assert {level.value for level in InternalTriadReadinessLevel} == {
        "not_ready",
        "contract_ready",
        "foundation_ready",
        "handoff_ready_for_v032",
        "blocked",
        "future_track",
    }


def test_release_flags_preserve_runtime_false_and_d4_d9_future_track() -> None:
    flags = build_v0319_release_flags()

    assert isinstance(flags, InternalTriadReleaseFlagSet)
    assert flags.internal_triad_skill_foundation_ready is True
    assert flags.ready_for_v032_external_harness_observation_pipeline is True
    assert internal_triad_release_flags_preserve_runtime_false(flags) is True
    assert flags.max_grantable_level == DominionLevel.D3_SIMULATE
    assert {
        DominionLevel.D4_EXECUTE_READ,
        DominionLevel.D5_EXECUTE_WRITE_PROPOSAL,
        DominionLevel.D6_EXECUTE_SANDBOX,
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D9_GATEWAY_CONTROL,
    }.issubset({DominionLevel(level) for level in flags.future_track_levels})

    for field_name in (
        "ready_for_execution",
        "ready_for_skill_activation",
        "ready_for_external_scan",
        "ready_for_read_only_tool_execution",
        "ready_for_ocel_emission",
        "ready_for_ui_runtime",
        "ready_for_action_execution",
        "ready_for_provider_invocation",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_command_execution",
        "ready_for_rpa_runtime_control",
        "ready_for_browser_runtime_control",
        "ready_for_gateway_control",
        "production_certified",
        "live_adapter_certified",
    ):
        with pytest.raises(ValueError, match=field_name):
            InternalTriadReleaseFlagSet(
                "flags:bad",
                "v0.31.9",
                True,
                True,
                **{field_name: True},
            )
    with pytest.raises(ValueError, match="max_grantable_level"):
        InternalTriadReleaseFlagSet("flags:bad", "v0.31.9", True, True, max_grantable_level=DominionLevel.D9_GATEWAY_CONTROL)


def test_snapshot_coverage_gap_risk_handoff_manifest_audit_and_report() -> None:
    flags = build_v0319_release_flags()
    snapshot = build_internal_triad_foundation_snapshot(release_flags=flags)
    coverage_classes = [
        TriadSkillContractCoverage,
        ObservationSkillCoverage,
        ObservationReportCoverage,
        DigestionSkillCoverage,
        InternalizationCoverage,
        DominionSkillCoverage,
        DominionTargetDecisionCoverage,
        TriadOCELTraceCoverageSummary,
        TriadWorkbenchCoverage,
    ]
    coverages = [
        build_triad_coverage_matrix(cls, f"coverage:{cls.__name__}", covered_artifact_refs=[cls.__name__])
        for cls in coverage_classes
    ]
    gap_register = build_internal_triad_gap_register()
    risk_register = build_internal_triad_risk_register()
    handoff = build_v032_handoff_packet(snapshot, gap_register=gap_register)
    manifest = build_internal_triad_release_manifest(snapshot, next_handoff_id=handoff.handoff_id)
    audit = build_v031_consolidation_audit_trail()
    report = build_v031_consolidation_report(snapshot, manifest, handoff, gap_register)

    assert isinstance(snapshot, InternalTriadFoundationSnapshot)
    assert set(V0319_INCLUDED_VERSIONS).issubset(set(snapshot.included_versions))
    assert snapshot.runtime_enablement is False
    assert all(coverage.coverage_complete is True and coverage.runtime_readiness is False for coverage in coverages)
    assert isinstance(gap_register, InternalTriadGapRegister)
    assert gap_register.blocks_v032 is False
    assert isinstance(risk_register, InternalTriadRiskRegister)
    assert set(V0319_PROHIBITED_RUNTIME_SURFACES).issubset(set(risk_register.prohibited_runtime_surfaces))
    assert risk_register.proves_exploitability is False
    assert isinstance(handoff, InternalTriadV032HandoffPacket)
    assert handoff.ready_for_v032 is True
    assert handoff.ready_for_execution is False
    assert "v0.32" in handoff.target_version_track
    assert any("external harness" in item.lower() for item in handoff.external_harness_pipeline_focus)
    assert v032_handoff_packet_is_design_stage_only(handoff) is True
    assert isinstance(manifest, InternalTriadReleaseManifest)
    assert set(V0319_INCLUDED_VERSIONS).issubset(set(manifest.included_versions))
    assert manifest.production_release is False
    assert isinstance(audit, V031ConsolidationAuditTrail)
    assert audit.no_execution_confirmed is True
    assert audit.no_external_scan_confirmed is True
    assert audit.no_tool_execution_confirmed is True
    assert audit.no_registry_mutation_confirmed is True
    assert audit.no_memory_mutation_confirmed is True
    assert audit.no_ocel_emission_confirmed is True
    assert audit.no_ui_runtime_confirmed is True
    assert audit.runtime_readiness_flags_false_confirmed is True
    assert audit.d4_d9_future_track_confirmed is True
    assert audit.runtime_audit_execution is False
    assert isinstance(report, V031ConsolidationReport)
    assert report.ready_for_v032 is True
    assert v031_consolidation_report_is_not_runtime_ready(report) is True
    assert internal_triad_consolidation_preserves_no_execution(report) is True


def test_v0319_negative_boundary_conditions_are_rejected() -> None:
    with pytest.raises(ValueError, match="included_versions"):
        build_internal_triad_foundation_snapshot().__class__(
            "snapshot:bad",
            "v0.31.9",
            "release",
            ["v0.31.8"],
            [],
            build_v0319_release_flags(),
            InternalTriadConsolidationStatus.CONSOLIDATED,
            InternalTriadReadinessLevel.FOUNDATION_READY,
            "summary",
        )
    with pytest.raises(ValueError, match="coverage_complete"):
        build_triad_coverage_matrix(TriadSkillContractCoverage, "coverage:bad", coverage_complete=True, blocking_gaps=["blocked"])
    snapshot = build_internal_triad_foundation_snapshot()
    with pytest.raises(ValueError, match="ready_for_execution"):
        InternalTriadV032HandoffPacket(
            "handoff:bad",
            "v0.31.9",
            "v0.32 External Harness Observation & Digestion Pipeline",
            snapshot.snapshot_id,
            None,
            "External Harness Observation & Digestion Pipeline",
            "v0.32.0",
            ["generic external harness observation"],
            ready_for_execution=True,
        )
    manifest = build_internal_triad_release_manifest(snapshot)
    with pytest.raises(ValueError, match="ready_for_v032"):
        V031ConsolidationReport(
            "report:bad",
            "v0.31.9",
            "release",
            snapshot.snapshot_id,
            manifest.release_manifest_id,
            None,
            InternalTriadConsolidationStatus.BLOCKED,
            InternalTriadReadinessLevel.BLOCKED,
            "summary",
            blocked_items=["blocking gap"],
            ready_for_v032=True,
        )
    with pytest.raises(ValueError, match="ready_for_execution"):
        V031ConsolidationReport(
            "report:bad",
            "v0.31.9",
            "release",
            snapshot.snapshot_id,
            manifest.release_manifest_id,
            None,
            InternalTriadConsolidationStatus.CONSOLIDATED,
            InternalTriadReadinessLevel.HANDOFF_READY_FOR_V032,
            "summary",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError, match="max_grantable_level"):
        build_v0319_release_flags().__class__(
            "flags:bad",
            "v0.31.9",
            True,
            True,
            max_grantable_level=DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        )
    with pytest.raises(ValueError, match="implementation"):
        build_v032_handoff_packet(snapshot, metadata={"implementation": True})


def test_v0319_helpers_are_pure_conservative() -> None:
    helpers = [
        build_v0319_release_flags,
        build_internal_triad_foundation_snapshot,
        build_triad_coverage_matrix,
        build_internal_triad_gap_register,
        build_internal_triad_risk_register,
        build_v032_handoff_packet,
        build_internal_triad_release_manifest,
        build_v031_consolidation_audit_trail,
        build_v031_consolidation_report,
        internal_triad_consolidation_preserves_no_execution,
        internal_triad_release_flags_preserve_runtime_false,
        v032_handoff_packet_is_design_stage_only,
        v031_consolidation_report_is_not_runtime_ready,
    ]
    for helper in helpers:
        source = inspect.getsource(helper)
        assert "ready_for_execution=True" not in source
        assert "ready_for_skill_activation=True" not in source
        assert "ready_for_external_scan=True" not in source
        assert "ready_for_read_only_tool_execution=True" not in source
        assert "ready_for_ocel_emission=True" not in source
        assert "ready_for_ui_runtime=True" not in source
        assert "production_certified=True" not in source
        assert "live_adapter_certified=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source
