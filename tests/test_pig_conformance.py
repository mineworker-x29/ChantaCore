from chanta_core.ocpx.models import OCPXEventView, OCPXObjectView, OCPXProcessView
from chanta_core.pig.conformance import PIGConformanceService


def make_view(
    activities: list[str],
    *,
    object_types: list[str] | None = None,
    related: bool = True,
) -> OCPXProcessView:
    objects = [
        OCPXObjectView(
            object_id=f"{object_type}:test-{index}",
            object_type=object_type,
            object_attrs={},
        )
        for index, object_type in enumerate(object_types or ["process_instance"])
    ]
    related_objects = [
        {"object_id": item.object_id, "object_type": item.object_type, "object_attrs": {}}
        for item in objects
    ]
    return OCPXProcessView(
        view_id="ocpx_view:test",
        source="pytest",
        session_id="session:test",
        events=[
            OCPXEventView(
                event_id=f"evt:{index}",
                event_activity=activity,
                event_timestamp=f"2026-05-03T00:00:{index:02d}Z",
                related_objects=related_objects if related else [],
                event_attrs={"process_instance_id": "process_instance:test"},
            )
            for index, activity in enumerate(activities)
        ],
        objects=objects,
        view_attrs={"process_instance_id": "process_instance:test"},
    )


def issue_types(report) -> set[str]:
    return {issue.issue_type for issue in report.issues}


def test_conformant_success_path() -> None:
    view = make_view(
        [
            "start_process_instance",
            "start_process_run_loop",
            "decide_next_activity",
            "select_skill",
            "execute_skill",
            "observe_result",
            "record_outcome",
            "complete_process_instance",
        ],
        object_types=["process_instance", "outcome"],
    )

    report = PIGConformanceService().check_view(view)

    assert report.status == "conformant"
    assert report.summary["issue_count"] == 0
    assert report.report_attrs["diagnostic_only"] is True


def test_missing_outcome_is_warning() -> None:
    view = make_view(
        [
            "start_process_instance",
            "start_process_run_loop",
            "decide_next_activity",
            "select_skill",
            "execute_skill",
            "observe_result",
            "record_outcome",
            "complete_process_instance",
        ],
        object_types=["process_instance"],
    )

    report = PIGConformanceService().check_view(view)

    assert report.status == "warning"
    assert "missing_outcome" in issue_types(report)


def test_failure_path_with_error_object_is_conformant() -> None:
    view = make_view(
        [
            "start_process_run_loop",
            "decide_next_activity",
            "select_skill",
            "execute_skill",
            "fail_skill_execution",
            "observe_result",
            "fail_process_instance",
        ],
        object_types=["process_instance", "error"],
    )

    report = PIGConformanceService().check_view(view)

    assert report.status == "conformant"
    assert "missing_error_object" not in issue_types(report)


def test_missing_error_object_is_warning() -> None:
    view = make_view(
        ["start_process_run_loop", "fail_skill_execution", "fail_process_instance"],
        object_types=["process_instance"],
    )

    report = PIGConformanceService().check_view(view)

    assert report.status == "warning"
    assert "missing_error_object" in issue_types(report)


def test_order_sanity_warning() -> None:
    view = make_view(
        ["start_process_run_loop", "execute_skill", "select_skill", "observe_result"],
        object_types=["process_instance"],
    )

    report = PIGConformanceService().check_view(view)

    assert report.status == "warning"
    assert "invalid_success_path" in issue_types(report)


def test_relation_coverage_warning() -> None:
    view = make_view(["start_process_run_loop"], related=False)

    report = PIGConformanceService().check_view(view)

    assert report.status == "warning"
    assert "missing_relation" in issue_types(report)


def test_empty_view_status_unknown() -> None:
    view = make_view([], object_types=[])

    report = PIGConformanceService().check_view(view)

    assert report.status == "unknown"
    assert report.summary["issue_count"] == 1
