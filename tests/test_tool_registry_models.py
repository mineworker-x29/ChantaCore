import pytest

from chanta_core.tool_registry import (
    ToolDescriptor,
    ToolPolicyNote,
    ToolRegistrySnapshot,
    ToolRiskAnnotation,
    hash_tool_snapshot,
    new_tool_descriptor_id,
    new_tool_policy_note_id,
    new_tool_registry_snapshot_id,
    new_tool_risk_annotation_id,
)
from chanta_core.tool_registry.errors import ToolPolicyNoteError


def test_tool_registry_models_to_dict_and_ids() -> None:
    descriptor = ToolDescriptor(
        tool_id=new_tool_descriptor_id(),
        tool_name="read_file",
        tool_type="builtin",
        description="Read a file",
        status="active",
        capability_tags=["read", "workspace"],
        input_schema_ref="schema:input",
        output_schema_ref="schema:output",
        execution_owner="core",
        source_kind="test",
        risk_level="read_only",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )
    snapshot = ToolRegistrySnapshot(
        snapshot_id=new_tool_registry_snapshot_id(),
        snapshot_name="test",
        created_at="2026-01-01T00:00:00Z",
        tool_ids=[descriptor.tool_id],
        source_kind="test",
        snapshot_hash=hash_tool_snapshot([descriptor.tool_id]),
    )
    note = ToolPolicyNote(
        policy_note_id=new_tool_policy_note_id(),
        tool_id=descriptor.tool_id,
        tool_name=descriptor.tool_name,
        note_type="review_needed",
        text="Review before future enforcement.",
        status="active",
        priority=10,
        source_kind="test",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )
    annotation = ToolRiskAnnotation(
        risk_annotation_id=new_tool_risk_annotation_id(),
        tool_id=descriptor.tool_id,
        risk_level="read_only",
        risk_category="read",
        rationale="Read only operation.",
        status="active",
        created_at="2026-01-01T00:00:00Z",
        updated_at="2026-01-01T00:00:00Z",
    )

    assert descriptor.to_dict()["tool_id"].startswith("tool_descriptor:")
    assert snapshot.to_dict()["snapshot_id"].startswith("tool_registry_snapshot:")
    assert note.to_dict()["policy_note_id"].startswith("tool_policy_note:")
    assert annotation.to_dict()["risk_annotation_id"].startswith("tool_risk_annotation:")
    assert hash_tool_snapshot(["b", "a"]) == hash_tool_snapshot(["a", "b"])


def test_forbidden_tool_policy_note_types_rejected() -> None:
    with pytest.raises(ToolPolicyNoteError):
        ToolPolicyNote(
            policy_note_id="tool_policy_note:test",
            tool_id=None,
            tool_name=None,
            note_type="allow",
            text="forbidden",
            status="active",
            priority=None,
            source_kind="test",
            created_at="2026-01-01T00:00:00Z",
            updated_at="2026-01-01T00:00:00Z",
        )
