from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
    SelfDirectedIntentionRequest,
    SelfDirectedIntentionService,
)
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def _service_bundle(**kwargs):
    return SelfDirectedIntentionService().create_candidates(
        SelfDirectedIntentionRequest(**kwargs)
    )


def _valid_source_bundle():
    return _service_bundle(
        goal_text="inspect project structure and propose next safe steps",
        source_candidate_ids=["self_project_structure_candidate:valid"],
        source_report_ids=["self_surface_verification_report:valid"],
    )


def test_plan_todo_no_action_candidates_from_valid_sources() -> None:
    bundle = _valid_source_bundle()

    assert bundle.review_status == "candidate_only"
    assert bundle.requires_review is True
    assert bundle.materialized is False
    assert bundle.execution_enabled is False
    assert bundle.canonical_promotion_enabled is False
    assert bundle.promoted is False
    assert bundle.plan_candidates
    assert bundle.todo_candidates
    assert bundle.no_action_candidates
    assert not bundle.needs_more_input_candidates
    assert bundle.evidence_refs
    assert bundle.limitations

    plan = bundle.plan_candidates[0]
    todo = bundle.todo_candidates[0]
    assert plan.review_status == "candidate_only"
    assert plan.requires_review is True
    assert plan.materialized is False
    assert plan.execution_enabled is False
    assert plan.canonical_promotion_enabled is False
    assert plan.promoted is False
    assert todo.review_status == "candidate_only"
    assert todo.requires_review is True
    assert todo.materialized is False
    assert todo.execution_enabled is False
    assert todo.canonical_promotion_enabled is False
    assert todo.promoted is False
    assert all(step.execution_enabled is False for step in plan.steps)
    assert all(step.materialized is False for step in plan.steps)


def test_needs_more_input_when_sources_are_insufficient() -> None:
    bundle = _service_bundle()

    assert bundle.needs_more_input_candidates
    candidate = bundle.needs_more_input_candidates[0]
    assert candidate.review_status == "candidate_only"
    assert candidate.recommended_review_decision == "needs_more_input"
    assert candidate.missing_inputs
    assert candidate.execution_enabled is False
    assert candidate.materialized is False


def test_no_action_is_first_class_and_not_failure() -> None:
    bundle = _valid_source_bundle()
    no_action = bundle.no_action_candidates[0]

    assert no_action.recommended_review_decision == "no_action"
    assert no_action.review_status == "candidate_only"
    assert no_action.execution_enabled is False
    assert no_action.materialized is False
    assert bundle.plan_candidates
    assert bundle.todo_candidates


def test_future_dangerous_steps_are_blocked_and_non_executable() -> None:
    plan = _valid_source_bundle().plan_candidates[0]
    by_type = {step.step_type: step for step in plan.steps}

    for step_type in [
        "future_write_candidate",
        "future_shell_candidate",
        "future_network_candidate",
        "future_mcp_candidate",
        "future_plugin_candidate",
    ]:
        assert step_type in by_type
        step = by_type[step_type]
        assert step.risk_assessment.risk_level == "blocked"
        assert step.execution_enabled is False
        assert step.materialized is False


def test_risk_defaults_and_constraints_are_review_only() -> None:
    bundle = _valid_source_bundle()
    risk = bundle.plan_candidates[0].risk_assessment
    constraints = {item.constraint_type for item in bundle.constraints}

    assert risk.required_review is True
    assert risk.safe_to_execute is False
    assert risk.safe_to_materialize is False
    assert "write" in risk.blocked_capabilities
    assert {
        "read_only_only",
        "no_write",
        "no_shell",
        "no_network",
        "no_mcp",
        "no_plugin",
        "candidate_only",
    }.issubset(constraints)


def test_skill_contracts_and_gate_are_candidate_only(tmp_path) -> None:
    registry = SelfAwarenessRegistryService()
    for skill_id in ["skill:self_awareness_plan_candidate", "skill:self_awareness_todo_candidate"]:
        contract = registry.get_contract(skill_id)
        assert contract is not None
        assert contract.implementation_status == "implemented"
        assert contract.effect_type == READ_ONLY_OBSERVATION_EFFECT
        assert contract.execution_enabled is False
        assert contract.canonical_mutation_enabled is False
        assert contract.gate_contract.allow_skill_execution is True
        assert contract.risk_profile.mutates_workspace is False
        assert contract.risk_profile.uses_shell is False
        assert contract.risk_profile.uses_network is False
        assert contract.risk_profile.uses_mcp is False
        assert contract.risk_profile.loads_plugin is False
        assert contract.risk_profile.executes_external_harness is False
        assert contract.risk_profile.dangerous_capability is False

    invocation = ExplicitSkillInvocationService()
    gate = SkillExecutionGateService(explicit_skill_invocation_service=invocation)
    result = gate.gate_explicit_invocation(
        skill_id="skill:self_awareness_plan_candidate",
        input_payload={
            "root_path": str(tmp_path),
            "goal_text": "inspect project structure",
            "source_candidate_ids": ["self_project_structure_candidate:valid"],
        },
    )
    output = invocation.last_result.output_payload["output_attrs"]
    assert result.executed is True
    assert output["review_status"] == "candidate_only"
    assert output["execution_enabled"] is False
    assert output["materialized"] is False
    assert output["canonical_promotion_enabled"] is False
    assert output["promoted"] is False
    assert output["bundle_attrs"]["llm_planner_used"] is False


def test_cli_intention_candidates(capsys) -> None:
    assert main(
        [
            "self-awareness",
            "intention",
            "candidates",
            "--goal",
            "inspect project structure and propose next safe steps",
            "--include-no-action",
        ]
    ) == 0
    output = capsys.readouterr().out
    assert "Self-Directed Intention Candidate" in output
    assert "bundle_id=" in output
    assert "review_status=candidate_only" in output
    assert "plan_candidate_count=1" in output
    assert "todo_candidate_count=1" in output
    assert "no_action_candidate_count=1" in output
    assert "execution_enabled=false" in output
    assert "materialized=false" in output
    assert "canonical_promotion_enabled=false" in output
    assert "promoted=false" in output
    assert "no_actual_execution_occurred=true" in output
    assert "ChantaResearchGroup" + "_Members" not in output


def test_pig_and_ocpx_directed_intention_coverage() -> None:
    reports = SelfAwarenessReportService()
    pig = reports.build_pig_report()
    ocpx = reports.build_ocpx_projection()

    assert pig["version"] == "0.20.9"
    assert pig["workspace_awareness_coverage"]["directed_intention_candidate"] == "implemented_candidate_only"
    assert pig["execution_enabled"] is False
    assert pig["materialization_enabled"] is False
    assert pig["auto_task_creation_enabled"] is False
    assert pig["todo_file_write_enabled"] is False
    assert pig["canonical_promotion_enabled"] is False
    assert pig["llm_planner_enabled"] is False
    assert pig["safety_boundary_counts"]["write_mutation_count"] == 0
    assert pig["safety_boundary_counts"]["shell_usage_count"] == 0
    assert pig["safety_boundary_counts"]["network_usage_count"] == 0
    assert pig["safety_boundary_counts"]["mcp_usage_count"] == 0
    assert pig["safety_boundary_counts"]["plugin_loading_count"] == 0

    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    for candidate_type in [
        "plan_candidate",
        "todo_candidate",
        "no_action_candidate",
        "needs_more_input_candidate",
        "directed_intention_candidate_bundle",
    ]:
        assert candidate_type in ocpx["candidate_types"]
    assert "read_only_observation" in ocpx["effect_types"]
    assert "state_candidate_created" in ocpx["effect_types"]
