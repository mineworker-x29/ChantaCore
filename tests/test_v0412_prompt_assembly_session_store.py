from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.personal_runtime.default_personal_cli_bootstrap import create_default_personal_init_plan, create_default_personal_init_request, execute_default_personal_init_plan
from chanta_core.personal_runtime.default_personal_prompt_session import (
    CLOSED_CAPABILITIES,
    INTEGRATED_DOC_PATH,
    OPEN_CAPABILITIES,
    PROMPT_BLOCK_ORDER,
    REQUIRED_FALSE_FLAGS,
    V0416_TARGET_COMMANDS,
    PromptAssemblyInput,
    PromptAssemblyStatus,
    PromptBlockKind,
    PromptPreviewCommandInput,
    PromptSourceKind,
    assemble_default_personal_prompt,
    create_default_personal_session,
    create_default_personal_session_create_request,
    create_default_personal_session_list_request,
    create_default_personal_session_store_config,
    create_default_personal_session_store_safety_report,
    create_prompt_assembly_policy,
    create_prompt_preview_command_result,
    create_prompt_source_provenance,
    create_project_instruction_ref,
    create_read_only_skill_policy_block,
    create_restore_summary_block,
    create_safety_invariant_block,
    create_soul_role_domain_binding,
    create_v0412_integrated_restore_context_snapshot,
    create_v0412_integrated_restore_document_manifest,
    create_v0412_integrated_restore_packet,
    create_v0412_readiness_report,
    create_v0413_provider_probe_skill_registry_handoff,
    create_v0416_user_test_target_update,
    integrated_restore_packet_uses_single_doc,
    list_default_personal_sessions,
    prompt_assembly_result_preserves_preview_only,
    session_create_result_preserves_runtime_closed,
    session_safety_report_preserves_closed,
    v0412_readiness_preserves_closed_runtime,
    DefaultPersonalSessionTurnRecord,
)


def _init_profile(home: Path) -> None:
    request = create_default_personal_init_request(str(home))
    execute_default_personal_init_plan(request, create_default_personal_init_plan(request))


def test_v0412_prompt_block_kinds_declared() -> None:
    assert {item.value for item in PromptBlockKind} == {
        "safety_invariant",
        "soul",
        "profile_role",
        "domain_instruction",
        "project_instruction",
        "read_only_skill_policy",
        "restore_summary",
        "session_context",
        "user_input",
        "diagnostic_note",
        "missing_source_notice",
    }


def test_v0412_prompt_source_kinds_declared() -> None:
    assert {item.value for item in PromptSourceKind} == {
        "built_in_safety",
        "profile_soul_file",
        "profile_role_file",
        "profile_domain_file",
        "profile_policy_file",
        "project_agents_file",
        "project_instruction_file",
        "restore_document",
        "session_store",
        "user_input",
        "generated_metadata",
    }


def test_v0412_prompt_assembly_status_values_declared() -> None:
    assert {item.value for item in PromptAssemblyStatus} == {
        "assembled",
        "assembled_with_warnings",
        "blocked",
        "missing_required_source",
        "invalid_input",
        "preview_only",
    }


def test_v0412_prompt_assembly_policy_closes_provider_prompt_agentloop_and_skill_execution() -> None:
    policy = create_prompt_assembly_policy()

    assert policy.safety_invariant_required is True
    assert policy.provider_invocation_allowed is False
    assert policy.prompt_submission_allowed is False
    assert policy.agent_loop_allowed is False
    assert policy.skill_execution_allowed is False
    assert policy.metadata_only is True


def test_v0412_prompt_block_order_is_safety_soul_role_domain_project_skill_restore_session_user(tmp_path: Path) -> None:
    result = assemble_default_personal_prompt(
        PromptAssemblyInput("input", "default-personal", str(tmp_path), "hello", None, None, True, True, True, True)
    )

    assert tuple(block.block_kind for block in sorted(result.blocks, key=lambda item: item.order_index)) == PROMPT_BLOCK_ORDER


def test_v0412_source_provenance_records_missing_sources() -> None:
    provenance = create_prompt_source_provenance(source_path="missing", source_present=False, source_read=False, warning="source missing")

    assert provenance.source_present is False
    assert provenance.source_read is False
    assert provenance.warning == "source missing"


def test_v0412_safety_invariant_block_states_provider_prompt_agentloop_skill_shell_subagent_closed() -> None:
    safety = create_safety_invariant_block()

    assert safety.provider_invocation_closed is True
    assert safety.prompt_submission_closed is True
    assert safety.agent_loop_closed is True
    assert safety.skill_execution_closed is True
    assert "Shell, test, subagent" in safety.block.content
    assert safety.preview_not_model_response is True


def test_v0412_soul_role_domain_binding_usable_for_preview_not_provider_run(tmp_path: Path) -> None:
    binding = create_soul_role_domain_binding(str(tmp_path))

    assert binding.usable_for_preview is True
    assert binding.usable_for_provider_run is False


def test_v0412_project_instruction_ref_cannot_override_safety_invariant(tmp_path: Path) -> None:
    ref = create_project_instruction_ref(str(tmp_path))

    assert ref.project_context_allowed is True
    assert ref.prompt_injection_warning is True


def test_v0412_read_only_skill_policy_block_does_not_execute_skills() -> None:
    block = create_read_only_skill_policy_block()

    assert block.skill_execution_allowed is False
    assert "does not execute skills" in block.block.content


def test_v0412_restore_summary_block_does_not_grant_runtime_authority() -> None:
    block = create_restore_summary_block()

    assert block.grants_runtime_authority is False
    assert "do not grant runtime authority" in block.block.content


def test_v0412_prompt_assembly_result_never_invokes_provider_or_submits_prompt(tmp_path: Path) -> None:
    result = assemble_default_personal_prompt(
        PromptAssemblyInput("input", "default-personal", str(tmp_path), "hello", None, None, True, True, True, True)
    )

    assert prompt_assembly_result_preserves_preview_only(result)


def test_v0412_prompt_preview_command_result_is_non_mutating(tmp_path: Path) -> None:
    result = create_prompt_preview_command_result(PromptPreviewCommandInput("default-personal", str(tmp_path), "hello", None, None))

    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.session_written is False
    assert "PROMPT PREVIEW ONLY" in result.rendered_preview


def test_v0412_session_store_config_allows_create_but_not_append_turns_or_overwrite(tmp_path: Path) -> None:
    config = create_default_personal_session_store_config(str(tmp_path))

    assert config.allow_create is True
    assert config.allow_append_turns is False
    assert config.allow_overwrite is False


def test_v0412_session_create_result_never_invokes_provider_prompt_agentloop_skill_shell_network_or_credentials(tmp_path: Path) -> None:
    result = create_default_personal_session(create_default_personal_session_create_request(str(tmp_path)))

    assert session_create_result_preserves_runtime_closed(result)


def test_v0412_session_new_creates_session_under_tmp_home(tmp_path: Path) -> None:
    result = create_default_personal_session(create_default_personal_session_create_request(str(tmp_path)))

    assert result.session_record is not None
    assert Path(result.session_record.session_json_path).exists()
    assert Path(result.session_record.turns_jsonl_path).exists()
    assert Path(result.session_record.events_jsonl_path).exists()
    assert Path(result.session_record.session_json_path).resolve().is_relative_to(tmp_path.resolve())


def test_v0412_session_new_does_not_overwrite_existing_session_files(tmp_path: Path) -> None:
    request = create_default_personal_session_create_request(str(tmp_path), explicit_session_id="fixed-session")
    first = create_default_personal_session(request)
    second = create_default_personal_session(request)

    assert first.created_files
    assert second.created_files == ()
    assert second.existing_files
    assert second.overwritten_files == ()


def test_v0412_session_list_reads_sessions_without_provider_or_agentloop(tmp_path: Path) -> None:
    create_default_personal_session(create_default_personal_session_create_request(str(tmp_path), explicit_session_id="session-a"))
    result = list_default_personal_sessions(create_default_personal_session_list_request(str(tmp_path)))

    assert len(result.sessions) == 1
    assert Path(result.sessions[0].session_json_path).resolve().is_relative_to(tmp_path.resolve())
    assert Path(result.sessions[0].turns_jsonl_path).resolve().is_relative_to(tmp_path.resolve())
    assert Path(result.sessions[0].events_jsonl_path).resolve().is_relative_to(tmp_path.resolve())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.agent_loop_started is False


def test_v0412_session_turn_record_schema_is_future_only() -> None:
    record = DefaultPersonalSessionTurnRecord("turn", "session", "user", "hello", "now", "schema", False, {"future_only": True})

    assert record.provider_generated is False
    assert record.metadata["future_only"] is True


def test_v0412_session_store_safety_report_closes_runtime_actions() -> None:
    assert session_safety_report_preserves_closed(create_default_personal_session_store_safety_report())


def test_v0412_readiness_report_keeps_run_provider_skill_trace_user_test_false() -> None:
    report = create_v0412_readiness_report()

    assert report.prompt_assembly_defined is True
    assert report.session_new_command_ready is True
    assert v0412_readiness_preserves_closed_runtime(report)
    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False


def test_v0412_v0413_handoff_targets_provider_probe_and_read_only_skill_registry() -> None:
    handoff = create_v0413_provider_probe_skill_registry_handoff()

    assert handoff.target_version == "v0.41.3 Safe Provider Probe & Read-only Skill Registry"
    assert "provider doctor --no-completion" in handoff.recommended_focus
    assert "static read-only skill registry" in handoff.recommended_focus


def test_v0412_v0416_user_test_target_preserves_required_commands() -> None:
    target = create_v0416_user_test_target_update()

    for command in V0416_TARGET_COMMANDS:
        assert command in target.commands
    assert "chanta-cli session new --profile default-personal" in target.commands_expected_in_v0412
    assert target.user_test_release_ready is False


def test_v0412_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = create_v0412_integrated_restore_context_snapshot()

    assert set(OPEN_CAPABILITIES).issubset(snapshot.open_capabilities)
    assert set(CLOSED_CAPABILITIES).issubset(snapshot.closed_capabilities)
    assert snapshot.next_recommended_version == "v0.41.3 Safe Provider Probe & Read-only Skill Registry"


def test_v0412_restore_packet_uses_single_integrated_doc_path() -> None:
    assert integrated_restore_packet_uses_single_doc(create_v0412_integrated_restore_packet())


def test_v0412_restore_packet_marks_separate_restore_doc_created_false() -> None:
    assert create_v0412_integrated_restore_packet().separate_restore_doc_created is False


def test_v0412_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = create_v0412_integrated_restore_document_manifest()

    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0412_integrated_document_exists_and_has_required_restore_sections() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    for section in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Repository Baseline Assumptions",
        "v0.41.1 CLI Bootstrap Summary",
        "Prompt Assembly Summary",
        "Prompt Block Order Contract",
        "Safety Invariant Block Contract",
        "Soul / Role / Domain Binding Contract",
        "Project Instruction Contract",
        "Read-only Skill Policy Block Contract",
        "Restore Summary Block Contract",
        "Session Context Block Contract",
        "Prompt Preview Contract",
        "Session Store Contract",
        "Session New Contract",
        "Session List Contract",
        "Unsupported Command Policy",
        "Safety Posture",
        "Runtime Opening Status",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Expected Test Interpretation",
        "Known Limitations",
        "Withdrawal Conditions",
        "v0.41.3 Recommended Next Step",
        "v0.41.6 User Test Target",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert section in text


def test_v0412_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    assert "You are continuing ChantaCore after v0.41.2." in text
    assert "v0.41.3 Safe Provider Probe & Read-only Skill Registry" in text
    assert "Do not call provider yet." in text


def test_v0412_no_separate_v0412_restore_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.2_restore_document.md").exists()


def test_v0412_no_separate_v0412_release_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.2_prompt_assembly.md").exists()
    assert not Path("docs/versions/v0.41/v0.41.2_session_store.md").exists()


def test_v0412_unsupported_run_provider_trace_and_unsafe_commands_still_do_not_execute(capsys) -> None:
    assert main(["run", "hello"]) == 1
    assert '"executed": false' in capsys.readouterr().out
    assert main(["provider", "doctor"]) == 1
    assert '"executed": false' in capsys.readouterr().out
    assert main(["trace", "recent"]) == 1
    assert '"executed": false' in capsys.readouterr().out
    assert main(["shell", "dir"]) == 2
    assert '"executed": false' in capsys.readouterr().out


def test_v0412_no_forbidden_runtime_call_patterns() -> None:
    paths = (
        Path("src/chanta_core/cli/main.py"),
        Path("src/chanta_core/personal_runtime/default_personal_prompt_session.py"),
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
        "client_create",
        "pytest",
        "unittest",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    for pattern in forbidden:
        assert pattern not in combined

    assert "Path.mkdir" not in combined
    assert ".mkdir(" in combined
    assert "Path.write_text" not in combined
    assert ".write_text(" in combined
    credential_lines = [line for line in combined.splitlines() if "credential" in line]
    assert credential_lines
    assert all("credentials_accessed" in line or "credential_access_allowed" in line for line in credential_lines)
    provider_invoke_lines = [line for line in combined.splitlines() if "provider_invoke" in line]
    assert provider_invoke_lines
    assert all("provider_invoked" in line or "provider_invocation_allowed" in line for line in provider_invoke_lines)
    prompt_submit_lines = [line for line in combined.splitlines() if "prompt_submit" in line]
    assert prompt_submit_lines
    assert all("prompt_submitted" in line or "prompt_submission_allowed" in line for line in prompt_submit_lines)


def test_v0412_main_prompt_preview_returns_preview_without_session_write(tmp_path: Path, capsys) -> None:
    _init_profile(tmp_path)
    assert main(["prompt", "preview", "--profile", "default-personal", "--home", str(tmp_path), "Summarize current ChantaCore status."]) == 0
    output = capsys.readouterr().out
    assert "PROMPT PREVIEW ONLY" in output
    assert "not a model response" in output
    assert not any((tmp_path / "profiles" / "default-personal" / "state" / "sessions").glob("session-*"))


def test_v0412_main_session_new_and_list_under_tmp_home(tmp_path: Path, capsys) -> None:
    _init_profile(tmp_path)
    assert main(["session", "new", "--profile", "default-personal", "--home", str(tmp_path), "--session-id", "manual-session"]) == 0
    new_output = capsys.readouterr().out
    assert '"session_id": "manual-session"' in new_output
    assert main(["session", "list", "--profile", "default-personal", "--home", str(tmp_path)]) == 0
    list_output = capsys.readouterr().out
    assert '"session_id": "manual-session"' in list_output


def test_v0412_prompt_preview_with_missing_identity_files_warns_but_does_not_fail(tmp_path: Path) -> None:
    result = create_prompt_preview_command_result(PromptPreviewCommandInput("default-personal", str(tmp_path), "hello", None, None))

    assert result.status == "assembled_with_warnings"
    assert result.provider_invoked is False


def test_v0412_prompt_assembly_with_fixture_identity_files_loads_bounded_content(tmp_path: Path) -> None:
    _init_profile(tmp_path)
    result = assemble_default_personal_prompt(
        PromptAssemblyInput("input", "default-personal", str(tmp_path), "hello", None, None, True, True, True, True)
    )

    assert result.blocks[1].present is True
    assert result.blocks[2].present is True
    assert result.blocks[3].present is True
