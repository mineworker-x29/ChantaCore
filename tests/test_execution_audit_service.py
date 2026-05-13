from chanta_core.execution.audit import ExecutionAuditService
from chanta_core.execution.envelope_service import ExecutionEnvelopeService
from chanta_core.ocel.store import OCELStore


def build_store(tmp_path):
    store = OCELStore(tmp_path / "audit.sqlite")
    envelope_service = ExecutionEnvelopeService(ocel_store=store)
    first = envelope_service.create_envelope(
        execution_kind="gated_skill_invocation",
        execution_subject_id="skill_execution_gate_result:one",
        skill_id="skill:read_workspace_text_file",
        session_id="session:alpha",
        turn_id="turn:one",
        process_instance_id="process:one",
        status="completed",
        execution_allowed=True,
        execution_performed=True,
        blocked=False,
    )
    envelope_service.record_input_snapshot(
        envelope=first,
        input_payload={
            "root_path": "C:\\example\\workspace",
            "relative_path": "note.md",
            "token": "sample-token",
        },
    )
    envelope_service.record_output_snapshot(
        envelope=first,
        output_payload={
            "content": "public-safe preview",
            "path": "C:\\example\\workspace\\note.md",
            "secret": "sample-secret",
        },
    )
    envelope_service.record_provenance(
        envelope=first,
        explicit_invocation_result_id="explicit_skill_invocation_result:one",
        gate_decision_id="skill_execution_gate_decision:one",
        gate_result_id="skill_execution_gate_result:one",
    )
    envelope_service.record_outcome_summary(envelope=first, output_snapshot_id=envelope_service.last_output_snapshot.output_snapshot_id)
    second = envelope_service.create_envelope(
        execution_kind="gated_skill_invocation",
        execution_subject_id="skill_execution_gate_result:two",
        skill_id="skill:list_workspace_files",
        session_id="session:beta",
        turn_id="turn:two",
        process_instance_id="process:two",
        status="blocked",
        execution_allowed=False,
        execution_performed=False,
        blocked=True,
    )
    envelope_service.record_input_snapshot(envelope=second, input_payload={"root_path": "C:\\example\\workspace"})
    envelope_service.record_provenance(
        envelope=second,
        gate_decision_id="skill_execution_gate_decision:two",
        gate_result_id="skill_execution_gate_result:two",
    )
    envelope_service.record_outcome_summary(envelope=second)
    third = envelope_service.create_envelope(
        execution_kind="explicit_skill_invocation",
        execution_subject_id="explicit_skill_invocation_result:three",
        skill_id="skill:summarize_workspace_markdown",
        session_id="session:alpha",
        turn_id="turn:three",
        process_instance_id="process:three",
        status="failed",
        execution_allowed=True,
        execution_performed=True,
        blocked=False,
    )
    envelope_service.record_input_snapshot(envelope=third, input_payload={"relative_path": "README.md"})
    envelope_service.record_outcome_summary(envelope=third)
    return store, first, second, third


def test_list_returns_recent_envelope_views(tmp_path) -> None:
    store, *_ = build_store(tmp_path)
    service = ExecutionAuditService(ocel_store=store)

    result = service.query_envelopes(limit=2)

    assert result.status == "completed"
    assert result.returned_count == 2
    assert len(service.last_record_views) == 2


def test_show_existing_and_missing_envelope(tmp_path) -> None:
    store, first, *_ = build_store(tmp_path)
    service = ExecutionAuditService(ocel_store=store)

    shown = service.show_envelope(first.envelope_id)
    missing = service.show_envelope("execution_envelope:missing")

    assert shown.status == "completed"
    assert service.last_record_views == []
    assert missing.status == "not_found"
    assert service.last_findings[0].finding_type == "envelope_not_found"


def test_filters_by_skill_session_blocked_failed_and_status(tmp_path) -> None:
    store, *_ = build_store(tmp_path)
    service = ExecutionAuditService(ocel_store=store)

    by_skill = service.query_envelopes(skill_id="skill:list_workspace_files")
    assert by_skill.matched_count == 1
    assert service.last_record_views[0].skill_id == "skill:list_workspace_files"

    by_session = service.query_envelopes(session_id="session:alpha")
    assert by_session.matched_count == 2

    blocked = service.query_envelopes(blocked=True)
    assert blocked.matched_count == 1
    assert service.last_record_views[0].blocked is True

    failed = service.query_envelopes(failed=True)
    assert failed.matched_count == 1
    assert service.last_record_views[0].status == "failed"

    by_status = service.query_envelopes(status="completed")
    assert by_status.matched_count == 1


def test_default_redacts_paths_and_hides_full_payloads(tmp_path) -> None:
    store, first, *_ = build_store(tmp_path)
    service = ExecutionAuditService(ocel_store=store)

    service.show_envelope(first.envelope_id)
    detail = service.render_audit_detail()
    view = service.last_record_views[0]

    assert "C:\\example\\workspace" not in detail
    assert "<REDACTED_PATH>" in detail
    assert view.input_preview["_full_payload"] == "<HIDDEN>"
    assert view.output_preview["_full_payload"] == "<HIDDEN>"
    assert view.input_preview["token"] == "<REDACTED>"
    assert view.output_preview["secret"] == "<REDACTED>"


def test_recent_and_audit_methods_work(tmp_path) -> None:
    store, *_ = build_store(tmp_path)
    service = ExecutionAuditService(ocel_store=store)

    recent = service.recent_envelopes(limit=1)
    audit = service.audit_envelopes()

    assert recent.status == "completed"
    assert recent.returned_count == 1
    assert audit.status == "completed"
    assert audit.matched_count == 3
