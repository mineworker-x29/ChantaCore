from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.workbench import PersonalRuntimeWorkbenchService
from chanta_core.utility.time import utc_now_iso


def record_object(store: OCELStore, object_type: str, object_id: str, attrs: dict) -> None:
    event = OCELEvent(
        event_id=f"evt:{object_id}",
        event_activity=f"{object_type}_seeded",
        event_timestamp=utc_now_iso(),
        event_attrs={"test_seed": True},
    )
    item = OCELObject(object_id=object_id, object_type=object_type, object_attrs={"object_key": object_id, "display_name": object_id, **attrs})
    relation = OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier="seeded_object")
    store.append_record(OCELRecord(event=event, objects=[item], relations=[relation]))


def build_workbench_store(tmp_path):
    store = OCELStore(tmp_path / "workbench.sqlite")
    record_object(store, "personal_prompt_activation_config", "personal_prompt_activation_config:demo", {"personal_directory_configured": True, "selected_mode_name": "operator_mode", "selected_profile_name": "default_profile", "runtime_kind": "local_runtime", "status": "active"})
    record_object(store, "personal_conformance_result", "personal_conformance_result:demo", {"status": "passed"})
    record_object(store, "personal_smoke_test_result", "personal_smoke_test_result:demo", {"status": "passed"})
    record_object(store, "skill_invocation_proposal", "skill_invocation_proposal:demo", {"proposal_id": "skill_invocation_proposal:demo", "proposal_status": "proposed", "review_required": True, "reason": "dummy proposal"})
    record_object(store, "skill_proposal_review_request", "skill_proposal_review_request:demo", {"review_request_id": "skill_proposal_review_request:demo", "status": "pending_review"})
    record_object(store, "execution_envelope", "execution_envelope:ok", {"envelope_id": "execution_envelope:ok", "skill_id": "skill:read_workspace_text_file", "status": "completed", "blocked": False, "execution_performed": True})
    record_object(store, "execution_envelope", "execution_envelope:block", {"envelope_id": "execution_envelope:block", "skill_id": "skill:read_workspace_text_file", "status": "failed", "blocked": True, "execution_performed": False})
    record_object(store, "execution_result_promotion_candidate", "execution_result_promotion_candidate:demo", {"candidate_id": "execution_result_promotion_candidate:demo", "candidate_title": "Promotion Candidate", "target_kind": "memory_candidate", "review_status": "pending_review", "source_ref": "C:\\private\\source.txt"})
    record_object(store, "workspace_read_summary_candidate", "workspace_read_summary_candidate:demo", {"summary_candidate_id": "workspace_read_summary_candidate:demo", "candidate_title": "Summary Candidate", "target_kind": "workspace_summary_candidate", "review_status": "pending_review"})
    return store


def test_status_works_without_personal_directory_configured(tmp_path, monkeypatch) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY", raising=False)
    service = PersonalRuntimeWorkbenchService(ocel_store=OCELStore(tmp_path / "empty.sqlite"))

    snapshot = service.build_snapshot()
    result = service.record_result(snapshot=snapshot, command_name="status")

    assert snapshot.personal_directory_configured is False
    assert result.status == "needs_review"
    assert any(finding.finding_type == "missing_personal_directory" for finding in service.last_findings)


def test_status_and_aggregation_with_dummy_data(tmp_path) -> None:
    service = PersonalRuntimeWorkbenchService(ocel_store=build_workbench_store(tmp_path))

    snapshot = service.build_snapshot()
    service.record_result(snapshot=snapshot, command_name="status")

    assert snapshot.personal_directory_configured is True
    assert snapshot.pending_proposal_count == 1
    assert snapshot.pending_review_count >= 1
    assert snapshot.recent_execution_count == 2
    assert snapshot.blocked_execution_count == 1
    assert snapshot.failed_execution_count == 1
    assert snapshot.promotion_candidate_count == 1
    assert snapshot.summary_candidate_count == 1


def test_renderers_redact_paths_and_show_sections(tmp_path) -> None:
    service = PersonalRuntimeWorkbenchService(ocel_store=build_workbench_store(tmp_path))
    snapshot = service.build_snapshot(show_paths=False)
    result = service.record_result(snapshot=snapshot, command_name="pending")

    assert "C:\\private\\source.txt" not in service.render_workbench_candidates(result)
    assert "pending_items" in service.render_workbench_pending(result)
    assert "recent_activities" in service.render_workbench_recent(result)
    assert "blocked=true" in service.render_workbench_blockers(result)
    assert "workspace_summary_candidate" in service.render_workbench_summaries(result)
    assert "conformance_status=passed" in service.render_workbench_health(result)
