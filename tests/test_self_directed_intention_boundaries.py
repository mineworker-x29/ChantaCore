from pathlib import Path

from chanta_core.self_awareness import (
    SELF_AWARENESS_OCEL_EVENT_TYPES,
    SELF_AWARENESS_OCEL_OBJECT_TYPES,
    SELF_AWARENESS_OCEL_RELATION_TYPES,
    SelfDirectedIntentionRequest,
    SelfDirectedIntentionService,
)


def test_no_task_queue_todo_memory_persona_or_overlay_materialization(tmp_path: Path) -> None:
    before = {item.name for item in tmp_path.iterdir()}
    bundle = SelfDirectedIntentionService().create_candidates(
        SelfDirectedIntentionRequest(
            goal_text="inspect project structure",
            source_candidate_ids=["self_project_structure_candidate:valid"],
        )
    )
    after = {item.name for item in tmp_path.iterdir()}

    assert before == after
    assert not (tmp_path / "TODO.md").exists()
    assert bundle.bundle_attrs["task_queue_entry_created"] is False
    assert bundle.bundle_attrs["todo_file_written"] is False
    assert bundle.bundle_attrs["memory_mutation_used"] is False
    assert bundle.bundle_attrs["persona_mutation_used"] is False
    assert bundle.bundle_attrs["overlay_mutation_used"] is False
    assert bundle.bundle_attrs["workspace_write_used"] is False
    assert bundle.bundle_attrs["shell_execution_used"] is False
    assert bundle.bundle_attrs["network_access_used"] is False
    assert bundle.bundle_attrs["mcp_connection_used"] is False
    assert bundle.bundle_attrs["plugin_loading_used"] is False
    assert bundle.bundle_attrs["external_harness_execution_used"] is False
    assert bundle.bundle_attrs["actual_execution_occurred"] is False
    assert bundle.bundle_attrs["llm_planner_used"] is False


def test_all_candidates_and_steps_are_non_executable_and_non_materialized() -> None:
    bundle = SelfDirectedIntentionService().create_candidates(
        SelfDirectedIntentionRequest(
            goal_text="inspect project structure",
            source_candidate_ids=["self_project_structure_candidate:valid"],
        )
    )

    for candidate in bundle.plan_candidates + bundle.todo_candidates:
        assert candidate.review_status == "candidate_only"
        assert candidate.requires_review is True
        assert candidate.execution_enabled is False
        assert candidate.materialized is False
        assert candidate.canonical_promotion_enabled is False
        assert candidate.promoted is False
        assert candidate.risk_assessment.safe_to_execute is False
        assert candidate.risk_assessment.safe_to_materialize is False
        assert candidate.risk_assessment.required_review is True
    for plan in bundle.plan_candidates:
        for step in plan.steps:
            assert step.execution_enabled is False
            assert step.materialized is False
            assert step.risk_assessment.safe_to_execute is False
            assert step.risk_assessment.safe_to_materialize is False


def test_ocel_mapping_contains_directed_intention_types() -> None:
    for object_type in [
        "directed_intention_request",
        "directed_intention_candidate_bundle",
        "plan_candidate",
        "plan_step_candidate",
        "todo_candidate",
        "todo_item_candidate",
        "no_action_candidate",
        "needs_more_input_candidate",
        "intention_source_ref",
        "intention_constraint",
        "intention_risk_assessment",
        "surface_verification_report",
        "project_structure_candidate",
        "summary_candidate",
        "search_result",
        "execution_envelope",
    ]:
        assert object_type in SELF_AWARENESS_OCEL_OBJECT_TYPES

    for event_type in [
        "self_directed_intention_requested",
        "self_directed_intention_policy_checked",
        "self_intention_sources_collected",
        "self_plan_candidate_created",
        "self_todo_candidate_created",
        "self_no_action_candidate_created",
        "self_needs_more_input_candidate_created",
        "self_directed_intention_bundle_created",
        "self_directed_intention_blocked",
    ]:
        assert event_type in SELF_AWARENESS_OCEL_EVENT_TYPES

    for relation_type in [
        "derived_from_request",
        "derived_from_source",
        "uses_verification_report",
        "uses_project_structure_candidate",
        "uses_summary_candidate",
        "uses_search_result",
        "constrained_by",
        "assesses_risk",
        "produces_plan_candidate",
        "produces_todo_candidate",
        "produces_no_action_candidate",
        "produces_needs_more_input_candidate",
        "belongs_to_bundle",
        "recorded_in_envelope",
    ]:
        assert relation_type in SELF_AWARENESS_OCEL_RELATION_TYPES


def test_runtime_source_does_not_contain_forbidden_execution_implementations() -> None:
    paths = [
        Path("src/chanta_core/self_awareness/self_directed_intention.py"),
        Path("src/chanta_core/skills/builtin/self_directed_intention.py"),
    ]
    forbidden = [
        "sub" + "process",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "apply_" + "patch",
        "write_" + "file",
        "memory_auto_" + "promotion",
        "persona_auto_" + "promotion",
        "overlay_auto_" + "mutation",
        "exec(",
        "eval(",
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            assert token not in text
        assert "canonical_promotion_enabled=True" not in text
        assert "promoted=True" not in text
        assert "execution_enabled=True" not in text
        assert "materialized=True" not in text
