import inspect

import pytest

from chanta_core.agent_runtime import (
    ModelOutputActionBlockedRecord,
    ModelOutputActionCandidate,
    ModelOutputActionCandidateKind,
    ModelOutputActionCandidateSet,
    ModelOutputActionDecisionKind,
    ModelOutputActionExtractionPolicy,
    ModelOutputActionNoExecutionGuarantee,
    ModelOutputActionQuarantineDecision,
    ModelOutputActionQuarantineFlagSet,
    ModelOutputActionQuarantinePacket,
    ModelOutputActionQuarantineReport,
    ModelOutputActionQuarantineRunPreview,
    ModelOutputActionQuarantineStatus,
    ModelOutputActionQuarantineValidationReport,
    ModelOutputActionReadinessLevel,
    ModelOutputActionRiskAssessment,
    ModelOutputActionRiskKind,
    ModelOutputActionRouteKind,
    ModelOutputActionRoutePolicy,
    ModelOutputActionSafeRoute,
    ModelOutputActionSignalStrength,
    ModelOutputActionSourceKind,
    ModelOutputActionSourceRef,
    ModelOutputActionTrustLevel,
    ModelResponseActionSignalKind,
    V0345ReadinessReport,
    assess_model_output_action_candidate_risk,
    build_model_output_action_blocked_record,
    build_model_output_action_candidate,
    build_model_output_action_candidate_set,
    build_model_output_action_extraction_policy,
    build_model_output_action_flags,
    build_model_output_action_no_execution_guarantee,
    build_model_output_action_quarantine_decision,
    build_model_output_action_quarantine_packet,
    build_model_output_action_quarantine_packet_from_candidates,
    build_model_output_action_quarantine_report,
    build_model_output_action_quarantine_run_preview,
    build_model_output_action_quarantine_validation_report,
    build_model_output_action_risk_assessment,
    build_model_output_action_route_policy,
    build_model_output_action_safe_route,
    build_model_output_action_source_ref,
    build_model_response_action_signal,
    build_model_response_envelope_from_supplied_text,
    build_v0345_readiness_report,
    decide_model_output_action_route,
    default_model_output_action_extraction_policy,
    default_model_output_action_route_policy,
    extract_model_output_action_candidates_from_action_signals,
    extract_model_output_action_candidates_from_response_envelope,
    model_output_action_candidate_is_not_execution,
    model_output_action_decision_is_not_execution,
    model_output_action_flags_preserve_execution_false,
    model_output_action_safe_route_is_not_execution,
    v0345_readiness_report_is_not_execution_ready,
    validate_model_output_action_quarantine_packet,
)
from chanta_core.agent_runtime import model_output_quarantine as quarantine_module


def test_v0345_taxonomies_cover_required_values() -> None:
    assert ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE.value == "final_response_candidate"
    assert ModelOutputActionCandidateKind.SAFE_WORKSPACE_INSPECTION_CANDIDATE.value == "safe_workspace_inspection_candidate"
    assert ModelOutputActionCandidateKind.PATCH_CANDIDATE.value == "patch_candidate"
    assert ModelOutputActionCandidateKind.OPENCODE_EXECUTION_CANDIDATE.value == "opencode_execution_candidate"
    assert ModelOutputActionSourceKind.V0343_MODEL_RESPONSE_ACTION_SIGNAL.value == "v0343_model_response_action_signal"
    assert ModelOutputActionTrustLevel.SANITIZED_BUT_UNTRUSTED.value == "sanitized_but_untrusted"
    assert ModelOutputActionRiskKind.PATCH_APPLICATION_RISK.value == "patch_application_risk"
    assert ModelOutputActionRouteKind.FUTURE_PATCH_PROPOSAL_TRACK.value == "future_patch_proposal_track"
    assert ModelOutputActionDecisionKind.BLOCK_UNSAFE_CANDIDATE.value == "block_unsafe_candidate"
    assert ModelOutputActionQuarantineStatus.QUARANTINED.value == "quarantined"
    assert ModelOutputActionReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0346.value == "design_handoff_ready_for_v0346"
    assert ModelOutputActionSignalStrength.EXPLICIT.value == "explicit"


def test_flags_allow_handoff_only_and_block_execution() -> None:
    flags = build_model_output_action_flags()
    assert isinstance(flags, ModelOutputActionQuarantineFlagSet)
    assert flags.action_quarantine_constructed is True
    assert flags.candidate_extraction_available is True
    assert flags.candidate_classification_available is True
    assert flags.quarantine_validation_available is True
    assert flags.ready_for_v0346_agent_step_runner_model_integration is True
    assert flags.ready_for_v0347_model_invocation_ocel_trace_packet is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_action_execution is False
    assert flags.ready_for_tool_execution is False
    assert flags.ready_for_safe_workspace_inspection_execution is False
    assert flags.ready_for_patch_proposal is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_existing_boundary_invocation is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_raw_response_persistence is False
    assert flags.production_certified is False
    assert model_output_action_flags_preserve_execution_false(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_action_execution",
        "ready_for_tool_execution",
        "ready_for_safe_workspace_inspection_execution",
        "ready_for_patch_proposal",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_provider_invocation",
        "ready_for_existing_boundary_invocation",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_raw_response_persistence",
    ],
)
def test_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_model_output_action_flags(**{unsafe_flag: True})


def test_source_ref_extraction_policy_candidate_and_candidate_set_are_metadata() -> None:
    source = build_model_output_action_source_ref(
        "source:quarantine:test",
        ModelOutputActionSourceKind.V0343_MODEL_RESPONSE_ACTION_SIGNAL,
        "signal:test",
        "Action signal source ref only.",
    )
    assert isinstance(source, ModelOutputActionSourceRef)
    assert source.execution is False
    assert source.provider_call is False
    assert source.file_read is False

    policy = default_model_output_action_extraction_policy()
    assert isinstance(policy, ModelOutputActionExtractionPolicy)
    assert policy.allow_final_response_candidate is True
    assert policy.allow_patch_candidate is False
    assert policy.allow_command_candidate is False
    assert policy.allow_provider_reinvoke_candidate is False
    assert policy.allow_credential_candidate is False
    assert policy.allow_external_harness_candidate is False
    assert policy.execution is False
    with pytest.raises(ValueError):
        build_model_output_action_extraction_policy(allow_patch_candidate=True)

    candidate = build_model_output_action_candidate(source_refs=[source])
    assert isinstance(candidate, ModelOutputActionCandidate)
    assert candidate.execution is False
    assert candidate.blocked_from_execution is False
    assert model_output_action_candidate_is_not_execution(candidate)

    unsafe = build_model_output_action_candidate(candidate_kind=ModelOutputActionCandidateKind.SHELL_COMMAND_CANDIDATE)
    assert unsafe.blocked_from_execution is True
    with pytest.raises(ValueError):
        build_model_output_action_candidate(candidate_kind=ModelOutputActionCandidateKind.SHELL_COMMAND_CANDIDATE, blocked_from_execution=False)

    candidate_set = build_model_output_action_candidate_set(candidates=[candidate, unsafe])
    assert isinstance(candidate_set, ModelOutputActionCandidateSet)
    assert candidate_set.candidate_count == 2
    assert candidate_set.blocked_candidate_count == 1
    assert candidate_set.action_queue is False


def test_risk_route_decision_blocked_record_and_safe_route_are_non_executing() -> None:
    risky = build_model_output_action_candidate(candidate_kind=ModelOutputActionCandidateKind.PATCH_CANDIDATE)
    assessment = assess_model_output_action_candidate_risk(risky)
    assert isinstance(assessment, ModelOutputActionRiskAssessment)
    assert assessment.must_block is True
    assert assessment.remediation_execution is False
    with pytest.raises(ValueError):
        build_model_output_action_risk_assessment(risk_kinds=[ModelOutputActionRiskKind.COMMAND_EXECUTION_RISK], must_block=False)

    route_policy = default_model_output_action_route_policy()
    assert isinstance(route_policy, ModelOutputActionRoutePolicy)
    assert route_policy.allow_final_response_route is True
    assert route_policy.allow_future_safe_workspace_inspection_route is True
    assert route_policy.allow_patch_proposal_route is False
    assert route_policy.allow_action_execution is False
    assert route_policy.allow_tool_execution is False
    assert route_policy.allow_workspace_write is False
    assert route_policy.allow_command_execution is False
    assert route_policy.allow_provider_reinvoke is False
    assert route_policy.allow_credential_access is False
    assert route_policy.allow_external_harness_execution is False
    for forbidden in ["allow_patch_proposal_route", "allow_action_execution", "allow_tool_execution", "allow_workspace_write", "allow_command_execution", "allow_provider_reinvoke", "allow_credential_access", "allow_external_harness_execution"]:
        with pytest.raises(ValueError):
            build_model_output_action_route_policy(**{forbidden: True})

    decision = decide_model_output_action_route(risky, route_policy)
    assert isinstance(decision, ModelOutputActionQuarantineDecision)
    assert decision.decision_kind == ModelOutputActionDecisionKind.BLOCK_UNSAFE_CANDIDATE
    assert decision.action_execution_allowed is False
    assert decision.tool_execution_allowed is False
    assert decision.workspace_write_allowed is False
    assert decision.command_execution_allowed is False
    assert decision.provider_invocation_allowed is False
    assert decision.credential_access_allowed is False
    assert model_output_action_decision_is_not_execution(decision)
    with pytest.raises(ValueError):
        build_model_output_action_quarantine_decision(action_execution_allowed=True)

    blocked = build_model_output_action_blocked_record(blocked_candidate_kind=ModelOutputActionCandidateKind.PATCH_CANDIDATE)
    assert isinstance(blocked, ModelOutputActionBlockedRecord)
    assert blocked.safe_outcome is True
    assert blocked.remediation_execution is False

    safe = build_model_output_action_safe_route()
    assert isinstance(safe, ModelOutputActionSafeRoute)
    assert safe.non_executing is True
    assert safe.ready_for_execution is False
    assert model_output_action_safe_route_is_not_execution(safe)
    with pytest.raises(ValueError):
        build_model_output_action_safe_route(ready_for_execution=True)


def test_packet_validation_report_run_preview_guarantee_and_readiness_are_safe() -> None:
    final_candidate = build_model_output_action_candidate(candidate_kind=ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE)
    blocked_candidate = build_model_output_action_candidate(candidate_kind=ModelOutputActionCandidateKind.COMMAND_EXECUTION_CANDIDATE)
    packet = build_model_output_action_quarantine_packet_from_candidates([final_candidate, blocked_candidate])
    assert isinstance(packet, ModelOutputActionQuarantinePacket)
    assert packet.ready_for_v0346_agent_step_runner_model_integration is True
    assert packet.ready_for_v0347_model_invocation_ocel_trace_packet is True
    assert packet.ready_for_action_execution is False
    assert packet.ready_for_execution is False
    assert packet.action_queue is False
    assert len(packet.decisions) == 2
    assert len(packet.blocked_records) == 1
    assert len(packet.safe_routes) == 1

    validation = validate_model_output_action_quarantine_packet(packet)
    assert isinstance(validation, ModelOutputActionQuarantineValidationReport)
    assert validation.action_execution_blocked is True
    assert validation.tool_execution_blocked is True
    assert validation.workspace_write_blocked is True
    assert validation.command_execution_blocked is True
    assert validation.provider_invocation_blocked is True
    assert validation.credential_access_blocked is True
    assert validation.ready_for_action_execution is False
    assert validation.ready_for_execution is False
    assert validation.execution_certification is False
    with pytest.raises(ValueError):
        build_model_output_action_quarantine_validation_report(action_execution_blocked=False)

    report = build_model_output_action_quarantine_report(candidate_count=2, blocked_candidate_count=1, safe_route_count=1)
    assert isinstance(report, ModelOutputActionQuarantineReport)
    assert report.ready_for_v0346_agent_step_runner_model_integration is True
    assert report.ready_for_v0347_model_invocation_ocel_trace_packet is True
    assert report.ready_for_action_execution is False
    assert report.ready_for_execution is False
    assert report.execution is False

    preview = build_model_output_action_quarantine_run_preview()
    assert isinstance(preview, ModelOutputActionQuarantineRunPreview)
    assert preview.execution is False
    for name in preview.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(preview, name) is True

    guarantee = build_model_output_action_no_execution_guarantee()
    assert isinstance(guarantee, ModelOutputActionNoExecutionGuarantee)
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    readiness = build_v0345_readiness_report()
    assert isinstance(readiness, V0345ReadinessReport)
    assert readiness.ready_for_v0346_agent_step_runner_model_integration is True
    assert readiness.ready_for_v0347_model_invocation_ocel_trace_packet is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_action_execution is False
    assert readiness.ready_for_tool_execution is False
    assert readiness.ready_for_patch_proposal is False
    assert readiness.ready_for_patch_application is False
    assert readiness.ready_for_provider_invocation is False
    assert readiness.ready_for_existing_boundary_invocation is False
    assert readiness.ready_for_raw_response_persistence is False
    assert v0345_readiness_report_is_not_execution_ready(readiness)
    with pytest.raises(ValueError):
        build_v0345_readiness_report(ready_for_action_execution=True)


def test_extract_candidates_from_response_envelope_and_action_signals() -> None:
    envelope = build_model_response_envelope_from_supplied_text("final response only")
    candidate_set = extract_model_output_action_candidates_from_response_envelope(envelope)
    assert candidate_set.candidates
    assert candidate_set.candidates[0].candidate_kind == ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE
    decision = decide_model_output_action_route(candidate_set.candidates[0])
    assert decision.route_kind == ModelOutputActionRouteKind.FINAL_RESPONSE_ROUTE
    assert decision.allowed_as_non_executing_route is True
    assert model_output_action_decision_is_not_execution(decision)

    signals = [
        build_model_response_action_signal("signal:final", ModelResponseActionSignalKind.FINAL_ANSWER_LIKE, blocked_from_execution=False),
        build_model_response_action_signal("signal:no_op", ModelResponseActionSignalKind.NO_ACTION_SIGNAL, blocked_from_execution=False),
        build_model_response_action_signal("signal:shell", ModelResponseActionSignalKind.SHELL_COMMAND_LIKE),
        build_model_response_action_signal("signal:patch", ModelResponseActionSignalKind.PATCH_LIKE),
        build_model_response_action_signal("signal:provider", ModelResponseActionSignalKind.PROVIDER_REINVOKE_LIKE),
        build_model_response_action_signal("signal:credential", ModelResponseActionSignalKind.CREDENTIAL_REQUEST_LIKE),
        build_model_response_action_signal("signal:harness", ModelResponseActionSignalKind.EXTERNAL_HARNESS_EXECUTE_LIKE),
        build_model_response_action_signal("signal:reference", ModelResponseActionSignalKind.REFERENCE_CODE_EXECUTE_LIKE),
    ]
    candidates = extract_model_output_action_candidates_from_action_signals(signals)
    kinds = {candidate.candidate_kind for candidate in candidates}
    assert ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE in kinds
    assert ModelOutputActionCandidateKind.NO_OP_CANDIDATE in kinds
    assert ModelOutputActionCandidateKind.SHELL_COMMAND_CANDIDATE in kinds
    assert ModelOutputActionCandidateKind.PATCH_CANDIDATE in kinds
    assert ModelOutputActionCandidateKind.PROVIDER_REINVOKE_CANDIDATE in kinds
    assert ModelOutputActionCandidateKind.CREDENTIAL_ACCESS_CANDIDATE in kinds
    assert ModelOutputActionCandidateKind.EXTERNAL_HARNESS_EXECUTION_CANDIDATE in kinds
    assert ModelOutputActionCandidateKind.REFERENCE_CODE_EXECUTION_CANDIDATE in kinds

    decisions = [decide_model_output_action_route(candidate) for candidate in candidates]
    blocked = [decision for decision in decisions if decision.route_kind == ModelOutputActionRouteKind.BLOCKED_ROUTE]
    assert blocked
    assert all(model_output_action_decision_is_not_execution(decision) for decision in decisions)


def test_future_safe_workspace_route_and_patch_future_track_do_not_execute() -> None:
    workspace_candidate = build_model_output_action_candidate(
        candidate_kind=ModelOutputActionCandidateKind.SAFE_WORKSPACE_INSPECTION_CANDIDATE,
        blocked_from_execution=False,
    )
    workspace_decision = decide_model_output_action_route(workspace_candidate)
    assert workspace_decision.route_kind == ModelOutputActionRouteKind.FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE
    assert workspace_decision.allowed_for_future_handoff is True
    assert workspace_decision.action_execution_allowed is False

    patch_candidate = build_model_output_action_candidate(candidate_kind=ModelOutputActionCandidateKind.PATCH_CANDIDATE)
    assert patch_candidate.proposed_route == ModelOutputActionRouteKind.FUTURE_PATCH_PROPOSAL_TRACK
    assert patch_candidate.blocked_from_execution is True
    patch_decision = decide_model_output_action_route(patch_candidate)
    assert patch_decision.route_kind == ModelOutputActionRouteKind.BLOCKED_ROUTE
    assert patch_decision.action_execution_allowed is False


def test_direct_dataclass_construction_with_valid_inputs() -> None:
    source = ModelOutputActionSourceRef(
        source_ref_id="source:direct",
        source_kind=ModelOutputActionSourceKind.TEST_FIXTURE,
        source_id="fixture",
        source_summary="fixture source only",
        trust_level=ModelOutputActionTrustLevel.TEST_FIXTURE,
    )
    candidate = ModelOutputActionCandidate(
        candidate_id="candidate:direct",
        candidate_kind=ModelOutputActionCandidateKind.ASK_USER_CANDIDATE,
        source_signal_id=None,
        source_response_envelope_id=None,
        candidate_summary="ask user candidate",
        candidate_preview="bounded ask user preview",
        signal_strength=ModelOutputActionSignalStrength.WEAK,
        risk_kinds=[],
        proposed_route=ModelOutputActionRouteKind.ASK_USER_ROUTE,
        source_refs=[source],
        blocked_from_execution=False,
        requires_review=False,
        future_gated=False,
    )
    assert model_output_action_candidate_is_not_execution(candidate)


def test_helpers_are_pure_conservative_source() -> None:
    source = inspect.getsource(quarantine_module)
    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        "eval(",
        "exec(",
        "importlib",
        "write_text(",
        "write_bytes(",
        "open(",
        "unlink(",
        ".rmdir(",
        ".mkdir(",
        ".rename(",
        "Path.replace(",
        ".chmod(",
        ".chown(",
        "shutil.",
        "sqlite",
        "logging.",
        "os.environ",
        "dotenv",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

    unsafe_true_patterns = [
        "ready_for_execution=True",
        "ready_for_action_execution=True",
        "ready_for_tool_execution=True",
        "ready_for_safe_workspace_inspection_execution=True",
        "ready_for_patch_proposal=True",
        "ready_for_patch_application=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_provider_invocation=True",
        "ready_for_existing_boundary_invocation=True",
        "ready_for_network_access=True",
        "ready_for_credential_access=True",
        "ready_for_raw_response_persistence=True",
        "production_certified=True",
    ]
    compact = source.replace(" ", "")
    for pattern in unsafe_true_patterns:
        assert pattern not in compact
