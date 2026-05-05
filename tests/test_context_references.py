from chanta_core.context import ContextReference, new_context_reference_id


def test_context_reference_to_dict() -> None:
    reference = ContextReference(
        ref_id="context_ref:1",
        ref_type="tool_result",
        source="tool",
        title="Tool Result",
        block_id="block:1",
        object_id="object:1",
        event_id="event:1",
        artifact_id=None,
        path=None,
        attrs={"priority": 10},
    )

    data = reference.to_dict()

    assert data["ref_id"] == "context_ref:1"
    assert data["ref_type"] == "tool_result"
    assert data["attrs"] == {"priority": 10}


def test_new_context_reference_id_prefix() -> None:
    assert new_context_reference_id().startswith("context_ref:")


def test_context_reference_does_not_store_raw_content() -> None:
    reference = ContextReference(
        ref_id="context_ref:2",
        ref_type="context_block",
        source="context",
        title="Collapsed",
        attrs={"content_length": 5000},
    )

    data = reference.to_dict()

    assert "content" not in data
    assert "raw_content" not in data["attrs"]
