import pytest

from chanta_core.external_harness import (
    DigestionCandidateCoverage,
    DominionCandidateEmissionCoverage,
    ExternalHarnessPipelineSnapshot,
    ExternalHarnessProfileCoverage,
    ExternalPipelineConsolidationAuditTrail,
    ExternalPipelineConsolidationStatus,
    ExternalPipelineReadinessLevel,
    ExternalPipelineReleaseFlagSet,
    ExternalPipelineReleaseManifest,
    ExternalPipelineRiskRegister,
    HermesObservationCoverage,
    InternalCandidateEmissionCoverage,
    ManifestExtractionCoverage,
    OpenClawObservationCoverage,
    OpenCodeObservationCoverage,
    ReferenceCorpusCoverage,
    RiskClassificationCoverage,
    V032ConsolidationReport,
    V033HandoffPacket,
    build_external_harness_pipeline_snapshot,
    build_external_pipeline_consolidation_audit_trail,
    build_external_pipeline_coverage_matrix,
    build_external_pipeline_gap_register,
    build_external_pipeline_release_manifest,
    build_external_pipeline_risk_register,
    build_v032_consolidation_report,
    build_v0328_readiness_report,
    build_v0329_release_flags,
    build_v033_handoff_packet,
    external_pipeline_coverage_is_not_certification,
    external_pipeline_release_flags_preserve_runtime_false,
    external_pipeline_snapshot_is_not_runtime_ready,
    v0328_readiness_report_is_not_runtime_ready,
    v032_consolidation_report_is_not_runtime_ready,
    v033_handoff_packet_is_design_stage_only,
)
from chanta_core.external_harness.consolidation import (
    DEFAULT_CONSOLIDATION_PROHIBITED_RUNTIME_SURFACES,
    DEFAULT_FUTURE_TRACK_LEVELS,
    DEFAULT_V033_FOCUS_ITEMS,
    REQUIRED_V032_INCLUDED_VERSIONS,
    RUNTIME_FLAG_NAMES,
)


def test_consolidation_taxonomies_and_release_flags_preserve_runtime_false():
    assert {item.value for item in ExternalPipelineConsolidationStatus} == {
        "unknown",
        "not_started",
        "in_progress",
        "consolidated",
        "consolidated_with_gaps",
        "blocked",
        "future_track",
        "no_op",
    }
    assert {item.value for item in ExternalPipelineReadinessLevel} == {
        "not_ready",
        "contract_ready",
        "profile_ready",
        "static_observation_ready",
        "pipeline_foundation_ready",
        "handoff_ready_for_v033",
        "blocked",
        "future_track",
    }

    flags = build_v0329_release_flags(
        ready_for_v033_internal_general_agent_runtime_mvp=True,
        max_grantable_level="D3_SIMULATE",
    )

    assert flags.external_harness_observation_digestion_pipeline_ready is True
    assert flags.ready_for_v033_internal_general_agent_runtime_mvp is True
    assert external_pipeline_release_flags_preserve_runtime_false(flags)
    assert flags.production_certified is False
    assert flags.live_adapter_certified is False
    assert set(DEFAULT_FUTURE_TRACK_LEVELS).issubset(set(flags.future_track_levels))

    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            ExternalPipelineReleaseFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.32.9",
                **{flag_name: True},
            )

    for cert_flag in ("production_certified", "live_adapter_certified"):
        with pytest.raises(ValueError):
            ExternalPipelineReleaseFlagSet(
                flag_set_id=f"flags:bad:{cert_flag}",
                version="v0.32.9",
                **{cert_flag: True},
            )

    with pytest.raises(ValueError):
        build_v0329_release_flags(max_grantable_level="D4_APPROVE")
    with pytest.raises(ValueError):
        build_v0329_release_flags(future_track_levels=["D4", "D5"])


def test_pipeline_snapshot_and_coverage_matrices_are_not_runtime_or_certification():
    flags = build_v0329_release_flags()
    snapshot = build_external_harness_pipeline_snapshot(
        "snapshot:1",
        flags,
        included_artifact_groups=[
            "profiles",
            "reference_corpus",
            "manifest_extraction",
            "risk_classification",
            "digestion_candidates",
            "internal_candidates",
            "dominion_candidates",
        ],
        evidence_refs=["evidence:snapshot"],
    )

    assert set(REQUIRED_V032_INCLUDED_VERSIONS).issubset(set(snapshot.included_versions))
    assert external_pipeline_snapshot_is_not_runtime_ready(snapshot)
    assert snapshot.runtime_enablement is False

    coverage_classes = (
        ExternalHarnessProfileCoverage,
        ReferenceCorpusCoverage,
        OpenCodeObservationCoverage,
        OpenClawObservationCoverage,
        HermesObservationCoverage,
        ManifestExtractionCoverage,
        RiskClassificationCoverage,
        DigestionCandidateCoverage,
        InternalCandidateEmissionCoverage,
        DominionCandidateEmissionCoverage,
    )
    for coverage_cls in coverage_classes:
        coverage = build_external_pipeline_coverage_matrix(
            f"coverage:{coverage_cls.__name__}",
            coverage_cls=coverage_cls,
            covered_artifact_refs=["artifact:1"],
            covered_test_refs=["test:1"],
            covered_doc_refs=["doc:1"],
            coverage_complete=True,
        )
        assert coverage.coverage_complete is True
        assert external_pipeline_coverage_is_not_certification(coverage)
        assert coverage.runtime_readiness is False

    with pytest.raises(ValueError):
        ExternalHarnessPipelineSnapshot(
            snapshot_id="snapshot:bad",
            version="v0.32.9",
            release_name="bad",
            included_versions=["v0.32.8"],
            included_artifact_groups=[],
            release_flags=flags,
            consolidation_status=ExternalPipelineConsolidationStatus.CONSOLIDATED,
            readiness_level=ExternalPipelineReadinessLevel.PIPELINE_FOUNDATION_READY,
            summary="bad",
        )
    with pytest.raises(ValueError):
        ExternalHarnessProfileCoverage(
            coverage_id="coverage:bad",
            version="v0.32.9",
            coverage_complete=True,
            blocking_gaps=["missing required contract"],
        )
    with pytest.raises(ValueError):
        ReferenceCorpusCoverage(
            coverage_id="coverage:certification",
            version="v0.32.9",
            metadata={"certification": True},
        )


def test_gap_risk_manifest_and_audit_are_consolidation_metadata_only():
    flags = build_v0329_release_flags()
    gap_register = build_external_pipeline_gap_register(
        future_track_items=["runtime execution", "read-only tool execution", "runtime adapter loading"],
        recommended_v033_items=["profile runtime design"],
        recommended_later_items=["D4-D9 governance"],
    )
    blocking_gap_register = build_external_pipeline_gap_register(blocking_gaps=["missing v0.32.8 evidence"])
    risk_register = build_external_pipeline_risk_register(
        known_risks=["runtime surfaces remain prohibited"],
        high_risk_surfaces=["command_execution"],
        mitigations=["contract boundary review"],
        unresolved_risks=["runtime behavior unknown"],
    )
    manifest = build_external_pipeline_release_manifest(
        "manifest:1",
        flags,
        snapshot_id="snapshot:1",
        included_modules=["src/chanta_core/external_harness/consolidation.py"],
        included_docs=["docs/versions/v0.32/v0.32.9_external_observation_digestion_consolidation.md"],
        included_tests=["tests/test_v0329_external_observation_digestion_consolidation.py"],
        optional_integration_tests=["reference corpus integration skeleton disabled-by-default"],
    )
    audit = build_external_pipeline_consolidation_audit_trail(
        boundary_checks=["runtime flags false"],
        negative_runtime_checks=["no subprocess"],
    )

    assert gap_register.blocks_handoff is False
    assert blocking_gap_register.blocks_handoff is True
    assert set(DEFAULT_CONSOLIDATION_PROHIBITED_RUNTIME_SURFACES).issubset(set(risk_register.prohibited_runtime_surfaces))
    assert risk_register.proof_of_exploitability is False
    assert risk_register.mitigation_permission is False
    assert manifest.production_release is False
    assert manifest.release_flags.ready_for_execution is False
    assert all(getattr(audit, name) is True for name in audit.__dataclass_fields__ if name.endswith("_confirmed"))

    with pytest.raises(ValueError):
        ExternalPipelineRiskRegister(
            risk_register_id="risk:bad",
            version="v0.32.9",
            prohibited_runtime_surfaces=["external_harness_execution"],
        )
    with pytest.raises(ValueError):
        ExternalPipelineReleaseManifest(
            release_manifest_id="manifest:bad",
            version="v0.32.9",
            release_name="bad",
            snapshot_id="snapshot",
            included_versions=list(REQUIRED_V032_INCLUDED_VERSIONS),
            included_modules=[],
            included_docs=[],
            included_tests=[],
            optional_integration_tests=["reference corpus integration skeleton"],
            release_flags=flags,
            focused_test_command="py -m pytest tests/test_v0329_external_observation_digestion_consolidation.py",
            full_track_test_command="py -m pytest tests/test_v0329_external_observation_digestion_consolidation.py",
        )
    with pytest.raises(ValueError):
        ExternalPipelineConsolidationAuditTrail(
            audit_trail_id="audit:bad",
            version="v0.32.9",
            no_execution_confirmed=False,
        )


def test_v033_handoff_packet_is_design_stage_only():
    packet = build_v033_handoff_packet(
        "handoff:1",
        "snapshot:1",
        release_manifest_id="manifest:1",
        readiness_level=ExternalPipelineReadinessLevel.HANDOFF_READY_FOR_V033,
        ready_for_v033=True,
        profile_runtime_handoff_items=["reuse profile contracts"],
        read_only_tool_registry_handoff_items=["design safe registry only"],
        future_track_items=["runtime adapter loading remains later gate"],
    )

    assert set(DEFAULT_V033_FOCUS_ITEMS).issubset(set(packet.v033_focus_items))
    assert "v0.33" in packet.target_version_track
    assert set(DEFAULT_CONSOLIDATION_PROHIBITED_RUNTIME_SURFACES).issubset(set(packet.prohibited_until_later_gate))
    assert packet.ready_for_v033 is True
    assert v033_handoff_packet_is_design_stage_only(packet)
    assert packet.ready_for_execution is False
    assert packet.ready_for_read_only_tool_execution is False
    assert packet.ready_for_runtime_adapter_loading is False

    for flag_name in (
        "ready_for_execution",
        "ready_for_read_only_tool_execution",
        "ready_for_runtime_adapter_loading",
    ):
        with pytest.raises(ValueError):
            V033HandoffPacket(
                handoff_id=f"handoff:bad:{flag_name}",
                source_version="v0.32.9",
                target_version_track="v0.33 Internal General Agent Runtime MVP",
                source_snapshot_id="snapshot",
                **{flag_name: True},
            )
    with pytest.raises(ValueError):
        V033HandoffPacket(
            handoff_id="handoff:bad-target",
            source_version="v0.32.9",
            target_version_track="v0.34",
            source_snapshot_id="snapshot",
        )
    with pytest.raises(ValueError):
        V033HandoffPacket(
            handoff_id="handoff:bad-readiness",
            source_version="v0.32.9",
            target_version_track="v0.33 Internal General Agent Runtime MVP",
            source_snapshot_id="snapshot",
            readiness_level=ExternalPipelineReadinessLevel.NOT_READY,
            ready_for_v033=True,
        )
    with pytest.raises(ValueError):
        V033HandoffPacket(
            handoff_id="handoff:bad-gap",
            source_version="v0.32.9",
            target_version_track="v0.33 Internal General Agent Runtime MVP",
            source_snapshot_id="snapshot",
            ready_for_v033=True,
            metadata={"blocking_gaps": ["missing consolidation evidence"]},
        )


def test_v032_consolidation_report_and_v0328_interaction_keep_runtime_false():
    report = build_v032_consolidation_report(
        "report:1",
        "snapshot:1",
        "manifest:1",
        handoff_id="handoff:1",
        ready_for_v033=True,
        completed_items=["v0.32.0-v0.32.8 contract artifacts consolidated"],
        runtime_not_ready_items=["external harness execution", "read-only tool execution"],
    )
    readiness_0328 = build_v0328_readiness_report(
        "readiness:v0328",
        ready_for_v0329_external_observation_digestion_consolidation=True,
    )

    assert report.ready_for_v033 is True
    assert v032_consolidation_report_is_not_runtime_ready(report)
    assert report.runtime_enablement is False
    assert report.production_certification is False
    assert v0328_readiness_report_is_not_runtime_ready(readiness_0328)
    assert readiness_0328.ready_for_execution is False
    assert readiness_0328.ready_for_external_control is False
    assert readiness_0328.ready_for_authority_grant is False

    for flag_name in (
        "ready_for_execution",
        "ready_for_external_harness_execution",
        "ready_for_reference_code_execution",
        "ready_for_live_scan",
        "ready_for_read_only_tool_execution",
        "ready_for_runtime_adapter_loading",
        "ready_for_ocel_emission",
        "ready_for_ui_runtime",
        "ready_for_external_control",
        "ready_for_authority_grant",
    ):
        with pytest.raises(ValueError):
            V032ConsolidationReport(
                report_id=f"report:bad:{flag_name}",
                version="v0.32.9",
                release_name="bad",
                snapshot_id="snapshot",
                release_manifest_id="manifest",
                **{flag_name: True},
            )

    with pytest.raises(ValueError):
        V032ConsolidationReport(
            report_id="report:bad-blocking",
            version="v0.32.9",
            release_name="bad",
            snapshot_id="snapshot",
            release_manifest_id="manifest",
            ready_for_v033=True,
            blocked_items=["blocking consolidation gap"],
        )
    with pytest.raises(ValueError):
        V032ConsolidationReport(
            report_id="report:bad-metadata",
            version="v0.32.9",
            release_name="bad",
            snapshot_id="snapshot",
            release_manifest_id="manifest",
            metadata={"production_certification": True},
        )
