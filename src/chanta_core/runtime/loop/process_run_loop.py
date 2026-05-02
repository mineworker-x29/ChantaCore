from __future__ import annotations

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.client import LLMClient
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.runtime.loop.context import ProcessContextAssembler
from chanta_core.runtime.loop.decider import ProcessActivityDecider
from chanta_core.runtime.loop.evaluation import ProcessRunEvaluator
from chanta_core.runtime.loop.observation import ProcessObservation
from chanta_core.runtime.loop.policy import ProcessRunPolicy
from chanta_core.runtime.loop.result import ProcessRunResult
from chanta_core.runtime.loop.state import ProcessRunState
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
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
        evaluator: ProcessRunEvaluator | None = None,
        agent_profile: AgentProfile | None = None,
        skill_executor: SkillExecutor | None = None,
    ) -> None:
        self.llm_client = llm_client or LLMClient()
        self.trace_service = trace_service or TraceService()
        self.skill_registry = skill_registry or SkillRegistry()
        self.context_assembler = context_assembler or ProcessContextAssembler()
        self.policy = policy or ProcessRunPolicy()
        self.decider = decider or ProcessActivityDecider()
        self.evaluator = evaluator or ProcessRunEvaluator()
        self.agent_profile = agent_profile or load_default_agent_profile()
        self.skill_executor = skill_executor or SkillExecutor(
            llm_client=self.llm_client,
            context_assembler=self.context_assembler,
            trace_service=self.trace_service,
        )
        self.events: list[AgentEvent] = []

    def run(
        self,
        *,
        process_instance_id: str,
        session_id: str,
        agent_id: str,
        user_input: str,
        system_prompt: str | None = None,
        skill_id: str | None = None,
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

                skill = (
                    self.skill_registry.require(skill_id)
                    if skill_id
                    else self.skill_registry.get_builtin_llm_chat()
                )
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
                # TODO: add context compaction before long-running model calls.
                skill_context = SkillExecutionContext(
                    process_instance_id=process_instance_id,
                    session_id=session_id,
                    agent_id=agent_id,
                    user_input=user_input,
                    system_prompt=system_prompt,
                    event_attrs={
                        "next_activity": next_activity,
                        "iteration": state.iteration,
                    },
                    context_attrs={
                        "iteration": state.iteration,
                        "temperature": self.agent_profile.default_temperature,
                        "max_tokens": self.agent_profile.max_tokens,
                        "agent_profile": self.agent_profile,
                    },
                )
                skill_result = self.skill_executor.execute(skill, skill_context)
                self.events.extend(self.skill_executor.events)

                observation = ProcessObservation(
                    activity=next_activity,
                    success=skill_result.success,
                    output_text=skill_result.output_text,
                    output_attrs={
                        **skill_result.output_attrs,
                        "skill_id": skill_result.skill_id,
                        "skill_name": skill_result.skill_name,
                        "iteration": state.iteration,
                    },
                    error=skill_result.error,
                )
                observations.append(observation)
                state.observations.append(observation.to_dict())
                if not skill_result.success:
                    state.status = "failed"
                    state.last_error = skill_result.error
                    failure_stage = str(
                        skill_result.output_attrs.get("failure_stage") or "skill_dispatch"
                    )
                    exception_type = str(
                        skill_result.output_attrs.get("exception_type") or "SkillExecutionError"
                    )
                    state.state_attrs["exception_type"] = exception_type
                    state.state_attrs["failure_stage"] = failure_stage
                    self._append_event(
                        self.trace_service.record_result_observed(
                            context,
                            observation=observation.to_dict(),
                            profile=self.agent_profile,
                            iteration=state.iteration,
                        )
                    )
                    self._append_event(
                        self.trace_service.record_process_instance_failed(
                            context,
                            RuntimeError(skill_result.error or "Skill execution failed"),
                            profile=self.agent_profile,
                            failure_stage=failure_stage,
                        )
                    )
                    state.state_attrs["_failure_recorded"] = True
                    if self.policy.raise_on_failure:
                        raise RuntimeError(skill_result.error or "Skill execution failed")
                    return ProcessRunResult(
                        process_instance_id=process_instance_id,
                        session_id=session_id,
                        agent_id=agent_id,
                        status="failed",
                        response_text="",
                        observations=observations,
                        result_attrs={
                            **self.evaluator.evaluate(state),
                            "iteration_count": state.iteration,
                            "selected_skill_id": state.selected_skill_id,
                            "error": skill_result.error,
                            "exception_type": exception_type,
                            "failure_stage": failure_stage,
                        },
                    )

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
                    **self.evaluator.evaluate(state),
                    "iteration_count": state.iteration,
                    "selected_skill_id": state.selected_skill_id,
                },
            )
        except Exception as error:
            state.status = "failed"
            state.last_error = str(error)
            failure_stage = state.current_activity or "process_run_loop"
            if state.current_activity == "execute_skill":
                failure_stage = "call_llm"
            state.state_attrs["exception_type"] = type(error).__name__
            state.state_attrs["failure_stage"] = failure_stage
            if not state.state_attrs.get("_failure_recorded"):
                observation = ProcessObservation(
                    activity=state.current_activity or failure_stage,
                    success=False,
                    output_text=None,
                    output_attrs={
                        "failure_stage": failure_stage,
                        "exception_type": type(error).__name__,
                        "iteration": state.iteration,
                        "selected_skill_id": state.selected_skill_id,
                    },
                    error=str(error),
                )
                observations.append(observation)
                state.observations.append(observation.to_dict())
                self._append_event(
                    self.trace_service.record_process_instance_failed(
                        context,
                        error,
                        profile=self.agent_profile,
                        failure_stage=failure_stage,
                    )
                )
            if self.policy.raise_on_failure:
                raise
            return ProcessRunResult(
                process_instance_id=process_instance_id,
                session_id=session_id,
                agent_id=agent_id,
                status="failed",
                response_text="",
                observations=observations,
                result_attrs={
                    **self.evaluator.evaluate(state),
                    "iteration_count": state.iteration,
                    "selected_skill_id": state.selected_skill_id,
                    "error": str(error),
                    "exception_type": type(error).__name__,
                    "failure_stage": failure_stage,
                },
            )

    def _append_event(self, event: AgentEvent) -> None:
        self.events.append(event)
