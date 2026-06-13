from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_rehearsal import (
    MINIMUM_EVENTS,
    MINIMUM_READ_ONLY_SKILLS,
    MINIMUM_USER_FACING_COMMANDS,
    REQUIRED_GAP_NAMES,
    V041_SEQUENCE,
    SandboxRehearsalResult,
    assess_default_personal_acceleration,
    create_default_personal_gap_register,
    create_default_personal_required_runtime_surface,
    create_sandbox_rehearsal_apply_plan,
    create_sandbox_rehearsal_input,
    create_sandbox_rehearsal_readiness_report,
    create_sandbox_rehearsal_retest_plan,
    create_sandbox_rehearsal_safety_report,
    create_standalone_agent_runtime_status,
    create_v041_default_personal_handoff_draft,
    run_sandbox_rehearsal,
    sandbox_rehearsal_readiness_preserves_no_unsafe_runtime,
    sandbox_rehearsal_result_preserves_runtime_boundary,
    standalone_agent_runtime_status_all_closed,
)


def test_v0401_sandbox_rehearsal_input_blocks_live_workspace_request() -> None:
    rehearsal_input = create_sandbox_rehearsal_input()

    assert rehearsal_input.live_workspace_apply_requested is False
    with pytest.raises(ValueError):
        create_sandbox_rehearsal_input(live_workspace_apply_requested=True)


def test_v0401_apply_plan_reuses_v0393_sandbox_apply_primitive() -> None:
    rehearsal_input = create_sandbox_rehearsal_input()
    plan = create_sandbox_rehearsal_apply_plan(rehearsal_input)

    assert plan.uses_v0393_sandbox_apply_primitive is True
    assert plan.exact_text_replacement_required is True
    assert plan.sandbox_root_ref == rehearsal_input.sandbox_root_ref
    assert plan.target_relative_path == rehearsal_input.target_relative_path


def test_v0401_apply_plan_blocks_git_apply_and_apply_patch() -> None:
    rehearsal_input = create_sandbox_rehearsal_input()
    plan = create_sandbox_rehearsal_apply_plan(rehearsal_input)

    assert plan.live_workspace_allowed is False
    assert plan.git_apply_allowed is False
    assert plan.apply_patch_allowed is False
    with pytest.raises(ValueError):
        create_sandbox_rehearsal_apply_plan(rehearsal_input, git_apply_allowed=True)
    with pytest.raises(ValueError):
        create_sandbox_rehearsal_apply_plan(rehearsal_input, apply_patch_allowed=True)


def test_v0401_retest_plan_reuses_v0394_controlled_retest_primitive() -> None:
    rehearsal_input = create_sandbox_rehearsal_input()
    plan = create_sandbox_rehearsal_retest_plan(rehearsal_input)

    assert plan.uses_v0394_controlled_retest_primitive is True
    assert plan.supplied_runner_required is True
    assert plan.bounded_argv_required is True
    assert plan.timeout_required is True
    assert plan.output_capture_bounded is True


def test_v0401_retest_plan_blocks_shell_network_and_dependency_install() -> None:
    rehearsal_input = create_sandbox_rehearsal_input()
    plan = create_sandbox_rehearsal_retest_plan(rehearsal_input)

    assert plan.shell_allowed is False
    assert plan.network_allowed is False
    assert plan.dependency_install_allowed is False
    with pytest.raises(ValueError):
        create_sandbox_rehearsal_retest_plan(rehearsal_input, shell_allowed=True)
    with pytest.raises(ValueError):
        create_sandbox_rehearsal_retest_plan(rehearsal_input, network_allowed=True)
    with pytest.raises(ValueError):
        create_sandbox_rehearsal_retest_plan(rehearsal_input, dependency_install_allowed=True)


def test_v0401_sandbox_rehearsal_runs_in_tmp_sandbox_only(tmp_path: Path) -> None:
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    target = sandbox_root / "example.txt"
    target.write_text("alpha before omega", encoding="utf-8")
    calls: list[tuple[list[str], str, int, dict[str, str]]] = []

    def fake_runner(argv: list[str], cwd_ref: str, timeout_seconds: int, env_overrides: dict[str, str]) -> dict[str, object]:
        calls.append((argv, cwd_ref, timeout_seconds, env_overrides))
        return {"stdout": "1 passed", "stderr": "", "exit_code": 0, "timed_out": False, "duration_ms": 3}

    rehearsal_input = create_sandbox_rehearsal_input(
        sandbox_root_ref=str(sandbox_root),
        target_relative_path="example.txt",
        original_text="before",
        replacement_text="after",
    )
    result, audit, safety = run_sandbox_rehearsal(rehearsal_input, runner=fake_runner)

    assert isinstance(result, SandboxRehearsalResult)
    assert target.read_text(encoding="utf-8") == "alpha after omega"
    assert result.apply_attempted is True
    assert result.apply_succeeded is True
    assert result.retest_attempted is True
    assert result.retest_succeeded is True
    assert result.sandbox_only is True
    assert audit.checked_sandbox_containment is True
    assert safety.safe_for_v0401 is True
    assert len(calls) == 1


def test_v0401_sandbox_rehearsal_does_not_mutate_live_workspace(tmp_path: Path) -> None:
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    (sandbox_root / "example.txt").write_text("before", encoding="utf-8")
    live_file = tmp_path / "live_workspace.txt"
    live_file.write_text("before", encoding="utf-8")

    rehearsal_input = create_sandbox_rehearsal_input(
        sandbox_root_ref=str(sandbox_root),
        target_relative_path="example.txt",
        original_text="before",
        replacement_text="after",
    )
    result, _, _ = run_sandbox_rehearsal(rehearsal_input)

    assert result.live_workspace_mutated is False
    assert live_file.read_text(encoding="utf-8") == "before"


def test_v0401_sandbox_rehearsal_result_keeps_runtime_authority_false(tmp_path: Path) -> None:
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    (sandbox_root / "example.txt").write_text("before", encoding="utf-8")
    result, _, _ = run_sandbox_rehearsal(
        create_sandbox_rehearsal_input(sandbox_root_ref=str(sandbox_root))
    )

    assert sandbox_rehearsal_result_preserves_runtime_boundary(result)
    assert result.runtime_authority_granted is False
    assert result.model_invoked is False
    assert result.prompt_submitted is False
    assert result.subagent_invoked is False
    assert result.external_agent_invoked is False


def test_v0401_safety_report_blocks_live_apply_autonomous_loop_model_and_subagent() -> None:
    report = create_sandbox_rehearsal_safety_report()

    assert report.safe_for_v0401 is True
    assert report.safe_for_live_apply is False
    assert report.safe_for_autonomous_loop is False
    assert report.safe_for_model_invocation is False
    assert report.safe_for_subagent_invocation is False
    assert report.requires_human_checkpoint_before_next_iteration is True


def test_v0401_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_sandbox_rehearsal_readiness_report()

    assert report.sandbox_rehearsal_runner_defined is True
    assert report.v0393_sandbox_apply_primitive_reused is True
    assert report.v0394_controlled_retest_primitive_reused is True
    assert report.temp_sandbox_fixture_ready is True
    assert sandbox_rehearsal_readiness_preserves_no_unsafe_runtime(report)
    with pytest.raises(ValueError):
        create_sandbox_rehearsal_readiness_report(ready_for_live_workspace_apply=True)
    with pytest.raises(ValueError):
        create_sandbox_rehearsal_readiness_report(production_certified=True)


def test_v0401_standalone_agent_runtime_status_all_closed() -> None:
    status = create_standalone_agent_runtime_status()

    assert standalone_agent_runtime_status_all_closed(status)
    assert status.standalone_default_personal_runtime_opened is False
    assert status.first_smoke_run_target_version == "v0.41.6-conservative"
    with pytest.raises(ValueError):
        create_standalone_agent_runtime_status(agent_loop_opened=True)


def test_v0401_gap_register_lists_required_default_personal_components() -> None:
    register = create_default_personal_gap_register()
    gap_names = {gap.gap_name for gap in register.gaps}

    assert set(REQUIRED_GAP_NAMES).issubset(gap_names)
    assert register.standalone_runtime_started is False
    assert register.conservative_first_smoke_target == "v0.41.6"


def test_v0401_required_runtime_surface_lists_minimum_commands_skills_and_events() -> None:
    surface = create_default_personal_required_runtime_surface()

    assert set(MINIMUM_USER_FACING_COMMANDS).issubset(surface.minimum_user_facing_commands)
    assert set(MINIMUM_READ_ONLY_SKILLS).issubset(surface.minimum_read_only_skills)
    assert set(MINIMUM_EVENTS).issubset(surface.minimum_events)


def test_v0401_acceleration_assessment_does_not_start_standalone_runtime() -> None:
    assessment = assess_default_personal_acceleration()

    assert assessment.standalone_runtime_started is False
    assert assessment.conservative_target == "v0.41.6"
    assert assessment.earliest_possible_target is None
    assert "ChatService" in assessment.blocking_gaps
    assert "v0.41.6" in assessment.recommendation


def test_v0401_v041_handoff_draft_contains_default_personal_sequence() -> None:
    draft = create_v041_default_personal_handoff_draft()

    assert draft.target_track == "Default Personal Standalone Runtime"
    assert draft.recommended_start_version == "v0.41.0"
    assert draft.first_smoke_run_conservative_target == "v0.41.6"
    assert tuple(V041_SEQUENCE) == draft.recommended_v041_sequence


def test_v0401_no_forbidden_runtime_call_patterns() -> None:
    implementation = Path("src/chanta_core/agent_runtime/repair_mission_loop_rehearsal.py")
    source = implementation.read_text(encoding="utf-8")
    lower_source = source.lower()
    actual_runtime_patterns = [
        "import subprocess",
        "subprocess.",
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
        "codex",
        "claude",
        "apply_patch(",
        "git apply",
        "git worktree",
    ]

    for pattern in actual_runtime_patterns:
        assert pattern not in lower_source
    assert re.search(r"(?<!no_)shell\s*=\s*True", source) is None
