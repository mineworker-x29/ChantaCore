from chanta_core.context import (
    AutoCompactPolicy,
    AutoCompactRequest,
    AutoCompactResult,
    ContextBudget,
    ContextCompactionPipeline,
    ContextCompactionReporter,
    make_auto_compact_output_block,
    make_context_block,
)
from chanta_core.context.layers import AutoCompactLayer


class FakeSummarizer:
    def summarize(
        self,
        request: AutoCompactRequest,
        policy: AutoCompactPolicy,
    ) -> AutoCompactResult:
        return AutoCompactResult(
            success=True,
            output_block=make_auto_compact_output_block(
                content="fake compact output",
                refs=request.refs,
            ),
            output_text="fake compact output",
            used_summarizer=True,
            result_attrs={"request_id": request.request_id},
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
            block_type="user_request",
            title="User",
            content="hello",
            priority=100,
            source="script",
        ),
    ]
    budget = ContextBudget()
    result = ContextCompactionPipeline.default().run(blocks, budget)
    auto_layer = result.layer_results[-1]
    print(f"default_autocompact_disabled={auto_layer.result_attrs.get('disabled')}")
    print(f"default_used_summarizer={auto_layer.result_attrs.get('used_summarizer')}")

    fake_result = AutoCompactLayer(
        policy=AutoCompactPolicy(enabled=True, allow_llm_summarizer=True),
        summarizer=FakeSummarizer(),
    ).apply(blocks, budget)
    print(f"fake_autocompact_changed={fake_result.changed}")
    print(f"fake_used_summarizer={fake_result.result_attrs.get('used_summarizer')}")

    report = ContextCompactionReporter().build_report(result, budget)
    print("--- report ---")
    print(report.report_text)


if __name__ == "__main__":
    main()
