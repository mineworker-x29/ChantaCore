from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from chanta_core.skills.builtin import (
    execute_apply_approved_patch_skill,
    execute_check_self_conformance_skill,
    execute_echo_skill,
    execute_ingest_human_pi_skill,
    execute_inspect_ocel_recent_skill,
    execute_list_workspace_files_skill,
    execute_llm_chat_skill,
    execute_propose_file_edit_skill,
    execute_read_workspace_text_file_skill,
    execute_run_worker_once_skill,
    execute_run_scheduler_once_skill,
    execute_summarize_pi_artifacts_skill,
    execute_summarize_process_trace_skill,
    execute_summarize_text_skill,
    execute_summarize_workspace_markdown_skill,
)
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


@dataclass(frozen=True)
class SkillExecutionPolicy:
    raise_on_failure: bool = False
    record_failure_event: bool = True


class SkillExecutor:
    """Dispatches known skills to concrete runtime handlers."""

    def __init__(
        self,
        *,
        llm_client,
        context_assembler=None,
        trace_service=None,
        policy: SkillExecutionPolicy | None = None,
    ) -> None:
        from chanta_core.runtime.loop.context import ProcessContextAssembler
        from chanta_core.traces.trace_service import TraceService

        self.llm_client = llm_client
        self.context_assembler = context_assembler or ProcessContextAssembler()
        self.trace_service = trace_service or TraceService()
        self.policy = policy or SkillExecutionPolicy()
        self.events: list[Any] = []
        self._handlers = {
            "skill:apply_approved_patch": execute_apply_approved_patch_skill,
            "skill:llm_chat": execute_llm_chat_skill,
            "skill:check_self_conformance": execute_check_self_conformance_skill,
            "skill:echo": execute_echo_skill,
            "skill:ingest_human_pi": execute_ingest_human_pi_skill,
            "skill:propose_file_edit": execute_propose_file_edit_skill,
            "skill:run_worker_once": execute_run_worker_once_skill,
            "skill:run_scheduler_once": execute_run_scheduler_once_skill,
            "skill:summarize_text": execute_summarize_text_skill,
            "skill:inspect_ocel_recent": execute_inspect_ocel_recent_skill,
            "skill:list_workspace_files": execute_list_workspace_files_skill,
            "skill:read_workspace_text_file": execute_read_workspace_text_file_skill,
            "skill:summarize_pi_artifacts": execute_summarize_pi_artifacts_skill,
            "skill:summarize_process_trace": execute_summarize_process_trace_skill,
            "skill:summarize_workspace_markdown": execute_summarize_workspace_markdown_skill,
        }

    def execute(
        self,
        skill: Skill,
        context: SkillExecutionContext,
    ) -> SkillExecutionResult:
        self.events = []
        skill.validate()
        handler = self._handlers.get(skill.skill_id)
        if handler is not None:
            result = handler(
                skill=skill,
                context=context,
                llm_client=self.llm_client,
                context_assembler=self.context_assembler,
                trace_service=_RecordingTraceService(self.trace_service, self.events),
                ocel_store=getattr(self.trace_service, "ocel_store", None),
            )
            self._handle_failure_event_if_needed(skill, context, result)
            if self.policy.raise_on_failure and not result.success:
                raise RuntimeError(result.error or "Skill execution failed")
            return result

        result = SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=False,
            output_text=None,
            output_attrs={
                "execution_type": skill.execution_type,
                "failure_stage": "skill_dispatch",
                "exception_type": "UnsupportedSkillExecution",
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
            },
            error=f"Unsupported skill execution_type: {skill.execution_type}",
        )
        self._handle_failure_event_if_needed(skill, context, result)
        if self.policy.raise_on_failure:
            raise RuntimeError(result.error or "Skill execution failed")
        return result

    def _handle_failure_event_if_needed(
        self,
        skill: Skill,
        context: SkillExecutionContext,
        result: SkillExecutionResult,
    ) -> None:
        if result.success or not self.policy.record_failure_event:
            return

        from chanta_core.agents.default_agent import load_default_agent_profile
        from chanta_core.runtime.execution_context import ExecutionContext

        execution_context = ExecutionContext.create(
            agent_id=context.agent_id,
            user_input=context.user_input,
            session_id=context.session_id,
            metadata={"process_instance_id": context.process_instance_id},
        )
        event = self.trace_service.record_skill_execution_failed(
            execution_context,
            skill,
            error_message=result.error or "Skill execution failed",
            error_type=str(result.output_attrs.get("exception_type") or "SkillExecutionError"),
            failure_stage=str(result.output_attrs.get("failure_stage") or "skill_dispatch"),
            profile=context.context_attrs.get("agent_profile") or load_default_agent_profile(),
        )
        self.events.append(event)


class _RecordingTraceService:
    def __init__(self, trace_service, events: list[Any]) -> None:
        self._trace_service = trace_service
        self._events = events

    def __getattr__(self, name: str):
        attr = getattr(self._trace_service, name)
        if not callable(attr):
            return attr

        def wrapper(*args, **kwargs):
            result = attr(*args, **kwargs)
            if hasattr(result, "event_id") and hasattr(result, "event_type"):
                self._events.append(result)
            return result

        return wrapper
