from pathlib import Path

from chanta_core.hooks import HookLifecycleService


def test_hooks_package_does_not_import_external_execution_surfaces() -> None:
    hooks_dir = Path("src/chanta_core/hooks")
    text = "\n".join(path.read_text(encoding="utf-8") for path in hooks_dir.glob("*.py"))

    assert "importlib" not in text
    assert "subprocess" not in text
    assert "requests" not in text
    assert "httpx" not in text
    assert "aiohttp" not in text
    assert "mcp" not in text.lower()
    assert "plugin" not in text.lower()


def test_hook_service_has_no_runtime_mutation_or_permission_methods() -> None:
    public_methods = {
        name
        for name in dir(HookLifecycleService)
        if not name.startswith("_") and callable(getattr(HookLifecycleService, name))
    }

    forbidden = {
        "permissionDecision",
        "block_tool",
        "rewrite_tool_input",
        "rewrite_tool_output",
        "mutate_input",
        "mutate_output",
    }
    assert public_methods.isdisjoint(forbidden)
