from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.execution import ExecutionEnvelopeService
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.ids import (
    new_reviewed_execution_bridge_decision_id,
    new_reviewed_execution_bridge_request_id,
    new_reviewed_execution_bridge_result_id,
    new_reviewed_execution_bridge_violation_id,
)
from chanta_core.skills.invocation import ExplicitSkillInvocationService
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import (
    SkillProposalReviewDecision,
    SkillProposalReviewResult,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


SUPPORTED_BRIDGE_SKILL_IDS = {
    "skill:list_workspace_files",
    "skill:read_workspace_text_file",
    "skill:summarize_workspace_markdown",
}
DENIED_BRIDGE_SKILL_CATEGORIES = {
    "write",
    "shell",
    "network",
    "mcp",
    "plugin",
    "external_capability",
}


@dataclass(frozen=True)
class ReviewedExecutionBridgeRequest:
    bridge_request_id: str
    proposal_id: str
    review_request_id: str
    review_decision_id: str
    review_result_id: str | None
    skill_id: str
    proposed_input_preview: dict[str, Any]
    approved_input_payload: dict[str, Any]
    invocation_mode: str
    requester_type: str | None
    requester_id: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    status: str
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "bridge_request_id": self.bridge_request_id,
            "proposal_id": self.proposal_id,
            "review_request_id": self.review_request_id,
            "review_decision_id": self.review_decision_id,
            "review_result_id": self.review_result_id,
            "skill_id": self.skill_id,
            "proposed_input_preview": dict(self.proposed_input_preview),
            "approved_input_payload": dict(self.approved_input_payload),
            "invocation_mode": self.invocation_mode,
            "requester_type": self.requester_type,
            "requester_id": self.requester_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "status": self.status,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class ReviewedExecutionBridgeDecision:
    bridge_decision_id: str
    bridge_request_id: str
    proposal_id: str
    review_decision_id: str
    decision: str
    decision_basis: str
    can_bridge: bool
    can_invoke_explicit_skill: bool
    requires_gate: bool
    requires_review: bool
    violation_ids: list[str]
    reason: str | None
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "bridge_decision_id": self.bridge_decision_id,
            "bridge_request_id": self.bridge_request_id,
            "proposal_id": self.proposal_id,
            "review_decision_id": self.review_decision_id,
            "decision": self.decision,
            "decision_basis": self.decision_basis,
            "can_bridge": self.can_bridge,
            "can_invoke_explicit_skill": self.can_invoke_explicit_skill,
            "requires_gate": self.requires_gate,
            "requires_review": self.requires_review,
            "violation_ids": list(self.violation_ids),
            "reason": self.reason,
            "created_at": self.created_at,
            "decision_attrs": dict(self.decision_attrs),
        }


@dataclass(frozen=True)
class ReviewedExecutionBridgeResult:
    bridge_result_id: str
    bridge_request_id: str
    bridge_decision_id: str
    status: str
    explicit_invocation_request_id: str | None
    explicit_invocation_result_id: str | None
    gate_request_id: str | None
    gate_decision_id: str | None
    gate_result_id: str | None
    execution_envelope_id: str | None
    executed: bool
    blocked: bool
    violation_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "bridge_result_id": self.bridge_result_id,
            "bridge_request_id": self.bridge_request_id,
            "bridge_decision_id": self.bridge_decision_id,
            "status": self.status,
            "explicit_invocation_request_id": self.explicit_invocation_request_id,
            "explicit_invocation_result_id": self.explicit_invocation_result_id,
            "gate_request_id": self.gate_request_id,
            "gate_decision_id": self.gate_decision_id,
            "gate_result_id": self.gate_result_id,
            "execution_envelope_id": self.execution_envelope_id,
            "executed": self.executed,
            "blocked": self.blocked,
            "violation_ids": list(self.violation_ids),
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


@dataclass(frozen=True)
class ReviewedExecutionBridgeViolation:
    violation_id: str
    bridge_request_id: str
    proposal_id: str
    review_decision_id: str
    violation_type: str
    severity: str
    message: str
    subject_ref: str | None
    created_at: str
    violation_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "bridge_request_id": self.bridge_request_id,
            "proposal_id": self.proposal_id,
            "review_decision_id": self.review_decision_id,
            "violation_type": self.violation_type,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "violation_attrs": dict(self.violation_attrs),
        }


class ReviewedExecutionBridgeService:
    def __init__(
        self,
        *,
        explicit_skill_invocation_service: ExplicitSkillInvocationService | None = None,
        skill_execution_gate_service: SkillExecutionGateService | None = None,
        execution_envelope_service: ExecutionEnvelopeService | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.explicit_skill_invocation_service = explicit_skill_invocation_service or ExplicitSkillInvocationService(
            trace_service=self.trace_service
        )
        self.skill_execution_gate_service = skill_execution_gate_service or SkillExecutionGateService(
            explicit_skill_invocation_service=self.explicit_skill_invocation_service,
            trace_service=self.trace_service,
        )
        if getattr(self.skill_execution_gate_service, "explicit_skill_invocation_service", None) is None:
            self.skill_execution_gate_service.explicit_skill_invocation_service = (
                self.explicit_skill_invocation_service
            )
        self.execution_envelope_service = execution_envelope_service
        self.last_request: ReviewedExecutionBridgeRequest | None = None
        self.last_decision: ReviewedExecutionBridgeDecision | None = None
        self.last_result: ReviewedExecutionBridgeResult | None = None
        self.last_violations: list[ReviewedExecutionBridgeViolation] = []

    def create_bridge_request(
        self,
        *,
        proposal: SkillInvocationProposal,
        review_decision: SkillProposalReviewDecision,
        review_result: SkillProposalReviewResult | None = None,
        invocation_mode: str = "explicit_api",
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> ReviewedExecutionBridgeRequest:
        approved_payload = review_decision.approved_input_payload or proposal.proposed_input_payload
        request = ReviewedExecutionBridgeRequest(
            bridge_request_id=new_reviewed_execution_bridge_request_id(),
            proposal_id=proposal.proposal_id,
            review_request_id=review_decision.review_request_id,
            review_decision_id=review_decision.review_decision_id,
            review_result_id=review_result.review_result_id if review_result else None,
            skill_id=proposal.skill_id,
            proposed_input_preview=_preview_mapping(proposal.proposed_input_payload),
            approved_input_payload=dict(approved_payload),
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            status="created",
            created_at=utc_now_iso(),
            request_attrs={
                "review_only_source": True,
                "natural_language_routing_used": False,
                "permission_grants_created": False,
                "proposal_missing_inputs": list(proposal.missing_inputs),
                "review_decision": review_decision.decision,
                "review_bridge_candidate": review_result.bridge_candidate if review_result else None,
            },
        )
        self.last_request = request
        self._record(
            "reviewed_execution_bridge_requested",
            objects=[_object("reviewed_execution_bridge_request", request.bridge_request_id, request.to_dict())],
            links=[
                ("reviewed_execution_bridge_request_object", request.bridge_request_id),
                ("skill_invocation_proposal_object", proposal.proposal_id),
                ("skill_proposal_review_decision_object", review_decision.review_decision_id),
            ]
            + (
                [("skill_proposal_review_result_object", review_result.review_result_id)]
                if review_result
                else []
            ),
            object_links=[
                (request.bridge_request_id, proposal.proposal_id, "uses_skill_invocation_proposal"),
                (
                    request.bridge_request_id,
                    review_decision.review_decision_id,
                    "uses_skill_proposal_review_decision",
                ),
            ]
            + (
                [
                    (
                        request.bridge_request_id,
                        review_result.review_result_id,
                        "uses_skill_proposal_review_result",
                    )
                ]
                if review_result
                else []
            ),
            attrs={"skill_id": request.skill_id},
        )
        return request

    def validate_review_for_bridge(
        self,
        *,
        request: ReviewedExecutionBridgeRequest,
        proposal: SkillInvocationProposal,
        review_decision: SkillProposalReviewDecision,
        review_result: SkillProposalReviewResult | None = None,
    ) -> list[ReviewedExecutionBridgeViolation]:
        violations: list[ReviewedExecutionBridgeViolation] = []
        category = _skill_category(proposal.skill_id)
        if review_decision.decision != "approved_for_explicit_invocation":
            violations.append(
                self.record_violation(
                    request=request,
                    proposal=proposal,
                    review_decision=review_decision,
                    violation_type="review_not_approved",
                    severity="high",
                    message="Only approved review decisions can bridge to gated explicit invocation.",
                    subject_ref=review_decision.decision,
                )
            )
        if not review_decision.can_bridge_to_execution:
            violations.append(
                self.record_violation(
                    request=request,
                    proposal=proposal,
                    review_decision=review_decision,
                    violation_type="review_decision_not_bridgeable",
                    severity="high",
                    message="Review decision is not marked as bridgeable.",
                    subject_ref=review_decision.review_decision_id,
                )
            )
        if review_result is not None and not review_result.bridge_candidate:
            violations.append(
                self.record_violation(
                    request=request,
                    proposal=proposal,
                    review_decision=review_decision,
                    violation_type="review_result_not_bridge_candidate",
                    severity="high",
                    message="Review result is not a bridge candidate.",
                    subject_ref=review_result.review_result_id,
                )
            )
        if proposal.missing_inputs:
            violations.append(
                self.record_violation(
                    request=request,
                    proposal=proposal,
                    review_decision=review_decision,
                    violation_type="missing_input",
                    severity="high",
                    message="Proposal still has missing inputs and cannot execute.",
                    subject_ref=",".join(proposal.missing_inputs),
                )
            )
        if category in DENIED_BRIDGE_SKILL_CATEGORIES:
            violations.append(
                self.record_violation(
                    request=request,
                    proposal=proposal,
                    review_decision=review_decision,
                    violation_type=f"{category}_not_supported",
                    severity="high",
                    message="This skill category is not supported by the reviewed execution bridge.",
                    subject_ref=proposal.skill_id,
                    violation_attrs={"skill_category": category},
                )
            )
        elif proposal.skill_id not in SUPPORTED_BRIDGE_SKILL_IDS:
            violations.append(
                self.record_violation(
                    request=request,
                    proposal=proposal,
                    review_decision=review_decision,
                    violation_type="unsupported_skill",
                    severity="high",
                    message="Only read-only workspace skills are supported by the bridge.",
                    subject_ref=proposal.skill_id,
                    violation_attrs={"skill_category": category},
                )
            )
        return violations

    def record_violation(
        self,
        *,
        request: ReviewedExecutionBridgeRequest,
        proposal: SkillInvocationProposal,
        review_decision: SkillProposalReviewDecision,
        violation_type: str,
        severity: str,
        message: str,
        subject_ref: str | None = None,
        violation_attrs: dict[str, Any] | None = None,
    ) -> ReviewedExecutionBridgeViolation:
        violation = ReviewedExecutionBridgeViolation(
            violation_id=new_reviewed_execution_bridge_violation_id(),
            bridge_request_id=request.bridge_request_id,
            proposal_id=proposal.proposal_id,
            review_decision_id=review_decision.review_decision_id,
            violation_type=violation_type,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            violation_attrs={
                "permission_grants_created": False,
                "natural_language_routing_used": False,
                **dict(violation_attrs or {}),
            },
        )
        self.last_violations.append(violation)
        self._record(
            "reviewed_execution_bridge_violation_recorded",
            objects=[
                _object(
                    "reviewed_execution_bridge_violation",
                    violation.violation_id,
                    violation.to_dict(),
                )
            ],
            links=[
                ("reviewed_execution_bridge_violation_object", violation.violation_id),
                ("reviewed_execution_bridge_request_object", request.bridge_request_id),
            ],
            object_links=[
                (violation.violation_id, request.bridge_request_id, "belongs_to_bridge_request")
            ],
            attrs={"violation_type": violation.violation_type, "severity": violation.severity},
        )
        return violation

    def record_decision(
        self,
        *,
        request: ReviewedExecutionBridgeRequest,
        proposal: SkillInvocationProposal,
        review_decision: SkillProposalReviewDecision,
        violations: list[ReviewedExecutionBridgeViolation],
    ) -> ReviewedExecutionBridgeDecision:
        if violations:
            first = next(
                (violation for violation in violations if violation.violation_type == "missing_input"),
                None,
            )
            if first is None:
                first = next(
                    (
                        violation
                        for violation in violations
                        if violation.violation_type.endswith("_not_supported")
                        or violation.violation_type == "unsupported_skill"
                    ),
                    None,
                )
            if first is None:
                first = violations[0]
            if first.violation_type == "missing_input":
                decision = "needs_more_input"
                basis = "missing_input"
            elif first.violation_type.endswith("_not_supported") or first.violation_type == "unsupported_skill":
                decision = "unsupported"
                basis = first.violation_type
            else:
                decision = "deny"
                basis = first.violation_type
            can_bridge = False
            reason = first.message
        else:
            decision = "allow"
            basis = "approved_complete_read_only_review"
            can_bridge = True
            reason = "Approved complete read-only proposal can enter the execution gate."
        item = ReviewedExecutionBridgeDecision(
            bridge_decision_id=new_reviewed_execution_bridge_decision_id(),
            bridge_request_id=request.bridge_request_id,
            proposal_id=proposal.proposal_id,
            review_decision_id=review_decision.review_decision_id,
            decision=decision,
            decision_basis=basis,
            can_bridge=can_bridge,
            can_invoke_explicit_skill=can_bridge,
            requires_gate=can_bridge,
            requires_review=False,
            violation_ids=[violation.violation_id for violation in violations],
            reason=reason,
            created_at=utc_now_iso(),
            decision_attrs={
                "supported_read_only_skill": proposal.skill_id in SUPPORTED_BRIDGE_SKILL_IDS,
                "permission_grants_created": False,
                "natural_language_routing_used": False,
                "direct_skill_execution": False,
            },
        )
        self.last_decision = item
        self._record(
            "reviewed_execution_bridge_decision_recorded",
            objects=[_object("reviewed_execution_bridge_decision", item.bridge_decision_id, item.to_dict())],
            links=[
                ("reviewed_execution_bridge_decision_object", item.bridge_decision_id),
                ("reviewed_execution_bridge_request_object", request.bridge_request_id),
            ]
            + [
                ("reviewed_execution_bridge_violation_object", violation.violation_id)
                for violation in violations
            ],
            object_links=[
                (item.bridge_decision_id, request.bridge_request_id, "decides_bridge_request")
            ],
            attrs={"decision": item.decision, "can_bridge": item.can_bridge},
        )
        self._record(
            "reviewed_execution_bridge_allowed" if item.can_bridge else "reviewed_execution_bridge_denied",
            objects=[_object("reviewed_execution_bridge_decision", item.bridge_decision_id, item.to_dict())],
            links=[
                ("reviewed_execution_bridge_decision_object", item.bridge_decision_id),
                ("reviewed_execution_bridge_request_object", request.bridge_request_id),
            ],
            object_links=[
                (item.bridge_decision_id, request.bridge_request_id, "decides_bridge_request")
            ],
            attrs={"decision": item.decision, "can_bridge": item.can_bridge},
        )
        return item

    def record_result(
        self,
        *,
        request: ReviewedExecutionBridgeRequest,
        decision: ReviewedExecutionBridgeDecision,
        status: str,
        executed: bool,
        blocked: bool,
        explicit_invocation_request_id: str | None = None,
        explicit_invocation_result_id: str | None = None,
        gate_request_id: str | None = None,
        gate_decision_id: str | None = None,
        gate_result_id: str | None = None,
        execution_envelope_id: str | None = None,
        violation_ids: list[str] | None = None,
    ) -> ReviewedExecutionBridgeResult:
        result = ReviewedExecutionBridgeResult(
            bridge_result_id=new_reviewed_execution_bridge_result_id(),
            bridge_request_id=request.bridge_request_id,
            bridge_decision_id=decision.bridge_decision_id,
            status=status,
            explicit_invocation_request_id=explicit_invocation_request_id,
            explicit_invocation_result_id=explicit_invocation_result_id,
            gate_request_id=gate_request_id,
            gate_decision_id=gate_decision_id,
            gate_result_id=gate_result_id,
            execution_envelope_id=execution_envelope_id,
            executed=executed,
            blocked=blocked,
            violation_ids=list(violation_ids or []),
            created_at=utc_now_iso(),
            result_attrs={
                "permission_grants_created": False,
                "natural_language_routing_used": False,
                "direct_skill_execution": False,
                "gate_required": decision.requires_gate,
            },
        )
        self.last_result = result
        self._record(
            "reviewed_execution_bridge_result_recorded",
            objects=[_object("reviewed_execution_bridge_result", result.bridge_result_id, result.to_dict())],
            links=[
                ("reviewed_execution_bridge_result_object", result.bridge_result_id),
                ("reviewed_execution_bridge_request_object", request.bridge_request_id),
                ("reviewed_execution_bridge_decision_object", decision.bridge_decision_id),
            ]
            + _optional_links(
                [
                    ("explicit_skill_invocation_request_object", explicit_invocation_request_id),
                    ("explicit_skill_invocation_result_object", explicit_invocation_result_id),
                    ("skill_execution_gate_request_object", gate_request_id),
                    ("skill_execution_gate_decision_object", gate_decision_id),
                    ("skill_execution_gate_result_object", gate_result_id),
                    ("execution_envelope_object", execution_envelope_id),
                ]
            ),
            object_links=[
                (result.bridge_result_id, request.bridge_request_id, "summarizes_bridge_request")
            ]
            + _optional_object_links(
                result.bridge_result_id,
                [
                    (explicit_invocation_result_id, "references_explicit_skill_invocation_result"),
                    (gate_result_id, "references_skill_execution_gate_result"),
                    (execution_envelope_id, "references_execution_envelope"),
                ],
            ),
            attrs={"status": result.status, "executed": result.executed, "blocked": result.blocked},
        )
        if gate_result_id is not None:
            self._record(
                "reviewed_execution_bridge_gate_completed",
                objects=[
                    _object("reviewed_execution_bridge_result", result.bridge_result_id, result.to_dict())
                ],
                links=[
                    ("reviewed_execution_bridge_result_object", result.bridge_result_id),
                    ("skill_execution_gate_result_object", gate_result_id),
                ],
                object_links=[
                    (result.bridge_result_id, gate_result_id, "references_skill_execution_gate_result")
                ],
                attrs={"status": result.status},
            )
        event_name = (
            "reviewed_execution_bridge_executed"
            if executed
            else "reviewed_execution_bridge_blocked"
        )
        self._record(
            event_name,
            objects=[_object("reviewed_execution_bridge_result", result.bridge_result_id, result.to_dict())],
            links=[("reviewed_execution_bridge_result_object", result.bridge_result_id)],
            object_links=[],
            attrs={"status": result.status, "executed": result.executed, "blocked": result.blocked},
        )
        return result

    def bridge_reviewed_proposal(
        self,
        *,
        proposal: SkillInvocationProposal,
        review_decision: SkillProposalReviewDecision,
        review_result: SkillProposalReviewResult | None = None,
        invocation_mode: str = "explicit_api",
        requester_type: str | None = None,
        requester_id: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> ReviewedExecutionBridgeResult:
        self.last_violations = []
        request = self.create_bridge_request(
            proposal=proposal,
            review_decision=review_decision,
            review_result=review_result,
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )
        violations = self.validate_review_for_bridge(
            request=request,
            proposal=proposal,
            review_decision=review_decision,
            review_result=review_result,
        )
        decision = self.record_decision(
            request=request,
            proposal=proposal,
            review_decision=review_decision,
            violations=violations,
        )
        if not decision.can_bridge:
            return self.record_result(
                request=request,
                decision=decision,
                status="bridge_denied" if decision.decision != "needs_more_input" else "needs_more_input",
                executed=False,
                blocked=True,
                violation_ids=decision.violation_ids,
            )
        self._record(
            "reviewed_execution_bridge_invocation_requested",
            objects=[_object("reviewed_execution_bridge_request", request.bridge_request_id, request.to_dict())],
            links=[("reviewed_execution_bridge_request_object", request.bridge_request_id)],
            object_links=[],
            attrs={"skill_id": request.skill_id},
        )
        gate_result = self.skill_execution_gate_service.gate_explicit_invocation(
            skill_id=request.skill_id,
            input_payload=request.approved_input_payload,
            invocation_mode=invocation_mode,
            requester_type=requester_type,
            requester_id=requester_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            request_attrs={
                "reviewed_execution_bridge": True,
                "proposal_id": proposal.proposal_id,
                "review_decision_id": review_decision.review_decision_id,
                "review_result_id": review_result.review_result_id if review_result else None,
            },
        )
        invocation_result = getattr(self.explicit_skill_invocation_service, "last_result", None)
        envelope_id = None
        if self.execution_envelope_service is not None:
            envelope = self.execution_envelope_service.wrap_gated_invocation_result(
                gate_result=gate_result,
                gate_request=self.skill_execution_gate_service.last_request,
                gate_decision=self.skill_execution_gate_service.last_decision,
                invocation_result=invocation_result,
                invocation_request=self.explicit_skill_invocation_service.last_request,
                invocation_input=self.explicit_skill_invocation_service.last_input,
                proposal_id=proposal.proposal_id,
            )
            envelope_id = envelope.envelope_id
        return self.record_result(
            request=request,
            decision=decision,
            status="bridged_executed" if gate_result.executed else "bridged_blocked",
            explicit_invocation_request_id=getattr(
                self.explicit_skill_invocation_service.last_request,
                "request_id",
                None,
            ),
            explicit_invocation_result_id=gate_result.explicit_invocation_result_id,
            gate_request_id=gate_result.gate_request_id,
            gate_decision_id=gate_result.gate_decision_id,
            gate_result_id=gate_result.gate_result_id,
            execution_envelope_id=envelope_id,
            executed=gate_result.executed,
            blocked=gate_result.blocked,
            violation_ids=decision.violation_ids,
        )

    def render_bridge_summary(self, result: ReviewedExecutionBridgeResult) -> str:
        lines = [
            "Reviewed Execution Bridge",
            f"status={result.status}",
            f"bridge_result_id={result.bridge_result_id}",
            f"bridge_decision_id={result.bridge_decision_id}",
            f"executed={str(result.executed).lower()}",
            f"blocked={str(result.blocked).lower()}",
            f"violation_count={len(result.violation_ids)}",
            "permission_grants_created=false",
            "natural_language_routing_used=false",
        ]
        if result.gate_result_id:
            lines.append(f"gate_result_id={result.gate_result_id}")
        if result.explicit_invocation_result_id:
            lines.append(f"explicit_invocation_result_id={result.explicit_invocation_result_id}")
        if result.execution_envelope_id:
            lines.append(f"execution_envelope_id={result.execution_envelope_id}")
        if self.last_decision is not None:
            lines.append(f"bridge_decision={self.last_decision.decision}")
            lines.append(f"bridge_decision_basis={self.last_decision.decision_basis}")
        if self.last_violations:
            lines.append(f"first_violation_type={self.last_violations[0].violation_type}")
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
                "reviewed_execution_bridge": True,
                "permission_grants_created": False,
                "natural_language_routing_used": False,
                "llm_classifier_used": False,
                "direct_skill_execution": False,
                "shell_execution_used": False,
                "network_access_used": False,
                "workspace_write_used": False,
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


def proposal_from_dict(value: dict[str, Any]) -> SkillInvocationProposal:
    return SkillInvocationProposal(
        proposal_id=str(value["proposal_id"]),
        intent_id=str(value["intent_id"]),
        requirement_id=value.get("requirement_id"),
        skill_id=str(value["skill_id"]),
        proposal_status=str(value.get("proposal_status") or "proposed"),
        invocation_mode=str(value.get("invocation_mode") or "review_only"),
        proposed_input_payload=dict(value.get("proposed_input_payload") or {}),
        missing_inputs=[str(item) for item in value.get("missing_inputs") or []],
        confidence=value.get("confidence"),
        reason=value.get("reason"),
        review_required=bool(value.get("review_required", True)),
        executable_now=bool(value.get("executable_now", False)),
        created_at=str(value.get("created_at") or utc_now_iso()),
        proposal_attrs=dict(value.get("proposal_attrs") or {}),
    )


def review_decision_from_dict(value: dict[str, Any]) -> SkillProposalReviewDecision:
    return SkillProposalReviewDecision(
        review_decision_id=str(value["review_decision_id"]),
        review_request_id=str(value["review_request_id"]),
        proposal_id=str(value["proposal_id"]),
        decision=str(value["decision"]),
        reviewer_type=value.get("reviewer_type"),
        reviewer_id=value.get("reviewer_id"),
        reason=value.get("reason"),
        approved_input_payload=dict(value["approved_input_payload"])
        if isinstance(value.get("approved_input_payload"), dict)
        else None,
        revised_input_payload=dict(value["revised_input_payload"])
        if isinstance(value.get("revised_input_payload"), dict)
        else None,
        requires_explicit_invocation=bool(value.get("requires_explicit_invocation", False)),
        can_bridge_to_execution=bool(value.get("can_bridge_to_execution", False)),
        expires_at=value.get("expires_at"),
        created_at=str(value.get("created_at") or utc_now_iso()),
        decision_attrs=dict(value.get("decision_attrs") or {}),
    )


def review_result_from_dict(value: dict[str, Any]) -> SkillProposalReviewResult:
    return SkillProposalReviewResult(
        review_result_id=str(value["review_result_id"]),
        review_request_id=str(value["review_request_id"]),
        proposal_id=str(value["proposal_id"]),
        decision_id=str(value["decision_id"]),
        finding_ids=[str(item) for item in value.get("finding_ids") or []],
        status=str(value["status"]),
        summary=str(value.get("summary") or ""),
        bridge_candidate=bool(value.get("bridge_candidate", False)),
        created_at=str(value.get("created_at") or utc_now_iso()),
        result_attrs=dict(value.get("result_attrs") or {}),
    )


def load_bridge_inputs_from_json(raw: str) -> tuple[
    SkillInvocationProposal,
    SkillProposalReviewDecision,
    SkillProposalReviewResult | None,
]:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("bridge JSON must be an object")
    if "proposal" in value:
        proposal_value = value["proposal"]
    else:
        proposal_value = value
    if "review_decision" not in value:
        raise ValueError("bridge JSON must include review_decision")
    if not isinstance(proposal_value, dict) or not isinstance(value["review_decision"], dict):
        raise ValueError("proposal and review_decision must be JSON objects")
    review_result_value = value.get("review_result")
    if review_result_value is not None and not isinstance(review_result_value, dict):
        raise ValueError("review_result must be a JSON object when supplied")
    return (
        proposal_from_dict(proposal_value),
        review_decision_from_dict(value["review_decision"]),
        review_result_from_dict(review_result_value) if review_result_value else None,
    )


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
    if skill_id in SUPPORTED_BRIDGE_SKILL_IDS:
        return "workspace_read"
    return "unknown"


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


def _optional_links(items: list[tuple[str, str | None]]) -> list[tuple[str, str]]:
    return [(qualifier, value) for qualifier, value in items if value]


def _optional_object_links(source_id: str, items: list[tuple[str | None, str]]) -> list[tuple[str, str, str]]:
    return [(source_id, value, qualifier) for value, qualifier in items if value]


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
