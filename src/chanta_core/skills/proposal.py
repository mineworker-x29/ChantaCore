from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_skill_invocation_proposal_id,
    new_skill_proposal_decision_id,
    new_skill_proposal_intent_id,
    new_skill_proposal_requirement_id,
    new_skill_proposal_result_id,
    new_skill_proposal_review_note_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


READ_ONLY_PROPOSAL_SKILLS = {
    "workspace_file_list": "skill:list_workspace_files",
    "workspace_file_read": "skill:read_workspace_text_file",
    "workspace_markdown_summary": "skill:summarize_workspace_markdown",
}


@dataclass(frozen=True)
class SkillProposalIntent:
    intent_id: str
    user_prompt_preview: str
    session_id: str | None
    turn_id: str | None
    message_id: str | None
    requested_operation: str
    target_refs: list[dict[str, Any]]
    created_at: str
    intent_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "user_prompt_preview": self.user_prompt_preview,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "message_id": self.message_id,
            "requested_operation": self.requested_operation,
            "target_refs": [dict(item) for item in self.target_refs],
            "created_at": self.created_at,
            "intent_attrs": dict(self.intent_attrs),
        }


@dataclass(frozen=True)
class SkillProposalRequirement:
    requirement_id: str
    intent_id: str
    requirement_type: str
    capability_name: str
    capability_category: str
    required_inputs: list[str]
    missing_inputs: list[str]
    target_type: str | None
    target_ref: str | None
    required_now: bool
    reason: str | None
    created_at: str
    requirement_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "intent_id": self.intent_id,
            "requirement_type": self.requirement_type,
            "capability_name": self.capability_name,
            "capability_category": self.capability_category,
            "required_inputs": list(self.required_inputs),
            "missing_inputs": list(self.missing_inputs),
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "required_now": self.required_now,
            "reason": self.reason,
            "created_at": self.created_at,
            "requirement_attrs": dict(self.requirement_attrs),
        }


@dataclass(frozen=True)
class SkillInvocationProposal:
    proposal_id: str
    intent_id: str
    requirement_id: str | None
    skill_id: str
    proposal_status: str
    invocation_mode: str
    proposed_input_payload: dict[str, Any]
    missing_inputs: list[str]
    confidence: float | None
    reason: str | None
    review_required: bool
    executable_now: bool
    created_at: str
    proposal_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "intent_id": self.intent_id,
            "requirement_id": self.requirement_id,
            "skill_id": self.skill_id,
            "proposal_status": self.proposal_status,
            "invocation_mode": self.invocation_mode,
            "proposed_input_payload": dict(self.proposed_input_payload),
            "missing_inputs": list(self.missing_inputs),
            "confidence": self.confidence,
            "reason": self.reason,
            "review_required": self.review_required,
            "executable_now": self.executable_now,
            "created_at": self.created_at,
            "proposal_attrs": dict(self.proposal_attrs),
        }


@dataclass(frozen=True)
class SkillProposalDecision:
    decision_id: str
    intent_id: str
    proposal_id: str | None
    decision: str
    decision_basis: str
    selected_skill_id: str | None
    can_execute_now: bool
    requires_explicit_invocation: bool
    requires_review: bool
    requires_permission: bool
    reason: str | None
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "intent_id": self.intent_id,
            "proposal_id": self.proposal_id,
            "decision": self.decision,
            "decision_basis": self.decision_basis,
            "selected_skill_id": self.selected_skill_id,
            "can_execute_now": self.can_execute_now,
            "requires_explicit_invocation": self.requires_explicit_invocation,
            "requires_review": self.requires_review,
            "requires_permission": self.requires_permission,
            "reason": self.reason,
            "created_at": self.created_at,
            "decision_attrs": dict(self.decision_attrs),
        }


@dataclass(frozen=True)
class SkillProposalReviewNote:
    review_note_id: str
    intent_id: str
    proposal_id: str | None
    note_type: str
    severity: str | None
    message: str
    created_at: str
    note_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_note_id": self.review_note_id,
            "intent_id": self.intent_id,
            "proposal_id": self.proposal_id,
            "note_type": self.note_type,
            "severity": self.severity,
            "message": self.message,
            "created_at": self.created_at,
            "note_attrs": dict(self.note_attrs),
        }


@dataclass(frozen=True)
class SkillProposalResult:
    result_id: str
    intent_id: str
    proposal_ids: list[str]
    decision_ids: list[str]
    review_note_ids: list[str]
    status: str
    summary: str
    suggested_cli_command: str | None
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "intent_id": self.intent_id,
            "proposal_ids": list(self.proposal_ids),
            "decision_ids": list(self.decision_ids),
            "review_note_ids": list(self.review_note_ids),
            "status": self.status,
            "summary": self.summary,
            "suggested_cli_command": self.suggested_cli_command,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class SkillProposalRouterService:
    def __init__(
        self,
        *,
        capability_decision_service: Any | None = None,
        explicit_skill_invocation_service: Any | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.capability_decision_service = capability_decision_service
        self.explicit_skill_invocation_service = explicit_skill_invocation_service
        self.last_intent: SkillProposalIntent | None = None
        self.last_requirements: list[SkillProposalRequirement] = []
        self.last_proposals: list[SkillInvocationProposal] = []
        self.last_decisions: list[SkillProposalDecision] = []
        self.last_review_notes: list[SkillProposalReviewNote] = []
        self.last_result: SkillProposalResult | None = None

    def create_intent(
        self,
        *,
        user_prompt: str,
        session_id: str | None = None,
        turn_id: str | None = None,
        message_id: str | None = None,
    ) -> SkillProposalIntent:
        operation = _detect_operation(user_prompt)
        target_ref = _detect_relative_path(user_prompt)
        target_refs = [{"target_type": "relative_path", "target_ref": target_ref}] if target_ref else []
        intent = SkillProposalIntent(
            intent_id=new_skill_proposal_intent_id(),
            user_prompt_preview=user_prompt[:300],
            session_id=session_id,
            turn_id=turn_id,
            message_id=message_id,
            requested_operation=operation,
            target_refs=target_refs,
            created_at=utc_now_iso(),
            intent_attrs={
                "deterministic_heuristic": True,
                "llm_classifier_used": False,
                "skills_executed": False,
                "permission_grants_created": False,
                "private_source_read": False,
            },
        )
        self.last_intent = intent
        self._record(
            "skill_proposal_intent_created",
            objects=[_object("skill_proposal_intent", intent.intent_id, intent.to_dict())],
            links=[("skill_proposal_intent_object", intent.intent_id)],
            object_links=[],
            attrs={"requested_operation": intent.requested_operation},
        )
        return intent

    def extract_requirements(
        self,
        *,
        intent: SkillProposalIntent,
        root_path: str | None = None,
        relative_path: str | None = None,
        recursive: bool | None = None,
    ) -> list[SkillProposalRequirement]:
        operation = intent.requested_operation
        category_by_operation = {
            "workspace_file_list": "workspace_read",
            "workspace_file_read": "workspace_read",
            "workspace_markdown_summary": "workspace_read",
            "workspace_file_write": "workspace_write",
            "shell_execution": "shell",
            "network_access": "network",
            "mcp_connection": "mcp",
            "plugin_loading": "plugin",
            "external_capability_use": "external_capability",
        }
        required_inputs = ["root_path"] if operation in READ_ONLY_PROPOSAL_SKILLS else []
        target_ref = relative_path or _first_target_ref(intent)
        if operation in {"workspace_file_read", "workspace_markdown_summary"}:
            required_inputs.append("relative_path")
        missing_inputs: list[str] = []
        if "root_path" in required_inputs and not root_path:
            missing_inputs.append("root_path")
        if "relative_path" in required_inputs and not target_ref:
            missing_inputs.append("relative_path")
        requirement = SkillProposalRequirement(
            requirement_id=new_skill_proposal_requirement_id(),
            intent_id=intent.intent_id,
            requirement_type="capability_requirement",
            capability_name=operation,
            capability_category=category_by_operation.get(operation, "unknown"),
            required_inputs=required_inputs,
            missing_inputs=missing_inputs,
            target_type="relative_path" if target_ref else None,
            target_ref=target_ref,
            required_now=True,
            reason=_requirement_reason(operation),
            created_at=utc_now_iso(),
            requirement_attrs={
                "recursive": bool(recursive),
                "deterministic_heuristic": True,
                "proposal_only": True,
            },
        )
        self.last_requirements = [requirement]
        self._record(
            "skill_proposal_requirement_recorded",
            objects=[_object("skill_proposal_requirement", requirement.requirement_id, requirement.to_dict())],
            links=[
                ("skill_proposal_requirement_object", requirement.requirement_id),
                ("skill_proposal_intent_object", intent.intent_id),
            ],
            object_links=[(requirement.requirement_id, intent.intent_id, "belongs_to_skill_proposal_intent")],
            attrs={
                "capability_category": requirement.capability_category,
                "missing_input_count": len(requirement.missing_inputs),
            },
        )
        return [requirement]

    def propose_skill_for_requirement(
        self,
        *,
        intent: SkillProposalIntent,
        requirement: SkillProposalRequirement,
        root_path: str | None = None,
        relative_path: str | None = None,
        recursive: bool | None = None,
    ) -> SkillInvocationProposal:
        skill_id = READ_ONLY_PROPOSAL_SKILLS.get(intent.requested_operation)
        target_ref = relative_path or requirement.target_ref
        payload: dict[str, Any] = {}
        if skill_id:
            payload["root_path"] = root_path or "<ROOT_PATH>"
            if intent.requested_operation == "workspace_file_list":
                payload["relative_path"] = target_ref or "."
                if recursive is not None:
                    payload["recursive"] = bool(recursive)
            else:
                payload["relative_path"] = target_ref or "<RELATIVE_PATH>"
        proposal_status = "unsupported"
        reason = "The requested operation is outside the read-only workspace proposal set."
        confidence = 0.2
        if skill_id and requirement.missing_inputs:
            proposal_status = "incomplete"
            reason = "Required input must be supplied before explicit invocation can be reviewed."
            confidence = 0.74
        elif skill_id:
            proposal_status = "proposed"
            reason = "A read-only workspace skill can be proposed for explicit invocation review."
            confidence = 0.86
        proposal = SkillInvocationProposal(
            proposal_id=new_skill_invocation_proposal_id(),
            intent_id=intent.intent_id,
            requirement_id=requirement.requirement_id,
            skill_id=skill_id or f"unsupported:{intent.requested_operation}",
            proposal_status=proposal_status,
            invocation_mode="review_only",
            proposed_input_payload=payload,
            missing_inputs=list(requirement.missing_inputs),
            confidence=confidence,
            reason=reason,
            review_required=True,
            executable_now=False,
            created_at=utc_now_iso(),
            proposal_attrs={
                "proposal_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                "suggested_cli_command_preview_only": True,
            },
        )
        self.last_proposals = [proposal]
        self._record(
            "skill_invocation_proposal_created",
            objects=[_object("skill_invocation_proposal", proposal.proposal_id, proposal.to_dict())],
            links=[
                ("skill_invocation_proposal_object", proposal.proposal_id),
                ("skill_proposal_intent_object", intent.intent_id),
                ("skill_proposal_requirement_object", requirement.requirement_id),
            ],
            object_links=[
                (proposal.proposal_id, intent.intent_id, "belongs_to_skill_proposal_intent"),
                (proposal.proposal_id, requirement.requirement_id, "addresses_skill_proposal_requirement"),
            ],
            attrs={"proposal_status": proposal.proposal_status, "skill_id": proposal.skill_id},
        )
        return proposal

    def decide_proposal(
        self,
        *,
        intent: SkillProposalIntent,
        proposal: SkillInvocationProposal,
    ) -> SkillProposalDecision:
        if proposal.proposal_status == "proposed":
            decision = "propose_explicit_invocation"
            basis = "supported_read_only_skill"
            reason = "Reviewable explicit invocation proposal is available."
            requires_explicit = True
        elif proposal.proposal_status == "incomplete":
            decision = "needs_more_input"
            basis = "missing_required_input"
            reason = "Required input is missing."
            requires_explicit = True
        else:
            decision = "unsupported_capability"
            basis = "unsupported_skill_family"
            reason = "This operation is not supported by the proposal router."
            requires_explicit = False
        item = SkillProposalDecision(
            decision_id=new_skill_proposal_decision_id(),
            intent_id=intent.intent_id,
            proposal_id=proposal.proposal_id,
            decision=decision,
            decision_basis=basis,
            selected_skill_id=proposal.skill_id if proposal.skill_id.startswith("skill:") else None,
            can_execute_now=False,
            requires_explicit_invocation=requires_explicit,
            requires_review=True,
            requires_permission=False,
            reason=reason,
            created_at=utc_now_iso(),
            decision_attrs={
                "deterministic_heuristic": True,
                "proposal_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
            },
        )
        self.last_decisions = [item]
        self._record(
            "skill_proposal_decision_recorded",
            objects=[_object("skill_proposal_decision", item.decision_id, item.to_dict())],
            links=[
                ("skill_proposal_decision_object", item.decision_id),
                ("skill_invocation_proposal_object", proposal.proposal_id),
                ("skill_proposal_intent_object", intent.intent_id),
            ],
            object_links=[
                (item.decision_id, intent.intent_id, "belongs_to_skill_proposal_intent"),
                (item.decision_id, proposal.proposal_id, "belongs_to_skill_invocation_proposal"),
            ],
            attrs={"decision": item.decision, "can_execute_now": item.can_execute_now},
        )
        return item

    def record_review_note(
        self,
        *,
        intent: SkillProposalIntent,
        proposal: SkillInvocationProposal | None,
        note_type: str,
        message: str,
        severity: str | None = "medium",
        note_attrs: dict[str, Any] | None = None,
    ) -> SkillProposalReviewNote:
        note = SkillProposalReviewNote(
            review_note_id=new_skill_proposal_review_note_id(),
            intent_id=intent.intent_id,
            proposal_id=proposal.proposal_id if proposal else None,
            note_type=note_type,
            severity=severity,
            message=message,
            created_at=utc_now_iso(),
            note_attrs={
                "proposal_only": True,
                "skills_executed": False,
                **dict(note_attrs or {}),
            },
        )
        self.last_review_notes.append(note)
        links = [
            ("skill_proposal_review_note_object", note.review_note_id),
            ("skill_proposal_intent_object", intent.intent_id),
        ]
        object_links = [(note.review_note_id, intent.intent_id, "belongs_to_skill_proposal_intent")]
        if proposal:
            links.append(("skill_invocation_proposal_object", proposal.proposal_id))
            object_links.append(
                (note.review_note_id, proposal.proposal_id, "belongs_to_skill_invocation_proposal")
            )
        self._record(
            "skill_proposal_review_note_recorded",
            objects=[_object("skill_proposal_review_note", note.review_note_id, note.to_dict())],
            links=links,
            object_links=object_links,
            attrs={"note_type": note.note_type, "severity": note.severity or ""},
        )
        return note

    def build_proposal_result(
        self,
        *,
        intent: SkillProposalIntent,
        proposals: list[SkillInvocationProposal],
        decisions: list[SkillProposalDecision],
        review_notes: list[SkillProposalReviewNote],
    ) -> SkillProposalResult:
        proposal = proposals[0] if proposals else None
        decision = decisions[0] if decisions else None
        if not proposal:
            status = "no_proposal"
        elif proposal.proposal_status == "proposed":
            status = "proposal_available"
        elif proposal.proposal_status == "incomplete":
            status = "incomplete"
        elif proposal.proposal_status == "unsupported":
            status = "unsupported"
        else:
            status = "needs_review"
        suggested = self.render_suggested_cli_command(proposal) if proposal and proposal.skill_id.startswith("skill:") else None
        summary = _result_summary(status, proposal, decision, review_notes)
        result = SkillProposalResult(
            result_id=new_skill_proposal_result_id(),
            intent_id=intent.intent_id,
            proposal_ids=[item.proposal_id for item in proposals],
            decision_ids=[item.decision_id for item in decisions],
            review_note_ids=[item.review_note_id for item in review_notes],
            status=status,
            summary=summary,
            suggested_cli_command=suggested,
            created_at=utc_now_iso(),
            result_attrs={
                "proposal_only": True,
                "skills_executed": False,
                "permission_grants_created": False,
                "llm_classifier_used": False,
            },
        )
        self.last_result = result
        self._record(
            "skill_proposal_result_recorded",
            objects=[_object("skill_proposal_result", result.result_id, result.to_dict())],
            links=[
                ("skill_proposal_result_object", result.result_id),
                ("skill_proposal_intent_object", intent.intent_id),
            ]
            + [("skill_invocation_proposal_object", item.proposal_id) for item in proposals]
            + [("skill_proposal_decision_object", item.decision_id) for item in decisions]
            + [("skill_proposal_review_note_object", item.review_note_id) for item in review_notes],
            object_links=[(result.result_id, intent.intent_id, "belongs_to_skill_proposal_intent")]
            + [(result.result_id, item.proposal_id, "includes_skill_invocation_proposal") for item in proposals]
            + [(result.result_id, item.decision_id, "includes_skill_proposal_decision") for item in decisions]
            + [(result.result_id, item.review_note_id, "includes_skill_proposal_review_note") for item in review_notes],
            attrs={"status": result.status, "proposal_count": len(proposals)},
        )
        return result

    def propose_from_prompt(
        self,
        *,
        user_prompt: str,
        root_path: str | None = None,
        relative_path: str | None = None,
        recursive: bool | None = None,
        session_id: str | None = None,
        turn_id: str | None = None,
        message_id: str | None = None,
    ) -> SkillProposalResult:
        self.last_review_notes = []
        intent = self.create_intent(
            user_prompt=user_prompt,
            session_id=session_id,
            turn_id=turn_id,
            message_id=message_id,
        )
        requirements = self.extract_requirements(
            intent=intent,
            root_path=root_path,
            relative_path=relative_path,
            recursive=recursive,
        )
        proposal = self.propose_skill_for_requirement(
            intent=intent,
            requirement=requirements[0],
            root_path=root_path,
            relative_path=relative_path,
            recursive=recursive,
        )
        decision = self.decide_proposal(intent=intent, proposal=proposal)
        notes: list[SkillProposalReviewNote] = []
        if proposal.missing_inputs:
            for missing in proposal.missing_inputs:
                notes.append(
                    self.record_review_note(
                        intent=intent,
                        proposal=proposal,
                        note_type="missing_input",
                        severity="medium",
                        message=f"{missing} is required before explicit invocation review.",
                        note_attrs={"missing_input": missing},
                    )
                )
        if proposal.proposal_status == "unsupported":
            notes.append(
                self.record_review_note(
                    intent=intent,
                    proposal=proposal,
                    note_type="unsupported_operation",
                    severity="high",
                    message="The requested operation is not supported by the proposal router.",
                )
            )
        if proposal.proposal_status in {"proposed", "incomplete"}:
            notes.append(
                self.record_review_note(
                    intent=intent,
                    proposal=proposal,
                    note_type="explicit_invocation_required",
                    severity="medium",
                    message="The proposal is review-only and must be executed separately by explicit invocation.",
                )
            )
        return self.build_proposal_result(
            intent=intent,
            proposals=[proposal],
            decisions=[decision],
            review_notes=notes,
        )

    def render_proposal_summary(self, result: SkillProposalResult) -> str:
        lines = [
            "Skill Proposal Router",
            f"status={result.status}",
            f"result_id={result.result_id}",
            f"summary={result.summary}",
            "skills_executed=false",
            "permission_grants_created=false",
            "llm_classifier_used=false",
        ]
        if result.suggested_cli_command:
            lines.append(f"suggested_cli_command={result.suggested_cli_command}")
        self._record(
            "skill_proposal_rendered",
            objects=[_object("skill_proposal_result", result.result_id, result.to_dict())],
            links=[("skill_proposal_result_object", result.result_id)],
            object_links=[],
            attrs={"status": result.status},
        )
        return "\n".join(lines)

    def render_suggested_cli_command(self, proposal: SkillInvocationProposal | None) -> str | None:
        if proposal is None or not proposal.skill_id.startswith("skill:"):
            return None
        payload = json.dumps(proposal.proposed_input_payload, ensure_ascii=False, sort_keys=True)
        escaped_payload = payload.replace('"', '\\"')
        return f'chanta-cli skill run {proposal.skill_id} --input-json "{escaped_payload}"'

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
                "skill_proposal": True,
                "proposal_only": True,
                "skills_executed": False,
                "llm_classifier_used": False,
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


def _detect_operation(user_prompt: str) -> str:
    text = user_prompt.lower()
    if any(token in text for token in ["write file", "edit file", "delete file", "파일 수정", "파일 삭제"]):
        return "workspace_file_write"
    if any(token in text for token in ["shell", "bash", "powershell", "cmd", "명령어 실행"]):
        return "shell_execution"
    if any(token in text for token in ["http://", "https://", "api 호출", "웹 요청"]):
        return "network_access"
    if "mcp" in text:
        return "mcp_connection"
    if any(token in text for token in ["plugin", "플러그인"]):
        return "plugin_loading"
    if any(token in text for token in ["external capability", "external tool"]):
        return "external_capability_use"
    if any(token in text for token in ["summarize markdown", "md 요약", "문서 요약", "heading", ".md 요약"]):
        return "workspace_markdown_summary"
    if any(token in text for token in ["list files", "show files", "파일 목록", "디렉토리", "폴더 안"]):
        return "workspace_file_list"
    if any(token in text for token in ["read file", "파일 읽", ".md", ".txt", "open this file", "show contents"]):
        return "workspace_file_read"
    return "unknown"


def _detect_relative_path(user_prompt: str) -> str | None:
    match = re.search(r"([A-Za-z0-9_.\-/]+[.](?:md|markdown|txt))", user_prompt)
    if match:
        return match.group(1).strip("/\\")
    return None


def _first_target_ref(intent: SkillProposalIntent) -> str | None:
    for item in intent.target_refs:
        if item.get("target_type") == "relative_path" and item.get("target_ref"):
            return str(item["target_ref"])
    return None


def _requirement_reason(operation: str) -> str:
    if operation in READ_ONLY_PROPOSAL_SKILLS:
        return "Read-only workspace skill may satisfy the request after explicit review."
    if operation == "unknown":
        return "No supported proposal target was detected."
    return "The operation is outside the current proposal router boundary."


def _result_summary(
    status: str,
    proposal: SkillInvocationProposal | None,
    decision: SkillProposalDecision | None,
    review_notes: list[SkillProposalReviewNote],
) -> str:
    if proposal and decision:
        return (
            f"{status}: {proposal.skill_id}; decision={decision.decision}; "
            f"review_notes={len(review_notes)}."
        )
    return f"{status}: no proposal generated."


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
