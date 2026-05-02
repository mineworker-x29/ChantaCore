from __future__ import annotations

from typing import Any

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.factory import OCELFactory
from chanta_core.ocel.models import OCELRecord
from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.execution_context import ExecutionContext
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

    def record_user_request_received(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.user_request_received(context, profile)
        return self._record(
            context,
            "user_request_received",
            {"user_input": context.user_input},
            record,
        )

    def record_run_started(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.agent_run_started(context, profile)
        return self._record(
            context,
            "agent_run_started",
            {"user_input": context.user_input, "metadata": context.metadata},
            record,
        )

    def record_prompt_assembled(
        self,
        context: ExecutionContext,
        messages: list[ChatMessage],
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.prompt_assembled(context, profile, messages)
        return self._record(
            context,
            "prompt_assembled",
            {"messages": messages},
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
        record = self.ocel_factory.llm_call_started(
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
        record = self.ocel_factory.llm_response_received(
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

    def record_run_completed(
        self,
        context: ExecutionContext,
        profile: AgentProfile | None = None,
        response_text: str | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.agent_run_completed(
            context=context,
            profile=profile,
            response_text=response_text,
        )
        return self._record(context, "agent_run_completed", {}, record)

    def record_run_failed(
        self,
        context: ExecutionContext,
        error: Exception,
        profile: AgentProfile | None = None,
    ) -> AgentEvent:
        profile = self._profile(profile)
        record = self.ocel_factory.agent_run_failed(context, profile, error)
        return self._record(
            context,
            "agent_run_failed",
            {"error_type": type(error).__name__, "error": str(error)},
            record,
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
