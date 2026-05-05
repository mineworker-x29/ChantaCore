from __future__ import annotations

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.client import LLMClient
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.context import PIGContext
from chanta_core.pig.feedback import PIGFeedbackService
from chanta_core.pig.guidance import PIGGuidance, PIGGuidanceService
from chanta_core.runtime.decision.context import DecisionContext
from chanta_core.runtime.decision.decision import ProcessDecision
from chanta_core.runtime.decision.service import DecisionService
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
        pig_feedback_service: PIGFeedbackService | None = None,
        pig_guidance_service: PIGGuidanceService | None = None,
        decision_service: DecisionService | None = None,
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
        self.pig_feedback_service = pig_feedback_service
        self.pig_guidance_service = pig_guidance_service
        self.decision_service = decision_service
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

                pig_guidance = self._build_pig_guidance_if_enabled(
                    state=state,
                    process_instance_id=process_instance_id,
                    session_id=session_id,
                )
                decision = self._decide_skill(
                    process_instance_id=process_instance_id,
                    session_id=session_id,
                    agent_id=agent_id,
                    user_input=user_input,
                    explicit_skill_id=skill_id,
                    pig_guidance=pig_guidance,
                )
                skill = self.skill_registry.require(decision.selected_skill_id)
                state.selected_skill_id = skill.skill_id
                self._record_decision_attrs(state, decision)
                self._append_event(
                    self.trace_service.record_skill_decision(
                        context,
                        skill,
                        decision=decision,
                        profile=self.agent_profile,
                    )
                )
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
                pig_context = self._build_pig_context_if_enabled(
                    state=state,
                    process_instance_id=process_instance_id,
                    session_id=session_id,
                )
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
                        "pig_context_included": pig_context is not None,
                        "context_budget": (
                            self.policy.context_budget
                            if self.policy.use_context_budget
                            else None
                        ),
                    },
                    pig_context=pig_context,
                )
                skill_result = self.skill_executor.execute(skill, skill_context)
                self.events.extend(self.skill_executor.events)
                self._record_context_compaction_attrs(state)

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
                            **self._decision_result_attrs(state),
                            **self._pig_result_attrs(state),
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
                    **self._decision_result_attrs(state),
                    **self._pig_result_attrs(state),
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
                    **self._decision_result_attrs(state),
                    **self._pig_result_attrs(state),
                    "error": str(error),
                    "exception_type": type(error).__name__,
                    "failure_stage": failure_stage,
                },
            )

    def _append_event(self, event: AgentEvent) -> None:
        self.events.append(event)

    def _record_context_compaction_attrs(self, state: ProcessRunState) -> None:
        result = getattr(self.context_assembler, "last_compaction_result", None)
        if result is None:
            return
        state.state_attrs["context_compaction"] = {
            "total_chars_after": result.total_chars,
            "total_estimated_tokens_after": result.total_estimated_tokens,
            "truncated_block_count": len(result.truncated_block_ids),
            "dropped_block_count": len(result.dropped_block_ids),
            "warnings": result.warnings,
            "layer_count": len(result.layer_results),
        }

    def _decide_skill(
        self,
        *,
        process_instance_id: str,
        session_id: str,
        agent_id: str,
        user_input: str,
        explicit_skill_id: str | None,
        pig_guidance: list[PIGGuidance],
    ) -> ProcessDecision:
        if explicit_skill_id:
            self.skill_registry.require(explicit_skill_id)
        available_skill_ids = [skill.skill_id for skill in self.skill_registry.list_skills()]
        if not self.policy.use_decision_service:
            selected_skill_id = explicit_skill_id or "skill:llm_chat"
            return ProcessDecision(
                selected_skill_id=selected_skill_id,
                decision_mode="explicit" if explicit_skill_id else "fallback",
                base_scores={skill_id: 0.0 for skill_id in available_skill_ids},
                final_scores={skill_id: 0.0 for skill_id in available_skill_ids},
                applied_guidance_ids=[],
                rationale=(
                    "Explicit skill_id was provided."
                    if explicit_skill_id
                    else "Decision service disabled; using safe LLM chat fallback."
                ),
                evidence_refs=[],
                decision_attrs={"advisory": True, "hard_policy": False},
            )
        service = self.decision_service or DecisionService(
            skill_registry=self.skill_registry,
        )
        return service.decide_skill(
            DecisionContext(
                process_instance_id=process_instance_id,
                session_id=session_id,
                agent_id=agent_id,
                user_input=user_input,
                available_skill_ids=available_skill_ids,
                explicit_skill_id=explicit_skill_id,
                pig_guidance=pig_guidance,
                context_attrs={"policy_use_pig_guidance": self.policy.use_pig_guidance},
            )
        )

    def _build_pig_guidance_if_enabled(
        self,
        *,
        state: ProcessRunState,
        process_instance_id: str,
        session_id: str,
    ) -> list[PIGGuidance]:
        if not self.policy.use_pig_guidance:
            return []
        try:
            service = self.pig_guidance_service or PIGGuidanceService(
                feedback_service=self.pig_feedback_service
                or PIGFeedbackService(
                    ocpx_loader=OCPXLoader(
                        store=getattr(self.trace_service, "ocel_store", None)
                    )
                )
            )
            if self.policy.guidance_scope == "process_instance":
                guidance = service.build_process_instance_guidance(process_instance_id)
            elif self.policy.guidance_scope == "session":
                context = service.feedback_service.build_session_context(session_id)
                guidance = service.build_from_context(context)
            else:
                guidance = service.build_recent_guidance()
            state.state_attrs["pig_guidance_count"] = len(guidance)
            return guidance
        except Exception as error:
            state.state_attrs["pig_guidance_warning"] = str(error)
            return []

    @staticmethod
    def _record_decision_attrs(
        state: ProcessRunState,
        decision: ProcessDecision,
    ) -> None:
        state.state_attrs["decision_mode"] = decision.decision_mode
        state.state_attrs["applied_guidance_ids"] = decision.applied_guidance_ids
        state.state_attrs["decision_final_scores"] = decision.final_scores
        state.state_attrs["decision_rationale"] = decision.rationale
        state.state_attrs["decision_attrs"] = decision.decision_attrs

    def _build_pig_context_if_enabled(
        self,
        *,
        state: ProcessRunState,
        process_instance_id: str,
        session_id: str,
    ) -> PIGContext | None:
        if not self.policy.include_pig_context:
            return None
        try:
            service = self.pig_feedback_service or PIGFeedbackService(
                ocpx_loader=OCPXLoader(store=getattr(self.trace_service, "ocel_store", None))
            )
            if self.policy.pig_context_scope == "process_instance":
                pig_context = service.build_process_instance_context(process_instance_id)
            elif self.policy.pig_context_scope == "session":
                pig_context = service.build_session_context(session_id)
            else:
                pig_context = service.build_recent_context()
            state.state_attrs["pig_context_included"] = True
            state.state_attrs["pig_context_scope"] = pig_context.scope
            return pig_context
        except Exception as error:
            state.state_attrs["pig_context_included"] = False
            state.state_attrs["pig_context_warning"] = str(error)
            return None

    @staticmethod
    def _pig_result_attrs(state: ProcessRunState) -> dict[str, object]:
        result: dict[str, object] = {}
        if "pig_context_included" in state.state_attrs:
            result["pig_context_included"] = bool(
                state.state_attrs.get("pig_context_included")
            )
        if state.state_attrs.get("pig_context_scope"):
            result["pig_context_scope"] = state.state_attrs["pig_context_scope"]
        if state.state_attrs.get("pig_context_warning"):
            result["pig_context_warning"] = state.state_attrs["pig_context_warning"]
        return result

    @staticmethod
    def _decision_result_attrs(state: ProcessRunState) -> dict[str, object]:
        result: dict[str, object] = {}
        if state.state_attrs.get("decision_mode"):
            result["decision_mode"] = state.state_attrs["decision_mode"]
        if "applied_guidance_ids" in state.state_attrs:
            result["applied_guidance_ids"] = state.state_attrs["applied_guidance_ids"]
        if "decision_final_scores" in state.state_attrs:
            result["decision_final_scores"] = state.state_attrs["decision_final_scores"]
        if state.state_attrs.get("decision_rationale"):
            result["decision_rationale"] = state.state_attrs["decision_rationale"]
        if state.state_attrs.get("decision_attrs"):
            result["decision_attrs"] = state.state_attrs["decision_attrs"]
        if "pig_guidance_count" in state.state_attrs:
            result["pig_guidance_count"] = state.state_attrs["pig_guidance_count"]
        if state.state_attrs.get("pig_guidance_warning"):
            result["pig_guidance_warning"] = state.state_attrs["pig_guidance_warning"]
        if state.state_attrs.get("context_compaction"):
            result["context_compaction"] = state.state_attrs["context_compaction"]
        return result
