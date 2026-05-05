from chanta_core.hooks import HookLifecycleService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_hook_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "hook_shape.sqlite")
    service = HookLifecycleService(trace_service=TraceService(ocel_store=store))

    hook = service.register_hook_definition(
        hook_name="Shape",
        hook_type="diagnostic",
        lifecycle_stage="post_process_run",
    )
    service.register_hook_policy(hook_id=hook.hook_id, policy_kind="log_only")
    service.observe_lifecycle_point(
        lifecycle_stage="post_process_run",
        session_id="session:shape",
        turn_id="conversation_turn:shape",
        process_instance_id="process_instance:shape",
        input_payload={"ok": True},
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    object_types = {
        "hook_definition": store.fetch_objects_by_type("hook_definition"),
        "hook_invocation": store.fetch_objects_by_type("hook_invocation"),
        "hook_result": store.fetch_objects_by_type("hook_result"),
        "hook_policy": store.fetch_objects_by_type("hook_policy"),
    }

    assert {
        "hook_definition_registered",
        "hook_policy_registered",
        "hook_matched",
        "hook_invoked",
        "post_process_run_hook_invoked",
        "hook_completed",
        "hook_result_recorded",
    }.issubset(activities)
    assert all(object_types.values())
    invocation = object_types["hook_invocation"][0]["object_attrs"]
    assert invocation["lifecycle_stage"] == "post_process_run"
    assert invocation["hook_id"] == hook.hook_id
    assert invocation["process_instance_id"] == "process_instance:shape"
