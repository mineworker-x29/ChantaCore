from chanta_core.tool_registry import (
    ToolDescriptor,
    ToolPolicyNote,
    ToolRegistrySnapshot,
    ToolRiskAnnotation,
    hash_tool_snapshot,
    render_tool_policy_view,
    render_tools_view,
)


def sample_tool(name: str = "read_file") -> ToolDescriptor:
    return ToolDescriptor(
        tool_id=f"tool_descriptor:{name}",
        tool_name=name,
        tool_type="builtin",
        description=f"{name} description",
        status="active",
        capability_tags=["read"],
        input_schema_ref="input",
        output_schema_ref="output",
        execution_owner="core",
        source_kind="test",
        risk_level="read_only",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )


def test_render_tools_view_contains_warning_and_tool_details() -> None:
    tool = sample_tool()
    snapshot = ToolRegistrySnapshot(
        snapshot_id="tool_registry_snapshot:test",
        snapshot_name="test",
        created_at="2026-01-01T00:00:00Z",
        tool_ids=[tool.tool_id],
        source_kind="test",
        snapshot_hash=hash_tool_snapshot([tool.tool_id]),
    )

    view = render_tools_view(tools=[tool], snapshot=snapshot, target_path=".chanta/TOOLS.md")

    assert view.canonical is False
    assert "Generated materialized view" in view.content
    assert "Canonical source: OCEL" in view.content
    assert "not the canonical tool registry" in view.content
    assert "do not change runtime tool availability" in view.content
    assert tool.tool_id in view.content
    assert tool.tool_name in view.content
    assert "read_only" in view.content


def test_render_tool_policy_view_contains_non_permission_warning_notes_and_risks() -> None:
    tool = sample_tool()
    note = ToolPolicyNote(
        policy_note_id="tool_policy_note:test",
        tool_id=tool.tool_id,
        tool_name=tool.tool_name,
        note_type="review_needed",
        text="Review this tool.",
        status="active",
        priority=5,
        source_kind="test",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )
    annotation = ToolRiskAnnotation(
        risk_annotation_id="tool_risk_annotation:test",
        tool_id=tool.tool_id,
        risk_level="read_only",
        risk_category="read",
        rationale="Read-only",
        status="active",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )

    view = render_tool_policy_view(
        tools=[tool],
        policy_notes=[note],
        risk_annotations=[annotation],
        target_path=".chanta/TOOL_POLICY.md",
    )

    assert view.canonical is False
    assert "not PermissionPolicy" in view.content
    assert "does not grant, deny, allow, ask, block, or sandbox" in view.content
    assert "v0.12.x" in view.content
    assert note.policy_note_id in view.content
    assert annotation.risk_annotation_id in view.content


def test_tool_registry_rendering_is_deterministic_except_generated_metadata() -> None:
    first = render_tools_view(tools=[sample_tool()], snapshot=None, target_path=".chanta/TOOLS.md")
    second = render_tools_view(tools=[sample_tool()], snapshot=None, target_path=".chanta/TOOLS.md")

    assert "read_file" in first.content
    assert first.content.replace(first.view_id, "VIEW").replace(first.generated_at, "TIME").replace(first.content_hash, "HASH") == second.content.replace(second.view_id, "VIEW").replace(second.generated_at, "TIME").replace(second.content_hash, "HASH")
