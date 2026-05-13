from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_skill_proposal_review_contract_id,
    new_skill_proposal_review_decision_id,
    new_skill_proposal_review_finding_id,
    new_skill_proposal_review_request_id,
    new_skill_proposal_review_result_id,
)
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


READ_ONLY_REVIEW_SKILL_IDS = {
    "skill:list_workspace_files",
    "skill:read_workspace_text_file",
    "skill:summarize_workspace_markdown",
}
DENIED_REVIEW_SKILL_CATEGORIES = [
    "write",
    "shell",
    "network",
    "mcp",
    "plugin",
    "external_capability",
]
ALLOWED_REVIEW_DECISIONS = [
    "approved_for_explicit_invocation",
    "rejected",
    "needs_more_input",
    "revise_proposal",
    "no_action",
    "needs_review",
    "error",
]


@dataclass(frozen=True)
class SkillProposalReviewContract:
    contract_id: str
    contract_name: str
    contract_type: str
    description: str
    allowed_decisions: list[str]
    supported_skill_ids: list[str]
    denied_skill_categories: list[str]
    require_explicit_reviewer: bool
    require_reason_for_approval: bool
    require_reason_for_rejection: bool
    status: str
    created_at: str
    updated_at: str
    contract_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "contract_name": self.contract_name,
            "contract_type": self.contract_type,
            "description": self.description,
            "allowed_decisions": list(self.allowed_decisions),
            "supported_skill_ids": list(self.supported_skill_ids),
            "denied_skill_categories": list(self.denied_skill_categories),
            "require_explicit_reviewer": self.require_explicit_reviewer,
            "require_reason_for_approval": self.require_reason_for_approval,
            "require_reason_for_rejection": self.require_reason_for_rejection,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "contract_attrs": dict(self.contract_attrs),
        }


@dataclass(frozen=True)
class SkillProposalReviewRequest:
    review_request_id: str
    contract_id: str
    proposal_id: str
    intent_id: str
    requirement_id: str | None
    skill_id: str
    proposed_input_preview: dict[str, Any]
    missing_inputs: list[str]
    requested_by: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    status: str
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_request_id": self.review_request_id,
            "contract_id": self.contract_id,
            "proposal_id": self.proposal_id,
            "intent_id": self.intent_id,
            "requirement_id": self.requirement_id,
            "skill_id": self.skill_id,
            "proposed_input_preview": dict(self.proposed_input_preview),
            "missing_inputs": list(self.missing_inputs),
            "requested_by": self.requested_by,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "status": self.status,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class SkillProposalReviewDecision:
    review_decision_id: str
    review_request_id: str
    proposal_id: str
    decision: str
    reviewer_type: str | None
    reviewer_id: str | None
    reason: str | None
    approved_input_payload: dict[str, Any] | None
    revised_input_payload: dict[str, Any] | None
    requires_explicit_invocation: bool
    can_bridge_to_execution: bool
    expires_at: str | None
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_decision_id": self.review_decision_id,
            "review_request_id": self.review_request_id,
            "proposal_id": self.proposal_id,
            "decision": self.decision,
            "reviewer_type": self.reviewer_type,
            "reviewer_id": self.reviewer_id,
            "reason": self.reason,
            "approved_input_payload": dict(self.approved_input_payload)
            if self.approved_input_payload is not None
            else None,
            "revised_input_payload": dict(self.revised_input_payload)
            if self.revised_input_payload is not None
            else None,
            "requires_explicit_invocation": self.requires_explicit_invocation,
            "can_bridge_to_execution": self.can_bridge_to_execution,
            "expires_at": self.expires_at,
            "created_at": self.created_at,
            "decision_attrs": dict(self.decision_attrs),
        }


@dataclass(frozen=True)
class SkillProposalReviewFinding:
    finding_id: str
    review_request_id: str
    proposal_id: str
    finding_type: str
    status: str
    severity: str
    message: str
    subject_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "review_request_id": self.review_request_id,
            "proposal_id": self.proposal_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class SkillProposalReviewResult:
    review_result_id: str
    review_request_id: str
    proposal_id: str
    decision_id: str
    finding_ids: list[str]
    status: str
    summary: str
    bridge_candidate: bool
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_result_id": self.review_result_id,
            "review_request_id": self.review_request_id,
            "proposal_id": self.proposal_id,
            "decision_id": self.decision_id,
            "finding_ids": list(self.finding_ids),
            "status": self.status,
            "summary": self.summary,
            "bridge_candidate": self.bridge_candidate,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class SkillProposalReviewService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.last_contract: SkillProposalReviewContract | None = None
        self.last_request: SkillProposalReviewRequest | None = None
        self.last_findings: list[SkillProposalReviewFinding] = []
        self.last_decision: SkillProposalReviewDecision | None = None
        self.last_result: SkillProposalReviewResult | None = None

    def create_default_contract(self, **contract_attrs: Any) -> SkillProposalReviewContract:
        now = utc_now_iso()
        contract = SkillProposalReviewContract(
            contract_id=new_skill_proposal_review_contract_id(),
            contract_name="default_read_only_skill_proposal_review_contract",
            contract_type="human_in_the_loop_skill_proposal_review",
            description=(
                "Review read-only skill proposals without executing them or granting permissions."
            ),
            allowed_decisions=list(ALLOWED_REVIEW_DECISIONS),
            supported_skill_ids=sorted(READ_ONLY_REVIEW_SKILL_IDS),
            denied_skill_categories=list(DENIED_REVIEW_SKILL_CATEGORIES),
            require_explicit_reviewer=bool(
                contract_attrs.pop("require_explicit_reviewer", True)
            ),
            require_reason_for_approval=bool(
                contract_attrs.pop("require_reason_for_approval", True)
            ),
            require_reason_for_rejection=bool(
                contract_attrs.pop("require_reason_for_rejection", False)
            ),
            status="active",
            created_at=now,
            updated_at=now,
            contract_attrs={
                "review_only": True,
                "skills_executed": False,
                "execution_bridge_created": False,
                "permission_grants_created": False,
                "no_action_allowed": True,
                **contract_attrs,
            },
        )
        self.last_contract = contract
        self._record(
            "skill_proposal_review_contract_registered",
            objects=[
                _object(
                    "skill_proposal_review_contract",
                    contract.contract_id,
                    contract.to_dict(),
                )
            ],
            links=[("skill_proposal_review_contract_object", contract.contract_id)],
            object_links=[],
            attrs={"contract_name": contract.contract_name},
        )
        return contract

    def create_review_request(
        self,
        *,
        proposal: SkillInvocationProposal,
        contract: SkillProposalReviewContract | None = None,
        requested_by: str | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> SkillProposalReviewRequest:
        active_contract = contract or self.create_default_contract()
        request = SkillProposalReviewRequest(
            review_request_id=new_skill_proposal_review_request_id(),
            contract_id=active_contract.contract_id,
            proposal_id=proposal.proposal_id,
            intent_id=proposal.intent_id,
            requirement_id=proposal.requirement_id,
            skill_id=proposal.skill_id,
            proposed_input_preview=_preview_mapping(proposal.proposed_input_payload),
            missing_inputs=list(proposal.missing_inputs),
            requested_by=requested_by,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
            status="created",
            created_at=utc_now_iso(),
            request_attrs={
                "proposal_status": proposal.proposal_status,
                "review_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                "proposed_input_payload": dict(proposal.proposed_input_payload),
            },
        )
        self.last_request = request
        self._record(
            "skill_proposal_review_requested",
            objects=[_object("skill_proposal_review_request", request.review_request_id, request.to_dict())],
            links=[
                ("skill_proposal_review_request_object", request.review_request_id),
                ("skill_invocation_proposal_object", proposal.proposal_id),
                ("skill_proposal_review_contract_object", active_contract.contract_id),
            ],
            object_links=[
                (request.review_request_id, proposal.proposal_id, "reviews_skill_invocation_proposal"),
                (request.review_request_id, active_contract.contract_id, "uses_review_contract"),
            ],
            attrs={"skill_id": request.skill_id, "missing_input_count": len(request.missing_inputs)},
        )
        return request

    def record_finding(
        self,
        *,
        request: SkillProposalReviewRequest,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        subject_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> SkillProposalReviewFinding:
        finding = SkillProposalReviewFinding(
            finding_id=new_skill_proposal_review_finding_id(),
            review_request_id=request.review_request_id,
            proposal_id=request.proposal_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={
                "review_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                **dict(finding_attrs or {}),
            },
        )
        self.last_findings.append(finding)
        self._record(
            "skill_proposal_review_finding_recorded",
            objects=[_object("skill_proposal_review_finding", finding.finding_id, finding.to_dict())],
            links=[
                ("skill_proposal_review_finding_object", finding.finding_id),
                ("skill_proposal_review_request_object", request.review_request_id),
            ],
            object_links=[
                (finding.finding_id, request.review_request_id, "belongs_to_review_request")
            ],
            attrs={"finding_type": finding.finding_type, "status": finding.status},
        )
        return finding

    def record_decision(
        self,
        *,
        request: SkillProposalReviewRequest,
        decision: str,
        reviewer_type: str | None = None,
        reviewer_id: str | None = None,
        reason: str | None = None,
        approved_input_payload: dict[str, Any] | None = None,
        revised_input_payload: dict[str, Any] | None = None,
        requires_explicit_invocation: bool = False,
        can_bridge_to_execution: bool = False,
        expires_at: str | None = None,
        decision_attrs: dict[str, Any] | None = None,
    ) -> SkillProposalReviewDecision:
        item = SkillProposalReviewDecision(
            review_decision_id=new_skill_proposal_review_decision_id(),
            review_request_id=request.review_request_id,
            proposal_id=request.proposal_id,
            decision=decision,
            reviewer_type=reviewer_type,
            reviewer_id=reviewer_id,
            reason=reason,
            approved_input_payload=dict(approved_input_payload) if approved_input_payload else None,
            revised_input_payload=dict(revised_input_payload) if revised_input_payload else None,
            requires_explicit_invocation=requires_explicit_invocation,
            can_bridge_to_execution=can_bridge_to_execution,
            expires_at=expires_at,
            created_at=utc_now_iso(),
            decision_attrs={
                "review_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                "execution_bridge_created": False,
                **dict(decision_attrs or {}),
            },
        )
        self.last_decision = item
        self._record(
            "skill_proposal_review_decision_recorded",
            objects=[_object("skill_proposal_review_decision", item.review_decision_id, item.to_dict())],
            links=[
                ("skill_proposal_review_decision_object", item.review_decision_id),
                ("skill_proposal_review_request_object", request.review_request_id),
            ],
            object_links=[
                (item.review_decision_id, request.review_request_id, "decides_review_request")
            ],
            attrs={
                "decision": item.decision,
                "can_bridge_to_execution": item.can_bridge_to_execution,
            },
        )
        return item

    def record_result(
        self,
        *,
        request: SkillProposalReviewRequest,
        decision: SkillProposalReviewDecision,
        findings: list[SkillProposalReviewFinding],
        status: str,
        summary: str,
        bridge_candidate: bool,
    ) -> SkillProposalReviewResult:
        result = SkillProposalReviewResult(
            review_result_id=new_skill_proposal_review_result_id(),
            review_request_id=request.review_request_id,
            proposal_id=request.proposal_id,
            decision_id=decision.review_decision_id,
            finding_ids=[finding.finding_id for finding in findings],
            status=status,
            summary=summary,
            bridge_candidate=bridge_candidate,
            created_at=utc_now_iso(),
            result_attrs={
                "review_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                "execution_bridge_created": False,
                "requires_explicit_invocation": decision.requires_explicit_invocation,
            },
        )
        self.last_result = result
        self._record(
            "skill_proposal_review_result_recorded",
            objects=[_object("skill_proposal_review_result", result.review_result_id, result.to_dict())],
            links=[
                ("skill_proposal_review_result_object", result.review_result_id),
                ("skill_proposal_review_request_object", request.review_request_id),
                ("skill_proposal_review_decision_object", decision.review_decision_id),
            ]
            + [
                ("skill_proposal_review_finding_object", finding.finding_id)
                for finding in findings
            ],
            object_links=[
                (result.review_result_id, request.review_request_id, "summarizes_review_request"),
                (result.review_result_id, decision.review_decision_id, "references_decision"),
            ]
            + [
                (result.review_result_id, finding.finding_id, "references_review_finding")
                for finding in findings
            ],
            attrs={"status": result.status, "bridge_candidate": result.bridge_candidate},
        )
        if status == "approved":
            self._record_status_event("skill_proposal_review_approved", result=result, request=request)
        elif status == "rejected":
            self._record_status_event("skill_proposal_review_rejected", result=result, request=request)
        elif status == "no_action":
            self._record_status_event(
                "skill_proposal_review_no_action_selected",
                result=result,
                request=request,
            )
        elif status == "needs_more_input":
            self._record_status_event(
                "skill_proposal_review_needs_more_input",
                result=result,
                request=request,
            )
        return result

    def review_proposal(
        self,
        *,
        proposal: SkillInvocationProposal,
        decision: str,
        reviewer_type: str | None = None,
        reviewer_id: str | None = None,
        reason: str | None = None,
        approved_input_payload: dict[str, Any] | None = None,
        revised_input_payload: dict[str, Any] | None = None,
        contract: SkillProposalReviewContract | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        process_instance_id: str | None = None,
    ) -> SkillProposalReviewResult:
        active_contract = contract or self.create_default_contract()
        self.last_findings = []
        request = self.create_review_request(
            proposal=proposal,
            contract=active_contract,
            requested_by=reviewer_id,
            session_id=session_id,
            turn_id=turn_id,
            process_instance_id=process_instance_id,
        )
        normalized_decision = normalize_review_decision(decision)
        findings: list[SkillProposalReviewFinding] = []
        skill_category = _skill_category(proposal.skill_id)
        supported = proposal.skill_id in active_contract.supported_skill_ids
        complete = not proposal.missing_inputs
        status = normalized_decision
        bridge_candidate = False
        requires_explicit = normalized_decision == "approved_for_explicit_invocation"

        if normalized_decision not in active_contract.allowed_decisions:
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="invalid_decision",
                    status="failed",
                    severity="high",
                    message="Review decision is not allowed by the active contract.",
                    subject_ref=normalized_decision,
                )
            )
            status = "error"
            normalized_decision = "error"
            requires_explicit = False
        if active_contract.require_explicit_reviewer and not (reviewer_type or reviewer_id):
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="explicit_reviewer_required",
                    status="failed",
                    severity="high",
                    message="An explicit reviewer is required by the active contract.",
                    subject_ref=request.review_request_id,
                )
            )
            if status == "approved_for_explicit_invocation":
                status = "needs_review"
                requires_explicit = False
        if (
            normalized_decision == "approved_for_explicit_invocation"
            and active_contract.require_reason_for_approval
            and not str(reason or "").strip()
        ):
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="approval_reason_required",
                    status="failed",
                    severity="high",
                    message="A reason is required to approve a proposal for explicit invocation.",
                    subject_ref=request.review_request_id,
                )
            )
            status = "needs_review"
            requires_explicit = False
        if (
            normalized_decision == "rejected"
            and active_contract.require_reason_for_rejection
            and not str(reason or "").strip()
        ):
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="rejection_reason_required",
                    status="failed",
                    severity="medium",
                    message="A reason is required to reject this proposal.",
                    subject_ref=request.review_request_id,
                )
            )
            status = "needs_review"
        if skill_category in active_contract.denied_skill_categories:
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type=f"{skill_category}_not_supported",
                    status="failed",
                    severity="high",
                    message="This skill category is outside the proposal review contract.",
                    subject_ref=proposal.skill_id,
                    finding_attrs={"skill_category": skill_category},
                )
            )
            if normalized_decision != "no_action":
                status = "rejected"
                requires_explicit = False
        elif not supported:
            findings.append(
                self.record_finding(
                    request=request,
                    finding_type="unsupported_skill",
                    status="failed",
                    severity="high",
                    message="The proposal skill is not supported by the review contract.",
                    subject_ref=proposal.skill_id,
                    finding_attrs={"skill_category": skill_category},
                )
            )
            if normalized_decision != "no_action":
                status = "rejected"
                requires_explicit = False
        if proposal.missing_inputs:
            for missing in proposal.missing_inputs:
                findings.append(
                    self.record_finding(
                        request=request,
                        finding_type="missing_input",
                        status="failed",
                        severity="high",
                        message=f"{missing} is required before explicit invocation can be reviewed.",
                        subject_ref=missing,
                    )
                )
            if normalized_decision == "approved_for_explicit_invocation":
                status = "needs_more_input"
                requires_explicit = False

        if normalized_decision == "no_action":
            status = "no_action"
            requires_explicit = False
        elif normalized_decision == "needs_more_input":
            status = "needs_more_input"
            requires_explicit = False
        elif normalized_decision == "needs_review" and status == "needs_review":
            requires_explicit = False
        elif normalized_decision == "needs_review" and not findings:
            status = "needs_review"
            requires_explicit = False
        elif normalized_decision == "revise_proposal" and not findings:
            status = "revise_proposal"
            requires_explicit = False
        elif normalized_decision == "rejected" and status == "rejected":
            requires_explicit = False
        elif normalized_decision == "approved_for_explicit_invocation" and not findings:
            status = "approved"
            bridge_candidate = supported and complete
            requires_explicit = True
        elif normalized_decision == "error":
            status = "error"
            requires_explicit = False

        if status != "approved":
            bridge_candidate = False
        decision_item = self.record_decision(
            request=request,
            decision=normalized_decision,
            reviewer_type=reviewer_type,
            reviewer_id=reviewer_id,
            reason=reason,
            approved_input_payload=approved_input_payload or proposal.proposed_input_payload,
            revised_input_payload=revised_input_payload,
            requires_explicit_invocation=requires_explicit,
            can_bridge_to_execution=bridge_candidate,
            decision_attrs={
                "supported_skill": supported,
                "complete_proposal": complete,
                "skill_category": skill_category,
            },
        )
        return self.record_result(
            request=request,
            decision=decision_item,
            findings=findings,
            status=status,
            summary=_result_summary(
                status=status,
                decision=normalized_decision,
                skill_id=proposal.skill_id,
                finding_count=len(findings),
                bridge_candidate=bridge_candidate,
            ),
            bridge_candidate=bridge_candidate,
        )

    def render_review_summary(self, result: SkillProposalReviewResult) -> str:
        lines = [
            "Skill Proposal Review",
            f"status={result.status}",
            f"review_result_id={result.review_result_id}",
            f"review_request_id={result.review_request_id}",
            f"decision_id={result.decision_id}",
            f"bridge_candidate={str(result.bridge_candidate).lower()}",
            f"finding_count={len(result.finding_ids)}",
            "skills_executed=false",
            "permission_grants_created=false",
            "execution_gate_called=false",
            "explicit_invocation_called=false",
            f"summary={result.summary}",
        ]
        if self.last_decision is not None:
            lines.append(f"decision={self.last_decision.decision}")
            lines.append(
                f"requires_explicit_invocation={str(self.last_decision.requires_explicit_invocation).lower()}"
            )
        if self.last_findings:
            lines.append(f"first_finding_type={self.last_findings[0].finding_type}")
        return "\n".join(lines)

    def _record_status_event(
        self,
        activity: str,
        *,
        result: SkillProposalReviewResult,
        request: SkillProposalReviewRequest,
    ) -> None:
        self._record(
            activity,
            objects=[_object("skill_proposal_review_result", result.review_result_id, result.to_dict())],
            links=[
                ("skill_proposal_review_result_object", result.review_result_id),
                ("skill_proposal_review_request_object", request.review_request_id),
            ],
            object_links=[
                (result.review_result_id, request.review_request_id, "summarizes_review_request")
            ],
            attrs={"status": result.status, "bridge_candidate": result.bridge_candidate},
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
                "skill_proposal_review": True,
                "review_only": True,
                "skills_executed": False,
                "explicit_invocation_called": False,
                "execution_gate_called": False,
                "permission_grants_created": False,
                "llm_classifier_used": False,
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


def normalize_review_decision(value: str) -> str:
    normalized = str(value or "").strip().lower().replace("-", "_")
    aliases = {
        "approve": "approved_for_explicit_invocation",
        "approved": "approved_for_explicit_invocation",
        "approved_for_invocation": "approved_for_explicit_invocation",
        "reject": "rejected",
        "revise": "revise_proposal",
        "more_input": "needs_more_input",
        "needs_more_input": "needs_more_input",
        "needs_review": "needs_review",
        "no_action": "no_action",
        "error": "error",
    }
    return aliases.get(normalized, normalized)


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


def proposal_from_json(raw: str) -> SkillInvocationProposal:
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise ValueError("proposal JSON must be an object")
    return proposal_from_dict(value)


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
    if skill_id in READ_ONLY_REVIEW_SKILL_IDS:
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


def _result_summary(
    *,
    status: str,
    decision: str,
    skill_id: str,
    finding_count: int,
    bridge_candidate: bool,
) -> str:
    return (
        f"{status}: skill_id={skill_id}; decision={decision}; "
        f"findings={finding_count}; bridge_candidate={str(bridge_candidate).lower()}."
    )


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
