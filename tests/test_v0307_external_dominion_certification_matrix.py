from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    ExternalDominionCertificationCase,
    ExternalDominionCertificationCaseKind,
    ExternalDominionCertificationCaseResult,
    ExternalDominionCertificationDecision,
    ExternalDominionCertificationMatrix,
    ExternalDominionCertificationPolicy,
    ExternalDominionCertificationReport,
    ExternalDominionCertificationSeverity,
    ExternalDominionCertificationStatus,
    ExternalDominionV0308PreviewGateHandoff,
    NoBrowserCertificationReport,
    NoGatewayCertificationReport,
    NoNetworkCertificationReport,
    NoProviderBypassCertificationReport,
    NoRPACertificationReport,
    build_certification_cases_from_policy,
    build_certification_matrix,
    build_certification_report,
    build_default_certification_policy,
    build_no_command_certification_report,
    build_no_credential_certification_report,
    build_no_execution_certification_report,
    build_no_network_certification_report,
    build_provider_gate_inheritance_certification_report,
    build_result_boundary_certification_report,
    build_v0308_preview_gate_handoff,
    certification_matrix_preserves_no_execution,
    certification_matrix_preserves_v0307_boundaries,
    certification_report_allows_v0308_gate_review_only,
    evaluate_certification_case,
)


def _policy(**overrides) -> ExternalDominionCertificationPolicy:
    data = {
        "policy_id": "certification_policy:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
    }
    data.update(overrides)
    return ExternalDominionCertificationPolicy(**data)


def _case(**overrides) -> ExternalDominionCertificationCase:
    data = {
        "case_id": "certification_case:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "case_kind": ExternalDominionCertificationCaseKind.NO_EXECUTION,
        "title": "No execution proof",
        "description": "Verify contract artifacts introduced no execution.",
        "severity": ExternalDominionCertificationSeverity.CRITICAL,
        "required_evidence_refs": ["evidence:boundary"],
        "source_artifact_refs": ["artifact:boundary"],
        "blocking": True,
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDominionCertificationCase(**data)


def _result(**overrides) -> ExternalDominionCertificationCaseResult:
    data = {
        "result_id": "certification_result:1",
        "case_id": "certification_case:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "case_kind": ExternalDominionCertificationCaseKind.NO_EXECUTION,
        "status": ExternalDominionCertificationStatus.PASSED,
        "passed": True,
        "blocking": True,
        "limitations": [],
        "failed_reasons": [],
        "evidence_refs": ["evidence:boundary"],
        "reviewer_refs": ["symbolic_reviewer"],
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDominionCertificationCaseResult(**data)


def _matrix(**overrides) -> ExternalDominionCertificationMatrix:
    case = _case()
    result = _result()
    data = {
        "matrix_id": "certification_matrix:1",
        "target_id": "target:external",
        "candidate_id": "candidate:1",
        "policy_id": "certification_policy:1",
        "cases": [case],
        "results": [result],
        "aggregate_status": ExternalDominionCertificationStatus.PASSED,
        "aggregate_decision": ExternalDominionCertificationDecision.PASS_FOR_LIMITED_PREVIEW_GATE_REVIEW,
        "passed_case_count": 1,
        "failed_case_count": 0,
        "blocked_case_count": 0,
        "limitation_count": 0,
        "unresolved_case_ids": [],
        "evidence_refs": ["evidence:boundary"],
        "ready_for_v0308_limited_preview_gate_review": True,
        "ready_for_execution": False,
        "production_certified": False,
        "live_adapter_certified": False,
        "metadata": {},
    }
    data.update(overrides)
    return ExternalDominionCertificationMatrix(**data)


def test_certification_policy_defaults_and_validation() -> None:
    policy = build_default_certification_policy("target:external", "candidate:1")

    assert policy.require_no_execution_proof is True
    assert policy.require_no_network_proof is True
    assert policy.require_no_credential_proof is True
    assert policy.require_no_command_proof is True
    assert policy.require_result_boundary is True
    assert policy.require_ocel_visibility_plan is True
    assert policy.require_provider_gate_inheritance is True
    assert policy.require_ready_for_execution_false is True
    assert policy.is_certification_result is False

    with pytest.raises(ValueError, match="policy_id"):
        _policy(policy_id="")
    with pytest.raises(ValueError, match="target_id"):
        _policy(target_id="")
    with pytest.raises(ValueError, match="require_no_execution_proof"):
        _policy(require_no_execution_proof=False)


def test_certification_case_and_result_validation() -> None:
    case = _case()
    result = _result()

    assert case.executes is False
    assert result.is_production_certification is False
    assert result.grants_execution is False
    assert result.blocks_matrix_pass is False

    with pytest.raises(ValueError, match="case_id"):
        _case(case_id="")
    with pytest.raises(ValueError, match="target_id"):
        _case(target_id="")
    with pytest.raises(ValueError, match="title"):
        _case(title=" ")
    with pytest.raises(ValueError, match="description"):
        _case(description="")

    with pytest.raises(ValueError, match="result_id"):
        _result(result_id="")
    with pytest.raises(ValueError, match="case_id"):
        _result(case_id="")
    with pytest.raises(ValueError, match="target_id"):
        _result(target_id="")
    with pytest.raises(ValueError, match="passed=True"):
        _result(status=ExternalDominionCertificationStatus.FAILED, passed=True, failed_reasons=["failed"])
    with pytest.raises(ValueError, match="limitations"):
        _result(status=ExternalDominionCertificationStatus.PASSED_WITH_LIMITATIONS, passed=True, limitations=[])
    with pytest.raises(ValueError, match="failed_reasons"):
        _result(status=ExternalDominionCertificationStatus.FAILED, passed=False, failed_reasons=[])

    failed = _result(status=ExternalDominionCertificationStatus.FAILED, passed=False, failed_reasons=["missing result boundary"])
    assert failed.blocks_matrix_pass is True


def test_certification_matrix_readiness_boundaries() -> None:
    matrix = _matrix()

    assert matrix.ready_for_v0308_limited_preview_gate_review is True
    assert matrix.ready_for_execution is False
    assert matrix.production_certified is False
    assert matrix.live_adapter_certified is False
    assert matrix.grants_execution is False
    assert certification_matrix_preserves_no_execution(matrix) is True
    assert certification_matrix_preserves_v0307_boundaries(matrix) is True

    with pytest.raises(ValueError, match="ready_for_execution"):
        _matrix(ready_for_execution=True)
    with pytest.raises(ValueError, match="production_certified"):
        _matrix(production_certified=True)
    with pytest.raises(ValueError, match="live_adapter_certified"):
        _matrix(live_adapter_certified=True)
    with pytest.raises(ValueError, match="preview gate review readiness"):
        _matrix(
            aggregate_decision=ExternalDominionCertificationDecision.REQUIRE_MORE_EVIDENCE,
            ready_for_v0308_limited_preview_gate_review=True,
        )
    with pytest.raises(ValueError, match="unresolved or failed blocking cases"):
        _matrix(unresolved_case_ids=["certification_case:1"], ready_for_v0308_limited_preview_gate_review=True)

    failed = _result(status=ExternalDominionCertificationStatus.FAILED, passed=False, failed_reasons=["missing provider gate"])
    with pytest.raises(ValueError, match="unresolved or failed blocking cases"):
        _matrix(
            results=[failed],
            aggregate_status=ExternalDominionCertificationStatus.PASSED,
            aggregate_decision=ExternalDominionCertificationDecision.PASS_FOR_LIMITED_PREVIEW_GATE_REVIEW,
            passed_case_count=0,
            failed_case_count=1,
            ready_for_v0308_limited_preview_gate_review=True,
        )


def test_certification_report_and_v0308_handoff_do_not_enable_execution() -> None:
    matrix = _matrix()
    report = build_certification_report(matrix)
    handoff = build_v0308_preview_gate_handoff(matrix, report)

    assert report.ready_for_execution is False
    assert report.grants_execution_permission is False
    assert report.is_production_certification is False
    assert certification_report_allows_v0308_gate_review_only(report) is True
    assert handoff.ready_for_v0308_limited_preview_gate_review is True
    assert handoff.ready_for_limited_preview_execution is False
    assert handoff.ready_for_execution is False
    assert handoff.production_certified is False
    assert handoff.live_adapter_certified is False
    assert handoff.executes_preview is False
    assert handoff.is_production_certification is False

    with pytest.raises(ValueError, match="summary"):
        ExternalDominionCertificationReport(
            "report:bad",
            matrix.matrix_id,
            matrix.target_id,
            matrix.candidate_id,
            "",
            matrix.aggregate_status,
            matrix.aggregate_decision,
            1,
            0,
            0,
            0,
        )
    with pytest.raises(ValueError, match="ready_for_execution"):
        ExternalDominionCertificationReport(
            "report:bad",
            matrix.matrix_id,
            matrix.target_id,
            matrix.candidate_id,
            "summary",
            matrix.aggregate_status,
            matrix.aggregate_decision,
            1,
            0,
            0,
            0,
            ready_for_execution=True,
        )
    with pytest.raises(ValueError, match="ready_for_limited_preview_execution"):
        ExternalDominionV0308PreviewGateHandoff(
            "handoff:bad",
            "target:external",
            "candidate:1",
            matrix.matrix_id,
            report.report_id,
            True,
            True,
            False,
            False,
            False,
        )


def test_specialized_no_runtime_reports_do_not_grant_runtime_permission() -> None:
    reports = [
        build_no_execution_certification_report("target:external", "candidate:1"),
        build_no_network_certification_report("target:external", "candidate:1"),
        build_no_credential_certification_report("target:external", "candidate:1"),
        build_no_command_certification_report("target:external", "candidate:1"),
        build_result_boundary_certification_report("target:external", "candidate:1"),
        build_provider_gate_inheritance_certification_report("target:external", "candidate:1"),
        NoProviderBypassCertificationReport("no_provider:1", "target:external", "candidate:1", ExternalDominionCertificationStatus.PASSED, True),
        NoRPACertificationReport("no_rpa:1", "target:external", "candidate:1", ExternalDominionCertificationStatus.PASSED, True),
        NoBrowserCertificationReport("no_browser:1", "target:external", "candidate:1", ExternalDominionCertificationStatus.PASSED, True),
        NoGatewayCertificationReport("no_gateway:1", "target:external", "candidate:1", ExternalDominionCertificationStatus.PASSED, True),
    ]

    for report in reports:
        assert report.passed is True
        assert report.grants_runtime_permission is False
        assert report.executes is False
        assert report.metadata.get("contract_artifact_check_only", True) is True

    with pytest.raises(ValueError, match="report_id"):
        NoNetworkCertificationReport("", "target:external", None, ExternalDominionCertificationStatus.PASSED, True)
    with pytest.raises(ValueError, match="target_id"):
        NoNetworkCertificationReport("report:bad", "", None, ExternalDominionCertificationStatus.PASSED, True)


def test_helpers_build_matrix_and_fail_missing_required_boundaries() -> None:
    policy = build_default_certification_policy("target:external", "candidate:1")
    cases = build_certification_cases_from_policy(policy)
    artifacts = {
        "result_boundary_policy": True,
        "provider_gate_inheritance": True,
        "ocel_visibility_plan": True,
        "rollback_or_no_op": True,
        "ready_for_execution": False,
    }
    results = [evaluate_certification_case(case, artifacts, ["evidence:boundary"]) for case in cases]
    matrix = build_certification_matrix(policy, cases, results)
    report = build_certification_report(matrix)
    handoff = build_v0308_preview_gate_handoff(matrix, report)

    assert matrix.ready_for_v0308_limited_preview_gate_review is True
    assert handoff.ready_for_limited_preview_execution is False
    assert handoff.ready_for_execution is False

    missing_result_case = next(case for case in cases if case.case_kind == ExternalDominionCertificationCaseKind.RESULT_BOUNDARY)
    missing_result = evaluate_certification_case(missing_result_case, {"result_boundary_policy": False})
    assert missing_result.passed is False
    assert missing_result.blocks_matrix_pass is True

    missing_provider_case = next(case for case in cases if case.case_kind == ExternalDominionCertificationCaseKind.PROVIDER_GATE_INHERITANCE)
    missing_provider = evaluate_certification_case(missing_provider_case, {"provider_gate_inheritance": False})
    assert missing_provider.passed is False
    assert missing_provider.blocks_matrix_pass is True
