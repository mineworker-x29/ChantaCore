from __future__ import annotations

import subprocess
import sys
from dataclasses import replace

from chanta_core.self_modification_safety import (
    DIFF_PREVIEW_SKILL_ID,
    PATCH_CANDIDATE_CREATE_SKILL_ID,
    PATCH_DRAFT_CREATE_SKILL_ID,
    REQUEST_CREATE_SKILL_ID,
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    PatchDraft,
    PatchDraftCreateRequest,
    PatchDraftNeedsMoreInputCandidate,
    PatchDraftNoActionCandidate,
    PatchDraftSourceService,
    SelfModificationDiffPreviewService,
    SelfModificationRegistryService,
    SelfModificationRequestCandidateService,
    SelfModificationRequestCreateRequest,
)


def _patch_candidate():
    result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    assert result.patch_candidate is not None
    return result.patch_candidate


def _draft_service(candidate):
    return SelfModificationDiffPreviewService(
        source_service=PatchDraftSourceService({candidate.candidate_id: candidate})
    )


def _draft_request(candidate_id: str, **overrides):
    payload = {
        "patch_candidate_id": candidate_id,
        "operation_hints": [
            {
                "relative_path": "README.md",
                "operation_type": "comment_only_change",
                "anchor_type": "eof",
                "provided_context": "sanitized context only",
                "anchor_text_preview": "end of file",
                "new_text_preview": "# preview-only candidate change",
            }
        ],
    }
    payload.update(overrides)
    return PatchDraftCreateRequest(**payload)


def test_patch_draft_and_diff_preview_can_be_created_from_candidate() -> None:
    candidate = _patch_candidate()
    result = _draft_service(candidate).create_patch_draft_and_preview(_draft_request(candidate.candidate_id))

    assert isinstance(result.draft, PatchDraft)
    assert result.diff_preview is not None
    assert result.draft.patch_candidate_id == candidate.candidate_id
    assert result.diff_preview.patch_candidate_id == candidate.candidate_id
    assert result.draft.lifecycle_state == "preview_created"
    assert result.draft.draft_status == "draft_only"
    assert result.diff_preview.preview_status == "preview_only"
    assert result.draft.candidate_status == "candidate_only"
    assert result.diff_preview.lifecycle_state == "preview_created"
    assert result.diff_preview.preview_text_sanitized is not None


def test_patch_draft_and_preview_safety_flags_remain_disabled() -> None:
    candidate = _patch_candidate()
    result = _draft_service(candidate).create_patch_draft_and_preview(_draft_request(candidate.candidate_id))
    assert result.draft is not None
    assert result.diff_preview is not None

    draft = result.draft
    preview = result.diff_preview
    assert draft.static_safety_checked is False
    assert draft.dry_run_checked is False
    assert draft.review_approved is False
    assert draft.apply_gate_opened is False
    assert draft.applied is False
    assert draft.file_write_enabled is False
    assert draft.apply_patch_enabled is False
    assert draft.execution_enabled is False
    assert draft.materialized is False
    assert draft.promoted is False
    assert preview.static_safety_checked is False
    assert preview.dry_run_checked is False
    assert preview.applies_cleanly is None
    assert preview.applied is False
    assert preview.file_write_enabled is False
    assert preview.apply_patch_enabled is False
    assert all(operation.applies_cleanly is None for operation in draft.operations)
    assert all(operation.static_safety_checked is False for operation in draft.operations)
    assert all(operation.dry_run_checked is False for operation in draft.operations)
    assert all(operation.applied is False for operation in draft.operations)


def test_missing_candidate_creates_needs_more_input_candidate() -> None:
    result = SelfModificationDiffPreviewService().create_patch_draft_and_preview(
        PatchDraftCreateRequest(patch_candidate_id="patch_candidate:missing")
    )

    assert result.draft is None
    assert result.diff_preview is None
    assert isinstance(result.needs_more_input_candidate, PatchDraftNeedsMoreInputCandidate)
    assert result.needs_more_input_candidate.recommended_review_decision == "needs_more_input"
    assert "existing_patch_candidate" in result.needs_more_input_candidate.missing_inputs


def test_non_candidate_only_and_already_applied_candidates_are_blocked() -> None:
    candidate = _patch_candidate()
    not_candidate_only = replace(candidate, candidate_status="reviewed")
    applied_candidate = replace(candidate, applied=True)

    for blocked_candidate in [not_candidate_only, applied_candidate]:
        result = _draft_service(blocked_candidate).create_patch_draft_and_preview(
            _draft_request(blocked_candidate.candidate_id)
        )
        assert result.draft is None
        assert result.diff_preview is None
        assert isinstance(result.no_action_candidate, PatchDraftNoActionCandidate)
        assert result.no_action_candidate.applied is False


def test_context_anchor_operation_and_limits_are_evaluated() -> None:
    candidate = _patch_candidate()
    service = _draft_service(candidate)

    ambiguous = service.create_patch_draft_and_preview(
        _draft_request(candidate.candidate_id, operation_hints=[{"relative_path": "README.md", "ambiguous_anchor": True}])
    )
    assert ambiguous.needs_more_input_candidate is not None
    assert any(finding.finding_type == "anchor_ambiguous" for finding in ambiguous.findings)

    forbidden = service.create_patch_draft_and_preview(
        _draft_request(
            candidate.candidate_id,
            operation_hints=[
                {
                    "relative_path": "README.md",
                    "operation_type": "delete_file",
                    "provided_context": "sanitized context only",
                }
            ],
        )
    )
    assert forbidden.no_action_candidate is not None
    assert any(finding.finding_type == "operation_type_forbidden" for finding in forbidden.findings)

    line_limited = service.create_patch_draft_and_preview(
        _draft_request(
            candidate.candidate_id,
            max_added_lines=1,
            operation_hints=[
                {
                    "relative_path": "README.md",
                    "operation_type": "comment_only_change",
                    "provided_context": "sanitized context only",
                    "new_text_preview": "one\ntwo",
                }
            ],
        )
    )
    assert line_limited.no_action_candidate is not None
    assert any(finding.finding_type == "added_lines_exceed_limit" for finding in line_limited.findings)


def test_ocel_pig_ocpx_and_skill_statuses_are_updated_for_v0_22_2() -> None:
    contracts = {item["skill_id"]: item for item in SelfModificationRegistryService().list_skill_contracts()}
    service = SelfModificationDiffPreviewService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert contracts[REQUEST_CREATE_SKILL_ID]["status"] == "implemented"
    assert contracts[PATCH_CANDIDATE_CREATE_SKILL_ID]["status"] == "implemented"
    assert contracts[PATCH_DRAFT_CREATE_SKILL_ID]["status"] == "implemented"
    assert contracts[DIFF_PREVIEW_SKILL_ID]["status"] == "implemented"
    assert contracts["skill:self_modification_static_safety_check"]["non_executable"] is True
    assert "patch_draft" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "diff_preview" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "self_modification_diff_preview_created" in SELF_MODIFICATION_OCEL_EVENT_TYPES
    assert "produces_diff_preview" in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert pig["version"] == "v0.22.2"
    assert pig["subject"] == "patch_draft_diff_preview"
    assert pig["file_write_enabled"] is False
    assert pig["apply_patch_enabled"] is False
    assert pig["dry_run_enabled"] is False
    assert pig["static_safety_passed"] is False
    assert pig["patch_apply_enabled"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_patch_draft_diff_preview_created"
    assert "PatchDraftState" in ocpx["target_read_models"]
    assert "DiffPreviewState" in ocpx["target_read_models"]
    assert "PatchOperationDraftState" in ocpx["target_read_models"]
    assert "PatchDraftFindingState" in ocpx["target_read_models"]


def test_self_modification_patch_draft_diff_cli_commands() -> None:
    commands = [
        ["diff", "preview", "--candidate-id", "patch_candidate:test"],
        ["diff", "preview", "--candidate-id", "patch_candidate:test", "--format", "structured"],
        ["patch-draft", "create", "--candidate-id", "patch_candidate:test"],
        ["patch-draft", "view", "--draft-id", "patch_draft:test"],
        ["diff", "view", "--preview-id", "diff_preview:test"],
        ["diff", "findings", "--preview-id", "diff_preview:test"],
        ["pig-report"],
        ["ocpx-projection"],
    ]
    for command in commands:
        completed = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", "self-modification", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "layer=self_modification_safety" in completed.stdout
        assert "file_write_enabled=false" in completed.stdout
        assert "apply_patch_enabled=false" in completed.stdout
        assert "No file mutation occurred." in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
        assert "D:\\" not in completed.stdout
