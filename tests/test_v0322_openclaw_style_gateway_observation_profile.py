import pytest

from chanta_core.external_harness import (
    OpenClawActionSurfaceObservation,
    OpenClawApprovalBoundaryRequirement,
    OpenClawCapabilityKind,
    OpenClawChannelSurfaceObservation,
    OpenClawConfigManifestObservation,
    OpenClawCredentialNetworkBoundaryObservation,
    OpenClawDigestionHint,
    OpenClawDominionHint,
    OpenClawEvidenceQuality,
    OpenClawGatewaySurfaceObservation,
    OpenClawHarnessSurfaceKind,
    OpenClawMessageSurfaceBoundary,
    OpenClawNoExecutionGuarantee,
    OpenClawObservationFinding,
    OpenClawObservationFocusKind,
    OpenClawObservationOutput,
    OpenClawObservationRunPreview,
    OpenClawObservationStatus,
    OpenClawPrivateDataBoundaryObservation,
    OpenClawReferenceSourceRef,
    OpenClawRiskSignal,
    OpenClawRiskSignalKind,
    OpenClawStaticObservationInput,
    OpenClawStyleObservationProfile,
    OpenClawSurfaceObservation,
    ReferenceFileInventoryEntry,
    V0322ReadinessReport,
    build_openclaw_action_surface_observation,
    build_openclaw_approval_boundary_requirement,
    build_openclaw_channel_surface_observation,
    build_openclaw_config_manifest_observation,
    build_openclaw_credential_network_boundary_observation,
    build_openclaw_digestion_hint,
    build_openclaw_dominion_hint,
    build_openclaw_gateway_surface_observation,
    build_openclaw_message_surface_boundary,
    build_openclaw_no_execution_guarantee,
    build_openclaw_observation_finding,
    build_openclaw_observation_output,
    build_openclaw_observation_run_preview,
    build_openclaw_private_data_boundary_observation,
    build_openclaw_reference_source_ref,
    build_openclaw_risk_signal,
    build_openclaw_static_observation_input,
    build_openclaw_style_observation_profile,
    build_openclaw_surface_observation,
    build_v0322_readiness_report,
    classify_inventory_entry_as_openclaw_surface,
    infer_openclaw_capability_from_surface,
    infer_openclaw_risk_signals_from_inventory_entry,
    openclaw_output_is_not_manifest_or_digestive_runtime,
    openclaw_profile_preserves_no_execution,
    openclaw_run_preview_preserves_no_execution,
    v0322_readiness_report_is_not_runtime_ready,
)


def test_openclaw_taxonomies_include_required_values() -> None:
    assert {item.value for item in OpenClawHarnessSurfaceKind} >= {
        "gateway_surface",
        "channel_surface",
        "message_receive_surface",
        "message_send_surface",
        "app_control_surface",
        "external_action_surface",
        "webhook_surface",
        "email_surface",
        "calendar_surface",
        "contact_surface",
        "notification_surface",
        "file_attachment_surface",
        "private_data_surface",
        "credential_surface",
        "network_surface",
        "approval_boundary_surface",
        "audit_boundary_surface",
        "action_manifest_surface",
        "automation_trigger_surface",
        "result_envelope_surface",
        "ocel_trace_surface",
        "unknown",
    }
    assert {item.value for item in OpenClawObservationFocusKind} >= {
        "gateway_model",
        "channel_model",
        "message_flow_model",
        "action_model",
        "webhook_model",
        "email_boundary",
        "calendar_boundary",
        "contact_boundary",
        "notification_boundary",
        "file_attachment_boundary",
        "private_data_boundary",
        "credential_boundary",
        "network_boundary",
        "approval_boundary",
        "audit_boundary",
        "automation_trigger_boundary",
        "result_envelope",
        "ocel_trace_relevance",
        "digestion_relevance",
        "dominion_relevance",
        "unknown",
    }
    assert {item.value for item in OpenClawCapabilityKind} >= {
        "observe_gateway",
        "observe_channel",
        "receive_message",
        "send_message",
        "invoke_app_action",
        "call_webhook",
        "read_email",
        "send_email",
        "read_calendar",
        "modify_calendar",
        "read_contacts",
        "send_notification",
        "read_attachment",
        "access_private_data",
        "use_credential",
        "access_network",
        "request_approval",
        "record_audit",
        "emit_result_envelope",
        "unknown",
    }
    assert {item.value for item in OpenClawRiskSignalKind} >= {
        "gateway_control_risk",
        "channel_access_risk",
        "message_send_risk",
        "email_send_risk",
        "calendar_write_risk",
        "contact_access_risk",
        "notification_send_risk",
        "attachment_access_risk",
        "private_data_exposure_risk",
        "credential_access_risk",
        "network_access_risk",
        "webhook_call_risk",
        "app_control_risk",
        "external_side_effect_risk",
        "approval_bypass_risk",
        "audit_gap_risk",
        "raw_output_persistence_risk",
        "memory_mutation_risk",
        "registry_mutation_risk",
        "ocel_emission_risk",
        "unknown",
    }
    assert {item.value for item in OpenClawObservationStatus} >= {
        "unknown",
        "draft",
        "observed",
        "observed_with_gaps",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert {item.value for item in OpenClawEvidenceQuality} >= {
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
    source_ref = build_openclaw_reference_source_ref(
        source_ref_id="openclaw-ref:1",
        reference_source_id="source:openclaw",
        reference_inventory_id="inventory:openclaw",
        reference_entry_ids=["entry:gateway"],
        local_path_ref="references/OpenClaw",
    )

    assert isinstance(source_ref, OpenClawReferenceSourceRef)
    assert source_ref.source_fetch is False
    assert source_ref.execution is False

    with pytest.raises(ValueError):
        OpenClawReferenceSourceRef(source_ref_id="bad", source_label="")
    with pytest.raises(ValueError):
        OpenClawReferenceSourceRef(source_ref_id="bad", metadata={"execution": True})


def test_surface_observation_requires_boundaries_for_high_risk_capabilities() -> None:
    observation = build_openclaw_surface_observation(
        observation_id="surface:webhook",
        surface_kind=OpenClawHarnessSurfaceKind.WEBHOOK_SURFACE,
        focus_kind=OpenClawObservationFocusKind.WEBHOOK_MODEL,
        capability_kind=OpenClawCapabilityKind.CALL_WEBHOOK,
        title="Webhook risk surface",
        summary="Webhook surface is observed as risk only.",
        risk_signal_kinds=[OpenClawRiskSignalKind.WEBHOOK_CALL_RISK],
    )

    assert isinstance(observation, OpenClawSurfaceObservation)
    assert observation.permission is False
    assert "webhook call" in observation.prohibited_runtime_actions

    with pytest.raises(ValueError):
        OpenClawSurfaceObservation(
            observation_id="surface:bad",
            surface_kind=OpenClawHarnessSurfaceKind.MESSAGE_SEND_SURFACE,
            focus_kind=OpenClawObservationFocusKind.MESSAGE_FLOW_MODEL,
            capability_kind=OpenClawCapabilityKind.SEND_MESSAGE,
            title="Message",
            summary="Missing prohibited runtime actions.",
        )


def test_gateway_channel_action_message_private_credential_approval_and_config_are_non_runtime() -> None:
    gateway = build_openclaw_gateway_surface_observation(
        "gateway:obs",
        possible_gateway_manifest_paths=["gateway.json"],
        gateway_control_risk_detected=True,
    )
    channel = build_openclaw_channel_surface_observation(
        "channel:obs",
        possible_channel_manifest_paths=["channels.json"],
        message_send_surface_detected=True,
    )
    action = build_openclaw_action_surface_observation(
        "action:obs",
        possible_action_manifest_paths=["actions.json"],
        external_side_effect_risk_detected=True,
    )
    message = build_openclaw_message_surface_boundary(
        "message:boundary",
        send_keywords_detected=["send"],
        required_boundaries=["message send remains prohibited"],
    )
    private_data = build_openclaw_private_data_boundary_observation(
        "private:boundary",
        possible_private_data_paths=["private/data"],
        pii_sensitive_surface_detected=True,
    )
    credential_network = build_openclaw_credential_network_boundary_observation(
        "credential-network:boundary",
        possible_credential_paths=["config/token.json"],
        possible_webhook_paths=["webhooks/send.json"],
    )
    approval = build_openclaw_approval_boundary_requirement(
        "approval:boundary",
        approval_required_for_surfaces=[OpenClawHarnessSurfaceKind.MESSAGE_SEND_SURFACE],
        approval_gap_detected=True,
    )
    config = build_openclaw_config_manifest_observation(
        "config:obs",
        possible_package_manifest_paths=["package.json"],
        possible_action_manifest_paths=["actions.json"],
        possible_script_entries=["send"],
    )

    assert isinstance(gateway, OpenClawGatewaySurfaceObservation)
    assert gateway.ready_for_gateway_connection is False
    assert gateway.ready_for_gateway_control is False
    assert gateway.ready_for_network_access is False
    assert gateway.ready_for_credential_access is False
    assert gateway.gateway_runtime is False
    assert isinstance(channel, OpenClawChannelSurfaceObservation)
    assert channel.ready_for_channel_access is False
    assert channel.ready_for_message_receive is False
    assert channel.ready_for_message_send is False
    assert channel.channel_access is False
    assert isinstance(action, OpenClawActionSurfaceObservation)
    assert action.ready_for_action_execution is False
    assert action.ready_for_external_action is False
    assert action.action_execution is False
    assert isinstance(message, OpenClawMessageSurfaceBoundary)
    assert message.ready_for_message_send is False
    assert message.ready_for_message_receive is False
    assert message.message_operation is False
    assert isinstance(private_data, OpenClawPrivateDataBoundaryObservation)
    assert private_data.ready_for_private_data_access is False
    assert private_data.ready_for_attachment_access is False
    assert private_data.private_data_access is False
    assert isinstance(credential_network, OpenClawCredentialNetworkBoundaryObservation)
    assert credential_network.ready_for_credential_access is False
    assert credential_network.ready_for_network_access is False
    assert credential_network.ready_for_webhook_call is False
    assert credential_network.credential_or_network_access is False
    assert isinstance(approval, OpenClawApprovalBoundaryRequirement)
    assert approval.approval_granted is False
    assert approval.ready_for_action_execution is False
    assert approval.approval_is_granted is False
    assert isinstance(config, OpenClawConfigManifestObservation)
    assert config.ready_for_dependency_install is False
    assert config.ready_for_script_execution is False
    assert config.dependency_install is False

    with pytest.raises(ValueError):
        OpenClawGatewaySurfaceObservation(gateway_observation_id="bad", ready_for_gateway_connection=True)
    with pytest.raises(ValueError):
        OpenClawChannelSurfaceObservation(channel_observation_id="bad", ready_for_channel_access=True)
    with pytest.raises(ValueError):
        OpenClawMessageSurfaceBoundary(message_boundary_id="bad", ready_for_message_send=True)
    with pytest.raises(ValueError):
        OpenClawPrivateDataBoundaryObservation(private_data_boundary_id="bad", ready_for_private_data_access=True)
    with pytest.raises(ValueError):
        OpenClawCredentialNetworkBoundaryObservation(credential_network_boundary_id="bad", ready_for_credential_access=True)
    with pytest.raises(ValueError):
        OpenClawCredentialNetworkBoundaryObservation(credential_network_boundary_id="bad", ready_for_network_access=True)
    with pytest.raises(ValueError):
        OpenClawApprovalBoundaryRequirement(approval_boundary_id="bad", approval_granted=True)


def test_input_finding_risk_and_hints_are_signals_only() -> None:
    static_input = build_openclaw_static_observation_input(
        "openclaw-input:1",
        requested_focus=[OpenClawObservationFocusKind.GATEWAY_MODEL],
    )
    finding = build_openclaw_observation_finding(
        finding_id="finding:1",
        openclaw_input_id=static_input.openclaw_input_id,
        surface_kind=OpenClawHarnessSurfaceKind.MESSAGE_SEND_SURFACE,
        capability_kind=OpenClawCapabilityKind.SEND_MESSAGE,
        summary="Message send surface appears in static inventory.",
        digestion_relevance=True,
        dominion_relevance=True,
    )
    risk = build_openclaw_risk_signal(
        risk_signal_id="risk:1",
        finding_id=finding.finding_id,
        signal_kind=OpenClawRiskSignalKind.MESSAGE_SEND_RISK,
        severity="critical",
        summary="Message send risk remains prohibited.",
        recommended_boundary="No message send until later gate.",
    )
    digestion = build_openclaw_digestion_hint(
        digestion_hint_id="digestion:1",
        finding_ids=[finding.finding_id],
        candidate_focus=OpenClawObservationFocusKind.ACTION_MODEL,
        summary="Static digestion relevance only.",
    )
    dominion = build_openclaw_dominion_hint(
        dominion_hint_id="dominion:1",
        finding_ids=[finding.finding_id],
        risk_signal_ids=[risk.risk_signal_id],
        suggested_boundary="Keep message send prohibited.",
        summary="Dominion boundary hint only.",
    )

    assert isinstance(static_input, OpenClawStaticObservationInput)
    assert static_input.execution_request is False
    assert "OpenClaw execution" in static_input.prohibited_runtime_actions
    assert isinstance(finding, OpenClawObservationFinding)
    assert finding.digestion_candidate is False
    assert finding.dominion_target is False
    assert isinstance(risk, OpenClawRiskSignal)
    assert risk.authority_grant is False
    assert isinstance(digestion, OpenClawDigestionHint)
    assert digestion.ready_for_internal_candidate_creation is False
    assert digestion.internal_skill_candidate is False
    assert isinstance(dominion, OpenClawDominionHint)
    assert dominion.ready_for_dominion_target_creation is False
    assert dominion.ready_for_external_control is False
    assert dominion.dominion_target is False

    with pytest.raises(ValueError):
        build_openclaw_risk_signal(
            risk_signal_id="risk:bad",
            finding_id=None,
            signal_kind=OpenClawRiskSignalKind.WEBHOOK_CALL_RISK,
            severity="high",
            summary="Missing conservative route.",
        )
    with pytest.raises(ValueError):
        OpenClawDigestionHint(
            digestion_hint_id="digestion:bad",
            finding_ids=[],
            candidate_focus=OpenClawObservationFocusKind.DIGESTION_RELEVANCE,
            suggested_internal_candidate_kind=None,
            summary="Bad readiness.",
            ready_for_internal_candidate_creation=True,
        )
    with pytest.raises(ValueError):
        OpenClawDominionHint(
            dominion_hint_id="dominion:bad",
            finding_ids=[],
            risk_signal_ids=[],
            suggested_boundary="Boundary",
            summary="Bad readiness.",
            ready_for_dominion_target_creation=True,
        )


def test_profile_output_preview_guarantee_and_readiness_are_non_runtime() -> None:
    profile = build_openclaw_style_observation_profile(
        openclaw_profile_id="openclaw-profile:1",
        display_name="OpenClaw-style profile",
        description="Static OpenClaw-style gateway/action observation profile.",
    )
    output = build_openclaw_observation_output(
        openclaw_output_id="openclaw-output:1",
        openclaw_input_id="openclaw-input:1",
        openclaw_profile=profile,
    )
    preview = build_openclaw_observation_run_preview(
        planned_steps=["Build static observations from inventory metadata."],
        expected_artifacts=["OpenClawObservationOutput"],
        explicitly_not_performed=["OpenClaw execution", "gateway connection", "message send"],
    )
    guarantee = build_openclaw_no_execution_guarantee()
    report = build_v0322_readiness_report(
        openclaw_profile_id=profile.openclaw_profile_id,
        openclaw_output_id=output.openclaw_output_id,
    )

    assert isinstance(profile, OpenClawStyleObservationProfile)
    assert openclaw_profile_preserves_no_execution(profile)
    assert isinstance(output, OpenClawObservationOutput)
    assert openclaw_output_is_not_manifest_or_digestive_runtime(output)
    assert isinstance(preview, OpenClawObservationRunPreview)
    assert openclaw_run_preview_preserves_no_execution(preview)
    assert isinstance(guarantee, OpenClawNoExecutionGuarantee)
    assert guarantee.no_openclaw_execution is True
    assert guarantee.no_reference_code_execution is True
    assert guarantee.no_dependency_install is True
    assert guarantee.no_import_runtime is True
    assert guarantee.no_gateway_connection is True
    assert guarantee.no_gateway_control is True
    assert guarantee.no_channel_access is True
    assert guarantee.no_message_receive is True
    assert guarantee.no_message_send is True
    assert guarantee.no_email_access is True
    assert guarantee.no_email_send is True
    assert guarantee.no_calendar_access is True
    assert guarantee.no_calendar_write is True
    assert guarantee.no_contact_access is True
    assert guarantee.no_notification_send is True
    assert guarantee.no_attachment_access is True
    assert guarantee.no_private_data_access is True
    assert guarantee.no_credential_access is True
    assert guarantee.no_webhook_call is True
    assert guarantee.no_network_access is True
    assert guarantee.no_command_execution is True
    assert guarantee.no_provider_invocation is True
    assert guarantee.no_registry_mutation is True
    assert guarantee.no_memory_mutation is True
    assert guarantee.no_ocel_emission is True
    assert isinstance(report, V0322ReadinessReport)
    assert v0322_readiness_report_is_not_runtime_ready(report)
    assert {"OpenClaw execution", "reference code execution", "gateway connection", "gateway control", "channel access", "message receive", "message send", "email access", "email send", "calendar access", "calendar write", "contact access", "notification send", "attachment access", "private data access", "credential access", "webhook call", "network", "command", "provider invocation", "registry mutation", "memory mutation", "OCEL emission"}.issubset(set(report.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        OpenClawStyleObservationProfile(
            openclaw_profile_id="profile:bad",
            base_harness_profile_id=None,
            display_name="Bad",
            description="Bad runtime flag.",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        OpenClawStyleObservationProfile(
            openclaw_profile_id="profile:bad",
            base_harness_profile_id=None,
            display_name="Bad",
            description="Bad runtime flag.",
            ready_for_openclaw_execution=True,
        )
    with pytest.raises(ValueError):
        V0322ReadinessReport(
            report_id="report:bad",
            version="v0.32.2",
            openclaw_profile_id=None,
            openclaw_output_id=None,
            summary="Bad readiness.",
            ready_for_message_send=True,
        )


def test_inventory_metadata_classification_is_static_and_non_executing(tmp_path) -> None:
    fake_root = tmp_path / "references" / "OpenClaw"
    gateway_entry = ReferenceFileInventoryEntry(
        entry_id="entry:gateway",
        source_id="source:openclaw",
        relative_path="gateway/config.json",
        file_name="config.json",
        file_extension=".json",
        detected_kind="manifest_candidate",
        metadata={"local_path_ref": str(fake_root)},
    )
    webhook_entry = ReferenceFileInventoryEntry(
        entry_id="entry:webhook",
        source_id="source:openclaw",
        relative_path="actions/webhook/send.json",
        file_name="send.json",
        file_extension=".json",
    )

    gateway_surface = classify_inventory_entry_as_openclaw_surface(gateway_entry)
    webhook_surface = classify_inventory_entry_as_openclaw_surface(webhook_entry)

    assert gateway_surface == OpenClawHarnessSurfaceKind.GATEWAY_SURFACE
    assert infer_openclaw_capability_from_surface(gateway_surface) == OpenClawCapabilityKind.OBSERVE_GATEWAY
    assert OpenClawRiskSignalKind.GATEWAY_CONTROL_RISK in infer_openclaw_risk_signals_from_inventory_entry(gateway_entry)
    assert webhook_surface == OpenClawHarnessSurfaceKind.WEBHOOK_SURFACE
    assert OpenClawRiskSignalKind.WEBHOOK_CALL_RISK in infer_openclaw_risk_signals_from_inventory_entry(webhook_entry)
