from pathlib import Path

from chanta_core.skills.onboarding import InternalSkillOnboardingService


def test_internal_skill_onboarding_does_not_execute_or_mutate_runtime() -> None:
    service = InternalSkillOnboardingService()
    bundle = service.create_read_only_skill_contract_bundle(skill_id="skill:execution_audit")

    result = service.validate_onboarding(**bundle)

    assert result.result_attrs["skills_executed"] is False
    assert result.result_attrs["runtime_registered"] is False
    assert result.result_attrs["permission_grants_created"] is False
    assert result.result_attrs["tool_dispatcher_mutated"] is False
    assert result.result_attrs["skill_executor_mutated"] is False
    assert result.result_attrs["llm_called"] is False
    assert result.result_attrs["shell_execution_used"] is False
    assert result.result_attrs["network_access_used"] is False
    assert result.result_attrs["mcp_connection_used"] is False
    assert result.result_attrs["plugin_loaded"] is False


def test_internal_skill_onboarding_source_avoids_execution_surfaces() -> None:
    text = Path("src/chanta_core/skills/onboarding.py").read_text(encoding="utf-8")

    forbidden = [
        "dis" + "patch(",
        "invoke_explicit_" + "skill(",
        "gate_explicit_" + "invocation(",
        "register_runtime_" + "skill",
        "mutate_tool_" + "dispatcher",
        "mutate_skill_" + "executor",
        "apply_" + "grant",
        "complete_" + "text",
        "complete_" + "json",
        "sub" + "process",
        "os." + "system",
        "requ" + "ests",
        "ht" + "tpx",
        "sock" + "et",
        "connect_" + "mcp",
        "load_" + "plugin",
        "write_" + "text",
        "op" + "en(",
        ".js" + "onl",
    ]
    for token in forbidden:
        assert token not in text


def test_internal_skill_onboarding_public_files_do_not_contain_private_tokens() -> None:
    roots = [Path("src/chanta_core"), Path("tests"), Path("docs")]
    forbidden = [
        "Ve" + "ra",
        "Mig" + "eon",
        "ChantaResearchGroup" + "_Members",
        "D:\\" + "ChantaResearchGroup",
    ]
    for root in roots:
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix in {".pyc", ".sqlite"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for token in forbidden:
                assert token not in text
