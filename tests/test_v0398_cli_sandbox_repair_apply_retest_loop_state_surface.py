from __future__ import annotations

import pytest

from chanta_core.agent_runtime.repair_loop_state_cli_surface import (
    RepairCLIDeniedLoopCommand,
    RepairCLILoopBundleView,
    RepairCLILoopCommandSpec,
    RepairCLILoopHandoffPacket,
    RepairCLILoopInvocation,
    RepairCLILoopRenderedView,
    RepairCLILoopSurfaceCommandKind,
    RepairCLILoopSurfaceDecision,
    RepairCLILoopSurfaceDecisionKind,
    RepairCLILoopSurfaceDisposition,
    RepairCLILoopSurfaceFlagSet,
    RepairCLILoopSurfaceInput,
    RepairCLILoopSurfaceMode,
    RepairCLILoopSurfaceOutputFormat,
    RepairCLILoopSurfacePolicy,
    RepairCLILoopSurfacePreviewOnlyGuarantee,
    RepairCLILoopSurfaceReadinessLevel,
    RepairCLILoopSurfaceReport,
    RepairCLILoopSurfaceResult,
    RepairCLILoopSurfaceRiskKind,
    RepairCLILoopSurfaceSourceKind,
    RepairCLILoopSurfaceStatus,
    RepairCLILoopSurfaceViewKind,
    V0398ReadinessReport,
    build_repair_cli_denied_loop_command,
    build_repair_cli_loop_bundle_view,
    build_repair_cli_loop_command_spec,
    build_repair_cli_loop_handoff_packet,
    build_repair_cli_loop_invocation,
    build_repair_cli_loop_rendered_view,
    build_repair_cli_loop_surface_decision,
    build_repair_cli_loop_surface_flags,
    build_repair_cli_loop_surface_input,
    build_repair_cli_loop_surface_policy,
    build_repair_cli_loop_surface_preview_only_guarantee,
    build_repair_cli_loop_surface_report,
    build_repair_cli_loop_surface_result,
    build_repair_cli_loop_surface_validation_report,
    build_v0398_readiness_report,
    classify_repair_cli_loop_command,
    create_repair_cli_loop_bundle_view,
    create_repair_cli_loop_handoff_packet,
    create_repair_cli_loop_surface_report,
    decide_repair_cli_loop_surface,
    default_repair_cli_loop_command_specs,
    default_repair_cli_loop_surface_policy,
    parse_repair_cli_loop_invocation,
    render_repair_cli_blocked_actions,
    render_repair_cli_loop_help,
    render_repair_cli_loop_status,
    render_repair_cli_loop_view,
    repair_cli_loop_decision_is_preview_only,
    repair_cli_loop_invocation_is_not_shell,
    repair_cli_loop_report_is_preview_only,
    repair_cli_loop_result_is_not_runtime,
    repair_cli_loop_surface_flags_preserve_no_execution,
    repair_cli_loop_surface_policy_blocks_runtime,
    run_repair_cli_loop_surface_preview,
    v0398_readiness_report_is_not_execution_ready,
)


def test_v0398_enum_values() -> None:
    assert [item.value for item in RepairCLILoopSurfaceMode] == [
        "cli_loop_state_surface",
        "cli_help_surface",
        "cli_status_surface",
        "cli_approval_preview",
        "cli_workspace_preview",
        "cli_sandbox_apply_preview",
        "cli_post_apply_retest_preview",
        "cli_outcome_comparison_preview",
        "cli_process_state_preview",
        "cli_self_prompt_draft_preview",
        "cli_subagent_prompt_draft_preview",
        "cli_human_handoff_preview",
        "cli_loop_bundle_preview",
        "cli_blocked_actions_preview",
        "cli_readiness_preview",
        "cli_consolidation_handoff_preview",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in RepairCLILoopSurfaceSourceKind] == [
        "v0397_self_prompting_draft_packet",
        "v0397_human_handoff_prompt",
        "v0397_prompt_safety_assessment",
        "v0397_readiness_report",
        "v0396_process_state_reconstruction_report",
        "v0396_mission_state_projection",
        "v0396_pig_diagnostic_input_context",
        "v0395_outcome_comparison_report",
        "v0395_effectiveness_assessment",
        "v0395_regression_signal",
        "v0394_post_apply_retest_result",
        "v0394_post_apply_retest_run_record",
        "v0394_output_capture",
        "v0393_sandbox_apply_result",
        "v0393_sandbox_apply_transaction",
        "v0393_sandbox_apply_audit",
        "v0392_workspace_descriptor",
        "v0392_workspace_isolation_decision",
        "v0391_approval_artifact_decision",
        "v0391_approval_process_state_gate",
        "cli_argv",
        "parsed_cli_args",
        "manual_operator_note",
        "test_fixture",
        "unknown",
    ]
    assert "view_rendered" in {item.value for item in RepairCLILoopSurfaceStatus}
    assert "design_handoff_ready_for_v0399" in {item.value for item in RepairCLILoopSurfaceReadinessLevel}
    assert "sandbox_apply_preview" in {item.value for item in RepairCLILoopSurfaceCommandKind}
    assert "deny_subprocess" in {item.value for item in RepairCLILoopSurfaceDecisionKind}
    assert "shell_execution_risk" in {item.value for item in RepairCLILoopSurfaceRiskKind}
    assert "blocked_actions_view" in {item.value for item in RepairCLILoopSurfaceViewKind}
    assert "json_like" in {item.value for item in RepairCLILoopSurfaceOutputFormat}
    assert "preview_rendered" in {item.value for item in RepairCLILoopSurfaceDisposition}


def test_flags_allow_preview_surface_and_future_consolidation_only() -> None:
    flags = build_repair_cli_loop_surface_flags()

    assert isinstance(flags, RepairCLILoopSurfaceFlagSet)
    assert flags.cli_loop_surface_layer_constructed is True
    assert flags.cli_command_registry_available is True
    assert flags.cli_invocation_parser_available is True
    assert flags.cli_preview_renderer_available is True
    assert flags.cli_loop_bundle_preview_available is True
    assert flags.cli_human_handoff_preview_available is True
    assert flags.future_v0399_consolidation_input_available is True
    assert flags.ready_for_v0399_consolidation is True
    assert flags.ready_for_cli_loop_state_surface is True
    assert flags.ready_for_cli_command_registry is True
    assert flags.ready_for_cli_invocation_parser is True
    assert flags.ready_for_cli_preview_renderer is True
    assert flags.ready_for_cli_sandbox_apply_preview is True
    assert flags.ready_for_cli_post_apply_retest_preview is True
    assert flags.ready_for_cli_self_prompt_draft_preview is True
    assert flags.ready_for_future_v0399_consolidation_input is True
    assert repair_cli_loop_surface_flags_preserve_no_execution(flags)

    assert flags.ready_for_execution is False
    assert flags.ready_for_cli_runtime_execution is False
    assert flags.ready_for_cli_apply_execution is False
    assert flags.ready_for_cli_retest_execution is False
    assert flags.ready_for_cli_prompt_submission is False
    assert flags.ready_for_cli_model_invocation is False
    assert flags.ready_for_cli_subagent_invocation is False
    assert flags.ready_for_cli_external_agent_execution is False
    assert flags.ready_for_cli_auto_continue is False
    assert flags.ready_for_cli_shell_execution is False
    assert flags.ready_for_cli_subprocess_execution is False
    assert flags.ready_for_cli_arbitrary_command_execution is False
    assert flags.ready_for_cli_file_export is False
    assert flags.ready_for_cli_external_send is False
    assert flags.ready_for_persistent_trace_write is False
    assert flags.ready_for_dominion_runtime is False
    assert flags.production_certified is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_cli_runtime_execution",
        "ready_for_cli_apply_execution",
        "ready_for_cli_retest_execution",
        "ready_for_cli_prompt_submission",
        "ready_for_cli_model_invocation",
        "ready_for_cli_subagent_invocation",
        "ready_for_cli_external_agent_execution",
        "ready_for_cli_auto_continue",
        "ready_for_cli_retry_loop",
        "ready_for_cli_multi_cycle_loop",
        "ready_for_cli_shell_execution",
        "ready_for_cli_subprocess_execution",
        "ready_for_cli_arbitrary_command_execution",
        "ready_for_cli_dependency_install",
        "ready_for_cli_network_access",
        "ready_for_cli_file_export",
        "ready_for_cli_external_send",
        "ready_for_model_provider_invocation",
        "ready_for_subagent_invocation",
        "ready_for_external_agent_execution",
        "ready_for_autonomous_loop_runtime",
        "ready_for_repair_execution",
        "ready_for_test_execution",
        "ready_for_patch_application",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_persistent_trace_write",
        "ready_for_dominion_runtime",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_cli_loop_surface_flags(**{field_name: True})


def test_policy_allows_preview_views_and_blocks_runtime_surfaces() -> None:
    policy = default_repair_cli_loop_surface_policy()

    assert isinstance(policy, RepairCLILoopSurfacePolicy)
    assert policy.allow_help is True
    assert policy.allow_status is True
    assert policy.allow_preview_views is True
    assert policy.allow_loop_bundle_preview is True
    assert policy.allow_blocked_actions_preview is True
    assert policy.allow_readiness_preview is True
    assert policy.allow_future_v0399_consolidation_input is True
    assert policy.require_preview_only is True
    assert policy.require_bounded_output is True
    assert policy.require_no_file_write is True
    assert policy.require_no_external_send is True
    assert policy.require_human_handoff is True
    assert repair_cli_loop_surface_policy_blocks_runtime(policy)

    assert policy.allow_cli_runtime_execution is False
    assert policy.allow_cli_apply_execution is False
    assert policy.allow_cli_retest_execution is False
    assert policy.allow_cli_prompt_submission is False
    assert policy.allow_cli_model_invocation is False
    assert policy.allow_cli_subagent_invocation is False
    assert policy.allow_cli_external_agent_execution is False
    assert policy.allow_cli_auto_continue is False
    assert policy.allow_cli_shell is False
    assert policy.allow_cli_subprocess is False
    assert policy.allow_cli_arbitrary_command is False
    assert policy.allow_cli_file_export is False
    assert policy.allow_cli_external_send is False
    assert policy.allow_trace_persistence is False
    assert policy.allow_ocel_write is False
    assert policy.allow_ocpx_persistence is False
    assert policy.allow_pig_execution is False
    assert policy.allow_dominion_runtime is False


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_cli_runtime_execution",
        "allow_cli_apply_execution",
        "allow_cli_retest_execution",
        "allow_cli_prompt_submission",
        "allow_cli_model_invocation",
        "allow_cli_subagent_invocation",
        "allow_cli_external_agent_execution",
        "allow_cli_auto_continue",
        "allow_cli_retry_loop",
        "allow_cli_multi_cycle_loop",
        "allow_cli_shell",
        "allow_cli_subprocess",
        "allow_cli_arbitrary_command",
        "allow_cli_dependency_install",
        "allow_cli_network_access",
        "allow_cli_file_export",
        "allow_cli_external_send",
        "allow_trace_persistence",
        "allow_ocel_write",
        "allow_ocpx_persistence",
        "allow_pig_execution",
        "allow_dominion_runtime",
    ],
)
def test_policy_rejects_runtime_allow(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_cli_loop_surface_policy(**{field_name: True})


def test_command_specs_include_safe_preview_and_denied_unsafe_commands() -> None:
    specs = default_repair_cli_loop_command_specs()
    kinds = {spec.command_kind for spec in specs}

    assert all(isinstance(spec, RepairCLILoopCommandSpec) for spec in specs)
    assert RepairCLILoopSurfaceCommandKind.STATUS in kinds
    assert RepairCLILoopSurfaceCommandKind.SANDBOX_APPLY_PREVIEW in kinds
    assert RepairCLILoopSurfaceCommandKind.POST_APPLY_RETEST_PREVIEW in kinds
    assert RepairCLILoopSurfaceCommandKind.SELF_PROMPT_DRAFT_PREVIEW in kinds
    assert RepairCLILoopSurfaceCommandKind.DENIED_APPLY in kinds
    assert RepairCLILoopSurfaceCommandKind.DENIED_RETEST in kinds
    assert RepairCLILoopSurfaceCommandKind.DENIED_MODEL_CALL in kinds
    assert RepairCLILoopSurfaceCommandKind.DENIED_SUBAGENT_INVOKE in kinds
    assert RepairCLILoopSurfaceCommandKind.DENIED_SHELL in kinds
    assert RepairCLILoopSurfaceCommandKind.DENIED_FILE_EXPORT in kinds
    assert all(spec.preview_only is True for spec in specs)

    denied = build_repair_cli_loop_command_spec(
        command_kind=RepairCLILoopSurfaceCommandKind.DENIED_APPLY,
        command_name="apply",
        view_kind=RepairCLILoopSurfaceViewKind.DENIED_COMMAND_VIEW,
        denied_by_default=True,
        preview_only=True,
    )
    assert denied.denied_by_default is True


def test_input_invocation_and_parser_are_metadata_only() -> None:
    cli_input = build_repair_cli_loop_surface_input(argv=["status"])
    invocation = parse_repair_cli_loop_invocation(cli_input)

    assert isinstance(cli_input, RepairCLILoopSurfaceInput)
    assert cli_input.artifact_context
    for action in [
        "apply_execution",
        "retest_execution",
        "prompt_submission",
        "model_invocation",
        "subagent_invocation",
        "external_agent",
        "shell",
        "subprocess",
        "arbitrary_command",
        "file_export",
        "external_send",
        "trace_persistence",
        "Dominion",
    ]:
        assert action in cli_input.prohibited_runtime_actions

    assert isinstance(invocation, RepairCLILoopInvocation)
    assert invocation.command_kind == RepairCLILoopSurfaceCommandKind.STATUS
    assert invocation.shell_used is False
    assert invocation.subprocess_used is False
    assert invocation.arbitrary_command_executed is False
    assert repair_cli_loop_invocation_is_not_shell(invocation)


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["help"], RepairCLILoopSurfaceCommandKind.HELP),
        (["status"], RepairCLILoopSurfaceCommandKind.STATUS),
        (["approval"], RepairCLILoopSurfaceCommandKind.APPROVAL_PREVIEW),
        (["workspace"], RepairCLILoopSurfaceCommandKind.WORKSPACE_PREVIEW),
        (["apply-preview"], RepairCLILoopSurfaceCommandKind.SANDBOX_APPLY_PREVIEW),
        (["retest-preview"], RepairCLILoopSurfaceCommandKind.POST_APPLY_RETEST_PREVIEW),
        (["comparison"], RepairCLILoopSurfaceCommandKind.OUTCOME_COMPARISON_PREVIEW),
        (["process-state"], RepairCLILoopSurfaceCommandKind.PROCESS_STATE_PREVIEW),
        (["self-prompt"], RepairCLILoopSurfaceCommandKind.SELF_PROMPT_DRAFT_PREVIEW),
        (["subagent-prompt"], RepairCLILoopSurfaceCommandKind.SUBAGENT_PROMPT_DRAFT_PREVIEW),
        (["handoff"], RepairCLILoopSurfaceCommandKind.HUMAN_HANDOFF_PREVIEW),
        (["bundle"], RepairCLILoopSurfaceCommandKind.LOOP_BUNDLE_PREVIEW),
        (["blocked"], RepairCLILoopSurfaceCommandKind.BLOCKED_ACTIONS_PREVIEW),
        (["readiness"], RepairCLILoopSurfaceCommandKind.READINESS_PREVIEW),
        (["consolidation"], RepairCLILoopSurfaceCommandKind.CONSOLIDATION_HANDOFF_PREVIEW),
    ],
)
def test_parser_maps_safe_preview_commands(argv: list[str], expected: RepairCLILoopSurfaceCommandKind) -> None:
    assert classify_repair_cli_loop_command(argv) == expected


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["apply"], RepairCLILoopSurfaceCommandKind.DENIED_APPLY),
        (["retest"], RepairCLILoopSurfaceCommandKind.DENIED_RETEST),
        (["test"], RepairCLILoopSurfaceCommandKind.DENIED_RUN_TESTS),
        (["apply-patch"], RepairCLILoopSurfaceCommandKind.DENIED_APPLY_PATCH),
        (["git-apply"], RepairCLILoopSurfaceCommandKind.DENIED_GIT_APPLY),
        (["prompt-submit"], RepairCLILoopSurfaceCommandKind.DENIED_PROMPT_SUBMIT),
        (["model"], RepairCLILoopSurfaceCommandKind.DENIED_MODEL_CALL),
        (["next-action-execute"], RepairCLILoopSurfaceCommandKind.DENIED_NEXT_ACTION_EXECUTE),
        (["subagent"], RepairCLILoopSurfaceCommandKind.DENIED_SUBAGENT_INVOKE),
        (["external-agent"], RepairCLILoopSurfaceCommandKind.DENIED_EXTERNAL_AGENT),
        (["auto-continue"], RepairCLILoopSurfaceCommandKind.DENIED_AUTO_CONTINUE),
        (["shell"], RepairCLILoopSurfaceCommandKind.DENIED_SHELL),
        (["subprocess"], RepairCLILoopSurfaceCommandKind.DENIED_SUBPROCESS),
        (["export"], RepairCLILoopSurfaceCommandKind.DENIED_FILE_EXPORT),
        (["unknown-command"], RepairCLILoopSurfaceCommandKind.UNKNOWN),
    ],
)
def test_parser_maps_unsafe_commands_to_denied(argv: list[str], expected: RepairCLILoopSurfaceCommandKind) -> None:
    assert classify_repair_cli_loop_command(argv) == expected


def test_decision_allows_preview_only_and_denies_unsafe_commands() -> None:
    safe_invocation = build_repair_cli_loop_invocation(argv=["status"])
    safe_decision = decide_repair_cli_loop_surface(safe_invocation)
    denied_invocation = build_repair_cli_loop_invocation(argv=["apply"])
    denied_decision = decide_repair_cli_loop_surface(denied_invocation)

    assert isinstance(safe_decision, RepairCLILoopSurfaceDecision)
    assert safe_decision.preview_allowed is True
    assert repair_cli_loop_decision_is_preview_only(safe_decision)
    assert safe_decision.runtime_execution_allowed is False
    assert safe_decision.apply_execution_allowed is False
    assert safe_decision.retest_execution_allowed is False
    assert safe_decision.prompt_submission_allowed is False
    assert safe_decision.model_invocation_allowed is False
    assert safe_decision.subagent_invocation_allowed is False
    assert safe_decision.shell_allowed is False
    assert safe_decision.subprocess_allowed is False
    assert safe_decision.file_export_allowed is False
    assert safe_decision.production_certified is False

    assert denied_decision.preview_allowed is False
    assert denied_decision.disposition == RepairCLILoopSurfaceDisposition.COMMAND_DENIED
    assert denied_decision.risk_kinds


@pytest.mark.parametrize(
    "field_name",
    [
        "apply_execution_allowed",
        "retest_execution_allowed",
        "prompt_submission_allowed",
        "model_invocation_allowed",
        "subagent_invocation_allowed",
        "external_agent_allowed",
        "auto_continue_allowed",
        "shell_allowed",
        "subprocess_allowed",
        "arbitrary_command_allowed",
        "file_export_allowed",
        "external_send_allowed",
        "trace_persistence_allowed",
        "dominion_runtime_allowed",
        "production_certified",
    ],
)
def test_decision_rejects_runtime_allowed_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_cli_loop_surface_decision(**{field_name: True})


def test_denied_command_rendered_views_bundle_and_handoff_are_in_memory_only() -> None:
    denied = build_repair_cli_denied_loop_command()
    status = render_repair_cli_loop_status()
    help_view = render_repair_cli_loop_help()
    blocked = render_repair_cli_blocked_actions()
    generic = render_repair_cli_loop_view(RepairCLILoopSurfaceCommandKind.SANDBOX_APPLY_PREVIEW)
    bundle = create_repair_cli_loop_bundle_view()
    handoff = create_repair_cli_loop_handoff_packet()

    assert isinstance(denied, RepairCLIDeniedLoopCommand)
    assert denied.safe_alternatives

    for view in [status, help_view, blocked, generic]:
        assert isinstance(view, RepairCLILoopRenderedView)
        assert view.bounded is True
        assert view.redacted is True
        assert view.written_to_file is False
        assert view.sent_externally is False

    assert isinstance(bundle, RepairCLILoopBundleView)
    assert bundle.approval_summary
    assert bundle.workspace_summary
    assert bundle.sandbox_apply_summary
    assert bundle.retest_summary
    assert bundle.outcome_comparison_summary
    assert bundle.process_state_summary
    assert bundle.self_prompt_summary
    assert bundle.human_handoff_summary
    assert bundle.blocked_actions_summary
    assert bundle.ready_for_v0399_consolidation_input is True

    assert isinstance(handoff, RepairCLILoopHandoffPacket)
    assert handoff.human_action_required is True
    assert handoff.auto_continue_allowed is False
    assert handoff.sent_externally is False


@pytest.mark.parametrize(
    ("builder", "field_name"),
    [
        (build_repair_cli_loop_invocation, "shell_used"),
        (build_repair_cli_loop_invocation, "subprocess_used"),
        (build_repair_cli_loop_invocation, "arbitrary_command_executed"),
        (build_repair_cli_loop_rendered_view, "written_to_file"),
        (build_repair_cli_loop_rendered_view, "sent_externally"),
        (build_repair_cli_loop_handoff_packet, "auto_continue_allowed"),
        (build_repair_cli_loop_handoff_packet, "sent_externally"),
    ],
)
def test_invocation_view_handoff_reject_runtime_flags(builder, field_name: str) -> None:
    with pytest.raises(ValueError):
        builder(**{field_name: True})


def test_result_report_and_readiness_preserve_preview_only_boundary() -> None:
    result = build_repair_cli_loop_surface_result()
    report = build_repair_cli_loop_surface_report(result=result)
    readiness = build_v0398_readiness_report(cli_surface_report=report)

    assert isinstance(result, RepairCLILoopSurfaceResult)
    assert result.preview_rendered is True
    assert result.command_denied is False
    assert repair_cli_loop_result_is_not_runtime(result)
    assert result.runtime_executed is False
    assert result.apply_executed is False
    assert result.retest_executed is False
    assert result.prompt_submitted is False
    assert result.model_invoked is False
    assert result.subagent_invoked is False
    assert result.external_agent_invoked is False
    assert result.shell_used is False
    assert result.subprocess_used is False
    assert result.file_exported is False
    assert result.trace_persisted is False
    assert result.dominion_runtime_invoked is False
    assert result.production_certified is False
    assert result.ready_for_execution is False

    denied_result = build_repair_cli_loop_surface_result(command_kind=RepairCLILoopSurfaceCommandKind.DENIED_APPLY)
    assert denied_result.preview_rendered is False
    assert denied_result.command_denied is True
    assert denied_result.denied_command is not None

    assert isinstance(report, RepairCLILoopSurfaceReport)
    assert report.ready_for_v0399_consolidation_input is True
    assert report.surface_completed is True
    assert report.preview_only is True
    assert repair_cli_loop_report_is_preview_only(report)
    assert report.runtime_executed is False
    assert report.apply_executed is False
    assert report.retest_executed is False
    assert report.prompt_executed is False
    assert report.model_invoked is False
    assert report.subagent_invoked is False
    assert report.external_agent_invoked is False
    assert report.trace_persisted is False
    assert report.dominion_runtime_invoked is False
    assert report.production_certified is False
    assert report.ready_for_execution is False

    assert isinstance(readiness, V0398ReadinessReport)
    assert readiness.ready_for_v0399_consolidation is True
    assert readiness.ready_for_cli_loop_state_surface is True
    assert readiness.ready_for_cli_command_registry is True
    assert readiness.ready_for_cli_invocation_parser is True
    assert readiness.ready_for_cli_preview_renderer is True
    assert readiness.ready_for_cli_loop_bundle_preview is True
    assert readiness.ready_for_cli_human_handoff_preview is True
    assert readiness.ready_for_future_v0399_consolidation_input is True
    assert readiness.preview_only is True
    assert readiness.cli_runtime_execution_enabled is False
    assert readiness.cli_apply_execution_enabled is False
    assert readiness.cli_retest_execution_enabled is False
    assert readiness.cli_prompt_submission_enabled is False
    assert readiness.cli_model_invocation_enabled is False
    assert readiness.cli_subagent_invocation_enabled is False
    assert readiness.shell_enabled is False
    assert readiness.subprocess_enabled is False
    assert readiness.file_export_enabled is False
    assert readiness.trace_persistence_enabled is False
    assert readiness.dominion_runtime_enabled is False
    assert readiness.production_certified is False
    assert readiness.ready_for_execution is False
    assert v0398_readiness_report_is_not_execution_ready(readiness)


@pytest.mark.parametrize(
    ("builder", "field_name"),
    [
        (build_repair_cli_loop_surface_result, "runtime_executed"),
        (build_repair_cli_loop_surface_result, "apply_executed"),
        (build_repair_cli_loop_surface_result, "file_exported"),
        (build_repair_cli_loop_surface_result, "ready_for_execution"),
        (build_repair_cli_loop_surface_report, "preview_only"),
        (build_repair_cli_loop_surface_report, "runtime_executed"),
        (build_repair_cli_loop_surface_report, "ready_for_execution"),
        (build_v0398_readiness_report, "cli_runtime_execution_enabled"),
        (build_v0398_readiness_report, "ready_for_execution"),
    ],
)
def test_result_report_readiness_reject_unsafe_flags(builder, field_name: str) -> None:
    value = False if field_name == "preview_only" else True
    with pytest.raises(ValueError):
        builder(**{field_name: value})


def test_validation_and_preview_only_guarantee_confirm_no_runtime() -> None:
    validation = build_repair_cli_loop_surface_validation_report()
    guarantee = build_repair_cli_loop_surface_preview_only_guarantee()

    assert validation.preview_only_confirmed is True
    assert validation.no_apply_execution_confirmed is True
    assert validation.no_retest_execution_confirmed is True
    assert validation.no_prompt_submission_confirmed is True
    assert validation.no_model_invocation_confirmed is True
    assert validation.no_subagent_invocation_confirmed is True
    assert validation.no_external_agent_confirmed is True
    assert validation.no_shell_confirmed is True
    assert validation.no_subprocess_confirmed is True
    assert validation.no_arbitrary_command_confirmed is True
    assert validation.no_file_export_confirmed is True
    assert validation.no_external_send_confirmed is True
    assert validation.no_trace_persistence_confirmed is True
    assert validation.no_pig_execution_confirmed is True
    assert validation.no_dominion_runtime_confirmed is True
    assert validation.no_production_certification_confirmed is True

    assert isinstance(guarantee, RepairCLILoopSurfacePreviewOnlyGuarantee)
    assert guarantee.no_cli_runtime_execution is True
    assert guarantee.no_cli_apply_execution is True
    assert guarantee.no_cli_retest_execution is True
    assert guarantee.no_prompt_submission is True
    assert guarantee.no_model_invocation is True
    assert guarantee.no_prompt_execution is True
    assert guarantee.no_next_action_execution is True
    assert guarantee.no_subagent_invocation is True
    assert guarantee.no_external_agent is True
    assert guarantee.no_shell is True
    assert guarantee.no_subprocess is True
    assert guarantee.no_arbitrary_command is True
    assert guarantee.no_dependency_install is True
    assert guarantee.no_network_access is True
    assert guarantee.no_file_export is True
    assert guarantee.no_external_send is True
    assert guarantee.no_trace_persistence is True
    assert guarantee.no_ocel_write is True
    assert guarantee.no_ocpx_persistence is True
    assert guarantee.no_pig_execution is True
    assert guarantee.no_autonomous_loop is True
    assert guarantee.no_retry_loop is True
    assert guarantee.no_multi_cycle_loop is True
    assert guarantee.no_repair_execution is True
    assert guarantee.no_dominion_runtime is True
    assert guarantee.no_production_certification is True


def test_preview_pipeline_is_in_memory_and_does_not_execute() -> None:
    cli_input = build_repair_cli_loop_surface_input(argv=["bundle"])
    report = run_repair_cli_loop_surface_preview(cli_input)
    report_from_alias = create_repair_cli_loop_surface_report(cli_input)

    assert report.invocation.command_kind == RepairCLILoopSurfaceCommandKind.LOOP_BUNDLE_PREVIEW
    assert report.result.preview_rendered is True
    assert report.result.bundle_view is not None
    assert report.ready_for_execution is False
    assert report_from_alias.preview_only is True

    denied_input = build_repair_cli_loop_surface_input(argv=["shell"])
    denied_report = run_repair_cli_loop_surface_preview(denied_input)
    assert denied_report.result.command_denied is True
    assert denied_report.result.denied_command is not None
    assert denied_report.result.shell_used is False
    assert denied_report.result.subprocess_used is False
