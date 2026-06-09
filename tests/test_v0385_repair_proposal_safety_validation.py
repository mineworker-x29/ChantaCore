from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    ProposedChangeOperationKind,
    ProposedPatchArtifactKind,
    RepairProposalBoundaryViolation,
    RepairProposalBoundaryViolationKind,
    RepairProposalContentValidation,
    RepairProposalSafetyConfidenceLevel,
    RepairProposalSafetyDecision,
    RepairProposalSafetyDecisionKind,
    RepairProposalSafetyDisposition,
    RepairProposalSafetyDoNothingComparison,
    RepairProposalSafetyDoNothingComparisonKind,
    RepairProposalSafetyFlagSet,
    RepairProposalSafetyInput,
    RepairProposalSafetyMode,
    RepairProposalSafetyNoApplyGuarantee,
    RepairProposalSafetyPolicy,
    RepairProposalSafetyReadinessLevel,
    RepairProposalSafetyReport,
    RepairProposalSafetyRiskAssessment,
    RepairProposalSafetyRiskKind,
    RepairProposalSafetyRunPreview,
    RepairProposalSafetySeverity,
    RepairProposalSafetySourceKind,
    RepairProposalSafetySourceRef,
    RepairProposalSafetyStatus,
    RepairProposalSafetyValidationFinding,
    RepairProposalSafetyValidationReport,
    RepairProposalStaticCheckKind,
    RepairProposalStaticRuleKind,
    RepairProposalStaticValidationFinding,
    RepairProposalStaticValidationRule,
    RepairProposalTargetValidation,
    RepairProposalUnsafeOperationKind,
    RepairProposalUnsafeOperationSignal,
    V0385ReadinessReport,
    build_proposed_change_evidence_map,
    build_proposed_change_rationale,
    build_proposed_code_hunk,
    build_proposed_diff_metadata,
    build_proposed_file_change,
    build_proposed_patch_do_nothing_comparison,
    build_proposed_patch_envelope,
    build_proposed_patch_review_requirement,
    build_repair_proposal_boundary_violation,
    build_repair_proposal_content_validation,
    build_repair_proposal_safety_decision,
    build_repair_proposal_safety_do_nothing_comparison,
    build_repair_proposal_safety_flags,
    build_repair_proposal_safety_input,
    build_repair_proposal_safety_input_from_patch_envelope,
    build_repair_proposal_safety_no_apply_guarantee,
    build_repair_proposal_safety_policy,
    build_repair_proposal_safety_report,
    build_repair_proposal_safety_risk_assessment,
    build_repair_proposal_safety_run_preview,
    build_repair_proposal_safety_source_ref,
    build_repair_proposal_safety_validation_finding,
    build_repair_proposal_safety_validation_report,
    build_repair_proposal_static_validation_finding,
    build_repair_proposal_static_validation_rule,
    build_repair_proposal_target_validation,
    build_repair_proposal_unsafe_operation_signal,
    build_v0385_readiness_report,
    compare_repair_proposal_safety_to_do_nothing,
    create_repair_proposal_safety_report,
    decide_repair_proposal_safety,
    default_repair_proposal_safety_policy,
    repair_proposal_content_validation_does_not_execute_content,
    repair_proposal_safety_decision_is_not_apply_permission,
    repair_proposal_safety_flags_preserve_no_apply,
    repair_proposal_safety_policy_blocks_runtime,
    repair_proposal_safety_report_is_not_apply_permission,
    repair_proposal_target_validation_is_metadata_only,
    scan_proposed_patch_text_for_unsafe_operations,
    v0385_readiness_report_is_not_execution_ready,
    validate_repair_proposal_content,
    validate_repair_proposal_safety_report,
    validate_repair_proposal_targets,
)
import chanta_core.agent_runtime.repair_proposal_safety as safety_module


SAFE_FLAG_NAMES = {
    "ready_for_v0386_human_review_packet",
    "ready_for_v0387_bounded_repair_proposal_loop_trial",
    "ready_for_repair_proposal_safety_validation",
    "ready_for_static_patch_metadata_validation",
    "ready_for_patch_target_validation",
    "ready_for_patch_content_validation",
    "ready_for_boundary_violation_scan",
    "ready_for_unsafe_operation_detection",
    "ready_for_repair_safety_risk_assessment",
    "ready_for_repair_safety_do_nothing_comparison",
    "ready_for_repair_safety_decision",
    "ready_for_future_human_review_packet_input",
    "ready_for_future_bounded_repair_proposal_loop_trial_input",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if (field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES)
        or field.name == "production_certified"
    ]


def _patch_envelope(text="return 2", path="src/pkg/module.py"):
    evidence_map = build_proposed_change_evidence_map()
    rationale = build_proposed_change_rationale(evidence_map_id=evidence_map.change_evidence_map_id)
    hunk = build_proposed_code_hunk(
        target_relative_path=path,
        original_text="return 1",
        proposed_text=text,
    )
    diff = build_proposed_diff_metadata(
        target_relative_path=path,
        proposed_diff_text=f"--- proposed/{path}\n+++ proposed/{path}\n@@ metadata only @@\n-return 1\n+{text}",
        hunk_ids=[hunk.proposed_hunk_id],
        evidence_map_id=evidence_map.change_evidence_map_id,
    )
    file_change = build_proposed_file_change(
        target_relative_path=path,
        operation_kinds=[ProposedChangeOperationKind.PROPOSE_REPLACE],
        proposed_hunks=[hunk],
        proposed_diff=diff,
        rationale=rationale,
        evidence_map=evidence_map,
    )
    return build_proposed_patch_envelope(
        file_changes=[file_change],
        proposed_diffs=[diff],
        proposed_hunks=[hunk],
        evidence_map=evidence_map,
        rationale=rationale,
        review_requirement=build_proposed_patch_review_requirement(),
        do_nothing_comparison=build_proposed_patch_do_nothing_comparison(),
        source_refs=[],
    )


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairProposalSafetyMode} == {
        "static_validation",
        "target_validation",
        "content_validation",
        "boundary_violation_scan",
        "unsafe_operation_detection",
        "safety_risk_assessment",
        "do_nothing_safety_comparison",
        "future_human_review_packet_input",
        "future_loop_trial_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0384_proposed_patch_envelope" in {item.value for item in RepairProposalSafetySourceKind}
    assert "unsafe_operation_detected" in {item.value for item in RepairProposalSafetyStatus}
    assert "future_loop_trial_input_ready" in {item.value for item in RepairProposalSafetyReadinessLevel}
    assert "allow_unsafe_operation_detection" in {item.value for item in RepairProposalSafetyDecisionKind}
    assert "dependency_install_risk" in {item.value for item in RepairProposalSafetyRiskKind}
    assert "prohibit_dependency_install" in {item.value for item in RepairProposalStaticRuleKind}
    assert "proposed_text_pattern_check" in {item.value for item in RepairProposalStaticCheckKind}
    assert "unsafe_patch_apply_call" in {item.value for item in RepairProposalBoundaryViolationKind}
    assert "model_provider_call" in {item.value for item in RepairProposalUnsafeOperationKind}
    assert "critical" in {item.value for item in RepairProposalSafetySeverity}
    assert "inconclusive" in {item.value for item in RepairProposalSafetyConfidenceLevel}
    assert "safety_pass" in {item.value for item in RepairProposalSafetyDisposition}
    assert "do_nothing_required_due_to_blocking_violation" in {item.value for item in RepairProposalSafetyDoNothingComparisonKind}


def test_required_models_are_exported():
    for model in (
        RepairProposalSafetyFlagSet,
        RepairProposalSafetySourceRef,
        RepairProposalSafetyPolicy,
        RepairProposalSafetyInput,
        RepairProposalStaticValidationRule,
        RepairProposalStaticValidationFinding,
        RepairProposalBoundaryViolation,
        RepairProposalUnsafeOperationSignal,
        RepairProposalTargetValidation,
        RepairProposalContentValidation,
        RepairProposalSafetyRiskAssessment,
        RepairProposalSafetyDoNothingComparison,
        RepairProposalSafetyDecision,
        RepairProposalSafetyReport,
        RepairProposalSafetyValidationFinding,
        RepairProposalSafetyValidationReport,
        RepairProposalSafetyRunPreview,
        RepairProposalSafetyNoApplyGuarantee,
        V0385ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_safety_readiness_and_preserve_no_apply():
    flags = build_repair_proposal_safety_flags()
    assert flags.repair_proposal_safety_layer_constructed
    assert flags.static_patch_metadata_validation_available
    assert flags.patch_target_validation_available
    assert flags.patch_content_validation_available
    assert flags.boundary_violation_scan_available
    assert flags.unsafe_operation_detection_available
    assert flags.repair_safety_risk_assessment_available
    assert flags.repair_safety_do_nothing_comparison_available
    assert flags.repair_safety_decision_available
    assert flags.ready_for_v0386_human_review_packet
    assert flags.ready_for_v0387_bounded_repair_proposal_loop_trial
    assert flags.ready_for_repair_proposal_safety_validation
    assert flags.ready_for_static_patch_metadata_validation
    assert flags.ready_for_patch_target_validation
    assert flags.ready_for_patch_content_validation
    assert flags.ready_for_boundary_violation_scan
    assert flags.ready_for_unsafe_operation_detection
    assert flags.ready_for_future_human_review_packet_input
    assert flags.ready_for_future_bounded_repair_proposal_loop_trial_input
    assert repair_proposal_safety_flags_preserve_no_apply(flags)
    for field_name in _unsafe_flag_names(RepairProposalSafetyFlagSet):
        assert getattr(flags, field_name) is False
    assert flags.production_certified is False
    assert flags.metadata["static_validation_only"] is True
    assert flags.metadata["mandatory_human_review_before_any_apply"] is True


@pytest.mark.parametrize("field_name", _unsafe_flag_names(RepairProposalSafetyFlagSet))
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_repair_proposal_safety_flags(**{field_name: True})


def test_policy_allows_static_validation_only_and_blocks_runtime():
    policy = build_repair_proposal_safety_policy()
    assert policy.allow_static_validation
    assert policy.allow_target_validation
    assert policy.allow_content_validation
    assert policy.allow_boundary_violation_scan
    assert policy.allow_unsafe_operation_detection
    assert policy.allow_safety_risk_assessment
    assert policy.allow_do_nothing_safety_comparison
    assert policy.allow_future_human_review_packet_input
    assert policy.allow_future_loop_trial_input
    assert RepairProposalStaticRuleKind.PROHIBIT_DEPENDENCY_INSTALL in policy.required_rule_kinds
    assert RepairProposalUnsafeOperationKind.DEPENDENCY_INSTALL in policy.prohibited_unsafe_operations
    assert repair_proposal_safety_policy_blocks_runtime(policy)
    for field in fields(RepairProposalSafetyPolicy):
        if field.name.startswith("allow_") and field.name not in {
            "allow_static_validation",
            "allow_target_validation",
            "allow_content_validation",
            "allow_boundary_violation_scan",
            "allow_unsafe_operation_detection",
            "allow_safety_risk_assessment",
            "allow_do_nothing_safety_comparison",
            "allow_future_human_review_packet_input",
            "allow_future_loop_trial_input",
        }:
            assert getattr(policy, field.name) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_source_file_read",
        "allow_source_file_write",
        "allow_patch_file_write",
        "allow_file_edit",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_repair_execution",
        "allow_test_execution",
        "allow_subprocess",
        "allow_shell",
        "allow_dependency_install",
        "allow_network_access",
        "allow_model_provider_invocation",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ],
)
def test_policy_rejects_runtime_allow_true(field_name):
    with pytest.raises(ValueError):
        build_repair_proposal_safety_policy(**{field_name: True})


def test_safety_input_is_validation_request_not_apply_request():
    source_ref = build_repair_proposal_safety_source_ref()
    safety_input = build_repair_proposal_safety_input(source_refs=[source_ref])
    assert safety_input.version == "v0.38.5"
    assert safety_input.requested_mode == RepairProposalSafetyMode.STATIC_VALIDATION
    for action in (
        "source_read",
        "source_write",
        "patch_file_write",
        "file_edit",
        "patch_apply",
        "apply_patch",
        "git_apply",
        "repair_execution",
        "test_execution",
        "subprocess",
        "shell",
        "dependency_install",
        "network",
        "model_provider",
        "external_agent",
        "dominion",
    ):
        assert action in safety_input.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_repair_proposal_safety_input(prohibited_runtime_actions=["source_read"])


def test_static_rule_and_finding_are_metadata_only():
    rule = build_repair_proposal_static_validation_rule(
        rule_kind=RepairProposalStaticRuleKind.PROHIBIT_NETWORK_CALL,
        check_kind=RepairProposalStaticCheckKind.PROPOSED_TEXT_PATTERN_CHECK,
    )
    assert rule.enabled
    assert rule.blocks_on_failure
    assert rule.metadata["does_not_execute_proposed_code"]
    finding = build_repair_proposal_static_validation_finding(
        severity=RepairProposalSafetySeverity.HIGH,
        passed=False,
        blocked=True,
        requires_review=True,
    )
    assert finding.blocked
    with pytest.raises(ValueError):
        build_repair_proposal_static_validation_finding(
            severity=RepairProposalSafetySeverity.HIGH,
            passed=False,
            blocked=False,
            requires_review=False,
        )


@pytest.mark.parametrize(
    ("path", "violation", "risk"),
    [
        ("C:/absolute/path.py", RepairProposalBoundaryViolationKind.ABSOLUTE_TARGET_PATH, RepairProposalSafetyRiskKind.ABSOLUTE_PATH_TARGET_RISK),
        ("../escape.py", RepairProposalBoundaryViolationKind.PARENT_TRAVERSAL_TARGET, RepairProposalSafetyRiskKind.PARENT_TRAVERSAL_TARGET_RISK),
        ("references/OpenCode/runtime.py", RepairProposalBoundaryViolationKind.REFERENCE_TARGET, RepairProposalSafetyRiskKind.REFERENCE_TARGET_RISK),
        ("src/.env", RepairProposalBoundaryViolationKind.SECRET_TARGET, RepairProposalSafetyRiskKind.SECRET_TARGET_RISK),
    ],
)
def test_target_validation_blocks_unsafe_targets(path, violation, risk):
    result = validate_repair_proposal_targets([path])[0]
    assert result.valid_target is False
    assert violation in result.violation_kinds
    assert risk in result.risk_kinds
    assert repair_proposal_target_validation_is_metadata_only(result)


def test_target_validation_accepts_relative_metadata_target():
    result = validate_repair_proposal_targets(["src/pkg/module.py"])[0]
    assert result.valid_target
    assert result.normalized_relative_path == "src/pkg/module.py"
    assert result.violation_kinds == [RepairProposalBoundaryViolationKind.NO_VIOLATION]
    assert result.source_read_performed is False
    assert result.write_allowed is False
    assert result.apply_allowed is False
    assert result.repair_execution_allowed is False


@pytest.mark.parametrize(
    ("text", "expected_kind"),
    [
        ("dependency install via pip install unsafe", RepairProposalUnsafeOperationKind.DEPENDENCY_INSTALL),
        ("package manager command npm run build", RepairProposalUnsafeOperationKind.PACKAGE_MANAGER_COMMAND),
        ("network call using requests", RepairProposalUnsafeOperationKind.NETWORK_CALL),
        ("subprocess shell command", RepairProposalUnsafeOperationKind.SUBPROCESS_SHELL),
        ("eval call over proposed content", RepairProposalUnsafeOperationKind.EVAL_EXEC),
        ("dynamic import with importlib", RepairProposalUnsafeOperationKind.DYNAMIC_IMPORT),
        ("file write using write file", RepairProposalUnsafeOperationKind.FILE_WRITE),
        ("patch apply call requested", RepairProposalUnsafeOperationKind.PATCH_APPLY),
        ("git_apply requested", RepairProposalUnsafeOperationKind.GIT_APPLY),
        ("model provider openai call", RepairProposalUnsafeOperationKind.MODEL_PROVIDER_CALL),
        ("external agent codex cli call", RepairProposalUnsafeOperationKind.EXTERNAL_AGENT_CALL),
        ("credential secret token read", RepairProposalUnsafeOperationKind.CREDENTIAL_SECRET_READ),
        ("Dominion runtime marker", RepairProposalUnsafeOperationKind.DOMINION_RUNTIME),
        ("automatic repair loop", RepairProposalUnsafeOperationKind.AUTOMATIC_REPAIR_LOOP),
        ("retry loop while true", RepairProposalUnsafeOperationKind.RETRY_LOOP),
        ("multi-cycle repair loop", RepairProposalUnsafeOperationKind.MULTI_CYCLE_LOOP),
        ("delete file request", RepairProposalUnsafeOperationKind.FILE_DELETE),
        ("rename file request", RepairProposalUnsafeOperationKind.FILE_RENAME),
        ("chmod permission change", RepairProposalUnsafeOperationKind.PERMISSION_CHANGE),
        ("binary change", RepairProposalUnsafeOperationKind.BINARY_CHANGE),
    ],
)
def test_unsafe_operation_scan_detects_static_patterns(text, expected_kind):
    signals = scan_proposed_patch_text_for_unsafe_operations(text)
    assert expected_kind in {signal.unsafe_operation_kind for signal in signals}
    assert all(signal.blocked or signal.requires_review for signal in signals)


def test_boundary_violation_blocks_or_requires_review():
    no_violation = build_repair_proposal_boundary_violation()
    assert no_violation.blocked is False
    violation = build_repair_proposal_boundary_violation(
        violation_kind=RepairProposalBoundaryViolationKind.UNSAFE_NETWORK_CALL,
    )
    assert violation.blocked
    assert violation.requires_review
    with pytest.raises(ValueError):
        build_repair_proposal_boundary_violation(
            violation_kind=RepairProposalBoundaryViolationKind.NO_VIOLATION,
            blocked=True,
        )


def test_unsafe_operation_signal_blocks_or_requires_review():
    signal = build_repair_proposal_unsafe_operation_signal(
        unsafe_operation_kind=RepairProposalUnsafeOperationKind.NETWORK_CALL,
        matched_pattern="requests",
    )
    assert signal.blocked
    assert signal.requires_review
    with pytest.raises(ValueError):
        build_repair_proposal_unsafe_operation_signal(
            unsafe_operation_kind=RepairProposalUnsafeOperationKind.NETWORK_CALL,
            blocked=False,
            requires_review=False,
        )


def test_content_validation_scans_metadata_without_execution():
    envelope = _patch_envelope("requests network call")
    validation = validate_repair_proposal_content(envelope)
    assert validation.blocked
    assert validation.safe_for_future_human_review_packet is False
    assert validation.safe_for_future_loop_trial is False
    assert validation.executed_content is False
    assert validation.unsafe_operation_signals
    assert repair_proposal_content_validation_does_not_execute_content(validation)
    with pytest.raises(ValueError):
        build_repair_proposal_content_validation(executed_content=True)


def test_content_validation_safe_metadata_has_no_signals():
    validation = validate_repair_proposal_content(_patch_envelope("return 2"))
    assert validation.blocked is False
    assert validation.executed_content is False
    assert validation.unsafe_operation_signals == []


def test_missing_patch_envelope_blocks_safety_report():
    safety_input = build_repair_proposal_safety_input()
    report = create_repair_proposal_safety_report(safety_input, None)
    assert report.status == RepairProposalSafetyStatus.VALIDATION_BLOCKED
    assert RepairProposalSafetyRiskKind.MISSING_PATCH_ENVELOPE_RISK in report.risk_assessment.risk_kinds
    assert report.ready_for_future_loop_trial_input is False
    assert report.ready_for_execution is False


def test_safety_risk_assessment_blocks_future_loop_trial_for_critical_risk():
    risk = build_repair_proposal_safety_risk_assessment(
        risk_kinds=[RepairProposalSafetyRiskKind.NETWORK_CALL_RISK],
        severity=RepairProposalSafetySeverity.CRITICAL,
        blocks_future_loop_trial=True,
    )
    assert risk.blocks_future_loop_trial
    with pytest.raises(ValueError):
        build_repair_proposal_safety_risk_assessment(
            risk_kinds=[RepairProposalSafetyRiskKind.NETWORK_CALL_RISK],
            severity=RepairProposalSafetySeverity.CRITICAL,
            blocks_future_loop_trial=False,
        )


def test_do_nothing_safety_comparison_always_represented():
    risk = build_repair_proposal_safety_risk_assessment()
    comparison = compare_repair_proposal_safety_to_do_nothing(risk)
    assert comparison.do_nothing_remains_valid
    assert comparison.comparison_kind == RepairProposalSafetyDoNothingComparisonKind.PATCH_METADATA_SAFE_BUT_DO_NOTHING_VALID
    blocking = build_repair_proposal_safety_risk_assessment(
        risk_kinds=[RepairProposalSafetyRiskKind.NETWORK_CALL_RISK],
        severity=RepairProposalSafetySeverity.CRITICAL,
        unsafe_signal_ids=["signal:network"],
        blocks_future_loop_trial=True,
    )
    blocking_comparison = compare_repair_proposal_safety_to_do_nothing(blocking)
    assert blocking_comparison.do_nothing_required
    assert blocking_comparison.proposal_safe_enough_to_review is False


def test_safety_decision_never_allows_runtime_now():
    risk = build_repair_proposal_safety_risk_assessment()
    comparison = compare_repair_proposal_safety_to_do_nothing(risk)
    decision = decide_repair_proposal_safety(risk, comparison)
    assert decision.ready_for_future_human_review_packet_input
    assert decision.ready_for_future_loop_trial_input
    assert repair_proposal_safety_decision_is_not_apply_permission(decision)
    for field_name in (
        "source_read_allowed_now",
        "write_allowed_now",
        "patch_file_write_allowed_now",
        "edit_allowed_now",
        "apply_allowed_now",
        "apply_patch_allowed_now",
        "git_apply_allowed_now",
        "repair_execution_allowed_now",
        "test_execution_allowed_now",
        "model_provider_invocation_allowed_now",
        "external_agent_allowed_now",
        "production_certified",
    ):
        with pytest.raises(ValueError):
            build_repair_proposal_safety_decision(**{field_name: True})


def test_safety_report_runtime_flags_are_false():
    safety_input = build_repair_proposal_safety_input()
    envelope = _patch_envelope()
    report = create_repair_proposal_safety_report(safety_input, envelope)
    assert report.ready_for_future_human_review_packet_input
    assert report.source_read_performed_by_v0385 is False
    assert report.file_write_performed is False
    assert report.patch_file_written is False
    assert report.file_edit_performed is False
    assert report.patch_applied is False
    assert report.apply_patch_called is False
    assert report.git_apply_called is False
    assert report.tests_run is False
    assert report.repair_executed is False
    assert report.model_invocation_performed is False
    assert report.external_agent_invoked is False
    assert report.production_certified is False
    assert report.ready_for_execution is False
    assert repair_proposal_safety_report_is_not_apply_permission(report)


@pytest.mark.parametrize(
    "field_name",
    [
        "patch_applied",
        "apply_patch_called",
        "git_apply_called",
        "tests_run",
        "repair_executed",
        "production_certified",
        "ready_for_execution",
    ],
)
def test_safety_report_rejects_runtime_state_true(field_name):
    with pytest.raises(ValueError):
        build_repair_proposal_safety_report(**{field_name: True})


def test_validation_report_preview_guarantee_and_readiness():
    report = build_repair_proposal_safety_report()
    validation = validate_repair_proposal_safety_report(report)
    assert validation.static_validation_confirmed
    assert validation.no_source_read_confirmed
    assert validation.no_file_write_confirmed
    assert validation.no_patch_file_write_confirmed
    assert validation.no_edit_confirmed
    assert validation.no_apply_confirmed
    assert validation.no_repair_confirmed
    assert validation.no_tests_confirmed
    assert validation.no_external_calls_confirmed
    assert validation.do_nothing_comparison_confirmed
    assert validation.human_review_requirement_confirmed
    assert validation.ready_for_execution is False
    preview = build_repair_proposal_safety_run_preview()
    assert preview.will_read_source is False
    assert preview.will_apply_patch is False
    guarantee = build_repair_proposal_safety_no_apply_guarantee()
    assert guarantee.no_source_read
    assert guarantee.no_write
    assert guarantee.no_patch_file
    assert guarantee.no_edit
    assert guarantee.no_apply
    assert guarantee.no_repair
    assert guarantee.no_test
    assert guarantee.no_external_call
    readiness = build_v0385_readiness_report()
    assert readiness.ready_for_v0386_human_review_packet
    assert readiness.ready_for_v0387_bounded_repair_proposal_loop_trial
    assert v0385_readiness_report_is_not_execution_ready(readiness)


def test_helper_functions_create_static_validation_report_from_patch_envelope():
    envelope = _patch_envelope("return 2")
    safety_input = build_repair_proposal_safety_input_from_patch_envelope(envelope)
    assert safety_input.proposed_patch_envelope_id == envelope.proposed_patch_envelope_id
    assert safety_input.proposed_diff_ids
    assert safety_input.proposed_hunk_ids
    report = create_repair_proposal_safety_report(safety_input, envelope)
    assert report.target_validations
    assert report.content_validations
    assert report.do_nothing_comparison.do_nothing_remains_valid
    assert report.ready_for_execution is False


def test_unsafe_operation_blocks_report_loop_trial_but_not_apply():
    envelope = _patch_envelope("pip install forbidden dependency install")
    safety_input = build_repair_proposal_safety_input_from_patch_envelope(envelope)
    report = create_repair_proposal_safety_report(safety_input, envelope)
    assert report.status == RepairProposalSafetyStatus.UNSAFE_OPERATION_DETECTED
    assert report.risk_assessment.blocks_future_loop_trial
    assert report.ready_for_future_loop_trial_input is False
    assert report.safety_decision.apply_allowed_now is False
    assert report.safety_decision.test_execution_allowed_now is False
    assert report.safety_decision.model_provider_invocation_allowed_now is False


def test_helpers_do_not_contain_forbidden_runtime_call_patterns():
    source = inspect.getsource(safety_module)
    forbidden = [
        "Path.read_text",
        "Path.read_bytes",
        "open(",
        "write_text",
        "write_bytes",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "eval(",
        "exec(",
        "apply_patch(",
    ]
    for pattern in forbidden:
        assert pattern not in source

