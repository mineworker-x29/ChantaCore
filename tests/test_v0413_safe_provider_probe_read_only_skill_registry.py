from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_provider_skills as v0413


MODULE_PATH = Path("src/chanta_core/personal_runtime/default_personal_provider_skills.py")
CLI_PATH = Path("src/chanta_core/cli/main.py")
DOC_PATH = Path("docs/versions/v0.41/v0.41.3_safe_provider_probe_read_only_skill_registry_restore.md")


def test_v0413_provider_kind_values_declared() -> None:
    assert {item.value for item in v0413.ProviderKind} >= {
        "openai_compatible",
        "local_openai_compatible",
        "lm_studio",
        "ollama_compatible",
        "mock",
        "unknown",
    }


def test_v0413_provider_config_source_values_declared() -> None:
    assert {item.value for item in v0413.ProviderConfigSource} >= {
        "profile_file",
        "environment",
        "default_metadata",
        "test_fixture",
        "unknown",
    }


def test_v0413_provider_endpoint_kind_values_declared() -> None:
    assert {item.value for item in v0413.ProviderEndpointKind} >= {"loopback", "remote", "missing", "invalid", "unknown"}


def test_v0413_provider_doctor_status_values_declared() -> None:
    assert {item.value for item in v0413.ProviderDoctorStatus} >= {
        "pass",
        "warn",
        "fail",
        "skipped",
        "blocked",
        "not_configured",
    }


def test_v0413_provider_secret_ref_never_prints_value(monkeypatch) -> None:
    monkeypatch.setenv("CHANTA_TEST_PROVIDER_TOKEN", "actual-token-value")
    ref = v0413.create_provider_secret_ref("CHANTA_TEST_PROVIDER_TOKEN")
    assert ref.present is True
    assert ref.value_loaded is False
    assert ref.value_printed is False
    assert "actual-token-value" not in ref.redacted_display


def test_v0413_secret_redaction_report_redacts_all_values(monkeypatch) -> None:
    monkeypatch.setenv("CHANTA_TEST_PROVIDER_TOKEN", "actual-token-value")
    report = v0413.create_provider_secret_redaction_report(
        (v0413.create_provider_secret_ref("CHANTA_TEST_PROVIDER_TOKEN"),)
    )
    assert report.all_values_redacted is True
    assert report.unsafe_secret_exposure_detected is False
    assert all("actual-token-value" not in ref.redacted_display for ref in report.secret_refs)


def test_v0413_provider_config_defaults_text_only_no_tools_no_functions_no_completion_in_doctor() -> None:
    config = v0413.create_provider_config()
    assert config.mode in {"text_only", "metadata_only"}
    assert config.tool_calling_allowed is False
    assert config.function_calling_allowed is False
    assert config.completion_allowed_in_doctor is False
    assert config.completion_allowed_in_run is False
    assert config.remote_network_probe_allowed is False


def test_v0413_provider_config_validation_completion_blocked() -> None:
    report = v0413.validate_provider_config(v0413.create_provider_config(base_url="http://127.0.0.1:1234"))
    assert report.valid_for_completion is False
    assert report.completion_blocked is True
    assert report.endpoint_kind == "loopback"
    assert report.secret_redaction_report.all_values_redacted is True


def test_v0413_provider_probe_network_policy_allows_loopback_models_only() -> None:
    policy = v0413.create_provider_probe_network_policy()
    assert policy.loopback_probe_allowed is True
    assert policy.remote_probe_allowed is False
    assert policy.completion_probe_allowed is False
    assert policy.allowed_paths == ("/models", "/v1/models")
    assert policy.timeout_seconds <= 3.0
    assert policy.sends_user_prompt is False
    assert policy.sends_completion_request is False
    assert policy.prints_secret is False


def test_v0413_models_probe_request_requires_explicit_probe_no_completion_and_loopback() -> None:
    request = v0413.create_provider_models_probe_request(
        v0413.create_provider_config(base_url="http://localhost:1234")
    )
    assert request.explicit_probe_requested is True
    assert request.no_completion is True
    assert request.endpoint_kind == "loopback"
    assert request.path in {"/models", "/v1/models"}


def test_v0413_models_probe_result_never_sends_user_prompt_or_completion_request() -> None:
    result = v0413.create_provider_models_probe_result(network_accessed=True)
    assert result.sent_user_prompt is False
    assert result.sent_completion_request is False
    assert result.printed_secret is False
    assert result.remote_network_accessed is False


def test_v0413_safe_loopback_models_probe_policy_blocks_remote_url() -> None:
    request = v0413.create_provider_models_probe_request(
        v0413.create_provider_config(base_url="https://example.com"),
        explicit_probe_requested=True,
        no_completion=True,
    )
    result = v0413.run_safe_loopback_models_probe(request)
    assert result.status == "blocked"
    assert result.network_accessed is False
    assert result.remote_network_accessed is False


def test_v0413_safe_loopback_models_probe_uses_models_path_only() -> None:
    request = v0413.create_provider_models_probe_request(
        v0413.create_provider_config(base_url="http://127.0.0.1:1234"),
        path="/bad",
    )
    result = v0413.run_safe_loopback_models_probe(request)
    assert result.status == "blocked"
    assert result.network_accessed is False


def test_v0413_provider_completion_blocked_record_targets_v0414() -> None:
    record = v0413.create_provider_completion_blocked_record()
    assert record.completion_blocked is True
    assert record.future_target_version == "v0.41.4"


def test_v0413_provider_doctor_report_never_invokes_completion_or_submits_prompt() -> None:
    report = v0413.create_provider_doctor_report(no_completion=True)
    assert v0413.provider_doctor_preserves_no_completion(report)
    assert report.completion_blocked_record.completion_blocked is True
    assert report.ready_for_v0414_run in {True, False}


def test_v0413_provider_runtime_still_closed_report_keeps_completion_prompt_agentloop_run_false() -> None:
    report = v0413.create_provider_runtime_still_closed_report()
    assert report.provider_doctor_opened is True
    assert report.provider_completion_opened is False
    assert report.prompt_submission_opened is False
    assert report.agent_loop_opened is False
    assert report.run_command_opened is False


def test_v0413_read_only_skill_kinds_declared() -> None:
    assert {item.value for item in v0413.ReadOnlySkillKind} >= {
        "profile_status",
        "config_view",
        "provider_status",
        "restore_summary",
        "trace_recent",
        "trace_summary",
        "status_summary",
        "docs_reference_search",
        "list_available_skills",
        "unsafe_command_check",
        "unknown",
    }


def test_v0413_read_only_skill_safety_classes_declared() -> None:
    assert {item.value for item in v0413.ReadOnlySkillSafetyClass} >= {
        "read_only_metadata",
        "read_only_file_bounded",
        "future_trace_read",
        "future_docs_read",
        "unsafe_write",
        "unsafe_shell",
        "unsafe_subagent",
        "unsafe_provider_tool",
        "unknown",
    }


def test_v0413_read_only_skill_capability_status_values_declared() -> None:
    assert {item.value for item in v0413.ReadOnlySkillCapabilityStatus} >= {
        "registered",
        "inspectable",
        "future_gated",
        "execution_closed",
        "unsupported",
        "unsafe_denied",
    }


def test_v0413_default_read_only_skill_registry_contains_required_skills() -> None:
    registry = v0413.build_default_read_only_skill_registry()
    names = {skill.skill_name for skill in registry.skills}
    assert names >= {
        "profile_status",
        "config_view",
        "provider_status",
        "restore_summary",
        "trace_recent",
        "trace_summary",
        "status_summary",
        "docs_reference_search",
        "list_available_skills",
        "unsafe_command_check",
    }
    assert registry.execution_enabled is False
    assert registry.skill_execution_allowed is False


def test_v0413_read_only_skill_specs_are_inspectable_but_execution_closed() -> None:
    registry = v0413.build_default_read_only_skill_registry()
    assert all(skill.capability_status == "inspectable" for skill in registry.skills)
    assert all(skill.execution_allowed is False for skill in registry.skills)
    assert all(skill.mutates_workspace is False for skill in registry.skills)
    assert all(skill.uses_shell is False for skill in registry.skills)
    assert all(skill.invokes_provider is False for skill in registry.skills)
    assert all(skill.invokes_subagent is False for skill in registry.skills)
    trace = [skill for skill in registry.skills if skill.skill_name == "trace_recent"][0]
    assert trace.future_target_version == "v0.41.5"


def test_v0413_skill_list_result_never_invokes_provider_or_executes_skill() -> None:
    result = v0413.list_read_only_skills()
    assert result.execution_enabled is False
    assert result.provider_invoked is False
    assert result.skill_executed is False
    assert result.prompt_submitted is False


def test_v0413_skill_inspect_result_never_invokes_provider_or_executes_skill() -> None:
    result = v0413.inspect_read_only_skill(v0413.create_read_only_skill_inspect_request("profile_status"))
    assert result.found is True
    assert result.execution_allowed is False
    assert result.provider_invoked is False
    assert result.skill_executed is False
    assert result.prompt_submitted is False


def test_v0413_unsafe_skill_request_kinds_declared() -> None:
    assert {item.value for item in v0413.UnsafeSkillRequestKind} >= {
        "file_write",
        "file_edit",
        "patch_apply",
        "shell_execute",
        "test_execute",
        "provider_tool_call",
        "function_call",
        "subagent_invoke",
        "child_session_create",
        "network_unbounded",
        "credential_access",
        "memory_mutate",
        "mission_schedule",
        "dominion_runtime",
        "production_certify",
    }


def test_v0413_skill_execution_blocked_decision_blocks_unsafe_requests() -> None:
    for request_kind in v0413.UnsafeSkillRequestKind:
        decision = v0413.create_skill_execution_blocked_decision(request_kind=request_kind.value)
        assert decision.blocked is True
        assert decision.executed is False


def test_v0413_skill_registry_safety_report_closes_write_shell_provider_tool_subagent_and_memory_mutation() -> None:
    report = v0413.create_read_only_skill_registry_safety_report()
    assert v0413.skill_registry_safety_preserves_closed(report)


def test_v0413_readiness_report_keeps_run_provider_text_completion_skill_execution_trace_user_test_false() -> None:
    report = v0413.create_v0413_readiness_report()
    assert report.provider_config_model_ready is True
    assert report.provider_doctor_ready is True
    assert report.skill_list_command_ready is True
    assert report.skill_inspect_command_ready is True
    assert v0413.v0413_readiness_preserves_closed_runtime(report)


def test_v0413_v0414_handoff_targets_minimal_single_turn_provider_run() -> None:
    handoff = v0413.create_v0414_minimal_provider_run_handoff()
    assert handoff.target_version == "v0.41.4 Minimal Single-turn Provider-backed Run"
    assert any("text-only completion" in item for item in handoff.recommended_focus)
    assert any("no tool calling" in item for item in handoff.recommended_focus)


def test_v0413_v0416_user_test_target_preserves_required_commands() -> None:
    target = v0413.create_v0416_user_test_target_update()
    assert target.user_test_release_ready is False
    joined = "\n".join(target.commands)
    assert "chanta-cli provider doctor --profile default-personal --no-completion" in joined
    assert "chanta-cli run --profile default-personal" in joined
    assert "chanta-cli trace recent --profile default-personal --limit 10" in joined


def test_v0413_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0413.create_v0413_integrated_restore_context_snapshot()
    assert snapshot.current_version == "v0.41.3 Safe Provider Probe & Read-only Skill Registry"
    assert "provider_doctor_no_completion" in snapshot.open_capabilities
    assert "read_only_skill_registry" in snapshot.open_capabilities
    assert "provider_text_completion" in snapshot.closed_capabilities
    assert "read_only_skill_execution" in snapshot.closed_capabilities


def test_v0413_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0413.create_v0413_integrated_restore_packet()
    assert v0413.integrated_restore_packet_uses_single_doc(packet)
    assert packet.single_integrated_doc_path == str(DOC_PATH).replace("\\", "/")


def test_v0413_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = v0413.create_v0413_integrated_restore_packet()
    assert packet.separate_restore_doc_created is False


def test_v0413_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0413.create_v0413_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0413_integrated_document_exists_and_has_required_restore_sections() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    for section in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Repository Baseline Assumptions",
        "v0.41.2 Prompt / Session Summary",
        "Provider Config Contract",
        "Provider Doctor Contract",
        "No-completion Policy",
        "Safe Loopback `/models` Probe Policy",
        "Secret Redaction Contract",
        "Provider Runtime Still-Closed Report",
        "Read-only Skill Registry Contract",
        "Skill List Contract",
        "Skill Inspect Contract",
        "Unsafe Skill Denial Policy",
        "Unsupported Command Policy",
        "Safety Posture",
        "Runtime Opening Status",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Withdrawal Conditions",
        "v0.41.4 Recommended Next Step",
        "v0.41.6 User Test Target",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert section in content
    assert "separate_restore_doc_allowed=False" in content
    assert "separate_restore_doc_created=False" in content


def test_v0413_integrated_document_contains_copy_paste_restore_prompt() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    assert "You are continuing ChantaCore after v0.41.3." in content
    assert "Next recommended version:" in content
    assert "v0.41.4 Minimal Single-turn Provider-backed Run." in content
    assert "Do not implement full autonomous AgentLoop yet." in content


def test_v0413_no_separate_v0413_restore_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.3_restore_document.md").exists()


def test_v0413_no_separate_v0413_release_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.3_safe_provider_probe.md").exists()
    assert not Path("docs/versions/v0.41/v0.41.3_read_only_skill_registry.md").exists()


def test_v0413_unsupported_run_trace_and_unsafe_commands_still_do_not_execute(capsys) -> None:
    assert cli_main(["run", "hello"]) != 0
    assert cli_main(["ask", "hello"]) != 0
    assert cli_main(["trace", "recent"]) != 0
    assert cli_main(["shell", "dir"]) != 0
    assert cli_main(["invoke-subagent"]) != 0
    output = capsys.readouterr().out
    assert "future_gated" in output
    assert "unsafe_denied" in output


def test_v0413_main_provider_doctor_no_completion_returns_report_without_provider_completion(capsys, tmp_path) -> None:
    code = cli_main(["provider", "doctor", "--profile", "default-personal", "--home", str(tmp_path), "--no-completion"])
    output = capsys.readouterr().out
    assert code == 0
    assert '"provider_invoked_completion": false' in output
    assert '"prompt_submitted": false' in output
    assert '"completion_blocked": true' in output


def test_v0413_main_skills_list_returns_registered_specs_without_execution(capsys, tmp_path) -> None:
    code = cli_main(["skills", "list", "--profile", "default-personal", "--home", str(tmp_path)])
    output = capsys.readouterr().out
    assert code == 0
    assert "profile_status" in output
    assert '"skill_executed": false' in output


def test_v0413_main_skills_inspect_returns_spec_without_execution(capsys, tmp_path) -> None:
    code = cli_main(["skills", "inspect", "profile_status", "--profile", "default-personal", "--home", str(tmp_path)])
    output = capsys.readouterr().out
    assert code == 0
    assert '"skill_name": "profile_status"' in output
    assert '"execution_allowed": false' in output


def test_v0413_no_forbidden_runtime_call_patterns_except_safe_loopback_probe_allowlist() -> None:
    text = MODULE_PATH.read_text(encoding="utf-8") + "\n" + CLI_PATH.read_text(encoding="utf-8")
    forbidden_absent = (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "requests",
        "httpx",
        "socket",
        "anthropic",
        "apply_patch",
        "git apply",
        "git worktree",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "client_create",
        "pytest",
        "unittest",
        "/chat/completions",
        "/completions",
        "/responses",
    )
    for pattern in forbidden_absent:
        assert pattern not in text

    assert "urllib.request.urlopen" in text
    assert "openai_compatible" in text
    assert "ollama_compatible" in text
    assert "api_key_env_var" in text
    assert "ProviderSecretRef" in text
    assert "credential_access" in text
    assert "provider_invoked_completion" in text
    assert "prompt_submitted" in text
