import inspect

import pytest

from chanta_core.agent_runtime import (
    DiffProposalMode,
    DiffProposalReadinessLevel,
    DiffProposalStatus,
    DiffProposalTargetKind,
    PatchConformanceFinding,
    PatchConformanceFindingKind,
    PatchConformanceRule,
    PatchConformanceRuleKind,
    PatchDiffRiskSummary,
    PatchProposalRiskReport,
    PatchRiskDecisionKind,
    PatchRiskFlagSet,
    PatchRiskNoApplyGuarantee,
    PatchRiskReadinessLevel,
    PatchRiskRunPreview,
    PatchRiskScanDecision,
    PatchRiskScanInput,
    PatchRiskScanReport,
    PatchRiskScannerMode,
    PatchRiskScannerPolicy,
    PatchRiskScannerStatus,
    PatchRiskSeverity,
    PatchRiskSignal,
    PatchRiskSignalKind,
    PatchRiskSourceKind,
    PatchRiskSourceRef,
    PatchRiskValidationFinding,
    PatchRiskValidationReport,
    PatchSafetyRegressionKind,
    PatchSafetyRegressionReport,
    PatchSafetyRegressionSignal,
    PatchScopeViolation,
    PatchScopeViolationKind,
    PatchScopeViolationReport,
    StructuredPatchProposal,
    V0355ReadinessReport,
    build_diff_proposal_envelope,
    build_diff_proposal_target_file,
    build_patch_conformance_finding,
    build_patch_conformance_rule,
    build_patch_diff_risk_summary,
    build_patch_file_proposal,
    build_patch_hunk_proposal,
    build_patch_proposal_risk_report,
    build_patch_proposal_risk_report_from_scan,
    build_patch_risk_flags,
    build_patch_risk_no_apply_guarantee,
    build_patch_risk_run_preview,
    build_patch_risk_scan_decision,
    build_patch_risk_scan_input,
    build_patch_risk_scan_input_from_diff_envelope,
    build_patch_risk_scan_report,
    build_patch_risk_scanner_policy,
    build_patch_risk_signal,
    build_patch_risk_source_ref,
    build_patch_risk_validation_finding,
    build_patch_risk_validation_report,
    build_patch_safety_regression_report,
    build_patch_safety_regression_signal,
    build_patch_scope_violation,
    build_patch_scope_violation_report,
    build_structured_patch_proposal,
    build_unified_diff_proposal,
    build_v0355_readiness_report,
    default_patch_risk_scanner_policy,
    patch_risk_decision_is_not_apply_permission,
    patch_risk_flags_preserve_no_apply,
    patch_risk_report_is_not_approval,
    patch_risk_scanner_policy_blocks_apply,
    scan_diff_proposal_risks,
    scan_patch_conformance,
    scan_patch_safety_regressions,
    scan_patch_scope_violations,
    v0355_readiness_report_is_not_execution_ready,
    validate_patch_proposal_risk_report,
)
from chanta_core.agent_runtime import patch_risk as risk_module


def test_v0355_taxonomies_have_required_values() -> None:
    assert [item.value for item in PatchRiskScannerMode] == [
        "diff_envelope_scan",
        "unified_diff_scan",
        "structured_patch_scan",
        "combined_diff_and_structured_scan",
        "metadata_only_scan",
        "blocked",
        "review_required",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in PatchRiskSourceKind] == [
        "v0354_diff_proposal_envelope",
        "v0354_unified_diff_proposal",
        "v0354_structured_patch_proposal",
        "v0354_patch_file_proposal",
        "v0354_patch_hunk_proposal",
        "v0353_patch_plan",
        "v0353_change_set_graph",
        "v0352_context_snapshot",
        "v0352_evidence_bundle",
        "v0351_patch_intent_scope_bundle",
        "v0350_reference_pattern_digest",
        "reference_rejection_record",
        "test_fixture",
        "unknown",
    ]
    assert [item.value for item in PatchRiskScannerStatus] == [
        "unknown",
        "draft",
        "scan_input_created",
        "scan_completed",
        "scan_completed_with_warnings",
        "blocked",
        "review_required",
        "future_gated",
        "no_op",
        "safe_failed",
    ]
    assert [item.value for item in PatchRiskReadinessLevel] == [
        "not_ready",
        "risk_contract_ready",
        "scanner_ready",
        "risk_report_ready",
        "conformance_report_ready",
        "design_handoff_ready_for_v0356",
        "design_handoff_ready_for_v0357",
        "blocked",
        "future_track",
    ]
    assert [item.value for item in PatchRiskDecisionKind] == [
        "acceptable_for_review",
        "review_required",
        "block_proposal",
        "block_unsafe_surface",
        "future_gate_required",
        "no_op",
        "insufficient_evidence",
        "unknown",
    ]
    assert [item.value for item in PatchRiskSeverity] == ["info", "low", "medium", "high", "critical", "blocked", "unknown"]
    assert PatchRiskSignalKind.APPLY_PATCH_SIGNAL.value == "apply_patch_signal"
    assert PatchConformanceRuleKind.NO_APPLY_RULE.value == "no_apply_rule"
    assert PatchConformanceFindingKind.BLOCKING_VIOLATION.value == "blocking_violation"
    assert PatchSafetyRegressionKind.PATCH_APPLY_BOUNDARY_REGRESSION.value == "patch_apply_boundary_regression"
    assert PatchScopeViolationKind.OUTSIDE_ALLOWED_ROOT.value == "outside_allowed_root"


def test_required_models_are_exported() -> None:
    for model in [
        PatchRiskFlagSet,
        PatchRiskSourceRef,
        PatchRiskScannerPolicy,
        PatchRiskScanInput,
        PatchRiskSignal,
        PatchConformanceRule,
        PatchConformanceFinding,
        PatchSafetyRegressionSignal,
        PatchSafetyRegressionReport,
        PatchScopeViolation,
        PatchScopeViolationReport,
        PatchDiffRiskSummary,
        PatchProposalRiskReport,
        PatchRiskScanDecision,
        PatchRiskValidationFinding,
        PatchRiskValidationReport,
        PatchRiskScanReport,
        PatchRiskRunPreview,
        PatchRiskNoApplyGuarantee,
        V0355ReadinessReport,
    ]:
        assert inspect.isclass(model)


def test_patch_risk_flags_allow_scanner_readiness_and_block_unsafe_runtime() -> None:
    flags = build_patch_risk_flags()
    assert flags.patch_risk_scanner_constructed is True
    assert flags.patch_conformance_scanner_constructed is True
    assert flags.patch_safety_regression_scanner_constructed is True
    assert flags.patch_scope_violation_scanner_constructed is True
    assert flags.patch_risk_report_available is True
    assert flags.ready_for_v0356_human_review_packet is True
    assert flags.ready_for_v0357_patch_proposal_ocel_trace_packet is True
    assert flags.ready_for_patch_risk_scan is True
    assert flags.ready_for_patch_conformance_scan is True
    assert flags.ready_for_patch_safety_regression_scan is True
    assert flags.ready_for_patch_scope_violation_scan is True
    assert flags.ready_for_patch_review_packet_input is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_code_edit is False
    assert flags.ready_for_apply_patch is False
    assert flags.ready_for_git_apply is False
    assert flags.ready_for_test_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_reference_execution is False
    assert flags.ready_for_reference_import is False
    assert flags.production_certified is False
    assert patch_risk_flags_preserve_no_apply(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_reference_execution",
        "ready_for_reference_import",
        "ready_for_provider_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
    ],
)
def test_patch_risk_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_patch_risk_flags(**{unsafe_flag: True})


def test_source_policy_and_scan_input_are_not_apply_permission() -> None:
    source_ref = build_patch_risk_source_ref()
    assert source_ref.source_kind == PatchRiskSourceKind.V0354_DIFF_PROPOSAL_ENVELOPE

    policy = default_patch_risk_scanner_policy()
    assert policy.allow_acceptable_for_review is True
    assert policy.allow_approved_for_apply is False
    assert policy.allow_patch_apply is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_test_execution is False
    assert policy.allow_shell is False
    assert policy.allow_dependency_install is False
    assert policy.allow_reference_execution is False
    assert policy.allow_provider_invocation is False
    assert policy.allow_network_access is False
    assert policy.allow_credential_access is False
    assert policy.allow_secret_read is False
    assert patch_risk_scanner_policy_blocks_apply(policy)

    for field in ["allow_approved_for_apply", "allow_patch_apply", "allow_workspace_write", "allow_code_edit", "allow_test_execution", "allow_shell", "allow_dependency_install", "allow_reference_execution", "allow_provider_invocation", "allow_network_access", "allow_credential_access", "allow_secret_read"]:
        with pytest.raises(ValueError):
            build_patch_risk_scanner_policy(**{field: True})

    scan_input = build_patch_risk_scan_input()
    assert "patch_application" in scan_input.prohibited_runtime_actions
    assert "workspace_write" in scan_input.prohibited_runtime_actions
    assert "reference_execution" in scan_input.prohibited_runtime_actions


def test_signals_findings_reports_and_decisions_preserve_no_approval() -> None:
    signal = build_patch_risk_signal(
        signal_kind=PatchRiskSignalKind.APPLY_PATCH_SIGNAL,
        severity=PatchRiskSeverity.BLOCKED,
        finding_summary="apply_patch detected",
        evidence_preview="apply_patch",
        blocked=True,
        requires_review=True,
    )
    assert signal.blocked is True
    with pytest.raises(ValueError):
        build_patch_risk_signal(signal_kind=PatchRiskSignalKind.GIT_APPLY_SIGNAL, severity=PatchRiskSeverity.HIGH)

    rule = build_patch_conformance_rule()
    assert rule.mandatory is True
    assert rule.blocked_if_violated is True
    with pytest.raises(ValueError):
        build_patch_conformance_rule(rule_kind=PatchConformanceRuleKind.NO_SHELL_RULE, mandatory=False)

    finding = build_patch_conformance_finding(
        finding_kind=PatchConformanceFindingKind.BLOCKING_VIOLATION,
        severity=PatchRiskSeverity.BLOCKED,
        blocked=True,
        requires_review=True,
    )
    assert finding.blocked is True
    with pytest.raises(ValueError):
        build_patch_conformance_finding(finding_kind=PatchConformanceFindingKind.BLOCKING_VIOLATION)

    safety = build_patch_safety_regression_report(regression_signals=[build_patch_safety_regression_signal()])
    assert safety.ready_for_apply is False
    assert safety.ready_for_execution is False

    scope = build_patch_scope_violation_report(scope_violations=[build_patch_scope_violation()])
    assert scope.ready_for_apply is False
    assert scope.ready_for_execution is False

    summary = build_patch_diff_risk_summary(risk_signals=[signal], conformance_findings=[finding])
    assert summary.risk_count == 1
    assert summary.blocking_risk_count == 1

    report = build_patch_proposal_risk_report(diff_risk_summary=summary, safety_regression_report=safety, scope_violation_report=scope)
    assert report.blocked is True
    assert report.approved_for_apply is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_execution is False
    assert patch_risk_report_is_not_approval(report)
    with pytest.raises(ValueError):
        build_patch_proposal_risk_report(approved_for_apply=True)

    decision = build_patch_risk_scan_decision()
    assert decision.acceptable_for_review is True
    assert decision.approved_for_apply is False
    assert decision.ready_for_apply is False
    assert patch_risk_decision_is_not_apply_permission(decision)
    with pytest.raises(ValueError):
        build_patch_risk_scan_decision(ready_for_apply=True)


def _unsafe_envelope(text: str):
    unified = build_unified_diff_proposal(diff_text=text)
    return build_diff_proposal_envelope(unified_diff=unified, structured_patch=build_structured_patch_proposal(file_proposals=[]))


@pytest.mark.parametrize(
    ("text", "expected_kind"),
    [
        ("ready_for_execution=True", PatchRiskSignalKind.UNSAFE_READINESS_TRUE_SIGNAL),
        ("ready_for_patch_application=True", PatchRiskSignalKind.UNSAFE_READINESS_TRUE_SIGNAL),
        ("Path.write_text('x')", PatchRiskSignalKind.WORKSPACE_WRITE_SIGNAL),
        ("open('x', 'w')", PatchRiskSignalKind.WORKSPACE_WRITE_SIGNAL),
        ("subprocess.run(['x'])", PatchRiskSignalKind.SUBPROCESS_EXECUTION_SIGNAL),
        ("os.system('x')", PatchRiskSignalKind.SHELL_EXECUTION_SIGNAL),
        ("shell=True", PatchRiskSignalKind.SHELL_EXECUTION_SIGNAL),
        ("apply_patch", PatchRiskSignalKind.APPLY_PATCH_SIGNAL),
        ("git apply change.patch", PatchRiskSignalKind.GIT_APPLY_SIGNAL),
        ("python -m pytest", PatchRiskSignalKind.TEST_EXECUTION_SIGNAL),
        ("npm install package", PatchRiskSignalKind.DEPENDENCY_INSTALL_SIGNAL),
        ("import OpenCode", PatchRiskSignalKind.REFERENCE_IMPORT_SIGNAL),
        ("execute Hermes", PatchRiskSignalKind.REFERENCE_EXECUTION_SIGNAL),
        ("SECRET_KEY=abc", PatchRiskSignalKind.SECRET_EXPOSURE_SIGNAL),
        ("token=abc", PatchRiskSignalKind.TOKEN_EXPOSURE_SIGNAL),
        ("openai.chat.completions.create", PatchRiskSignalKind.PROVIDER_INVOCATION_OPENING_SIGNAL),
        ("requests.get('https://example.test')", PatchRiskSignalKind.NETWORK_ACCESS_OPENING_SIGNAL),
    ],
)
def test_scan_detects_unsafe_diff_patterns(text: str, expected_kind: PatchRiskSignalKind) -> None:
    signals = scan_diff_proposal_risks(_unsafe_envelope(text))
    assert any(signal.signal_kind == expected_kind for signal in signals)
    assert any(signal.blocked or signal.requires_review for signal in signals)


def test_scope_scan_detects_outside_and_blocked_targets() -> None:
    blocked_target = build_diff_proposal_target_file(
        target_path_ref="../outside.py",
        target_kind=DiffProposalTargetKind.BLOCKED_EXTERNAL_TARGET,
    )
    file_proposal = build_patch_file_proposal(target_file=blocked_target, hunk_proposals=[build_patch_hunk_proposal(target_file_id=blocked_target.target_file_id)])
    structured = build_structured_patch_proposal(file_proposals=[file_proposal])
    envelope = build_diff_proposal_envelope(structured_patch=structured)
    report = scan_patch_scope_violations(envelope)
    assert report.violation_count >= 1
    assert report.ready_for_apply is False
    assert report.ready_for_execution is False


def test_clean_metadata_only_proposal_is_acceptable_for_review_not_apply() -> None:
    envelope = build_diff_proposal_envelope()
    report = build_patch_proposal_risk_report_from_scan(envelope)
    assert report.overall_decision == PatchRiskDecisionKind.ACCEPTABLE_FOR_REVIEW
    assert report.acceptable_for_review is True
    assert report.approved_for_apply is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_execution is False
    validation = validate_patch_proposal_risk_report(report)
    assert validation.valid is True
    assert validation.ready_for_patch_application is False
    assert validation.ready_for_workspace_write is False
    assert validation.ready_for_execution is False


def test_conformance_and_safety_scans_return_reports_without_execution() -> None:
    envelope = _unsafe_envelope("ready_for_patch_application=True\napply_patch\npytest")
    conformance = scan_patch_conformance(envelope)
    assert any(item.finding_kind in {PatchConformanceFindingKind.VIOLATION, PatchConformanceFindingKind.BLOCKING_VIOLATION} for item in conformance)
    signals = scan_diff_proposal_risks(envelope)
    safety = scan_patch_safety_regressions(signals)
    assert safety.boundary_regression_count >= 1
    assert safety.ready_for_apply is False
    assert safety.ready_for_execution is False


def test_validation_scan_report_preview_guarantee_and_readiness_preserve_no_apply() -> None:
    validation_finding = build_patch_risk_validation_finding()
    validation_report = build_patch_risk_validation_report(findings=[validation_finding])
    assert validation_report.ready_for_patch_application is False
    assert validation_report.ready_for_workspace_write is False
    assert validation_report.ready_for_execution is False

    scan_report = build_patch_risk_scan_report()
    assert scan_report.risk_scan_ready is True
    assert scan_report.conformance_scan_ready is True
    assert scan_report.ready_for_patch_application is False
    assert scan_report.ready_for_workspace_write is False
    assert scan_report.ready_for_execution is False

    preview = build_patch_risk_run_preview()
    assert preview.no_patch_approval_guarantee is True
    assert preview.no_patch_application_guarantee is True
    assert preview.no_git_apply_runtime_call_guarantee is True

    guarantee = build_patch_risk_no_apply_guarantee()
    for field_name in guarantee.__dataclass_fields__:
        if field_name.startswith("no_"):
            assert getattr(guarantee, field_name) is True

    readiness = build_v0355_readiness_report()
    assert readiness.ready_for_v0356_human_review_packet is True
    assert readiness.ready_for_v0357_patch_proposal_ocel_trace_packet is True
    assert readiness.ready_for_patch_risk_scan is True
    assert readiness.ready_for_patch_review_packet_input is True
    assert readiness.ready_for_patch_application is False
    assert readiness.ready_for_workspace_write is False
    assert readiness.ready_for_code_edit is False
    assert readiness.ready_for_execution is False
    assert readiness.production_certified is False
    assert v0355_readiness_report_is_not_execution_ready(readiness)


def test_scan_input_from_diff_envelope_consumes_metadata_only() -> None:
    envelope = build_diff_proposal_envelope()
    scan_input = build_patch_risk_scan_input_from_diff_envelope(envelope)
    assert scan_input.diff_envelope_id == envelope.diff_envelope_id
    assert scan_input.unified_diff_id == envelope.unified_diff.unified_diff_id
    assert scan_input.structured_patch_id == envelope.structured_patch.structured_patch_id

    missing = build_patch_risk_scan_input_from_diff_envelope(None)
    assert missing.diff_envelope_id is None
    assert missing.requested_mode == PatchRiskScannerMode.REVIEW_REQUIRED


def test_helpers_do_not_use_forbidden_runtime_capabilities() -> None:
    source = inspect.getsource(risk_module)
    forbidden_tokens = [
        "from pathlib",
        "Path(",
        ".read_text(",
        ".read_bytes(",
        "import subprocess\n",
        "os.system(",
        "shell=True",
        ".unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "import requests\n",
        "import httpx\n",
        "import urllib\n",
        "import aiohttp\n",
        "import socket\n",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
    ]
    for token in forbidden_tokens:
        assert token not in source


def test_helpers_cannot_set_unsafe_readiness_true() -> None:
    with pytest.raises(ValueError):
        build_v0355_readiness_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v0355_readiness_report(ready_for_patch_application=True)
    with pytest.raises(ValueError):
        build_patch_risk_scan_report(ready_for_workspace_write=True)
    with pytest.raises(ValueError):
        build_patch_risk_validation_report(ready_for_execution=True)
