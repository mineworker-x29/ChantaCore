from chanta_core.context import (
    AutoCompactPolicy,
    AutoCompactRequest,
    AutoCompactResult,
    ContextBudget,
    make_auto_compact_output_block,
    make_context_block,
)
from chanta_core.context.layers import AutoCompactLayer


class FakeSummarizer:
    def __init__(self) -> None:
        self.calls = 0

    def summarize(
        self,
        request: AutoCompactRequest,
        policy: AutoCompactPolicy,
    ) -> AutoCompactResult:
        self.calls += 1
        return AutoCompactResult(
            success=True,
            output_block=make_auto_compact_output_block(
                content="fake deterministic compact output",
                refs=request.refs,
            ),
            output_text="fake deterministic compact output",
            used_summarizer=True,
            result_attrs={"request_id": request.request_id},
        )


def block():
    return make_context_block(
        block_type="other",
        title="Block",
        content="content",
        priority=1,
        source="test",
        refs=[{"ref_id": "r:1"}],
    )


def test_disabled_layer_noop() -> None:
    summarizer = FakeSummarizer()

    result = AutoCompactLayer(summarizer=summarizer).apply([block()], ContextBudget())

    assert result.changed is False
    assert result.result_attrs["disabled"] is True
    assert summarizer.calls == 0


def test_enabled_but_llm_summarizer_not_allowed_does_not_run() -> None:
    summarizer = FakeSummarizer()

    result = AutoCompactLayer(
        policy=AutoCompactPolicy(enabled=True, allow_llm_summarizer=False),
        summarizer=summarizer,
    ).apply([block()], ContextBudget())

    assert result.changed is False
    assert "not allowed" in result.warnings[0]
    assert summarizer.calls == 0


def test_enabled_but_no_summarizer_does_not_run() -> None:
    result = AutoCompactLayer(
        policy=AutoCompactPolicy(enabled=True, allow_llm_summarizer=True),
    ).apply([block()], ContextBudget())

    assert result.changed is False
    assert "no summarizer" in result.warnings[0]


def test_fake_summarizer_runs_only_when_explicitly_enabled_and_allowed() -> None:
    summarizer = FakeSummarizer()

    result = AutoCompactLayer(
        policy=AutoCompactPolicy(enabled=True, allow_llm_summarizer=True),
        summarizer=summarizer,
    ).apply([block()], ContextBudget())

    assert result.changed is True
    assert summarizer.calls == 1
    assert result.result_attrs["used_summarizer"] is True
    assert result.blocks[0].content == "fake deterministic compact output"
