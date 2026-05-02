from __future__ import annotations

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.client import LLMClient
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.runtime.loop.context import ProcessContextAssembler
from chanta_core.runtime.loop.decider import ProcessActivityDecider
from chanta_core.runtime.loop.observation import ProcessObservation
from chanta_core.runtime.loop.policy import ProcessRunPolicy
from chanta_core.runtime.loop.result import ProcessRunResult
from chanta_core.runtime.loop.state import ProcessRunState
from chanta_core.skills.registry import SkillRegistry
from chanta_core.traces.event import AgentEvent
from chanta_core.traces.trace_service import TraceService


class ProcessRunLoop:
    def __init__(
        self,
        *,
        llm_client: LLMClient | None = None,
        trace_service: TraceService | None = None,
        skill_registry: SkillRegistry | None = None,
        context_assembler: ProcessContextAssembler | None = None,
        policy: ProcessRunPolicy | None = None,
        decider: ProcessActivityDecider | None = None,
        agent_profile: AgentProfile | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.trace_service = trace_service or TraceService()
        self.skill_registry = skill_registry or SkillRegistry()
        self.context_assembler = context_assembler or ProcessContextAssembler()
        self.policy = policy or ProcessRunPolicy()
        self.decider = decider or ProcessActivityDecider()
        self.agent_profile = agent_profile or load_default_agent_profile()
        self.events: list[AgentEvent] = []

    def run(
        self,
        *,
        process_instance_id: str,
        session_id: str,
        agent_id: str,
        user_input: str,
        system_prompt: str | None = None,
    ) -> ProcessRunResult:
        context = ExecutionContext.create(
            agent_id=agent_id,
            user_input=user_input,
            session_id=session_id,
            metadata={"process_instance_id": process_instance_id},
        )
        state = ProcessRunState(
            process_instance_id=process_instance_id,
            session_id=session_id,
            agent_id=agent_id,
            status="running",
            iteration=0,
            max_iterations=self.policy.max_iterations,
            current_activity=None,
            selected_skill_id=None,
        )
        observations: list[ProcessObservation] = []
        self.events = []

        try:
            self._append_event(
                self.trace_service.record_process_run_loop_started(
                    context,
                    profile=self.agent_profile,
                    state_attrs=state.state_attrs,
                    max_iterations=state.max_iterations,
                )
            )

            while self.policy.should_continue(state):
                next_activity = self.decider.decide_next_activity(state)
                state.current_activity = next_activity
                self._append_event(
                    self.trace_service.record_next_activity_decided(
                        context,
                        next_activity=next_activity,
                        iteration=state.iteration,
                        profile=self.agent_profile,
                    )
                )

                if next_activity != "execute_skill":
                    break

                skill = self.skill_registry.get_builtin_llm_chat()
                state.selected_skill_id = skill.skill_id
                self._append_event(
                    self.trace_service.record_skill_selected(
                        context,
                        skill,
                        profile=self.agent_profile,
                    )
                )
                self._append_event(
                    self.trace_service.record_skill_executed(
                        context,
                        skill,
                        profile=self.agent_profile,
                    )
                )

                # TODO: add permission gate before external tool or shell dispatch.
                messages = self.context_assembler.assemble_for_llm_chat(
                    user_input=user_input,
                    system_prompt=system_prompt,
                )
                # TODO: add context compaction before long-running model calls.
                self._append_event(
                    self.trace_service.record_context_assembled(
                        context,
                        messages,
                        profile=self.agent_profile,
                        iteration=state.iteration,
                    )
                )
                self._append_event(
                    self.trace_service.record_llm_call_started(
                        context,
                        messages,
                        provider_name=self.llm_client.settings.provider,
                        model_id=self.llm_client.settings.model,
                        profile=self.agent_profile,
                    )
                )
                response_text = self.llm_client.chat_messages(
                    messages=messages,
                    temperature=self.agent_profile.default_temperature,
                    max_tokens=self.agent_profile.max_tokens,
                )
                self._append_event(
                    self.trace_service.record_llm_response_received(
                        context,
                        response_text,
                        profile=self.agent_profile,
                    )
                )

                observation = ProcessObservation(
                    activity=next_activity,
                    success=True,
                    output_text=response_text,
                    output_attrs={
                        "skill_id": skill.skill_id,
                        "iteration": state.iteration,
                    },
                )
                observations.append(observation)
                state.observations.append(observation.to_dict())
                self._append_event(
                    self.trace_service.record_result_observed(
                        context,
                        observation=observation.to_dict(),
                        profile=self.agent_profile,
                        iteration=state.iteration,
                    )
                )
                state.iteration += 1

                # TODO: add tool dispatch and subagent delegation in later versions.
                if self.policy.should_stop_after_observation(state, observation):
                    break

            response_text = observations[-1].output_text if observations else ""
            self._append_event(
                self.trace_service.record_outcome_recorded(
                    context,
                    profile=self.agent_profile,
                    response_text=response_text,
                )
            )
            self._append_event(
                self.trace_service.record_process_instance_completed(
                    context,
                    profile=self.agent_profile,
                    response_text=response_text,
                )
            )
            state.status = "completed"
            return ProcessRunResult(
                process_instance_id=process_instance_id,
                session_id=session_id,
                agent_id=agent_id,
                status="completed",
                response_text=response_text or "",
                observations=observations,
                result_attrs={
                    "iteration_count": state.iteration,
                    "selected_skill_id": state.selected_skill_id,
                },
            )
        except Exception as error:
            state.status = "failed"
            state.last_error = str(error)
            self._append_event(
                self.trace_service.record_process_instance_failed(
                    context,
                    error,
                    profile=self.agent_profile,
                )
            )
            if self.policy.fail_on_exception:
                raise
            return ProcessRunResult(
                process_instance_id=process_instance_id,
                session_id=session_id,
                agent_id=agent_id,
                status="failed",
                response_text="",
                observations=observations,
                result_attrs={
                    "iteration_count": state.iteration,
                    "selected_skill_id": state.selected_skill_id,
                    "error": str(error),
                },
            )

    def _append_event(self, event: AgentEvent) -> None:
        self.events.append(event)
