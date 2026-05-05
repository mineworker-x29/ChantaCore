from pathlib import Path

from chanta_core.tool_registry import ToolRegistryViewService


def test_tool_registry_package_has_no_enforcement_or_loading_surfaces() -> None:
    text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in Path("src/chanta_core/tool_registry").glob("*.py")
    )

    assert "PermissionGrant" not in text
    assert "allow_tool" not in text
    assert "deny_tool" not in text
    assert "ask_permission" not in text
    assert "grant_permission" not in text
    assert "block_tool" not in text
    assert "sandbox_tool" not in text
    assert "mutate_tool_input" not in text
    assert "mutate_tool_output" not in text
    assert "load_mcp_tools" not in text
    assert "load_plugins" not in text
    assert "markdown_as_tool_registry" not in text
    assert "sync_markdown_to_tools" not in text
    assert "import_tools_from_markdown" not in text


def test_tool_registry_service_public_api_is_view_oriented() -> None:
    public_methods = {
        name
        for name in dir(ToolRegistryViewService)
        if not name.startswith("_") and callable(getattr(ToolRegistryViewService, name))
    }

    assert "execute_tool" not in public_methods
    assert "register_runtime_tool" not in public_methods
    assert "enforce_policy" not in public_methods
