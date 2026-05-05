from __future__ import annotations

from typing import Any

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.factory import OCELFactory
from chanta_core.ocel.models import OCELRecord
from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.skills.skill import Skill
from chanta_core.traces.event import AgentEvent
from chanta_core.traces.event_store import AgentEventStore


class TraceService:
    def __init__(
        self,
        event_store: AgentEventStore | None = None,
        ocel_store: OCELStore | None = None,
        ocel_factory: OCELFactory | None = None,
    ) -> None:
        self.event_store = event_store or AgentEventStore()
        self.ocel_store = ocel_store or OCELStore()
        self.ocel_factory = ocel_factory or OCELFactory()
        self._llm_call_by_session: dict[str, str] = {}
        self._outcome_by_session: dict[str, str] = {}

    def record_user_request_received(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.receive_user_request(context, profile)
        return self._record(
            context,
            "user_request_received",
            {"user_input": context.user_input},
            record,
        )

    def record_process_instance_started(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.start_process_instance(context, profile)
        return self._record(
            context,
            "process_instance_started",
            {"user_input": context.user_input, "runtime_metadata": context.metadata},
            record,
        )

    def record_process_run_loop_started(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
        *,
        max_iterations: int,
        state_attrs: dict[str, Any] | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.start_process_run_loop(
            context,
            profile,
            max_iterations=max_iterations,
            state_attrs=state_attrs,
        )
        return self._record(
            context,
            "process_run_loop_started",
            {
                "process_instance_id": context.metadata.get("process_instance_id"),
                "max_iterations": max_iterations,
                "state_attrs": state_attrs or {},
            },
            record,
        )

    def record_next_activity_decided(
        self,
        context: ExecutionContext,
        *,
        next_activity: str,
        iteration: int,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.decide_next_activity(
            context,
            profile,
            next_activity=next_activity,
            iteration=iteration,
        )
        return self._record(
            context,
            "next_activity_decided",
            {
                "process_instance_id": context.metadata.get("process_instance_id"),
                "next_activity": next_activity,
                "iteration": iteration,
            },
            record,
        )

    def record_run_started(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        event = self.record_process_instance_started(context, profile)
        return AgentEvent(
            event_type="agent_run_started",
            session_id=event.session_id,
            agent_id=event.agent_id,
            payload=event.payload,
            event_id=event.event_id,
            timestamp=event.timestamp,
        )

    def record_prompt_assembled(
        self,
        context: ExecutionContext,
        messages: list[ChatMessage],
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.assemble_prompt(context, profile, messages)
        return self._record(
            context,
            "prompt_assembled",
            {"messages": messages},
            record,
        )

    def record_context_assembled(
        self,
        context: ExecutionContext,
        messages: list[ChatMessage],
        profile: AgentProfile | None = None,
        *,
        iteration: int,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.assemble_context(
            context,
            profile,
            messages,
            iteration=iteration,
        )
        return self._record(
            context,
            "context_assembled",
            {
                "process_instance_id": context.metadata.get("process_instance_id"),
                "iteration": iteration,
                "messages": messages,
            },
            record,
        )

    def record_skill_selected(
        self,
        context: ExecutionContext,
        skill: Skill,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.select_skill(context, profile, skill)
        return self._record(
            context,
            "skill_selected",
            {"skill_id": skill.skill_id, "skill_name": skill.skill_name},
            record,
        )

    def record_skill_decision(
        self,
        context: ExecutionContext,
        skill: Skill,
        *,
        decision,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        decision_attrs = {
            "selected_skill_id": decision.selected_skill_id,
            "decision_mode": decision.decision_mode,
            "applied_guidance_ids": decision.applied_guidance_ids,
            "tie_break_used": bool(decision.decision_attrs.get("tie_break_used")),
            "fallback_used": bool(decision.decision_attrs.get("fallback_used")),
            "rationale": decision.rationale,
            "advisory": True,
            "hard_policy": False,
        }
        record = self.ocel_factory.decide_skill(
            context,
            profile,
            skill,
            decision_attrs=decision_attrs,
        )
        return self._record(
            context,
            "skill_decision_recorded",
            {
                "process_instance_id": context.metadata.get("process_instance_id"),
                **decision_attrs,
            },
            record,
        )

    def record_skill_executed(
        self,
        context: ExecutionContext,
        skill: Skill,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.execute_skill(context, profile, skill)
        return self._record(
            context,
            "skill_executed",
            {"skill_id": skill.skill_id, "skill_name": skill.skill_name},
            record,
        )

    def record_skill_execution_failed(
        self,
        context: ExecutionContext,
        skill: Skill,
        *,
        error_message: str,
        error_type: str,
        failure_stage: str,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.fail_skill_execution(
            context,
            profile,
            skill,
            error_message=error_message,
            error_type=error_type,
            failure_stage=failure_stage,
        )
        return self._record(
            context,
            "skill_execution_failed",
            {
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
                "error": error_message,
                "error_type": error_type,
                "failure_stage": failure_stage,
            },
            record,
        )

    def record_tool_lifecycle_event(
        self,
        *,
        tool,
        request,
        context,
        event_activity: str,
        result=None,
        authorization: dict[str, Any] | None = None,
        error: str | None = None,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        execution_context = ExecutionContext.create(
            agent_id=context.agent_id,
            user_input=f"{request.tool_id}:{request.operation}",
            session_id=context.session_id,
            metadata={"process_instance_id": context.process_instance_id},
        )
        lifecycle = {
            "create_tool_request": "created",
            "authorize_tool_request": "authorized",
            "dispatch_tool": "dispatched",
            "execute_tool_operation": "executed",
            "complete_tool_operation": "completed",
            "fail_tool_operation": "failed",
            "observe_tool_result": "observed",
        }.get(event_activity, "recorded")
        record = self.ocel_factory.tool_lifecycle_event(
            execution_context,
            profile,
            event_activity=event_activity,
            lifecycle=lifecycle,
            tool=tool,
            request=request,
            result=result,
            authorization=authorization,
            error_message=error,
        )
        payload: dict[str, Any] = {
            "tool_id": tool.tool_id,
            "tool_name": tool.tool_name,
            "tool_request_id": request.tool_request_id,
            "operation": request.operation,
            "authorization": authorization or {},
        }
        if result is not None:
            payload["tool_result_id"] = result.tool_result_id
            payload["success"] = result.success
        if error:
            payload["error"] = error
        return self._record(execution_context, event_activity, payload, record)

    def record_worker_lifecycle_event(
        self,
        *,
        event_activity: str,
        worker,
        job=None,
        status: str,
        event_attrs: dict[str, Any] | None = None,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        process_instance_id = getattr(job, "process_instance_id", None) or (
            f"process_instance:{getattr(job, 'job_id', 'worker')}" if job is not None else None
        )
        session_id = getattr(job, "session_id", None) or "worker-session"
        agent_id = getattr(job, "agent_id", None) or profile.agent_id
        execution_context = ExecutionContext.create(
            agent_id=agent_id,
            user_input=getattr(job, "user_input", "") if job is not None else event_activity,
            session_id=session_id,
            metadata={"process_instance_id": process_instance_id},
        )
        record = self.ocel_factory.worker_lifecycle_event(
            execution_context,
            profile,
            event_activity=event_activity,
            worker=worker,
            job=job,
            status=status,
            event_attrs=event_attrs or {},
        )
        payload = {
            "worker_id": worker.worker_id,
            "job_id": getattr(job, "job_id", None),
            "status": status,
            **(event_attrs or {}),
        }
        return self._record(execution_context, event_activity, payload, record)

    def record_scheduler_lifecycle_event(
        self,
        *,
        event_activity: str,
        schedule=None,
        job_id: str | None = None,
        status: str,
        event_attrs: dict[str, Any] | None = None,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        execution_context = ExecutionContext.create(
            agent_id=getattr(schedule, "agent_id", None) or profile.agent_id,
            user_input=getattr(schedule, "user_input", "") if schedule is not None else event_activity,
            session_id="scheduler-session",
            metadata={"process_instance_id": f"process_instance:scheduler:{event_activity}"},
        )
        record = self.ocel_factory.scheduler_lifecycle_event(
            execution_context,
            profile,
            event_activity=event_activity,
            schedule=schedule,
            job_id=job_id,
            status=status,
            event_attrs=event_attrs or {},
        )
        payload = {
            "schedule_id": getattr(schedule, "schedule_id", None),
            "job_id": job_id,
            "status": status,
            **(event_attrs or {}),
        }
        return self._record(execution_context, event_activity, payload, record)

    def record_session_ocel_record(self, record: OCELRecord) -> None:
        self.ocel_store.append_record(record)

    def record_llm_call_started(
        self,
        context: ExecutionContext,
        messages: list[ChatMessage],
        provider_name: str | None = None,
        model_id: str | None = None,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.call_llm(
            context=context,
            profile=profile,
            messages=messages,
            provider_name=provider_name,
            model_id=model_id,
        )
        llm_call_id = str(record.event.event_attrs.get("llm_call_id") or "")
        if llm_call_id:
            self._llm_call_by_session[context.session_id] = llm_call_id
        return self._record(
            context,
            "llm_call_started",
            {
                "llm_call_id": llm_call_id,
                "provider": provider_name,
                "model": model_id,
            },
            record,
        )

    def record_llm_response_received(
        self,
        context: ExecutionContext,
        response_text: str,
        profile: AgentProfile | None = None,
        llm_call_id: str | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        llm_call_id = llm_call_id or self._llm_call_by_session.get(context.session_id)
        record = self.ocel_factory.receive_llm_response(
            context=context,
            profile=profile,
            response_text=response_text,
            llm_call_id=llm_call_id,
        )
        return self._record(
            context,
            "llm_response_received",
            {"response_text": response_text, "llm_call_id": llm_call_id},
            record,
        )

    def record_outcome_recorded(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
        response_text: str | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.record_outcome(
            context=context,
            profile=profile,
            response_text=response_text,
        )
        outcome_id = str(record.event.event_attrs.get("outcome_id") or "")
        if outcome_id:
            self._outcome_by_session[context.session_id] = outcome_id
        return self._record(
            context,
            "outcome_recorded",
            {"outcome_id": outcome_id, "response_text": response_text},
            record,
        )

    def record_result_observed(
        self,
        context: ExecutionContext,
        *,
        observation: dict[str, Any],
        iteration: int,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.observe_result(
            context,
            profile,
            observation=observation,
            iteration=iteration,
        )
        return self._record(
            context,
            "result_observed",
            {
                "process_instance_id": context.metadata.get("process_instance_id"),
                "iteration": iteration,
                "observation": observation,
            },
            record,
        )

    def record_process_instance_completed(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
        response_text: str | None = None,
        outcome_id: str | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        outcome_id = outcome_id or self._outcome_by_session.get(context.session_id)
        record = self.ocel_factory.complete_process_instance(
            context=context,
            profile=profile,
            response_text=response_text,
            outcome_id=outcome_id,
        )
        return self._record(
            context,
            "process_instance_completed",
            {"outcome_id": outcome_id, "response_text": response_text},
            record,
        )

    def record_run_completed(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
        response_text: str | None = None,
    ) -> AgentEvent:
        event = self.record_process_instance_completed(context, profile, response_text)
        return AgentEvent(
            event_type="agent_run_completed",
            session_id=event.session_id,
            agent_id=event.agent_id,
            payload=event.payload,
            event_id=event.event_id,
            timestamp=event.timestamp,
        )

    def record_process_instance_failed(
        self,
        context: ExecutionContext,
        error: Exception,
        profile: AgentProfile | None = None,
        failure_stage: str | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.fail_process_instance(
            context,
            profile,
            error,
            failure_stage=failure_stage,
        )
        return self._record(
            context,
            "process_instance_failed",
            {
                "error_type": type(error).__name__,
                "error": str(error),
                "failure_stage": failure_stage,
            },
            record,
        )

    def record_run_failed(
        self,
        context: ExecutionContext,
        error: Exception,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        event = self.record_process_instance_failed(context, error, profile)
        return AgentEvent(
            event_type="agent_run_failed",
            session_id=event.session_id,
            agent_id=event.agent_id,
            payload=event.payload,
            event_id=event.event_id,
            timestamp=event.timestamp,
        )

    def _record(
        self,
        context: ExecutionContext,
        event_type: str,
        payload: dict[str, Any],
        ocel_record: OCELRecord | None = None,
    ) -> AgentEvent:
        event = AgentEvent(
            event_type=event_type,
            session_id=context.session_id,
            agent_id=context.agent_id,
            payload=payload,
        )
        if ocel_record is not None:
            self.ocel_store.append_record(ocel_record, raw_event=event.to_dict())
        self.event_store.append(event)
        return event

    @staticmethod
    def _profile(profile: AgentProfile | None) -> AgentProfile:
        return profile or load_default_agent_profile()
