from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import subprocess
import sys

from chanta_core.self_modification_safety import (
    ModificationOutcomeRecordService,
    PostApplyVerificationReportService,
    PostApplyVerificationRequest,
    PostApplyVerificationSourceService,
    SelfModificationBoundedApplyService,
    SelfModificationPostApplyVerificationService,
    SelfModificationRegistryService,
)
from chanta_core.self_modification_safety.bounded_apply import BoundedPatchApplyReportService

from tests.test_self_modification_bounded_apply import _bundle


def _applied_bundle(tmp_path: Path):
    source, request, target = _bundle(tmp_path)
    apply_report = SelfModificationBoundedApplyService(
        report_service=BoundedPatchApplyReportService(source_service=source)
    ).apply_bounded_patch(request).report
    post_source = PostApplyVerificationSourceService(
        workspace_root=tmp_path,
        apply_reports={apply_report.report_id: apply_report},
        authorizations={request.authorization_id: source.authorizations[request.authorization_id]},
        rollback_plans={request.rollback_plan_id: source.rollback_plans[request.rollback_plan_id]},
    )
    service = SelfModificationPostApplyVerificationService(
        report_service=PostApplyVerificationReportService(source_service=post_source)
    )
    return service, post_source, apply_report, source, request, target


def test_post_apply_verification_report_builds_and_records_outcome(tmp_path: Path) -> None:
    service, _, apply_report, _, _, _ = _applied_bundle(tmp_path)

    result = service.verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id=apply_report.report_id))
    report = result.verification_report
    outcome = result.outcome_record

    assert report.verification_status == "passed"
    assert report.changed_file_count == 1
    assert report.verified_change_count == 1
    assert report.failed_change_count == 0
    assert report.rollback_recommended is False
    assert report.file_write_performed is False
    assert report.additional_patch_applied is False
    assert report.shell_executed is False
    assert report.test_lint_executed is False
    assert report.rollback_executed is False
    assert report.raw_content_emitted is False
    assert report.hash_results[0].hash_status == "matched"
    assert report.ocel_trace_results[0].trace_status == "complete"
    assert report.authorization_result is not None
    assert report.authorization_result.authorization_consumed is True
    assert report.rollback_result is not None
    assert report.rollback_result.rollback_status == "ready"
    assert report.scope_result is not None
    assert report.scope_result.scope_status == "matched"
    assert report.safety_regression_check is not None
    assert report.safety_regression_check.regression_status == "passed"
    assert outcome is not None
    assert outcome.outcome_status == "applied_verified"
    assert outcome.canonical_promotion_enabled is False
    assert outcome.memory_mutation_enabled is False
    assert outcome.persona_mutation_enabled is False
    assert outcome.overlay_mutation_enabled is False


def test_post_apply_missing_apply_report_blocks() -> None:
    service = SelfModificationPostApplyVerificationService()

    result = service.verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id="missing"))

    assert result.verification_report.verification_status == "blocked"
    assert result.outcome_record is not None
    assert result.outcome_record.outcome_status == "blocked"
    assert result.needs_more_input_candidate is not None
    assert "missing_apply_report" in [item.finding_type for item in result.verification_report.findings]


def test_post_apply_missing_workspace_file_changed_event_fails(tmp_path: Path) -> None:
    service, post_source, apply_report, _, _, _ = _applied_bundle(tmp_path)
    assert apply_report.transaction is not None
    change = replace(apply_report.transaction.file_changes[0], workspace_file_changed_event_id=None)
    transaction = replace(apply_report.transaction, file_changes=[change])
    altered = replace(apply_report, transaction=transaction)
    post_source.apply_reports = {altered.report_id: altered}

    result = service.verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id=altered.report_id))

    assert result.verification_report.verification_status == "failed"
    assert "missing_workspace_file_changed_event" in [item.finding_type for item in result.verification_report.findings]


def test_post_apply_after_hash_mismatch_recommends_rollback(tmp_path: Path) -> None:
    service, _, apply_report, _, _, target = _applied_bundle(tmp_path)
    target.write_text("drifted\n", encoding="utf-8", newline="")

    result = service.verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id=apply_report.report_id))

    assert result.verification_report.verification_status == "failed"
    assert result.verification_report.rollback_recommended is True
    assert result.outcome_record is not None
    assert result.outcome_record.outcome_status == "rollback_recommended"
    assert result.rollback_recommended_candidate is not None
    assert "after_hash_mismatch" in [item.finding_type for item in result.verification_report.findings]


def test_post_apply_current_target_missing_blocks(tmp_path: Path) -> None:
    service, _, apply_report, _, _, target = _applied_bundle(tmp_path)
    target.unlink()

    result = service.verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id=apply_report.report_id))

    assert result.verification_report.verification_status == "blocked"
    assert "current_target_missing" in [item.finding_type for item in result.verification_report.findings]


def test_post_apply_authorization_not_consumed_fails(tmp_path: Path) -> None:
    service, post_source, apply_report, _, request, _ = _applied_bundle(tmp_path)
    post_source.authorizations[request.authorization_id] = replace(
        post_source.authorizations[request.authorization_id],
        consumed=False,
    )

    result = service.verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id=apply_report.report_id))

    assert result.verification_report.verification_status == "failed"
    assert result.verification_report.authorization_result is not None
    assert result.verification_report.authorization_result.authorization_status == "unconsumed"
    assert "authorization_not_consumed" in [item.finding_type for item in result.verification_report.findings]


def test_post_apply_rollback_executed_unexpectedly_fails(tmp_path: Path) -> None:
    service, post_source, apply_report, _, request, _ = _applied_bundle(tmp_path)
    post_source.rollback_plans[request.rollback_plan_id] = replace(
        post_source.rollback_plans[request.rollback_plan_id],
        rollback_executed=True,
    )

    result = service.verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id=apply_report.report_id))

    assert result.verification_report.verification_status == "failed"
    assert result.verification_report.rollback_result is not None
    assert result.verification_report.rollback_result.rollback_status == "executed_unexpectedly"
    assert "rollback_executed_unexpectedly" in [item.finding_type for item in result.verification_report.findings]


def test_post_apply_scope_mismatch_fails(tmp_path: Path) -> None:
    service, post_source, apply_report, _, _, _ = _applied_bundle(tmp_path)
    assert apply_report.transaction is not None
    change = replace(apply_report.transaction.file_changes[0], applied_operation_ids=["unexpected_operation"])
    transaction = replace(apply_report.transaction, file_changes=[change])
    altered = replace(apply_report, transaction=transaction)
    post_source.apply_reports = {altered.report_id: altered}

    result = service.verify_and_record_outcome(PostApplyVerificationRequest(apply_report_id=altered.report_id))

    assert result.verification_report.verification_status == "failed"
    assert result.verification_report.scope_result is not None
    assert result.verification_report.scope_result.scope_status == "mismatch"
    assert "scope_mismatch" in [item.finding_type for item in result.verification_report.findings]


def test_post_apply_pig_ocpx_and_skill_contracts() -> None:
    service = SelfModificationPostApplyVerificationService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    contracts = {item["skill_id"]: item for item in SelfModificationRegistryService().list_skill_contracts()}

    assert pig["version"] == "v0.22.7"
    assert pig["subject"] == "post_apply_verification_outcome"
    assert pig["additional_file_write_performed"] is False
    assert pig["additional_patch_applied"] is False
    assert pig["rollback_executed"] is False
    assert pig["shell_executed"] is False
    assert pig["test_lint_executed"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_post_apply_verified_outcome_recorded"
    assert "PostApplyVerificationState" in ocpx["target_read_models"]
    assert "ModificationOutcomeState" in ocpx["target_read_models"]
    assert "outcome_recorded" in ocpx["effect_types"]
    assert contracts["skill:self_modification_post_apply_verify"]["status"] == "implemented"
    assert contracts["skill:self_modification_outcome_record"]["status"] == "implemented"
    assert contracts["skill:self_modification_post_apply_verify"]["post_apply_verify_enabled"] is True
    assert contracts["skill:self_modification_outcome_record"]["outcome_record_enabled"] is True


def test_post_apply_cli_commands_are_visible() -> None:
    commands = [
        ["post-apply", "verify", "--apply-report-id", "bounded_patch_apply_report:test"],
        ["post-apply", "verify", "--transaction-id", "bounded_patch_apply_transaction:test"],
        ["post-apply", "report", "--report-id", "post_apply_verification_report:test"],
        ["post-apply", "findings", "--report-id", "post_apply_verification_report:test"],
        ["outcome", "record", "--verification-report-id", "post_apply_verification_report:test"],
        ["outcome", "view", "--outcome-id", "modification_outcome_record:test"],
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
        assert "layer=self_modification_safety" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
        if command[:2] == ["post-apply", "verify"]:
            assert completed.returncode == 1
            assert "verification_status=blocked" in completed.stdout
            assert "file_write_performed=false" in completed.stdout
        else:
            assert completed.returncode == 0
