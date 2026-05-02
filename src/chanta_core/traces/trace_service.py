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
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.fail_process_instance(context, profile, error)
        return self._record(
            context,
            "process_instance_failed",
            {"error_type": type(error).__name__, "error": str(error)},
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
