from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_read_only_execution_gate_policy_id,
    new_skill_execution_gate_decision_id,
    new_skill_execution_gate_finding_id,
    new_skill_execution_gate_request_id,
    new_skill_execution_gate_result_id,
)
from chanta_core.skills.invocation import ExplicitSkillInvocationService, SUPPORTED_EXPLICIT_SKILL_IDS
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


DENIED_SKILL_CATEGORIES = ["write", "shell", "network", "mcp", "plugin", "external_capability"]


@dataclass(frozen=True)
class ReadOnlyExecutionGatePolicy:
    policy_id: str
    policy_name: str
    supported_skill_ids: list[str]
    denied_skill_categories: list[str]
    requires_permission_for_read_only: bool
    allow_without_permission_for_read_only: bool
    require_capability_available: bool
    enforce_workspace_boundary: bool
    status: str
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "supported_skill_ids": list(self.supported_skill_ids),
            "denied_skill_categories": list(self.denied_skill_categories),
            "requires_permission_for_read_only": self.requires_permission_for_read_only,
            "allow_without_permission_for_read_only": self.allow_without_permission_for_read_only,
            "require_capability_available": self.require_capability_available,
            "enforce_workspace_boundary": self.enforce_workspace_boundary,
            "status": self.status,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class SkillExecutionGateRequest:
    gate_request_id: str
    explicit_invocation_request_id: str | None
    skill_id: str
    input_payload_preview: dict[str, Any]
    invocation_mode: str
    requester_type: str | None
    requester_id: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    capability_decision_id: str | None
    permission_request_id: str | None
    permission_decision_id: str | None
    session_permission_resolution_id: str | None
    workspace_read_root_id: str | None
    workspace_sandbox_decision_id: str | None
    shell_network_decision_id: str | None
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_request_id": self.gate_request_id,
            "explicit_invocation_request_id": self.explicit_invocation_request_id,
            "skill_id": self.skill_id,
            "input_payload_preview": dict(self.input_payload_preview),
            "invocation_mode": self.invocation_mode,
            "requester_type": self.requester_type,
            "requester_id": self.requester_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "capability_decision_id": self.capability_decision_id,
            "permission_request_id": self.permission_request_id,
            "permission_decision_id": self.permission_decision_id,
            "session_permission_resolution_id": self.session_permission_resolution_id,
            "workspace_read_root_id": self.workspace_read_root_id,
            "workspace_sandbox_decision_id": self.workspace_sandbox_decision_id,
            "shell_network_decision_id": self.shell_network_decision_id,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class SkillExecutionGateDecision:
    gate_decision_id: str
    gate_request_id: str
    skill_id: str
    decision: str
    decision_basis: str
    can_execute: bool
    enforcement_enabled: bool
    enforcement_scope: str
    requires_review: bool
    requires_permission: bool
    finding_ids: list[str]
    reason: str | None
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_decision_id": self.gate_decision_id,
            "gate_request_id": self.gate_request_id,
            "skill_id": self.skill_id,
            "decision": self.decision,
            "decision_basis": self.decision_basis,
            "can_execute": self.can_execute,
            "enforcement_enabled": self.enforcement_enabled,
            "enforcement_scope": self.enforcement_scope,
            "requires_review": self.requires_review,
            "requires_permission": self.requires_permission,
            "finding_ids": list(self.finding_ids),
            "reason": self.reason,
            "created_at": self.created_at,
            "decision_attrs": dict(self.decision_attrs),
        }


@dataclass(frozen=True)
class SkillExecutionGateFinding:
    finding_id: str
    gate_request_id: str
    finding_type: str
    status: str
    severity: str | None
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "gate_request_id": self.gate_request_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class SkillExecutionGateResult:
    gate_result_id: str
    gate_request_id: str
    gate_decision_id: str
    explicit_invocation_result_id: str | None
    status: str
    executed: bool
    blocked: bool
    finding_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_result_id": self.gate_result_id,
            "gate_request_id": self.gate_request_id,
            "gate_decision_id": self.gate_decision_id,
            "explicit_invocation_result_id": self.explicit_invocation_result_id,
            "status": self.status,
            "executed": self.executed,
            "blocked": self.blocked,
            "finding_ids": list(self.finding_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class SkillExecutionGateService:
    def __init__(
        self,
        *,
        explicit_skill_invocation_service: ExplicitSkillInvocationService | Any | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.explicit_skill_invocation_service = explicit_skill_invocation_service
        self.last_policy: ReadOnlyExecutionGatePolicy | None = None
        self.last_request: SkillExecutionGateRequest | None = None
        self.last_decision: SkillExecutionGateDecision | None = None
        self.last_findings: list[SkillExecutionGateFinding] = []
        self.last_result: SkillExecutionGateResult | None = None

    def create_default_policy(self, **policy_attrs: Any) -> ReadOnlyExecutionGatePolicy:
        policy = ReadOnlyExecutionGatePolicy(
            policy_id=new_read_only_execution_gate_policy_id(),
            policy_name="default_read_only_explicit_skill_gate",
            supported_skill_ids=sorted(SUPPORTED_EXPLICIT_SKILL_IDS),
            denied_skill_categories=list(DENIED_SKILL_CATEGORIES),
            requires_permission_for_read_only=bool(
                policy_attrs.pop("requires_permission_for_read_only", False)
            ),
            allow_without_permission_for_read_only=bool(
                policy_attrs.pop("allow_without_permission_for_read_only", True)
            ),
            require_capability_available=bool(policy_attrs.pop("require_capability_available", False)),
            enforce_workspace_boundary=bool(policy_attrs.pop("enforce_workspace_boundary", True)),
            status="active",
            created_at=utc_now_iso(),
            policy_attrs={
                "enforcement_enabled": True,
                "enforcement_scope": "read_only_explicit_skills",
                "permission_grants_created": False,
                **policy_attrs,
            },
        )
        self.last_policy = policy
        self._record(
            "read_only_execution_gate_policy_registered",
            objects=[_object("read_only_execution_gate_policy", policy.policy_id, policy.to_dict())],
            links=[("read_only_execution_gate_policy_object", policy.policy_id)],
            object_links=[],
            attrs={"policy_name": policy.policy_name},
        )
        return policy

    def create_gate_request(
        self,
        *,
        skill_id: str,
        input_payload: dict[str, Any],
        explicit_invocation_request_id: str | None = None,
        invocation_mode: str = "explicit_api",
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        capability_decision_id: str | None = None,
        permission_request_id: str | None = None,
        permission_decision_id: str | None = None,
        session_permission_resolution_id: str | None = None,
        workspace_read_root_id: str | None = None,
        workspace_sandbox_decision_id: str | None = None,
        shell_network_decision_id: str | None = None,
        request_attrs: dict[str, Any] | None = None,
    ) -> SkillExecutionGateRequest:
        request = SkillExecutionGateRequest(
            gate_request_id=new_skill_execution_gate_request_id(),
            explicit_invocation_request_id=explicit_invocation_request_id,
            skill_id=skill_id,
            input_payload_preview=_preview_mapping(input_payload),
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            capability_decision_id=capability_decision_id,
            permission_request_id=permission_request_id,
            permission_decision_id=permission_decision_id,
            session_permission_resolution_id=session_permission_resolution_id,
            workspace_read_root_id=workspace_read_root_id,
            workspace_sandbox_decision_id=workspace_sandbox_decision_id,
            shell_network_decision_id=shell_network_decision_id,
            created_at=utc_now_iso(),
            request_attrs={
                "input_payload": dict(input_payload),
                "explicit_skill_id_required": True,
                "natural_language_routing_used": False,
                "permission_grants_created": False,
                **dict(request_attrs or {}),
            },
        )
        self.last_request = request
        self._record(
            "skill_execution_gate_requested",
            objects=[_object("skill_execution_gate_request", request.gate_request_id, request.to_dict())],
            links=[("skill_execution_gate_request_object", request.gate_request_id)]
            + _reference_links(request),
            object_links=[],
            attrs={"skill_id": request.skill_id, "invocation_mode": request.invocation_mode},
        )
        return request

    def record_finding(
        self,
        *,
        request: SkillExecutionGateRequest,
        finding_type: str,
        status: str,
        message: str,
        subject_ref: str | None = None,
        severity: str | None = "medium",
        finding_attrs: dict[str, Any] | None = None,
    ) -> SkillExecutionGateFinding:
        finding = SkillExecutionGateFinding(
            finding_id=new_skill_execution_gate_finding_id(),
            gate_request_id=request.gate_request_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={
                "permission_grants_created": False,
                **dict(finding_attrs or {}),
            },
        )
        self.last_findings.append(finding)
        self._record(
            "skill_execution_gate_finding_recorded",
            objects=[_object("skill_execution_gate_finding", finding.finding_id, finding.to_dict())],
            links=[
                ("skill_execution_gate_finding_object", finding.finding_id),
                ("skill_execution_gate_request_object", request.gate_request_id),
            ],
            object_links=[(finding.finding_id, request.gate_request_id, "belongs_to_skill_execution_gate_request")],
            attrs={"finding_type": finding.finding_type, "status": finding.status},
        )
        return finding

    def record_decision(
        self,
        *,
        request: SkillExecutionGateRequest,
        decision: str,
        decision_basis: str,
        can_execute: bool,
        findings: list[SkillExecutionGateFinding],
        reason: str | None,
        requires_review: bool = False,
        requires_permission: bool = False,
    ) -> SkillExecutionGateDecision:
        item = SkillExecutionGateDecision(
            gate_decision_id=new_skill_execution_gate_decision_id(),
            gate_request_id=request.gate_request_id,
            skill_id=request.skill_id,
            decision=decision,
            decision_basis=decision_basis,
            can_execute=can_execute,
            enforcement_enabled=True,
            enforcement_scope="read_only_explicit_skills",
            requires_review=requires_review,
            requires_permission=requires_permission,
            finding_ids=[finding.finding_id for finding in findings],
            reason=reason,
            created_at=utc_now_iso(),
            decision_attrs={
                "read_only_skill": request.skill_id in SUPPORTED_EXPLICIT_SKILL_IDS,
                "skill_category": _skill_category(request.skill_id),
                "permission_grants_created": False,
                "natural_language_routing_used": False,
            },
        )
        self.last_decision = item
        event_activity = (
            "skill_execution_gate_allowed"
            if decision == "allow"
            else "skill_execution_gate_needs_review"
            if decision == "needs_review"
            else "skill_execution_gate_denied"
        )
        self._record(
            "skill_execution_gate_decision_recorded",
            objects=[_object("skill_execution_gate_decision", item.gate_decision_id, item.to_dict())],
            links=[
                ("skill_execution_gate_decision_object", item.gate_decision_id),
                ("skill_execution_gate_request_object", request.gate_request_id),
            ]
            + [("skill_execution_gate_finding_object", finding.finding_id) for finding in findings],
            object_links=[(item.gate_decision_id, request.gate_request_id, "decides_skill_execution_gate_request")]
            + [
                (item.gate_decision_id, finding.finding_id, "references_skill_execution_gate_finding")
                for finding in findings
            ],
            attrs={"decision": item.decision, "can_execute": item.can_execute},
        )
        self._record(
            event_activity,
            objects=[_object("skill_execution_gate_decision", item.gate_decision_id, item.to_dict())],
            links=[
                ("skill_execution_gate_decision_object", item.gate_decision_id),
                ("skill_execution_gate_request_object", request.gate_request_id),
            ],
            object_links=[(item.gate_decision_id, request.gate_request_id, "decides_skill_execution_gate_request")],
            attrs={"decision": item.decision, "skill_id": item.skill_id},
        )
        return item

    def record_result(
        self,
        *,
        request: SkillExecutionGateRequest,
        decision: SkillExecutionGateDecision,
        explicit_invocation_result_id: str | None,
        executed: bool,
        blocked: bool,
        findings: list[SkillExecutionGateFinding],
        status: str | None = None,
    ) -> SkillExecutionGateResult:
        result = SkillExecutionGateResult(
            gate_result_id=new_skill_execution_gate_result_id(),
            gate_request_id=request.gate_request_id,
            gate_decision_id=decision.gate_decision_id,
            explicit_invocation_result_id=explicit_invocation_result_id,
            status=status or ("executed" if executed else decision.decision),
            executed=executed,
            blocked=blocked,
            finding_ids=[finding.finding_id for finding in findings],
            created_at=utc_now_iso(),
            result_attrs={
                "enforcement_enabled": True,
                "enforcement_scope": "read_only_explicit_skills",
                "permission_grants_created": False,
                "workspace_write_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
            },
        )
        self.last_result = result
        self._record(
            "skill_execution_gate_result_recorded",
            objects=[_object("skill_execution_gate_result", result.gate_result_id, result.to_dict())],
            links=[
                ("skill_execution_gate_result_object", result.gate_result_id),
                ("skill_execution_gate_request_object", request.gate_request_id),
                ("skill_execution_gate_decision_object", decision.gate_decision_id),
            ]
            + (
                [("explicit_skill_invocation_result_object", explicit_invocation_result_id)]
                if explicit_invocation_result_id
                else []
            ),
            object_links=[
                (result.gate_result_id, request.gate_request_id, "belongs_to_skill_execution_gate_request"),
                (result.gate_result_id, decision.gate_decision_id, "uses_skill_execution_gate_decision"),
            ]
            + (
                [(result.gate_result_id, explicit_invocation_result_id, "references_explicit_invocation_result")]
                if explicit_invocation_result_id
                else []
            ),
            attrs={"status": result.status, "executed": result.executed, "blocked": result.blocked},
        )
        return result

    def evaluate_gate(
        self,
        *,
        request: SkillExecutionGateRequest,
        policy: ReadOnlyExecutionGatePolicy | None = None,
    ) -> SkillExecutionGateDecision:
        active_policy = policy or self.create_default_policy()
        self.last_findings = []
        findings: list[SkillExecutionGateFinding] = []
        category = _skill_category(request.skill_id)
        if not request.skill_id:
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="missing_skill_id",
                    status="failed",
                    severity="high",
                    message="Explicit skill_id is required.",
                    subject_ref=None,
                )
            )
            return self.record_decision(
                request=request,
                decision="deny",
                decision_basis="missing_skill_id",
                can_execute=False,
                findings=findings,
                reason="Explicit skill_id is required.",
            )
        if category in active_policy.denied_skill_categories:
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type=f"{category}_not_allowed",
                    status="failed",
                    severity="high",
                    message=f"{category} skills are outside the read-only execution gate.",
                    subject_ref=request.skill_id,
                )
            )
            return self.record_decision(
                request=request,
                decision="deny",
                decision_basis="unsafe_skill_category",
                can_execute=False,
                findings=findings,
                reason="Only read-only workspace explicit skills can pass this gate.",
            )
        if request.skill_id not in active_policy.supported_skill_ids:
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="unsupported_skill",
                    status="failed",
                    severity="high",
                    message="The skill is not supported by the read-only execution gate.",
                    subject_ref=request.skill_id,
                )
            )
            return self.record_decision(
                request=request,
                decision="unsupported",
                decision_basis="unsupported_skill",
                can_execute=False,
                findings=findings,
                reason="Unsupported skill.",
            )
        if active_policy.require_capability_available and _metadata_denies(request, "capability"):
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="capability_unavailable",
                    status="failed",
                    severity="high",
                    message="Capability metadata indicates the capability is unavailable.",
                    subject_ref=request.capability_decision_id or request.skill_id,
                )
            )
        if _metadata_denies(request, "permission"):
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="permission_denied",
                    status="failed",
                    severity="high",
                    message="Permission decision metadata denies execution.",
                    subject_ref=request.permission_decision_id,
                )
            )
        if _metadata_denies(request, "session_permission"):
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="session_permission_denied",
                    status="failed",
                    severity="high",
                    message="Session permission resolution metadata denies execution.",
                    subject_ref=request.session_permission_resolution_id,
                )
            )
        has_permission_context = bool(
            request.permission_decision_id or request.session_permission_resolution_id
        )
        if not has_permission_context:
            if active_policy.requires_permission_for_read_only:
                findings.append(
                    self.record_finding(
                        request=request,
                        finding_type="permission_context_absent",
                        status="failed",
                        severity="high",
                        message="Policy requires permission context for read-only execution.",
                        subject_ref=request.skill_id,
                    )
                )
            else:
                findings.append(
                    self.record_finding(
                        request=request,
                        finding_type="permission_context_absent",
                        status="warning",
                        severity="medium",
                        message="No permission context was provided; policy allows read-only execution.",
                        subject_ref=request.skill_id,
                    )
                )
        failed_findings = [finding for finding in findings if finding.status == "failed"]
        if failed_findings:
            decision = "needs_review" if active_policy.requires_permission_for_read_only and not has_permission_context else "deny"
            return self.record_decision(
                request=request,
                decision=decision,
                decision_basis=failed_findings[0].finding_type,
                can_execute=False,
                findings=findings,
                reason=failed_findings[0].message,
                requires_review=decision == "needs_review",
                requires_permission=active_policy.requires_permission_for_read_only,
            )
        return self.record_decision(
            request=request,
            decision="allow",
            decision_basis="read_only_workspace_skill_allowed",
            can_execute=True,
            findings=findings,
            reason="Read-only explicit workspace skill passed the execution gate.",
            requires_permission=active_policy.requires_permission_for_read_only,
        )

    def gate_explicit_invocation(
        self,
        *,
        skill_id: str,
        input_payload: dict[str, Any],
        policy: ReadOnlyExecutionGatePolicy | None = None,
        invocation_mode: str = "explicit_api",
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
        capability_decision_id: str | None = None,
        permission_request_id: str | None = None,
        permission_decision_id: str | None = None,
        session_permission_resolution_id: str | None = None,
        workspace_read_root_id: str | None = None,
        workspace_sandbox_decision_id: str | None = None,
        shell_network_decision_id: str | None = None,
        request_attrs: dict[str, Any] | None = None,
    ) -> SkillExecutionGateResult:
        request = self.create_gate_request(
            skill_id=skill_id,
            input_payload=input_payload,
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            capability_decision_id=capability_decision_id,
            permission_request_id=permission_request_id,
            permission_decision_id=permission_decision_id,
            session_permission_resolution_id=session_permission_resolution_id,
            workspace_read_root_id=workspace_read_root_id,
            workspace_sandbox_decision_id=workspace_sandbox_decision_id,
            shell_network_decision_id=shell_network_decision_id,
            request_attrs=request_attrs,
        )
        decision = self.evaluate_gate(request=request, policy=policy)
        findings = list(self.last_findings)
        if not decision.can_execute:
            return self.record_result(
                request=request,
                decision=decision,
                explicit_invocation_result_id=None,
                executed=False,
                blocked=True,
                findings=findings,
                status="blocked" if decision.decision == "deny" else decision.decision,
            )
        invocation_service = self.explicit_skill_invocation_service or ExplicitSkillInvocationService(
            trace_service=self.trace_service
        )
        invocation_result = invocation_service.invoke_explicit_skill(
            skill_id=skill_id,
            input_payload=input_payload,
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
        invocation_result_id = getattr(invocation_result, "result_id", None)
        return self.record_result(
            request=request,
            decision=decision,
            explicit_invocation_result_id=invocation_result_id,
            executed=True,
            blocked=False,
            findings=findings,
            status="executed",
        )

    def render_gate_summary(self, result: SkillExecutionGateResult) -> str:
        lines = [
            "Skill Execution Gate",
            f"status={result.status}",
            f"gate_result_id={result.gate_result_id}",
            f"gate_decision_id={result.gate_decision_id}",
            f"executed={str(result.executed).lower()}",
            f"blocked={str(result.blocked).lower()}",
            f"finding_count={len(result.finding_ids)}",
            "enforcement_scope=read_only_explicit_skills",
            "permission_grants_created=false",
        ]
        if result.explicit_invocation_result_id:
            lines.append(f"explicit_invocation_result_id={result.explicit_invocation_result_id}")
        return "\n".join(lines)

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
                "skill_execution_gate": True,
                "enforcement_enabled": True,
                "enforcement_scope": "read_only_explicit_skills",
                "permission_grants_created": False,
                "natural_language_routing_used": False,
                "shell_execution_used": False,
                "network_access_used": False,
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


def _skill_category(skill_id: str) -> str:
    normalized = skill_id.lower()
    if any(token in normalized for token in ["write", "edit", "delete", "patch", "chmod", "mkdir", "rmdir"]):
        return "write"
    if any(token in normalized for token in ["shell", "bash", "powershell", "cmd"]):
        return "shell"
    if any(token in normalized for token in ["network", "http", "request", "api"]):
        return "network"
    if "mcp" in normalized:
        return "mcp"
    if "plugin" in normalized:
        return "plugin"
    if "external" in normalized:
        return "external_capability"
    if skill_id in SUPPORTED_EXPLICIT_SKILL_IDS:
        return "workspace_read"
    return "unknown"


def _metadata_denies(request: SkillExecutionGateRequest, category: str) -> bool:
    attrs = request.request_attrs
    keys_by_category = {
        "capability": ["capability_available", "capability_status", "capability_decision"],
        "permission": ["permission_decision", "permission_status"],
        "session_permission": ["session_permission_decision", "session_permission_status"],
    }
    for key in keys_by_category[category]:
        if key in attrs and _is_denial(attrs[key]):
            return True
    return False


def _is_denial(value: Any) -> bool:
    if value is False:
        return True
    return str(value).strip().lower() in {"deny", "denied", "unavailable", "blocked", "false"}


def _preview_mapping(value: dict[str, Any], *, max_chars: int = 160) -> dict[str, Any]:
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


def _reference_links(request: SkillExecutionGateRequest) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for qualifier, value in [
        ("explicit_invocation_request", request.explicit_invocation_request_id),
        ("capability_decision", request.capability_decision_id),
        ("permission_request", request.permission_request_id),
        ("permission_decision", request.permission_decision_id),
        ("session_permission_resolution", request.session_permission_resolution_id),
        ("workspace_read_root", request.workspace_read_root_id),
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
