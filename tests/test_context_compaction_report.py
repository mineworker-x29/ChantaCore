from chanta_core.context import (
    ContextBudget,
    ContextCompactionLayerResult,
    ContextCompactionReporter,
    ContextCompactionResult,
)


def test_compaction_report_builds_without_raw_content_dump() -> None:
    result = ContextCompactionResult(
        blocks=[],
        layer_results=[
            ContextCompactionLayerResult(
                layer_name="BudgetReductionLayer",
                blocks=[],
                changed=True,
                truncated_block_ids=["secret raw content should not appear"],
            ),
            ContextCompactionLayerResult(
                layer_name="AutoCompactLayer",
                blocks=[],
                changed=False,
                result_attrs={"disabled": True},
            ),
        ],
        total_chars=100,
        total_estimated_tokens=25,
        truncated_block_ids=["b:1"],
        result_attrs={"collapsed_block_count": 0},
    )

    report = ContextCompactionReporter().build_report(
        result,
        ContextBudget(max_total_chars=1000, reserve_chars=100),
    )

    assert report.status == "warning"
    assert "BudgetReductionLayer" in report.report_text
    assert "AutoCompact disabled: True" in report.report_text
    assert "AutoCompact recommended: False" in report.report_text
    assert "secret raw content should not appear" not in report.report_text
