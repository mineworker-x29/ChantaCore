from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.workspace.summary import WorkspaceReadSummarizationService


def test_workspace_read_summary_ocel_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "summary.sqlite")
    service = WorkspaceReadSummarizationService(ocel_store=store)

    result = service.summarize_markdown("# Title\n\n## Part\nBody")
    service.create_summary_candidate(result=result)

    assert store.fetch_objects_by_type("workspace_read_summary_policy")
    assert store.fetch_objects_by_type("workspace_read_summary_request")
    assert store.fetch_objects_by_type("workspace_read_summary_section")
    assert store.fetch_objects_by_type("workspace_read_summary_result")
    assert store.fetch_objects_by_type("workspace_read_summary_candidate")
    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    assert "workspace_read_summary_requested" in activities
    assert "workspace_read_summary_completed" in activities
    assert "workspace_read_summary_candidate_created" in activities


def test_workspace_read_summary_pig_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "summary.sqlite")
    service = WorkspaceReadSummarizationService(ocel_store=store)
    result = service.summarize_markdown("# Title\n")
    service.create_summary_candidate(result=result)
    tiny_policy = service.create_default_policy()
    tiny_policy = tiny_policy.__class__(**{**tiny_policy.to_dict(), "max_input_chars": 2})
    service.summarize_from_text(text="abcdef", input_kind="text", policy=tiny_policy)

    objects = []
    for object_type in [
        "workspace_read_summary_policy",
        "workspace_read_summary_request",
        "workspace_read_summary_section",
        "workspace_read_summary_result",
        "workspace_read_summary_candidate",
        "workspace_read_summary_finding",
    ]:
        for row in store.fetch_objects_by_type(object_type):
            objects.append(OCPXObjectView(row["object_id"], row["object_type"], row["object_attrs"]))
    summary = PIGReportService._workspace_read_summary({}, {}, OCPXProcessView("view:test", "test", None, [], objects))

    assert summary["workspace_read_summary_result_count"] == 2
    assert summary["workspace_read_summary_completed_count"] == 2
    assert summary["workspace_read_summary_candidate_pending_count"] == 1
    assert summary["workspace_read_summary_by_input_kind"]["markdown"] == 1
    assert summary["workspace_read_summary_finding_by_type"]["input_truncated"] == 1
