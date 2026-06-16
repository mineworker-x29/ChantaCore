from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime.default_personal_business_ux import (
    INTEGRATED_DOC_PATH,
    REQUIRED_V0429_DOC_SECTIONS,
    V042BusinessOutputAudience,
    V042BusinessOutputVerbosity,
    V042BusinessUXMode,
    create_v042_business_chat_banner,
    create_v042_business_chat_help_view,
    create_v042_business_chat_render_policy,
    create_v042_business_command_guide,
    create_v042_business_empty_response_view,
    create_v042_business_provider_status_view,
    create_v042_business_run_render_policy,
    create_v042_debug_disclosure_policy,
    create_v042_operation_readiness_report,
    create_v042_runtime_identity_answer_policy,
    create_v042_user_facing_error_card,
    create_v042_ux_polish_report,
    create_v0429_readiness_report,
    render_v042_business_run_output,
)


def _run_cli(args: list[str]) -> tuple[int, str]:
    output = io.StringIO()
    with redirect_stdout(output):
        code = cli_main(args)
    return code, output.getvalue()


def test_v0429_business_ux_modes_declared() -> None:
    assert {item.value for item in V042BusinessUXMode} >= {"default", "debug", "verbose", "json", "compact", "unknown"}
    assert {item.value for item in V042BusinessOutputVerbosity} >= {"clean", "normal", "detailed", "debug", "json", "unknown"}


def test_v0429_business_output_audiences_declared() -> None:
    assert {item.value for item in V042BusinessOutputAudience} >= {
        "business_user",
        "operator",
        "developer",
        "process_intelligence_reviewer",
        "unknown",
    }


def test_v0429_business_run_policy_hides_internal_trace_banner_by_default() -> None:
    policy = create_v042_business_run_render_policy()
    assert policy.default_audience == "business_user"
    assert policy.show_internal_trace_banner_by_default is False
    assert policy.show_provider_untrusted_warning_by_default is False
    assert policy.show_debug_fields_only_with_debug is True


def test_v0429_business_run_policy_preserves_debug_and_json_output() -> None:
    policy = create_v042_business_run_render_policy()
    assert policy.preserve_debug_output is True
    assert policy.preserve_json_output is True


def test_v0429_business_run_render_default_contains_assistant_text_without_raw_trace_banner() -> None:
    result = render_v042_business_run_output("Work answer", "run-1", "session-1")
    assert "Work answer" in result.rendered_text
    assert "[v0.41.5 traced" not in result.rendered_text
    assert "trace runtime emitted" not in result.rendered_text
    assert "provider text is untrusted" not in result.rendered_text
    assert result.debug_fields_hidden is True


def test_v0429_business_run_render_debug_contains_run_session_parse_and_trace_fields() -> None:
    result = render_v042_business_run_output("Work answer", "run-1", "session-1", "debug", "parsed", "none", 7)
    assert "ChantaCore Run Debug" in result.rendered_text
    assert "run_id: run-1" in result.rendered_text
    assert "session_id: session-1" in result.rendered_text
    assert "response_parse_status: parsed" in result.rendered_text
    assert "trace_event_count: 7" in result.rendered_text
    assert result.debug_fields_hidden is False


def test_v0429_business_chat_policy_uses_clean_prompt_and_grouped_help() -> None:
    policy = create_v042_business_chat_render_policy()
    assert policy.prompt_label == "ChantaCore>"
    assert policy.show_provider_in_prompt is False
    assert policy.show_turn_count_in_prompt is False
    assert policy.group_help_by_purpose is True


def test_v0429_business_chat_banner_is_clean_and_not_developer_jargon() -> None:
    banner = create_v042_business_chat_banner(session_id="session-test")
    assert "ChantaCore Agent" in banner.rendered_text
    assert "Type /help for commands" in banner.rendered_text
    assert "bounded append-only" not in banner.rendered_text
    assert "provider text is untrusted" not in banner.rendered_text


def test_v0429_business_chat_help_groups_conversation_status_review_safety_commands() -> None:
    help_view = create_v042_business_chat_help_view()
    for heading in ("Conversation", "Status", "Review", "Safety"):
        assert heading in help_view.rendered_text
    assert "/status" in help_view.rendered_text
    assert "/trace" in help_view.rendered_text
    assert help_view.includes_developer_jargon is False
    assert help_view.includes_shell_safety_statement is True


def test_v0429_business_provider_status_view_distinguishes_ready_not_configured_and_needs_attention() -> None:
    default_view = create_v042_business_provider_status_view()
    assert default_view.status_label in {"Ready", "Not configured", "Needs attention"}
    ready = create_v042_business_provider_status_view(
        configured_provider_ready=True,
        status_label="Ready",
        rendered_text="Provider\nStatus: Ready",
    )
    attention = create_v042_business_provider_status_view(
        configured_provider_ready=False,
        status_label="Needs attention",
        rendered_text="Provider\nStatus: Needs attention",
    )
    assert ready.status_label == "Ready"
    assert attention.status_label == "Needs attention"


def test_v0429_business_provider_status_view_does_not_show_secrets() -> None:
    view = create_v042_business_provider_status_view()
    assert view.secrets_visible is False
    assert "api_key" not in view.rendered_text.lower()
    assert view.production_certified is False


def test_v0429_business_empty_response_view_uses_plain_language_and_next_actions() -> None:
    view = create_v042_business_empty_response_view()
    assert "could not find a final answer" in view.rendered_text
    assert "max_tokens" in view.rendered_text
    assert "LM Studio" in view.rendered_text
    assert view.blames_user is False
    assert view.exposes_raw_trace_by_default is False


def test_v0429_command_guide_includes_start_talk_provider_review_skills_diagnostics_and_safety_sections() -> None:
    guide = create_v042_business_command_guide()
    for heading in ("Start", "Talk", "Provider", "Review", "Skills", "Diagnostics", "Safety"):
        assert heading in guide.rendered_text
    assert "chanta-cli commands" not in " ".join(section.title for section in guide.sections)
    assert guide.includes_core_workflow is True


def test_v0429_command_guide_hides_internal_artifact_names() -> None:
    guide = create_v042_business_command_guide()
    assert guide.hides_internal_artifact_names is True
    assert "V042" not in guide.rendered_text
    assert "dataclass" not in guide.rendered_text


def test_v0429_runtime_identity_answer_policy_positions_chantacore_as_business_agent() -> None:
    policy = create_v042_runtime_identity_answer_policy()
    assert "ChantaCore default-personal" in policy.runtime_identity
    assert "work/business assistant" in policy.business_agent_positioning
    assert "ChantaCore default-personal runtime" in policy.primary_identity_answer
    assert "provider" in policy.provider_identity_treatment


def test_v0429_runtime_identity_answer_policy_disallows_base_model_identity_as_primary() -> None:
    policy = create_v042_runtime_identity_answer_policy()
    assert policy.base_model_identity_primary_allowed is False


def test_v0429_user_facing_error_card_has_no_stack_trace_by_default() -> None:
    card = create_v042_user_facing_error_card()
    assert card.includes_stack_trace_by_default is False
    assert "Traceback" not in card.rendered_text
    assert card.debug_command == "chanta-cli run-report last"


def test_v0429_debug_disclosure_policy_hides_internal_fields_by_default_but_keeps_debug_trace_report_access() -> None:
    policy = create_v042_debug_disclosure_policy()
    assert policy.internal_fields_hidden_by_default is True
    assert policy.internal_fields_available_on_debug is True
    assert policy.trace_available_via_trace_commands is True
    assert policy.report_available_via_report_bundle is True


def test_v0429_operation_readiness_report_contains_required_checks() -> None:
    report = create_v042_operation_readiness_report()
    titles = {check.title for check in report.checks}
    required = {
        "quickstart works",
        "provider connectivity works",
        "configured run handles content or empty response correctly",
        "chat starts cleanly",
        "chat help is grouped",
        "run output is business-friendly",
        "debug details remain available",
        "trace timeline available",
        "report bundle available",
        "feedback note available",
        "unsafe capabilities closed",
    }
    assert required <= titles
    assert report.production_certified is False


def test_v0429_ux_polish_report_tracks_fixed_and_deferred_findings() -> None:
    report = create_v042_ux_polish_report()
    assert report.fixed_count >= 3
    assert report.deferred_count >= 1
    assert report.recommends_v04210 is True


def test_v0429_readiness_report_sets_business_ux_flags_true() -> None:
    report = create_v0429_readiness_report()
    assert report.business_run_output_ready is True
    assert report.business_chat_output_ready is True
    assert report.grouped_help_ready is True
    assert report.command_guide_ready is True
    assert report.runtime_identity_policy_ready is True


def test_v0429_readiness_report_keeps_tools_functions_shell_subagent_agentloop_and_production_false() -> None:
    report = create_v0429_readiness_report()
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_general_agent_loop is False
    assert report.production_certified is False


def test_v0429_cli_commands_outputs_business_command_guide() -> None:
    code, output = _run_cli(["commands"])
    assert code == 0
    assert "ChantaCore Commands" in output
    assert "Start" in output and "Safety" in output
    assert "V042" not in output


def test_v0429_cli_default_run_hides_raw_trace_banner_and_debug_run_exposes_details(tmp_path: Path) -> None:
    home = tmp_path / "home"
    code, output = _run_cli(["run", "--home", str(home), "--provider", "mock", "넌 누구야?"])
    assert code == 0
    assert "Mock provider response" in output
    assert "[v0.41.5 traced" not in output
    assert "trace runtime emitted" not in output
    assert "provider text is untrusted" not in output
    assert "run:" in output and "session:" in output

    code, debug_output = _run_cli(["run", "--home", str(home), "--provider", "mock", "--debug", "넌 누구야?"])
    assert code == 0
    assert "ChantaCore Run Debug" in debug_output
    assert "run_id:" in debug_output
    assert "session_id:" in debug_output
    assert "trace_event_count:" in debug_output
    assert "production_certified: false" in debug_output


def test_v0429_cli_provider_status_is_readable_and_hides_raw_config_path(tmp_path: Path) -> None:
    code, output = _run_cli(["provider", "status", "--home", str(tmp_path / "home")])
    assert code == 0
    assert "Provider" in output
    assert "Status:" in output
    assert "Next:" in output
    assert "config_path" not in output
    assert "api_key" not in output.lower()


def test_v0429_integrated_document_exists_and_has_required_sections() -> None:
    path = Path(INTEGRATED_DOC_PATH)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for section in REQUIRED_V0429_DOC_SECTIONS:
        assert f"## {section}" in text


def test_v0429_integrated_document_contains_user_ux_direction_and_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    assert "clean business/work agent" in text
    assert "developer console" in text
    assert "Copy-Paste Restore Prompt" in text


def test_v0429_no_separate_v0429_restore_business_ux_or_chat_docs_created() -> None:
    forbidden = (
        Path("docs/versions/v0.42/v0.42.9_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.9_business_ux.md"),
        Path("docs/versions/v0.42/v0.42.9_chat_ux.md"),
        Path("docs/versions/v0.42/v0.42.9_help_text.md"),
    )
    assert not any(path.exists() for path in forbidden)


def test_v0429_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/personal_runtime/default_personal_business_ux.py").read_text(encoding="utf-8")
    forbidden = ("subprocess.", "Popen(", "os.system(", "shell=True", "tool_calls")
    assert not any(pattern in source for pattern in forbidden)
