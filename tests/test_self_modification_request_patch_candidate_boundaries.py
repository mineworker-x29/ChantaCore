from __future__ import annotations

from pathlib import Path

from chanta_core.self_modification_safety import (
    SelfModificationRequestCandidateService,
    SelfModificationRequestCreateRequest,
)


DOC_FILE = Path("docs/versions/v0.22/v0.22.1_self_modification_request_patch_candidate.md")


def test_docs_define_request_candidate_boundary() -> None:
    text = DOC_FILE.read_text(encoding="utf-8")

    assert "Self-Modification Request & Patch Candidate" in text
    assert "자기수정 요청·패치 후보" in text
    assert "Self-modification request is not file mutation." in text
    assert "Patch candidate is not patch draft." in text
    assert "Patch candidate is not diff preview." in text
    assert "Patch candidate is not patch apply." in text
    assert "No-action and needs-more-input are valid outcomes." in text
    assert "v0.22.2 Patch Draft / Diff Preview" in text
    assert "Implemented File List" in text
    assert "Restore Procedure" in text
    assert "Restore Checklist" in text


def test_request_candidate_outputs_do_not_expose_full_paths_or_file_content() -> None:
    result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    rendered = SelfModificationRequestCandidateService().render_result_cli(result)

    assert "README.md" in rendered
    assert "D:\\" not in rendered
    assert "raw_file_content" not in rendered.replace("raw_file_content_printed=False", "")
    assert "raw_secrets_printed=False" in rendered
    assert "private_full_paths_printed=False" in rendered


def test_no_diff_write_apply_or_execution_state_is_created() -> None:
    result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    candidate = result.patch_candidate
    assert candidate is not None

    assert candidate.diff_generated is False
    assert candidate.applied is False
    assert candidate.file_write_enabled is False
    assert candidate.apply_patch_enabled is False
    assert candidate.execution_enabled is False
    assert candidate.dry_run_checked is False
    assert candidate.review_approved is False
    assert candidate.apply_gate_opened is False


def test_outside_workspace_target_is_blocked_without_full_path_output() -> None:
    result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["..\\outside.md"])
    )

    assert result.request.scope.scope_status == "blocked"
    assert result.patch_candidate is None
    assert result.no_action_candidate is not None
    assert result.request.target_refs[0].relative_path is None
    rendered = SelfModificationRequestCandidateService().render_result_cli(result)
    assert "D:\\" not in rendered
    assert "No file mutation occurred." in rendered


def test_runtime_source_avoids_forbidden_call_tokens() -> None:
    text = Path("src/chanta_core/self_modification_safety/candidate.py").read_text(encoding="utf-8")
    forbidden_call_tokens = [
        "write_text",
        "write_bytes",
        "shutil.move",
        "os.remove",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "generate_patch(",
        "generate_diff(",
        "patch_draft(",
        "patch_apply(",
        "workspace_file_changed(",
        "openai",
        "anthropic",
        "chat.completions",
        "exec(",
        "eval(",
    ]

    for token in forbidden_call_tokens:
        assert token not in text
