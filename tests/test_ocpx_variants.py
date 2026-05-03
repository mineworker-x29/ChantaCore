from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.models import OCPXEventView, OCPXObjectView, OCPXProcessView


def make_view(
    activities: list[str],
    *,
    process_instance_id: str = "process_instance:test",
    skill_id: str = "skill:echo",
) -> OCPXProcessView:
    return OCPXProcessView(
        view_id=f"view:{process_instance_id}",
        source="test",
        session_id="session-test",
        events=[
            OCPXEventView(
                event_id=f"evt:{index}",
                event_activity=activity,
                event_timestamp=f"2026-05-03T00:00:{index:02d}Z",
                related_objects=[],
                event_attrs={"skill_id": skill_id, "process_instance_id": process_instance_id},
            )
            for index, activity in enumerate(activities)
        ],
        objects=[
            OCPXObjectView(
                object_id=process_instance_id,
                object_type="process_instance",
                object_attrs={},
            ),
            OCPXObjectView(
                object_id=skill_id,
                object_type="skill",
                object_attrs={},
            ),
        ],
    )


def test_compute_variant_summary_from_activity_sequence() -> None:
    view = make_view(["start_process_run_loop", "complete_process_instance"])
    summary = OCPXEngine().compute_variant_summary(view)

    assert summary.variant_key == "start_process_run_loop>complete_process_instance"
    assert summary.trace_count == 1
    assert summary.success_count == 1
    assert summary.failure_count == 0
    assert summary.skill_ids == ["skill:echo"]
    assert summary.example_process_instance_ids == ["process_instance:test"]


def test_compute_variant_summary_failure_count() -> None:
    view = make_view(["start_process_run_loop", "fail_skill_execution"])
    summary = OCPXEngine().compute_variant_summary(view)

    assert summary.success_count == 0
    assert summary.failure_count == 1


def test_compute_variant_summaries_groups_identical_variants_deterministically() -> None:
    engine = OCPXEngine()
    view_a = make_view(
        ["start_process_run_loop", "complete_process_instance"],
        process_instance_id="process_instance:a",
    )
    view_b = make_view(
        ["start_process_run_loop", "complete_process_instance"],
        process_instance_id="process_instance:b",
    )
    view_c = make_view(
        ["start_process_run_loop", "fail_process_instance"],
        process_instance_id="process_instance:c",
    )

    summaries = engine.compute_variant_summaries([view_c, view_b, view_a])

    assert [item.variant_key for item in summaries] == sorted(
        item.variant_key for item in summaries
    )
    clean = summaries[0]
    assert clean.trace_count == 2
    assert clean.success_count == 2
    assert clean.failure_count == 0
    assert clean.example_process_instance_ids == [
        "process_instance:b",
        "process_instance:a",
    ]
