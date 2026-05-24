from __future__ import annotations

from pathlib import Path

from chanta_core.self_modification_safety import (
    PatchDraftCreateRequest,
    PatchDraftSourceService,
    PatchStaticSafetyCheckRequest,
    PatchStaticSafetyReportService,
    PatchStaticSafetySourceService,
    SelfModificationDiffPreviewService,
    SelfModificationRequestCandidateService,
    SelfModificationRequestCreateRequest,
    SelfModificationStaticSafetyService,
)


DOC_FILE = Path("docs/versions/v0.22/v0.22.3_patch_static_safety_check.md")


def _static_result():
    candidate_result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    assert candidate_result.patch_candidate is not None
    candidate = candidate_result.patch_candidate
    draft_result = SelfModificationDiffPreviewService(
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
    assert draft_result.draft is not None
    assert draft_result.diff_preview is not None
    return SelfModificationStaticSafetyService(
        report_service=PatchStaticSafetyReportService(
            source_service=PatchStaticSafetySourceService(
                patch_candidates={candidate.candidate_id: candidate},
                patch_drafts={draft_result.draft.draft_id: draft_result.draft},
                diff_previews={draft_result.diff_preview.preview_id: draft_result.diff_preview},
            )
        )
    ).check_static_safety(
        PatchStaticSafetyCheckRequest(
            patch_candidate_id=candidate.candidate_id,
            draft_id=draft_result.draft.draft_id,
            preview_id=draft_result.diff_preview.preview_id,
        )
    )


def test_docs_define_static_safety_boundary() -> None:
    text = DOC_FILE.read_text(encoding="utf-8")

    assert "Patch Static Safety Check" in text
    assert "Static safety check is not dry-run." in text
    assert "Static safety report is not approval." in text
    assert "Static safety pass is not clean application." in text
    assert "Static safety pass does not imply patch apply." in text
    assert "v0.22.4 Patch Dry-run / Applicability Check" in text
    assert "Implemented File List" in text
    assert "Restore Procedure" in text
    assert "Restore Checklist" in text


def test_static_safety_output_is_report_only_and_sanitized() -> None:
    result = _static_result()
    rendered = SelfModificationStaticSafetyService().render_result_cli(result)

    assert result.report.review_status == "report_only"
    assert result.report.safe_to_apply is False
    assert result.report.file_write_enabled is False
    assert result.report.apply_patch_enabled is False
    assert result.report.dry_run_executed is False
    assert result.report.applied is False
    assert result.report.workspace_file_changed_emitted is False
    assert "D:\\" not in rendered
    assert "raw_full_file_content_printed=False" in rendered
    assert "raw_secrets_printed=False" in rendered
    assert "No file mutation occurred." in rendered


def test_static_safety_does_not_create_execution_or_apply_state() -> None:
    result = _static_result()
    as_text = str(result.to_dict())

    assert "dry_run_executed': True" not in as_text
    assert "review_approved': True" not in as_text
    assert "apply_gate_opened': True" not in as_text
    assert "applied': True" not in as_text
    assert "safe_to_apply': True" not in as_text
    assert "workspace_file_changed" in as_text
    assert "workspace_file_changed_emitted': False" in as_text


def test_runtime_source_avoids_forbidden_call_tokens() -> None:
    text = Path("src/chanta_core/self_modification_safety/static_safety.py").read_text(encoding="utf-8")
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
