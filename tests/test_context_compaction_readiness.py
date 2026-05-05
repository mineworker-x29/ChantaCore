from chanta_core.context import (
    ContextBudget,
    ContextCompactionLayerResult,
    ContextCompactionReadinessChecker,
    ContextCompactionResult,
)


def result(
    *,
    total_chars: int,
    truncated=None,
    dropped=None,
    warnings=None,
    collapsed_count: int = 0,
) -> ContextCompactionResult:
    return ContextCompactionResult(
        blocks=[],
        layer_results=[
            ContextCompactionLayerResult(
                layer_name="TestLayer",
                blocks=[],
                changed=False,
            )
        ],
        total_chars=total_chars,
        total_estimated_tokens=max(1, total_chars // 4),
        truncated_block_ids=truncated or [],
        dropped_block_ids=dropped or [],
        warnings=warnings or [],
        result_attrs={"collapsed_block_count": collapsed_count},
    )


def test_readiness_ok_status() -> None:
    readiness = ContextCompactionReadinessChecker().evaluate(
        result(total_chars=100),
        ContextBudget(max_total_chars=1000, reserve_chars=100),
    )

    assert readiness.status == "ok"
    assert readiness.auto_compact_recommended is False


def test_readiness_warning_status() -> None:
    readiness = ContextCompactionReadinessChecker().evaluate(
        result(total_chars=100, truncated=["b:1"]),
        ContextBudget(max_total_chars=1000, reserve_chars=100),
    )

    assert readiness.status == "warning"


def test_readiness_over_budget_recommends_auto_compact() -> None:
    readiness = ContextCompactionReadinessChecker().evaluate(
        result(total_chars=950),
        ContextBudget(max_total_chars=1000, reserve_chars=100),
    )

    assert readiness.status == "over_budget"
    assert readiness.remaining_over_budget is True
    assert readiness.auto_compact_recommended is True


def test_readiness_recommends_for_many_dropped_blocks() -> None:
    readiness = ContextCompactionReadinessChecker(dropped_recommend_threshold=2).evaluate(
        result(total_chars=100, dropped=["a", "b", "c"]),
        ContextBudget(max_total_chars=1000, reserve_chars=100),
    )

    assert readiness.status == "warning"
    assert readiness.auto_compact_recommended is True
