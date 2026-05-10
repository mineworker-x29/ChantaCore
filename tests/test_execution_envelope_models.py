from chanta_core.execution.models import (
    ExecutionArtifactRef,
    ExecutionEnvelope,
    ExecutionInputSnapshot,
    ExecutionOutcomeSummary,
    ExecutionOutputSnapshot,
    ExecutionProvenanceRecord,
)
from chanta_core.utility.time import utc_now_iso


def test_execution_envelope_models_to_dict() -> None:
    now = utc_now_iso()
    envelope = ExecutionEnvelope(
        envelope_id="execution_envelope:test",
        execution_kind="explicit_skill_invocation",
        execution_subject_id="explicit_skill_invocation_result:test",
        skill_id="skill:read_workspace_text_file",
        session_id="session:test",
        turn_id="turn:test",
        process_instance_id="process:test",
        status="completed",
        execution_allowed=True,
        execution_performed=True,
        blocked=False,
        started_at=now,
        completed_at=now,
        created_at=now,
    )
    provenance = ExecutionProvenanceRecord(
        provenance_id="execution_provenance_record:test",
        envelope_id=envelope.envelope_id,
        actor_type="test",
        actor_id="actor:test",
        runtime_kind="explicit_skill_invocation",
        invocation_mode="test",
        proposal_id=None,
        explicit_invocation_request_id="explicit_skill_invocation_request:test",
        explicit_invocation_result_id="explicit_skill_invocation_result:test",
        gate_request_id=None,
        gate_decision_id=None,
        gate_result_id=None,
        capability_decision_id=None,
        permission_request_id=None,
        permission_decision_id=None,
        session_permission_resolution_id=None,
        sandbox_ref_ids=[],
        risk_ref_ids=[],
        created_at=now,
    )
    input_snapshot = ExecutionInputSnapshot(
        input_snapshot_id="execution_input_snapshot:test",
        envelope_id=envelope.envelope_id,
        input_kind="explicit_skill_input",
        input_preview={"relative_path": "docs/example.txt"},
        input_hash="hash",
        redacted_fields=[],
        full_input_stored=False,
        created_at=now,
    )
    output_snapshot = ExecutionOutputSnapshot(
        output_snapshot_id="execution_output_snapshot:test",
        envelope_id=envelope.envelope_id,
        output_kind="explicit_skill_output",
        output_preview={"output_text": "preview"},
        output_hash="hash",
        output_ref="explicit_skill_invocation_result:test",
        truncated=False,
        redacted_fields=[],
        full_output_stored=False,
        created_at=now,
    )
    artifact = ExecutionArtifactRef(
        artifact_ref_id="execution_artifact_ref:test",
        envelope_id=envelope.envelope_id,
        artifact_kind="test",
        artifact_ref="artifact:test",
        artifact_hash="hash",
        artifact_preview={"artifact_ref": "artifact:test"},
        private=False,
        created_at=now,
    )
    summary = ExecutionOutcomeSummary(
        summary_id="execution_outcome_summary:test",
        envelope_id=envelope.envelope_id,
        status="completed",
        succeeded=True,
        blocked=False,
        failed=False,
        skipped=False,
        violation_ids=[],
        finding_ids=[],
        output_snapshot_id=output_snapshot.output_snapshot_id,
        reason=None,
        created_at=now,
    )

    assert envelope.to_dict()["status"] == "completed"
    assert provenance.to_dict()["explicit_invocation_result_id"] == "explicit_skill_invocation_result:test"
    assert input_snapshot.to_dict()["full_input_stored"] is False
    assert output_snapshot.to_dict()["full_output_stored"] is False
    assert artifact.to_dict()["private"] is False
    assert summary.to_dict()["succeeded"] is True
