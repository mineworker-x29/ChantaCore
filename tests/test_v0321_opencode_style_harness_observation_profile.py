import pytest

from chanta_core.external_harness import (
    OpenCodeCapabilityKind,
    OpenCodeCommandRiskBoundary,
    OpenCodeConfigManifestObservation,
    OpenCodeDigestionHint,
    OpenCodeDominionHint,
    OpenCodeEvidenceQuality,
    OpenCodeHarnessSurfaceKind,
    OpenCodeNoExecutionGuarantee,
    OpenCodeObservationFinding,
    OpenCodeObservationFocusKind,
    OpenCodeObservationOutput,
    OpenCodeObservationRunPreview,
    OpenCodeObservationStatus,
    OpenCodePluginSurfaceObservation,
    OpenCodeProviderHookSurfaceObservation,
    OpenCodeReferenceSourceRef,
    OpenCodeRiskSignal,
    OpenCodeRiskSignalKind,
    OpenCodeStaticObservationInput,
    OpenCodeStyleObservationProfile,
    OpenCodeSurfaceObservation,
    OpenCodeToolRegistrySurfaceObservation,
    OpenCodeWorkspaceSurfaceObservation,
    ReferenceFileInventoryEntry,
    V0321ReadinessReport,
    build_opencode_command_risk_boundary,
    build_opencode_config_manifest_observation,
    build_opencode_digestion_hint,
    build_opencode_dominion_hint,
    build_opencode_no_execution_guarantee,
    build_opencode_observation_finding,
    build_opencode_observation_output,
    build_opencode_observation_run_preview,
    build_opencode_plugin_surface_observation,
    build_opencode_provider_hook_surface_observation,
    build_opencode_reference_source_ref,
    build_opencode_risk_signal,
    build_opencode_static_observation_input,
    build_opencode_style_observation_profile,
    build_opencode_surface_observation,
    build_opencode_tool_registry_surface_observation,
    build_opencode_workspace_surface_observation,
    build_v0321_readiness_report,
    classify_inventory_entry_as_opencode_surface,
    infer_opencode_capability_from_surface,
    infer_opencode_risk_signals_from_inventory_entry,
    opencode_output_is_not_manifest_or_digestive_runtime,
    opencode_profile_preserves_no_execution,
    opencode_run_preview_preserves_no_execution,
    v0321_readiness_report_is_not_runtime_ready,
)


def test_opencode_taxonomies_include_required_values() -> None:
    assert {item.value for item in OpenCodeHarnessSurfaceKind} >= {
        "workspace_tree_surface",
        "file_read_surface",
        "file_write_surface",
        "code_edit_surface",
        "patch_surface",
        "search_surface",
        "tool_registry_surface",
        "tool_invocation_surface",
        "plugin_manifest_surface",
        "plugin_runtime_surface",
        "external_plugin_surface",
        "provider_hook_surface",
        "command_execution_surface",
        "shell_surface",
        "lsp_editor_surface",
        "configuration_manifest_surface",
        "dependency_manifest_surface",
        "approval_boundary_surface",
        "audit_boundary_surface",
        "result_envelope_surface",
        "ocel_trace_surface",
        "unknown",
    }
    assert {item.value for item in OpenCodeObservationFocusKind} >= {
        "workspace_structure",
        "file_operation_model",
        "code_edit_model",
        "patch_model",
        "search_model",
        "tool_registry_model",
        "plugin_model",
        "external_plugin_model",
        "provider_hook_model",
        "command_execution_boundary",
        "shell_boundary",
        "lsp_editor_boundary",
        "dependency_manifest",
        "configuration_manifest",
        "approval_boundary",
        "audit_boundary",
        "result_envelope",
        "ocel_trace_relevance",
        "digestion_relevance",
        "dominion_relevance",
        "unknown",
    }
    assert {item.value for item in OpenCodeCapabilityKind} >= {
        "read_workspace",
        "read_file",
        "write_file",
        "edit_code",
        "apply_patch",
        "search_workspace",
        "invoke_tool",
        "register_tool",
        "load_plugin",
        "load_external_plugin",
        "invoke_provider",
        "execute_command",
        "execute_shell",
        "editor_integration",
        "dependency_resolution",
        "config_loading",
        "approval_gate",
        "audit_trace",
        "result_envelope",
        "unknown",
    }
    assert {item.value for item in OpenCodeRiskSignalKind} >= {
        "workspace_write_risk",
        "code_edit_risk",
        "patch_application_risk",
        "command_execution_risk",
        "shell_execution_risk",
        "provider_invocation_risk",
        "network_access_risk",
        "credential_access_risk",
        "plugin_loading_risk",
        "external_plugin_risk",
        "dependency_install_risk",
        "tool_registry_mutation_risk",
        "tool_invocation_risk",
        "lsp_editor_runtime_risk",
        "raw_output_persistence_risk",
        "secret_file_read_risk",
        "memory_mutation_risk",
        "registry_mutation_risk",
        "ocel_emission_risk",
        "unknown",
    }
    assert {item.value for item in OpenCodeObservationStatus} >= {
        "unknown",
        "draft",
        "observed",
        "observed_with_gaps",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert {item.value for item in OpenCodeEvidenceQuality} >= {
        "unknown",
        "none",
        "weak",
        "partial",
        "sufficient_for_static_observation",
        "sufficient_for_profile",
        "sufficient_for_manifest_extraction_review",
        "conflicting",
        "blocked",
    }


def test_reference_source_ref_is_path_reference_only() -> None:
    source_ref = build_opencode_reference_source_ref(
        source_ref_id="opencode-ref:1",
        reference_source_id="source:opencode",
        reference_inventory_id="inventory:opencode",
        reference_entry_ids=["entry:package"],
        local_path_ref="references/OpenCode",
    )

    assert isinstance(source_ref, OpenCodeReferenceSourceRef)
    assert source_ref.local_path_ref == "references/OpenCode"
    assert source_ref.source_fetch is False
    assert source_ref.execution is False

    with pytest.raises(ValueError):
        OpenCodeReferenceSourceRef(source_ref_id="bad", source_label="")
    with pytest.raises(ValueError):
        OpenCodeReferenceSourceRef(source_ref_id="bad", metadata={"source_fetch": True})


def test_surface_observation_requires_boundaries_for_high_risk_capabilities() -> None:
    observation = build_opencode_surface_observation(
        observation_id="surface:command",
        surface_kind=OpenCodeHarnessSurfaceKind.COMMAND_EXECUTION_SURFACE,
        focus_kind=OpenCodeObservationFocusKind.COMMAND_EXECUTION_BOUNDARY,
        capability_kind=OpenCodeCapabilityKind.EXECUTE_COMMAND,
        title="Command risk surface",
        summary="Command-capable surface is observed as risk only.",
        risk_signal_kinds=[OpenCodeRiskSignalKind.COMMAND_EXECUTION_RISK],
    )

    assert isinstance(observation, OpenCodeSurfaceObservation)
    assert observation.permission is False
    assert "command" in observation.prohibited_runtime_actions

    with pytest.raises(ValueError):
        OpenCodeSurfaceObservation(
            observation_id="surface:bad",
            surface_kind=OpenCodeHarnessSurfaceKind.PATCH_SURFACE,
            focus_kind=OpenCodeObservationFocusKind.PATCH_MODEL,
            capability_kind=OpenCodeCapabilityKind.APPLY_PATCH,
            title="Patch",
            summary="Missing prohibited runtime actions.",
        )


def test_workspace_tool_plugin_provider_command_and_config_observations_are_non_runtime() -> None:
    workspace = build_opencode_workspace_surface_observation(
        "workspace:obs",
        manifest_candidate_paths=["package.json"],
        write_surface_detected=True,
    )
    tools = build_opencode_tool_registry_surface_observation(
        "tools:obs",
        possible_tool_registry_paths=["src/tools"],
        risk_signal_kinds=[OpenCodeRiskSignalKind.TOOL_REGISTRY_MUTATION_RISK],
    )
    plugins = build_opencode_plugin_surface_observation(
        "plugins:obs",
        possible_plugin_manifest_paths=["plugins/example.json"],
        external_plugin_risk_detected=True,
        risk_signal_kinds=[OpenCodeRiskSignalKind.PLUGIN_LOADING_RISK],
    )
    provider = build_opencode_provider_hook_surface_observation(
        "provider:obs",
        possible_provider_config_paths=["provider.json"],
        network_risk_detected=True,
        credential_risk_detected=True,
        risk_signal_kinds=[OpenCodeRiskSignalKind.PROVIDER_INVOCATION_RISK],
    )
    command = build_opencode_command_risk_boundary(
        "command:boundary",
        command_keywords_detected=["exec"],
        required_boundaries=["command execution remains prohibited"],
    )
    config = build_opencode_config_manifest_observation(
        "config:obs",
        possible_package_manifest_paths=["package.json"],
        possible_script_entries=["test"],
        possible_dependency_entries=["typescript"],
    )

    assert isinstance(workspace, OpenCodeWorkspaceSurfaceObservation)
    assert workspace.ready_for_workspace_access is False
    assert workspace.ready_for_workspace_write is False
    assert workspace.ready_for_execution is False
    assert workspace.workspace_access is False
    assert isinstance(tools, OpenCodeToolRegistrySurfaceObservation)
    assert tools.ready_for_tool_registration is False
    assert tools.ready_for_tool_invocation is False
    assert tools.registry_mutation is False
    assert isinstance(plugins, OpenCodePluginSurfaceObservation)
    assert plugins.ready_for_plugin_loading is False
    assert plugins.ready_for_external_plugin_loading is False
    assert plugins.plugin_loading is False
    assert isinstance(provider, OpenCodeProviderHookSurfaceObservation)
    assert provider.ready_for_provider_invocation is False
    assert provider.ready_for_network_access is False
    assert provider.ready_for_credential_access is False
    assert provider.provider_invocation is False
    assert isinstance(command, OpenCodeCommandRiskBoundary)
    assert command.ready_for_command_execution is False
    assert command.ready_for_shell_execution is False
    assert command.command_execution is False
    assert isinstance(config, OpenCodeConfigManifestObservation)
    assert config.ready_for_dependency_install is False
    assert config.ready_for_script_execution is False
    assert config.dependency_install is False

    with pytest.raises(ValueError):
        OpenCodeWorkspaceSurfaceObservation(
            workspace_observation_id="workspace:bad",
            ready_for_workspace_write=True,
        )
    with pytest.raises(ValueError):
        OpenCodePluginSurfaceObservation(
            plugin_observation_id="plugin:bad",
            ready_for_plugin_loading=True,
        )
    with pytest.raises(ValueError):
        OpenCodeProviderHookSurfaceObservation(
            provider_hook_observation_id="provider:bad",
            ready_for_provider_invocation=True,
        )
    with pytest.raises(ValueError):
        OpenCodeCommandRiskBoundary(
            command_boundary_id="command:bad",
            ready_for_command_execution=True,
        )


def test_input_finding_risk_and_hints_are_signals_only() -> None:
    static_input = build_opencode_static_observation_input(
        "opencode-input:1",
        requested_focus=[OpenCodeObservationFocusKind.WORKSPACE_STRUCTURE],
    )
    finding = build_opencode_observation_finding(
        finding_id="finding:1",
        opencode_input_id=static_input.opencode_input_id,
        surface_kind=OpenCodeHarnessSurfaceKind.TOOL_REGISTRY_SURFACE,
        capability_kind=OpenCodeCapabilityKind.REGISTER_TOOL,
        summary="Tool registry surface appears in static inventory.",
        digestion_relevance=True,
        dominion_relevance=True,
    )
    risk = build_opencode_risk_signal(
        risk_signal_id="risk:1",
        finding_id=finding.finding_id,
        signal_kind=OpenCodeRiskSignalKind.TOOL_REGISTRY_MUTATION_RISK,
        severity="high",
        summary="Tool registry mutation risk remains prohibited.",
        recommended_boundary="No registry mutation until later gate.",
    )
    digestion = build_opencode_digestion_hint(
        digestion_hint_id="digestion:1",
        finding_ids=[finding.finding_id],
        candidate_focus=OpenCodeObservationFocusKind.TOOL_REGISTRY_MODEL,
        summary="Static digestion relevance only.",
    )
    dominion = build_opencode_dominion_hint(
        dominion_hint_id="dominion:1",
        finding_ids=[finding.finding_id],
        risk_signal_ids=[risk.risk_signal_id],
        suggested_boundary="Keep tool registry mutation prohibited.",
        summary="Dominion boundary hint only.",
    )

    assert isinstance(static_input, OpenCodeStaticObservationInput)
    assert static_input.execution_request is False
    assert "OpenCode execution" in static_input.prohibited_runtime_actions
    assert isinstance(finding, OpenCodeObservationFinding)
    assert finding.digestion_candidate is False
    assert finding.dominion_target is False
    assert isinstance(risk, OpenCodeRiskSignal)
    assert risk.authority_grant is False
    assert isinstance(digestion, OpenCodeDigestionHint)
    assert digestion.ready_for_internal_candidate_creation is False
    assert digestion.ready_for_execution is False
    assert digestion.internal_skill_candidate is False
    assert isinstance(dominion, OpenCodeDominionHint)
    assert dominion.ready_for_dominion_target_creation is False
    assert dominion.ready_for_external_control is False
    assert dominion.ready_for_execution is False
    assert dominion.dominion_target is False

    with pytest.raises(ValueError):
        build_opencode_risk_signal(
            risk_signal_id="risk:bad",
            finding_id=None,
            signal_kind=OpenCodeRiskSignalKind.COMMAND_EXECUTION_RISK,
            severity="critical",
            summary="Missing conservative route.",
        )
    with pytest.raises(ValueError):
        OpenCodeDigestionHint(
            digestion_hint_id="digestion:bad",
            finding_ids=[],
            candidate_focus=OpenCodeObservationFocusKind.DIGESTION_RELEVANCE,
            suggested_internal_candidate_kind=None,
            summary="Bad readiness.",
            ready_for_internal_candidate_creation=True,
        )
    with pytest.raises(ValueError):
        OpenCodeDominionHint(
            dominion_hint_id="dominion:bad",
            finding_ids=[],
            risk_signal_ids=[],
            suggested_boundary="Boundary",
            summary="Bad readiness.",
            ready_for_dominion_target_creation=True,
        )


def test_profile_output_preview_guarantee_and_readiness_are_non_runtime() -> None:
    profile = build_opencode_style_observation_profile(
        opencode_profile_id="opencode-profile:1",
        display_name="OpenCode-style profile",
        description="Static OpenCode-style observation profile.",
    )
    output = build_opencode_observation_output(
        opencode_output_id="opencode-output:1",
        opencode_input_id="opencode-input:1",
        opencode_profile=profile,
    )
    preview = build_opencode_observation_run_preview(
        planned_steps=["Build static observations from inventory metadata."],
        expected_artifacts=["OpenCodeObservationOutput"],
        explicitly_not_performed=["OpenCode execution", "workspace write", "command execution"],
    )
    guarantee = build_opencode_no_execution_guarantee()
    report = build_v0321_readiness_report(
        opencode_profile_id=profile.opencode_profile_id,
        opencode_output_id=output.opencode_output_id,
    )

    assert isinstance(profile, OpenCodeStyleObservationProfile)
    assert opencode_profile_preserves_no_execution(profile)
    assert isinstance(output, OpenCodeObservationOutput)
    assert opencode_output_is_not_manifest_or_digestive_runtime(output)
    assert isinstance(preview, OpenCodeObservationRunPreview)
    assert opencode_run_preview_preserves_no_execution(preview)
    assert isinstance(guarantee, OpenCodeNoExecutionGuarantee)
    assert guarantee.no_opencode_execution is True
    assert guarantee.no_reference_code_execution is True
    assert guarantee.no_dependency_install is True
    assert guarantee.no_import_runtime is True
    assert guarantee.no_workspace_write is True
    assert guarantee.no_code_edit is True
    assert guarantee.no_patch_application is True
    assert guarantee.no_tool_invocation is True
    assert guarantee.no_tool_registration is True
    assert guarantee.no_plugin_loading is True
    assert guarantee.no_external_plugin_loading is True
    assert guarantee.no_provider_invocation is True
    assert guarantee.no_command_execution is True
    assert guarantee.no_shell_execution is True
    assert guarantee.no_network_access is True
    assert guarantee.no_credential_access is True
    assert guarantee.no_secret_file_read is True
    assert guarantee.no_registry_mutation is True
    assert guarantee.no_memory_mutation is True
    assert guarantee.no_ocel_emission is True
    assert isinstance(report, V0321ReadinessReport)
    assert v0321_readiness_report_is_not_runtime_ready(report)
    assert {"OpenCode execution", "reference code execution", "workspace write", "code edit", "patch application", "tool invocation", "tool registration", "plugin loading", "external plugin loading", "provider invocation", "command", "shell", "network", "credential", "secret file read", "registry mutation", "memory mutation", "OCEL emission"}.issubset(set(report.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        OpenCodeStyleObservationProfile(
            opencode_profile_id="profile:bad",
            base_harness_profile_id=None,
            display_name="Bad",
            description="Bad runtime flag.",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        OpenCodeStyleObservationProfile(
            opencode_profile_id="profile:bad",
            base_harness_profile_id=None,
            display_name="Bad",
            description="Bad runtime flag.",
            ready_for_opencode_execution=True,
        )
    with pytest.raises(ValueError):
        V0321ReadinessReport(
            report_id="report:bad",
            version="v0.32.1",
            opencode_profile_id=None,
            opencode_output_id=None,
            summary="Bad readiness.",
            ready_for_command_execution=True,
        )


def test_inventory_metadata_classification_is_static_and_non_executing(tmp_path) -> None:
    fake_root = tmp_path / "references" / "OpenCode"
    entry = ReferenceFileInventoryEntry(
        entry_id="entry:package",
        source_id="source:opencode",
        relative_path="package.json",
        file_name="package.json",
        file_extension=".json",
        detected_kind="manifest_candidate",
        metadata={"local_path_ref": str(fake_root)},
    )
    provider_entry = ReferenceFileInventoryEntry(
        entry_id="entry:provider",
        source_id="source:opencode",
        relative_path="src/provider/config.json",
        file_name="config.json",
        file_extension=".json",
    )

    surface = classify_inventory_entry_as_opencode_surface(entry)
    provider_surface = classify_inventory_entry_as_opencode_surface(provider_entry)

    assert surface == OpenCodeHarnessSurfaceKind.DEPENDENCY_MANIFEST_SURFACE
    assert infer_opencode_capability_from_surface(surface) == OpenCodeCapabilityKind.DEPENDENCY_RESOLUTION
    assert OpenCodeRiskSignalKind.DEPENDENCY_INSTALL_RISK in infer_opencode_risk_signals_from_inventory_entry(entry)
    assert provider_surface == OpenCodeHarnessSurfaceKind.PROVIDER_HOOK_SURFACE
    assert OpenCodeRiskSignalKind.PROVIDER_INVOCATION_RISK in infer_opencode_risk_signals_from_inventory_entry(provider_entry)
