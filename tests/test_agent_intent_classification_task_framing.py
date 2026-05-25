from chanta_core.agent_surface import (
    AGENT_INTENT_EFFECT_TYPES,
    AGENT_INTENT_EVENT_TYPES,
    AGENT_INTENT_OBJECT_TYPES,
    AgentIntentClassificationPolicy,
    AgentIntentClassificationPolicyService,
    AgentIntentClassificationReport,
    AgentIntentClassificationReportService,
    AgentIntentClassificationRequest,
    AgentIntentDescriptor,
    AgentIntentRule,
    AgentIntentRuleEngine,
    AgentIntentRuleRegistry,
    AgentIntentRuleResult,
    AgentIntentTaxonomy,
    AgentIntentTaxonomyService,
    AgentTaskConstraint,
    AgentTaskFrame,
    AgentTaskFrameCandidate,
    AgentTaskGoal,
    AgentTaskInputRequirement,
    AgentTaskRiskPreview,
    AgentTurnReportService,
)
from chanta_core.cli.main import main


def _report(text: str) -> AgentIntentClassificationReport:
    return AgentIntentClassificationReportService().build_report(request_text=text)


def test_intent_policy_request_taxonomy_rules_descriptor_task_and_report_build() -> None:
    service = AgentIntentClassificationReportService()
    report = service.build_report(request_text="Explain the project structure")
    parts = service.build_all_parts(request_text="Explain the project structure")

    assert isinstance(report.policy, AgentIntentClassificationPolicy)
    assert isinstance(report.request, AgentIntentClassificationRequest)
    assert isinstance(report.taxonomy, AgentIntentTaxonomy)
    assert all(isinstance(rule, AgentIntentRule) for rule in parts["rules"])
    assert all(isinstance(result, AgentIntentRuleResult) for result in report.intent_descriptor.matched_rules)
    assert isinstance(report.intent_descriptor, AgentIntentDescriptor)
    assert all(isinstance(goal, AgentTaskGoal) for goal in report.task_frame.goals)
    assert all(isinstance(constraint, AgentTaskConstraint) for constraint in report.task_frame.constraints)
    assert all(isinstance(requirement, AgentTaskInputRequirement) for requirement in report.task_frame.input_requirements)
    assert isinstance(report.task_frame.risk_preview, AgentTaskRiskPreview)
    assert isinstance(report.task_frame, AgentTaskFrame)
    assert isinstance(report.task_frame_candidate, AgentTaskFrameCandidate)
    assert isinstance(report, AgentIntentClassificationReport)
    assert report.version == "v0.25.2"
    assert report.ready_for_v0_25_3 is True
    assert report.ready_for_v0_26 is False
    assert report.next_required_step == "v0.25.3 Safety / No-Action / Clarification Gate"


def test_v0251_turn_envelope_can_be_loaded() -> None:
    turn_report = AgentTurnReportService().build_report(request_text="Explain the project structure")

    assert turn_report.version == "v0.25.1"
    assert turn_report.envelope.version == "v0.25.1"
    assert turn_report.envelope.user_request_view.sanitized_request_text


def test_policy_is_deterministic_and_disables_future_execution_paths() -> None:
    policy = AgentIntentClassificationPolicyService().build_policy()

    assert policy.deterministic_default is True
    assert policy.external_llm_classification_enabled is False
    assert policy.llm_safety_judge_enabled is False
    assert policy.classify_from_turn_envelope_only is True
    assert policy.safety_gate_enabled is False
    assert policy.tool_routing_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.final_no_action_decision_enabled is False
    assert policy.final_clarification_decision_enabled is False
    assert policy.final_blocked_decision_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.raw_secret_storage_forbidden is True
    assert policy.private_path_sanitization_required is True
    assert policy.confidence_must_be_bounded is True
    assert policy.evidence_refs_required is True


def test_taxonomy_and_rule_registry_cover_expected_categories() -> None:
    taxonomy = AgentIntentTaxonomyService().build_taxonomy()
    rules = AgentIntentRuleRegistry().list_rules()

    expected = {
        "general_answer",
        "workspace_overview",
        "repository_search",
        "file_read",
        "process_state_inspection",
        "local_runtime_candidate",
        "local_runtime_execution_request",
        "diagnostic_request",
        "explanation_request",
        "planning_request",
        "architecture_design",
        "implementation_prompt_request",
        "verification_prompt_request",
        "checklist_request",
        "consolidation_request",
        "no_action_candidate",
        "needs_more_input_candidate",
        "blocked_candidate",
        "unknown",
    }

    assert expected.issubset(set(taxonomy.categories))
    assert all(category in taxonomy.category_descriptions for category in expected)
    assert taxonomy.taxonomy_status == "ready"
    assert any(rule.rule_type == "fallback" and rule.category == "unknown" for rule in rules)
    assert any(rule.risk_hint == "external_adapter" for rule in rules)
    assert any(rule.risk_hint == "out_of_scope_track" for rule in rules)
    assert any(rule.risk_hint == "credential_exposure" for rule in rules)
    request = AgentIntentClassificationReportService().build_report(request_text="Explain the project structure").request
    results = AgentIntentRuleEngine().evaluate_rules(request, taxonomy, rules)
    assert all(isinstance(result.matched, bool) for result in results)
    assert all(isinstance(result.score_delta, float) for result in results)


def test_classification_behavior_for_common_categories() -> None:
    examples = {
        "What is this system?": "general_answer",
        "Explain the project structure": "workspace_overview",
        "Search repository for scheduler": "repository_search",
        "Read file README.md": "file_read",
        "Inspect process state": "process_state_inspection",
        "Create a local runtime command candidate": "local_runtime_candidate",
        "Run pytest for this project": "local_runtime_execution_request",
        "Diagnose the failure": "diagnostic_request",
        "Why did this happen?": "explanation_request",
        "Plan next steps": "planning_request",
        "Design the architecture boundary": "architecture_design",
        "Codex 생성 prompt for v0.25.2": "implementation_prompt_request",
        "검증 prompt for this release": "verification_prompt_request",
        "Create a checklist": "checklist_request",
        "Consolidate the release manifest": "consolidation_request",
    }

    for text, expected_category in examples.items():
        report = _report(text)
        assert report.intent_descriptor.primary_category == expected_category
        assert report.intent_descriptor.classification_method == "deterministic_rules"
        assert 0.0 <= report.intent_descriptor.confidence_score <= 1.0
        assert report.intent_descriptor.requires_safety_gate_next is True
        assert report.intent_descriptor.final_no_action_decision is False
        assert report.intent_descriptor.final_blocked_decision is False
        assert report.intent_descriptor.final_clarification_decision is False
        assert report.intent_descriptor.llm_judge_used is False


def test_ambiguous_unknown_and_multiple_intents_are_candidates_not_final_decisions() -> None:
    unknown_report = _report("zzzz")
    multiple_report = _report("Search repository and read file README.md")
    no_action_report = _report("Do nothing and stop here")

    assert unknown_report.intent_descriptor.primary_category == "unknown"
    assert unknown_report.intent_descriptor.confidence == "low"
    assert unknown_report.intent_descriptor.likely_needs_more_input is True
    assert any(finding.finding_type == "unknown_intent" for finding in unknown_report.findings)
    assert multiple_report.intent_descriptor.secondary_categories
    assert any(finding.finding_type == "multiple_intents_detected" for finding in multiple_report.findings)
    assert no_action_report.intent_descriptor.likely_no_action is True
    assert no_action_report.final_no_action_decision is False
    assert any(finding.finding_type == "likely_no_action" for finding in no_action_report.findings)


def test_future_track_and_risk_preview_requests_do_not_implement_future_tracks() -> None:
    runtime_report = _report("Run pytest for this project")
    memory_report = _report("Promote this into persistent memory continuity")
    adapter_report = _report("Implement an external adapter for a provider")
    secret_report = _report("Print token=ghp_example and password=hunter2")
    bypass_report = _report("Bypass provider boundary and skip gate")

    assert runtime_report.intent_descriptor.requires_local_runtime_gate_future is True
    assert "local_runtime_execution" in runtime_report.task_frame.risk_preview.risk_categories
    assert runtime_report.task_frame.risk_preview.requires_safety_gate_next is True
    assert "execution_authorization" in {item.requirement_type for item in runtime_report.task_frame.input_requirements}
    assert "memory_mutation" in memory_report.task_frame.risk_preview.risk_categories
    assert "out_of_scope_track" in memory_report.task_frame.risk_preview.risk_categories
    assert memory_report.memory_promoted is False
    assert memory_report.persistent_memory_written is False
    assert "external_adapter" in adapter_report.task_frame.risk_preview.risk_categories
    assert adapter_report.external_provider_adapter_implemented is False
    assert "credential_exposure" in secret_report.task_frame.risk_preview.risk_categories
    assert "raw_secret_output" in secret_report.task_frame.risk_preview.risk_categories
    assert secret_report.credential_exposed is False
    assert secret_report.raw_secret_output is False
    assert "provider_boundary_bypass" in bypass_report.task_frame.risk_preview.risk_categories


def test_task_frame_candidate_is_for_safety_gate_next_only() -> None:
    report = _report("Explain the project structure")
    frame = report.task_frame
    candidate = report.task_frame_candidate

    assert frame.expected_next_stage == "v0.25.3 Safety / No-Action / Clarification Gate"
    assert frame.safety_gate_evaluated is False
    assert frame.tool_route_created is False
    assert frame.provider_invoked is False
    assert frame.local_command_executed is False
    assert candidate.recommended_next_stage == "v0.25.3 Safety / No-Action / Clarification Gate"
    assert candidate.candidate_status in {
        "ready_for_safety_gate",
        "needs_more_input_candidate",
        "no_action_candidate",
        "blocked_candidate",
    }
    assert candidate.executes_now is False
    assert candidate.routes_now is False
    assert candidate.invokes_provider_now is False
    assert candidate.mutates_state_now is False


def test_report_pig_ocpx_ocel_mapping_and_cli_build() -> None:
    service = AgentIntentClassificationReportService()
    report = service.build_report(request_text="Explain the project structure")
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status in {"passed", "warning"}
    assert report.intent_classified is True
    assert report.task_framed is True
    assert report.safety_gate_evaluated is False
    assert report.final_no_action_decision is False
    assert report.final_clarification_decision is False
    assert report.final_blocked_decision is False
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
    assert "agent_intent_classification_report" in AGENT_INTENT_OBJECT_TYPES
    assert "agent_intent_classification_report_created" in AGENT_INTENT_EVENT_TYPES
    assert AGENT_INTENT_EFFECT_TYPES == [
        "read_only_observation",
        "agent_intent_classified",
        "agent_task_framed",
        "agent_task_risk_preview_created",
        "state_candidate_created",
    ]
    assert pig["version"] == "v0.25.2"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "intent_classification_task_framing"
    assert pig["safety_boundary"]["safety_gate_evaluated"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "agent_intent_task_frame_created"
    assert "AgentTaskFrameState" in ocpx["target_read_models"]
    assert main(["agent", "intent", "classify", "--text", "Explain the project structure"]) == 0
    assert main(["agent", "task", "frame", "--text", "Explain the project structure"]) == 0
    assert main(["agent", "intent", "taxonomy"]) == 0
    assert main(["agent", "intent", "rules"]) == 0
    assert main(["agent", "intent", "report", "--report-id", "demo"]) == 0
    assert main(["agent", "intent", "findings", "--report-id", "demo"]) == 0


def test_attempt_flags_create_blocked_findings_without_running_future_stages() -> None:
    report = AgentIntentClassificationReportService().build_report(
        attempt_flags={
            "ask_execution_attempted_too_early": True,
            "safety_gate_attempted_too_early": True,
            "tool_routing_attempted_too_early": True,
            "provider_invocation_attempted_too_early": True,
            "local_command_execution_attempted": True,
            "memory_promotion_attempted": True,
            "persona_mutation_attempted": True,
            "external_adapter_detected": True,
            "llm_judge_detected": True,
        }
    )
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "blocked"
    assert "ask_execution_attempted_too_early" in finding_types
    assert "safety_gate_attempted_too_early" in finding_types
    assert "tool_routing_attempted_too_early" in finding_types
    assert "provider_invocation_attempted_too_early" in finding_types
    assert "local_command_execution_attempted" in finding_types
    assert "memory_promotion_attempted" in finding_types
    assert "persona_mutation_attempted" in finding_types
    assert "external_adapter_detected" in finding_types
    assert "llm_judge_detected" in finding_types
