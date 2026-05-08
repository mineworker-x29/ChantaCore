from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.cli.main import EMPTY_MODEL_RESPONSE_MESSAGE, format_assistant_output
from chanta_core.llm.types import ChatMessage
from chanta_core.runtime.loop.context import ProcessContextAssembler
from chanta_core.skills.builtin import create_llm_chat_skill
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor


class CapabilityAwareFakeLLMClient:
    class settings:
        provider = "fake_provider"
        model = "fake_model"

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 1024,
    ) -> str:
        system_text = "\n".join(
            message["content"] for message in messages if message["role"] == "system"
        )
        if "Runtime capability contract:" in system_text:
            return (
                "I can use configured local LLM chat and OCEL/session/process "
                "event recording. I cannot directly read files, execute shell "
                "commands, call network resources, connect MCP, load plugins, "
                "or act as an active Soul in this chat path."
            )
        return "missing capability contract"


def test_default_agent_prompt_states_default_chat_limitations() -> None:
    profile = load_default_agent_profile()

    assert "Always provide a non-empty response" in profile.system_prompt
    assert "do not have direct filesystem" in profile.system_prompt
    assert "shell" in profile.system_prompt
    assert "network" in profile.system_prompt
    assert "MCP" in profile.system_prompt
    assert "plugin" in profile.system_prompt
    assert "state that limitation plainly" in profile.system_prompt


def test_cli_formats_empty_model_response_as_diagnostic() -> None:
    assert format_assistant_output("") == EMPTY_MODEL_RESPONSE_MESSAGE
    assert format_assistant_output("   \n") == EMPTY_MODEL_RESPONSE_MESSAGE
    assert format_assistant_output("hello") == "hello"


def test_what_can_you_do_response_uses_capability_contract() -> None:
    executor = SkillExecutor(
        llm_client=CapabilityAwareFakeLLMClient(),
        context_assembler=ProcessContextAssembler(),
    )

    result = executor.execute(
        create_llm_chat_skill(),
        SkillExecutionContext(
            process_instance_id="process_instance:capability-contract",
            session_id="session-capability-contract",
            agent_id="chanta_core_default",
            user_input="what can you do?",
            system_prompt=load_default_agent_profile().system_prompt,
            event_attrs={},
            context_attrs={"iteration": 0},
        ),
    )

    assert result.success is True
    assert "configured local LLM chat" in str(result.output_text)
    assert "OCEL/session/process event recording" in str(result.output_text)
    assert "cannot directly read files" in str(result.output_text)
    assert "execute shell commands" in str(result.output_text)
    assert "connect MCP" in str(result.output_text)
    assert "load plugins" in str(result.output_text)
    assert "active Soul" in str(result.output_text)
