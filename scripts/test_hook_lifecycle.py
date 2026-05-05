from chanta_core.hooks import HookLifecycleService, HookRegistry
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    store = OCELStore("data/hooks/test_hook_lifecycle.sqlite")
    service = HookLifecycleService(
        trace_service=TraceService(ocel_store=store),
        registry=HookRegistry(),
    )
    hook = service.register_hook_definition(
        hook_name="Observe process run",
        hook_type="observer",
        lifecycle_stage="pre_process_run",
        description="Observability-only hook for v0.10.3 smoke test.",
        priority=10,
        source_kind="test",
        handler_ref="metadata.only",
    )
    policy = service.register_hook_policy(hook_id=hook.hook_id, policy_kind="observe_only")
    invocations = service.observe_lifecycle_point(
        lifecycle_stage="pre_process_run",
        session_id="session:hook-smoke",
        turn_id="conversation_turn:hook-smoke",
        process_instance_id="process_instance:hook-smoke",
        input_payload={"reason": "smoke"},
    )

    print(f"hook_id={hook.hook_id}")
    print(f"policy_id={policy.policy_id}")
    for invocation in invocations:
        print(f"invocation_id={invocation.invocation_id}")
    print("recent hook activities:")
    for event in store.fetch_recent_events(20):
        activity = event["event_activity"]
        if activity.startswith("hook_") or activity.endswith("_hook_invoked"):
            print(f"- {activity}")


if __name__ == "__main__":
    main()
