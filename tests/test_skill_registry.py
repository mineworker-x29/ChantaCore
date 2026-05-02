import pytest

from chanta_core.skills.builtin import create_llm_chat_skill
from chanta_core.skills.errors import SkillRegistryError
from chanta_core.skills.registry import SkillRegistry
from chanta_core.skills.skill import Skill


def test_skill_registry_registers_builtin_llm_chat() -> None:
    registry = SkillRegistry()

    by_id = registry.get("skill:llm_chat")
    by_name = registry.get("llm_chat")

    assert by_id is not None
    assert by_name is not None
    assert by_id == by_name
    assert registry.require("skill:llm_chat").skill_name == "llm_chat"
    assert "llm_chat" in [skill.skill_name for skill in registry.list_skills()]
    assert registry.get("skill:echo") is not None
    assert registry.get("echo") is not None
    assert registry.get("skill:summarize_text") is not None
    assert registry.get("skill:inspect_ocel_recent") is not None
    assert registry.get("skill:summarize_process_trace") is not None


def test_duplicate_identical_skill_registration_is_idempotent() -> None:
    registry = SkillRegistry(include_builtins=False)
    skill = create_llm_chat_skill()

    registry.register(skill)
    registry.register(skill)

    assert registry.list_skills() == [skill]


def test_duplicate_skill_id_with_different_definition_raises() -> None:
    registry = SkillRegistry(include_builtins=False)
    registry.register(create_llm_chat_skill())

    with pytest.raises(SkillRegistryError):
        registry.register(
            Skill(
                skill_id="skill:llm_chat",
                skill_name="llm_chat_alt",
                description="Different definition.",
                execution_type="llm",
                input_schema={},
                output_schema={},
                tags=["llm"],
                skill_attrs={},
            )
        )


def test_duplicate_skill_name_with_different_id_raises() -> None:
    registry = SkillRegistry(include_builtins=False)
    registry.register(create_llm_chat_skill())

    with pytest.raises(SkillRegistryError):
        registry.register(
            Skill(
                skill_id="skill:another_llm_chat",
                skill_name="llm_chat",
                description="Name collision.",
                execution_type="llm",
                input_schema={},
                output_schema={},
                tags=["llm"],
                skill_attrs={},
            )
        )


def test_list_skills_is_sorted_by_skill_id() -> None:
    registry = SkillRegistry(include_builtins=False)
    registry.register(
        Skill(
            skill_id="skill:z",
            skill_name="z",
            description="Z.",
            execution_type="test",
            input_schema={},
            output_schema={},
            tags=[],
            skill_attrs={},
        )
    )
    registry.register(
        Skill(
            skill_id="skill:a",
            skill_name="a",
            description="A.",
            execution_type="test",
            input_schema={},
            output_schema={},
            tags=[],
            skill_attrs={},
        )
    )

    assert [skill.skill_id for skill in registry.list_skills()] == ["skill:a", "skill:z"]
