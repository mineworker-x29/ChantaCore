from __future__ import annotations

from pathlib import Path

from chanta_core.personal_runtime import default_personal_ux_baseline as v0420


def _values(enum_cls: type) -> set[str]:
    return {item.value for item in enum_cls}


def test_v0420_track_identity_declares_ux_hardening_track() -> None:
    identity = v0420.create_v042_track_identity()
    assert identity.version == "v0.42.0"
    assert "Default Personal Runtime UX Hardening" in identity.track_name
    assert "use, inspect, diagnose" in identity.track_goal


def test_v0420_track_identity_references_v0416_baseline_and_no_high_risk_expansion() -> None:
    identity = v0420.create_v042_track_identity()
    assert "v0.41 Default Personal Runtime Opening Track" in identity.previous_track
    assert identity.starting_baseline_version == "v0.41.6"
    assert identity.process_intelligence_review_required is True
    assert identity.high_risk_capability_expansion_allowed is False
    assert identity.production_certified is False


def test_v0420_v0416_user_test_evidence_records_clean_home_pass_values() -> None:
    evidence = v0420.create_v0416_user_test_evidence()
    assert evidence.fresh_home_used is True
    assert evidence.init_passed is True
    assert evidence.profile_status_passed is True
    assert evidence.provider_doctor_no_completion_passed is True
    assert evidence.mock_run_passed is True
    assert evidence.trace_recent_passed is True
    assert evidence.trace_summary_passed is True
    assert evidence.run_report_last_passed is True
    assert evidence.safety_denial_passed is True
    assert evidence.run_count == 1
    assert evidence.denial_count == 1
    assert evidence.provider_call_count_observed == 2
    assert evidence.provider_call_count_semantics == "event_count_not_transaction_count"
    assert evidence.shell_execution_count == 0
    assert evidence.skill_execution_count == 0
    assert evidence.subagent_invocation_count == 0
    assert evidence.production_certification_count == 0
    assert evidence.total_events == 12
    assert evidence.deterministic_mock_flow_passed is True
    assert evidence.configured_provider_flow_verified is False


def test_v0420_v0416_evidence_interpretation_marks_v0416_passed_and_ready_for_v042() -> None:
    interpretation = v0420.interpret_v0416_user_test_evidence()
    assert interpretation.v0416_passed is True
    assert interpretation.v041_track_can_close is True
    assert interpretation.ready_for_v042_ux_hardening is True
    assert interpretation.blockers == ()
    assert interpretation.recommended_next_track == "v0.42 Default Personal Runtime UX Hardening Track"


def test_v0420_known_notes_include_explicit_home_provider_count_configured_provider_version_json_trace_and_diagnostic_gaps() -> None:
    note_ids = {note.note_id for note in v0420.build_v0416_known_notes()}
    assert {
        "explicit-home-required",
        "provider-call-count-semantics",
        "configured-provider-not-manually-verified",
        "package-version-metadata-mismatch",
        "json-trace-readability",
        "diagnostic-bundle-gap",
    } <= note_ids


def test_v0420_ux_pain_point_kinds_declared() -> None:
    assert {
        "default_home_friction",
        "provider_setup_friction",
        "json_trace_readability",
        "run_history_visibility",
        "session_visibility",
        "diagnostic_handoff_gap",
        "version_metadata_mismatch",
        "provider_count_semantics",
        "user_command_discoverability",
        "unknown",
    } <= _values(v0420.V042UXPainPointKind)


def test_v0420_ux_pain_point_register_targets_v0421_to_v0426_without_high_risk_capability() -> None:
    register = v0420.build_v042_ux_pain_point_register()
    targets = {point.recommended_target_version for point in register}
    assert {"v0.42.1", "v0.42.2", "v0.42.3", "v0.42.6"} <= targets
    assert all(point.high_risk_capability_required is False for point in register)


def test_v0420_user_personas_include_primary_user_operator_process_intelligence_reviewer_codex_implementer_and_gpt_design_synthesizer() -> None:
    personas = {persona.persona_id for persona in v0420.build_v042_user_personas()}
    assert {
        "primary_user_operator",
        "process_intelligence_reviewer",
        "codex_implementer",
        "gpt_design_synthesizer",
    } <= personas


def test_v0420_user_review_modes_include_user_flow_command_output_process_trace_and_limited_code_review() -> None:
    assert {
        "user_flow_review",
        "command_output_review",
        "process_trace_review",
        "run_report_review",
        "denial_evidence_review",
        "code_level_review_limited",
        "unknown",
    } <= _values(v0420.V042UserReviewMode)


def test_v0420_user_journey_contract_covers_install_doctor_quickstart_provider_run_trace_history_denial_and_diagnostic_bundle() -> None:
    contract = v0420.build_v042_user_journey_contract()
    kinds = {step.step_kind for step in contract.steps}
    assert {
        "install",
        "first_doctor",
        "quickstart",
        "profile_status",
        "provider_status",
        "mock_run",
        "configured_provider_run",
        "trace_review",
        "run_history_review",
        "session_review",
        "denial_test",
        "diagnostic_bundle",
        "feedback_note",
    } <= kinds
    assert contract.user_can_review_without_code is True
    assert contract.process_trace_review_required is True
    assert contract.high_risk_capabilities_remain_closed is True
    assert all(step.opens_high_risk_capability is False for step in contract.steps)


def test_v0420_command_surface_review_includes_quickstart_provider_setup_trace_timeline_run_history_session_show_report_bundle_and_closed_unsafe_commands() -> None:
    review = v0420.build_v042_command_surface_review()
    commands = {item.command_name for item in review.items}
    assert {
        "chanta-cli quickstart",
        "chanta-cli provider setup",
        "chanta-cli provider status",
        "chanta-cli trace timeline",
        "chanta-cli run history",
        "chanta-cli run show last",
        "chanta-cli session show last",
        "chanta-cli report bundle",
        "chanta-cli feedback note",
        "shell/edit/apply/subagent commands",
    } <= commands
    assert review.default_home_required is True
    assert review.human_readable_outputs_required is True
    assert review.closed_capabilities_visible_to_user is True


def test_v0420_default_home_ux_decision_targets_v0421_and_uses_explicit_env_platform_resolution_order() -> None:
    decision = v0420.create_v042_default_home_ux_decision()
    assert decision.target_version == "v0.42.1"
    assert decision.default_home_path == "%LOCALAPPDATA%\\ChantaCore"
    assert decision.home_resolution_order == (
        "explicit --home",
        "CHANTACORE_HOME",
        "platform default local app data",
    )
    assert decision.should_support_explicit_home is True
    assert decision.should_support_env_override is True
    assert decision.should_auto_create_home is False
    assert "quickstart/init" in decision.safety_notes


def test_v0420_provider_ux_decision_targets_v0422_and_keeps_doctor_completion_tools_and_functions_closed() -> None:
    decision = v0420.create_v042_provider_ux_decision()
    assert decision.target_version == "v0.42.2"
    assert {"mock", "local_openai_compatible", "configured_provider"} <= set(decision.provider_modes)
    assert decision.completion_allowed_only_in_run is True
    assert decision.provider_doctor_completion_allowed is False
    assert decision.tool_calling_allowed is False
    assert decision.function_calling_allowed is False
    assert decision.secret_redaction_required is True


def test_v0420_trace_ux_decision_targets_v0423_and_clarifies_provider_event_vs_transaction_count() -> None:
    decision = v0420.create_v042_trace_ux_decision()
    assert decision.target_version == "v0.42.3"
    assert decision.json_trace_stays_available is True
    assert decision.human_readable_timeline_required is True
    assert decision.run_history_required is True
    assert decision.provider_call_event_vs_transaction_count_must_be_clarified is True


def test_v0420_human_readable_output_needs_include_trace_timeline_run_history_run_show_session_show_provider_status_and_diagnostic_bundle() -> None:
    needs = {need.need_id for need in v0420.build_v042_human_readable_output_needs()}
    assert {
        "trace-timeline",
        "run-history",
        "run-show-last",
        "session-show-last",
        "provider-status",
        "diagnostic-bundle",
    } <= needs


def test_v0420_process_intelligence_review_contract_includes_process_instance_object_link_event_name_denial_evidence_and_untrusted_provider_text_criteria() -> None:
    contract = v0420.build_v042_process_intelligence_review_contract()
    criteria = {criterion.criterion_id for criterion in contract.criteria}
    assert {
        "run-process-instance",
        "object-links",
        "semantic-event-names",
        "event-vs-transaction-count",
        "denial-non-execution",
        "provider-text-untrusted",
        "unsafe-counts-visible",
        "diagnostic-handoff",
    } <= criteria
    assert contract.process_trace_review_required is True
    assert contract.reviewer_persona == "process_intelligence_reviewer"


def test_v0420_user_operability_risk_register_includes_usability_provider_trace_safety_version_diagnostic_and_scope_creep_risks() -> None:
    register = v0420.build_v042_user_operability_risk_register()
    classes = {risk.risk_class for risk in register.risks}
    assert {
        "usability",
        "provider_config",
        "trace_semantics",
        "safety_boundary",
        "version_hygiene",
        "user_diagnostic",
        "scope_creep",
    } <= classes
    assert register.high_risk_count == 2
    assert register.blocks_v0420 is False


def test_v0420_closed_capability_matrix_keeps_high_risk_capabilities_closed_and_production_false() -> None:
    matrix = v0420.build_v042_closed_capability_matrix()
    names = {capability.name for capability in matrix.capabilities}
    assert set(v0420.REQUIRED_CLOSED_CAPABILITIES) <= names
    assert all(capability.closed is True for capability in matrix.capabilities)
    assert matrix.all_required_closed is True
    assert matrix.production_certified is False


def test_v0420_roadmap_contains_v0420_to_v0426_in_order() -> None:
    roadmap = v0420.build_v042_roadmap()
    assert [item.version for item in roadmap.items] == [
        "v0.42.0",
        "v0.42.1",
        "v0.42.2",
        "v0.42.3",
        "v0.42.4",
        "v0.42.5",
        "v0.42.6",
    ]
    assert roadmap.high_risk_expansion_deferred is True
    assert roadmap.user_operability_priority is True
    assert roadmap.process_intelligence_review_priority is True


def test_v0420_roadmap_defers_shell_edit_apply_subagent_general_agentloop_dominion_and_production_certification() -> None:
    roadmap = v0420.build_v042_roadmap()
    for item in roadmap.items:
        closed = set(item.must_not_open)
        assert "shell_execution" in closed
        assert "file_edit" in closed
        assert "patch_apply" in closed
        assert "subagent_invocation" in closed
        assert "general_agent_loop" in closed
        assert "dominion_runtime" in closed
        assert "production_certification" in closed
    chat = next(item for item in roadmap.items if item.version == "v0.42.4")
    assert "Manual loop only" in chat.implementation_scope
    skills = next(item for item in roadmap.items if item.version == "v0.42.5")
    assert "read-only" in skills.implementation_scope
    assert "no broad scan, shell, edit, or apply" in skills.implementation_scope


def test_v0420_readiness_report_sets_baseline_contract_and_handoff_ready_flags_true() -> None:
    report = v0420.create_v0420_readiness_report()
    true_flags = [
        report.v0416_user_test_evidence_captured,
        report.v0416_deterministic_mock_flow_interpreted,
        report.v042_track_identity_defined,
        report.v042_ux_pain_point_register_ready,
        report.v042_user_journey_contract_ready,
        report.v042_command_surface_review_ready,
        report.v042_default_home_decision_ready,
        report.v042_provider_ux_decision_ready,
        report.v042_trace_ux_decision_ready,
        report.v042_process_intelligence_review_contract_ready,
        report.v042_roadmap_ready,
        report.v0421_handoff_ready,
        report.integrated_restore_document_ready,
    ]
    assert all(true_flags)


def test_v0420_readiness_report_keeps_implementation_and_high_risk_flags_false() -> None:
    report = v0420.create_v0420_readiness_report()
    assert report.ready_for_default_home_resolver_implementation is False
    assert report.ready_for_quickstart_command is False
    assert report.ready_for_provider_setup_command is False
    assert report.ready_for_trace_timeline_command is False
    assert report.ready_for_interactive_chat_shell is False
    assert report.ready_for_read_only_skill_execution_as_actions is False
    assert report.ready_for_provider_doctor_completion is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_multi_step_agent_loop is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_autonomous_retry_loop is False
    assert report.ready_for_dominion_runtime is False
    assert report.production_certified is False


def test_v0420_v0421_handoff_targets_default_home_resolver_and_quickstart() -> None:
    handoff = v0420.create_v0421_default_home_quickstart_handoff()
    assert handoff.target_version == "v0.42.1"
    assert "Default Home Resolver & Quickstart" in handoff.title
    assert "default home resolver" in handoff.recommended_focus
    assert "chanta-cli quickstart" in handoff.recommended_focus
    assert "provider doctor completion" in handoff.must_not_open


def test_v0420_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0420.create_v0420_integrated_restore_context_snapshot()
    assert snapshot.current_version == "v0.42.0 Default Personal Runtime UX Baseline & User Journey Contract"
    assert "v042_user_journey_contract" in snapshot.open_capabilities
    assert "process_intelligence_review_contract" in snapshot.open_capabilities
    assert "default_home_resolver_implementation" in snapshot.closed_capabilities
    assert "quickstart_command" in snapshot.closed_capabilities
    assert "production_certification" in snapshot.closed_capabilities


def test_v0420_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0420.create_v0420_integrated_restore_packet()
    assert packet.single_integrated_doc_path == v0420.INTEGRATED_DOC_PATH


def test_v0420_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = v0420.create_v0420_integrated_restore_packet()
    assert packet.separate_restore_doc_created is False


def test_v0420_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0420.create_v0420_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0420_integrated_document_exists_and_has_required_restore_sections() -> None:
    doc = Path(v0420.INTEGRATED_DOC_PATH)
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    for section in v0420.REQUIRED_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0420_integrated_document_contains_v0416_evidence_and_v0421_handoff() -> None:
    text = Path(v0420.INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    assert "run_count=1" in text
    assert "denial_count=1" in text
    assert "provider_call_count=2" in text
    assert "v0.42.1 should implement Default Home Resolver & Quickstart" in text


def test_v0420_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(v0420.INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    assert "You are continuing ChantaCore after v0.42.0." in text
    assert "Next recommended version:" in text
    assert "v0.42.1 Default Home Resolver & Quickstart." in text
    assert "Do not implement provider doctor completion." in text


def test_v0420_no_separate_v0420_restore_document_created() -> None:
    assert not Path("docs/versions/v0.42/v0.42.0_restore_document.md").exists()


def test_v0420_no_separate_v0420_ux_baseline_document_created() -> None:
    assert not Path("docs/versions/v0.42/v0.42.0_ux_baseline.md").exists()
    assert not Path("docs/versions/v0.42/v0.42.0_user_journey_contract.md").exists()
    assert not Path("docs/versions/v0.42/v0.42.0_v042_roadmap.md").exists()


def test_v0420_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/personal_runtime/default_personal_ux_baseline.py").read_text(
        encoding="utf-8"
    )
    lower = source.lower()
    absent_tokens = (
        "subprocess",
        "shell=true",
        "os.system",
        "eval(",
        "exec(",
        "anthropic",
        "ollama",
        "lmstudio",
        "requests",
        "httpx",
        "urllib",
        "socket",
        "apply_patch",
        "git apply",
        "git worktree",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "prompt_submit",
        "provider_invoke",
        "client_create",
        "pytest",
        "unittest",
        "path.write_text",
        "mkdir",
        "makedirs",
    )
    for token in absent_tokens:
        assert token not in lower, f"{token} found in v0.42.0 UX baseline module"
    metadata_only_tokens = (
        "openai",
        "shell_execution",
        "patch_apply",
        "subagent_invocation",
    )
    for token in metadata_only_tokens:
        assert token in lower
    assert "import openai" not in lower
