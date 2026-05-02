from __future__ import annotations

import hashlib
import json
from typing import Any
from uuid import uuid4

from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.utility.time import utc_now_iso


def short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def new_event_id(prefix: str = "evt") -> str:
    return f"{prefix}:{uuid4()}"


def new_object_id(prefix: str) -> str:
    return f"{prefix}:{uuid4()}"


class OCELFactory:
    source_runtime = "chanta_core"

    def user_request_received(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="user_request_received",
            event_activity="receive_user_request",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="received",
            event_attrs={"user_input": context.user_input},
        )
        objects = self._base_objects(context, profile, timestamp)
        return self._record(
            event=event,
            objects=objects,
            relations=[
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                self._e2o(event, self._request_id(context), "primary_request"),
                self._e2o(event, self._goal_id(context), "goal_context"),
                *self._goal_object_relations(context, profile),
            ],
        )

    def agent_run_started(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="agent_run_started",
            event_activity="start_goal",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="started",
            event_attrs={"runtime_metadata": context.metadata},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp),
            relations=[
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                self._e2o(event, self._request_id(context), "primary_request"),
                self._e2o(event, self._goal_id(context), "goal_context"),
                *self._goal_object_relations(context, profile),
            ],
        )

    def prompt_assembled(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        messages: list[ChatMessage],
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        prompt = self._prompt_object(messages, timestamp)
        event = self._event(
            runtime_event_type="prompt_assembled",
            event_activity="assemble_prompt",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="assembled",
            event_attrs={"message_count": len(messages), "messages": messages},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp) + [prompt],
            relations=[
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                self._e2o(event, self._request_id(context), "primary_request"),
                self._e2o(event, self._goal_id(context), "goal_context"),
                self._e2o(event, prompt.object_id, "assembled_prompt"),
                *self._goal_object_relations(context, profile),
                self._o2o(self._request_id(context), prompt.object_id, "request_to_prompt"),
            ],
        )

    def llm_call_started(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        messages: list[ChatMessage],
        provider_name: str | None,
        model_id: str | None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        llm_call = self._llm_call_object(messages, timestamp)
        provider = self._provider_object(provider_name, timestamp)
        model = self._model_object(model_id, timestamp)
        prompt = self._prompt_object(messages, timestamp)
        event = self._event(
            runtime_event_type="llm_call_started",
            event_activity="call_llm",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="started",
            event_attrs={
                "llm_call_id": llm_call.object_id,
                "provider": provider_name,
                "model": model_id,
            },
        )
        return self._record(
            event=event,
            objects=(
                self._base_objects(context, profile, timestamp)
                + [prompt, llm_call, provider, model]
            ),
            relations=[
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                self._e2o(event, self._goal_id(context), "goal_context"),
                self._e2o(event, prompt.object_id, "assembled_prompt"),
                self._e2o(event, llm_call.object_id, "llm_call"),
                self._e2o(event, provider.object_id, "used_provider"),
                self._e2o(event, model.object_id, "used_model"),
                *self._goal_object_relations(context, profile),
                self._o2o(prompt.object_id, llm_call.object_id, "prompt_to_llm_call"),
            ],
        )

    def llm_response_received(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        response_text: str,
        llm_call_id: str | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        response = OCELObject(
            object_id=new_object_id("response"),
            object_type="llm_response",
            object_attrs={
                "object_key": short_hash(response_text),
                "display_name": "LLM response",
                "response_text": response_text,
                "created_at": timestamp,
            },
        )
        event = self._event(
            runtime_event_type="llm_response_received",
            event_activity="receive_llm_response",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="received",
            event_attrs={"response_text": response_text, "llm_call_id": llm_call_id},
        )
        objects = self._base_objects(context, profile, timestamp) + [response]
        relations: list[OCELRelation] = [
            self._e2o(event, self._session_id(context), "session_context"),
            self._e2o(event, self._agent_id(profile), "acting_agent"),
            self._e2o(event, self._goal_id(context), "goal_context"),
            self._e2o(event, response.object_id, "generated_response"),
            *self._goal_object_relations(context, profile),
        ]
        if llm_call_id:
            llm_call = OCELObject(
                object_id=llm_call_id,
                object_type="llm_call",
                object_attrs={
                    "object_key": llm_call_id,
                    "display_name": "LLM call",
                    "created_at": timestamp,
                },
            )
            objects.append(llm_call)
            relations.append(self._e2o(event, llm_call_id, "llm_call"))
            relations.append(
                self._o2o(llm_call_id, response.object_id, "llm_call_to_response")
            )
        return self._record(event, objects, relations)

    def agent_run_completed(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        response_text: str | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        outcome = OCELObject(
            object_id=new_object_id("outcome"),
            object_type="outcome",
            object_attrs={
                "object_key": context.session_id,
                "display_name": "Agent run outcome",
                "response_text": response_text,
                "created_at": timestamp,
            },
        )
        event = self._event(
            runtime_event_type="agent_run_completed",
            event_activity="complete_goal",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="completed",
            event_attrs={"response_text": response_text},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp) + [outcome],
            relations=[
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                self._e2o(event, self._goal_id(context), "goal_context"),
                self._e2o(event, outcome.object_id, "produced_outcome"),
                *self._goal_object_relations(context, profile),
                self._o2o(outcome.object_id, self._goal_id(context), "outcome_of_run"),
            ],
        )

    def agent_run_failed(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        error: Exception,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        error_object = OCELObject(
            object_id=new_object_id("error"),
            object_type="error",
            object_attrs={
                "object_key": type(error).__name__,
                "display_name": type(error).__name__,
                "error_type": type(error).__name__,
                "error": str(error),
                "created_at": timestamp,
            },
        )
        event = self._event(
            runtime_event_type="agent_run_failed",
            event_activity="fail_run",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="failed",
            event_attrs={"error_type": type(error).__name__, "error": str(error)},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp) + [error_object],
            relations=[
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                self._e2o(event, self._goal_id(context), "goal_context"),
                self._e2o(event, error_object.object_id, "observed_error"),
                *self._goal_object_relations(context, profile),
                self._o2o(error_object.object_id, self._goal_id(context), "error_from_run"),
            ],
        )

    def _event(
        self,
        *,
        runtime_event_type: str,
        event_activity: str,
        context: ExecutionContext,
        profile: AgentProfile,
        timestamp: str,
        lifecycle: str,
        event_attrs: dict[str, Any],
    ) -> OCELEvent:
        attrs = {
            **event_attrs,
            "runtime_event_type": runtime_event_type,
            "lifecycle": lifecycle,
            "source_runtime": self.source_runtime,
            "session_id": context.session_id,
            "trace_id": context.session_id,
            "actor_type": "agent",
            "actor_id": profile.agent_id,
        }
        return OCELEvent(
            event_id=new_event_id("evt"),
            event_activity=event_activity,
            event_timestamp=timestamp,
            event_attrs=attrs,
        )

    def _base_objects(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        timestamp: str,
    ) -> list[OCELObject]:
        return [
            OCELObject(
                object_id=self._session_id(context),
                object_type="session",
                object_attrs={
                    "object_key": context.session_id,
                    "display_name": f"Session {context.session_id}",
                    "session_id": context.session_id,
                    "created_at": context.created_at,
                    "updated_at": timestamp,
                },
            ),
            OCELObject(
                object_id=self._agent_id(profile),
                object_type="agent",
                object_attrs={
                    "object_key": profile.agent_id,
                    "display_name": profile.name,
                    "role": profile.role,
                    "created_at": timestamp,
                    "updated_at": timestamp,
                },
            ),
            self._request_object(context, timestamp),
            self._goal_object(context, timestamp),
        ]

    def _request_object(
        self,
        context: ExecutionContext,
        timestamp: str,
    ) -> OCELObject:
        request_id = self._request_id(context)
        return OCELObject(
            object_id=request_id,
            object_type="user_request",
            object_attrs={
                "object_key": request_id,
                "display_name": "User request",
                "user_input": context.user_input,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _goal_object(
        self,
        context: ExecutionContext,
        timestamp: str,
    ) -> OCELObject:
        goal_id = self._goal_id(context)
        return OCELObject(
            object_id=goal_id,
            object_type="goal",
            object_attrs={
                "object_key": goal_id,
                "display_name": "Runtime goal",
                "goal_kind": "respond_to_user_request",
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _prompt_object(
        self,
        messages: list[ChatMessage],
        timestamp: str,
    ) -> OCELObject:
        prompt_text = json.dumps(messages, ensure_ascii=False, sort_keys=True)
        prompt_id = f"prompt:{short_hash(prompt_text)}"
        return OCELObject(
            object_id=prompt_id,
            object_type="prompt",
            object_attrs={
                "object_key": prompt_id,
                "display_name": "Runtime prompt",
                "messages": messages,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _llm_call_object(
        self,
        messages: list[ChatMessage],
        timestamp: str,
    ) -> OCELObject:
        return OCELObject(
            object_id=new_object_id("llm_call"),
            object_type="llm_call",
            object_attrs={
                "object_key": short_hash(json.dumps(messages, ensure_ascii=False, sort_keys=True)),
                "display_name": "LLM call",
                "message_count": len(messages),
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _provider_object(
        self,
        provider_name: str | None,
        timestamp: str,
    ) -> OCELObject:
        provider_key = provider_name or "unknown"
        return OCELObject(
            object_id=f"provider:{provider_key}",
            object_type="provider",
            object_attrs={
                "object_key": provider_key,
                "display_name": provider_key,
                "provider": provider_name,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _model_object(self, model_id: str | None, timestamp: str) -> OCELObject:
        model_key = model_id or "unknown"
        return OCELObject(
            object_id=f"model:{short_hash(model_key)}",
            object_type="llm_model",
            object_attrs={
                "object_key": model_key,
                "display_name": model_key,
                "model": model_id,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _goal_object_relations(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
    ) -> list[OCELRelation]:
        return [
            self._o2o(self._request_id(context), self._session_id(context), "belongs_to_session"),
            self._o2o(self._goal_id(context), self._request_id(context), "derived_from_request"),
            self._o2o(self._goal_id(context), self._session_id(context), "handled_in_session"),
            self._o2o(self._goal_id(context), self._agent_id(profile), "executed_by_agent"),
        ]

    @staticmethod
    def _session_id(context: ExecutionContext) -> str:
        return f"session:{context.session_id}"

    @staticmethod
    def _agent_id(profile: AgentProfile) -> str:
        return f"agent:{profile.agent_id}"

    @staticmethod
    def _request_id(context: ExecutionContext) -> str:
        return f"request:{short_hash(f'{context.session_id}:{context.user_input}')}"

    @staticmethod
    def _goal_id(context: ExecutionContext) -> str:
        return f"goal:{short_hash(f'{context.session_id}:{context.user_input}:goal')}"

    @staticmethod
    def _e2o(
        event: OCELEvent,
        object_id: str,
        qualifier: str,
    ) -> OCELRelation:
        return OCELRelation.event_object(
            event_id=event.event_id,
            object_id=object_id,
            qualifier=qualifier,
        )

    @staticmethod
    def _o2o(
        source_object_id: str,
        target_object_id: str,
        qualifier: str,
    ) -> OCELRelation:
        return OCELRelation.object_object(
            source_object_id=source_object_id,
            target_object_id=target_object_id,
            qualifier=qualifier,
        )

    @staticmethod
    def _record(
        event: OCELEvent,
        objects: list[OCELObject],
        relations: list[OCELRelation],
    ) -> OCELRecord:
        unique_objects: dict[str, OCELObject] = {}
        for item in objects:
            unique_objects[item.object_id] = item
        unique_relations: dict[tuple[str, str, str, str], OCELRelation] = {}
        for relation in relations:
            unique_relations[
                (
                    relation.relation_kind,
                    relation.source_id,
                    relation.target_id,
                    relation.qualifier,
                )
            ] = relation
        return OCELRecord(
            event=event,
            objects=list(unique_objects.values()),
            relations=list(unique_relations.values()),
        )
