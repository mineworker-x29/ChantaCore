from __future__ import annotations

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.client import LLMClient
from chanta_core.prompts.assembly import PromptAssemblyService
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.runtime.run_result import AgentRunResult
from chanta_core.skills.registry import SkillRegistry
from chanta_core.traces.event import AgentEvent
from chanta_core.traces.trace_service import TraceService


class AgentRuntime:
    def __init__(
        self,
        *,
        llm_client: LLMClient | None = None,
        prompt_assembly: PromptAssemblyService | None = None,
        trace_service: TraceService | None = None,
        agent_profile: AgentProfile | None = None,
        skill_registry: SkillRegistry | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.prompt_assembly = prompt_assembly or PromptAssemblyService()
        self.trace_service = trace_service or TraceService()
        self.agent_profile = agent_profile or load_default_agent_profile()
        self.skill_registry = skill_registry or SkillRegistry()

    def run(
        self,
        user_input: str,
        session_id: str | None = None,
    ) -> AgentRunResult:
        context = ExecutionContext.create(
            agent_id=self.agent_profile.agent_id,
            user_input=user_input,
            session_id=session_id,
        )
        events: list[AgentEvent] = []

        try:
            events.append(
                self.trace_service.record_user_request_received(
                    context,
                    profile=self.agent_profile,
                )
            )
            events.append(
                self.trace_service.record_run_started(
                    context,
                    profile=self.agent_profile,
                )
            )
            messages = self.prompt_assembly.assemble(context, self.agent_profile)
            events.append(
                self.trace_service.record_prompt_assembled(
                    context,
                    messages,
                    profile=self.agent_profile,
                )
            )
            llm_skill = self.skill_registry.get_builtin_llm_chat()
            events.append(
                self.trace_service.record_skill_selected(
                    context,
                    llm_skill,
                    profile=self.agent_profile,
                )
            )
            events.append(
                self.trace_service.record_skill_executed(
                    context,
                    llm_skill,
                    profile=self.agent_profile,
                )
            )
            llm_call_event = self.trace_service.record_llm_call_started(
                context,
                messages,
                provider_name=self.llm_client.settings.provider,
                model_id=self.llm_client.settings.model,
                profile=self.agent_profile,
            )
            events.append(llm_call_event)
            response_text = self.llm_client.chat_messages(
                messages=messages,
                temperature=self.agent_profile.default_temperature,
                max_tokens=self.agent_profile.max_tokens,
            )
            events.append(
                self.trace_service.record_llm_response_received(
                    context,
                    response_text,
                    profile=self.agent_profile,
                    llm_call_id=llm_call_event.payload.get("llm_call_id"),
                )
            )
            events.append(
                self.trace_service.record_outcome_recorded(
                    context,
                    profile=self.agent_profile,
                    response_text=response_text,
                )
            )
            events.append(
                self.trace_service.record_process_instance_completed(
                    context,
                    profile=self.agent_profile,
                    response_text=response_text,
                )
            )
        except Exception as error:
            events.append(
                self.trace_service.record_process_instance_failed(
                    context,
                    error,
                    profile=self.agent_profile,
                )
            )
            raise

        return AgentRunResult(
            session_id=context.session_id,
            agent_id=context.agent_id,
            user_input=context.user_input,
            response_text=response_text,
            events=events,
            metadata=context.metadata,
        )
