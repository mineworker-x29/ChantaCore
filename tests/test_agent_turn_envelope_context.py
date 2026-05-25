from chanta_core.agent_surface import (
    AGENT_TURN_EFFECT_TYPES,
    AGENT_TURN_EVENT_TYPES,
    AGENT_TURN_OBJECT_TYPES,
    AgentContextBoundaryPolicy,
    AgentContextBoundaryPolicyService,
    AgentContextRef,
    AgentContextRefService,
    AgentInteractionSession,
    AgentRequestContextView,
    AgentRequestContextViewService,
    AgentSurfaceContractReportService,
    AgentTurnContext,
    AgentTurnEnvelope,
    AgentTurnEnvelopePolicy,
    AgentTurnEnvelopePolicyService,
    AgentTurnEnvelopeService,
    AgentTurnReport,
    AgentTurnReportService,
    AgentTurnSourceDescriptor,
    AgentTurnSourceDescriptorService,
    AgentTurnTrace,
    AgentUserRequestSanitizationService,
    AgentUserRequestView,
)
from chanta_core.cli.main import main


def test_agent_turn_policy_session_source_request_context_and_envelope_build() -> None:
    service = AgentTurnReportService()
    report = service.build_report(request_text="Explain the project structure")

    assert isinstance(report.policy, AgentTurnEnvelopePolicy)
    assert isinstance(report.session, AgentInteractionSession)
    assert isinstance(report.envelope.source_descriptor, AgentTurnSourceDescriptor)
    assert isinstance(report.envelope.user_request_view, AgentUserRequestView)
    assert isinstance(report.context_view, AgentRequestContextView)
    assert isinstance(report.envelope.turn_context, AgentTurnContext)
    assert isinstance(report.envelope, AgentTurnEnvelope)
    assert isinstance(report.trace, AgentTurnTrace)
    assert isinstance(report, AgentTurnReport)
    assert report.version == "v0.25.1"
    assert report.ready_for_v0_25_2 is True
    assert report.ready_for_v0_26 is False
    assert report.next_required_step == "v0.25.2 Intent Classification & Task Framing"


def test_v0250_agent_surface_contract_can_be_loaded() -> None:
    contract = AgentSurfaceContractReportService().build_report().contract

    assert contract.version == "v0.25.0"
    assert contract.layer == "agent_surface"
    assert contract.status == "contract_only"


def test_envelope_policy_disables_premature_execution_and_memory() -> None:
    policy = AgentTurnEnvelopePolicyService().build_policy()

    assert policy.envelope_only is True
    assert policy.ask_execution_enabled is False
    assert policy.repl_execution_enabled is False
    assert policy.intent_classification_enabled is False
    assert policy.task_framing_enabled is False
    assert policy.safety_gate_enabled is False
    assert policy.tool_routing_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.raw_secret_storage_forbidden is True
    assert policy.private_path_sanitization_required is True
    assert policy.context_scope == "conversation_local"
    assert policy.ocel_visible is True
    assert policy.pig_visible is True
    assert policy.ocpx_visible is True


def test_request_sanitization_detects_and_redacts_sensitive_shapes() -> None:
    text = "Use api_key=abc123 and token=ghp_example at C:\\Users\\sample\\secret.txt"
    request_view = AgentUserRequestSanitizationService().build_request_view("request:test", text)

    assert request_view.raw_request_stored is False
    assert request_view.secret_like_input_detected is True
    assert request_view.credential_like_input_detected is True
    assert request_view.private_path_like_input_detected is True
    assert request_view.redaction_applied is True
    assert request_view.redaction_count >= 3
    assert request_view.raw_secret_persisted is False
    assert request_view.raw_credential_persisted is False
    assert request_view.private_full_path_output is False
    assert "abc123" not in request_view.sanitized_request_text
    assert "ghp_example" not in request_view.sanitized_request_text
    assert "C:\\Users\\sample" not in request_view.sanitized_request_text


def test_context_boundary_refs_and_context_view_are_sanitized_and_bounded() -> None:
    policy = AgentContextBoundaryPolicyService().build_policy()
    raw_refs = [
        {"context_type": "workspace_snapshot", "source_id": f"workspace:{index}", "summary": "workspace ref"}
        for index in range(policy.max_context_refs + 5)
    ]
    refs = AgentContextRefService().build_context_refs(raw_refs)
    context_view = AgentRequestContextViewService().build_context_view(raw_refs, policy)

    assert isinstance(policy, AgentContextBoundaryPolicy)
    assert policy.context_scope == "conversation_local"
    assert policy.persistent_memory_read_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.raw_provider_output_inline_forbidden is True
    assert policy.raw_secret_context_forbidden is True
    assert all(isinstance(ref, AgentContextRef) for ref in refs)
    assert all(ref.sanitized is True for ref in refs)
    assert all(ref.raw_content_included is False for ref in refs)
    assert all(ref.raw_secret_included is False for ref in refs)
    assert all(ref.private_full_path_included is False for ref in refs)
    assert context_view.included_context_count == policy.max_context_refs
    assert context_view.excluded_context_count == 5
    assert context_view.truncated is True
    assert context_view.persistent_memory_used is False
    assert context_view.memory_promoted is False


def test_turn_context_envelope_trace_and_report_keep_all_execution_flags_false() -> None:
    session, context_view, envelope = AgentTurnEnvelopeService().create_envelope(
        request_text="Explain the project structure"
    )
    report = AgentTurnReportService().build_report(request_text="Explain the project structure")

    assert session.session_scope == "conversation_local"
    assert session.persistent_memory_session is False
    assert session.memory_continuity_enabled is False
    assert session.persona_mutation_enabled is False
    assert envelope.expected_next_stage == "v0.25.2 Intent Classification & Task Framing"
    assert envelope.ask_executed is False
    assert envelope.repl_started is False
    assert envelope.intent_classified is False
    assert envelope.task_framed is False
    assert envelope.safety_gate_evaluated is False
    assert envelope.tool_route_executed is False
    assert envelope.provider_invoked is False
    assert envelope.local_command_executed is False
    assert envelope.memory_promoted is False
    assert envelope.persona_mutated is False
    assert envelope.credential_exposed is False
    assert envelope.raw_secret_output is False
    assert envelope.turn_context.conversation_local is True
    assert envelope.turn_context.persistent_memory_context is False
    assert envelope.turn_context.intent_classification_performed is False
    assert envelope.turn_context.safety_gate_evaluated is False
    assert envelope.turn_context.tool_route_created is False
    assert envelope.turn_context.provider_invoked is False
    assert envelope.turn_context.local_command_executed is False
    assert context_view.persistent_memory_used is False
    assert report.trace.ocel_visible is True
    assert report.trace.raw_secret_in_trace is False
    assert report.trace.private_full_path_in_trace is False
    assert report.turn_envelope_created is True
    assert report.interaction_context_created is True
    assert report.intent_classified is False
    assert report.task_framed is False
    assert report.safety_gate_evaluated is False
    assert report.tool_route_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.ask_executed is False
    assert report.repl_started is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_pig_ocpx_ocel_mapping_and_cli_build() -> None:
    service = AgentTurnReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "agent_turn_envelope" in AGENT_TURN_OBJECT_TYPES
    assert "agent_turn_report_created" in AGENT_TURN_EVENT_TYPES
    assert AGENT_TURN_EFFECT_TYPES == [
        "read_only_observation",
        "agent_turn_received",
        "agent_turn_envelope_created",
        "agent_context_view_created",
        "agent_turn_trace_recorded",
        "state_candidate_created",
    ]
    assert pig["version"] == "v0.25.1"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "turn_envelope_interaction_context"
    assert pig["safety_boundary"]["intent_classified"] is False
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["persistent_memory_written"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "agent_turn_envelope_context_created"
    assert "AgentTurnEnvelopeState" in ocpx["target_read_models"]
    assert main(["agent", "turn", "envelope", "--text", "Explain the project structure"]) == 0
    assert main(["agent", "turn", "context", "--text", "Explain the project structure"]) == 0
    assert main(["agent", "turn", "report", "--text", "Explain the project structure"]) == 0
    assert main(["agent", "turn", "findings", "--report-id", "demo"]) == 0
    assert main(["agent", "session", "view"]) == 0
    assert main(["agent", "context-policy"]) == 0


def test_attempt_flags_create_blocked_findings() -> None:
    report = AgentTurnReportService().build_report(
        attempt_flags={
            "intent_classification_attempted_too_early": True,
            "safety_gate_attempted_too_early": True,
            "provider_invocation_attempted_too_early": True,
            "ask_execution_attempted_too_early": True,
            "memory_promotion_attempted": True,
        }
    )
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "blocked"
    assert "intent_classification_attempted_too_early" in finding_types
    assert "safety_gate_attempted_too_early" in finding_types
    assert "provider_invocation_attempted_too_early" in finding_types
    assert "ask_execution_attempted_too_early" in finding_types
    assert "memory_promotion_attempted" in finding_types
