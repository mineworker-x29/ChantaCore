from __future__ import annotations

from typing import Any
from uuid import uuid4

from chanta_core.capabilities.ids import (
    new_capability_decision_evidence_id,
    new_capability_decision_id,
    new_capability_decision_surface_id,
    new_capability_request_intent_id,
    new_capability_requirement_id,
)
from chanta_core.capabilities.models import (
    CapabilityDecision,
    CapabilityDecisionEvidence,
    CapabilityDecisionSurface,
    CapabilityRequestIntent,
    CapabilityRequirement,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.runtime.capability_contract import (
    AgentCapabilityProfile,
    RuntimeCapabilityIntrospectionService,
    RuntimeCapabilitySnapshot,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


class CapabilityDecisionSurfaceService:
    def __init__(self, *, trace_service: TraceService | None = None) -> None:
        self.trace_service = trace_service or TraceService()
        self.last_intent: CapabilityRequestIntent | None = None
        self.last_requirements: list[CapabilityRequirement] = []
        self.last_decisions: list[CapabilityDecision] = []
        self.last_evidence: list[CapabilityDecisionEvidence] = []
        self.last_surface: CapabilityDecisionSurface | None = None

    def create_request_intent(
        self,
        user_prompt: str,
        *,
        session_id: str | None = None,
        turn_id: str | None = None,
        message_id: str | None = None,
        intent_attrs: dict[str, Any] | None = None,
    ) -> CapabilityRequestIntent:
        operation, targets = _detect_operation_and_targets(user_prompt)
        intent = CapabilityRequestIntent(
            intent_id=new_capability_request_intent_id(),
            session_id=session_id,
            turn_id=turn_id,
            message_id=message_id,
            user_prompt_preview=_preview(user_prompt),
            requested_operation=operation,
            target_refs=targets,
            inferred_requirement_ids=[],
            created_at=utc_now_iso(),
            intent_attrs={
                "deterministic_extraction": True,
                "uses_llm_classifier": False,
                **dict(intent_attrs or {}),
            },
        )
        self.last_intent = intent
        self._record(
            "capability_request_intent_created",
            objects=[_object("capability_request_intent", intent.intent_id, intent.to_dict())],
            links=[("intent_object", intent.intent_id), *_session_links(session_id, turn_id, message_id)],
            object_links=[],
            attrs={"requested_operation": operation},
        )
        return intent

    def extract_requirements(
        self,
        intent: CapabilityRequestIntent,
    ) -> list[CapabilityRequirement]:
        specs = _requirements_for_operation(
            operation=intent.requested_operation,
            target_refs=intent.target_refs,
            prompt_preview=intent.user_prompt_preview,
        )
        requirements = [
            CapabilityRequirement(
                requirement_id=new_capability_requirement_id(),
                requirement_type=spec["requirement_type"],
                capability_name=spec["capability_name"],
                capability_category=spec["capability_category"],
                target_type=spec.get("target_type"),
                target_ref=spec.get("target_ref"),
                required_now=bool(spec.get("required_now", True)),
                reason=spec.get("reason"),
                created_at=utc_now_iso(),
                requirement_attrs={
                    "deterministic_extraction": True,
                    "source_intent_id": intent.intent_id,
                },
            )
            for spec in specs
        ]
        self.last_requirements = requirements
        for requirement in requirements:
            self._record(
                "capability_requirement_recorded",
                objects=[
                    _object(
                        "capability_requirement",
                        requirement.requirement_id,
                        requirement.to_dict(),
                    )
                ],
                links=[
                    ("requirement_object", requirement.requirement_id),
                    ("intent_object", intent.intent_id),
                ],
                object_links=[
                    (
                        requirement.requirement_id,
                        intent.intent_id,
                        "inferred_from_intent",
                    )
                ],
                attrs={
                    "capability_name": requirement.capability_name,
                    "capability_category": requirement.capability_category,
                },
            )
        return requirements

    def decide_requirement(
        self,
        intent: CapabilityRequestIntent,
        requirement: CapabilityRequirement,
        *,
        capability_snapshot: RuntimeCapabilitySnapshot | None = None,
        agent_profile: AgentCapabilityProfile | None = None,
    ) -> tuple[CapabilityDecision, CapabilityDecisionEvidence]:
        snapshot = capability_snapshot or (
            agent_profile.snapshot if agent_profile is not None else None
        )
        if snapshot is None:
            snapshot = RuntimeCapabilityIntrospectionService().build_default_agent_snapshot()
        availability, mode, reason = _decide_availability(requirement, snapshot)
        evidence = CapabilityDecisionEvidence(
            evidence_id=new_capability_decision_evidence_id(),
            decision_id=None,
            evidence_type="runtime_capability_snapshot",
            source_kind="runtime_capability_snapshot",
            source_ref=snapshot.snapshot_id,
            content=reason,
            created_at=utc_now_iso(),
            evidence_attrs={
                "capability_category": requirement.capability_category,
                "snapshot_agent_id": snapshot.agent_id,
            },
        )
        decision = CapabilityDecision(
            decision_id=new_capability_decision_id(),
            intent_id=intent.intent_id,
            requirement_id=requirement.requirement_id,
            capability_name=requirement.capability_name,
            availability=availability,
            can_execute_now=availability == "available_now",
            requires_review=availability in {"requires_review", "disabled_candidate"},
            requires_permission=availability == "requires_permission",
            reason=reason,
            recommended_response=_recommended_response(availability, mode),
            evidence_ids=[evidence.evidence_id],
            created_at=utc_now_iso(),
            decision_attrs={
                "recommended_agent_mode": mode,
                "executes_operation": False,
                "uses_llm_classifier": False,
            },
        )
        evidence = CapabilityDecisionEvidence(
            **{**evidence.to_dict(), "decision_id": decision.decision_id}
        )
        self._record_evidence(evidence, decision_id=decision.decision_id)
        self._record_decision(decision, requirement=requirement, evidence=evidence)
        return decision, evidence

    def build_decision_surface(
        self,
        user_prompt: str,
        *,
        session_id: str | None = None,
        turn_id: str | None = None,
        message_id: str | None = None,
        capability_snapshot: RuntimeCapabilitySnapshot | None = None,
        agent_profile: AgentCapabilityProfile | None = None,
    ) -> CapabilityDecisionSurface:
        snapshot = capability_snapshot or (
            agent_profile.snapshot if agent_profile is not None else None
        )
        if snapshot is None:
            snapshot = RuntimeCapabilityIntrospectionService().build_default_agent_snapshot()
        intent = self.create_request_intent(
            user_prompt,
            session_id=session_id,
            turn_id=turn_id,
            message_id=message_id,
        )
        requirements = self.extract_requirements(intent)
        decisions: list[CapabilityDecision] = []
        evidence_items: list[CapabilityDecisionEvidence] = []
        for requirement in requirements:
            decision, evidence = self.decide_requirement(
                intent,
                requirement,
                capability_snapshot=snapshot,
                agent_profile=agent_profile,
            )
            decisions.append(decision)
            evidence_items.append(evidence)
        overall = _overall_availability(decisions)
        mode = _surface_mode(overall, decisions)
        surface = CapabilityDecisionSurface(
            surface_id=new_capability_decision_surface_id(),
            session_id=session_id,
            turn_id=turn_id,
            message_id=message_id,
            capability_snapshot_id=snapshot.snapshot_id,
            intent_id=intent.intent_id,
            decision_ids=[decision.decision_id for decision in decisions],
            overall_availability=overall,
            can_fulfill_now=all(decision.can_execute_now for decision in decisions),
            recommended_agent_mode=mode,
            limitation_summary=_limitation_summary(overall, decisions),
            created_at=utc_now_iso(),
            surface_attrs={
                "read_model_only": True,
                "executes_operation": False,
                "uses_llm_classifier": False,
                "requirement_count": len(requirements),
            },
        )
        self.last_intent = intent
        self.last_requirements = requirements
        self.last_decisions = decisions
        self.last_evidence = evidence_items
        self.last_surface = surface
        self._record_surface(surface, intent=intent, decisions=decisions)
        if not surface.can_fulfill_now:
            self._record(
                "capability_limitation_detected",
                objects=[_object("capability_decision_surface", surface.surface_id, surface.to_dict())],
                links=[("surface_object", surface.surface_id)],
                object_links=[],
                attrs={
                    "overall_availability": surface.overall_availability,
                    "recommended_agent_mode": surface.recommended_agent_mode,
                },
            )
            self._record(
                "capability_request_unfulfillable",
                objects=[_object("capability_decision_surface", surface.surface_id, surface.to_dict())],
                links=[("surface_object", surface.surface_id)],
                object_links=[],
                attrs={"overall_availability": surface.overall_availability},
            )
        return surface

    def render_decision_surface_block(
        self,
        surface: CapabilityDecisionSurface,
        decisions: list[CapabilityDecision] | None = None,
    ) -> str:
        decision_items = decisions if decisions is not None else self.last_decisions
        lines = [
            "Runtime capability decision surface:",
            f"- overall_availability: {surface.overall_availability}",
            f"- can_fulfill_now: {surface.can_fulfill_now}",
            f"- recommended_agent_mode: {surface.recommended_agent_mode}",
        ]
        if surface.limitation_summary:
            lines.append(f"- limitation: {surface.limitation_summary}")
        for decision in decision_items:
            lines.append(
                "- decision: "
                f"{decision.capability_name} -> {decision.availability}; "
                f"can_execute_now={decision.can_execute_now}; "
                f"reason={decision.reason or 'none'}"
            )
        lines.append(
            "Use this surface as prompt guidance only. Do not execute tools, read files, "
            "call network resources, connect MCP, load plugins, or create permissions."
        )
        return "\n".join(lines)

    def _record_evidence(
        self,
        evidence: CapabilityDecisionEvidence,
        *,
        decision_id: str,
    ) -> None:
        self._record(
            "capability_decision_evidence_recorded",
            objects=[
                _object(
                    "capability_decision_evidence",
                    evidence.evidence_id,
                    evidence.to_dict(),
                )
            ],
            links=[("evidence_object", evidence.evidence_id), ("decision_object", decision_id)],
            object_links=[(evidence.evidence_id, decision_id, "supports_decision")],
            attrs={"evidence_type": evidence.evidence_type},
        )

    def _record_decision(
        self,
        decision: CapabilityDecision,
        *,
        requirement: CapabilityRequirement,
        evidence: CapabilityDecisionEvidence,
    ) -> None:
        self._record(
            "capability_decision_recorded",
            objects=[
                _object("capability_decision", decision.decision_id, decision.to_dict())
            ],
            links=[
                ("decision_object", decision.decision_id),
                ("requirement_object", requirement.requirement_id),
                ("evidence_object", evidence.evidence_id),
            ],
            object_links=[
                (
                    decision.decision_id,
                    requirement.requirement_id,
                    "decides_requirement",
                ),
                (decision.decision_id, evidence.evidence_id, "supported_by_evidence"),
            ],
            attrs={
                "availability": decision.availability,
                "can_execute_now": decision.can_execute_now,
            },
        )

    def _record_surface(
        self,
        surface: CapabilityDecisionSurface,
        *,
        intent: CapabilityRequestIntent,
        decisions: list[CapabilityDecision],
    ) -> None:
        self._record(
            "capability_decision_surface_created",
            objects=[
                _object(
                    "capability_decision_surface",
                    surface.surface_id,
                    surface.to_dict(),
                )
            ],
            links=[
                ("surface_object", surface.surface_id),
                ("intent_object", intent.intent_id),
                *_session_links(surface.session_id, surface.turn_id, surface.message_id),
                *[("decision_object", decision.decision_id) for decision in decisions],
            ],
            object_links=[
                (surface.surface_id, intent.intent_id, "evaluates_intent"),
                *[
                    (surface.surface_id, decision.decision_id, "includes_decision")
                    for decision in decisions
                ],
            ],
            attrs={
                "overall_availability": surface.overall_availability,
                "can_fulfill_now": surface.can_fulfill_now,
            },
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
                "capability_decision_read_model": True,
            },
        )
        relations = [
            OCELRelation.event_object(
                event_id=event.event_id,
                object_id=object_id,
                qualifier=qualifier,
            )
            for qualifier, object_id in links
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(
                source_object_id=source_id,
                target_object_id=target_id,
                qualifier=qualifier,
            )
            for source_id, target_id, qualifier in object_links
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(
            OCELRecord(event=event, objects=objects, relations=relations)
        )


def _detect_operation_and_targets(prompt: str) -> tuple[str, list[dict[str, Any]]]:
    text = prompt.casefold()
    targets = _extract_targets(prompt)
    if _has_any(text, ["external capability", "외부 capability", "외부 기능 실행"]):
        return "external_capability_use", targets
    if _has_any(text, ["external ocel", "ocel import", "ocel merge", "외부 ocel"]):
        return "external_ocel_import", targets
    if _has_any(text, ["write", "edit", "delete", "수정", "삭제", "저장", "써줘"]):
        return "workspace_file_write", targets
    if _has_any(text, ["powershell", "bash", "command", "명령어", "실행"]):
        return "shell_execution", targets
    if "http://" in text or "https://" in text or _has_any(text, ["api call", "호출"]):
        return "network_access", targets
    if "mcp" in text:
        return "mcp_connection", targets
    if _has_any(text, ["plugin", "플러그인"]):
        return "plugin_loading", targets
    if _has_any(text, ["registry update", "runtime registry", "런타임 레지스트리"]):
        return "runtime_registry_update", targets
    if _has_any(text, ["방금", "이전 대화", "아까", "previous conversation"]):
        return "session_context", targets
    if _has_any(text, ["read", "읽어", "markdown", ".md", "personal directory", "directory", "폴더"]):
        return "workspace_file_read", targets
    if _has_any(text, ["뭘 할 수", "무엇을 할 수", "what can you do", "할 수 있어"]):
        return "chat", targets
    return "chat", targets


def _requirements_for_operation(
    *,
    operation: str,
    target_refs: list[dict[str, Any]],
    prompt_preview: str,
) -> list[dict[str, Any]]:
    target = target_refs[0] if target_refs else {}
    target_ref = target.get("ref")
    mapping = {
        "chat": [
            ("chat_response", "skill:llm_chat", "llm_chat"),
            ("bounded_session_context", "session_context_projection", "session_context"),
        ],
        "session_context": [
            ("bounded_session_context", "session_context_projection", "session_context")
        ],
        "workspace_file_read": [
            ("workspace_file_read", "workspace file read", "workspace")
        ],
        "workspace_file_write": [
            ("workspace_file_write", "workspace file write", "workspace")
        ],
        "shell_execution": [("shell_execution", "shell execution", "shell")],
        "network_access": [("network_access", "network access", "network")],
        "mcp_connection": [("mcp_connection", "MCP connection", "mcp")],
        "plugin_loading": [("plugin_loading", "plugin loading", "plugin")],
        "external_capability_use": [
            ("external_capability_use", "external capability execution", "external_capability")
        ],
        "external_ocel_import": [
            ("external_ocel_import", "external OCEL import candidate", "external_ocel")
        ],
        "runtime_registry_update": [
            ("runtime_registry_update", "runtime registry update", "tool_dispatch")
        ],
    }
    specs = mapping.get(operation) or [("unknown", "unknown capability", "unknown")]
    return [
        {
            "requirement_type": requirement_type,
            "capability_name": capability_name,
            "capability_category": category,
            "target_type": target.get("type"),
            "target_ref": target_ref,
            "required_now": True,
            "reason": f"Extracted from prompt preview: {prompt_preview}",
        }
        for requirement_type, capability_name, category in specs
    ]


def _decide_availability(
    requirement: CapabilityRequirement,
    snapshot: RuntimeCapabilitySnapshot,
) -> tuple[str, str, str]:
    category = requirement.capability_category
    name = requirement.capability_name
    if category == "llm_chat":
        return "available_now", "answer_with_llm", "skill:llm_chat is available_now."
    if category == "session_context":
        available = _contains(snapshot.available_now, "session context") or _contains(
            snapshot.available_now, "OCEL/session"
        )
        if available:
            return (
                "available_now",
                "answer_with_llm",
                "Bounded OCEL session context projection is available.",
            )
        return (
            "metadata_only",
            "state_limitation",
            "Session context appears as metadata/read-model only in the snapshot.",
        )
    if category == "workspace" and "read" in name:
        return (
            "requires_explicit_skill",
            "requires_explicit_skill",
            "Workspace file read exists only through explicit root-constrained read-only skills, not ambient chat.",
        )
    if category == "workspace":
        return (
            "requires_permission",
            "requires_permission",
            "Workspace file write requires explicit permission and reviewed skill.",
        )
    if category == "shell":
        return (
            "requires_permission",
            "requires_permission",
            "Shell execution requires explicit permission and is not executed here.",
        )
    if category == "network":
        return (
            "requires_permission",
            "requires_permission",
            "Network access requires explicit permission and is not executed here.",
        )
    if category == "mcp":
        return (
            "not_implemented",
            "state_limitation",
            "MCP descriptors may be metadata-only, but MCP connection is not implemented.",
        )
    if category == "plugin":
        return (
            "not_implemented",
            "state_limitation",
            "Plugin descriptors may be metadata-only, but plugin loading is not implemented.",
        )
    if category == "external_capability":
        return (
            "disabled_candidate",
            "requires_review",
            "Imported external capabilities remain disabled candidates requiring review.",
        )
    if category == "external_ocel":
        return (
            "requires_review",
            "requires_review",
            "External OCEL import candidates are metadata/review records only.",
        )
    if category == "tool_dispatch":
        return (
            "not_implemented",
            "requires_review",
            "Runtime registry updates are not implemented in this decision surface.",
        )
    return "unknown", "unknown", "No deterministic capability match was found."


def _overall_availability(decisions: list[CapabilityDecision]) -> str:
    priority = [
        "not_implemented",
        "requires_permission",
        "requires_explicit_skill",
        "disabled_candidate",
        "requires_review",
        "metadata_only",
        "unknown",
        "available_now",
    ]
    available = {decision.availability for decision in decisions}
    for item in priority:
        if item in available:
            return item
    return "unknown"


def _surface_mode(overall: str, decisions: list[CapabilityDecision]) -> str:
    if overall == "available_now":
        return "answer_with_llm"
    if overall == "requires_explicit_skill":
        return "requires_explicit_skill"
    if overall == "requires_permission":
        if any("workspace file read" in decision.capability_name for decision in decisions):
            return "ask_for_pasted_content"
        return "requires_permission"
    if overall in {"requires_review", "disabled_candidate"}:
        return "requires_review"
    if overall in {"metadata_only", "not_implemented"}:
        return "state_limitation"
    return "unknown"


def _limitation_summary(overall: str, decisions: list[CapabilityDecision]) -> str | None:
    if overall == "available_now":
        return None
    reasons = [decision.reason for decision in decisions if not decision.can_execute_now and decision.reason]
    return " ".join(reasons[:2]) if reasons else "Requested capability is not available now."


def _recommended_response(availability: str, mode: str) -> str:
    if availability == "available_now":
        return "Answer using the current LLM chat path."
    if mode == "ask_for_pasted_content":
        return "State that direct file reading is unavailable and ask for pasted content."
    if availability == "requires_permission":
        return "State the permission boundary; do not execute the operation."
    if availability == "requires_explicit_skill":
        return "State that workspace read requires an explicit root-constrained read-only skill path."
    if availability in {"requires_review", "disabled_candidate"}:
        return "State that this requires review and is not active."
    if availability in {"metadata_only", "not_implemented"}:
        return "State the limitation clearly and avoid claiming execution capability."
    return "State uncertainty and avoid claiming unsupported capability."


def _extract_targets(prompt: str) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    for token in prompt.replace("\\", "/").split():
        if token.endswith(".md") or token.startswith("/"):
            targets.append({"type": "path_hint", "ref": token.strip(".,;:")})
        elif token.startswith("http://") or token.startswith("https://"):
            targets.append({"type": "url", "ref": token.strip(".,;:")})
    return targets


def _preview(text: str, limit: int = 240) -> str:
    compact = " ".join(text.split())
    return compact[:limit]


def _has_any(text: str, needles: list[str]) -> bool:
    return any(needle.casefold() in text for needle in needles)


def _contains(items: list[str], needle: str) -> bool:
    return any(needle.casefold() in item.casefold() for item in items)


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


def _session_links(
    session_id: str | None,
    turn_id: str | None,
    message_id: str | None,
) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    if session_id:
        links.append(("session_context", session_id if session_id.startswith("session:") else f"session:{session_id}"))
    if turn_id:
        links.append(("turn_context", turn_id))
    if message_id:
        links.append(("message_object", message_id))
    return links
