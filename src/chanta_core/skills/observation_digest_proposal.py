from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.observation_digest import DIGESTION_SKILL_IDS, OBSERVATION_SKILL_IDS
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_observation_digest_intent_candidate_id,
    new_observation_digest_proposal_binding_id,
    new_observation_digest_proposal_finding_id,
    new_observation_digest_proposal_policy_id,
    new_observation_digest_proposal_result_id,
    new_observation_digest_proposal_set_id,
    new_skill_invocation_proposal_id,
)
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.registry_view import SkillRegistryViewService
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


OBSERVATION_DIGESTION_SKILL_IDS = [*OBSERVATION_SKILL_IDS, *DIGESTION_SKILL_IDS]

INTENT_TO_SKILLS: dict[str, list[str]] = {
    "agent_observation_source_inspect": ["skill:agent_observation_source_inspect"],
    "agent_trace_observation": ["skill:agent_trace_observe"],
    "agent_observation_normalization": ["skill:agent_observation_normalize"],
    "agent_behavior_inference": ["skill:agent_behavior_infer"],
    "agent_process_narrative": ["skill:agent_process_narrative"],
    "external_skill_source_inspection": ["skill:external_skill_source_inspect"],
    "external_skill_static_digest": ["skill:external_skill_static_digest"],
    "external_behavior_fingerprint": ["skill:external_behavior_fingerprint"],
    "external_skill_assimilation": ["skill:external_skill_assimilate"],
    "external_skill_adapter_mapping": ["skill:external_skill_adapter_candidate"],
}

REQUIRED_INPUTS_BY_SKILL_ID: dict[str, list[str]] = {
    "skill:agent_observation_source_inspect": ["root_path", "relative_path", "source_runtime_hint_or_format_hint"],
    "skill:agent_trace_observe": ["root_path", "relative_path", "source_runtime", "format_hint"],
    "skill:agent_observation_normalize": ["observation_batch_id_or_raw_records"],
    "skill:agent_behavior_infer": ["observed_run_id"],
    "skill:agent_process_narrative": ["observed_run_id_or_inference_id"],
    "skill:external_skill_source_inspect": ["root_path", "relative_path", "vendor_hint"],
    "skill:external_skill_static_digest": ["source_descriptor_id_or_root_path_relative_path"],
    "skill:external_behavior_fingerprint": ["observed_run_id"],
    "skill:external_skill_assimilate": ["static_profile_id_or_behavior_fingerprint_id"],
    "skill:external_skill_adapter_candidate": ["assimilation_candidate_id_or_source_skill_ref"],
}


@dataclass(frozen=True)
class ObservationDigestProposalPolicy:
    policy_id: str
    policy_name: str
    allowed_skill_layers: list[str]
    allowed_skill_ids: list[str]
    denied_skill_ids: list[str]
    allow_multi_step_proposal: bool
    allow_execution: bool
    require_review: bool
    max_proposals_per_request: int
    status: str
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.allow_execution is not False:
            raise ValueError("allow_execution must remain False")

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "allowed_skill_layers": list(self.allowed_skill_layers),
            "allowed_skill_ids": list(self.allowed_skill_ids),
            "denied_skill_ids": list(self.denied_skill_ids),
            "allow_multi_step_proposal": self.allow_multi_step_proposal,
            "allow_execution": self.allow_execution,
            "require_review": self.require_review,
            "max_proposals_per_request": self.max_proposals_per_request,
            "status": self.status,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestIntentCandidate:
    intent_candidate_id: str
    user_text_preview: str
    intent_family: str
    intent_name: str
    confidence: float
    matched_terms: list[str]
    suggested_skill_ids: list[str]
    missing_inputs: list[str]
    created_at: str
    intent_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", max(0.0, min(float(self.confidence), 1.0)))

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_candidate_id": self.intent_candidate_id,
            "user_text_preview": self.user_text_preview,
            "intent_family": self.intent_family,
            "intent_name": self.intent_name,
            "confidence": self.confidence,
            "matched_terms": list(self.matched_terms),
            "suggested_skill_ids": list(self.suggested_skill_ids),
            "missing_inputs": list(self.missing_inputs),
            "created_at": self.created_at,
            "intent_attrs": dict(self.intent_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestProposalBinding:
    binding_id: str
    intent_candidate_id: str
    skill_id: str
    proposal_id: str | None
    binding_order: int
    binding_reason: str
    required_inputs: list[str]
    provided_inputs: dict[str, Any]
    missing_inputs: list[str]
    can_create_proposal: bool
    requires_review: bool
    created_at: str
    binding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "binding_id": self.binding_id,
            "intent_candidate_id": self.intent_candidate_id,
            "skill_id": self.skill_id,
            "proposal_id": self.proposal_id,
            "binding_order": self.binding_order,
            "binding_reason": self.binding_reason,
            "required_inputs": list(self.required_inputs),
            "provided_inputs": dict(self.provided_inputs),
            "missing_inputs": list(self.missing_inputs),
            "can_create_proposal": self.can_create_proposal,
            "requires_review": self.requires_review,
            "created_at": self.created_at,
            "binding_attrs": dict(self.binding_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestProposalSet:
    proposal_set_id: str
    user_text_preview: str
    intent_candidate_ids: list[str]
    proposal_ids: list[str]
    binding_ids: list[str]
    family: str
    status: str
    requires_review: bool
    execution_performed: bool
    created_at: str
    set_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.execution_performed is not False:
            raise ValueError("execution_performed must remain False")

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_set_id": self.proposal_set_id,
            "user_text_preview": self.user_text_preview,
            "intent_candidate_ids": list(self.intent_candidate_ids),
            "proposal_ids": list(self.proposal_ids),
            "binding_ids": list(self.binding_ids),
            "family": self.family,
            "status": self.status,
            "requires_review": self.requires_review,
            "execution_performed": self.execution_performed,
            "created_at": self.created_at,
            "set_attrs": dict(self.set_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestProposalFinding:
    finding_id: str
    proposal_set_id: str | None
    intent_candidate_id: str | None
    skill_id: str | None
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
            "proposal_set_id": self.proposal_set_id,
            "intent_candidate_id": self.intent_candidate_id,
            "skill_id": self.skill_id,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_ref": self.subject_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestProposalResult:
    result_id: str
    proposal_set_id: str
    status: str
    created_proposal_count: int
    finding_ids: list[str]
    summary: str
    execution_performed: bool
    review_required: bool
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.execution_performed is not False:
            raise ValueError("execution_performed must remain False")
        if self.review_required is not True:
            raise ValueError("review_required must remain True")

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "proposal_set_id": self.proposal_set_id,
            "status": self.status,
            "created_proposal_count": self.created_proposal_count,
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "execution_performed": self.execution_performed,
            "review_required": self.review_required,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class ObservationDigestProposalService:
    def __init__(
        self,
        *,
        skill_registry_view_service: SkillRegistryViewService | Any | None = None,
        skill_proposal_service: Any | None = None,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        self.skill_registry_view_service = skill_registry_view_service
        self.skill_proposal_service = skill_proposal_service
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.last_policy: ObservationDigestProposalPolicy | None = None
        self.last_intents: list[ObservationDigestIntentCandidate] = []
        self.last_bindings: list[ObservationDigestProposalBinding] = []
        self.last_skill_proposals: list[SkillInvocationProposal] = []
        self.last_set: ObservationDigestProposalSet | None = None
        self.last_findings: list[ObservationDigestProposalFinding] = []
        self.last_result: ObservationDigestProposalResult | None = None
        self.registry_available = True

    def create_default_policy(self, **policy_attrs: Any) -> ObservationDigestProposalPolicy:
        policy = ObservationDigestProposalPolicy(
            policy_id=new_observation_digest_proposal_policy_id(),
            policy_name="observation_digest_review_only_proposal_policy",
            allowed_skill_layers=["internal_observation", "internal_digestion"],
            allowed_skill_ids=list(OBSERVATION_DIGESTION_SKILL_IDS),
            denied_skill_ids=[],
            allow_multi_step_proposal=True,
            allow_execution=False,
            require_review=True,
            max_proposals_per_request=int(policy_attrs.pop("max_proposals_per_request", 8)),
            status="active",
            created_at=utc_now_iso(),
            policy_attrs={
                "deterministic_rules_only": True,
                "llm_classifier_used": False,
                "execution_performed": False,
                "permission_grants_created": False,
                **policy_attrs,
            },
        )
        self.last_policy = policy
        self._record_model(
            "observation_digest_proposal_policy_registered",
            "observation_digest_proposal_policy",
            policy.policy_id,
            policy,
        )
        return policy

    def classify_intent(
        self,
        user_text: str,
        *,
        provided_inputs: dict[str, Any] | None = None,
    ) -> ObservationDigestIntentCandidate:
        provided = dict(provided_inputs or {})
        matched = _match_intents(user_text)
        ordered_names = _ordered_intent_names(matched)
        suggested_skill_ids = self.map_intent_to_skills(ordered_names)
        family = _intent_family(suggested_skill_ids)
        intent_name = ordered_names[0] if len(ordered_names) == 1 else "unknown"
        if family == "mixed_observation_digestion":
            intent_name = "unknown"
        if not suggested_skill_ids:
            family = "unknown"
            intent_name = "unknown"
        missing = _missing_inputs_for_skills(suggested_skill_ids, provided)
        confidence = 0.25 if not suggested_skill_ids else min(0.92, 0.55 + 0.08 * len(matched))
        intent = ObservationDigestIntentCandidate(
            intent_candidate_id=new_observation_digest_intent_candidate_id(),
            user_text_preview=user_text[:300],
            intent_family=family,
            intent_name=intent_name,
            confidence=confidence,
            matched_terms=sorted(matched),
            suggested_skill_ids=suggested_skill_ids,
            missing_inputs=missing,
            created_at=utc_now_iso(),
            intent_attrs={
                "deterministic_rules_only": True,
                "llm_classifier_used": False,
                "registry_available": self._registry_skill_ids() is not None,
            },
        )
        self.last_intents = [intent]
        self._record_model(
            "observation_digest_intent_classified",
            "observation_digest_intent_candidate",
            intent.intent_candidate_id,
            intent,
        )
        return intent

    def map_intent_to_skills(self, intent_names: list[str] | str) -> list[str]:
        names = [intent_names] if isinstance(intent_names, str) else list(intent_names)
        registry_ids = self._registry_skill_ids()
        result: list[str] = []
        for name in names:
            for skill_id in INTENT_TO_SKILLS.get(name, []):
                if registry_ids is None or skill_id in registry_ids:
                    if skill_id not in result:
                        result.append(skill_id)
        return result

    def infer_inputs_from_text(
        self,
        user_text: str,
        *,
        root_path: str | None = None,
        relative_path: str | None = None,
        source_runtime: str | None = None,
        format_hint: str | None = None,
        vendor_hint: str | None = None,
    ) -> dict[str, Any]:
        inputs: dict[str, Any] = {}
        if root_path:
            inputs["root_path"] = root_path
        if relative_path:
            inputs["relative_path"] = relative_path
        if source_runtime:
            inputs["source_runtime"] = source_runtime
            inputs["source_runtime_hint"] = source_runtime
        if format_hint:
            inputs["format_hint"] = format_hint
        if vendor_hint:
            inputs["vendor_hint"] = vendor_hint
        lowered = user_text.casefold()
        if "jsonl" in lowered and "format_hint" not in inputs:
            inputs["format_hint"] = "generic_jsonl"
        return inputs

    def create_proposal_binding(
        self,
        *,
        intent: ObservationDigestIntentCandidate,
        skill_id: str,
        binding_order: int,
        provided_inputs: dict[str, Any],
    ) -> ObservationDigestProposalBinding:
        required = REQUIRED_INPUTS_BY_SKILL_ID.get(skill_id, [])
        missing = _missing_inputs(required, provided_inputs)
        binding = ObservationDigestProposalBinding(
            binding_id=new_observation_digest_proposal_binding_id(),
            intent_candidate_id=intent.intent_candidate_id,
            skill_id=skill_id,
            proposal_id=None,
            binding_order=binding_order,
            binding_reason=f"{intent.intent_family}:{intent.intent_name}",
            required_inputs=required,
            provided_inputs=_proposal_payload(skill_id, provided_inputs, missing),
            missing_inputs=missing,
            can_create_proposal=True,
            requires_review=True,
            created_at=utc_now_iso(),
            binding_attrs={
                "execution_performed": False,
                "review_required": True,
                "registry_available": self.registry_available,
            },
        )
        self.last_bindings.append(binding)
        self._record_model(
            "observation_digest_proposal_binding_created",
            "observation_digest_proposal_binding",
            binding.binding_id,
            binding,
            links=[("observation_digest_intent_candidate_object", intent.intent_candidate_id)],
            object_links=[
                (
                    binding.binding_id,
                    intent.intent_candidate_id,
                    "proposal_binding_binds_intent_to_skill",
                )
            ],
        )
        return binding

    def create_skill_proposal(self, *, intent: ObservationDigestIntentCandidate, binding: ObservationDigestProposalBinding) -> SkillInvocationProposal:
        status = "incomplete" if binding.missing_inputs else "proposed"
        proposal = SkillInvocationProposal(
            proposal_id=new_skill_invocation_proposal_id(),
            intent_id=intent.intent_candidate_id,
            requirement_id=None,
            skill_id=binding.skill_id,
            proposal_status=status,
            invocation_mode="review_only",
            proposed_input_payload=dict(binding.provided_inputs),
            missing_inputs=list(binding.missing_inputs),
            confidence=intent.confidence,
            reason="Observation/Digestion proposal generated by deterministic rules.",
            review_required=True,
            executable_now=False,
            created_at=utc_now_iso(),
            proposal_attrs={
                "proposal_family": intent.intent_family,
                "execution_performed": False,
                "permission_grants_created": False,
                "llm_classifier_used": False,
            },
        )
        updated = ObservationDigestProposalBinding(
            **{**binding.to_dict(), "proposal_id": proposal.proposal_id}
        )
        self.last_bindings = [
            updated if item.binding_id == binding.binding_id else item for item in self.last_bindings
        ]
        self.last_skill_proposals.append(proposal)
        return proposal

    def create_proposal_set(
        self,
        *,
        user_text: str,
        intent: ObservationDigestIntentCandidate,
        bindings: list[ObservationDigestProposalBinding],
        proposals: list[SkillInvocationProposal],
    ) -> ObservationDigestProposalSet:
        if not proposals:
            status = "no_matching_skill"
        elif all(item.missing_inputs for item in proposals):
            status = "needs_more_input"
        elif any(item.missing_inputs for item in proposals):
            status = "partial"
        else:
            status = "proposal_created"
        proposal_set = ObservationDigestProposalSet(
            proposal_set_id=new_observation_digest_proposal_set_id(),
            user_text_preview=user_text[:300],
            intent_candidate_ids=[intent.intent_candidate_id],
            proposal_ids=[item.proposal_id for item in proposals],
            binding_ids=[item.binding_id for item in bindings],
            family=intent.intent_family,
            status=status,
            requires_review=True,
            execution_performed=False,
            created_at=utc_now_iso(),
            set_attrs={
                "ordered_skill_ids": [item.skill_id for item in bindings],
                "proposal_only": True,
                "llm_classifier_used": False,
            },
        )
        self.last_set = proposal_set
        self._record_model(
            "observation_digest_proposal_set_created",
            "observation_digest_proposal_set",
            proposal_set.proposal_set_id,
            proposal_set,
            links=[("observation_digest_intent_candidate_object", intent.intent_candidate_id)]
            + [("observation_digest_proposal_binding_object", item.binding_id) for item in bindings],
            object_links=[
                (intent.intent_candidate_id, proposal_set.proposal_set_id, "intent_candidate_belongs_to_proposal_set"),
                *[
                    (item.binding_id, proposal_set.proposal_set_id, "proposal_binding_belongs_to_proposal_set")
                    for item in bindings
                ],
            ],
        )
        if status == "needs_more_input":
            self._record_event("observation_digest_proposal_needs_more_input", proposal_set.proposal_set_id)
        if status == "no_matching_skill":
            self._record_event("observation_digest_proposal_no_matching_skill", proposal_set.proposal_set_id)
        return proposal_set

    def record_finding(
        self,
        *,
        proposal_set_id: str | None,
        intent_candidate_id: str | None,
        skill_id: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        subject_ref: str | None = None,
    ) -> ObservationDigestProposalFinding:
        finding = ObservationDigestProposalFinding(
            finding_id=new_observation_digest_proposal_finding_id(),
            proposal_set_id=proposal_set_id,
            intent_candidate_id=intent_candidate_id,
            skill_id=skill_id,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            subject_ref=subject_ref,
            created_at=utc_now_iso(),
            finding_attrs={"proposal_only": True, "execution_performed": False},
        )
        self.last_findings.append(finding)
        self._record_model(
            "observation_digest_proposal_finding_recorded",
            "observation_digest_proposal_finding",
            finding.finding_id,
            finding,
            links=[("observation_digest_proposal_set_object", proposal_set_id or "")],
            object_links=[
                (finding.finding_id, proposal_set_id or "", "proposal_finding_belongs_to_proposal_set")
            ],
        )
        return finding

    def record_result(self, *, proposal_set: ObservationDigestProposalSet) -> ObservationDigestProposalResult:
        result = ObservationDigestProposalResult(
            result_id=new_observation_digest_proposal_result_id(),
            proposal_set_id=proposal_set.proposal_set_id,
            status=proposal_set.status,
            created_proposal_count=len(proposal_set.proposal_ids),
            finding_ids=[item.finding_id for item in self.last_findings],
            summary=f"{proposal_set.status}: {len(proposal_set.proposal_ids)} proposal(s), {len(self.last_findings)} finding(s).",
            execution_performed=False,
            review_required=True,
            created_at=utc_now_iso(),
            result_attrs={
                "proposal_only": True,
                "llm_classifier_used": False,
                "permission_grants_created": False,
            },
        )
        self.last_result = result
        self._record_model(
            "observation_digest_proposal_result_recorded",
            "observation_digest_proposal_result",
            result.result_id,
            result,
            links=[("observation_digest_proposal_set_object", proposal_set.proposal_set_id)],
            object_links=[(result.result_id, proposal_set.proposal_set_id, "proposal_result_summarizes_proposal_set")],
        )
        return result

    def propose(
        self,
        user_text: str,
        *,
        root_path: str | None = None,
        relative_path: str | None = None,
        source_runtime: str | None = None,
        format_hint: str | None = None,
        vendor_hint: str | None = None,
    ) -> ObservationDigestProposalResult:
        self.last_bindings = []
        self.last_skill_proposals = []
        self.last_findings = []
        self.create_default_policy()
        provided = self.infer_inputs_from_text(
            user_text,
            root_path=root_path,
            relative_path=relative_path,
            source_runtime=source_runtime,
            format_hint=format_hint,
            vendor_hint=vendor_hint,
        )
        intent = self.classify_intent(user_text, provided_inputs=provided)
        bindings = [
            self.create_proposal_binding(
                intent=intent,
                skill_id=skill_id,
                binding_order=index,
                provided_inputs=provided,
            )
            for index, skill_id in enumerate(intent.suggested_skill_ids, start=1)
        ]
        proposals = [self.create_skill_proposal(intent=intent, binding=binding) for binding in bindings]
        proposal_set = self.create_proposal_set(
            user_text=user_text,
            intent=intent,
            bindings=list(self.last_bindings),
            proposals=proposals,
        )
        if not intent.suggested_skill_ids:
            self.record_finding(
                proposal_set_id=proposal_set.proposal_set_id,
                intent_candidate_id=intent.intent_candidate_id,
                skill_id=None,
                finding_type="no_matching_skill",
                status="no_match",
                severity="high",
                message="No Observation/Digestion skill matched the request.",
                subject_ref=intent.intent_candidate_id,
            )
        for proposal in proposals:
            for missing in proposal.missing_inputs:
                self.record_finding(
                    proposal_set_id=proposal_set.proposal_set_id,
                    intent_candidate_id=intent.intent_candidate_id,
                    skill_id=proposal.skill_id,
                    finding_type="missing_required_input",
                    status="needs_more_input",
                    severity="medium",
                    message=f"{missing} is required before review can proceed.",
                    subject_ref=proposal.proposal_id,
                )
        if intent.confidence < 0.5:
            self.record_finding(
                proposal_set_id=proposal_set.proposal_set_id,
                intent_candidate_id=intent.intent_candidate_id,
                skill_id=None,
                finding_type="low_confidence_intent",
                status="needs_review",
                severity="medium",
                message="Intent confidence is low.",
                subject_ref=intent.intent_candidate_id,
            )
        return self.record_result(proposal_set=proposal_set)

    def render_proposal_summary(self, result: ObservationDigestProposalResult | None = None) -> str:
        item = result or self.last_result
        if item is None:
            return "Observation/Digestion Proposal: unavailable"
        lines = [
            "Observation/Digestion Proposal",
            f"status={item.status}",
            f"result_id={item.result_id}",
            f"proposal_set_id={item.proposal_set_id}",
            f"created_proposal_count={item.created_proposal_count}",
            "review_required=true",
            "execution_performed=false",
        ]
        if self.last_set is not None:
            lines.append(f"family={self.last_set.family}")
            lines.append(f"ordered_skill_ids={','.join(self.last_set.set_attrs.get('ordered_skill_ids') or [])}")
        missing = sorted({missing for proposal in self.last_skill_proposals for missing in proposal.missing_inputs})
        if missing:
            lines.append(f"missing_inputs={','.join(missing)}")
        return "\n".join(lines)

    def _registry_skill_ids(self) -> set[str] | None:
        if self.skill_registry_view_service is False:
            self.registry_available = False
            return None
        service = self.skill_registry_view_service or SkillRegistryViewService()
        try:
            service.build_registry_view()
        except Exception:
            self.registry_available = False
            return None
        self.registry_available = True
        return {item.skill_id for item in service.last_entries}

    def _record_model(
        self,
        activity: str,
        object_type: str,
        object_id: str,
        model: Any,
        *,
        links: list[tuple[str, str]] | None = None,
        object_links: list[tuple[str, str, str]] | None = None,
    ) -> None:
        _record(
            self.trace_service,
            activity,
            objects=[_object(object_type, object_id, model.to_dict())],
            links=[(f"{object_type}_object", object_id), *(links or [])],
            object_links=object_links or [],
        )

    def _record_event(self, activity: str, proposal_set_id: str) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "proposal_only": True,
                "execution_performed": False,
            },
        )
        relation = OCELRelation.event_object(
            event_id=event.event_id,
            object_id=proposal_set_id,
            qualifier="observation_digest_proposal_set_object",
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=[], relations=[relation]))


def _match_intents(user_text: str) -> dict[str, list[str]]:
    text = user_text.casefold()
    mapping: list[tuple[str, list[str]]] = [
        ("agent_trace_observation", ["log", "로그", "jsonl", "ocel", "trace", "트레이스", "관찰", "다른 agent", "다른 에이전트", "뭘 했는지"]),
        ("agent_observation_normalization", ["normalize", "정규화", "chantacore 기준", "event candidate"]),
        ("agent_behavior_inference", ["추론", "행동", "목표", "intent", "goal", "inference"]),
        ("agent_process_narrative", ["narrative", "요약", "타임라인", "timeline"]),
        ("agent_observation_source_inspect", ["source", "형식", "inspect", "무슨 로그"]),
        ("external_skill_source_inspection", ["소화", "digest", "assimilate", "external skill", "외부 skill", "skill.md", "manifest"]),
        ("external_skill_static_digest", ["소화", "digest", "external skill", "외부 skill", "skill.md", "manifest"]),
        ("external_skill_assimilation", ["skill 후보", "capability 후보", "chantacore skill 후보"]),
        ("external_behavior_fingerprint", ["behavior fingerprint", "실제 동작", "behavior"]),
        ("external_skill_adapter_mapping", ["adapter", "mapping", "매핑", "대응 skill"]),
    ]
    matched: dict[str, list[str]] = {}
    for intent_name, terms in mapping:
        hits = [term for term in terms if term.casefold() in text]
        if hits:
            matched[intent_name] = hits
    return matched


def _ordered_intent_names(matched: dict[str, list[str]]) -> list[str]:
    order = [
        "agent_observation_source_inspect",
        "agent_trace_observation",
        "agent_observation_normalization",
        "agent_behavior_inference",
        "agent_process_narrative",
        "external_skill_source_inspection",
        "external_skill_static_digest",
        "external_behavior_fingerprint",
        "external_skill_assimilation",
        "external_skill_adapter_mapping",
    ]
    return [name for name in order if name in matched]


def _intent_family(skill_ids: list[str]) -> str:
    has_observation = any(skill_id in OBSERVATION_SKILL_IDS for skill_id in skill_ids)
    has_digestion = any(skill_id in DIGESTION_SKILL_IDS for skill_id in skill_ids)
    if has_observation and has_digestion:
        return "mixed_observation_digestion"
    if has_observation:
        return "observation"
    if has_digestion:
        return "digestion"
    return "unknown"


def _missing_inputs_for_skills(skill_ids: list[str], provided_inputs: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for skill_id in skill_ids:
        for item in _missing_inputs(REQUIRED_INPUTS_BY_SKILL_ID.get(skill_id, []), provided_inputs):
            if item not in missing:
                missing.append(item)
    return missing


def _missing_inputs(required_inputs: list[str], provided_inputs: dict[str, Any]) -> list[str]:
    missing: list[str] = []
    for required in required_inputs:
        if required == "source_runtime_hint_or_format_hint":
            ok = bool(provided_inputs.get("source_runtime_hint") or provided_inputs.get("format_hint"))
        elif required == "observation_batch_id_or_raw_records":
            ok = bool(provided_inputs.get("observation_batch_id") or provided_inputs.get("raw_records"))
        elif required == "observed_run_id_or_inference_id":
            ok = bool(provided_inputs.get("observed_run_id") or provided_inputs.get("inference_id"))
        elif required == "source_descriptor_id_or_root_path_relative_path":
            ok = bool(provided_inputs.get("source_descriptor_id") or (provided_inputs.get("root_path") and provided_inputs.get("relative_path")))
        elif required == "static_profile_id_or_behavior_fingerprint_id":
            ok = bool(provided_inputs.get("static_profile_id") or provided_inputs.get("behavior_fingerprint_id"))
        elif required == "assimilation_candidate_id_or_source_skill_ref":
            ok = bool(provided_inputs.get("assimilation_candidate_id") or provided_inputs.get("source_skill_ref"))
        else:
            ok = bool(provided_inputs.get(required))
        if not ok:
            missing.append(required)
    return missing


def _proposal_payload(skill_id: str, provided_inputs: dict[str, Any], missing_inputs: list[str]) -> dict[str, Any]:
    payload = {key: value for key, value in provided_inputs.items() if value is not None}
    for missing in missing_inputs:
        payload.setdefault(missing, f"<{missing.upper()}>")
    payload["skill_id"] = skill_id
    payload["proposal_only"] = True
    return payload


def _record(
    trace_service: TraceService,
    activity: str,
    *,
    objects: list[OCELObject],
    links: list[tuple[str, str]],
    object_links: list[tuple[str, str, str]],
) -> None:
    event = OCELEvent(
        event_id=f"evt:{uuid4()}",
        event_activity=activity,
        event_timestamp=utc_now_iso(),
        event_attrs={
            "runtime_event_type": activity,
            "source_runtime": "chanta_core",
            "proposal_only": True,
            "execution_performed": False,
            "review_required": True,
            "permission_grants_created": False,
            "llm_classifier_used": False,
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
    trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def _object(object_type: str, object_id: str, attrs: dict[str, Any]) -> OCELObject:
    return OCELObject(
        object_id=object_id,
        object_type=object_type,
        object_attrs={"object_key": object_id, "display_name": object_id, **attrs},
    )
