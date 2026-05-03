from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
from chanta_core.skills.registry import SkillRegistry


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake"
    model: str = "fake"


class FakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(self, messages: list[ChatMessage], **_) -> str:
        return "unused"


def test_propose_file_edit_skill(tmp_path) -> None:
    (tmp_path / "app.py").write_text("old\n", encoding="utf-8")
    context = SkillExecutionContext(
        process_instance_id="process_instance:edit-skill",
        session_id="session-edit-skill",
        agent_id="chanta_core_default",
        user_input="propose edit",
        system_prompt=None,
        context_attrs={
            "workspace_root": str(tmp_path),
            "edit_proposal_store_path": str(tmp_path / "proposals.jsonl"),
            "target_path": "app.py",
            "proposed_text": "new\n",
            "title": "Replace",
            "rationale": "Skill proposal",
        },
    )

    result = SkillExecutor(llm_client=FakeLLMClient()).execute(
        SkillRegistry().require("skill:propose_file_edit"),
        context,
    )

    assert result.success is True
    assert result.output_attrs["proposal_id"].startswith("edit_proposal:")
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "old\n"
