from chanta_core.hooks import HookDefinition, HookRegistry


def make_hook(hook_id: str, name: str, priority: int | None, status: str = "active") -> HookDefinition:
    return HookDefinition(
        hook_id=hook_id,
        hook_name=name,
        hook_type="observer",
        lifecycle_stage="pre_process_run",
        description=None,
        status=status,
        priority=priority,
        scope=None,
        source_kind="test",
        handler_ref="metadata.only",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )


def test_hook_registry_register_list_find_disable_clear() -> None:
    registry = HookRegistry()
    low = make_hook("hook_definition:low", "b-low", 1)
    high_b = make_hook("hook_definition:high-b", "b-high", 10)
    high_a = make_hook("hook_definition:high-a", "a-high", 10)
    none = make_hook("hook_definition:none", "none", None)

    registry.register(low)
    registry.register(high_b)
    registry.register(high_a)
    registry.register(none)

    assert registry.get_hook(low.hook_id) == low
    assert [hook.hook_id for hook in registry.list_hooks()] == [
        "hook_definition:high-a",
        "hook_definition:high-b",
        "hook_definition:low",
        "hook_definition:none",
    ]
    assert [hook.hook_id for hook in registry.find_by_stage("pre-process-run")] == [
        "hook_definition:high-a",
        "hook_definition:high-b",
        "hook_definition:low",
        "hook_definition:none",
    ]
    disabled = registry.disable_hook(low.hook_id)
    assert disabled is not None
    assert disabled.status == "disabled"

    registry.clear()
    assert registry.list_hooks() == []
