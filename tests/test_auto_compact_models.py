from chanta_core.context import (
    AutoCompactRequest,
    AutoCompactResult,
    make_context_block,
    new_auto_compact_request_id,
)


def test_auto_compact_request_to_dict() -> None:
    block = make_context_block(
        block_type="other",
        title="Block",
        content="content",
        priority=1,
        source="test",
    )
    request = AutoCompactRequest(
        request_id="auto_compact_request:1",
        blocks=[block],
        input_text="content",
        refs=[{"ref_id": "r:1"}],
        reason="test",
        request_attrs={"a": 1},
    )

    data = request.to_dict()

    assert data["request_id"] == "auto_compact_request:1"
    assert data["blocks"][0]["block_id"] == block.block_id
    assert data["refs"] == [{"ref_id": "r:1"}]


def test_auto_compact_result_to_dict() -> None:
    result = AutoCompactResult(
        success=False,
        output_block=None,
        output_text=None,
        used_summarizer=False,
        warnings=["blocked"],
        error="no summarizer",
        result_attrs={"safe": True},
    )

    data = result.to_dict()

    assert data["success"] is False
    assert data["used_summarizer"] is False
    assert data["warnings"] == ["blocked"]


def test_new_auto_compact_request_id_prefix() -> None:
    assert new_auto_compact_request_id().startswith("auto_compact_request:")
