from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace.summary import (
    WorkspaceReadSummaryCandidate,
    WorkspaceReadSummaryFinding,
    WorkspaceReadSummaryPolicy,
    WorkspaceReadSummaryRequest,
    WorkspaceReadSummaryResult,
    WorkspaceReadSummarySection,
)


def test_workspace_read_summary_models_to_dict() -> None:
    now = utc_now_iso()
    policy = WorkspaceReadSummaryPolicy(
        policy_id="workspace_read_summary_policy:test",
        policy_name="Default",
        supported_input_kinds=["markdown"],
        max_input_chars=100,
        max_preview_chars=50,
        max_sections=5,
        max_section_preview_chars=20,
        allow_llm_summary=False,
        allow_private_summary=True,
        require_review_for_promotion=True,
        status="active",
        created_at=now,
    )
    request = WorkspaceReadSummaryRequest(
        summary_request_id="workspace_read_summary_request:test",
        envelope_id=None,
        output_snapshot_id=None,
        artifact_ref_id=None,
        source_kind="workspace_text",
        source_ref=None,
        input_kind="markdown",
        file_name="README.md",
        relative_path_redacted="<REDACTED_PATH>",
        requested_by="tester",
        session_id=None,
        turn_id=None,
        process_instance_id=None,
        created_at=now,
    )
    section = WorkspaceReadSummarySection(
        section_id="workspace_read_summary_section:test",
        summary_request_id=request.summary_request_id,
        section_type="markdown_heading",
        title="Title",
        level=1,
        order_index=0,
        preview="",
        char_count=7,
        line_start=1,
        line_end=1,
        created_at=now,
    )
    result = WorkspaceReadSummaryResult(
        summary_result_id="workspace_read_summary_result:test",
        summary_request_id=request.summary_request_id,
        status="completed",
        input_kind="markdown",
        summary_title="Title",
        summary_text="# Title",
        section_ids=[section.section_id],
        input_char_count=7,
        input_line_count=1,
        truncated=False,
        private=False,
        sensitive=False,
        finding_ids=[],
        created_at=now,
    )
    candidate = WorkspaceReadSummaryCandidate(
        summary_candidate_id="workspace_read_summary_candidate:test",
        summary_result_id=result.summary_result_id,
        envelope_id=None,
        target_kind="workspace_summary_candidate",
        candidate_title="Title",
        candidate_preview="# Title",
        candidate_hash="hash",
        review_status="pending_review",
        promotion_candidate_id=None,
        canonical_promotion_enabled=False,
        created_at=now,
    )
    finding = WorkspaceReadSummaryFinding(
        finding_id="workspace_read_summary_finding:test",
        summary_request_id=request.summary_request_id,
        summary_result_id=result.summary_result_id,
        finding_type="input_truncated",
        status="truncated",
        severity="medium",
        message="truncated",
        subject_ref=None,
        created_at=now,
    )

    assert policy.to_dict()["allow_llm_summary"] is False
    assert request.to_dict()["relative_path_redacted"] == "<REDACTED_PATH>"
    assert section.to_dict()["section_type"] == "markdown_heading"
    assert result.to_dict()["status"] == "completed"
    assert candidate.to_dict()["canonical_promotion_enabled"] is False
    assert finding.to_dict()["finding_type"] == "input_truncated"
