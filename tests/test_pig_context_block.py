from chanta_core.context import ContextBudget, ContextCompactionPipeline
from chanta_core.pig.context import PIGContext


def make_pig_context(context_text: str = "Process Intelligence Context") -> PIGContext:
    return PIGContext(
        source="pig",
        scope="recent",
        process_instance_id="pi:1",
        session_id="session:1",
        activity_sequence=["a", "b"],
        event_activity_counts={"a": 1},
        object_type_counts={"session": 1},
        relation_coverage={},
        basic_variant={},
        performance_summary={},
        guide={},
        diagnostics=[{"x": 1}],
        recommendations=[{"y": 1}],
        context_text=context_text,
        pi_artifacts=[{"artifact_id": "a:1"}],
        conformance_report={"status": "ok"},
    )


def test_pig_context_to_context_block() -> None:
    block = make_pig_context().to_context_block()

    assert block.block_type == "pig_context"
    assert block.title == "Process Intelligence Context"
    assert block.block_attrs["activity_count"] == 2
    assert block.block_attrs["diagnostic_count"] == 1
    assert block.block_attrs["recommendation_count"] == 1
    assert block.block_attrs["has_conformance_report"] is True
    assert block.block_attrs["pi_artifact_count"] == 1


def test_pig_context_compaction_can_cap_long_context() -> None:
    block = make_pig_context("x" * 1000).to_context_block()
    budget = ContextBudget(max_pig_context_chars=160)

    result = ContextCompactionPipeline.default().run([block], budget)

    assert result.blocks[0].char_length <= 160
    assert result.blocks[0].was_truncated is True
