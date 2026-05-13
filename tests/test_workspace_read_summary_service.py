from chanta_core.workspace.summary import WorkspaceReadSummarizationService


def test_plain_text_bounded_preview_and_large_input_finding() -> None:
    service = WorkspaceReadSummarizationService()
    policy = service.create_default_policy()
    small = service.summarize_plain_text("one\ntwo\nthree", policy=policy)

    assert small.status == "completed"
    assert "Lines: 3" in small.summary_text
    assert service.last_sections[0].section_type == "text_preview"

    tiny_policy = service.create_default_policy()
    tiny_policy = tiny_policy.__class__(
        **{**tiny_policy.to_dict(), "max_input_chars": 5}
    )
    large = service.summarize_from_text(text="abcdefg", input_kind="text", policy=tiny_policy)

    assert large.truncated is True
    assert any(finding.finding_type == "input_truncated" for finding in service.last_findings)


def test_summary_candidate_is_pending_review() -> None:
    service = WorkspaceReadSummarizationService()
    result = service.summarize_plain_text("public-safe text")

    candidate = service.create_summary_candidate(result=result)

    assert candidate.review_status == "pending_review"
    assert candidate.canonical_promotion_enabled is False
    assert candidate.candidate_preview
