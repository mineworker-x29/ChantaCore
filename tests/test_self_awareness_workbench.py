from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    SelfAwarenessCandidateQueueView,
    SelfAwarenessCoverageService,
    SelfAwarenessSafetyBoundaryStatus,
    SelfAwarenessVerificationQueueView,
    SelfAwarenessWorkbenchFinding,
    SelfAwarenessWorkbenchRequest,
    SelfAwarenessWorkbenchService,
    determine_workbench_status,
)
from chanta_core.self_awareness.reports import SelfAwarenessReportService


class FakeOCELStore:
    def fetch_objects_by_type(self, object_type: str):
        data = {
            "plan_candidate": [
                {"object_id": "plan_candidate:1", "object_attrs": {"review_status": "candidate_only"}}
            ],
            "todo_candidate": [
                {"object_id": "todo_candidate:1", "object_attrs": {"review_status": "candidate_only"}}
            ],
            "no_action_candidate": [{"object_id": "no_action_candidate:1", "object_attrs": {}}],
            "needs_more_input_candidate": [{"object_id": "needs_more_input_candidate:1", "object_attrs": {}}],
            "summary_candidate": [{"object_id": "summary_candidate:1", "object_attrs": {}}],
            "project_structure_candidate": [{"object_id": "project_structure_candidate:1", "object_attrs": {}}],
            "surface_verification_report": [
                {"object_id": "surface_verification_report:1", "object_attrs": {"status": "passed"}}
            ],
            "execution_envelope": [
                {
                    "object_id": "execution_envelope:1",
                    "object_attrs": {
                        "skill_id": "skill:self_awareness_plan_candidate",
                        "event_type": "skill_execution_gate_result_recorded",
                        "effect_types": ["read_only_observation"],
                        "blocked": False,
                        "created_at": "2026-01-01T00:00:00Z",
                        "summary": "read-only summary with C:/private/path redacted and secret token",
                        "object_refs": [{"ref_type": "plan_candidate", "ref_id": "C:/private/path/plan_candidate:1"}],
                    },
                }
            ],
        }
        return data.get(object_type, [])


def test_workbench_snapshot_builds_read_only_and_sections() -> None:
    snapshot = SelfAwarenessWorkbenchService(ocel_store=FakeOCELStore()).build_snapshot(
        SelfAwarenessWorkbenchRequest(section="overview", max_recent_items=2)
    )

    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.status == "ok"
    assert snapshot.coverage
    assert snapshot.safety_boundary.dangerous_capability_count == 0
    assert snapshot.safety_boundary.write_enabled_count == 0
    assert snapshot.safety_boundary.shell_enabled_count == 0
    assert snapshot.safety_boundary.network_enabled_count == 0
    assert snapshot.safety_boundary.mcp_enabled_count == 0
    assert snapshot.safety_boundary.plugin_enabled_count == 0
    assert snapshot.safety_boundary.external_harness_enabled_count == 0
    assert snapshot.safety_boundary.memory_mutation_enabled_count == 0
    assert snapshot.safety_boundary.persona_mutation_enabled_count == 0
    assert snapshot.safety_boundary.overlay_mutation_enabled_count == 0
    assert snapshot.candidate_queue.plan_candidate_count == 1
    assert snapshot.candidate_queue.todo_candidate_count == 1
    assert snapshot.candidate_queue.no_action_candidate_count == 1
    assert snapshot.candidate_queue.needs_more_input_candidate_count == 1
    assert snapshot.candidate_queue.summary_candidate_count == 1
    assert snapshot.candidate_queue.project_structure_candidate_count == 1
    assert snapshot.candidate_queue.verification_report_count == 1
    assert snapshot.candidate_queue.promoted_count == 0
    assert snapshot.candidate_queue.materialized_count == 0
    assert snapshot.verification_queue.total_reports == 1
    assert snapshot.verification_queue.passed_count == 1
    assert snapshot.recent_envelopes
    assert len(snapshot.recent_envelopes) <= 2


def test_coverage_includes_v0200_through_v0207_and_contract_only_surfaces() -> None:
    rows = SelfAwarenessCoverageService().build_coverage()
    versions = {row.version for row in rows}
    by_skill = {row.skill_id: row for row in rows}

    for version in [f"v0.20.{index}" for index in range(0, 8)]:
        assert version in versions
    for skill_id in [
        "skill:self_awareness_workspace_inventory",
        "skill:self_awareness_path_verify",
        "skill:self_awareness_text_read",
        "skill:self_awareness_workspace_search",
        "skill:self_awareness_markdown_structure",
        "skill:self_awareness_python_symbols",
        "skill:self_awareness_project_structure",
        "skill:self_awareness_surface_verify",
        "skill:self_awareness_plan_candidate",
        "skill:self_awareness_todo_candidate",
    ]:
        assert by_skill[skill_id].status == "implemented"
        assert by_skill[skill_id].execution_enabled is False
        assert by_skill[skill_id].materialization_enabled is False
        assert by_skill[skill_id].canonical_promotion_enabled is False
        assert by_skill[skill_id].effect_types
    for skill_id in [
        "skill:self_awareness_config_surface",
        "skill:self_awareness_test_surface",
        "skill:self_awareness_capability_registry",
        "skill:self_awareness_runtime_boundary",
    ]:
        assert by_skill[skill_id].status == "contract_only"
        assert by_skill[skill_id].execution_enabled is False


def test_status_rules_for_warnings_and_violations() -> None:
    assert (
        determine_workbench_status(
            [SelfAwarenessWorkbenchFinding("finding:ok", "info", "ok", "ok")],
            SelfAwarenessSafetyBoundaryStatus(),
            SelfAwarenessCandidateQueueView(),
        )
        == "ok"
    )
    assert (
        determine_workbench_status(
            [SelfAwarenessWorkbenchFinding("finding:warning", "warning", "coverage_gap", "gap")],
            SelfAwarenessSafetyBoundaryStatus(),
            SelfAwarenessCandidateQueueView(),
        )
        == "warning"
    )
    assert (
        determine_workbench_status(
            [SelfAwarenessWorkbenchFinding("finding:error", "error", "verification_failed", "failed")],
            SelfAwarenessSafetyBoundaryStatus(),
            SelfAwarenessCandidateQueueView(),
        )
        == "violation"
    )
    assert (
        determine_workbench_status(
            [],
            SelfAwarenessSafetyBoundaryStatus(dangerous_capability_count=1, status="violation"),
            SelfAwarenessCandidateQueueView(),
        )
        == "violation"
    )
    assert (
        determine_workbench_status(
            [],
            SelfAwarenessSafetyBoundaryStatus(),
            SelfAwarenessCandidateQueueView(promoted_count=1),
        )
        == "violation"
    )
    assert (
        determine_workbench_status(
            [],
            SelfAwarenessSafetyBoundaryStatus(),
            SelfAwarenessCandidateQueueView(materialized_count=1),
        )
        == "violation"
    )


def test_envelope_view_is_sanitized() -> None:
    snapshot = SelfAwarenessWorkbenchService(ocel_store=FakeOCELStore()).build_snapshot()
    envelope = snapshot.recent_envelopes[0]

    assert "C:/private/path" not in envelope.summary
    assert "secret" not in envelope.summary.casefold()
    assert "raw file content" not in envelope.summary.casefold()
    assert all("/" not in ref["ref_id"] for ref in envelope.object_refs)


def test_cli_workbench_sections(capsys) -> None:
    for args in [
        ["self-awareness", "workbench"],
        ["self-awareness", "workbench", "--section", "coverage"],
        ["self-awareness", "workbench", "--section", "candidates"],
        ["self-awareness", "workbench", "--section", "verification"],
        ["self-awareness", "workbench", "--section", "risks"],
    ]:
        assert main(args) == 0
        output = capsys.readouterr().out
        assert "Self-Awareness Workbench" in output
        assert "status=" in output
        assert "read_only=true" in output
        assert "mutation_performed=false" in output
        assert "dangerous_capability_count=0" in output
        assert "promoted_count=0" in output
        assert "materialized_count=0" in output
        assert "ChantaResearchGroup" + "_Members" not in output
        assert "raw_file_content_printed=false" in output


def test_pig_and_ocpx_workbench_coverage() -> None:
    reports = SelfAwarenessReportService()
    pig = reports.build_pig_report()
    ocpx = reports.build_ocpx_projection()

    assert pig["version"] == "0.20.9"
    assert pig["state"] == "self_awareness_foundation_v1_consolidated"
    assert pig["workbench"] == "implemented_read_only_operator_surface"
    assert pig["read_only"] is True
    assert pig["mutation_performed"] is False
    assert pig["approval_enabled"] is False
    assert pig["promotion_enabled"] is False
    assert pig["materialization_enabled"] is False
    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    for read_model_type in [
        "self_awareness_workbench_snapshot",
        "self_awareness_coverage_row",
        "self_awareness_candidate_queue_view",
        "self_awareness_verification_queue_view",
        "self_awareness_safety_boundary_status",
    ]:
        assert read_model_type in ocpx["read_model_types"]
    assert "read_only_observation" in ocpx["effect_types"]
