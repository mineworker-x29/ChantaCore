from chanta_core.context import ContextBudget, MicrocompactPolicy, make_context_block
from chanta_core.context.layers import MicrocompactLayer


def block(block_type: str, content: str, attrs=None):
    return make_context_block(
        block_type=block_type,
        title=f"{block_type} block",
        content=content,
        priority=50,
        source="test",
        refs=[{"ref_type": "test", "ref_id": block_type}],
        block_attrs=attrs or {},
    )


def test_microcompact_layer_handles_structured_block_types() -> None:
    blocks = [
        block(
            "pig_context",
            "\n".join(f"pig line {index}" for index in range(80)),
            {
                "activity_sequence": [f"a{index}" for index in range(60)],
                "diagnostic_count": 3,
                "recommendation_count": 2,
                "pi_artifact_count": 1,
                "conformance_status": "ok",
                "scope": "recent",
            },
        ),
        block(
            "pig_report",
            "\n".join(["# Report"] + [f"line {index}" for index in range(80)]),
        ),
        block("tool_result", '{"z": [1, 2, 3], "a": {"nested": true}}'),
        block(
            "decision",
            "\n".join(f"score-{index}: {index}" for index in range(80)),
            {"selected_skill_id": "skill:llm_chat", "decision_mode": "fallback"},
        ),
        block("workspace", "\n".join(f"file-{index}.py" for index in range(80))),
        block("repo", "\n".join(f"match-{index}" for index in range(80))),
    ]
    layer = MicrocompactLayer(policy=MicrocompactPolicy(max_lines=20, max_report_chars=800))

    result = layer.apply(blocks, ContextBudget(max_block_chars=900))

    assert result.changed is True
    assert result.result_attrs["microcompacted_block_count"] >= 5
    assert result.result_attrs["block_type_counts"]["pig_context"] == 1
    for compacted in result.blocks:
        assert compacted.refs == [{"ref_type": "test", "ref_id": compacted.block_type}]
        assert compacted.block_attrs["microcompacted"] is True
    assert "Activity sequence:" in result.blocks[0].content
    assert "activities omitted" in result.blocks[0].content


def test_microcompact_layer_preserves_attrs_and_reports_truncated_ids() -> None:
    source = block("tool_result", "x" * 800, {"tool_id": "tool:repo"})

    result = MicrocompactLayer().apply([source], ContextBudget())

    assert result.blocks[0].block_attrs["tool_id"] == "tool:repo"
    assert result.blocks[0].block_attrs["microcompacted"] is True
    assert result.truncated_block_ids == [source.block_id]
