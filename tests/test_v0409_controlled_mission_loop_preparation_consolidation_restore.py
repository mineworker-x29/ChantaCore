from __future__ import annotations

import re
from pathlib import Path

from chanta_core.agent_runtime.repair_mission_loop_v040_consolidation import (
    BOUNDARY_NAMES,
    CLOSED_RUNTIME_CAPABILITIES,
    INTEGRATED_DOC_PATH,
    OPEN_METADATA_PREVIEW_CAPABILITIES,
    REQUIRED_FALSE_FLAGS,
    REQUIRED_V041_COMPONENTS,
    SAFETY_CLOSURE_SURFACES,
    V040ConsolidationReadinessLevel,
    V040ConsolidationStatus,
    assess_v041_acceleration,
    build_v040_artifact_inventory,
    build_v040_boundary_inventory,
    build_v040_capability_matrix,
    build_v040_restore_index,
    build_v040_safety_closure_register,
    build_v040_stage_summaries,
    build_v040_test_coverage_summary,
    build_v041_standalone_runtime_gap_register,
    create_v0409_consolidation_audit_record,
    create_v0409_integrated_restore_context_snapshot,
    create_v0409_integrated_restore_document_manifest,
    create_v0409_integrated_restore_packet,
    create_v0409_readiness_report,
    create_v0409_safety_report,
    create_v040_stage_summary,
    create_v040_standalone_runtime_still_closed_record,
    create_v0410_default_personal_profile_runtime_handoff,
    create_v041_default_personal_smoke_scenario,
    create_v041_default_personal_startup_plan,
    create_v041_runtime_opening_gate,
    integrated_restore_packet_uses_single_doc,
    v0409_readiness_preserves_no_unsafe_runtime,
    v040_boundary_inventory_preserves_no_runtime_authority,
    v040_capability_matrix_is_not_permission_grant,
    v040_safety_closure_register_preserves_closed,
    v040_standalone_runtime_record_preserves_closed,
    v041_acceleration_assessment_is_non_authoritative,
    v041_gap_register_is_design_only,
    v041_runtime_opening_gate_is_design_only,
    v041_smoke_scenario_is_not_executed,
)


def test_v0409_consolidation_status_values_declared() -> None:
    assert {item.value for item in V040ConsolidationStatus} == {
        "unknown",
        "draft",
        "consolidated",
        "consolidated_with_notes",
        "consolidated_with_gaps",
        "v041_handoff_ready",
        "blocked",
        "rejected",
        "review_required",
    }


def test_v0409_consolidation_readiness_levels_declared() -> None:
    assert {item.value for item in V040ConsolidationReadinessLevel} == {
        "not_ready",
        "boundary_preparation_complete",
        "rehearsal_preparation_complete",
        "negative_gate_complete",
        "checkpoint_hardening_complete",
        "provider_prompt_boundary_complete",
        "verifier_subagent_boundary_complete",
        "coverage_consolidation_complete",
        "cli_preview_surface_complete",
        "v040_final_consolidation_complete",
        "v041_design_handoff_ready",
        "blocked",
    }


def test_v0409_stage_summary_covers_v0400_through_v0408() -> None:
    summaries = build_v040_stage_summaries()

    assert {summary.version for summary in summaries} == {f"v0.40.{index}" for index in range(9)}
    for summary in summaries:
        assert summary.release_name
        assert summary.primary_purpose
        assert summary.opened_capabilities
        assert summary.closed_capabilities
        assert summary.implementation_artifact_refs
        assert summary.test_refs
        assert summary.doc_refs
        assert summary.handoff_target
        assert "runtime authority remains closed" in summary.safety_notes


def test_v0409_capability_matrix_lists_open_metadata_preview_and_closed_runtime_capabilities() -> None:
    matrix = build_v040_capability_matrix()

    assert set(OPEN_METADATA_PREVIEW_CAPABILITIES).issubset(matrix.open_metadata_preview_capabilities)
    assert set(CLOSED_RUNTIME_CAPABILITIES).issubset(matrix.closed_runtime_capabilities)


def test_v0409_capability_matrix_is_not_permission_grant() -> None:
    matrix = build_v040_capability_matrix()

    assert matrix.permission_grant is False
    assert v040_capability_matrix_is_not_permission_grant(matrix)


def test_v0409_capability_matrix_is_not_production_certification() -> None:
    assert build_v040_capability_matrix().production_certified is False


def test_v0409_boundary_inventory_lists_all_major_v040_boundaries() -> None:
    inventory = build_v040_boundary_inventory()
    names = {boundary["boundary_name"] for boundary in inventory.boundaries}

    assert set(BOUNDARY_NAMES) == names
    assert inventory.all_major_boundaries_listed is True


def test_v0409_boundary_inventory_never_grants_runtime_authority() -> None:
    inventory = build_v040_boundary_inventory()

    assert v040_boundary_inventory_preserves_no_runtime_authority(inventory)


def test_v0409_safety_closure_register_closes_all_unsafe_runtime_surfaces() -> None:
    register = build_v040_safety_closure_register()

    assert set(SAFETY_CLOSURE_SURFACES) == set(register.closure_items)
    assert v040_safety_closure_register_preserves_closed(register)
    for item in register.closure_items.values():
        assert item["closed"] is True
        assert item["readiness_flag"] is False


def test_v0409_artifact_inventory_lists_modules_tests_and_docs() -> None:
    inventory = build_v040_artifact_inventory()

    assert "src/chanta_core/agent_runtime/repair_mission_loop_v040_consolidation.py" in inventory.implementation_modules
    assert "tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py" in inventory.test_files
    assert INTEGRATED_DOC_PATH in inventory.documentation_files


def test_v0409_test_coverage_summary_records_focused_and_regression_commands() -> None:
    summary = build_v040_test_coverage_summary()

    assert summary.focused_v0409_test.endswith("test_v0409_controlled_mission_loop_preparation_consolidation_restore.py")
    assert summary.regression_v0408.endswith("test_v0408_cli_execution_test_preview_surface_restore.py")
    assert summary.regression_v0399.endswith("test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py")


def test_v0409_restore_index_confirms_copy_paste_restore_prompt_and_no_standalone_claim() -> None:
    index = build_v040_restore_index()

    assert INTEGRATED_DOC_PATH in index.integrated_restore_docs
    assert index.copy_paste_restore_prompt_exists is True
    assert index.capability_matrix_exists is True
    assert index.safety_flag_table_exists is True
    assert index.next_handoff_exists is True
    assert index.does_not_claim_standalone_runtime_opened is True


def test_v0409_standalone_runtime_still_closed_record_all_runtime_components_false() -> None:
    record = create_v040_standalone_runtime_still_closed_record()

    assert v040_standalone_runtime_record_preserves_closed(record)


def test_v0409_v041_required_runtime_components_include_profile_prompt_entry_orchestrator_agentloop_skills_response_trace() -> None:
    register = build_v041_standalone_runtime_gap_register()
    names = {component.component_name for component in register.required_components}

    assert set(REQUIRED_V041_COMPONENTS) == names


def test_v0409_v041_gap_register_marks_standalone_runtime_not_started() -> None:
    register = build_v041_standalone_runtime_gap_register()

    assert register.standalone_runtime_started is False
    assert register.ready_for_v041_runtime_execution is False
    assert register.ready_for_first_smoke_run is False
    assert v041_gap_register_is_design_only(register)


def test_v0409_v041_startup_plan_contains_v0410_through_v0416_sequence() -> None:
    plan = create_v041_default_personal_startup_plan()

    assert plan.recommended_sequence == (
        "v0.41.0",
        "v0.41.1",
        "v0.41.2",
        "v0.41.3",
        "v0.41.4",
        "v0.41.5",
        "v0.41.6",
    )
    for stage in plan.stages:
        assert stage["purpose"]
        assert stage["required_artifacts"]
        assert stage["required_tests"]
        assert stage["opens"]
        assert stage["still_closed"]
        assert stage["withdrawal_conditions"]


def test_v0409_v041_smoke_scenario_is_design_only_and_not_executed() -> None:
    scenario = create_v041_default_personal_smoke_scenario()

    assert "Vera" in scenario.input_text
    assert "DefaultPersonalProfileRuntime" in scenario.expected_runtime_path
    assert v041_smoke_scenario_is_not_executed(scenario)


def test_v0409_v041_runtime_opening_gate_does_not_open_runtime_in_v0409() -> None:
    gate = create_v041_runtime_opening_gate()

    assert "profile_loaded" in gate.required_gates
    assert gate.required_gates["smoke_scenario_passed"] is False
    assert v041_runtime_opening_gate_is_design_only(gate)


def test_v0409_v041_acceleration_assessment_is_non_authoritative() -> None:
    assessment = assess_v041_acceleration()

    assert assessment.earliest_candidate_target == "v0.41.6"
    assert assessment.recommendation == "keep_conservative_target"
    assert v041_acceleration_assessment_is_non_authoritative(assessment)


def test_v0409_consolidation_audit_confirms_no_runtime_expansion() -> None:
    audit = create_v0409_consolidation_audit_record()

    assert audit.all_v040_stages_summarized is True
    assert audit.all_major_boundaries_inventoried is True
    assert audit.all_unsafe_runtime_capabilities_closed is True
    assert audit.no_runtime_expansion_introduced is True
    assert audit.no_standalone_runtime_opened is True
    assert audit.no_production_certification_claimed is True


def test_v0409_safety_report_keeps_runtime_and_standalone_false() -> None:
    report = create_v0409_safety_report()

    assert report.safe_for_v0409_consolidation is True
    assert report.safe_for_runtime_execution is False
    assert report.safe_for_cli_runtime_execution is False
    assert report.safe_for_model_provider_invocation is False
    assert report.safe_for_subagent_invocation is False
    assert report.safe_for_standalone_default_personal_runtime is False
    assert report.production_certified is False
    assert report.ready_for_v041_design_handoff is True


def test_v0409_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_v0409_readiness_report()

    assert report.v040_final_consolidation_defined is True
    assert report.v041_handoff_ready is True
    assert v0409_readiness_preserves_no_unsafe_runtime(report)
    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False


def test_v0409_integrated_restore_snapshot_lists_full_v040_chain_and_open_closed_capabilities() -> None:
    snapshot = create_v0409_integrated_restore_context_snapshot()

    assert len(snapshot.baseline_versions) == 10
    assert snapshot.baseline_versions[0].startswith("v0.40.0")
    assert snapshot.baseline_versions[-1].startswith("v0.40.9")
    assert "v040_final_consolidation" in snapshot.open_capabilities
    assert "standalone_default_personal_runtime" in snapshot.closed_capabilities


def test_v0409_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = create_v0409_integrated_restore_packet()

    assert integrated_restore_packet_uses_single_doc(packet)


def test_v0409_restore_packet_marks_separate_restore_doc_created_false() -> None:
    assert create_v0409_integrated_restore_packet().separate_restore_doc_created is False


def test_v0409_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = create_v0409_integrated_restore_document_manifest()

    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0409_integrated_document_exists_and_has_required_restore_sections() -> None:
    doc = Path(INTEGRATED_DOC_PATH)
    text = doc.read_text(encoding="utf-8")

    for section in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Version Chain Summary",
        "v0.40 Final Stage Summary",
        "v0.40 Final Capability Matrix",
        "v0.40 Boundary Inventory",
        "v0.40 Safety Closure Register",
        "v0.40 Artifact Inventory",
        "v0.40 Test Coverage Summary",
        "v0.40 Restore Index",
        "Standalone Runtime Still-Closed Record",
        "Why v0.40.9 Is Still Not Standalone",
        "v0.41 Required Runtime Components",
        "v0.41 Standalone Runtime Gap Register",
        "v0.41 Default Personal Startup Plan",
        "v0.41 Default Personal Smoke Scenario",
        "v0.41 Runtime Opening Gates",
        "v0.41 Acceleration Assessment",
        "Capability Matrix",
        "Safety Flag Canonical Values",
        "How To Verify This State",
        "Required Test Commands",
        "Withdrawal Conditions",
        "v0.41.0 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert section in text


def test_v0409_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    assert "You are continuing ChantaCore after v0.40.9." in text
    assert "v0.41.0 Default Personal Profile Runtime" in text


def test_v0409_no_separate_v0409_restore_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.9_restore_document.md").exists()


def test_v0409_no_separate_v0409_release_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.9_controlled_mission_loop_preparation_consolidation.md").exists()
    assert not Path("docs/versions/v0.40/v0.40.9_v041_handoff.md").exists()


def test_v0409_v0410_handoff_targets_default_personal_profile_runtime() -> None:
    handoff = create_v0410_default_personal_profile_runtime_handoff()

    assert handoff.target_version == "v0.41.0 Default Personal Profile Runtime"
    assert "create DefaultPersonalProfileRuntime artifact" in handoff.recommended_focus
    assert "no production certification" in handoff.recommended_focus


def test_v0409_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/agent_runtime/repair_mission_loop_v040_consolidation.py").read_text(
        encoding="utf-8"
    )
    forbidden = (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "requests",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "anthropic",
        "ollama",
        "lmstudio",
        "apply_patch",
        "git apply",
        "git worktree",
        "api_key",
        "secret",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "prompt_submit",
        "provider_invoke",
        "client_create",
        "pytest",
        "unittest",
        "os.remove",
        "Path.write_text",
        "open(",
    )
    for pattern in forbidden:
        assert pattern not in source

    credential_lines = [line for line in source.splitlines() if re.search(r"credential", line, re.I)]
    assert credential_lines
    assert all(
        "credential_access" in line
        or "safe_for_credential_access" in line
        or '"no network/dependency install/credential access is introduced"' in line
        for line in credential_lines
    )


def test_v0409_stage_summaries_to_capability_matrix_to_safety_closure_flow() -> None:
    summaries = build_v040_stage_summaries()
    matrix = build_v040_capability_matrix()
    closure = build_v040_safety_closure_register()

    assert len(summaries) == 9
    assert matrix.consolidation_status == "v041_handoff_ready"
    assert closure.all_closures_confirmed is True


def test_v0409_v041_gap_register_to_startup_plan_to_handoff_flow() -> None:
    register = build_v041_standalone_runtime_gap_register()
    plan = create_v041_default_personal_startup_plan()
    handoff = create_v0410_default_personal_profile_runtime_handoff()

    assert len(register.required_components) == len(REQUIRED_V041_COMPONENTS)
    assert plan.recommended_sequence[0] == "v0.41.0"
    assert handoff.target_version.startswith("v0.41.0")


def test_v0409_restore_packet_is_suitable_for_new_session_handoff() -> None:
    packet = create_v0409_integrated_restore_packet()
    manifest = create_v0409_integrated_restore_document_manifest()

    assert packet.restore_sections
    assert manifest.suitable_for_new_session_handoff is True


def test_v0409_create_single_stage_summary_accepts_v0400() -> None:
    summary = create_v040_stage_summary("v0.40.0")

    assert summary.version == "v0.40.0"
    assert "mission_loop_boundary" in summary.opened_capabilities
