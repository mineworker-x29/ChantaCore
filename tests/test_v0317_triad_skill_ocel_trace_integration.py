from __future__ import annotations

import inspect

import pytest

from chanta_core.internal_triad import ocel_trace
from chanta_core.internal_triad.ocel_trace import (
    TriadOCELArtifactKind,
    TriadOCELArtifactMapping,
    TriadOCELArtifactRef,
    TriadOCELNoEmissionGuarantee,
    TriadOCELObjectRef,
    TriadOCELObjectTypeKind,
    TriadOCELRelationTypeKind,
    TriadOCELTraceCoverage,
    TriadOCELTraceCoverageStatus,
    TriadOCELTraceEmissionPreview,
    TriadOCELTraceEventKind,
    TriadOCELTraceEventSpec,
    TriadOCELTraceIntegrationReport,
    TriadOCELTraceObjectSpec,
    TriadOCELTracePlan,
    TriadOCELTracePlanStatus,
    TriadOCELTraceRelationSpec,
    V0317ReadinessReport,
    build_default_triad_ocel_event_specs,
    build_default_triad_ocel_object_specs,
    build_default_triad_ocel_relation_specs,
    build_triad_ocel_artifact_mapping,
    build_triad_ocel_artifact_ref,
    build_triad_ocel_event_spec,
    build_triad_ocel_no_emission_guarantee,
    build_triad_ocel_object_ref,
    build_triad_ocel_object_spec,
    build_triad_ocel_relation_spec,
    build_triad_ocel_trace_coverage,
    build_triad_ocel_trace_emission_preview,
    build_triad_ocel_trace_integration_report,
    build_triad_ocel_trace_plan,
    build_v0317_readiness_report,
    ocel_event_spec_preserves_no_emission,
    ocel_object_spec_preserves_no_persistence,
    ocel_relation_spec_preserves_no_persistence,
    ocel_trace_coverage_is_not_runtime_proof,
    ocel_trace_plan_preserves_no_emission,
    ocel_trace_report_is_not_runtime_ready,
)


def test_v0317_taxonomies_are_complete_and_contract_only() -> None:
    assert {kind.value for kind in TriadOCELTraceEventKind} == {
        "triad_skill_contract_created",
        "triad_skill_input_received",
        "triad_skill_result_recorded",
        "observation_skill_started",
        "observation_target_ref_recorded",
        "observation_artifact_ref_recorded",
        "observation_evidence_ref_recorded",
        "observation_finding_recorded",
        "observation_gap_recorded",
        "observation_risk_signal_recorded",
        "observation_report_created",
        "capability_map_created",
        "digestion_skill_started",
        "digestion_source_ref_recorded",
        "digestion_pattern_signal_recorded",
        "digestion_finding_recorded",
        "digestion_blocker_recorded",
        "digestion_route_decision_recorded",
        "internal_candidate_created",
        "internalization_plan_created",
        "dominion_skill_started",
        "dominion_boundary_signal_recorded",
        "dominion_governance_finding_recorded",
        "dominion_blocker_recorded",
        "dominion_route_decision_recorded",
        "dominion_target_recorded",
        "dominion_decision_recorded",
        "dominion_future_gate_recorded",
        "dominion_no_op_recorded",
        "triad_no_op_recorded",
        "triad_skill_blocked",
        "triad_skill_completed",
        "unknown",
    }
    assert {kind.value for kind in TriadOCELObjectTypeKind} >= {
        "triad_skill",
        "triad_skill_contract",
        "observation_report",
        "capability_map",
        "digestion_route_decision",
        "internal_candidate_set",
        "internalization_plan",
        "dominion_target",
        "dominion_decision",
        "future_gate_item",
        "no_op_decision",
        "unknown",
    }
    assert {kind.value for kind in TriadOCELRelationTypeKind} == {
        "consumes",
        "produces",
        "references",
        "derives_from",
        "maps_to",
        "classifies",
        "blocks",
        "routes_to",
        "requires",
        "prohibits",
        "supports",
        "evidences",
        "mitigates",
        "supersedes",
        "hands_off_to",
        "unknown",
    }
    assert {kind.value for kind in TriadOCELArtifactKind} >= {
        "triad_skill_contract",
        "triad_skill_input_envelope",
        "triad_skill_result_envelope",
        "observation_skill_output",
        "internal_observation_report",
        "internal_capability_map",
        "digestion_skill_output",
        "internal_candidate_set",
        "internalization_plan",
        "dominion_skill_output",
        "internal_dominion_target",
        "internal_dominion_decision",
        "readiness_report",
        "unknown",
    }
    assert {status.value for status in TriadOCELTracePlanStatus} == {
        "unknown",
        "draft",
        "plan_ready",
        "plan_ready_with_gaps",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert {status.value for status in TriadOCELTraceCoverageStatus} == {
        "unknown",
        "not_started",
        "partial",
        "covered",
        "covered_with_gaps",
        "blocked",
        "future_track",
        "no_op",
    }
    assert ocel_trace.triad_ocel_event_kind_emits(TriadOCELTraceEventKind.TRIAD_SKILL_COMPLETED) is False
    assert ocel_trace.triad_ocel_object_type_persists(TriadOCELObjectTypeKind.TRIAD_SKILL) is False
    assert ocel_trace.triad_ocel_relation_type_persists(TriadOCELRelationTypeKind.PRODUCES) is False


def _artifact_ref() -> TriadOCELArtifactRef:
    return build_triad_ocel_artifact_ref(
        "triad_ocel_artifact_ref:1",
        TriadOCELArtifactKind.INTERNAL_DOMINION_TARGET,
        "internal_dominion_target:1",
        version="v0.31.6",
        evidence_refs=["evidence:1"],
    )


def _object_ref() -> TriadOCELObjectRef:
    return build_triad_ocel_object_ref(
        "triad_ocel_object_ref:1",
        TriadOCELObjectTypeKind.DOMINION_TARGET,
        "internal_dominion_target:1",
        TriadOCELArtifactKind.INTERNAL_DOMINION_TARGET,
        source_artifact_id="internal_dominion_target:1",
    )


def test_refs_specs_mapping_plan_and_coverage_are_contract_only() -> None:
    artifact_ref = _artifact_ref()
    object_ref = _object_ref()
    event_spec = build_triad_ocel_event_spec(
        "triad_ocel_event_spec:dominion_target_recorded:v0.31.7",
        TriadOCELTraceEventKind.DOMINION_TARGET_RECORDED,
        "dominion_target_recorded",
        "Record the contract vocabulary for dominion target trace visibility.",
        required_object_types=[TriadOCELObjectTypeKind.DOMINION_TARGET],
        required_attributes=["artifact_ref"],
        source_artifact_kinds=[TriadOCELArtifactKind.INTERNAL_DOMINION_TARGET],
    )
    object_spec = build_triad_ocel_object_spec(
        "triad_ocel_object_spec:dominion_target:v0.31.7",
        TriadOCELObjectTypeKind.DOMINION_TARGET,
        "dominion_target",
        "Contract-only object vocabulary for dominion targets.",
        source_artifact_kinds=[TriadOCELArtifactKind.INTERNAL_DOMINION_TARGET],
    )
    relation_spec = build_triad_ocel_relation_spec(
        "triad_ocel_relation_spec:references:v0.31.7",
        TriadOCELRelationTypeKind.REFERENCES,
        TriadOCELObjectTypeKind.DOMINION_DECISION,
        TriadOCELObjectTypeKind.DOMINION_TARGET,
        "Contract-only relation vocabulary.",
    )
    mapping = build_triad_ocel_artifact_mapping(
        "triad_ocel_artifact_mapping:1",
        artifact_ref,
        object_refs=[object_ref],
        event_spec_ids=[event_spec.event_spec_id],
        relation_spec_ids=[relation_spec.relation_spec_id],
        mapping_notes=["mapping only"],
    )
    plan = build_triad_ocel_trace_plan(
        "triad_ocel_trace_plan:1",
        source_artifact_refs=[artifact_ref],
        object_specs=[object_spec],
        event_specs=[event_spec],
        relation_specs=[relation_spec],
        artifact_mappings=[mapping],
    )
    coverage = build_triad_ocel_trace_coverage(
        "triad_ocel_trace_coverage:1",
        plan.trace_plan_id,
        artifact_kinds_covered=[TriadOCELArtifactKind.INTERNAL_DOMINION_TARGET],
        event_kinds_covered=[TriadOCELTraceEventKind.DOMINION_TARGET_RECORDED],
        object_types_covered=[TriadOCELObjectTypeKind.DOMINION_TARGET],
        relation_types_covered=[TriadOCELRelationTypeKind.REFERENCES],
        non_blocking_gaps=["runtime emission remains later-gated"],
    )

    assert artifact_ref.mutates_artifact is False
    assert object_ref.persisted_object is False
    assert isinstance(event_spec, TriadOCELTraceEventSpec)
    assert event_spec.emits_runtime_event is False
    assert event_spec.is_emitted_event is False
    assert ocel_event_spec_preserves_no_emission(event_spec) is True
    assert isinstance(object_spec, TriadOCELTraceObjectSpec)
    assert object_spec.persists_runtime_object is False
    assert ocel_object_spec_preserves_no_persistence(object_spec) is True
    assert isinstance(relation_spec, TriadOCELTraceRelationSpec)
    assert relation_spec.persists_runtime_relation is False
    assert ocel_relation_spec_preserves_no_persistence(relation_spec) is True
    assert isinstance(mapping, TriadOCELArtifactMapping)
    assert mapping.emits_runtime_events is False
    assert mapping.persists_runtime_objects is False
    assert mapping.mutates_artifact is False
    assert isinstance(plan, TriadOCELTracePlan)
    assert plan.ready_for_ocel_emission is False
    assert plan.ready_for_runtime_trace_persistence is False
    assert plan.ready_for_execution is False
    assert ocel_trace_plan_preserves_no_emission(plan) is True
    assert isinstance(coverage, TriadOCELTraceCoverage)
    assert coverage.ready_for_ocel_emission is False
    assert coverage.runtime_completeness_proof is False
    assert ocel_trace_coverage_is_not_runtime_proof(coverage) is True


def test_preview_guarantee_report_and_readiness_are_not_runtime_ready() -> None:
    plan = build_triad_ocel_trace_plan("triad_ocel_trace_plan:2")
    coverage = build_triad_ocel_trace_coverage("triad_ocel_trace_coverage:2", plan.trace_plan_id)
    preview = build_triad_ocel_trace_emission_preview("triad_ocel_emission_preview:1", plan.trace_plan_id)
    guarantee = build_triad_ocel_no_emission_guarantee("triad_ocel_no_emission_guarantee:1")
    report = build_triad_ocel_trace_integration_report("triad_ocel_trace_integration_report:1", plan, coverage)
    readiness = build_v0317_readiness_report(report)

    assert isinstance(preview, TriadOCELTraceEmissionPreview)
    assert preview.no_ocel_event_emission_guarantee is True
    assert preview.no_runtime_persistence_guarantee is True
    assert preview.no_log_write_guarantee is True
    assert preview.no_registry_mutation_guarantee is True
    assert preview.no_memory_mutation_guarantee is True
    assert preview.emits_preview is False
    assert isinstance(guarantee, TriadOCELNoEmissionGuarantee)
    assert guarantee.no_ocel_event_emission is True
    assert guarantee.no_ocel_object_persistence is True
    assert guarantee.no_ocel_relation_persistence is True
    assert guarantee.no_runtime_trace_write is True
    assert guarantee.no_log_write is True
    assert guarantee.no_database_write is True
    assert guarantee.no_registry_mutation is True
    assert guarantee.no_memory_mutation is True
    assert guarantee.runtime_enforcement is False
    assert isinstance(report, TriadOCELTraceIntegrationReport)
    assert report.ready_for_ocel_emission is False
    assert report.ready_for_runtime_trace_persistence is False
    assert report.ready_for_execution is False
    assert report.runtime_trace_integration is False
    assert ocel_trace_report_is_not_runtime_ready(report) is True
    assert isinstance(readiness, V0317ReadinessReport)
    assert readiness.ready_for_ocel_emission is False
    assert readiness.ready_for_runtime_trace_persistence is False
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_skill_activation is False
    assert readiness.runtime_enablement is False


def test_v0317_negative_runtime_flags_are_rejected() -> None:
    with pytest.raises(ValueError, match="emits_runtime_event"):
        TriadOCELTraceEventSpec("event:bad", TriadOCELTraceEventKind.UNKNOWN, "event", "description", emits_runtime_event=True)
    with pytest.raises(ValueError, match="persists_runtime_object"):
        TriadOCELTraceObjectSpec("object:bad", TriadOCELObjectTypeKind.UNKNOWN, "object", "description", persists_runtime_object=True)
    with pytest.raises(ValueError, match="persists_runtime_relation"):
        TriadOCELTraceRelationSpec(
            "relation:bad",
            TriadOCELRelationTypeKind.UNKNOWN,
            TriadOCELObjectTypeKind.UNKNOWN,
            TriadOCELObjectTypeKind.UNKNOWN,
            "description",
            persists_runtime_relation=True,
        )
    with pytest.raises(ValueError, match="ready_for_ocel_emission"):
        TriadOCELTracePlan("plan:bad", "v0.31.7", ready_for_ocel_emission=True)
    with pytest.raises(ValueError, match="ready_for_runtime_trace_persistence"):
        TriadOCELTracePlan("plan:bad", "v0.31.7", ready_for_runtime_trace_persistence=True)
    with pytest.raises(ValueError, match="no_ocel_event_emission_guarantee"):
        TriadOCELTraceEmissionPreview("preview:bad", "plan:bad", no_ocel_event_emission_guarantee=False)
    with pytest.raises(ValueError, match="no_ocel_event_emission"):
        TriadOCELNoEmissionGuarantee("guarantee:bad", "v0.31.7", no_ocel_event_emission=False)
    with pytest.raises(ValueError, match="ready_for_execution"):
        TriadOCELTraceIntegrationReport(
            "report:bad",
            "v0.31.7",
            "plan:bad",
            None,
            "summary",
            TriadOCELTracePlanStatus.PLAN_READY,
            0,
            0,
            0,
            0,
            ready_for_execution=True,
        )


def test_default_builders_and_helpers_are_pure_conservative() -> None:
    assert build_default_triad_ocel_event_specs()
    assert build_default_triad_ocel_object_specs()
    assert build_default_triad_ocel_relation_specs()

    helpers = [
        build_triad_ocel_object_ref,
        build_triad_ocel_artifact_ref,
        build_triad_ocel_event_spec,
        build_triad_ocel_object_spec,
        build_triad_ocel_relation_spec,
        build_triad_ocel_artifact_mapping,
        build_default_triad_ocel_event_specs,
        build_default_triad_ocel_object_specs,
        build_default_triad_ocel_relation_specs,
        build_triad_ocel_trace_plan,
        build_triad_ocel_trace_coverage,
        build_triad_ocel_trace_emission_preview,
        build_triad_ocel_no_emission_guarantee,
        build_triad_ocel_trace_integration_report,
        build_v0317_readiness_report,
        ocel_event_spec_preserves_no_emission,
        ocel_object_spec_preserves_no_persistence,
        ocel_relation_spec_preserves_no_persistence,
        ocel_trace_plan_preserves_no_emission,
        ocel_trace_coverage_is_not_runtime_proof,
        ocel_trace_report_is_not_runtime_ready,
    ]
    for helper in helpers:
        source = inspect.getsource(helper)
        assert "ready_for_ocel_emission=True" not in source
        assert "ready_for_runtime_trace_persistence=True" not in source
        assert "ready_for_execution=True" not in source
        assert "emits_runtime_event=True" not in source
        assert "persists_runtime_object=True" not in source
        assert "persists_runtime_relation=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source
