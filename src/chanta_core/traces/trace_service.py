from __future__ import annotations

from chanta_core.llm.types import ChatMessage
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.traces.event import AgentEvent
from chanta_core.traces.event_store import AgentEventStore


class TraceService:
    def __init__(self, event_store: AgentEventStore | None = None) -> None:
        self.event_store = event_store or AgentEventStore()

    def record_run_started(self, context: ExecutionContext) -> AgentEvent:
        return self._record(
            context,
            "agent_run_started",
            {"user_input": context.user_input, "metadata": context.metadata},
        )

    def record_prompt_assembled(
        self,
        context: ExecutionContext,
        messages: list[ChatMessage],
    ) -> AgentEvent:
        return self._record(context, "prompt_assembled", {"messages": messages})

    def record_llm_response_received(
        self,
        context: ExecutionContext,
        response_text: str,
    ) -> AgentEvent:
        return self._record(
            context,
            "llm_response_received",
            {"response_text": response_text},
        )

    def record_run_completed(self, context: ExecutionContext) -> AgentEvent:
        return self._record(context, "agent_run_completed", {})

    def record_run_failed(
        self,
        context: ExecutionContext,
        error: Exception,
    ) -> AgentEvent:
        return self._record(
            context,
            "agent_run_failed",
            {"error_type": type(error).__name__, "error": str(error)},
        )

    def _record(
        self,
        context: ExecutionContext,
        event_type: str,
        payload: dict,
    ) -> AgentEvent:
        event = AgentEvent(
            event_type=event_type,
            session_id=context.session_id,
            agent_id=context.agent_id,
            payload=payload,
        )
        self.event_store.append(event)
        return event
