from __future__ import annotations

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.client import LLMClient
from chanta_core.ocel.factory import short_hash
from chanta_core.prompts.assembly import PromptAssemblyService
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.runtime.loop.process_run_loop import ProcessRunLoop
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
        process_run_loop: ProcessRunLoop | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.prompt_assembly = prompt_assembly or PromptAssemblyService()
        self.trace_service = trace_service or TraceService()
        self.agent_profile = agent_profile or load_default_agent_profile()
        self.skill_registry = skill_registry or SkillRegistry()
        self.process_run_loop = process_run_loop

    def run(
        self,
        user_input: str,
        session_id: str | None = None,
    ) -> AgentRunResult:
        process_instance_id = None
        if session_id:
            process_instance_id = (
                f"process_instance:{short_hash(f'{session_id}:{user_input}:process')}"
            )
        context = ExecutionContext.create(
            agent_id=self.agent_profile.agent_id,
            user_input=user_input,
            session_id=session_id,
            metadata=(
                {"process_instance_id": process_instance_id}
                if process_instance_id
                else None
            ),
        )
        if process_instance_id is None:
            process_instance_id = (
                f"process_instance:{short_hash(f'{context.session_id}:{user_input}:process')}"
            )
            context.metadata["process_instance_id"] = process_instance_id
        events: list[AgentEvent] = []

        loop: ProcessRunLoop | None = None
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
            loop = self.process_run_loop or ProcessRunLoop(
                llm_client=self.llm_client,
                trace_service=self.trace_service,
                skill_registry=self.skill_registry,
                agent_profile=self.agent_profile,
            )
            loop_result = loop.run(
                process_instance_id=process_instance_id,
                session_id=context.session_id,
                agent_id=context.agent_id,
                user_input=context.user_input,
                system_prompt=self.agent_profile.system_prompt,
            )
            events.extend(loop.events)
            response_text = loop_result.response_text
        except Exception as error:
            if loop is not None:
                events.extend(loop.events)
            if not events or events[-1].event_type != "process_instance_failed":
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
            metadata={
                **context.metadata,
                "process_instance_id": process_instance_id,
            },
        )
