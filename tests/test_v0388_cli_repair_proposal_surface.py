from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairCLIArgumentSpec,
    RepairCLICommandDisposition,
    RepairCLICommandKind,
    RepairCLICommandResult,
    RepairCLICommandSpec,
    RepairCLIDecisionKind,
    RepairCLIDeniedCommand,
    RepairCLIFlagSet,
    RepairCLIInvocation,
    RepairCLIInvocationDecision,
    RepairCLINoRuntimeGuarantee,
    RepairCLIOutput,
    RepairCLIOutputFormat,
    RepairCLIReadinessLevel,
    RepairCLIReport,
    RepairCLIRiskKind,
    RepairCLIRunPreview,
    RepairCLISourceKind,
    RepairCLISourceRef,
    RepairCLIStatus,
    RepairCLISurface,
    RepairCLISurfaceMode,
    RepairCLISurfacePolicy,
    V0388ReadinessReport,
    build_default_repair_cli_surface,
    build_repair_cli_argument_spec,
    build_repair_cli_command_result,
    build_repair_cli_command_spec,
    build_repair_cli_denied_command,
    build_repair_cli_flags,
    build_repair_cli_invocation,
    build_repair_cli_invocation_decision,
    build_repair_cli_no_runtime_guarantee,
    build_repair_cli_output,
    build_repair_cli_report,
    build_repair_cli_run_preview,
    build_repair_cli_source_ref,
    build_repair_cli_surface,
    build_repair_cli_surface_policy,
    build_v0388_readiness_report,
    create_repair_cli_bundle_preview,
    create_repair_cli_handoff_preview,
    default_repair_cli_command_specs,
    default_repair_cli_surface_policy,
    evaluate_repair_cli_invocation,
    parse_repair_cli_invocation,
    render_repair_cli_help,
    render_repair_cli_preview,
    render_repair_cli_status,
    repair_cli_command_result_is_not_runtime,
    repair_cli_decision_is_preview_only,
    repair_cli_flags_preserve_no_runtime,
    repair_cli_invocation_is_not_shell,
    repair_cli_output_is_in_memory_only,
    repair_cli_policy_blocks_runtime,
    run_repair_cli_command,
    v0388_readiness_report_is_not_execution_ready,
)
import chanta_core.agent_runtime.repair_cli_surface as cli_module


SAFE_FLAG_NAMES = {
    "ready_for_v0389_bounded_repair_proposal_loop_consolidation",
    "ready_for_v039_human_approved_sandbox_repair_apply",
    "ready_for_cli_repair_proposal_surface",
    "ready_for_cli_command_registry",
    "ready_for_cli_argument_parsing",
    "ready_for_cli_help_command",
    "ready_for_cli_status_command",
    "ready_for_cli_boundary_preview",
    "ready_for_cli_evidence_preview",
    "ready_for_cli_source_context_preview",
    "ready_for_cli_scope_preview",
    "ready_for_cli_patch_metadata_preview",
    "ready_for_cli_safety_preview",
    "ready_for_cli_human_review_packet_preview",
    "ready_for_cli_loop_packet_preview",
    "ready_for_cli_bundle_preview",
    "ready_for_cli_do_nothing_preview",
    "ready_for_cli_handoff_preview",
    "ready_for_future_v0389_consolidation_input",
    "ready_for_future_v039_apply_handoff_metadata",
}

SAFE_COMMANDS = {
    "repair-proposal-help": RepairCLICommandKind.REPAIR_PROPOSAL_HELP,
    "repair-proposal-status": RepairCLICommandKind.REPAIR_PROPOSAL_STATUS,
    "repair-boundary-preview": RepairCLICommandKind.REPAIR_BOUNDARY_PREVIEW,
    "repair-evidence-preview": RepairCLICommandKind.REPAIR_EVIDENCE_PREVIEW,
    "repair-source-context-preview": RepairCLICommandKind.REPAIR_SOURCE_CONTEXT_PREVIEW,
    "repair-scope-preview": RepairCLICommandKind.REPAIR_SCOPE_PREVIEW,
    "repair-patch-metadata-preview": RepairCLICommandKind.REPAIR_PATCH_METADATA_PREVIEW,
    "repair-safety-preview": RepairCLICommandKind.REPAIR_SAFETY_PREVIEW,
    "repair-review-packet-preview": RepairCLICommandKind.REPAIR_REVIEW_PACKET_PREVIEW,
    "repair-loop-packet-preview": RepairCLICommandKind.REPAIR_LOOP_PACKET_PREVIEW,
    "repair-proposal-bundle-preview": RepairCLICommandKind.REPAIR_PROPOSAL_BUNDLE_PREVIEW,
    "repair-do-nothing-preview": RepairCLICommandKind.REPAIR_DO_NOTHING_PREVIEW,
    "repair-handoff-preview": RepairCLICommandKind.REPAIR_HANDOFF_PREVIEW,
    "repair-no-op": RepairCLICommandKind.REPAIR_NO_OP,
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if (field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES)
        or field.name == "production_certified"
    ]


def _surface():
    return build_default_repair_cli_surface()


def _artifact_context():
    return {
        "boundary": "boundary metadata",
        "evidence": "evidence bundle metadata",
        "source_context": "existing source context snapshot metadata",
        "scope": "scope plan metadata",
        "patch_metadata": "proposed patch envelope metadata",
        "safety": "safety report metadata",
        "review_packet": "human review packet metadata",
        "loop_packet": "one-shot loop packet metadata",
        "do_nothing": "do-nothing comparison metadata",
    }


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairCLISurfaceMode} == {
        "cli_repair_proposal_surface",
        "cli_command_registry",
        "cli_argument_parsing",
        "cli_help",
        "cli_status",
        "cli_preview",
        "cli_bundle_preview",
        "cli_handoff_preview",
        "denied",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0387_loop_packet" in {item.value for item in RepairCLISourceKind}
    assert "allowed_preview" in {item.value for item in RepairCLIStatus}
    assert "preview_surface_ready" in {item.value for item in RepairCLIReadinessLevel}
    assert "repair_patch_metadata_preview" in {item.value for item in RepairCLICommandKind}
    assert "denied_dominion" in {item.value for item in RepairCLICommandKind}
    assert "allow_loop_packet_preview" in {item.value for item in RepairCLIDecisionKind}
    assert "deny_external_agent" in {item.value for item in RepairCLIDecisionKind}
    assert "arbitrary_command_execution_risk" in {item.value for item in RepairCLIRiskKind}
    assert "structured_artifact" in {item.value for item in RepairCLIOutputFormat}
    assert "future_gated" in {item.value for item in RepairCLICommandDisposition}


def test_required_models_are_exported():
    for model in (
        RepairCLIFlagSet,
        RepairCLISourceRef,
        RepairCLIArgumentSpec,
        RepairCLICommandSpec,
        RepairCLISurfacePolicy,
        RepairCLISurface,
        RepairCLIInvocation,
        RepairCLIInvocationDecision,
        RepairCLIDeniedCommand,
        RepairCLICommandResult,
        RepairCLIOutput,
        RepairCLIReport,
        RepairCLIRunPreview,
        RepairCLINoRuntimeGuarantee,
        V0388ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_cli_preview_metadata_and_preserve_no_runtime():
    flags = build_repair_cli_flags()
    assert flags.repair_cli_surface_layer_constructed
    assert flags.cli_command_registry_available
    assert flags.cli_argument_parsing_available
    assert flags.cli_preview_output_available
    assert flags.cli_denied_command_handling_available
    assert flags.cli_bundle_preview_available
    assert flags.cli_handoff_preview_available
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name)
    for name in _unsafe_flag_names(RepairCLIFlagSet):
        assert not getattr(flags, name)
    assert repair_cli_flags_preserve_no_runtime(flags)
    assert flags.metadata["no_shell_execution"]
    assert flags.metadata["no_arbitrary_command_execution"]


@pytest.mark.parametrize("flag_name", _unsafe_flag_names(RepairCLIFlagSet))
def test_flags_reject_unsafe_readiness(flag_name):
    with pytest.raises(ValueError):
        build_repair_cli_flags(**{flag_name: True})


def test_policy_allows_preview_commands_and_blocks_runtime():
    policy = default_repair_cli_surface_policy()
    for kind in SAFE_COMMANDS.values():
        assert kind in policy.allowed_command_kinds
    assert policy.allow_help
    assert policy.allow_status
    assert policy.allow_boundary_preview
    assert policy.allow_evidence_preview
    assert policy.allow_source_context_preview
    assert policy.allow_scope_preview
    assert policy.allow_patch_metadata_preview
    assert policy.allow_safety_preview
    assert policy.allow_review_packet_preview
    assert policy.allow_loop_packet_preview
    assert policy.allow_bundle_preview
    assert policy.allow_do_nothing_preview
    assert policy.allow_handoff_preview
    assert repair_cli_policy_blocks_runtime(policy)
    for name in (
        "allow_file_export",
        "allow_external_send",
        "allow_ui_runtime",
        "allow_shell",
        "allow_subprocess",
        "allow_arbitrary_command_execution",
        "allow_dependency_install",
        "allow_network_access",
        "allow_source_file_read",
        "allow_sandbox_source_read",
        "allow_source_file_write",
        "allow_patch_file_write",
        "allow_file_edit",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_repair_execution",
        "allow_test_execution",
        "allow_new_patch_generation",
        "allow_approval_capture",
        "allow_approval_grant",
        "allow_apply_permission",
        "allow_model_provider_invocation",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ):
        assert not getattr(policy, name)
        with pytest.raises(ValueError):
            build_repair_cli_surface_policy(**{name: True})


def test_default_command_specs_include_safe_and_denied_commands():
    specs = default_repair_cli_command_specs()
    by_name = {spec.command_name: spec for spec in specs}
    for command in SAFE_COMMANDS:
        assert command in by_name
        assert by_name[command].preview_only
        assert by_name[command].dispatch_target.startswith("render:")
    for command in (
        "shell",
        "bash",
        "powershell",
        "cmd",
        "python",
        "pytest",
        "npm",
        "pip",
        "curl",
        "wget",
        "git",
        "git-apply",
        "apply-patch",
        "apply_patch",
        "repair-apply",
        "auto-repair",
        "retry-loop",
        "multi-cycle-loop",
        "approve",
        "capture-approval",
        "run-codex",
        "run-claude-code",
        "provider-call",
        "model-call",
        "external-agent",
        "dominion",
        "infinite-loop",
        "recursive-agent",
    ):
        assert command in by_name
        assert by_name[command].dispatch_target == "deny:static-policy"


def test_argument_spec_and_source_ref_are_bounded_metadata_only():
    arg = build_repair_cli_argument_spec(max_value_chars=16)
    assert arg.allow_text_value
    assert arg.allow_ref_value
    assert not arg.allow_json_value
    with pytest.raises(ValueError):
        build_repair_cli_argument_spec(max_value_chars=-1)
    source_ref = build_repair_cli_source_ref()
    assert source_ref.source_summary
    assert source_ref.evidence_refs == []


@pytest.mark.parametrize("command, expected_kind", list(SAFE_COMMANDS.items()))
def test_parse_safe_commands(command, expected_kind):
    invocation = parse_repair_cli_invocation([command, "--format", "markdown"], _surface())
    assert invocation.command_kind == expected_kind
    assert invocation.argv[0] == command
    assert invocation.requested_output_format == RepairCLIOutputFormat.MARKDOWN
    assert repair_cli_invocation_is_not_shell(invocation)


@pytest.mark.parametrize(
    "command",
    [
        "shell",
        "bash",
        "powershell",
        "cmd",
        "python",
        "pytest",
        "unittest",
        "npm",
        "pnpm",
        "yarn",
        "pip",
        "poetry",
        "install",
        "dependency-install",
        "network",
        "curl",
        "wget",
        "write-file",
        "write-patch-file",
        "export-file",
        "send-review",
        "send-email",
        "webhook",
        "apply-patch",
        "apply_patch",
        "git-apply",
        "repair-apply",
        "apply-repair",
        "auto-repair",
        "repair-loop",
        "retry-loop",
        "multi-cycle-loop",
        "approve",
        "capture-approval",
        "grant-approval",
        "run-codex",
        "run-claude-code",
        "run-opencode",
        "run-hermes",
        "run-openclaw",
        "provider-call",
        "model-call",
        "external-agent",
        "dominion",
        "infinite-loop",
        "recursive-agent",
    ],
)
def test_unsafe_commands_are_denied(command):
    surface = _surface()
    invocation = parse_repair_cli_invocation([command], surface)
    decision = evaluate_repair_cli_invocation(invocation, surface)
    output = run_repair_cli_command(invocation, surface)
    assert decision.disposition == RepairCLICommandDisposition.DENIED
    assert not decision.preview_allowed
    assert repair_cli_decision_is_preview_only(decision)
    assert output.status == RepairCLIStatus.DENIED
    assert output.denied_command is not None
    assert output.denied_command.safe_alternatives
    assert repair_cli_output_is_in_memory_only(output)


def test_git_apply_two_token_command_is_denied():
    invocation = parse_repair_cli_invocation(["git", "apply", "patch.diff"], _surface())
    assert invocation.command_kind == RepairCLICommandKind.DENIED_GIT_APPLY
    output = run_repair_cli_command(invocation, _surface())
    assert output.status == RepairCLIStatus.DENIED


def test_unknown_command_is_denied():
    invocation = parse_repair_cli_invocation(["something-new"], _surface())
    assert invocation.command_kind == RepairCLICommandKind.UNKNOWN
    output = run_repair_cli_command(invocation, _surface())
    assert output.status == RepairCLIStatus.DENIED
    assert output.denied_command is not None


def test_safe_decision_allows_preview_only_and_runtime_booleans_false():
    surface = _surface()
    invocation = parse_repair_cli_invocation(["repair-loop-packet-preview"], surface)
    decision = evaluate_repair_cli_invocation(invocation, surface, _artifact_context())
    assert decision.preview_allowed
    assert decision.allowed_command_kind == RepairCLICommandKind.REPAIR_LOOP_PACKET_PREVIEW
    assert repair_cli_decision_is_preview_only(decision)
    for name in (
        "file_export_allowed",
        "external_send_allowed",
        "ui_runtime_allowed",
        "shell_allowed",
        "subprocess_allowed",
        "command_execution_allowed",
        "source_read_allowed",
        "source_write_allowed",
        "new_patch_generation_allowed",
        "patch_application_allowed",
        "apply_patch_allowed",
        "git_apply_allowed",
        "repair_execution_allowed",
        "test_execution_allowed",
        "approval_capture_allowed",
        "approval_grant_allowed",
        "apply_permission_allowed",
        "model_provider_invocation_allowed",
        "external_agent_allowed",
        "dominion_runtime_allowed",
        "production_certified",
    ):
        assert not getattr(decision, name)
        with pytest.raises(ValueError):
            build_repair_cli_invocation_decision(**{name: True})


def test_run_safe_command_returns_preview_result_and_in_memory_output():
    surface = _surface()
    invocation = parse_repair_cli_invocation(["repair-patch-metadata-preview", "--format=json"], surface)
    output = run_repair_cli_command(invocation, surface, _artifact_context())
    assert output.status == RepairCLIStatus.COMPLETED
    assert output.command_result is not None
    result = output.command_result
    assert result.preview_only
    assert result.redacted
    assert result.structured_result["preview_only"]
    assert "patch" in result.rendered_preview
    assert repair_cli_command_result_is_not_runtime(result)
    assert repair_cli_output_is_in_memory_only(output)
    assert not output.written_to_file
    assert not output.sent_externally
    assert not output.ready_for_execution


def test_command_result_rejects_runtime_or_granted_state():
    for name in (
        "file_export_performed",
        "external_send_performed",
        "ui_runtime_invoked",
        "shell_used",
        "subprocess_used",
        "command_executed",
        "source_read_performed_by_v0388",
        "new_patch_metadata_generated_by_v0388",
        "file_write_performed",
        "patch_file_written",
        "file_edit_performed",
        "patch_applied",
        "apply_patch_called",
        "git_apply_called",
        "tests_run",
        "repair_executed",
        "approval_captured",
        "approval_granted",
        "apply_permission_granted",
        "model_invocation_performed",
        "external_agent_invoked",
        "dominion_runtime_invoked",
        "production_certified",
        "ready_for_execution",
    ):
        with pytest.raises(ValueError):
            build_repair_cli_command_result(**{name: True})


def test_output_rejects_file_write_send_or_execution_ready():
    with pytest.raises(ValueError):
        build_repair_cli_output(written_to_file=True)
    with pytest.raises(ValueError):
        build_repair_cli_output(sent_externally=True)
    with pytest.raises(ValueError):
        build_repair_cli_output(ready_for_execution=True)


def test_render_helpers_are_in_memory_previews():
    surface = _surface()
    assert "Safe repair proposal preview commands" in render_repair_cli_help(surface, RepairCLIOutputFormat.TEXT)
    assert "ready_for_execution" in render_repair_cli_status(surface, RepairCLIOutputFormat.JSON)
    preview = render_repair_cli_preview(
        RepairCLICommandKind.REPAIR_SAFETY_PREVIEW,
        _artifact_context(),
        RepairCLIOutputFormat.MARKDOWN,
    )
    assert "Preview only" in preview
    bundle = create_repair_cli_bundle_preview(_artifact_context(), RepairCLIOutputFormat.JSON)
    assert bundle["preview_only"]
    assert bundle["in_memory_only"]
    handoff = create_repair_cli_handoff_preview(_artifact_context(), RepairCLIOutputFormat.JSON)
    assert handoff["future_v0389_consolidation_input"]
    assert handoff["future_v039_apply_handoff_metadata"]
    assert not handoff["apply_permission"]


def test_surface_report_preview_guarantee_and_readiness_are_not_execution():
    surface = build_repair_cli_surface()
    assert surface.ready_for_cli_repair_proposal_surface
    assert surface.ready_for_future_v0389_consolidation_input
    assert not surface.ready_for_execution
    report = build_repair_cli_report()
    assert report.ready_for_future_v0389_consolidation_input
    assert report.ready_for_future_v039_apply_handoff_metadata
    assert not report.ready_for_execution
    preview = build_repair_cli_run_preview()
    assert not preview.would_execute_shell
    assert not preview.would_use_subprocess
    assert not preview.would_export_file
    assert not preview.would_apply_patch
    assert not preview.would_run_tests
    assert not preview.would_invoke_external_systems
    guarantee = build_repair_cli_no_runtime_guarantee()
    assert guarantee.no_shell
    assert guarantee.no_subprocess
    assert guarantee.no_command_execution
    assert guarantee.no_file_export
    assert guarantee.no_external_send
    assert guarantee.no_ui
    assert guarantee.no_source_read
    assert guarantee.no_new_patch_generation
    assert guarantee.no_apply
    assert guarantee.no_approval
    assert guarantee.no_repair
    assert guarantee.no_test
    assert guarantee.no_model
    assert guarantee.no_external_agent
    assert guarantee.no_dominion
    readiness = build_v0388_readiness_report(no_runtime_guarantee=guarantee)
    assert readiness.ready_for_v0389_bounded_repair_proposal_loop_consolidation
    assert readiness.ready_for_v039_human_approved_sandbox_repair_apply
    assert readiness.ready_for_cli_repair_proposal_surface
    assert v0388_readiness_report_is_not_execution_ready(readiness)


def test_builder_helpers_exist():
    helpers = (
        build_repair_cli_flags,
        build_repair_cli_source_ref,
        build_repair_cli_argument_spec,
        build_repair_cli_command_spec,
        build_repair_cli_surface_policy,
        build_repair_cli_surface,
        build_repair_cli_invocation,
        build_repair_cli_invocation_decision,
        build_repair_cli_denied_command,
        build_repair_cli_command_result,
        build_repair_cli_output,
        build_repair_cli_report,
        build_repair_cli_run_preview,
        build_repair_cli_no_runtime_guarantee,
        build_v0388_readiness_report,
        default_repair_cli_command_specs,
        default_repair_cli_surface_policy,
        build_default_repair_cli_surface,
        parse_repair_cli_invocation,
        evaluate_repair_cli_invocation,
        run_repair_cli_command,
        render_repair_cli_preview,
        render_repair_cli_status,
        render_repair_cli_help,
        create_repair_cli_bundle_preview,
        create_repair_cli_handoff_preview,
        repair_cli_flags_preserve_no_runtime,
        repair_cli_policy_blocks_runtime,
        repair_cli_invocation_is_not_shell,
        repair_cli_decision_is_preview_only,
        repair_cli_command_result_is_not_runtime,
        repair_cli_output_is_in_memory_only,
        v0388_readiness_report_is_not_execution_ready,
    )
    assert all(callable(helper) for helper in helpers)


def test_implementation_does_not_contain_runtime_action_calls():
    source = inspect.getsource(cli_module)
    forbidden_fragments = (
        "Path.read_text",
        "Path.read_bytes",
        "open(",
        "write_text",
        "write_bytes",
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
        "apply_patch(",
        "approval_granted=True",
        "human_approval_present=True",
        "approval_captured_now=True",
        "apply_allowed=True",
        "sandbox_apply_allowed=True",
    )
    for forbidden in forbidden_fragments:
        assert forbidden not in source
