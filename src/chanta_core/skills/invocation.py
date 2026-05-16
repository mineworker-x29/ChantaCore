from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.builtin.workspace_read import (
    execute_list_workspace_files_skill,
    execute_read_workspace_text_file_skill,
    execute_summarize_workspace_markdown_skill,
)
from chanta_core.skills.builtin.self_workspace_awareness import (
    execute_self_awareness_path_verify_skill,
    execute_self_awareness_workspace_inventory_skill,
)
from chanta_core.skills.builtin.self_code_text_perception import execute_self_awareness_text_read_skill
from chanta_core.skills.builtin.self_code_search_awareness import execute_self_awareness_workspace_search_skill
from chanta_core.skills.builtin.self_structure_summarization import execute_self_awareness_structure_summary_skill
from chanta_core.skills.builtin.self_project_structure_awareness import (
    execute_self_awareness_project_structure_skill,
)
from chanta_core.skills.builtin.self_surface_verification import execute_self_awareness_surface_verify_skill
from chanta_core.skills.builtin.self_directed_intention import execute_self_awareness_intention_candidate_skill
from chanta_core.skills.builtin.observation_digest import execute_observation_digest_skill
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.observation_digest import OBSERVATION_DIGESTION_SKILL_IDS
from chanta_core.skills.ids import (
    new_explicit_skill_invocation_decision_id,
    new_explicit_skill_invocation_input_id,
    new_explicit_skill_invocation_request_id,
    new_explicit_skill_invocation_result_id,
    new_explicit_skill_invocation_violation_id,
)
from chanta_core.skills.registry import SkillRegistry
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


SUPPORTED_EXPLICIT_SKILL_IDS = {
    "skill:list_workspace_files",
    "skill:read_workspace_text_file",
    "skill:summarize_workspace_markdown",
    "skill:self_awareness_workspace_inventory",
    "skill:self_awareness_path_verify",
    "skill:self_awareness_text_read",
    "skill:self_awareness_workspace_search",
    "skill:self_awareness_markdown_structure",
    "skill:self_awareness_python_symbols",
    "skill:self_awareness_project_structure",
    "skill:self_awareness_surface_verify",
    "skill:self_awareness_plan_candidate",
    "skill:self_awareness_todo_candidate",
    *OBSERVATION_DIGESTION_SKILL_IDS,
}


@dataclass(frozen=True)
class ExplicitSkillInvocationRequest:
    request_id: str
    skill_id: str
    requester_type: str | None
    requester_id: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    capability_decision_id: str | None
    permission_request_id: str | None
    session_permission_resolution_id: str | None
    workspace_sandbox_decision_id: str | None
    shell_network_decision_id: str | None
    invocation_mode: str
    status: str
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "skill_id": self.skill_id,
            "requester_type": self.requester_type,
            "requester_id": self.requester_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "capability_decision_id": self.capability_decision_id,
            "permission_request_id": self.permission_request_id,
            "session_permission_resolution_id": self.session_permission_resolution_id,
            "workspace_sandbox_decision_id": self.workspace_sandbox_decision_id,
            "shell_network_decision_id": self.shell_network_decision_id,
            "invocation_mode": self.invocation_mode,
            "status": self.status,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class ExplicitSkillInvocationInput:
    input_id: str
    request_id: str
    skill_id: str
    input_payload: dict[str, Any]
    input_preview: dict[str, Any]
    input_hash: str | None
    validation_status: str
    validation_messages: list[str]
    created_at: str
    input_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_id": self.input_id,
            "request_id": self.request_id,
            "skill_id": self.skill_id,
            "input_payload": dict(self.input_payload),
            "input_preview": dict(self.input_preview),
            "input_hash": self.input_hash,
            "validation_status": self.validation_status,
            "validation_messages": list(self.validation_messages),
            "created_at": self.created_at,
            "input_attrs": dict(self.input_attrs),
        }


@dataclass(frozen=True)
class ExplicitSkillInvocationDecision:
    decision_id: str
    request_id: str
    skill_id: str
    decision: str
    decision_basis: str
    can_execute: bool
    requires_permission: bool
    requires_review: bool
    reason: str | None
    violation_ids: list[str]
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "skill_id": self.skill_id,
            "decision": self.decision,
            "decision_basis": self.decision_basis,
            "can_execute": self.can_execute,
            "requires_permission": self.requires_permission,
            "requires_review": self.requires_review,
            "reason": self.reason,
            "violation_ids": list(self.violation_ids),
            "created_at": self.created_at,
            "decision_attrs": dict(self.decision_attrs),
        }


@dataclass(frozen=True)
class ExplicitSkillInvocationResult:
    result_id: str
    request_id: str
    skill_id: str
    status: str
    output_payload: dict[str, Any]
    output_preview: dict[str, Any]
    violation_ids: list[str]
    started_at: str | None
    completed_at: str | None
    error_message: str | None
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "request_id": self.request_id,
            "skill_id": self.skill_id,
            "status": self.status,
            "output_payload": dict(self.output_payload),
            "output_preview": dict(self.output_preview),
            "violation_ids": list(self.violation_ids),
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "error_message": self.error_message,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class ExplicitSkillInvocationViolation:
    violation_id: str
    request_id: str | None
    skill_id: str | None
    violation_type: str
    severity: str | None
    message: str
    subject_ref: str | None
    created_at: str
    violation_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "request_id": self.request_id,
            "skill_id": self.skill_id,
            "violation_type": self.violation_type,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "violation_attrs": dict(self.violation_attrs),
        }


class ExplicitSkillInvocationService:
    def __init__(
        self,
        *,
        skill_registry: SkillRegistry | None = None,
        capability_decision_service: Any | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.skill_registry = skill_registry or SkillRegistry()
        self.capability_decision_service = capability_decision_service
        self.last_request: ExplicitSkillInvocationRequest | None = None
        self.last_input: ExplicitSkillInvocationInput | None = None
        self.last_decision: ExplicitSkillInvocationDecision | None = None
        self.last_result: ExplicitSkillInvocationResult | None = None
        self.last_violations: list[ExplicitSkillInvocationViolation] = []

    def create_request(
        self,
        *,
        skill_id: str,
        invocation_mode: str = "explicit_api",
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        capability_decision_id: str | None = None,
        permission_request_id: str | None = None,
        session_permission_resolution_id: str | None = None,
        workspace_sandbox_decision_id: str | None = None,
        shell_network_decision_id: str | None = None,
    ) -> ExplicitSkillInvocationRequest:
        request = ExplicitSkillInvocationRequest(
            request_id=new_explicit_skill_invocation_request_id(),
            skill_id=skill_id,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            capability_decision_id=capability_decision_id,
            permission_request_id=permission_request_id,
            session_permission_resolution_id=session_permission_resolution_id,
            workspace_sandbox_decision_id=workspace_sandbox_decision_id,
            shell_network_decision_id=shell_network_decision_id,
            invocation_mode=invocation_mode,
            status="created",
            created_at=utc_now_iso(),
            request_attrs={
                "explicit_skill_id_required": True,
                "nl_route_used": False,
                "llm_classifier_used": False,
                "permission_grants_created": False,
            },
        )
        self.last_request = request
        self._record(
            "explicit_skill_invocation_requested",
            objects=[_object("explicit_skill_invocation_request", request.request_id, request.to_dict())],
            links=[("invocation_request_object", request.request_id)] + _reference_links(request),
            object_links=[],
            attrs={"skill_id": request.skill_id, "invocation_mode": request.invocation_mode},
        )
        return request

    def record_input(
        self,
        *,
        request: ExplicitSkillInvocationRequest,
        input_payload: dict[str, Any],
    ) -> ExplicitSkillInvocationInput:
        item = ExplicitSkillInvocationInput(
            input_id=new_explicit_skill_invocation_input_id(),
            request_id=request.request_id,
            skill_id=request.skill_id,
            input_payload=dict(input_payload),
            input_preview=_preview_mapping(input_payload),
            input_hash=_hash_mapping(input_payload),
            validation_status="needs_review",
            validation_messages=[],
            created_at=utc_now_iso(),
            input_attrs={
                "source_bodies_printed": False,
                "private_source_input": False,
            },
        )
        self.last_input = item
        self._record(
            "explicit_skill_invocation_input_recorded",
            objects=[_object("explicit_skill_invocation_input", item.input_id, item.to_dict())],
            links=[
                ("invocation_input_object", item.input_id),
                ("invocation_request_object", request.request_id),
            ],
            object_links=[(item.input_id, request.request_id, "belongs_to_invocation_request")],
            attrs={"skill_id": item.skill_id},
        )
        return item

    def validate_input(
        self,
        *,
        request: ExplicitSkillInvocationRequest,
        invocation_input: ExplicitSkillInvocationInput,
    ) -> ExplicitSkillInvocationInput:
        messages: list[str] = []
        payload = invocation_input.input_payload
        if not request.skill_id:
            messages.append("skill_id is required")
        if request.skill_id not in SUPPORTED_EXPLICIT_SKILL_IDS:
            messages.append("skill_id is not supported for explicit invocation")
        if request.skill_id in SUPPORTED_EXPLICIT_SKILL_IDS:
            if not str(payload.get("root_path") or "").strip():
                if request.skill_id not in {
                    "skill:agent_observation_normalize",
                    "skill:agent_behavior_infer",
                    "skill:agent_process_narrative",
                    "skill:external_behavior_fingerprint",
                    "skill:external_skill_assimilate",
                    "skill:external_skill_adapter_candidate",
                }:
                    messages.append("root_path is required")
            if request.skill_id in {
                "skill:read_workspace_text_file",
                "skill:summarize_workspace_markdown",
                "skill:agent_observation_source_inspect",
                "skill:agent_trace_observe",
                "skill:external_skill_source_inspect",
                "skill:external_skill_static_digest",
            } and not str(payload.get("relative_path") or "").strip():
                messages.append("relative_path is required")
            if request.skill_id == "skill:self_awareness_path_verify" and not str(payload.get("input_path") or "").strip():
                messages.append("input_path is required")
            if request.skill_id == "skill:self_awareness_text_read" and not str(payload.get("path") or "").strip():
                messages.append("path is required")
            if request.skill_id == "skill:self_awareness_workspace_search" and not str(payload.get("query") or "").strip():
                messages.append("query is required")
            if request.skill_id in {
                "skill:self_awareness_markdown_structure",
                "skill:self_awareness_python_symbols",
            } and not str(payload.get("path") or "").strip():
                messages.append("path is required")
            if request.skill_id == "skill:self_awareness_project_structure" and not str(
                payload.get("relative_path") or payload.get("path") or "."
            ).strip():
                messages.append("relative_path is required")
            if request.skill_id == "skill:self_awareness_surface_verify" and not str(payload.get("target_type") or "").strip():
                messages.append("target_type is required")
            relative_path = str(payload.get("relative_path") or ".")
            if Path(relative_path).is_absolute():
                messages.append("relative_path must not be absolute")
            input_path = str(payload.get("input_path") or ".")
            if request.skill_id == "skill:self_awareness_path_verify" and Path(input_path).is_absolute():
                messages.append("input_path must not be absolute")
            path_value = str(payload.get("path") or ".")
            if request.skill_id == "skill:self_awareness_text_read" and Path(path_value).is_absolute():
                messages.append("path must not be absolute")
            if request.skill_id in {
                "skill:self_awareness_markdown_structure",
                "skill:self_awareness_python_symbols",
            } and Path(path_value).is_absolute():
                messages.append("path must not be absolute")
            if request.skill_id == "skill:self_awareness_project_structure" and Path(relative_path).is_absolute():
                messages.append("relative_path must not be absolute")
        status = "invalid" if messages else "valid"
        validated = ExplicitSkillInvocationInput(
            **{
                **invocation_input.to_dict(),
                "validation_status": status,
                "validation_messages": messages,
            }
        )
        self.last_input = validated
        self._record(
            "explicit_skill_invocation_input_validated",
            objects=[_object("explicit_skill_invocation_input", validated.input_id, validated.to_dict())],
            links=[
                ("invocation_input_object", validated.input_id),
                ("invocation_request_object", request.request_id),
            ],
            object_links=[(validated.input_id, request.request_id, "belongs_to_invocation_request")],
            attrs={"validation_status": status, "message_count": len(messages)},
        )
        return validated

    def decide_invocation(
        self,
        *,
        request: ExplicitSkillInvocationRequest,
        invocation_input: ExplicitSkillInvocationInput,
        violations: list[ExplicitSkillInvocationViolation] | None = None,
    ) -> ExplicitSkillInvocationDecision:
        skill = self.skill_registry.get(request.skill_id) if request.skill_id else None
        current_violations = list(violations or [])
        if not request.skill_id:
            current_violations.append(
                self.record_violation(
                    request=request,
                    violation_type="invalid_input",
                    message="skill_id is required for explicit invocation.",
                    subject_ref=None,
                )
            )
        elif skill is None or request.skill_id not in SUPPORTED_EXPLICIT_SKILL_IDS:
            current_violations.append(
                self.record_violation(
                    request=request,
                    violation_type="unsupported_skill",
                    message="Only registered read-only workspace skills are supported.",
                    subject_ref=request.skill_id,
                )
            )
        for message in invocation_input.validation_messages:
            current_violations.append(
                self.record_violation(
                    request=request,
                    violation_type="invalid_input",
                    message=message,
                    subject_ref=request.skill_id,
                )
            )
        if any(item.violation_type == "unsupported_skill" for item in current_violations):
            decision = "unsupported"
            basis = "unsupported_skill"
            can_execute = False
        elif current_violations:
            decision = "deny"
            basis = "invalid_input"
            can_execute = False
        else:
            decision = "allow_explicit"
            basis = "input_valid"
            can_execute = True
        item = ExplicitSkillInvocationDecision(
            decision_id=new_explicit_skill_invocation_decision_id(),
            request_id=request.request_id,
            skill_id=request.skill_id,
            decision=decision,
            decision_basis=basis,
            can_execute=can_execute,
            requires_permission=False,
            requires_review=False,
            reason=None if can_execute else "Explicit invocation boundary check did not allow execution.",
            violation_ids=[violation.violation_id for violation in current_violations],
            created_at=utc_now_iso(),
            decision_attrs={
                "explicit_skill_id": True,
                "registered_skill": skill is not None,
                "supported_read_only_skill": request.skill_id in SUPPORTED_EXPLICIT_SKILL_IDS,
                "permission_grants_created": False,
            },
        )
        self.last_decision = item
        self.last_violations = current_violations
        self._record(
            "explicit_skill_invocation_decided",
            objects=[_object("explicit_skill_invocation_decision", item.decision_id, item.to_dict())],
            links=[
                ("invocation_decision_object", item.decision_id),
                ("invocation_request_object", request.request_id),
            ]
            + [("invocation_violation_object", violation.violation_id) for violation in current_violations],
            object_links=[(item.decision_id, request.request_id, "belongs_to_invocation_request")]
            + [
                (item.decision_id, violation.violation_id, "references_invocation_violation")
                for violation in current_violations
            ],
            attrs={"decision": item.decision, "can_execute": item.can_execute},
        )
        return item

    def record_violation(
        self,
        *,
        request: ExplicitSkillInvocationRequest | None,
        violation_type: str,
        message: str,
        subject_ref: str | None,
        severity: str | None = "high",
        violation_attrs: dict[str, Any] | None = None,
    ) -> ExplicitSkillInvocationViolation:
        violation = ExplicitSkillInvocationViolation(
            violation_id=new_explicit_skill_invocation_violation_id(),
            request_id=request.request_id if request else None,
            skill_id=request.skill_id if request else None,
            violation_type=violation_type,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            violation_attrs={
                "permission_grants_created": False,
                **dict(violation_attrs or {}),
            },
        )
        self._record(
            "explicit_skill_invocation_violation_recorded",
            objects=[
                _object(
                    "explicit_skill_invocation_violation",
                    violation.violation_id,
                    violation.to_dict(),
                )
            ],
            links=[("invocation_violation_object", violation.violation_id)]
            + (
                [("invocation_request_object", request.request_id)]
                if request is not None
                else []
            ),
            object_links=(
                [(violation.violation_id, request.request_id, "belongs_to_invocation_request")]
                if request is not None
                else []
            ),
            attrs={"violation_type": violation.violation_type, "severity": violation.severity or ""},
        )
        return violation

    def invoke_explicit_skill(
        self,
        *,
        skill_id: str,
        input_payload: dict[str, Any],
        invocation_mode: str = "explicit_api",
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        capability_decision_id: str | None = None,
        permission_request_id: str | None = None,
        session_permission_resolution_id: str | None = None,
        workspace_sandbox_decision_id: str | None = None,
        shell_network_decision_id: str | None = None,
    ) -> ExplicitSkillInvocationResult:
        request = self.create_request(
            skill_id=skill_id,
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            capability_decision_id=capability_decision_id,
            permission_request_id=permission_request_id,
            session_permission_resolution_id=session_permission_resolution_id,
            workspace_sandbox_decision_id=workspace_sandbox_decision_id,
            shell_network_decision_id=shell_network_decision_id,
        )
        invocation_input = self.record_input(request=request, input_payload=input_payload)
        validated_input = self.validate_input(request=request, invocation_input=invocation_input)
        decision = self.decide_invocation(request=request, invocation_input=validated_input)
        if not decision.can_execute:
            status = "unsupported" if decision.decision == "unsupported" else "denied"
            return self.record_result(
                request=request,
                status=status,
                output_payload={},
                violation_ids=decision.violation_ids,
                error_message=decision.reason,
                started_at=None,
            )
        started_at = utc_now_iso()
        self._record(
            "explicit_skill_invocation_started",
            objects=[_object("explicit_skill_invocation_request", request.request_id, request.to_dict())],
            links=[("invocation_request_object", request.request_id)],
            object_links=[],
            attrs={"skill_id": request.skill_id},
        )
        skill_result = self._execute_supported_skill(
            request=request,
            input_payload=validated_input.input_payload,
        )
        status = "completed" if skill_result.success else "failed"
        violation_ids = list(skill_result.output_attrs.get("violation_ids") or [])
        if not skill_result.success and not violation_ids:
            violation = self.record_violation(
                request=request,
                violation_type="boundary_violation",
                message=skill_result.error or "Explicit skill invocation failed.",
                subject_ref=request.skill_id,
            )
            violation_ids.append(violation.violation_id)
        return self.record_result(
            request=request,
            status=status,
            output_payload=skill_result.to_dict(),
            violation_ids=violation_ids,
            error_message=skill_result.error,
            started_at=started_at,
        )

    def record_result(
        self,
        *,
        request: ExplicitSkillInvocationRequest,
        status: str,
        output_payload: dict[str, Any],
        violation_ids: list[str],
        error_message: str | None,
        started_at: str | None,
    ) -> ExplicitSkillInvocationResult:
        normalized_output_payload = _with_flattened_output_attrs(output_payload)
        result = ExplicitSkillInvocationResult(
            result_id=new_explicit_skill_invocation_result_id(),
            request_id=request.request_id,
            skill_id=request.skill_id,
            status=status,
            output_payload=normalized_output_payload,
            output_preview=_preview_mapping(normalized_output_payload),
            violation_ids=list(violation_ids),
            started_at=started_at,
            completed_at=utc_now_iso(),
            error_message=error_message,
            result_attrs={
                "explicit_skill_id": True,
                "nl_route_used": False,
                "llm_call_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "mcp_connection_used": False,
                "plugin_loading_used": False,
                "workspace_write_used": False,
                "permission_grants_created": False,
                "line_delimited_invocation_store_created": False,
            },
        )
        self.last_result = result
        event_activity = (
            "explicit_skill_invocation_completed"
            if status == "completed"
            else "explicit_skill_invocation_denied"
            if status in {"denied", "unsupported"}
            else "explicit_skill_invocation_failed"
        )
        self._record(
            event_activity,
            objects=[_object("explicit_skill_invocation_result", result.result_id, result.to_dict())],
            links=[
                ("invocation_result_object", result.result_id),
                ("invocation_request_object", request.request_id),
            ],
            object_links=[(result.result_id, request.request_id, "belongs_to_invocation_request")],
            attrs={"status": result.status, "skill_id": result.skill_id},
        )
        return result

    def render_invocation_summary(self, result: ExplicitSkillInvocationResult) -> str:
        lines = [
            f"Explicit Skill Invocation: {result.skill_id}",
            f"status={result.status}",
            f"result_id={result.result_id}",
            f"violation_count={len(result.violation_ids)}",
            "natural_language_routing=false",
            "permission_grants_created=false",
            "shell_network_mcp_plugin_execution=false",
        ]
        if result.error_message:
            lines.append(f"error={result.error_message}")
        preview = result.output_preview
        if preview:
            lines.append(f"output_preview={json.dumps(preview, ensure_ascii=False, sort_keys=True)}")
        return "\n".join(lines)

    def _execute_supported_skill(
        self,
        *,
        request: ExplicitSkillInvocationRequest,
        input_payload: dict[str, Any],
    ) -> SkillExecutionResult:
        skill = self.skill_registry.require(request.skill_id)
        context = SkillExecutionContext(
            process_instance_id=request.process_instance_id or "process_instance:explicit_skill_invocation",
            session_id=request.session_id or "session:explicit_skill_invocation",
            agent_id=request.requester_id or "explicit_skill_invocation",
            user_input=f"explicit skill invocation: {request.skill_id}",
            system_prompt=None,
            context_attrs=dict(input_payload),
        )
        executor_by_id: dict[str, Callable[..., SkillExecutionResult]] = {
            "skill:list_workspace_files": execute_list_workspace_files_skill,
            "skill:read_workspace_text_file": execute_read_workspace_text_file_skill,
            "skill:summarize_workspace_markdown": execute_summarize_workspace_markdown_skill,
            "skill:self_awareness_workspace_inventory": execute_self_awareness_workspace_inventory_skill,
            "skill:self_awareness_path_verify": execute_self_awareness_path_verify_skill,
            "skill:self_awareness_text_read": execute_self_awareness_text_read_skill,
            "skill:self_awareness_workspace_search": execute_self_awareness_workspace_search_skill,
            "skill:self_awareness_markdown_structure": execute_self_awareness_structure_summary_skill,
            "skill:self_awareness_python_symbols": execute_self_awareness_structure_summary_skill,
            "skill:self_awareness_project_structure": execute_self_awareness_project_structure_skill,
            "skill:self_awareness_surface_verify": execute_self_awareness_surface_verify_skill,
            "skill:self_awareness_plan_candidate": execute_self_awareness_intention_candidate_skill,
            "skill:self_awareness_todo_candidate": execute_self_awareness_intention_candidate_skill,
        }
        executor = executor_by_id.get(request.skill_id, execute_observation_digest_skill)
        return executor(
            skill=skill,
            context=context,
            trace_service=self.trace_service,
        )

    def _record(
        self,
        activity: str,
        *,
        objects: list[OCELObject],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
        attrs: dict[str, Any],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "explicit_skill_invocation": True,
                "nl_route_used": False,
                "llm_call_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "permission_grants_created": False,
            },
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in links
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
            for source_id, target_id, qualifier in object_links
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def _preview_mapping(value: dict[str, Any], *, max_chars: int = 200) -> dict[str, Any]:
    preview: dict[str, Any] = {}
    for key, item in value.items():
        if isinstance(item, str):
            preview[key] = item[:max_chars]
        elif isinstance(item, (int, float, bool)) or item is None:
            preview[key] = item
        elif isinstance(item, list):
            preview[key] = {"list_count": len(item)}
        elif isinstance(item, dict):
            preview[key] = {"dict_keys": sorted(str(inner_key) for inner_key in item)[:20]}
        else:
            preview[key] = str(type(item).__name__)
    return preview


def _with_flattened_output_attrs(value: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(value)
    output_attrs = normalized.get("output_attrs")
    if not isinstance(output_attrs, dict):
        return normalized
    flattened_attrs = dict(output_attrs)
    nested_result_attrs = flattened_attrs.get("result_attrs")
    if isinstance(nested_result_attrs, dict):
        for key, item in nested_result_attrs.items():
            flattened_attrs.setdefault(key, item)
    normalized["output_attrs"] = flattened_attrs
    return normalized


def _hash_mapping(value: dict[str, Any]) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _reference_links(request: ExplicitSkillInvocationRequest) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for qualifier, value in [
        ("capability_decision", request.capability_decision_id),
        ("permission_request", request.permission_request_id),
        ("session_permission_resolution", request.session_permission_resolution_id),
        ("workspace_sandbox_decision", request.workspace_sandbox_decision_id),
        ("shell_network_decision", request.shell_network_decision_id),
    ]:
        if value:
            links.append((qualifier, value))
    return links


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={
            "object_key": object_id,
            "display_name": object_id,
            **attrs,
        },
    )
