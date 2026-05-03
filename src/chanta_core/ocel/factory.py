from __future__ import annotations

import hashlib
import json
from typing import Any
from uuid import uuid4

from chanta_core.agents.profile import AgentProfile
from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELEvent, OCELRelation
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.skills.skill import Skill
from chanta_core.utility.time import utc_now_iso


def short_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:16]


def new_event_id(prefix: str = "evt") -> str:
    return f"{prefix}:{uuid4()}"


def new_object_id(prefix: str) -> str:
    return f"{prefix}:{uuid4()}"


class OCELFactory:
    source_runtime = "chanta_core"

    def receive_user_request(
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
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp, status="received"),
            relations=[
                self._e2o(event, self._request_id(context), "primary_request"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
            ],
        )

    def start_process_instance(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="process_instance_started",
            event_activity="start_process_instance",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="started",
            event_attrs={"runtime_metadata": context.metadata},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp, status="running"),
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, self._request_id(context), "primary_request"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
            ],
        )

    def start_process_run_loop(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        *,
        max_iterations: int,
        state_attrs: dict[str, Any] | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="process_run_loop_started",
            event_activity="start_process_run_loop",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="started",
            event_attrs={
                "max_iterations": max_iterations,
                "state_attrs": state_attrs or {},
            },
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp, status="running"),
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
            ],
        )

    def decide_next_activity(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        *,
        next_activity: str,
        iteration: int,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="next_activity_decided",
            event_activity="decide_next_activity",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="decided",
            event_attrs={
                "next_activity": next_activity,
                "iteration": iteration,
            },
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp),
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
            ],
        )

    def assemble_context(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        messages: list[ChatMessage],
        *,
        iteration: int,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        prompt = self._prompt_object(messages, timestamp)
        event = self._event(
            runtime_event_type="context_assembled",
            event_activity="assemble_context",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="assembled",
            event_attrs={
                "iteration": iteration,
                "message_count": len(messages),
                "messages": messages,
            },
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp) + [prompt],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, prompt.object_id, "assembled_prompt"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
                self._o2o(self._request_id(context), prompt.object_id, "request_to_prompt"),
            ],
        )

    def assemble_prompt(
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
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, prompt.object_id, "assembled_prompt"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
                self._o2o(self._request_id(context), prompt.object_id, "request_to_prompt"),
            ],
        )

    def select_skill(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        skill: Skill,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="skill_selected",
            event_activity="select_skill",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="selected",
            event_attrs={"skill_id": skill.skill_id, "skill_name": skill.skill_name},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp) + [self._skill_object(skill, timestamp)],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, skill.skill_id, "selected_skill"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
                self._o2o(self._process_id(context), skill.skill_id, "uses_skill"),
            ],
        )

    def decide_skill(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        skill: Skill,
        *,
        decision_attrs: dict[str, Any],
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="skill_decided",
            event_activity="decide_skill",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="decided",
            event_attrs=decision_attrs,
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp)
            + [self._skill_object(skill, timestamp)],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, skill.skill_id, "selected_skill"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
            ],
        )

    def execute_skill(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        skill: Skill,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="skill_executed",
            event_activity="execute_skill",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="executed",
            event_attrs={"skill_id": skill.skill_id, "skill_name": skill.skill_name},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp) + [self._skill_object(skill, timestamp)],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, skill.skill_id, "executed_skill"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
                self._o2o(self._process_id(context), skill.skill_id, "uses_skill"),
            ],
        )

    def fail_skill_execution(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        skill: Skill,
        *,
        error_message: str,
        error_type: str,
        failure_stage: str,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        error_object = OCELObject(
            object_id=new_object_id("error"),
            object_type="error",
            object_attrs={
                "object_key": error_type,
                "display_name": error_type,
                "error_message": error_message,
                "error_type": error_type,
                "failure_stage": failure_stage,
                "skill_id": skill.skill_id,
                "process_instance_id": self._process_id(context),
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )
        event = self._event(
            runtime_event_type="skill_execution_failed",
            event_activity="fail_skill_execution",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="failed",
            event_attrs={
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
                "error_message": error_message,
                "error_type": error_type,
                "failure_stage": failure_stage,
            },
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp, status="failed")
            + [self._skill_object(skill, timestamp), error_object],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, skill.skill_id, "failed_skill"),
                self._e2o(event, error_object.object_id, "observed_error"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
                self._o2o(self._process_id(context), skill.skill_id, "uses_skill"),
                self._o2o(error_object.object_id, skill.skill_id, "error_from_skill_execution"),
                self._o2o(error_object.object_id, self._process_id(context), "error_from_process"),
            ],
        )

    def call_llm(
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
            objects=self._base_objects(context, profile, timestamp) + [llm_call, provider, model],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, llm_call.object_id, "llm_call"),
                self._e2o(event, provider.object_id, "used_provider"),
                self._e2o(event, model.object_id, "used_model"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
            ],
        )

    def receive_llm_response(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        response_text: str,
        llm_call_id: str | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        response = self._response_object(response_text, timestamp)
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
            self._e2o(event, self._process_id(context), "process_context"),
            self._e2o(event, response.object_id, "generated_response"),
            self._e2o(event, self._session_id(context), "session_context"),
            self._e2o(event, self._agent_id(profile), "acting_agent"),
            *self._process_object_relations(context, profile),
        ]
        if llm_call_id:
            objects.append(self._llm_call_placeholder(llm_call_id, timestamp))
            relations.append(self._e2o(event, llm_call_id, "llm_call"))
            relations.append(self._o2o(llm_call_id, response.object_id, "llm_call_to_response"))
        return self._record(event, objects, relations)

    def observe_result(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        *,
        observation: dict[str, Any],
        iteration: int,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event = self._event(
            runtime_event_type="result_observed",
            event_activity="observe_result",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="observed",
            event_attrs={
                "iteration": iteration,
                "observation": observation,
            },
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp),
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
            ],
        )

    def record_outcome(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        response_text: str | None = None,
        outcome_id: str | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        outcome = self._outcome_object(context, timestamp, response_text, outcome_id)
        event = self._event(
            runtime_event_type="outcome_recorded",
            event_activity="record_outcome",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="recorded",
            event_attrs={"response_text": response_text, "outcome_id": outcome.object_id},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp) + [outcome],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, outcome.object_id, "produced_outcome"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
                self._o2o(outcome.object_id, self._process_id(context), "outcome_of_process"),
            ],
        )

    def complete_process_instance(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        response_text: str | None = None,
        outcome_id: str | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        outcome = self._outcome_object(context, timestamp, response_text, outcome_id)
        event = self._event(
            runtime_event_type="process_instance_completed",
            event_activity="complete_process_instance",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="completed",
            event_attrs={"response_text": response_text, "outcome_id": outcome.object_id},
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp, status="completed") + [outcome],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, outcome.object_id, "produced_outcome"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
                self._o2o(outcome.object_id, self._process_id(context), "outcome_of_process"),
            ],
        )

    def fail_process_instance(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        error: Exception,
        *,
        failure_stage: str | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        failure_stage = failure_stage or "unknown"
        error_object = OCELObject(
            object_id=new_object_id("error"),
            object_type="error",
            object_attrs={
                "object_key": type(error).__name__,
                "display_name": type(error).__name__,
                "error_message": str(error),
                "error_type": type(error).__name__,
                "error": str(error),
                "failure_stage": failure_stage,
                "process_instance_id": self._process_id(context),
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )
        event = self._event(
            runtime_event_type="process_instance_failed",
            event_activity="fail_process_instance",
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle="failed",
            event_attrs={
                "error_message": str(error),
                "error_type": type(error).__name__,
                "error": str(error),
                "failure_stage": failure_stage,
            },
        )
        return self._record(
            event=event,
            objects=self._base_objects(context, profile, timestamp, status="failed") + [error_object],
            relations=[
                self._e2o(event, self._process_id(context), "process_context"),
                self._e2o(event, error_object.object_id, "observed_error"),
                self._e2o(event, self._session_id(context), "session_context"),
                self._e2o(event, self._agent_id(profile), "acting_agent"),
                *self._process_object_relations(context, profile),
                self._o2o(error_object.object_id, self._process_id(context), "error_from_process"),
            ],
        )

    def tool_lifecycle_event(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        *,
        event_activity: str,
        lifecycle: str,
        tool,
        request,
        result=None,
        authorization: dict[str, Any] | None = None,
        error_message: str | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        event_attrs: dict[str, Any] = {
            "tool_id": tool.tool_id,
            "tool_name": tool.tool_name,
            "operation": request.operation,
            "tool_request_id": request.tool_request_id,
            "authorization": authorization or {},
        }
        if authorization:
            event_attrs.update(
                {
                    "decision": authorization.get("decision"),
                    "allowed": authorization.get("allowed"),
                    "requires_approval": authorization.get("requires_approval"),
                    "risk_level": authorization.get("risk_level"),
                    "permission_mode": authorization.get("mode"),
                    "reason": authorization.get("reason"),
                }
            )
        if result is not None:
            event_attrs.update(
                {
                    "tool_result_id": result.tool_result_id,
                    "tool_success": result.success,
                    "tool_error": result.error,
                }
            )
        if error_message:
            event_attrs["error_message"] = error_message

        event = self._event(
            runtime_event_type=event_activity,
            event_activity=event_activity,
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle=lifecycle,
            event_attrs=event_attrs,
        )
        tool_object = self._tool_object(tool, timestamp)
        request_object = self._tool_request_object(request, timestamp)
        objects = self._base_objects(context, profile, timestamp) + [
            tool_object,
            request_object,
        ]
        relations = [
            self._e2o(event, self._process_id(context), "process_context"),
            self._e2o(event, tool.tool_id, "requested_tool"),
            self._e2o(event, request.tool_request_id, "tool_request"),
            self._e2o(event, self._session_id(context), "session_context"),
            self._e2o(event, self._agent_id(profile), "acting_agent"),
            *self._process_object_relations(context, profile),
            self._o2o(request.tool_request_id, tool.tool_id, "requests_tool"),
        ]
        workspace_objects, workspace_relations = self._workspace_tool_context(
            event=event,
            tool=tool,
            request=request,
            result=result,
            timestamp=timestamp,
        )
        objects.extend(workspace_objects)
        relations.extend(workspace_relations)
        if event_activity in {
            "dispatch_tool",
            "execute_tool_operation",
            "complete_tool_operation",
            "fail_tool_operation",
            "observe_tool_result",
        }:
            relations.append(self._e2o(event, tool.tool_id, "executed_tool"))
        if result is not None:
            result_object = self._tool_result_object(result, timestamp)
            objects.append(result_object)
            relations.extend(
                [
                    self._e2o(event, result.tool_result_id, "tool_result"),
                    self._o2o(
                        result.tool_result_id,
                        request.tool_request_id,
                        "result_of_tool_request",
                    ),
                ]
            )
        if error_message:
            error_object = self._tool_error_object(
                request=request,
                error_message=error_message,
                timestamp=timestamp,
            )
            objects.append(error_object)
            relations.extend(
                [
                    self._e2o(event, error_object.object_id, "observed_error"),
                    self._o2o(
                        error_object.object_id,
                        request.tool_request_id,
                        "error_from_tool_execution",
                    ),
                ]
            )
        return self._record(event, objects, relations)

    def worker_lifecycle_event(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        *,
        event_activity: str,
        worker,
        job=None,
        status: str,
        event_attrs: dict[str, Any] | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        attrs = {
            "worker_id": worker.worker_id,
            "worker_name": worker.worker_name,
            "worker_status": status,
            "job_id": getattr(job, "job_id", None),
            "job_status": getattr(job, "status", None),
            **(event_attrs or {}),
        }
        event = self._event(
            runtime_event_type=event_activity,
            event_activity=event_activity,
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle=status,
            event_attrs=attrs,
        )
        worker_object = OCELObject(
            object_id=worker.worker_id,
            object_type="worker",
            object_attrs={
                "object_key": worker.worker_id,
                "display_name": worker.worker_name,
                "worker_name": worker.worker_name,
                "status": status,
                "created_at": worker.created_at,
                "updated_at": timestamp,
                **worker.worker_attrs,
            },
        )
        objects = self._base_objects(context, profile, timestamp) + [worker_object]
        relations = [
            self._e2o(event, self._process_id(context), "process_context"),
            self._e2o(event, worker.worker_id, "worker"),
            self._e2o(event, self._session_id(context), "session_context"),
            self._e2o(event, self._agent_id(profile), "acting_agent"),
            *self._process_object_relations(context, profile),
        ]
        if job is not None:
            job_object = OCELObject(
                object_id=job.job_id,
                object_type="process_job",
                object_attrs={
                    "object_key": job.job_id,
                    "display_name": job.job_id,
                    "job_type": job.job_type,
                    "status": job.status,
                    "priority": job.priority,
                    "retry_count": job.retry_count,
                    "max_retries": job.max_retries,
                    "created_at": job.created_at,
                    "updated_at": timestamp,
                    **job.job_attrs,
                },
            )
            objects.append(job_object)
            relations.extend(
                [
                    self._e2o(event, job.job_id, "process_job"),
                    self._o2o(job.job_id, worker.worker_id, "claimed_by_worker"),
                ]
            )
            if job.process_instance_id:
                relations.append(
                    self._o2o(job.job_id, job.process_instance_id, "runs_process_instance")
                )
        return self._record(event, objects, relations)

    def scheduler_lifecycle_event(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        *,
        event_activity: str,
        schedule=None,
        job_id: str | None = None,
        status: str,
        event_attrs: dict[str, Any] | None = None,
    ) -> OCELRecord:
        timestamp = utc_now_iso()
        attrs = {
            "schedule_id": getattr(schedule, "schedule_id", None),
            "schedule_name": getattr(schedule, "schedule_name", None),
            "schedule_status": status,
            "job_id": job_id,
            **(event_attrs or {}),
        }
        event = self._event(
            runtime_event_type=event_activity,
            event_activity=event_activity,
            context=context,
            profile=profile,
            timestamp=timestamp,
            lifecycle=status,
            event_attrs=attrs,
        )
        objects = self._base_objects(context, profile, timestamp)
        relations = [
            self._e2o(event, self._process_id(context), "process_context"),
            self._e2o(event, self._session_id(context), "session_context"),
            self._e2o(event, self._agent_id(profile), "acting_agent"),
            *self._process_object_relations(context, profile),
        ]
        if schedule is not None:
            schedule_object = OCELObject(
                object_id=schedule.schedule_id,
                object_type="process_schedule",
                object_attrs={
                    "object_key": schedule.schedule_id,
                    "display_name": schedule.schedule_name,
                    "schedule_name": schedule.schedule_name,
                    "schedule_type": schedule.schedule_type,
                    "status": schedule.status,
                    "interval_seconds": schedule.interval_seconds,
                    "run_at": schedule.run_at,
                    "next_run_at": schedule.next_run_at,
                    "last_run_at": schedule.last_run_at,
                    "created_at": schedule.created_at,
                    "updated_at": timestamp,
                    **schedule.schedule_attrs,
                },
            )
            objects.append(schedule_object)
            relations.extend(
                [
                    self._e2o(event, schedule.schedule_id, "process_schedule"),
                    self._o2o(schedule.schedule_id, self._agent_id(profile), "scheduled_for_agent"),
                ]
            )
        if job_id:
            job_object = OCELObject(
                object_id=job_id,
                object_type="process_job",
                object_attrs={
                    "object_key": job_id,
                    "display_name": job_id,
                    "created_at": timestamp,
                    "updated_at": timestamp,
                },
            )
            objects.append(job_object)
            relations.append(self._e2o(event, job_id, "process_job"))
            if schedule is not None:
                relations.append(self._o2o(schedule.schedule_id, job_id, "creates_process_job"))
        return self._record(event, objects, relations)

    # Backward-compatible wrappers used by v0.3 scripts/tests.
    def user_request_received(self, context: ExecutionContext, profile: AgentProfile) -> OCELRecord:
        return self.receive_user_request(context, profile)

    def agent_run_started(self, context: ExecutionContext, profile: AgentProfile) -> OCELRecord:
        return self.start_process_instance(context, profile)

    def prompt_assembled(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        messages: list[ChatMessage],
    ) -> OCELRecord:
        return self.assemble_prompt(context, profile, messages)

    def llm_call_started(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        messages: list[ChatMessage],
        provider_name: str | None,
        model_id: str | None,
    ) -> OCELRecord:
        return self.call_llm(context, profile, messages, provider_name, model_id)

    def llm_response_received(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        response_text: str,
        llm_call_id: str | None = None,
    ) -> OCELRecord:
        return self.receive_llm_response(context, profile, response_text, llm_call_id)

    def agent_run_completed(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        response_text: str | None = None,
    ) -> OCELRecord:
        return self.complete_process_instance(context, profile, response_text)

    def agent_run_failed(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
        error: Exception,
    ) -> OCELRecord:
        return self.fail_process_instance(context, profile, error)

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
            "process_instance_id": self._process_id(context),
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
        *,
        status: str = "running",
    ) -> list[OCELObject]:
        return [
            self._session_object(context, timestamp),
            self._agent_object(profile, timestamp),
            self._request_object(context, timestamp),
            self._process_object(context, timestamp, status=status),
        ]

    def _session_object(self, context: ExecutionContext, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=self._session_id(context),
            object_type="session",
            object_attrs={
                "object_key": context.session_id,
                "display_name": f"Session {context.session_id}",
                "session_id": context.session_id,
                "created_at": context.created_at,
                "updated_at": timestamp,
            },
        )

    def _agent_object(self, profile: AgentProfile, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=self._agent_id(profile),
            object_type="agent",
            object_attrs={
                "object_key": profile.agent_id,
                "display_name": profile.name,
                "role": profile.role,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _request_object(self, context: ExecutionContext, timestamp: str) -> OCELObject:
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

    def _process_object(
        self,
        context: ExecutionContext,
        timestamp: str,
        *,
        status: str,
    ) -> OCELObject:
        process_id = self._process_id(context)
        return OCELObject(
            object_id=process_id,
            object_type="process_instance",
            object_attrs={
                "object_key": process_id,
                "display_name": "Interactive user request process",
                "process_kind": "interactive_user_request",
                "source_type": "user_request",
                "mission_text": None,
                "goal_text": "Answer the user's request",
                "objective_text": context.user_input,
                "status": status,
                "created_at": context.created_at,
                "updated_at": timestamp,
            },
        )

    def _skill_object(self, skill: Skill, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=skill.skill_id,
            object_type="skill",
            object_attrs={
                "object_key": skill.skill_id,
                "display_name": skill.skill_name,
                "skill_name": skill.skill_name,
                "description": skill.description,
                "execution_type": skill.execution_type,
                "input_schema": skill.input_schema,
                "output_schema": skill.output_schema,
                "tags": skill.tags,
                "created_at": timestamp,
                "updated_at": timestamp,
                **skill.skill_attrs,
            },
        )

    def _tool_object(self, tool, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=tool.tool_id,
            object_type="tool",
            object_attrs={
                "object_key": tool.tool_id,
                "display_name": tool.tool_name,
                "tool_name": tool.tool_name,
                "description": tool.description,
                "tool_kind": tool.tool_kind,
                "safety_level": tool.safety_level,
                "supported_operations": tool.supported_operations,
                "created_at": timestamp,
                "updated_at": timestamp,
                **tool.tool_attrs,
            },
        )

    def _tool_request_object(self, request, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=request.tool_request_id,
            object_type="tool_request",
            object_attrs={
                "object_key": request.tool_request_id,
                "display_name": "Tool request",
                "tool_id": request.tool_id,
                "operation": request.operation,
                "process_instance_id": request.process_instance_id,
                "session_id": request.session_id,
                "agent_id": request.agent_id,
                "input_attrs": request.input_attrs,
                "request_attrs": request.request_attrs,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _tool_result_object(self, result, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=result.tool_result_id,
            object_type="tool_result",
            object_attrs={
                "object_key": result.tool_result_id,
                "display_name": "Tool result",
                "tool_request_id": result.tool_request_id,
                "tool_id": result.tool_id,
                "operation": result.operation,
                "success": result.success,
                "output_text": result.output_text,
                "output_attrs": result.output_attrs,
                "error": result.error,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _tool_error_object(
        self,
        *,
        request,
        error_message: str,
        timestamp: str,
    ) -> OCELObject:
        error_id = new_object_id("error")
        return OCELObject(
            object_id=error_id,
            object_type="error",
            object_attrs={
                "object_key": "ToolDispatchError",
                "display_name": "Tool dispatch error",
                "error_message": error_message,
                "error_type": "ToolDispatchError",
                "tool_id": request.tool_id,
                "operation": request.operation,
                "tool_request_id": request.tool_request_id,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _workspace_tool_context(
        self,
        *,
        event: OCELEvent,
        tool,
        request,
        result,
        timestamp: str,
    ) -> tuple[list[OCELObject], list[OCELRelation]]:
        if getattr(tool, "tool_id", None) != "tool:workspace":
            return [], []
        output_attrs = getattr(result, "output_attrs", {}) if result is not None else {}
        workspace_label = str(output_attrs.get("workspace_root_name") or "workspace")
        workspace_id = f"workspace:{short_hash(workspace_label)}"
        workspace = OCELObject(
            object_id=workspace_id,
            object_type="workspace",
            object_attrs={
                "object_key": workspace_id,
                "display_name": workspace_label,
                "workspace_root_name": workspace_label,
                "read_only": True,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )
        objects: list[OCELObject] = [workspace]
        relations: list[OCELRelation] = [
            self._e2o(event, workspace_id, "workspace_context"),
        ]
        relative_path = output_attrs.get("path") or request.input_attrs.get("path")
        if relative_path and str(relative_path) != ".":
            safe_path = str(relative_path).replace("\\", "/")
            file_id = f"file:{short_hash(safe_path)}"
            file_object = OCELObject(
                object_id=file_id,
                object_type="file",
                object_attrs={
                    "object_key": file_id,
                    "display_name": safe_path,
                    "relative_path": safe_path,
                    "size_bytes": output_attrs.get("size_bytes"),
                    "read_only": True,
                    "created_at": timestamp,
                    "updated_at": timestamp,
                },
            )
            objects.append(file_object)
            relations.extend(
                [
                    self._e2o(event, file_id, "target_file"),
                    self._o2o(request.tool_request_id, file_id, "targets_file"),
                    self._o2o(file_id, workspace_id, "belongs_to_workspace"),
                ]
            )
        return objects, relations

    def _prompt_object(self, messages: list[ChatMessage], timestamp: str) -> OCELObject:
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

    def _llm_call_object(self, messages: list[ChatMessage], timestamp: str) -> OCELObject:
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

    def _llm_call_placeholder(self, llm_call_id: str, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=llm_call_id,
            object_type="llm_call",
            object_attrs={
                "object_key": llm_call_id,
                "display_name": "LLM call",
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _provider_object(self, provider_name: str | None, timestamp: str) -> OCELObject:
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

    def _response_object(self, response_text: str, timestamp: str) -> OCELObject:
        return OCELObject(
            object_id=new_object_id("response"),
            object_type="llm_response",
            object_attrs={
                "object_key": short_hash(response_text),
                "display_name": "LLM response",
                "response_text": response_text,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _outcome_object(
        self,
        context: ExecutionContext,
        timestamp: str,
        response_text: str | None,
        outcome_id: str | None,
    ) -> OCELObject:
        return OCELObject(
            object_id=outcome_id or new_object_id("outcome"),
            object_type="outcome",
            object_attrs={
                "object_key": context.session_id,
                "display_name": "Process outcome",
                "response_text": response_text,
                "created_at": timestamp,
                "updated_at": timestamp,
            },
        )

    def _process_object_relations(
        self,
        context: ExecutionContext,
        profile: AgentProfile,
    ) -> list[OCELRelation]:
        return [
            self._o2o(self._request_id(context), self._session_id(context), "belongs_to_session"),
            self._o2o(self._process_id(context), self._request_id(context), "derived_from_request"),
            self._o2o(self._process_id(context), self._session_id(context), "handled_in_session"),
            self._o2o(self._process_id(context), self._agent_id(profile), "executed_by_agent"),
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
    def _process_id(context: ExecutionContext) -> str:
        process_instance_id = context.metadata.get("process_instance_id")
        if process_instance_id:
            return str(process_instance_id)
        return f"process_instance:{short_hash(f'{context.session_id}:{context.user_input}:process')}"

    @staticmethod
    def _e2o(event: OCELEvent, object_id: str, qualifier: str) -> OCELRelation:
        return OCELRelation.event_object(
            event_id=event.event_id,
            object_id=object_id,
            qualifier=qualifier,
        )

    @staticmethod
    def _o2o(source_object_id: str, target_object_id: str, qualifier: str) -> OCELRelation:
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
