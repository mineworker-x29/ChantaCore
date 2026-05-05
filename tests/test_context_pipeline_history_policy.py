from chanta_core.context import (
    ContextBudget,
    ContextCompactionPipeline,
    ContextHistoryPolicy,
    SessionContextPolicy,
)
from chanta_core.context.block import make_context_block


def test_pipeline_with_history_policy_runs_and_reports_snipped_history() -> None:
    blocks = [
        make_context_block(
            block_id="system",
            block_type="system",
            title="System",
            content="system",
            priority=100,
            source="runtime",
        ),
        make_context_block(
            block_id="old-history",
            block_type="history",
            title="History",
            content="old" + ("x" * 500),
            priority=1,
            source="chat",
            block_attrs={
                "is_history": True,
                "role": "assistant",
                "created_at": "2026-05-05T00:00:00Z",
                "session_id": "session:1",
                "process_instance_id": "pi:1",
            },
        ),
        make_context_block(
            block_id="user",
            block_type="user_request",
            title="User",
            content="current",
            priority=100,
            source="runtime",
        ),
    ]
    session_policy = SessionContextPolicy(
        session_id="session:1",
        process_instance_id="pi:1",
        history_policy=ContextHistoryPolicy(
            preserve_last_user_blocks=0,
            preserve_last_assistant_blocks=0,
            min_priority_to_keep=50,
        ),
    )

    result = ContextCompactionPipeline.default(
        session_context_policy=session_policy,
    ).run(blocks, ContextBudget(max_total_chars=200, reserve_chars=50))

    assert [layer.layer_name for layer in result.layer_results][1] == "SnipLayer"
    assert "old-history" in result.dropped_block_ids
    assert result.result_attrs["snipped_history_count"] == 1
    assert result.result_attrs["history_block_count_before"] == 1
    assert result.result_attrs["history_block_count_after"] == 0
