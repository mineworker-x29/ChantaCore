import pytest

from chanta_core.external_harness import (
    ExternalGatewayManifestCandidate,
    ExternalManifestCandidateKind,
    ExternalManifestCandidateSet,
    ExternalManifestCapabilityKind,
    ExternalManifestEffectSurfaceKind,
    ExternalManifestEvidenceQuality,
    ExternalManifestExtractionFinding,
    ExternalManifestExtractionInput,
    ExternalManifestExtractionReport,
    ExternalManifestExtractionRule,
    ExternalManifestExtractionRunPreview,
    ExternalManifestExtractionStatus,
    ExternalManifestFieldObservation,
    ExternalManifestNoRuntimeGuarantee,
    ExternalManifestRiskSurfaceKind,
    ExternalManifestSourceKind,
    ExternalManifestSourceRef,
    ExternalMissionManifestCandidate,
    ExternalPluginManifestCandidate,
    ExternalProfileManifestCandidate,
    ExternalProviderManifestCandidate,
    ExternalSkillManifestCandidate,
    ExternalToolManifestCandidate,
    ReferenceFileInventoryEntry,
    V0324ReadinessReport,
    build_external_gateway_manifest_candidate,
    build_external_manifest_candidate_set,
    build_external_manifest_extraction_finding,
    build_external_manifest_extraction_input,
    build_external_manifest_extraction_report,
    build_external_manifest_extraction_rule,
    build_external_manifest_extraction_run_preview,
    build_external_manifest_field_observation,
    build_external_manifest_no_runtime_guarantee,
    build_external_manifest_source_ref,
    build_external_mission_manifest_candidate,
    build_external_plugin_manifest_candidate,
    build_external_profile_manifest_candidate,
    build_external_provider_manifest_candidate,
    build_external_skill_manifest_candidate,
    build_external_tool_manifest_candidate,
    build_v0324_readiness_report,
    infer_manifest_candidate_kind_from_inventory_entry,
    infer_manifest_effect_surfaces_from_candidate_kind,
    infer_manifest_risk_surfaces_from_candidate_kind,
    manifest_candidate_preserves_no_activation,
    manifest_candidate_set_is_not_registry,
    manifest_extraction_report_is_not_runtime,
    v0324_readiness_report_is_not_runtime_ready,
)


def test_manifest_extraction_taxonomies_include_required_values() -> None:
    assert {item.value for item in ExternalManifestSourceKind} >= {
        "opencode_observation_output",
        "openclaw_observation_output",
        "hermes_observation_output",
        "external_harness_profile",
        "reference_file_inventory",
        "reference_corpus_snapshot",
        "reference_manifest_path",
        "reference_documentation_path",
        "reference_config_path",
        "manual_manifest_ref",
        "sanitized_manifest",
        "unknown",
    }
    assert {item.value for item in ExternalManifestCandidateKind} >= {
        "skill_manifest",
        "tool_manifest",
        "plugin_manifest",
        "external_plugin_manifest",
        "mission_manifest",
        "gateway_manifest",
        "channel_manifest",
        "provider_manifest",
        "profile_manifest",
        "memory_schema_manifest",
        "approval_policy_manifest",
        "audit_policy_manifest",
        "result_envelope_manifest",
        "ocel_trace_manifest",
        "generic_manifest",
        "unknown",
    }
    assert {item.value for item in ExternalManifestExtractionStatus} >= {
        "unknown",
        "draft",
        "extracted",
        "extracted_with_gaps",
        "blocked",
        "deferred",
        "rejected",
        "future_track",
        "no_op",
    }
    assert {item.value for item in ExternalManifestCapabilityKind} >= {
        "declare_skill",
        "declare_tool",
        "declare_plugin",
        "declare_external_plugin",
        "declare_mission",
        "declare_gateway",
        "declare_channel",
        "declare_provider",
        "declare_profile",
        "declare_memory_schema",
        "declare_approval_policy",
        "declare_audit_policy",
        "declare_result_envelope",
        "declare_ocel_trace",
        "unknown",
    }
    assert {item.value for item in ExternalManifestEffectSurfaceKind} >= {
        "no_effect",
        "file_workspace",
        "tool_registry",
        "plugin_runtime",
        "mission_runtime",
        "gateway_runtime",
        "channel_runtime",
        "provider_runtime",
        "network",
        "credential",
        "command",
        "browser",
        "rpa",
        "delegation",
        "memory",
        "registry",
        "policy",
        "private_data",
        "raw_output",
        "ocel_trace",
        "unknown",
    }
    assert {item.value for item in ExternalManifestRiskSurfaceKind} >= {
        "reference_code_execution",
        "dependency_install",
        "runtime_import",
        "plugin_loading",
        "external_plugin_loading",
        "tool_registration",
        "tool_invocation",
        "mission_installation",
        "mission_execution",
        "provider_invocation",
        "gateway_connection",
        "channel_access",
        "message_send",
        "webhook_call",
        "network_access",
        "credential_access",
        "secret_file_read",
        "command_execution",
        "browser_automation",
        "rpa_control",
        "memory_mutation",
        "registry_mutation",
        "private_data_exposure",
        "raw_output_persistence",
        "ocel_emission",
        "unknown",
    }
    assert {item.value for item in ExternalManifestEvidenceQuality} >= {
        "unknown",
        "none",
        "weak",
        "partial",
        "sufficient_for_manifest_candidate",
        "sufficient_for_risk_classification_review",
        "conflicting",
        "blocked",
    }


def test_source_ref_field_observation_and_extraction_rule_are_static_only() -> None:
    source_ref = build_external_manifest_source_ref(
        source_ref_id="manifest-source:1",
        source_kind=ExternalManifestSourceKind.REFERENCE_FILE_INVENTORY,
        source_id="inventory:1",
        reference_entry_ids=["entry:skill"],
        manifest_path_refs=["references/Hermes/skills/skill.json"],
    )
    field = build_external_manifest_field_observation(
        field_observation_id="field:1",
        field_name="name",
        field_summary="Observed candidate name from static metadata.",
        observed_values=["static-skill"],
        inferred_capability_kinds=[ExternalManifestCapabilityKind.DECLARE_SKILL],
        inferred_effect_surfaces=[ExternalManifestEffectSurfaceKind.REGISTRY],
        inferred_risk_surfaces=[ExternalManifestRiskSurfaceKind.REGISTRY_MUTATION],
    )
    rule = build_external_manifest_extraction_rule(
        rule_id="rule:manifest",
        name="Manifest-like metadata",
        description="Classify manifest-like safe metadata only.",
        source_kinds=[ExternalManifestSourceKind.REFERENCE_FILE_INVENTORY],
        candidate_kinds=[ExternalManifestCandidateKind.SKILL_MANIFEST],
        path_patterns=["skills"],
        file_extensions=[".json"],
        detected_kinds=["manifest_candidate"],
    )

    assert isinstance(source_ref, ExternalManifestSourceRef)
    assert source_ref.source_fetch is False
    assert source_ref.file_execution_or_import is False
    assert isinstance(field, ExternalManifestFieldObservation)
    assert field.manifest_activation is False
    assert isinstance(rule, ExternalManifestExtractionRule)
    assert rule.produces_runtime_effects is False
    assert rule.scanner_runtime is False

    with pytest.raises(ValueError):
        ExternalManifestSourceRef(
            source_ref_id="bad",
            source_kind=ExternalManifestSourceKind.REFERENCE_MANIFEST_PATH,
            source_id="source",
            metadata={"source_fetch": True},
        )
    with pytest.raises(ValueError):
        ExternalManifestExtractionRule(
            rule_id="bad",
            name="Bad",
            description="Bad runtime rule.",
            produces_runtime_effects=True,
        )


def test_specialized_manifest_candidates_are_inactive_design_artifacts() -> None:
    skill = build_external_skill_manifest_candidate("candidate:skill", "static-skill")
    tool = build_external_tool_manifest_candidate("candidate:tool", "static-tool")
    plugin = build_external_plugin_manifest_candidate("candidate:plugin", "static-plugin")
    external_plugin = build_external_plugin_manifest_candidate(
        "candidate:external-plugin",
        "external-static-plugin",
        external_plugin=True,
    )
    mission = build_external_mission_manifest_candidate("candidate:mission", "static-mission")
    gateway = build_external_gateway_manifest_candidate("candidate:gateway", "static-gateway")
    provider = build_external_provider_manifest_candidate("candidate:provider", "static-provider")
    profile = build_external_profile_manifest_candidate("candidate:profile", "static-profile")

    assert isinstance(skill, ExternalSkillManifestCandidate)
    assert manifest_candidate_preserves_no_activation(skill)
    assert skill.active_skill is False
    assert isinstance(tool, ExternalToolManifestCandidate)
    assert tool.registered_tool is False
    assert tool.tool_invocation is False
    assert isinstance(plugin, ExternalPluginManifestCandidate)
    assert plugin.plugin_loading is False
    assert isinstance(external_plugin, ExternalPluginManifestCandidate)
    assert external_plugin.external_plugin is True
    assert ExternalManifestRiskSurfaceKind.EXTERNAL_PLUGIN_LOADING in [ExternalManifestRiskSurfaceKind(value) for value in external_plugin.risk_surfaces]
    assert isinstance(mission, ExternalMissionManifestCandidate)
    assert mission.mission_installation_or_execution is False
    assert isinstance(gateway, ExternalGatewayManifestCandidate)
    assert gateway.gateway_connection_or_message_action is False
    assert isinstance(provider, ExternalProviderManifestCandidate)
    assert provider.provider_network_or_credential_access is False
    assert isinstance(profile, ExternalProfileManifestCandidate)
    assert profile.profile_activation_or_memory_access is False

    for candidate in (skill, tool, plugin, external_plugin, mission, gateway, provider, profile):
        assert candidate.ready_for_manifest_activation is False
        assert candidate.ready_for_execution is False
        assert candidate.active_manifest is False

    with pytest.raises(ValueError):
        ExternalSkillManifestCandidate(
            manifest_candidate_id="candidate:bad",
            candidate_kind=ExternalManifestCandidateKind.SKILL_MANIFEST,
            status=ExternalManifestExtractionStatus.EXTRACTED,
            declared_name="bad",
            proposed_skill_name="bad",
            ready_for_manifest_activation=True,
        )


def test_candidate_set_input_finding_report_preview_guarantee_and_readiness_are_non_runtime() -> None:
    skill = build_external_skill_manifest_candidate("candidate:skill", "static-skill")
    candidate_set = build_external_manifest_candidate_set(
        candidate_set_id="candidate-set:1",
        source_input_id="input:1",
        skill_candidates=[skill],
    )
    extraction_input = build_external_manifest_extraction_input(
        "input:1",
        reference_inventory_ids=["inventory:1"],
        requested_candidate_kinds=[ExternalManifestCandidateKind.SKILL_MANIFEST],
    )
    finding = build_external_manifest_extraction_finding(
        finding_id="finding:1",
        extraction_input_id=extraction_input.extraction_input_id,
        source_ref_ids=["manifest-source:1"],
        candidate_kind=ExternalManifestCandidateKind.SKILL_MANIFEST,
        summary="Skill manifest candidate inferred from static metadata.",
        inferred_capability_kinds=[ExternalManifestCapabilityKind.DECLARE_SKILL],
        inferred_effect_surfaces=[ExternalManifestEffectSurfaceKind.REGISTRY],
        inferred_risk_surfaces=[ExternalManifestRiskSurfaceKind.REGISTRY_MUTATION],
    )
    report = build_external_manifest_extraction_report(
        report_id="report:1",
        extraction_input_id=extraction_input.extraction_input_id,
        candidate_set_id=candidate_set.candidate_set_id,
        findings=[finding],
        extracted_candidate_count=1,
    )
    preview = build_external_manifest_extraction_run_preview(
        planned_steps=["Classify manifest-like inventory metadata."],
        expected_artifacts=["ExternalManifestCandidateSet"],
        explicitly_not_performed=["plugin loading", "tool registration", "mission installation"],
    )
    guarantee = build_external_manifest_no_runtime_guarantee()
    readiness = build_v0324_readiness_report(
        extraction_report_id=report.report_id,
        candidate_set_id=candidate_set.candidate_set_id,
    )

    assert isinstance(candidate_set, ExternalManifestCandidateSet)
    assert manifest_candidate_set_is_not_registry(candidate_set)
    assert isinstance(extraction_input, ExternalManifestExtractionInput)
    assert extraction_input.execution_request is False
    assert "plugin loading" in extraction_input.prohibited_runtime_actions
    assert "tool invocation" in extraction_input.prohibited_runtime_actions
    assert isinstance(finding, ExternalManifestExtractionFinding)
    assert finding.certification is False
    assert finding.manifest_activation is False
    assert isinstance(report, ExternalManifestExtractionReport)
    assert manifest_extraction_report_is_not_runtime(report)
    assert isinstance(preview, ExternalManifestExtractionRunPreview)
    assert preview.execution is False
    assert all(
        getattr(preview, name)
        for name in (
            "no_harness_execution_guarantee",
            "no_reference_code_execution_guarantee",
            "no_install_guarantee",
            "no_import_runtime_guarantee",
            "no_plugin_loading_guarantee",
            "no_tool_registration_guarantee",
            "no_tool_invocation_guarantee",
            "no_mission_installation_guarantee",
            "no_mission_execution_guarantee",
            "no_provider_invocation_guarantee",
            "no_gateway_connection_guarantee",
            "no_network_access_guarantee",
            "no_credential_access_guarantee",
            "no_command_execution_guarantee",
            "no_secret_file_read_guarantee",
        )
    )
    assert isinstance(guarantee, ExternalManifestNoRuntimeGuarantee)
    assert all(
        getattr(guarantee, name)
        for name in (
            "no_manifest_activation",
            "no_harness_execution",
            "no_reference_code_execution",
            "no_dependency_install",
            "no_import_runtime",
            "no_plugin_loading",
            "no_external_plugin_loading",
            "no_tool_registration",
            "no_tool_invocation",
            "no_mission_installation",
            "no_mission_execution",
            "no_gateway_connection",
            "no_provider_invocation",
            "no_network_access",
            "no_credential_access",
            "no_secret_file_read",
            "no_command_execution",
            "no_registry_mutation",
            "no_memory_mutation",
            "no_ocel_emission",
        )
    )
    assert isinstance(readiness, V0324ReadinessReport)
    assert v0324_readiness_report_is_not_runtime_ready(readiness)
    assert {"manifest activation", "harness execution", "reference code execution", "install", "import runtime", "plugin loading", "external plugin loading", "tool registration", "tool invocation", "mission installation", "mission execution", "gateway connection", "provider invocation", "network", "credential", "secret file read", "command", "registry mutation", "memory mutation", "OCEL emission"}.issubset(set(readiness.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        ExternalManifestCandidateSet(
            candidate_set_id="bad",
            version="v0.32.4",
            ready_for_manifest_activation=True,
        )
    with pytest.raises(ValueError):
        ExternalManifestCandidateSet(
            candidate_set_id="bad",
            version="v0.32.4",
            metadata={"registry": True},
        )
    with pytest.raises(ValueError):
        ExternalManifestExtractionReport(
            report_id="bad",
            version="v0.32.4",
            extraction_input_id="input:1",
            ready_for_execution=True,
        )
    for flag_name in (
        "ready_for_plugin_loading",
        "ready_for_tool_registration",
        "ready_for_tool_invocation",
        "ready_for_mission_installation",
        "ready_for_provider_invocation",
        "ready_for_gateway_connection",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_command_execution",
    ):
        with pytest.raises(ValueError):
            V0324ReadinessReport(
                report_id=f"bad:{flag_name}",
                version="v0.32.4",
                **{flag_name: True},
            )


def test_inventory_metadata_can_infer_manifest_candidate_kinds_without_execution(tmp_path) -> None:
    fake_root = tmp_path / "references"
    entries = [
        ReferenceFileInventoryEntry(
            entry_id="entry:skill",
            source_id="source:ref",
            relative_path="Hermes/skills/skill.json",
            file_name="skill.json",
            file_extension=".json",
            detected_kind="manifest_candidate",
            metadata={"local_path_ref": str(fake_root)},
        ),
        ReferenceFileInventoryEntry(
            entry_id="entry:tool",
            source_id="source:ref",
            relative_path="OpenCode/tools/tool.yaml",
            file_name="tool.yaml",
            file_extension=".yaml",
        ),
        ReferenceFileInventoryEntry(
            entry_id="entry:gateway",
            source_id="source:ref",
            relative_path="OpenClaw/gateway/manifest.json",
            file_name="manifest.json",
            file_extension=".json",
        ),
        ReferenceFileInventoryEntry(
            entry_id="entry:provider",
            source_id="source:ref",
            relative_path="Hermes/providers/provider.toml",
            file_name="provider.toml",
            file_extension=".toml",
        ),
        ReferenceFileInventoryEntry(
            entry_id="entry:secret",
            source_id="source:ref",
            relative_path="Hermes/.env",
            file_name=".env",
            file_extension=None,
        ),
    ]

    inferred = [infer_manifest_candidate_kind_from_inventory_entry(entry) for entry in entries]

    assert inferred[:4] == [
        ExternalManifestCandidateKind.SKILL_MANIFEST,
        ExternalManifestCandidateKind.TOOL_MANIFEST,
        ExternalManifestCandidateKind.GATEWAY_MANIFEST,
        ExternalManifestCandidateKind.PROVIDER_MANIFEST,
    ]
    assert inferred[4] == ExternalManifestCandidateKind.UNKNOWN
    assert ExternalManifestRiskSurfaceKind.TOOL_REGISTRATION in infer_manifest_risk_surfaces_from_candidate_kind(ExternalManifestCandidateKind.TOOL_MANIFEST)
    assert ExternalManifestRiskSurfaceKind.PROVIDER_INVOCATION in infer_manifest_risk_surfaces_from_candidate_kind(ExternalManifestCandidateKind.PROVIDER_MANIFEST)
    assert ExternalManifestEffectSurfaceKind.GATEWAY_RUNTIME in infer_manifest_effect_surfaces_from_candidate_kind(ExternalManifestCandidateKind.GATEWAY_MANIFEST)
