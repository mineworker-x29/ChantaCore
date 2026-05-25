from __future__ import annotations

from pathlib import Path

from chanta_core.agent_surface import AgentAskReplReportService
from chanta_core.agent_surface.ask_repl import AGENT_ASK_REPL_FORBIDDEN_EFFECT_TYPES


SOURCE_FILES = [
    Path("src/chanta_core/agent_surface/ask_repl.py"),
    Path("docs/versions/v0.25/v0.25.7_ask_repl_surface.md"),
]


def _source() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_FILES)


def test_ask_repl_source_has_no_direct_execution_or_loop_markers() -> None:
    source = _source()
    forbidden_exact = [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "exec" + "(",
        "eval" + "(",
        "autonomous_loop_started" + "=True",
        "background_execution_started" + "=True",
        "self_prompt_loop_started" + "=True",
        "direct_provider_invocation" + "=True",
        "direct_file_access_performed" + "=True",
        "direct_repository_search_performed" + "=True",
        "direct_process_inspection_performed" + "=True",
        "direct_subprocess_performed" + "=True",
        "direct_local_command_executed" + "=True",
        "command_rerun_performed" + "=True",
        "automatic_repair_performed" + "=True",
        "memory_candidate_created" + "=True",
        "memory_continuity_implemented" + "=True",
        "memory_promoted" + "=True",
        "persistent_memory_written" + "=True",
        "persona_mutated" + "=True",
        "file_write_performed" + "=True",
        "file_edit_performed" + "=True",
        "file_delete_performed" + "=True",
        "patch_applied" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "external_provider_invoked" + "=True",
        "external_agent_runtime_touched" + "=True",
        "opencode_runtime_dependency_allowed" + "=True",
        "openclaw_runtime_dependency_allowed" + "=True",
        "hermes_runtime_dependency_allowed" + "=True",
        "raw_user_secret_persisted" + "=True",
        "credential_exposed" + "=True",
        "raw_secret_output" + "=True",
        "raw_provider_output_inline" + "=True",
        "workspace_workbench_implemented" + "=True",
        "schumpeter_split_introduced" + "=True",
        "growthkernel_dependency_required" + "=True",
    ]

    for marker in forbidden_exact:
        assert marker not in source


def test_ask_repl_forbidden_effects_are_not_emitted() -> None:
    ocpx = AgentAskReplReportService().build_ocpx_projection()

    for forbidden_effect in AGENT_ASK_REPL_FORBIDDEN_EFFECT_TYPES:
        assert forbidden_effect not in ocpx["effect_types"]
    assert "agent_ask_executed" in ocpx["effect_types"]
    assert "agent_repl_started" in ocpx["effect_types"]
    assert "final_response_emitted" in ocpx["effect_types"]


def test_attempted_forbidden_actions_create_blocking_findings() -> None:
    report = AgentAskReplReportService().build_report(
        "Explain the project structure",
        attempt_flags={
            "autonomous_loop_attempted": True,
            "background_execution_attempted": True,
            "self_prompting_attempted": True,
            "direct_provider_invocation_attempted": True,
            "direct_file_access_attempted": True,
            "direct_subprocess_attempted": True,
            "direct_local_command_execution_attempted": True,
            "command_rerun_attempted": True,
            "memory_promotion_attempted": True,
            "persistent_memory_write_attempted": True,
            "persona_mutation_attempted": True,
            "external_provider_adapter_detected": True,
            "external_agent_adapter_detected": True,
            "opencode_runtime_dependency_detected": True,
            "openclaw_runtime_dependency_detected": True,
            "hermes_runtime_dependency_detected": True,
            "schumpeter_split_detected": True,
            "credential_exposure_detected": True,
            "raw_secret_output_detected": True,
            "raw_provider_output_inline_detected": True,
            "llm_judge_detected": True,
        },
    )
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "blocked"
    assert "autonomous_loop_attempted" in finding_types
    assert "background_execution_attempted" in finding_types
    assert "self_prompting_attempted" in finding_types
    assert "direct_provider_invocation_attempted" in finding_types
    assert "direct_file_access_attempted" in finding_types
    assert "direct_subprocess_attempted" in finding_types
    assert "direct_local_command_execution_attempted" in finding_types
    assert "command_rerun_attempted" in finding_types
    assert "memory_promotion_attempted" in finding_types
    assert "persistent_memory_write_attempted" in finding_types
    assert "persona_mutation_attempted" in finding_types
    assert "external_provider_adapter_detected" in finding_types
    assert "external_agent_adapter_detected" in finding_types
    assert "opencode_runtime_dependency_detected" in finding_types
    assert "openclaw_runtime_dependency_detected" in finding_types
    assert "hermes_runtime_dependency_detected" in finding_types
    assert "schumpeter_split_detected" in finding_types
    assert "credential_exposure_detected" in finding_types
    assert "raw_secret_output_detected" in finding_types
    assert "raw_provider_output_inline_detected" in finding_types
    assert "llm_judge_detected" in finding_types
    assert report.autonomous_loop_started is False
    assert report.background_execution_started is False
    assert report.self_prompt_loop_started is False
    assert report.direct_provider_invocation is False
    assert report.direct_file_access_performed is False
    assert report.direct_subprocess_performed is False
    assert report.direct_local_command_executed is False
    assert report.memory_promoted is False
    assert report.persona_mutated is False
    assert report.raw_provider_output_inline is False


def test_private_path_and_secret_like_text_are_sanitized() -> None:
    module = __import__("chanta_core.agent_surface.ask_repl", fromlist=["_sanitize_text"])
    sanitized = module._sanitize_text(r"See D:\private\secret.txt token=abc123")

    assert "[private-path]" in sanitized
    assert "token=[redacted]" in sanitized
    assert "abc123" not in sanitized
