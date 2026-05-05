from chanta_core.context import (
    ContextBudget,
    ContextCompactionPipeline,
    ContextCompactionReporter,
    make_context_block,
)


def main() -> None:
    blocks = [
        make_context_block(
            block_type="system",
            title="System",
            content="system",
            priority=100,
            source="script",
        ),
        make_context_block(
            block_type="tool_result",
            title="Tool",
            content="x" * 2000,
            priority=10,
            source="tool",
        ),
        make_context_block(
            block_type="user_request",
            title="User",
            content="hello",
            priority=100,
            source="script",
        ),
    ]
    budget = ContextBudget(max_total_chars=900, reserve_chars=100)
    result = ContextCompactionPipeline.default().run(blocks, budget)
    report = ContextCompactionReporter().build_report(result, budget)
    print(report.report_text)


if __name__ == "__main__":
    main()
