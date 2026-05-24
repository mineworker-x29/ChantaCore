from __future__ import annotations

from pathlib import Path

from chanta_core.self_modification_safety import (
    PatchDraftCreateRequest,
    PatchDraftSourceService,
    SelfModificationDiffPreviewService,
    SelfModificationRequestCandidateService,
    SelfModificationRequestCreateRequest,
)


DOC_FILE = Path("docs/versions/v0.22/v0.22.2_patch_draft_diff_preview.md")


def test_docs_define_patch_draft_diff_preview_boundary() -> None:
    text = DOC_FILE.read_text(encoding="utf-8")

    assert "Patch Draft / Diff Preview" in text
    assert "Patch draft is not patch apply." in text
    assert "Diff preview is not file mutation." in text
    assert "Diff preview is not dry-run." in text
    assert "Preview-created does not mean safety-checked." in text
    assert "v0.22.3 Patch Static Safety Check" in text
    assert "Implemented File List" in text
    assert "Restore Procedure" in text
    assert "Restore Checklist" in text


def test_patch_draft_outputs_are_sanitized_and_do_not_expose_full_paths() -> None:
    candidate_result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    assert candidate_result.patch_candidate is not None
    candidate = candidate_result.patch_candidate
    result = SelfModificationDiffPreviewService(
        source_service=PatchDraftSourceService({candidate.candidate_id: candidate})
    ).create_patch_draft_and_preview(
        PatchDraftCreateRequest(
            patch_candidate_id=candidate.candidate_id,
            operation_hints=[
                {
                    "relative_path": "README.md",
                    "operation_type": "append_block",
                    "provided_context": "sanitized context only",
                    "new_text_preview": "# preview-only candidate change",
                }
            ],
        )
    )
    rendered = SelfModificationDiffPreviewService().render_result_cli(result)

    assert result.diff_preview is not None
    assert result.diff_preview.redacted is True
    assert result.diff_preview.truncated is True
    assert "D:\\" not in rendered
    assert "raw_full_file_content_printed=False" in rendered
    assert "raw_secrets_printed=False" in rendered
    assert "No file mutation occurred." in rendered


def test_no_apply_safety_dry_run_or_workspace_change_state_is_created() -> None:
    candidate_result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    assert candidate_result.patch_candidate is not None
    candidate = candidate_result.patch_candidate
    result = SelfModificationDiffPreviewService(
        source_service=PatchDraftSourceService({candidate.candidate_id: candidate})
    ).create_patch_draft_and_preview(
        PatchDraftCreateRequest(
            patch_candidate_id=candidate.candidate_id,
            operation_hints=[
                {
                    "relative_path": "README.md",
                    "operation_type": "comment_only_change",
                    "provided_context": "sanitized context only",
                    "new_text_preview": "# preview-only candidate change",
                }
            ],
        )
    )

    assert result.draft is not None
    assert result.diff_preview is not None
    assert result.draft.static_safety_checked is False
    assert result.draft.dry_run_checked is False
    assert result.draft.review_approved is False
    assert result.draft.apply_gate_opened is False
    assert result.draft.applied is False
    assert result.diff_preview.applies_cleanly is None
    assert result.diff_preview.applied is False
    assert "workspace_file_changed" not in str(result.to_dict())


def test_runtime_source_avoids_forbidden_call_tokens() -> None:
    text = Path("src/chanta_core/self_modification_safety/draft.py").read_text(encoding="utf-8")
    forbidden_call_tokens = [
        "write_text",
        "write_bytes",
        "shutil.move",
        "os.remove",
        "subprocess",
        "os.system",
        "requests(",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "patch_apply(",
        "patch_applied(",
        "workspace_file_changed(",
        "openai",
        "anthropic",
        "chat.completions",
        "exec(",
        "eval(",
    ]

    for token in forbidden_call_tokens:
        assert token not in text
