import pytest

from chanta_core.hooks import HookLifecycleService, HookRegistry
from chanta_core.hooks.errors import HookPolicyError
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_hook_lifecycle_service_records_lifecycle_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "hooks.sqlite")
    service = HookLifecycleService(
        trace_service=TraceService(ocel_store=store),
        registry=HookRegistry(),
    )
    hook = service.register_hook_definition(
        hook_name="Observe process",
        hook_type="observer",
        lifecycle_stage="pre_process_run",
        priority=10,
        handler_ref="not.executed",
        source_kind="test",
    )
    policy = service.register_hook_policy(hook_id=hook.hook_id)
    matches = service.match_hooks(
        lifecycle_stage="pre_process_run",
        session_id="session:test",
        turn_id="conversation_turn:test",
        process_instance_id="process_instance:test",
    )
    invocation = service.record_hook_invocation(
        hook=hook,
        input_payload={"process_instance_id": "process_instance:test"},
        session_id="session:test",
        turn_id="conversation_turn:test",
        process_instance_id="process_instance:test",
    )
    result = service.complete_hook_invocation(invocation=invocation)
    failed = service.fail_hook_invocation(invocation=invocation, error_message="observed failure")
    skipped = service.skip_hook_invocation(hook=hook, reason="test")
    observed = service.observe_lifecycle_point(
        lifecycle_stage="pre_process_run",
        input_payload={"noop": True},
    )

    activities = [event["event_activity"] for event in store.fetch_recent_events(50)]

    assert policy.policy_kind == "observe_only"
    assert matches == [hook]
    assert result.result_kind == "observed"
    assert failed.result_kind == "failed"
    assert skipped.result_kind == "skipped"
    assert len(observed) == 1
    assert "hook_definition_registered" in activities
    assert "hook_policy_registered" in activities
    assert "hook_matched" in activities
    assert "hook_invoked" in activities
    assert "pre_process_run_hook_invoked" in activities
    assert "hook_completed" in activities
    assert "hook_failed" in activities
    assert "hook_skipped" in activities
    assert "hook_result_recorded" in activities
    assert store.fetch_objects_by_type("hook_definition")
    assert store.fetch_objects_by_type("hook_invocation")
    assert store.fetch_objects_by_type("hook_result")
    assert store.fetch_objects_by_type("hook_policy")


def test_hook_lifecycle_service_does_not_execute_handler_ref_or_policy_enforcement(tmp_path) -> None:
    store = OCELStore(tmp_path / "hooks_noexec.sqlite")
    service = HookLifecycleService(trace_service=TraceService(ocel_store=store))
    hook = service.register_hook_definition(
        hook_name="Metadata only",
        hook_type="observer",
        lifecycle_stage="pre_tool_dispatch",
        handler_ref="module.that.must.not.be.imported",
    )

    invocations = service.observe_lifecycle_point(
        lifecycle_stage="pre_tool_dispatch",
        input_payload={"tool_id": "tool:test", "operation": "read"},
    )

    assert invocations[0].hook_id == hook.hook_id
    with pytest.raises(HookPolicyError):
        service.register_hook_policy(hook_id=hook.hook_id, policy_kind="block")
