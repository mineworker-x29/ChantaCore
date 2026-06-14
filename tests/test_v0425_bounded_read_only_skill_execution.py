from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_read_only_skills as v0425
from chanta_core.personal_runtime.default_personal_home_quickstart import run_v042_quickstart


def _prepared_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    result = run_v042_quickstart(explicit_home=str(home), with_mock_run=True)
    assert result.exit_code == 0
    return home


def _run_skill(home: Path, skill_id: str, **args: object) -> v0425.V042SkillRunCommandResult:
    return v0425.create_v042_skill_run_command_result(
        v0425.create_v042_skill_run_command_input(skill_id, home_path=str(home), args=args)
    )


def test_v0425_skill_execution_gate_status_values_declared() -> None:
    assert {item.value for item in v0425.V042SkillExecutionGateStatus} == {
        "open_for_bounded_read_only",
        "closed",
        "denied",
        "blocked",
        "unknown",
    }


def test_v0425_skill_capability_classes_declared() -> None:
    assert {item.value for item in v0425.V042SkillCapabilityClass} == {
        "metadata_read",
        "status_read",
        "trace_read",
        "run_read",
        "session_read",
        "config_read",
        "safety_read",
        "provider_read_no_call",
        "file_read_arbitrary",
        "file_write",
        "shell",
        "provider_call",
        "prompt_submit",
        "function_call",
        "tool_call",
        "subagent",
        "memory_write",
        "unknown",
    }


def test_v0425_skill_mutability_classes_declared() -> None:
    assert {item.value for item in v0425.V042SkillMutabilityClass} == {
        "read_only",
        "trace_append_only",
        "mutating",
        "destructive",
        "unknown",
    }


def test_v0425_skill_boundary_classes_declared() -> None:
    assert {item.value for item in v0425.V042SkillBoundaryClass} == {
        "bounded_home",
        "bounded_profile",
        "bounded_trace_store",
        "bounded_session_store",
        "bounded_config",
        "arbitrary_path",
        "network",
        "shell",
        "unknown",
    }


def test_v0425_skill_execution_status_values_declared() -> None:
    assert {item.value for item in v0425.V042SkillExecutionStatus} == {
        "completed",
        "denied",
        "blocked",
        "failed",
        "skipped",
        "dry_run",
    }


def test_v0425_skill_risk_levels_declared() -> None:
    assert {item.value for item in v0425.V042SkillRiskLevel} == {"low", "moderate", "high", "forbidden", "unknown"}


def test_v0425_registry_opens_only_bounded_read_only_execution_gate() -> None:
    registry = v0425.build_v042_read_only_skill_registry()
    assert registry.execution_gate_status == "open_for_bounded_read_only"
    assert registry.provider_calls_allowed is False
    assert registry.prompt_submission_allowed is False
    assert registry.shell_execution_allowed is False
    assert registry.subagent_allowed is False
    assert registry.production_certified is False


def test_v0425_registry_contains_required_executable_safe_skills() -> None:
    registry = v0425.build_v042_read_only_skill_registry()
    assert set(v0425.EXECUTABLE_SKILL_IDS).issubset(set(registry.executable_skill_ids))


def test_v0425_registry_contains_required_denied_unsafe_skills() -> None:
    registry = v0425.build_v042_read_only_skill_registry()
    assert set(v0425.DENIED_SKILL_IDS).issubset(set(registry.denied_skill_ids))


def test_v0425_executable_skill_definitions_never_call_provider_submit_prompt_execute_shell_or_invoke_subagent() -> None:
    registry = v0425.build_v042_read_only_skill_registry()
    for skill in registry.skills:
        if skill.execution_allowed:
            assert skill.requires_provider_call is False
            assert skill.submits_prompt is False
            assert skill.executes_shell is False
            assert skill.allows_network is False


def test_v0425_executable_skill_definitions_do_not_mutate_workspace_memory_or_session() -> None:
    for skill_id in v0425.EXECUTABLE_SKILL_IDS:
        skill = v0425.create_v042_read_only_skill_definition(skill_id)
        assert skill.mutates_workspace is False
        assert skill.mutates_memory is False
        assert skill.mutates_session is False


def test_v0425_executable_skill_definitions_disallow_arbitrary_path_and_network() -> None:
    for skill_id in v0425.EXECUTABLE_SKILL_IDS:
        skill = v0425.create_v042_read_only_skill_definition(skill_id)
        assert skill.allows_arbitrary_path is False
        assert skill.allows_network is False
        assert skill.risk_level == "low"


def test_v0425_denied_skill_definitions_have_safe_alternatives() -> None:
    for skill_id in v0425.DENIED_SKILL_IDS:
        skill = v0425.create_v042_read_only_skill_definition(skill_id)
        assert skill.execution_allowed is False
        assert skill.risk_level in {"forbidden", "high"}
        assert skill.safe_alternative


def test_v0425_skill_input_schema_disallows_arbitrary_path_shell_text_and_provider_prompt() -> None:
    for skill_id in (*v0425.EXECUTABLE_SKILL_IDS, *v0425.DENIED_SKILL_IDS):
        schema = v0425.create_v042_skill_input_schema(skill_id)
        assert schema.arbitrary_path_allowed is False
        assert schema.raw_shell_text_allowed is False
        assert schema.provider_prompt_allowed is False


def test_v0425_skill_execution_plan_for_profile_status_is_safe_and_bounded(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    plan = v0425.create_v042_skill_execution_plan(v0425.create_v042_skill_execution_request("profile_status", home_path=str(home)))
    assert plan.safe_to_execute is True
    assert plan.resolved_home_path == str(home)
    assert plan.outside_home_paths == ()
    assert plan.will_call_provider is False
    assert plan.will_append_trace is True


def test_v0425_skill_execution_plan_for_trace_timeline_requires_limit_and_no_provider_call(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    plan = v0425.create_v042_skill_execution_plan(
        v0425.create_v042_skill_execution_request("trace_timeline", home_path=str(home), args={"limit": 10})
    )
    assert plan.safe_to_execute is True
    assert plan.input_schema is not None
    assert plan.input_schema.max_limit == 200
    assert plan.will_call_provider is False


def test_v0425_skill_execution_plan_for_unknown_skill_is_denied(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    plan = v0425.create_v042_skill_execution_plan(v0425.create_v042_skill_execution_request("unknown_skill", home_path=str(home)))
    assert plan.safe_to_execute is False
    assert plan.denial_reason == "unknown_skill"


def test_v0425_skill_execution_plan_for_shell_command_is_denied(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    plan = v0425.create_v042_skill_execution_plan(v0425.create_v042_skill_execution_request("shell_command", home_path=str(home)))
    assert plan.safe_to_execute is False
    assert plan.will_execute_shell is False
    assert plan.denial_reason == "execution_not_allowed"


def test_v0425_skill_list_result_is_read_only_and_non_provider() -> None:
    result = v0425.create_v042_skill_list_result(v0425.create_v042_skill_list_request())
    assert result.executable_count == len(v0425.EXECUTABLE_SKILL_IDS)
    assert result.denied_count == len(v0425.DENIED_SKILL_IDS)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.production_certified is False


def test_v0425_skill_inspect_result_is_read_only_and_non_provider() -> None:
    result = v0425.create_v042_skill_inspect_result(v0425.create_v042_skill_inspect_request("profile_status"))
    assert result.found is True
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.production_certified is False


def test_v0425_skill_run_profile_status_completes_without_provider_prompt_shell_subagent_or_mutation(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "profile_status")
    assert result.execution_result is not None
    execution = result.execution_result
    assert execution.skill_executed is True
    assert execution.provider_invoked is False
    assert execution.prompt_submitted is False
    assert execution.shell_executed is False
    assert execution.subagent_invoked is False
    assert execution.workspace_mutated is False
    assert execution.memory_mutated is False
    assert execution.session_mutated is False
    assert execution.production_certified is False


def test_v0425_skill_run_provider_status_completes_without_provider_call(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "provider_status")
    assert result.execution_result is not None
    assert result.provider_invoked is False
    assert "provider_invoked: false" in result.rendered_text


def test_v0425_skill_run_provider_config_show_redacts_secrets(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "provider_config_show")
    assert result.execution_result is not None
    assert result.execution_result.data["secret_values_redacted"] is True
    assert "sk-" not in result.rendered_text


def test_v0425_skill_run_trace_summary_reads_trace_without_mutation_except_optional_trace_record(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "trace_summary")
    assert result.execution_result is not None
    assert result.execution_result.trace_record is not None
    assert result.workspace_mutated is False
    assert result.provider_invoked is False


def test_v0425_skill_run_trace_timeline_respects_limit(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "trace_timeline", limit=3)
    assert result.execution_result is not None
    assert result.execution_result.data["event_count"] <= 3


def test_v0425_skill_run_run_report_last_reads_report_without_prompt(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "run_report_last")
    assert result.execution_result is not None
    assert result.prompt_submitted is False
    assert result.execution_result.data["found"] is True


def test_v0425_skill_run_run_history_respects_limit(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "run_history", limit=1)
    assert result.execution_result is not None
    assert result.execution_result.data["run_count"] <= 1


def test_v0425_skill_run_session_show_respects_turn_limit_and_no_session_mutation(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "session_show", target="last", max_turns=1)
    assert result.execution_result is not None
    assert result.execution_result.data["session_turn_count"] <= 1
    assert result.execution_result.session_mutated is False


def test_v0425_skill_run_safety_summary_reports_high_risk_counts(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "safety_summary")
    assert result.execution_result is not None
    data = result.execution_result.data
    assert data["shell_execution_count"] == 0
    assert data["subagent_invocation_count"] == 0
    assert data["production_certification_count"] == 0


def test_v0425_skill_run_config_view_is_bounded_and_redacted(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "config_view")
    assert result.execution_result is not None
    assert result.execution_result.data["secret_values_redacted"] is True
    assert result.execution_result.workspace_mutated is False


def test_v0425_skill_denial_result_for_unsafe_skill_never_executes_shell(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "shell_command")
    assert result.denial_result is not None
    assert result.execution_result is None
    assert result.denial_result.shell_executed is False
    assert result.denial_result.provider_invoked is False
    assert result.denial_result.workspace_mutated is False
    assert "safe_alternative" in result.rendered_text


def test_v0425_skill_execution_trace_record_is_pi_reviewable_and_high_risk_counts_zero(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "profile_status")
    trace = result.execution_result.trace_record if result.execution_result else None
    assert trace is not None
    assert trace.event_kind == "read_only_skill_executed"
    assert trace.provider_invoked is False
    assert trace.prompt_submitted is False
    assert trace.shell_executed is False
    assert trace.subagent_invoked is False
    assert trace.workspace_mutated is False
    assert trace.memory_mutated is False
    assert trace.session_mutated is False
    assert trace.production_certified is False


def test_v0425_skill_pi_review_record_marks_process_event_reconstructable() -> None:
    review = v0425.create_v042_skill_pi_review_record("profile_status")
    assert review.reconstructable_as_process_event is True
    assert review.input_bounded is True
    assert review.output_bounded is True
    assert review.high_risk_counts_zero is True


def test_v0425_skill_evidence_view_contains_no_provider_prompt_shell_subagent_or_workspace_mutation(tmp_path: Path) -> None:
    result = _run_skill(_prepared_home(tmp_path), "profile_status")
    view = v0425.create_v042_skill_evidence_view(result.execution_result)
    assert view.provider_invoked is False
    assert view.prompt_submitted is False
    assert view.shell_executed is False
    assert view.subagent_invoked is False
    assert view.workspace_mutated is False
    assert view.production_certified is False


def test_v0425_skill_closed_capability_matrix_keeps_high_risk_capabilities_closed() -> None:
    matrix = v0425.create_v042_skill_closed_capability_matrix()
    assert matrix.shell_execution_closed is True
    assert matrix.file_write_closed is True
    assert matrix.file_read_arbitrary_closed is True
    assert matrix.provider_call_closed_for_skills is True
    assert matrix.prompt_submission_closed_for_skills is True
    assert matrix.function_calling_closed is True
    assert matrix.tool_calling_closed is True
    assert matrix.subagent_closed is True
    assert matrix.memory_write_closed is True
    assert matrix.broad_scan_closed is True
    assert matrix.production_certified is False


def test_v0425_chat_skill_command_policy_is_bounded_or_marked_future() -> None:
    policy = v0425.create_v042_chat_skill_command_policy()
    assert policy.chat_skill_command_supported is False
    assert policy.arbitrary_args_allowed is False
    assert policy.provider_call_allowed is False
    assert policy.prompt_submission_allowed is False
    assert policy.shell_allowed is False
    assert policy.subagent_allowed is False


def test_v0425_readiness_report_sets_bounded_skill_flags_true() -> None:
    report = v0425.create_v0425_readiness_report()
    assert report.bounded_read_only_skill_execution_ready is True
    assert report.skill_list_command_ready is True
    assert report.skill_inspect_command_ready is True
    assert report.skill_run_command_ready is True
    assert report.executable_safe_skill_subset_ready is True
    assert report.unsafe_skill_denial_ready is True
    assert report.skill_execution_trace_evidence_ready is True
    assert report.skill_pi_review_record_ready is True
    assert report.skill_output_render_policy_ready is True
    assert report.skill_safety_report_ready is True
    assert report.integrated_restore_document_ready is True
    assert report.v0426_handoff_ready is True


def test_v0425_readiness_report_keeps_shell_arbitrary_file_provider_prompt_tool_function_agentloop_subagent_memory_and_production_flags_false() -> None:
    report = v0425.create_v0425_readiness_report()
    assert report.ready_for_shell_execution is False
    assert report.ready_for_file_write is False
    assert report.ready_for_arbitrary_file_read is False
    assert report.ready_for_broad_filesystem_scan is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_provider_call_from_skills is False
    assert report.ready_for_prompt_submission_from_skills is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_memory_write is False
    assert report.production_certified is False


def test_v0425_v0426_handoff_targets_diagnostic_bundle_and_feedback_loop() -> None:
    handoff = v0425.create_v0426_diagnostic_bundle_feedback_handoff()
    assert handoff.target_version == "v0.42.6 Diagnostic Bundle & User Feedback Loop"
    assert "chanta-cli report bundle" in handoff.recommended_focus
    assert handoff.production_certified is False


def test_v0425_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0425.create_v0425_integrated_restore_context_snapshot()
    assert "bounded_read_only_skill_execution_gate" in snapshot.open_capabilities
    assert "skill_run_command" in snapshot.open_capabilities
    assert "shell_execution" in snapshot.closed_capabilities
    assert "provider_call_from_skills" in snapshot.closed_capabilities
    assert "production_certification" in snapshot.closed_capabilities


def test_v0425_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0425.create_v0425_integrated_restore_packet()
    assert packet.single_integrated_doc_path == "docs/versions/v0.42/v0.42.5_bounded_read_only_skill_execution_restore.md"


def test_v0425_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = v0425.create_v0425_integrated_restore_packet()
    assert packet.separate_restore_doc_created is False


def test_v0425_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0425.create_v0425_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0425_integrated_document_exists_and_has_required_restore_sections() -> None:
    path = Path("docs/versions/v0.42/v0.42.5_bounded_read_only_skill_execution_restore.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for heading in [
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Project Context for New Codex Session",
        "v0.41.6 User Test Baseline",
        "v0.42.0 UX Baseline Summary",
        "v0.42.1 Home / Quickstart Summary",
        "v0.42.2 Provider Setup Summary",
        "v0.42.3 Trace / Run History Summary",
        "v0.42.4 Chat Shell Summary",
        "Bounded Read-only Skill Execution Summary",
        "Skill Execution Gate Contract",
        "Executable Skill Subset",
        "Denied Skill Subset",
        "Skill Input Schema Contract",
        "Skill Run Command Contract",
        "Skill Trace Evidence Contract",
        "Skill Denial Contract",
        "Skill PI Review Contract",
        "Skill Safety Boundary",
        "Chat Skill Command Policy",
        "Runtime Opening Status",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Expected Test Interpretation",
        "Withdrawal Conditions",
        "v0.42.6 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]:
        assert f"## {heading}" in text


def test_v0425_integrated_document_contains_skill_execution_examples_and_copy_paste_restore_prompt() -> None:
    text = Path("docs/versions/v0.42/v0.42.5_bounded_read_only_skill_execution_restore.md").read_text(encoding="utf-8")
    assert "chanta-cli skill list" in text
    assert "chanta-cli skill inspect <skill_id>" in text
    assert "chanta-cli skill run <skill_id>" in text
    assert "chanta-cli skill run shell_command" in text
    assert "You are continuing ChantaCore after v0.42.5." in text


def test_v0425_no_separate_v0425_restore_or_skill_documents_created() -> None:
    forbidden = [
        "docs/versions/v0.42/v0.42.5_restore_document.md",
        "docs/versions/v0.42/v0.42.5_read_only_skill_execution.md",
        "docs/versions/v0.42/v0.42.5_skill_gate_contract.md",
        "docs/versions/v0.42/v0.42.5_skill_user_guide.md",
    ]
    for path in forbidden:
        assert not Path(path).exists()


def test_v0425_no_forbidden_runtime_call_patterns_except_bounded_trace_event_append_and_bounded_reads() -> None:
    module_text = Path("src/chanta_core/personal_runtime/default_personal_read_only_skills.py").read_text(encoding="utf-8")
    cli_text = Path("src/chanta_core/cli/main.py").read_text(encoding="utf-8")
    combined = module_text + "\n" + cli_text
    for forbidden in [
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "openai",
        "anthropic",
        "ollama",
        "lmstudio",
        "apply_patch",
        "git apply",
        "git worktree",
        "invoke_subagent(",
        "run_subagent(",
        "create_child_session(",
        "spawn_agent(",
        "pytest",
        "unittest",
    ]:
        assert forbidden not in combined


def test_v0425_cli_skill_list_inspect_run_and_denial(tmp_path: Path, monkeypatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["skill", "list"]) == 0
    assert cli_main(["skill", "inspect", "profile_status"]) == 0
    assert cli_main(["skill", "run", "profile_status"]) == 0
    assert cli_main(["skill", "run", "trace_summary"]) == 0
    assert cli_main(["skill", "run", "shell_command"]) == 1
