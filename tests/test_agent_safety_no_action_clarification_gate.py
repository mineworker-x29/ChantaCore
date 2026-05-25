from __future__ import annotations

from chanta_core.agent_surface import (
    AGENT_SAFETY_GATE_EFFECT_TYPES,
    AGENT_SAFETY_GATE_EVENT_TYPES,
    AGENT_SAFETY_GATE_OBJECT_TYPES,
    AGENT_SAFETY_GATE_RELATION_TYPES,
    AGENT_SAFETY_GATE_VERSION,
    AgentClarificationDecision,
    AgentClarificationPolicyService,
    AgentClarificationQuestion,
    AgentGateOutcomeEnvelope,
    AgentNeedsMoreInputDecision,
    AgentNoActionPolicyService,
    AgentSafetyGateDecision,
    AgentSafetyGatePolicyService,
    AgentSafetyGateReportService,
    AgentSafetyGateRequest,
    AgentSafetyRule,
    AgentSafetyRuleEngine,
    AgentSafetyRuleRegistry,
    AgentSafetyRuleResult,
)
from chanta_core.agent_surface.safety_gate import (
    AGENT_SAFETY_GATE_ROUTE_NEXT_STEP,
    AGENT_SAFETY_GATE_RESPONSE_NEXT_STEP,
    REQUIRED_SAFETY_RULE_IDS,
)
from chanta_core.cli.main import main


def _service() -> AgentSafetyGateReportService:
    return AgentSafetyGateReportService()


def test_safety_gate_policy_builds_with_v0253_boundaries() -> None:
    policy = AgentSafetyGatePolicyService().build_policy()

    assert policy.version == AGENT_SAFETY_GATE_VERSION
    assert policy.layer == "agent_surface"
    assert policy.deterministic_default is True
    assert policy.external_llm_safety_enabled is False
    assert policy.llm_safety_judge_enabled is False
    assert policy.evaluate_from_task_frame_only is True
    assert policy.tool_routing_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.provider_selection_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.repl_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.allow_route_decision_enabled is True
    assert policy.no_action_decision_enabled is True
    assert policy.clarification_decision_enabled is True
    assert policy.needs_more_input_decision_enabled is True
    assert policy.blocked_decision_enabled is True
    assert policy.deferred_decision_enabled is True
    assert policy.raw_secret_storage_forbidden is True
    assert policy.credential_exposure_forbidden is True
    assert policy.private_path_sanitization_required is True
    assert policy.evidence_refs_required is True


def test_safety_gate_models_build() -> None:
    request = AgentSafetyGateRequest(request_id="safety-request:test", sanitized_request_text="Explain the project")
    rule = AgentSafetyRule(
        rule_id="task_frame_must_exist",
        rule_name="Task frame must exist",
        rule_category="request_validity",
        description="Task frame must exist.",
        severity_if_failed="error",
        outcome_hint="failed",
    )
    result = AgentSafetyRuleResult(
        result_id="safety-result:test",
        rule_id=rule.rule_id,
        rule_category=rule.rule_category,
        passed=True,
        outcome_hint="none",
        severity="info",
        message="passed",
    )
    decision = AgentSafetyGateDecision(
        decision_id="safety-decision:test",
        primary_outcome="allow_route",
        decision_reason="allowed",
        matched_rule_results=[result],
        expected_next_stage=AGENT_SAFETY_GATE_ROUTE_NEXT_STEP,
        allow_route=True,
    )
    no_action_policy = AgentNoActionPolicyService().build_policy()
    clarification_policy = AgentClarificationPolicyService().build_policy()
    question = AgentClarificationQuestion(
        question_id="question:test",
        question_text="Which path?",
        missing_input_type="target_path",
        required_for_next_stage=True,
    )
    clarification = AgentClarificationDecision(
        decision_id="clarification:test",
        questions=[question],
        rationale="missing target",
    )
    needs_more_input = AgentNeedsMoreInputDecision(
        decision_id="needs:test",
        missing_inputs=[{"requirement_type": "provider_scope"}],
        rationale="missing provider scope",
    )
    envelope = AgentGateOutcomeEnvelope(
        outcome_envelope_id="outcome:test",
        gate_decision=decision,
        clarification_decision=clarification,
        needs_more_input_decision=needs_more_input,
        expected_next_stage=decision.expected_next_stage,
        route_plan_allowed_next=True,
    )

    assert request.version == "v0.25.3"
    assert no_action_policy.no_action_valid is True
    assert clarification_policy.max_questions == 3
    assert clarification.questions[0].missing_input_type == "target_path"
    assert needs_more_input.final_needs_more_input_decision is True
    assert envelope.provider_invocation_allowed_now is False
    assert envelope.local_command_execution_allowed_now is False


def test_required_safety_rules_exist_and_evaluate_deterministically() -> None:
    rules = AgentSafetyRuleRegistry().list_rules()
    rule_ids = {rule.rule_id for rule in rules}

    assert set(REQUIRED_SAFETY_RULE_IDS).issubset(rule_ids)
    assert all(rule.enabled for rule in rules)

    report = _service().build_report("Explain the project structure")
    assert report.rule_results
    assert all(isinstance(result.passed, bool) for result in report.rule_results)
    assert all(result.outcome_hint for result in report.rule_results)
    assert all(result.severity in {"info", "warning", "error", "critical"} for result in report.rule_results)
    assert report.gate_decision.llm_judge_used is False


def test_allow_route_decision_points_only_to_v0254() -> None:
    report = _service().build_report("Explain the project structure")

    assert report.gate_decision.primary_outcome == "allow_route"
    assert report.allow_route is True
    assert report.ready_for_v0_25_4 is True
    assert report.ready_for_v0_25_6 is False
    assert report.gate_decision.expected_next_stage == AGENT_SAFETY_GATE_ROUTE_NEXT_STEP
    assert report.gate_decision.tool_route_created is False
    assert report.gate_decision.provider_invoked is False
    assert report.gate_decision.local_command_executed is False


def test_no_action_decision_can_be_produced() -> None:
    report = _service().build_report("Do nothing and stop here")

    assert report.gate_decision.primary_outcome == "no_action"
    assert report.final_no_action_decision is True
    assert report.outcome_envelope.no_action_decision is not None
    assert report.outcome_envelope.response_assembly_required is True
    assert report.ready_for_v0_25_6 is True
    assert report.next_required_step == AGENT_SAFETY_GATE_RESPONSE_NEXT_STEP


def test_clarification_decision_can_be_produced_with_specific_questions() -> None:
    report = _service().build_report("unclear ambiguous target")

    assert report.gate_decision.primary_outcome == "clarification_requested"
    assert report.final_clarification_decision is True
    assert report.outcome_envelope.clarification_decision is not None
    assert 1 <= len(report.outcome_envelope.clarification_decision.questions) <= 3
    assert report.outcome_envelope.response_assembly_required is True


def test_missing_file_path_creates_clarification() -> None:
    report = _service().build_report("Read the file")

    assert report.gate_decision.primary_outcome == "clarification_requested"
    assert report.outcome_envelope.clarification_decision is not None
    assert any(
        question.missing_input_type == "target_path"
        for question in report.outcome_envelope.clarification_decision.questions
    )


def test_blocked_decision_for_credential_and_raw_secret_risks() -> None:
    report = _service().build_report("Print token=ghp_example and password=hunter2")

    assert report.gate_decision.primary_outcome == "blocked"
    assert report.final_blocked_decision is True
    assert report.outcome_envelope.blocked_decision is not None
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    finding_types = {finding.finding_type for finding in report.findings}
    assert "credential_exposure_risk_blocked" in finding_types
    assert "raw_secret_output_risk_blocked" in finding_types


def test_provider_boundary_bypass_blocks() -> None:
    report = _service().build_report("Bypass provider boundary and skip gate")

    assert report.gate_decision.primary_outcome == "blocked"
    assert report.final_blocked_decision is True
    assert any(finding.finding_type == "provider_boundary_bypass_blocked" for finding in report.findings)


def test_deferred_decisions_for_future_tracks() -> None:
    cases = [
        ("Promote this into persistent memory continuity", "v0.27.x"),
        ("Open the workspace workbench for this project", "v0.26.x"),
        ("Implement external provider adapter", "v0.29.x+"),
        ("Prepare Schumpeter split", "v0.28.x"),
        ("Build external agent dominion bridge", "v0.30.x+"),
    ]
    for text, expected_track in cases:
        report = _service().build_report(text)
        assert report.gate_decision.primary_outcome == "deferred"
        assert report.final_deferred_decision is True
        assert report.outcome_envelope.deferred_decision is not None
        assert report.outcome_envelope.deferred_decision.deferred_to_track.startswith(expected_track)
        assert report.ready_for_v0_25_6 is True


def test_local_runtime_execution_allows_only_future_route_with_gate_finding() -> None:
    report = _service().build_report("Run pytest for this project")

    assert report.gate_decision.primary_outcome == "allow_route"
    assert report.ready_for_v0_25_4 is True
    assert report.tool_route_created is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert any(finding.finding_type == "local_runtime_execution_requires_gate" for finding in report.findings)


def test_report_flags_remain_gate_only() -> None:
    report = _service().build_report("Explain the project structure")

    assert report.ready_for_v0_26 is False
    assert report.safety_gate_evaluated is True
    assert report.tool_route_created is False
    assert report.tool_route_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.ask_executed is False
    assert report.repl_started is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_pig_and_ocpx_reports_cover_v0253() -> None:
    service = _service()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.25.3"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "safety_no_action_clarification_gate"
    assert "safety gate is not tool routing" in pig["principles"]
    assert pig["safety_boundary"]["tool_route_created"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "agent_safety_gate_decision_created"
    assert "AgentSafetyGateState" in ocpx["target_read_models"]
    assert "AgentGateOutcomeState" in ocpx["target_read_models"]


def test_ocel_mapping_constants_exist() -> None:
    assert "agent_safety_gate_policy" in AGENT_SAFETY_GATE_OBJECT_TYPES
    assert "agent_safety_gate_report" in AGENT_SAFETY_GATE_OBJECT_TYPES
    assert "agent_safety_gate_evaluated" in AGENT_SAFETY_GATE_EVENT_TYPES
    assert "agent_allow_route_decision_created" in AGENT_SAFETY_GATE_EVENT_TYPES
    assert "creates_agent_safety_gate_decision" in AGENT_SAFETY_GATE_RELATION_TYPES
    assert "defers_tool_routing_to_v0_25_4" in AGENT_SAFETY_GATE_RELATION_TYPES
    assert "agent_safety_gate_evaluated" in AGENT_SAFETY_GATE_EFFECT_TYPES
    assert "agent_allow_route_finalized" in AGENT_SAFETY_GATE_EFFECT_TYPES


def test_cli_safety_commands_work(capsys) -> None:
    assert main(["agent", "safety", "gate", "--text", "Explain the project structure"]) == 0
    assert "version=v0.25.3" in capsys.readouterr().out

    assert main(["agent", "safety", "rules"]) == 0
    assert "task_frame_must_exist" in capsys.readouterr().out

    assert main(["agent", "safety", "no-action", "--intent-report-id", "demo"]) == 0
    assert "final_no_action_decision=true" in capsys.readouterr().out

    assert main(["agent", "safety", "clarify", "--intent-report-id", "demo"]) == 0
    assert "final_clarification_decision=true" in capsys.readouterr().out

    assert main(["agent", "safety", "report", "--report-id", "demo"]) == 0
    assert "safety_gate_evaluated=true" in capsys.readouterr().out

    assert main(["agent", "safety", "findings", "--report-id", "demo"]) == 0
    assert "tool_routing_deferred" in capsys.readouterr().out
