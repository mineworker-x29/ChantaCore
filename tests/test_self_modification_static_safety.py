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
    STATIC_SAFETY_CHECK_SKILL_ID,
    STATIC_SAFETY_REPORT_SKILL_ID,
    PatchDraft,
    PatchDraftCreateRequest,
    PatchDraftSourceService,
    PatchStaticRuleRegistry,
    PatchStaticSafetyCheckRequest,
    PatchStaticSafetyNoActionCandidate,
    PatchStaticSafetyReport,
    PatchStaticSafetyReportService,
    PatchStaticSafetySourceService,
    SelfModificationDiffPreviewService,
    SelfModificationRegistryService,
    SelfModificationRequestCandidateService,
    SelfModificationRequestCreateRequest,
    SelfModificationStaticSafetyService,
)


def _bundle(**hint_overrides):
    candidate_result = SelfModificationRequestCandidateService().create_request_and_candidate(
        SelfModificationRequestCreateRequest(goal_text="docs cleanup", target_paths=["README.md"])
    )
    assert candidate_result.patch_candidate is not None
    candidate = candidate_result.patch_candidate
    hint = {
        "relative_path": "README.md",
        "operation_type": "comment_only_change",
        "anchor_type": "eof",
        "provided_context": "sanitized context only",
        "new_text_preview": "# preview-only candidate change",
    }
    hint.update(hint_overrides)
    draft_result = SelfModificationDiffPreviewService(
        source_service=PatchDraftSourceService({candidate.candidate_id: candidate})
    ).create_patch_draft_and_preview(
        PatchDraftCreateRequest(patch_candidate_id=candidate.candidate_id, operation_hints=[hint])
    )
    assert draft_result.draft is not None
    assert draft_result.diff_preview is not None
    return candidate, draft_result.draft, draft_result.diff_preview


def _service(candidate, draft, preview):
    return SelfModificationStaticSafetyService(
        report_service=PatchStaticSafetyReportService(
            source_service=PatchStaticSafetySourceService(
                patch_candidates={candidate.candidate_id: candidate},
                patch_drafts={draft.draft_id: draft},
                diff_previews={preview.preview_id: preview},
            )
        )
    )


def _report(candidate, draft, preview) -> PatchStaticSafetyReport:
    result = _service(candidate, draft, preview).check_static_safety(
        PatchStaticSafetyCheckRequest(
            patch_candidate_id=candidate.candidate_id,
            draft_id=draft.draft_id,
            preview_id=preview.preview_id,
        )
    )
    return result.report


def test_static_safety_report_builds_from_valid_draft_preview() -> None:
    candidate, draft, preview = _bundle()
    report = _report(candidate, draft, preview)

    assert report.report_id.startswith("patch_static_safety_report:")
    assert report.patch_candidate_id == candidate.candidate_id
    assert report.draft_id == draft.draft_id
    assert report.preview_id == preview.preview_id
    assert report.static_safety_status == "passed"
    assert report.eligible_for_dry_run is True
    assert report.safe_to_apply is False
    assert report.checked_rule_count > 0
    assert report.passed_rule_count > 0
    assert report.category_results
    assert isinstance(report, PatchStaticSafetyReport)


def test_missing_draft_or_preview_blocks_static_safety() -> None:
    candidate, draft, preview = _bundle()
    missing_draft_report = SelfModificationStaticSafetyService(
        report_service=PatchStaticSafetyReportService(
            source_service=PatchStaticSafetySourceService(
                patch_candidates={candidate.candidate_id: candidate},
                diff_previews={preview.preview_id: preview},
            )
        )
    ).check_static_safety(PatchStaticSafetyCheckRequest(preview_id=preview.preview_id))
    missing_preview_report = SelfModificationStaticSafetyService(
        report_service=PatchStaticSafetyReportService(
            source_service=PatchStaticSafetySourceService(
                patch_candidates={candidate.candidate_id: candidate},
                patch_drafts={draft.draft_id: draft},
            )
        )
    ).check_static_safety(PatchStaticSafetyCheckRequest(draft_id=draft.draft_id))

    assert missing_draft_report.report.static_safety_status == "blocked"
    assert isinstance(missing_draft_report.no_action_candidate, PatchStaticSafetyNoActionCandidate)
    assert missing_preview_report.report.static_safety_status == "blocked"
    assert isinstance(missing_preview_report.no_action_candidate, PatchStaticSafetyNoActionCandidate)


def test_path_secret_binary_generated_and_applied_states_are_checked() -> None:
    candidate, draft, preview = _bundle()
    applied_candidate = replace(candidate, applied=True)
    assert _report(applied_candidate, draft, preview).static_safety_status == "blocked"

    context = draft.target_context_refs[0]
    for relative_path, expected_type in [
        ("../outside.md", "path_not_workspace_relative"),
        ("private/notes.md", "private_path_risk"),
        (".env", "secret_file_risk"),
        ("image.png", "binary_file_risk"),
        ("build/generated.py", "generated_file_risk"),
    ]:
        changed_context = replace(
            context,
            relative_path=relative_path,
            private_boundary_risk=relative_path.startswith("private/"),
        )
        changed_draft = replace(draft, target_context_refs=[changed_context])
        changed_preview = replace(preview, target_refs=[changed_context.to_dict()])
        report = _report(candidate, changed_draft, changed_preview)
        assert any(finding.finding_type == expected_type for finding in report.findings)


def test_operation_scope_and_content_patterns_are_checked() -> None:
    candidate, draft, preview = _bundle()
    operation = draft.operations[0]

    forbidden_draft = replace(draft, operations=[replace(operation, operation_type="delete_file")])
    assert any(
        finding.finding_type == "forbidden_operation_type"
        for finding in _report(candidate, forbidden_draft, preview).findings
    )

    hunk_overflow = replace(preview, hunk_previews=preview.hunk_previews * 4)
    assert any(finding.finding_type == "hunk_count_exceeds_limit" for finding in _report(candidate, draft, hunk_overflow).findings)

    added_overflow = replace(draft, operations=[replace(operation, added_line_count=81)])
    assert any(finding.finding_type == "added_lines_exceed_limit" for finding in _report(candidate, added_overflow, preview).findings)

    removed_overflow = replace(draft, operations=[replace(operation, removed_line_count=81)])
    assert any(
        finding.finding_type == "removed_lines_exceed_limit"
        for finding in _report(candidate, removed_overflow, preview).findings
    )

    dangerous = replace(draft, operations=[replace(operation, new_text_preview="eval(user_input)")])
    assert any(finding.finding_type == "dangerous_pattern_detected" for finding in _report(candidate, dangerous, preview).findings)

    permission = replace(draft, operations=[replace(operation, new_text_preview="permission_grant = True")])
    assert any(
        finding.finding_type == "permission_grant_pattern_detected"
        for finding in _report(candidate, permission, preview).findings
    )

    shell = replace(draft, operations=[replace(operation, new_text_preview="os.system(command)")])
    assert any(
        finding.finding_type == "shell_network_mcp_plugin_pattern_detected"
        for finding in _report(candidate, shell, preview).findings
    )


def test_lifecycle_flags_and_report_safety_flags_are_checked() -> None:
    candidate, draft, preview = _bundle()
    operation = draft.operations[0]

    write_draft = replace(draft, file_write_enabled=True)
    assert any(finding.finding_type == "mutation_flag_enabled" for finding in _report(candidate, write_draft, preview).findings)

    apply_draft = replace(draft, apply_patch_enabled=True)
    assert any(finding.finding_type == "apply_flag_enabled" for finding in _report(candidate, apply_draft, preview).findings)

    applied_draft = replace(draft, applied=True, operations=[replace(operation, applied=True)])
    assert _report(candidate, applied_draft, preview).static_safety_status == "blocked"

    report = _report(candidate, draft, preview)
    finding_types = {finding.finding_type for finding in report.findings}
    assert "dry_run_not_performed" in finding_types
    assert "review_not_approved" in finding_types
    assert "apply_gate_not_opened" in finding_types
    assert report.safe_to_apply is False
    assert report.file_write_enabled is False
    assert report.apply_patch_enabled is False
    assert report.dry_run_executed is False
    assert report.applied is False
    assert report.workspace_file_changed_emitted is False
    assert report.dry_run_required is True
    assert report.human_review_required is True
    assert report.apply_gate_required is True
    assert report.rollback_plan_required is True
    assert report.post_apply_verification_required is True


def test_static_safety_ocel_pig_ocpx_and_skill_statuses() -> None:
    contracts = {item["skill_id"]: item for item in SelfModificationRegistryService().list_skill_contracts()}
    service = SelfModificationStaticSafetyService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    for skill_id in [
        REQUEST_CREATE_SKILL_ID,
        PATCH_CANDIDATE_CREATE_SKILL_ID,
        PATCH_DRAFT_CREATE_SKILL_ID,
        DIFF_PREVIEW_SKILL_ID,
        STATIC_SAFETY_CHECK_SKILL_ID,
        STATIC_SAFETY_REPORT_SKILL_ID,
    ]:
        assert contracts[skill_id]["status"] == "implemented"
        assert contracts[skill_id]["non_executable"] is True
        assert contracts[skill_id]["file_write_enabled"] is False
        assert contracts[skill_id]["apply_patch_enabled"] is False
    assert contracts["skill:self_modification_dry_run"]["status"] == "implemented"
    assert contracts["skill:self_modification_applicability_check"]["status"] == "implemented"
    assert "patch_static_safety_report" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "patch_static_safety_rule_result" in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    assert "self_modification_static_safety_report_created" in SELF_MODIFICATION_OCEL_EVENT_TYPES
    assert "checks_patch_static_safety" in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert "eligible_for_dry_run" in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert pig["version"] == "v0.22.3"
    assert pig["subject"] == "patch_static_safety_check"
    assert pig["file_write_enabled"] is False
    assert pig["apply_patch_enabled"] is False
    assert pig["dry_run_executed"] is False
    assert pig["review_approved"] is False
    assert pig["apply_gate_opened"] is False
    assert pig["workspace_file_changed_emitted"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_patch_static_safety_checked"
    assert "PatchStaticSafetyState" in ocpx["target_read_models"]
    assert "PatchStaticSafetyFindingState" in ocpx["target_read_models"]
    assert "PatchDryRunEligibilityState" in ocpx["target_read_models"]


def test_rule_registry_and_static_safety_cli_commands() -> None:
    rules = PatchStaticRuleRegistry().list_rules()
    assert {"path", "operation", "scope", "content_pattern", "secret_private", "lifecycle", "policy"} <= {
        rule.category for rule in rules
    }

    commands = [
        ["static-safety", "check", "--preview-id", "diff_preview:test"],
        ["static-safety", "check", "--draft-id", "patch_draft:test"],
        ["static-safety", "summary", "--preview-id", "diff_preview:test"],
        ["static-safety", "report", "--report-id", "patch_static_safety_report:test"],
        ["static-safety", "findings", "--report-id", "patch_static_safety_report:test"],
        ["static-safety", "rules"],
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
        assert "safe_to_apply=false" in completed.stdout
        assert "file_write_enabled=false" in completed.stdout
        assert "apply_patch_enabled=false" in completed.stdout
        assert "No file mutation occurred." in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
        assert "D:\\" not in completed.stdout
