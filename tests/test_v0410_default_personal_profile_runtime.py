from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.personal_runtime.default_personal_profile_runtime import (
    CLOSED_CAPABILITIES,
    INTEGRATED_DOC_PATH,
    OPEN_CAPABILITIES,
    REQUIRED_FALSE_FLAGS,
    V0409_RESTORE_DOC_PATH,
    V0416_TARGET_COMMANDS,
    DefaultPersonalProfileKind,
    DefaultPersonalProfileStatus,
    create_default_personal_identity_files,
    create_default_personal_policy_files,
    create_default_personal_profile_config,
    create_default_personal_profile_load_request,
    create_default_personal_profile_paths,
    create_default_personal_profile_safety_posture,
    create_default_personal_profile_status_report,
    create_default_personal_runtime_state,
    create_personal_runtime_root,
    create_restore_context_ref,
    create_v040_compatibility_gate,
    create_v0410_integrated_restore_context_snapshot,
    create_v0410_integrated_restore_document_manifest,
    create_v0410_integrated_restore_packet,
    create_v0410_readiness_report,
    create_v0411_installable_cli_bootstrap_handoff,
    create_v0416_user_test_target,
    create_v041_runtime_opening_status,
    default_profile_config_preserves_no_runtime_authority,
    integrated_restore_packet_uses_single_doc,
    load_default_personal_profile,
    profile_load_result_preserves_no_side_effects,
    profile_safety_posture_preserves_denial,
    v040_compatibility_gate_blocks_runtime_execution,
    v0410_readiness_preserves_closed_runtime,
    validate_default_personal_profile_config,
)


def test_v0410_profile_kind_values_declared() -> None:
    assert {item.value for item in DefaultPersonalProfileKind} == {
        "default_personal",
        "custom_personal",
        "test_fixture",
        "unknown",
    }
    assert "loaded_with_gaps" in {item.value for item in DefaultPersonalProfileStatus}


def test_v0410_personal_runtime_root_is_metadata_only_and_does_not_create_root(tmp_path: Path) -> None:
    root_path = tmp_path / "missing-root"
    root = create_personal_runtime_root(str(root_path), check_exists=True)

    assert root.metadata_only is True
    assert root.created_by_init is False
    assert root.exists is False
    assert root.writable_checked is False
    assert root.writable is None
    assert not root_path.exists()


def test_v0410_default_personal_profile_config_defaults_keep_runtime_authority_false() -> None:
    config = create_default_personal_profile_config()

    assert config.profile_id == "default-personal"
    assert default_profile_config_preserves_no_runtime_authority(config)


def test_v0410_profile_config_is_not_sandbox() -> None:
    assert create_default_personal_profile_config().profile_is_sandbox is False


def test_v0410_profile_paths_are_metadata_only() -> None:
    paths = create_default_personal_profile_paths()

    assert paths.profile_id == "default-personal"
    assert paths.all_paths_metadata_only is True
    assert paths.soul_path.endswith("identity/soul.md")


def test_v0410_identity_files_report_missing_without_hard_failure(tmp_path: Path) -> None:
    config = create_default_personal_profile_config(str(tmp_path / "profile"))
    identity = create_default_personal_identity_files(config)

    assert identity.missing_identity_items == ("soul", "role", "domain", "core_memory")
    assert identity.soul_exists is False


def test_v0410_policy_files_keep_unsafe_capabilities_closed() -> None:
    policy = create_default_personal_policy_files()

    assert policy.unsafe_capabilities_closed is True
    assert "policy" in policy.missing_policy_items


def test_v0410_profile_load_request_disallows_write_and_profile_creation() -> None:
    request = create_default_personal_profile_load_request()

    assert request.allow_filesystem_write is False
    assert request.allow_profile_creation is False
    assert request.metadata_only is True
    with pytest.raises(ValueError):
        load_default_personal_profile(create_default_personal_profile_load_request(allow_filesystem_write=True))


def test_v0410_profile_load_result_does_not_mutate_filesystem_or_call_provider() -> None:
    result = load_default_personal_profile()

    assert profile_load_result_preserves_no_side_effects(result)
    assert result.runtime_state.runtime_opened is False


def test_v0410_profile_status_report_marks_runtime_not_opened() -> None:
    report = create_default_personal_profile_status_report()

    assert report.runtime_opened is False
    assert report.unsafe_capabilities_closed is True
    assert report.next_recommended_version == "v0.41.1"
    assert "installable CLI bootstrap" in report.next_recommended_action


def test_v0410_profile_safety_posture_is_deny_first_and_non_sandbox() -> None:
    posture = create_default_personal_profile_safety_posture()

    assert profile_safety_posture_preserves_denial(posture)


def test_v0410_validation_report_not_valid_for_runtime_execution() -> None:
    report = validate_default_personal_profile_config()

    assert report.valid_for_v0410 is True
    assert report.valid_for_runtime_execution is False
    assert report.unsafe_authority_detected is False


def test_v0410_restore_context_ref_points_to_v0409_handoff_when_present() -> None:
    restore = create_restore_context_ref()

    assert restore.source_version == "v0.40.9"
    assert restore.restore_doc_path == V0409_RESTORE_DOC_PATH
    assert restore.restore_doc_expected is True
    assert restore.copy_paste_restore_prompt_expected is True


def test_v0410_v040_compatibility_gate_allows_profile_runtime_foundation_only() -> None:
    gate = create_v040_compatibility_gate()

    assert gate.compatible_for_v0410_profile_runtime is True
    assert v040_compatibility_gate_blocks_runtime_execution(gate)


def test_v0410_runtime_opening_status_only_profile_foundation_may_be_open() -> None:
    status = create_v041_runtime_opening_status()

    assert status.profile_runtime_opened is True
    assert status.cli_entrypoint_opened is False
    assert status.profile_init_opened is False
    assert status.prompt_assembly_opened is False
    assert status.session_store_opened is False
    assert status.provider_text_invocation_opened is False
    assert status.read_only_skill_registry_opened is False
    assert status.agent_loop_opened is False
    assert status.trace_emission_opened is False
    assert status.user_test_release_ready is False


def test_v0410_readiness_report_keeps_provider_prompt_agentloop_skill_trace_user_test_false() -> None:
    report = create_v0410_readiness_report()

    assert report.default_personal_profile_runtime_defined is True
    assert report.v0411_handoff_ready is True
    assert v0410_readiness_preserves_closed_runtime(report)
    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False


def test_v0410_v0411_handoff_targets_installable_cli_bootstrap() -> None:
    handoff = create_v0411_installable_cli_bootstrap_handoff()

    assert handoff.fixed_cli_command_name == "chanta-cli"
    assert handoff.target_version == "v0.41.1 Installable CLI Bootstrap & Doctor"
    assert "expose chanta-cli doctor" in handoff.recommended_focus
    assert "no run/ask" in handoff.recommended_focus


def test_v0410_v0416_user_test_target_contains_required_chanta_cli_commands() -> None:
    target = create_v0416_user_test_target()

    assert target.design_only is True
    assert target.user_test_release_ready is False
    for command in V0416_TARGET_COMMANDS:
        assert command in target.commands
    assert any(command.startswith("chanta-cli run") for command in target.commands)


def test_v0410_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = create_v0410_integrated_restore_context_snapshot()

    assert "default_personal_profile_runtime_foundation" in snapshot.open_capabilities
    assert set(OPEN_CAPABILITIES).issubset(snapshot.open_capabilities)
    assert set(CLOSED_CAPABILITIES).issubset(snapshot.closed_capabilities)


def test_v0410_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = create_v0410_integrated_restore_packet()

    assert integrated_restore_packet_uses_single_doc(packet)


def test_v0410_restore_packet_marks_separate_restore_doc_created_false() -> None:
    assert create_v0410_integrated_restore_packet().separate_restore_doc_created is False


def test_v0410_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = create_v0410_integrated_restore_document_manifest()

    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0410_integrated_document_exists_and_has_required_restore_sections() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    for section in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Repository Baseline Assumptions",
        "v0.40.9 Handoff Summary",
        "v0.41 Master Design Summary",
        "Default Personal Profile Runtime Summary",
        "Personal Runtime Root Contract",
        "Default Personal Profile Config Contract",
        "Default Personal Profile Paths Contract",
        "Identity Files Contract",
        "Policy Files Contract",
        "Profile Runtime State Contract",
        "Profile Status Report Contract",
        "Profile Safety Posture Contract",
        "Restore Context Reference",
        "v0.40 Compatibility Gate",
        "Runtime Opening Status",
        "Still-Closed Capabilities",
        "Why v0.41.0 Is Not Yet Runnable",
        "Required Test Commands",
        "Withdrawal Conditions",
        "v0.41.1 Recommended Next Step",
        "v0.41.6 User Test Target",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert section in text


def test_v0410_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    assert "You are continuing ChantaCore after v0.41.0." in text
    assert "chanta-cli" in text
    assert "v0.41.1 Installable CLI Bootstrap & Doctor" in text


def test_v0410_no_separate_v0410_restore_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.0_restore_document.md").exists()


def test_v0410_no_separate_v0410_release_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.0_default_personal_profile_runtime.md").exists()
    assert not Path("docs/versions/v0.41/v0.41.0_profile_runtime_contract.md").exists()


def test_v0410_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/personal_runtime/default_personal_profile_runtime.py").read_text(
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
        "credential",
        "secret",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "client_create",
        "pytest",
        "unittest",
        "os.remove",
        "Path.write_text",
        "mkdir",
        "makedirs",
        "open(",
    )
    for pattern in forbidden:
        assert pattern not in source

    prompt_submit_lines = [line for line in source.splitlines() if "prompt_submit" in line]
    assert prompt_submit_lines
    assert all("prompt_submitted" in line for line in prompt_submit_lines)

    provider_invoke_lines = [line for line in source.splitlines() if "provider_invoke" in line]
    assert provider_invoke_lines
    assert all("provider_invoked" in line for line in provider_invoke_lines)


def test_v0410_profile_load_to_status_report_flow_missing_files(tmp_path: Path) -> None:
    request = create_default_personal_profile_load_request(profile_home_path=str(tmp_path / "profile"))
    result = load_default_personal_profile(request)

    assert result.loaded is True
    assert result.status_report.status == "loaded_with_gaps"
    assert "missing_identity_files" in result.runtime_state.blocking_gaps
    assert not (tmp_path / "profile").exists()


def test_v0410_profile_load_to_status_report_flow_with_temp_fixture_files(tmp_path: Path) -> None:
    profile = tmp_path / "profile"
    identity = profile / "identity"
    policy = profile / "policy"
    identity.mkdir(parents=True)
    policy.mkdir(parents=True)
    for name in ("soul.md", "role.md", "domain.md", "core_memory.md"):
        (identity / name).write_text("fixture", encoding="utf-8")
    (policy / "safety.md").write_text("fixture", encoding="utf-8")

    request = create_default_personal_profile_load_request(profile_home_path=str(profile))
    result = load_default_personal_profile(request)

    assert result.runtime_state.identity_files_status.missing_identity_items == ()
    assert "policy" not in result.runtime_state.policy_files_status.missing_policy_items
    assert profile_load_result_preserves_no_side_effects(result)


def test_v0410_v040_compatibility_gate_blocks_runtime_execution() -> None:
    assert create_v040_compatibility_gate().compatible_for_v041_runtime_execution is False


def test_v0410_restore_packet_is_suitable_for_new_session_handoff() -> None:
    manifest = create_v0410_integrated_restore_document_manifest()

    assert manifest.required_sections_present is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0410_validation_detects_unsafe_authority() -> None:
    config = create_default_personal_profile_config(provider_invocation_allowed=True)
    report = validate_default_personal_profile_config(config)

    assert report.unsafe_authority_detected is True
    assert report.valid_for_v0410 is False
    assert any(finding.blocks_runtime for finding in report.findings)
