import subprocess
import sys
from dataclasses import replace

from chanta_core.deep_self_introspection import (
    CandidateMemoryBoundarySourceRef,
    CandidateMemoryBoundarySourceService,
    CandidateMemoryBoundaryTruthCheckService,
    CandidateStateInspector,
    MaterializationBoundaryDescriptor,
    MemoryBoundaryDescriptor,
    PersonaOverlayBoundaryDescriptor,
    PromotionBoundaryDescriptor,
    SelfCandidateMemoryBoundaryAwarenessService,
    SelfCandidateMemoryBoundaryRequest,
    SelfCapabilityRegistryAwarenessService,
)


def _ref(ref_id: str, ref_type: str = "candidate", status: str = "candidate_only", **evidence):
    evidence_payload = {
        "review_status": status,
        "canonical_promotion_enabled": False,
        "promoted": False,
        "materialized": False,
        "execution_enabled": False,
        "verification_ref": f"verification:{ref_id}",
    }
    evidence_payload.update(evidence)
    return CandidateMemoryBoundarySourceRef(
        ref_id=ref_id,
        ref_type=ref_type,
        object_type="surface_verification_report" if ref_type == "report" else "self_structure_summary_candidate",
        status=status,
        source_refs=[{"source": "test_owner", "read_only": True}],
        evidence_refs=[evidence_payload],
    )


def _service(refs=None):
    return SelfCandidateMemoryBoundaryAwarenessService(
        source_service=CandidateMemoryBoundarySourceService(source_refs=refs or [_ref("candidate:safe"), _ref("report:safe", "report", "report_only")])
    )


def _finding_types(report):
    return {item.finding_type for item in report.findings}


def test_candidate_memory_boundary_snapshot_builds_and_passes_for_safe_state() -> None:
    service = _service()
    snapshot = service.view_boundary()
    report = service.truth_check()

    assert snapshot.snapshot_id
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.source_refs
    assert snapshot.candidate_states
    assert snapshot.memory_boundary.boundary_id
    assert snapshot.persona_overlay_boundary.boundary_id
    assert snapshot.promotion_boundary.boundary_id
    assert snapshot.materialization_boundary.boundary_id
    assert report.status == "passed"
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False


def test_default_source_loads_candidate_report_and_projection_refs() -> None:
    snapshot = SelfCandidateMemoryBoundaryAwarenessService().view_boundary()
    ref_types = {item.ref_type for item in snapshot.source_refs}

    assert "candidate" in ref_types
    assert "report" in ref_types
    assert "projection_item" in ref_types


def test_candidate_state_descriptor_exposes_boundary_flags_and_counts() -> None:
    states = CandidateStateInspector().inspect([_ref("candidate:safe"), _ref("report:safe", "report", "report_only")])

    assert states
    candidate = next(item for item in states if item.candidate_only)
    report = next(item for item in states if item.report_only)
    assert candidate.review_status == "candidate_only"
    assert candidate.candidate_status == "candidate_only"
    assert candidate.canonical_promotion_enabled is False
    assert candidate.promoted is False
    assert candidate.materialized is False
    assert candidate.execution_enabled is False
    assert candidate.source_ref_count == 1
    assert candidate.evidence_ref_count == 1
    assert candidate.verification_ref_count == 1
    assert candidate.state_status == "ok"
    assert report.report_status == "report_only"


def test_memory_persona_promotion_and_materialization_boundaries_are_safe_by_default() -> None:
    snapshot = SelfCandidateMemoryBoundaryAwarenessService().view_boundary()

    assert snapshot.memory_boundary.memory_write_enabled is False
    assert snapshot.memory_boundary.memory_auto_promotion_enabled is False
    assert snapshot.memory_boundary.candidate_to_memory_relation_allowed is False
    assert snapshot.memory_boundary.candidate_memory_separation_required is True
    assert snapshot.persona_overlay_boundary.persona_mutation_enabled is False
    assert snapshot.persona_overlay_boundary.overlay_mutation_enabled is False
    assert snapshot.persona_overlay_boundary.candidate_to_persona_promotion_allowed is False
    assert snapshot.persona_overlay_boundary.candidate_to_overlay_promotion_allowed is False
    assert snapshot.persona_overlay_boundary.private_persona_material_exposure_allowed is False
    assert snapshot.persona_overlay_boundary.public_projection_only is True
    assert snapshot.promotion_boundary.canonical_promotion_enabled is False
    assert snapshot.promotion_boundary.auto_promotion_allowed is False
    assert snapshot.promotion_boundary.promotion_requires_explicit_operator_action is True
    assert snapshot.promotion_boundary.promotion_gate_status == "disabled"
    assert snapshot.materialization_boundary.materialization_enabled is False
    assert snapshot.materialization_boundary.todo_file_creation_allowed is False
    assert snapshot.materialization_boundary.task_queue_creation_allowed is False
    assert snapshot.materialization_boundary.scheduler_registration_allowed is False
    assert snapshot.materialization_boundary.file_artifact_creation_allowed is False


def test_truth_check_fails_for_promoted_materialized_executable_or_canonical_candidate() -> None:
    refs = [
        _ref("candidate:promoted", promoted=True),
        _ref("candidate:materialized", materialized=True),
        _ref("candidate:execution", execution_enabled=True),
        _ref("candidate:canonical", canonical_promotion_enabled=True),
    ]
    report = _service(refs).truth_check()
    findings = _finding_types(report)

    assert report.status == "failed"
    assert "candidate_promoted_violation" in findings
    assert "candidate_materialized_violation" in findings
    assert "candidate_execution_enabled_violation" in findings
    assert report.promoted_count == 1
    assert report.materialized_count == 1
    assert report.execution_enabled_count == 1


def test_truth_check_fails_for_memory_boundary_violations() -> None:
    service = _service()
    snapshot = service.view_boundary()
    bad_memory = replace(
        snapshot.memory_boundary,
        memory_write_enabled=True,
        memory_auto_promotion_enabled=True,
        candidate_memory_separation_required=False,
    )
    snapshot = replace(snapshot, memory_boundary=bad_memory)
    snapshot = replace(snapshot, findings=service.finding_service.evaluate(snapshot))
    report = CandidateMemoryBoundaryTruthCheckService().check_truth(snapshot)
    findings = _finding_types(report)

    assert report.status == "failed"
    assert "memory_write_enabled_violation" in findings
    assert "memory_auto_promotion_enabled_violation" in findings
    assert "candidate_memory_confusion" in findings


def test_truth_check_fails_for_persona_overlay_and_private_material_violations() -> None:
    service = _service()
    snapshot = service.view_boundary()
    bad_persona = replace(
        snapshot.persona_overlay_boundary,
        persona_mutation_enabled=True,
        overlay_mutation_enabled=True,
        candidate_to_persona_promotion_allowed=True,
        candidate_to_overlay_promotion_allowed=True,
        private_persona_material_exposure_allowed=True,
    )
    snapshot = replace(snapshot, persona_overlay_boundary=bad_persona)
    snapshot = replace(snapshot, findings=service.finding_service.evaluate(snapshot))
    report = CandidateMemoryBoundaryTruthCheckService().check_truth(snapshot)
    findings = _finding_types(report)

    assert report.status == "failed"
    assert "persona_mutation_enabled_violation" in findings
    assert "overlay_mutation_enabled_violation" in findings
    assert "candidate_to_persona_promotion_violation" in findings
    assert "candidate_to_overlay_promotion_violation" in findings
    assert "private_persona_material_exposure_risk" in findings


def test_truth_check_fails_for_promotion_and_materialization_boundaries() -> None:
    service = _service()
    snapshot = service.view_boundary()
    snapshot = replace(
        snapshot,
        promotion_boundary=replace(snapshot.promotion_boundary, canonical_promotion_enabled=True, auto_promotion_allowed=True),
        materialization_boundary=replace(
            snapshot.materialization_boundary,
            materialization_enabled=True,
            todo_file_creation_allowed=True,
            task_queue_creation_allowed=True,
            scheduler_registration_allowed=True,
            file_artifact_creation_allowed=True,
        ),
    )
    snapshot = replace(snapshot, findings=service.finding_service.evaluate(snapshot))
    report = CandidateMemoryBoundaryTruthCheckService().check_truth(snapshot)
    findings = _finding_types(report)

    assert report.status == "failed"
    assert "candidate_promoted_violation" in findings
    assert "candidate_materialized_violation" in findings


def test_candidate_memory_confusion_and_report_canonical_truth_are_detected() -> None:
    refs = [
        _ref("candidate:memory", status="memory"),
        _ref("candidate:canonical-memory", status="promoted"),
        _ref("report:canonical", "report", "report_only", canonical_truth=True),
        _ref("candidate:private-risk", private_persona_material_exposure_allowed=True),
    ]
    report = _service(refs).truth_check()
    findings = _finding_types(report)

    assert report.status == "failed"
    assert "candidate_memory_confusion" in findings
    assert "candidate_projected_as_canonical_memory" in findings
    assert "report_projected_as_canonical_truth" in findings
    assert "private_persona_material_exposure_risk" in findings
    assert report.memory_confusion_count >= 2


def test_missing_source_or_evidence_refs_are_warnings() -> None:
    bad_ref = CandidateMemoryBoundarySourceRef(
        ref_id="candidate:no-evidence",
        ref_type="candidate",
        object_type="self_structure_summary_candidate",
        status="candidate_only",
        source_refs=[],
        evidence_refs=[],
    )
    report = _service([bad_ref]).truth_check()

    assert report.status == "warning"
    assert "candidate_without_source_refs" in _finding_types(report)
    assert "candidate_without_evidence_refs" in _finding_types(report)


def test_candidate_boundary_skills_are_implemented_and_claim_consistency_is_implemented() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    records = {record.skill_id: record for record in snapshot.records if record.skill_id}

    assert records["skill:deep_self_candidate_memory_boundary_report"].status == "implemented"
    assert records["skill:deep_self_promotion_boundary_check"].status == "implemented"
    assert records["skill:deep_self_context_projection_view"].status == "implemented"
    assert records["skill:deep_self_claim_consistency_check"].status == "implemented"
    assert records["skill:deep_self_candidate_memory_boundary_report"].read_only is True
    assert records["skill:deep_self_promotion_boundary_check"].execution_enabled is False


def test_pig_and_ocpx_projection_build() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.21.6"
    assert pig["subject"] == "candidate_memory_boundary"
    assert "candidate is not memory" in pig["principles"]
    assert "report is not canonical truth" in pig["principles"]
    assert "projection is not promotion" in pig["principles"]
    assert "candidate creation is not materialization" in pig["principles"]
    assert pig["checks_candidate_status"] is True
    assert pig["checks_promotion_boundary"] is True
    assert pig["checks_materialization_boundary"] is True
    assert pig["checks_memory_boundary"] is True
    assert pig["checks_persona_overlay_boundary"] is True
    assert pig["promotes_candidate"] is False
    assert pig["mutates_memory"] is False
    assert pig["mutates_persona"] is False
    assert pig["mutates_overlay"] is False
    assert ocpx["state"] == "self_candidate_memory_boundary_awareness"
    assert "SelfCandidateMemoryBoundaryState" in ocpx["target_read_models"]
    assert "SelfCandidateMemoryConfusionState" in ocpx["target_read_models"]


def test_cli_candidate_memory_boundary_views_work() -> None:
    commands = [
        ["deep-self", "boundary", "candidate-memory"],
        ["deep-self", "boundary", "candidate-memory", "truth-check"],
        ["deep-self", "boundary", "candidate-memory", "--candidate-id", "candidate:self_awareness_summary"],
        ["deep-self", "boundary", "candidates"],
        ["deep-self", "boundary", "memory"],
        ["deep-self", "boundary", "promotion"],
        ["deep-self", "boundary", "materialization"],
        ["deep-self", "boundary", "persona-overlay"],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert result.returncode == 0
        assert "Self-Candidate/Memory Boundary Awareness" in result.stdout
        assert "No promotion performed." in result.stdout
        assert "No memory mutation performed." in result.stdout
        assert "raw_memory_content_printed=False" in result.stdout
        assert "raw_persona_private_material_printed=False" in result.stdout


def test_descriptor_types_exported() -> None:
    assert MemoryBoundaryDescriptor
    assert PersonaOverlayBoundaryDescriptor
    assert PromotionBoundaryDescriptor
    assert MaterializationBoundaryDescriptor
