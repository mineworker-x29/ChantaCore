from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any

from chanta_core.agent_surface.contract import AgentSurfaceContractReportService
from chanta_core.agent_surface.intent_task import AgentIntentClassificationReportService
from chanta_core.agent_surface.provider_invocation import (
    AgentProviderEvidenceSeed,
    AgentProviderInvocationReport,
    AgentProviderInvocationReportService,
    AgentProviderResultBundle,
)
from chanta_core.agent_surface.safety_gate import (
    AgentGateOutcomeEnvelope,
    AgentSafetyGateReport,
    AgentSafetyGateReportService,
)
from chanta_core.agent_surface.turn_context import AgentTurnReportService
from chanta_core.utility.time import utc_now_iso


AGENT_RESPONSE_ASSEMBLY_VERSION = "v0.25.6"
AGENT_RESPONSE_ASSEMBLY_VERSION_NAME = "Response Assembly & Evidence Binder"
AGENT_RESPONSE_ASSEMBLY_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_RESPONSE_ASSEMBLY_NEXT_STEP = "v0.25.7 Ask / REPL Surface"

AGENT_RESPONSE_ASSEMBLY_OBJECT_TYPES = [
    "agent_response_assembly_policy",
    "agent_response_assembly_request",
    "agent_evidence_binding_policy",
    "agent_evidence_source_ref",
    "agent_evidence_item",
    "agent_evidence_bundle",
    "agent_claim",
    "agent_claim_support",
    "agent_response_section",
    "agent_uncertainty_note",
    "agent_limitation_note",
    "agent_no_action_response_draft",
    "agent_clarification_response_draft",
    "agent_blocked_response_draft",
    "agent_deferred_response_draft",
    "agent_answer_draft",
    "agent_assembled_response",
    "agent_response_assembly_trace",
    "agent_response_assembly_finding",
    "agent_response_assembly_report",
    "agent_provider_invocation_report",
    "agent_provider_result_bundle",
    "agent_provider_evidence_seed",
    "agent_gate_outcome_envelope",
    "agent_safety_gate_report",
    "agent_turn_envelope",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_RESPONSE_ASSEMBLY_EVENT_TYPES = [
    "agent_response_assembly_requested",
    "agent_response_assembly_policy_created",
    "agent_evidence_binding_policy_created",
    "agent_evidence_source_ref_created",
    "agent_evidence_item_created",
    "agent_evidence_bundle_created",
    "agent_claim_created",
    "agent_claim_support_created",
    "agent_response_section_created",
    "agent_uncertainty_note_created",
    "agent_limitation_note_created",
    "agent_answer_draft_created",
    "agent_response_assembled",
    "agent_response_assembly_trace_created",
    "agent_response_assembly_report_created",
    "agent_response_assembly_warning_created",
    "agent_response_assembly_blocked",
]

AGENT_RESPONSE_ASSEMBLY_RELATION_TYPES = [
    "uses_agent_provider_evidence_seed",
    "uses_agent_provider_result_bundle",
    "uses_agent_gate_outcome_envelope",
    "uses_agent_safety_gate_report",
    "uses_agent_turn_envelope",
    "creates_evidence_source_ref",
    "creates_evidence_item",
    "creates_evidence_bundle",
    "creates_agent_claim",
    "binds_claim_to_evidence",
    "creates_response_section",
    "creates_uncertainty_note",
    "creates_limitation_note",
    "creates_answer_draft",
    "assembles_agent_response",
    "records_response_assembly_trace",
    "prepares_ask_repl_surface",
    "defers_response_emission_to_v0_25_7",
    "defers_agent_trace_telemetry_to_v0_25_8",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_final_response_emitted",
    "not_agent_ask_executed",
    "not_agent_repl_started",
    "not_memory_promoted",
    "not_persona_mutated",
    "prevents_credential_exposure",
    "blocks_raw_provider_output_inline",
    "blocks_raw_secret_output",
    "derived_from_agent_provider_invocation_report",
    "derived_from_agent_gate_outcome",
    "recorded_in_envelope",
]

AGENT_RESPONSE_ASSEMBLY_EFFECT_TYPES = [
    "read_only_observation",
    "agent_evidence_bound",
    "agent_response_assembled",
    "agent_answer_draft_created",
    "state_candidate_created",
]

AGENT_RESPONSE_ASSEMBLY_FORBIDDEN_EFFECT_TYPES = [
    "final_response_emitted",
    "agent_ask_executed",
    "agent_repl_started",
    "provider_invoked",
    "local_command_executed",
    "bounded_local_command_executed",
    "command_rerun_performed",
    "direct_file_access_performed",
    "direct_subprocess_called",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "external_provider_called",
    "external_agent_runtime_touched",
    "file_written",
    "file_edited",
    "file_deleted",
    "credential_exposed",
    "raw_secret_output",
    "raw_provider_output_inline",
    "schumpeter_split_introduced",
]


def _safe_id(text: str | None) -> str:
    value = text or "unknown"
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "-", value.strip().lower())[:140] or "unknown"


def _dict_ref(ref_type: str, ref_id: str | None) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id or "unknown"}


def _sanitize_text(text: str) -> str:
    value = text or ""
    value = re.sub(r"[A-Za-z]:\\[^\s`\"']+", "[private-path]", value)
    value = re.sub(r"(?i)(api[_-]?key|token|secret|password)=\S+", r"\1=[redacted]", value)
    return value[:20000]


@dataclass
class AgentResponseAssemblyPolicy:
    policy_id: str
    version: str = AGENT_RESPONSE_ASSEMBLY_VERSION
    layer: str = "agent_surface"
    deterministic_default: bool = True
    external_llm_response_generation_enabled: bool = False
    llm_factuality_judge_enabled: bool = False
    llm_safety_judge_enabled: bool = False
    response_assembly_enabled: bool = True
    response_emission_enabled: bool = False
    ask_execution_enabled: bool = False
    repl_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    require_evidence_for_provider_claims: bool = True
    fact_inference_uncertainty_separation_required: bool = True
    provider_result_label_required: bool = True
    no_action_rationale_required: bool = True
    blocked_rationale_required: bool = True
    clarification_questions_required_when_selected: bool = True
    raw_provider_output_inline_forbidden: bool = True
    raw_secret_output_forbidden: bool = True
    credential_output_forbidden: bool = True
    private_path_sanitization_required: bool = True
    final_conclusion_once: bool = True
    max_response_chars: int = 20000
    max_evidence_items: int = 100
    evidence_refs_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResponseAssemblyRequest:
    request_id: str
    version: str = AGENT_RESPONSE_ASSEMBLY_VERSION
    provider_invocation_report_id: str | None = None
    evidence_seed_id: str | None = None
    safety_gate_report_id: str | None = None
    gate_outcome_envelope_id: str | None = None
    intent_report_id: str | None = None
    task_frame_id: str | None = None
    turn_envelope_id: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentEvidenceBindingPolicy:
    policy_id: str
    version: str = AGENT_RESPONSE_ASSEMBLY_VERSION
    evidence_required_for_provider_outputs: bool = True
    raw_provider_output_inline_forbidden: bool = True
    evidence_item_must_have_source_ref: bool = True
    evidence_item_must_have_kind: bool = True
    source_ref_must_be_sanitized: bool = True
    private_path_sanitization_required: bool = True
    raw_secret_evidence_forbidden: bool = True
    credential_evidence_forbidden: bool = True
    max_evidence_items: int = 100
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentEvidenceSourceRef:
    source_ref_id: str
    source_type: str
    source_id: str | None
    provider_id: str | None
    provider_type: str | None
    sanitized_label: str
    raw_content_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentEvidenceItem:
    evidence_item_id: str
    evidence_kind: str
    source_ref: AgentEvidenceSourceRef
    summary: str
    supports_claim_ids: list[str]
    confidence: str
    raw_content_included: bool = False
    raw_secret_included: bool = False
    credential_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentEvidenceBundle:
    evidence_bundle_id: str
    version: str = AGENT_RESPONSE_ASSEMBLY_VERSION
    evidence_items: list[AgentEvidenceItem] = field(default_factory=list)
    evidence_count: int = 0
    provider_evidence_count: int = 0
    policy_evidence_count: int = 0
    uncertainty_evidence_count: int = 0
    bundle_status: str = "ready"
    raw_provider_output_inline: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentClaim:
    claim_id: str
    claim_type: str
    text: str
    confidence: str
    requires_evidence: bool
    evidence_item_ids: list[str]
    unsupported: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentClaimSupport:
    support_id: str
    claim_id: str
    evidence_item_ids: list[str]
    support_status: str
    missing_evidence_reason: str | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResponseSection:
    section_id: str
    section_type: str
    title: str | None
    body: str
    claim_ids: list[str]
    evidence_item_ids: list[str]
    section_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentUncertaintyNote:
    uncertainty_id: str
    message: str
    cause: str
    affected_claim_ids: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentLimitationNote:
    limitation_id: str
    message: str
    limitation_type: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentNoActionResponseDraft:
    draft_id: str
    no_action_decision_ref: dict[str, Any]
    rationale: str
    safe_alternative: str | None
    sections: list[AgentResponseSection]
    response_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentClarificationResponseDraft:
    draft_id: str
    clarification_decision_ref: dict[str, Any]
    questions: list[str]
    rationale: str
    sections: list[AgentResponseSection]
    response_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentBlockedResponseDraft:
    draft_id: str
    blocked_decision_ref: dict[str, Any]
    blocked_reason: str
    safe_alternative: str | None
    sections: list[AgentResponseSection]
    response_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentDeferredResponseDraft:
    draft_id: str
    deferred_decision_ref: dict[str, Any]
    deferred_to_track: str
    deferred_reason: str
    sections: list[AgentResponseSection]
    response_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentAnswerDraft:
    draft_id: str
    response_mode: str
    claims: list[AgentClaim]
    claim_supports: list[AgentClaimSupport]
    sections: list[AgentResponseSection]
    uncertainty_notes: list[AgentUncertaintyNote]
    limitation_notes: list[AgentLimitationNote]
    draft_status: str
    evidence_bundle_id: str | None
    version: str = AGENT_RESPONSE_ASSEMBLY_VERSION
    final_conclusion_once: bool = True
    raw_provider_output_inline: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentAssembledResponse:
    assembled_response_id: str
    created_at: str
    request_ref: dict[str, Any]
    answer_draft: AgentAnswerDraft
    response_text: str
    response_status: str
    version: str = AGENT_RESPONSE_ASSEMBLY_VERSION
    response_assembled: bool = True
    final_response_emitted: bool = False
    ask_executed: bool = False
    repl_started: bool = False
    provider_invoked_in_v0256: bool = False
    local_command_executed: bool = False
    memory_promoted: bool = False
    persona_mutated: bool = False
    raw_provider_output_inline: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    private_full_paths_included: bool = False
    next_required_step: str = AGENT_RESPONSE_ASSEMBLY_NEXT_STEP
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResponseAssemblyTrace:
    trace_id: str
    version: str = AGENT_RESPONSE_ASSEMBLY_VERSION
    assembly_request_id: str = ""
    evidence_bundle_id: str | None = None
    answer_draft_id: str | None = None
    assembled_response_id: str | None = None
    events: list[dict[str, Any]] = field(default_factory=list)
    object_refs: list[dict[str, Any]] = field(default_factory=list)
    relation_refs: list[dict[str, Any]] = field(default_factory=list)
    trace_status: str = "recorded"
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    raw_secret_in_trace: bool = False
    private_full_path_in_trace: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResponseAssemblyFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResponseAssemblyReport:
    report_id: str
    version: str = AGENT_RESPONSE_ASSEMBLY_VERSION
    created_at: str = ""
    policy: AgentResponseAssemblyPolicy | None = None
    request: AgentResponseAssemblyRequest | None = None
    evidence_binding_policy: AgentEvidenceBindingPolicy | None = None
    evidence_bundle: AgentEvidenceBundle | None = None
    answer_draft: AgentAnswerDraft | None = None
    assembled_response: AgentAssembledResponse | None = None
    assembly_trace: AgentResponseAssemblyTrace | None = None
    findings: list[AgentResponseAssemblyFinding] = field(default_factory=list)
    report_status: str = "failed"
    ready_for_v0_25_7: bool = False
    ready_for_v0_26: bool = False
    response_assembled: bool = False
    final_response_emitted: bool = False
    evidence_bound: bool = False
    unsupported_claim_count: int = 0
    uncertainty_note_count: int = 0
    limitation_note_count: int = 0
    provider_invoked: bool = False
    local_command_executed: bool = False
    ask_executed: bool = False
    repl_started: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_RESPONSE_ASSEMBLY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.7 ask/repl emission begins or response/evidence policy changes."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentResponseAssemblyPrerequisiteSourceService:
    def load_agent_surface_contract(self) -> dict[str, Any]:
        return AgentSurfaceContractReportService().build_report().to_dict()

    def load_provider_invocation_report_if_available(self) -> AgentProviderInvocationReport:
        return AgentProviderInvocationReportService().build_report()

    def load_provider_evidence_seed_if_available(self) -> AgentProviderEvidenceSeed | None:
        report = self.load_provider_invocation_report_if_available()
        return report.evidence_seed

    def load_provider_result_bundle_if_available(self) -> AgentProviderResultBundle | None:
        report = self.load_provider_invocation_report_if_available()
        return report.result_bundle

    def load_safety_gate_report_if_available(self) -> AgentSafetyGateReport:
        return AgentSafetyGateReportService().build_report()

    def load_gate_outcome_envelope_if_available(self) -> AgentGateOutcomeEnvelope | None:
        report = self.load_safety_gate_report_if_available()
        return report.outcome_envelope

    def load_intent_report_if_available(self) -> dict[str, Any]:
        return AgentIntentClassificationReportService().build_report().to_dict()

    def load_task_frame_if_available(self) -> dict[str, Any]:
        return AgentIntentClassificationReportService().build_report().task_frame.to_dict()

    def load_turn_envelope_if_available(self) -> dict[str, Any]:
        return AgentTurnReportService().build_report().turn_envelope.to_dict()


class AgentResponseAssemblyPolicyService:
    def build_policy(self) -> AgentResponseAssemblyPolicy:
        return AgentResponseAssemblyPolicy(
            policy_id="agent_response_assembly_policy:v0.25.6",
            evidence_refs=[
                {"type": "version", "value": AGENT_RESPONSE_ASSEMBLY_VERSION},
                {"type": "track", "value": AGENT_RESPONSE_ASSEMBLY_TRACK},
            ],
        )


class AgentEvidenceBindingPolicyService:
    def build_policy(self) -> AgentEvidenceBindingPolicy:
        return AgentEvidenceBindingPolicy(
            policy_id="agent_evidence_binding_policy:v0.25.6",
            evidence_refs=[{"type": "raw_provider_output_inline_forbidden", "value": True}],
        )


class AgentEvidenceSourceRefService:
    def build_source_refs(
        self,
        provider_report: AgentProviderInvocationReport | None = None,
        safety_gate_report: AgentSafetyGateReport | None = None,
    ) -> list[AgentEvidenceSourceRef]:
        refs: list[AgentEvidenceSourceRef] = []
        if provider_report and provider_report.evidence_seed:
            refs.append(
                AgentEvidenceSourceRef(
                    source_ref_id=f"agent_evidence_source_ref:{_safe_id(provider_report.evidence_seed.evidence_seed_id)}",
                    source_type="provider_evidence_seed",
                    source_id=provider_report.evidence_seed.evidence_seed_id,
                    provider_id=None,
                    provider_type=None,
                    sanitized_label="Provider evidence seed reference",
                    evidence_refs=[_dict_ref("agent_provider_invocation_report", provider_report.report_id)],
                )
            )
            for result_ref in provider_report.result_bundle.result_refs if provider_report.result_bundle else []:
                refs.append(
                    AgentEvidenceSourceRef(
                        source_ref_id=f"agent_evidence_source_ref:{_safe_id(result_ref.result_ref_id)}",
                        source_type="provider_result_ref",
                        source_id=result_ref.result_ref_id,
                        provider_id=result_ref.provider_id,
                        provider_type=result_ref.provider_type,
                        sanitized_label=_sanitize_text(f"{result_ref.provider_type} result reference"),
                        evidence_refs=[_dict_ref("agent_provider_result_bundle", provider_report.result_bundle.bundle_id)],
                    )
                )
        if safety_gate_report and safety_gate_report.outcome_envelope:
            gate_decision = safety_gate_report.gate_decision
            refs.append(
                AgentEvidenceSourceRef(
                    source_ref_id=f"agent_evidence_source_ref:{_safe_id(safety_gate_report.outcome_envelope.outcome_envelope_id)}",
                    source_type="safety_gate_decision",
                    source_id=gate_decision.decision_id if gate_decision else safety_gate_report.report_id,
                    provider_id=None,
                    provider_type=None,
                    sanitized_label="Safety gate decision reference",
                    evidence_refs=[_dict_ref("agent_safety_gate_report", safety_gate_report.report_id)],
                )
            )
        return refs


class AgentEvidenceItemService:
    def build_evidence_items(
        self,
        source_refs: list[AgentEvidenceSourceRef],
        provider_report: AgentProviderInvocationReport | None = None,
        safety_gate_report: AgentSafetyGateReport | None = None,
    ) -> list[AgentEvidenceItem]:
        items: list[AgentEvidenceItem] = []
        for source_ref in source_refs:
            if source_ref.source_type == "provider_result_ref":
                kind = "observed_provider_result"
                summary = f"Observed provider result reference from {source_ref.provider_type}."
                confidence = "medium"
            elif source_ref.source_type == "provider_evidence_seed":
                kind = "route_context"
                summary = "Provider evidence seed is ready for response assembly."
                confidence = "medium"
            elif source_ref.source_type == "safety_gate_decision":
                kind = "gate_decision"
                outcome = safety_gate_report.gate_decision.primary_outcome if safety_gate_report and safety_gate_report.gate_decision else "unknown"
                summary = f"Safety gate outcome is {outcome}."
                confidence = "high"
            else:
                kind = "unknown"
                summary = "Unknown evidence source reference."
                confidence = "low"
            items.append(
                AgentEvidenceItem(
                    evidence_item_id=f"agent_evidence_item:{_safe_id(source_ref.source_ref_id)}",
                    evidence_kind=kind,
                    source_ref=source_ref,
                    summary=_sanitize_text(summary),
                    supports_claim_ids=[],
                    confidence=confidence,
                    evidence_refs=[_dict_ref("agent_evidence_source_ref", source_ref.source_ref_id)],
                )
            )
        if provider_report and provider_report.result_bundle and provider_report.result_bundle.result_count == 0:
            source_ref = AgentEvidenceSourceRef(
                source_ref_id=f"agent_evidence_source_ref:no_provider_result:{_safe_id(provider_report.report_id)}",
                source_type="provider_evidence_seed",
                source_id=provider_report.evidence_seed.evidence_seed_id if provider_report.evidence_seed else None,
                provider_id=None,
                provider_type=None,
                sanitized_label="No provider result was required",
            )
            items.append(
                AgentEvidenceItem(
                    evidence_item_id=f"agent_evidence_item:{_safe_id(source_ref.source_ref_id)}",
                    evidence_kind="limitation",
                    source_ref=source_ref,
                    summary="No provider invocation result was required for this response source.",
                    supports_claim_ids=[],
                    confidence="medium",
                )
            )
        return items


class AgentEvidenceBundleService:
    def build_bundle(self, evidence_items: list[AgentEvidenceItem]) -> AgentEvidenceBundle:
        provider_count = sum(1 for item in evidence_items if item.evidence_kind == "observed_provider_result")
        policy_count = sum(1 for item in evidence_items if item.evidence_kind in {"gate_decision", "policy_constraint"})
        uncertainty_count = sum(1 for item in evidence_items if item.evidence_kind == "uncertainty")
        if any(item.raw_secret_included or item.credential_included for item in evidence_items):
            status = "blocked"
        elif not evidence_items:
            status = "failed"
        elif provider_count == 0:
            status = "warning"
        else:
            status = "ready"
        return AgentEvidenceBundle(
            evidence_bundle_id="agent_evidence_bundle:v0.25.6",
            evidence_items=evidence_items[:100],
            evidence_count=len(evidence_items[:100]),
            provider_evidence_count=provider_count,
            policy_evidence_count=policy_count,
            uncertainty_evidence_count=uncertainty_count,
            bundle_status=status,
            evidence_refs=[{"type": "evidence_item_count", "value": len(evidence_items[:100])}],
        )


class AgentClaimService:
    def build_claims(
        self,
        evidence_bundle: AgentEvidenceBundle,
        provider_report: AgentProviderInvocationReport | None = None,
        safety_gate_report: AgentSafetyGateReport | None = None,
    ) -> list[AgentClaim]:
        claims: list[AgentClaim] = []
        provider_items = [item for item in evidence_bundle.evidence_items if item.evidence_kind == "observed_provider_result"]
        if provider_items:
            claim = self._claim(
                "provider_observation",
                "Provider observations are available as sanitized result references, not raw provider output.",
                "medium",
                True,
                [item.evidence_item_id for item in provider_items],
            )
            claims.append(claim)
            claims.append(
                self._claim(
                    "inference",
                    "The response can summarize the availability of provider-backed evidence without treating provider output as an automatic fact.",
                    "medium",
                    True,
                    [item.evidence_item_id for item in provider_items],
                )
            )
            return claims
        if safety_gate_report and safety_gate_report.outcome_envelope:
            outcome = safety_gate_report.gate_decision.primary_outcome if safety_gate_report.gate_decision else "unknown"
            gate_item_ids = [item.evidence_item_id for item in evidence_bundle.evidence_items if item.evidence_kind == "gate_decision"]
            if outcome == "no_action":
                claims.append(self._claim("no_action_rationale", "No-action response is selected because action is unnecessary or redundant under the gate policy.", "high", True, gate_item_ids))
            elif outcome == "clarification_requested":
                claims.append(self._claim("clarification_request", "Clarification response must ask for the specific missing input before later stages proceed.", "high", True, gate_item_ids))
            elif outcome == "needs_more_input":
                claims.append(self._claim("clarification_request", "More input is required before a useful response can proceed.", "high", True, gate_item_ids))
            elif outcome == "blocked":
                claims.append(self._claim("blocked_rationale", "Blocked response is policy-grounded and should include a safe alternative when possible.", "high", True, gate_item_ids))
            elif outcome == "deferred":
                claims.append(self._claim("deferred_scope", "The request belongs to a future track and is deferred by policy.", "high", True, gate_item_ids))
            else:
                claims.append(self._claim("confirmed_fact", f"Safety gate outcome is {outcome}.", "medium", True, gate_item_ids))
        if not claims:
            claims.append(self._claim("uncertainty", "No complete response source is available.", "low", True, []))
        return claims

    def _claim(self, claim_type: str, text: str, confidence: str, requires_evidence: bool, evidence_item_ids: list[str]) -> AgentClaim:
        return AgentClaim(
            claim_id=f"agent_claim:{claim_type}:{_safe_id(text)}",
            claim_type=claim_type,
            text=_sanitize_text(text),
            confidence=confidence,
            requires_evidence=requires_evidence,
            evidence_item_ids=evidence_item_ids,
            unsupported=requires_evidence and not evidence_item_ids,
            evidence_refs=[_dict_ref("agent_evidence_item", evidence_item_ids[0])] if evidence_item_ids else [],
        )


class AgentClaimSupportService:
    def bind_claims_to_evidence(self, claims: list[AgentClaim], evidence_bundle: AgentEvidenceBundle) -> list[AgentClaimSupport]:
        evidence_ids = {item.evidence_item_id for item in evidence_bundle.evidence_items}
        supports: list[AgentClaimSupport] = []
        for claim in claims:
            valid_ids = [item_id for item_id in claim.evidence_item_ids if item_id in evidence_ids]
            if not claim.requires_evidence:
                status = "not_required"
                reason = None
            elif valid_ids:
                status = "supported"
                reason = None
            else:
                status = "unsupported"
                reason = "Evidence is required but no bound evidence item is available."
            supports.append(
                AgentClaimSupport(
                    support_id=f"agent_claim_support:{_safe_id(claim.claim_id)}",
                    claim_id=claim.claim_id,
                    evidence_item_ids=valid_ids,
                    support_status=status,
                    missing_evidence_reason=reason,
                    evidence_refs=[_dict_ref("agent_claim", claim.claim_id)],
                )
            )
        return supports


class AgentUncertaintyNoteService:
    def build_uncertainty_notes(self, claims: list[AgentClaim], evidence_bundle: AgentEvidenceBundle) -> list[AgentUncertaintyNote]:
        notes: list[AgentUncertaintyNote] = []
        unsupported = [claim.claim_id for claim in claims if claim.unsupported]
        if unsupported:
            notes.append(
                AgentUncertaintyNote(
                    uncertainty_id="agent_uncertainty_note:unsupported_claim",
                    message="Some claims lack required evidence and are marked unsupported.",
                    cause="unsupported_claim",
                    affected_claim_ids=unsupported,
                )
            )
        if evidence_bundle.bundle_status in {"warning", "failed"}:
            notes.append(
                AgentUncertaintyNote(
                    uncertainty_id="agent_uncertainty_note:partial_evidence",
                    message="Evidence is partial or non-provider-only; confidence is limited.",
                    cause="partial_provider_result" if evidence_bundle.provider_evidence_count == 0 else "missing_evidence",
                    affected_claim_ids=[claim.claim_id for claim in claims],
                )
            )
        return notes


class AgentLimitationNoteService:
    def build_limitation_notes(
        self,
        evidence_bundle: AgentEvidenceBundle,
        provider_report: AgentProviderInvocationReport | None = None,
    ) -> list[AgentLimitationNote]:
        notes = [
            AgentLimitationNote(
                limitation_id="agent_limitation_note:emission_deferred",
                message="v0.25.6 assembles a response artifact only; ask/REPL emission is deferred to v0.25.7.",
                limitation_type="future_track",
            )
        ]
        if provider_report is None or evidence_bundle.provider_evidence_count == 0:
            notes.append(
                AgentLimitationNote(
                    limitation_id="agent_limitation_note:no_provider_invocation",
                    message="Response assembly did not invoke providers in v0.25.6.",
                    limitation_type="no_provider_invocation",
                )
            )
        return notes


class AgentResponseSectionService:
    def build_sections(
        self,
        response_mode: str,
        claims: list[AgentClaim],
        evidence_bundle: AgentEvidenceBundle,
        uncertainty_notes: list[AgentUncertaintyNote],
        limitation_notes: list[AgentLimitationNote],
        safety_gate_report: AgentSafetyGateReport | None = None,
    ) -> list[AgentResponseSection]:
        claim_ids = [claim.claim_id for claim in claims]
        evidence_ids = [item.evidence_item_id for item in evidence_bundle.evidence_items]
        sections: list[AgentResponseSection] = []
        if response_mode == "provider_backed_answer":
            sections.append(self._section("direct_answer", "Answer Draft", "A provider-backed answer draft was assembled from sanitized evidence references.", claim_ids, evidence_ids))
            sections.append(self._section("observations", "Observations", "Provider result references are treated as observations and are not automatically promoted to facts.", claim_ids, evidence_ids))
            sections.append(self._section("evidence", "Evidence", f"{evidence_bundle.evidence_count} sanitized evidence item(s) are bound to the draft.", claim_ids, evidence_ids))
            sections.append(self._section("inference", "Inference", "Any interpretation is labeled as inference and remains evidence-bound.", claim_ids, evidence_ids))
        elif response_mode == "no_action_response":
            sections.append(self._section("no_action_rationale", "No-Action Rationale", "No action is a valid gate outcome; the response records the rationale instead of invoking tools.", claim_ids, evidence_ids))
        elif response_mode in {"clarification_response", "needs_more_input_response"}:
            questions = self._clarification_questions(safety_gate_report)
            sections.append(self._section("clarification_questions", "Clarification Questions", "\n".join(f"- {question}" for question in questions), claim_ids, evidence_ids))
        elif response_mode == "blocked_response":
            sections.append(self._section("blocked_reason", "Blocked Reason", self._blocked_reason(safety_gate_report), claim_ids, evidence_ids))
            sections.append(self._section("next_steps", "Safe Alternative", self._blocked_safe_alternative(safety_gate_report), claim_ids, evidence_ids))
        elif response_mode == "deferred_response":
            sections.append(self._section("deferred_reason", "Deferred Reason", self._deferred_reason(safety_gate_report), claim_ids, evidence_ids))
        else:
            sections.append(self._section("direct_answer", "Answer Draft", "A response-only draft was assembled from policy and task context.", claim_ids, evidence_ids))
        if uncertainty_notes:
            sections.append(self._section("uncertainty", "Uncertainty", " ".join(note.message for note in uncertainty_notes), claim_ids, evidence_ids))
        if limitation_notes:
            sections.append(self._section("limitations", "Limitations", " ".join(note.message for note in limitation_notes), claim_ids, evidence_ids))
        sections.append(self._section("final_conclusion", "Conclusion", "Response artifact assembled for v0.25.7 emission surface; it has not been emitted.", claim_ids, evidence_ids))
        return sections

    def _section(self, section_type: str, title: str, body: str, claim_ids: list[str], evidence_ids: list[str]) -> AgentResponseSection:
        return AgentResponseSection(
            section_id=f"agent_response_section:{section_type}",
            section_type=section_type,
            title=title,
            body=_sanitize_text(body),
            claim_ids=claim_ids,
            evidence_item_ids=evidence_ids,
            section_status="ready",
        )

    def _clarification_questions(self, safety_gate_report: AgentSafetyGateReport | None) -> list[str]:
        envelope = safety_gate_report.outcome_envelope if safety_gate_report else None
        if envelope and envelope.clarification_decision:
            return [question.question_text for question in envelope.clarification_decision.questions]
        if envelope and envelope.needs_more_input_decision:
            return [str(item.get("description") or item.get("missing_input_type") or "Please provide the missing required input.") for item in envelope.needs_more_input_decision.missing_inputs]
        return ["Please provide the specific missing target, scope, or required input."]

    def _blocked_reason(self, safety_gate_report: AgentSafetyGateReport | None) -> str:
        envelope = safety_gate_report.outcome_envelope if safety_gate_report else None
        if envelope and envelope.blocked_decision:
            return envelope.blocked_decision.blocked_reason
        return "The request is blocked by the agent safety gate policy."

    def _blocked_safe_alternative(self, safety_gate_report: AgentSafetyGateReport | None) -> str:
        envelope = safety_gate_report.outcome_envelope if safety_gate_report else None
        if envelope and envelope.blocked_decision and envelope.blocked_decision.safe_alternative:
            return envelope.blocked_decision.safe_alternative
        return "Use a request that avoids credentials, raw secrets, external adapters, or forbidden execution."

    def _deferred_reason(self, safety_gate_report: AgentSafetyGateReport | None) -> str:
        envelope = safety_gate_report.outcome_envelope if safety_gate_report else None
        if envelope and envelope.deferred_decision:
            return f"Deferred to {envelope.deferred_decision.deferred_to_track}: {envelope.deferred_decision.deferred_reason}"
        return "The request belongs to a future track."


class AgentAnswerDraftService:
    def build_answer_draft(
        self,
        request: AgentResponseAssemblyRequest,
        evidence_bundle: AgentEvidenceBundle,
        provider_report: AgentProviderInvocationReport | None = None,
        safety_gate_report: AgentSafetyGateReport | None = None,
    ) -> AgentAnswerDraft:
        response_mode = self._response_mode(provider_report, safety_gate_report)
        claims = AgentClaimService().build_claims(evidence_bundle, provider_report, safety_gate_report)
        supports = AgentClaimSupportService().bind_claims_to_evidence(claims, evidence_bundle)
        uncertainty_notes = AgentUncertaintyNoteService().build_uncertainty_notes(claims, evidence_bundle)
        limitation_notes = AgentLimitationNoteService().build_limitation_notes(evidence_bundle, provider_report)
        sections = AgentResponseSectionService().build_sections(response_mode, claims, evidence_bundle, uncertainty_notes, limitation_notes, safety_gate_report)
        status = "blocked" if evidence_bundle.bundle_status == "blocked" else "warning" if uncertainty_notes or evidence_bundle.bundle_status == "warning" else "ready"
        return AgentAnswerDraft(
            draft_id=f"agent_answer_draft:{_safe_id(request.request_id)}",
            response_mode=response_mode,
            claims=claims,
            claim_supports=supports,
            sections=sections,
            uncertainty_notes=uncertainty_notes,
            limitation_notes=limitation_notes,
            draft_status=status,
            evidence_bundle_id=evidence_bundle.evidence_bundle_id,
            evidence_refs=[_dict_ref("agent_evidence_bundle", evidence_bundle.evidence_bundle_id)],
        )

    def build_no_action_response_draft(self, answer_draft: AgentAnswerDraft, safety_gate_report: AgentSafetyGateReport) -> AgentNoActionResponseDraft:
        decision = safety_gate_report.outcome_envelope.no_action_decision if safety_gate_report.outcome_envelope else None
        return AgentNoActionResponseDraft(
            draft_id=f"agent_no_action_response_draft:{_safe_id(answer_draft.draft_id)}",
            no_action_decision_ref=_dict_ref("no_action_decision", decision.decision_id if decision else None),
            rationale=decision.rationale if decision else "No-action selected by policy.",
            safe_alternative=decision.safe_alternative if decision else None,
            sections=answer_draft.sections,
        )

    def build_clarification_response_draft(self, answer_draft: AgentAnswerDraft, safety_gate_report: AgentSafetyGateReport) -> AgentClarificationResponseDraft:
        envelope = safety_gate_report.outcome_envelope
        decision = envelope.clarification_decision if envelope and envelope.clarification_decision else None
        questions = [question.question_text for question in decision.questions] if decision else ["Please provide the missing required input."]
        return AgentClarificationResponseDraft(
            draft_id=f"agent_clarification_response_draft:{_safe_id(answer_draft.draft_id)}",
            clarification_decision_ref=_dict_ref("clarification_decision", decision.decision_id if decision else None),
            questions=questions,
            rationale=decision.rationale if decision else "Clarification is required before proceeding.",
            sections=answer_draft.sections,
        )

    def build_blocked_response_draft(self, answer_draft: AgentAnswerDraft, safety_gate_report: AgentSafetyGateReport) -> AgentBlockedResponseDraft:
        decision = safety_gate_report.outcome_envelope.blocked_decision if safety_gate_report.outcome_envelope else None
        return AgentBlockedResponseDraft(
            draft_id=f"agent_blocked_response_draft:{_safe_id(answer_draft.draft_id)}",
            blocked_decision_ref=_dict_ref("blocked_decision", decision.decision_id if decision else None),
            blocked_reason=decision.blocked_reason if decision else "Blocked by safety policy.",
            safe_alternative=decision.safe_alternative if decision else "Use a request within the current safety boundary.",
            sections=answer_draft.sections,
        )

    def build_deferred_response_draft(self, answer_draft: AgentAnswerDraft, safety_gate_report: AgentSafetyGateReport) -> AgentDeferredResponseDraft:
        decision = safety_gate_report.outcome_envelope.deferred_decision if safety_gate_report.outcome_envelope else None
        return AgentDeferredResponseDraft(
            draft_id=f"agent_deferred_response_draft:{_safe_id(answer_draft.draft_id)}",
            deferred_decision_ref=_dict_ref("deferred_decision", decision.decision_id if decision else None),
            deferred_to_track=decision.deferred_to_track if decision else "future_track",
            deferred_reason=decision.deferred_reason if decision else "Deferred to a future track.",
            sections=answer_draft.sections,
        )

    def _response_mode(self, provider_report: AgentProviderInvocationReport | None, safety_gate_report: AgentSafetyGateReport | None) -> str:
        if provider_report and provider_report.evidence_seed and provider_report.evidence_seed.ready_for_evidence_binder and provider_report.provider_invoked:
            return "provider_backed_answer"
        outcome = safety_gate_report.gate_decision.primary_outcome if safety_gate_report and safety_gate_report.gate_decision else "unknown"
        return {
            "no_action": "no_action_response",
            "clarification_requested": "clarification_response",
            "needs_more_input": "needs_more_input_response",
            "blocked": "blocked_response",
            "deferred": "deferred_response",
            "failed": "failed_response",
        }.get(outcome, "response_only_answer")


class AgentAssembledResponseService:
    def assemble_response_text(self, answer_draft: AgentAnswerDraft, max_chars: int = 20000) -> str:
        chunks = []
        for section in answer_draft.sections:
            title = section.title or section.section_type
            chunks.append(f"{title}\n{section.body}")
        text = "\n\n".join(chunks)
        return _sanitize_text(text)[:max_chars]

    def build_assembled_response(self, request: AgentResponseAssemblyRequest, answer_draft: AgentAnswerDraft) -> AgentAssembledResponse:
        text = self.assemble_response_text(answer_draft)
        status = "blocked" if answer_draft.draft_status == "blocked" else "warning" if answer_draft.draft_status == "warning" else "assembled"
        return AgentAssembledResponse(
            assembled_response_id=f"agent_assembled_response:{_safe_id(answer_draft.draft_id)}",
            created_at=utc_now_iso(),
            request_ref=_dict_ref("agent_response_assembly_request", request.request_id),
            answer_draft=answer_draft,
            response_text=text,
            response_status=status,
            evidence_refs=[_dict_ref("agent_answer_draft", answer_draft.draft_id)],
        )


class AgentResponseAssemblyTraceService:
    def build_trace(
        self,
        request: AgentResponseAssemblyRequest,
        evidence_bundle: AgentEvidenceBundle | None,
        answer_draft: AgentAnswerDraft | None,
        assembled_response: AgentAssembledResponse | None,
    ) -> AgentResponseAssemblyTrace:
        return AgentResponseAssemblyTrace(
            trace_id=f"agent_response_assembly_trace:{_safe_id(request.request_id)}",
            assembly_request_id=request.request_id,
            evidence_bundle_id=evidence_bundle.evidence_bundle_id if evidence_bundle else None,
            answer_draft_id=answer_draft.draft_id if answer_draft else None,
            assembled_response_id=assembled_response.assembled_response_id if assembled_response else None,
            events=[
                {"type": "agent_response_assembly_requested", "version": AGENT_RESPONSE_ASSEMBLY_VERSION},
                {"type": "agent_response_assembled", "version": AGENT_RESPONSE_ASSEMBLY_VERSION},
                {"type": "agent_response_assembly_trace_created", "version": AGENT_RESPONSE_ASSEMBLY_VERSION},
            ],
            object_refs=[
                _dict_ref("agent_response_assembly_request", request.request_id),
                _dict_ref("agent_evidence_bundle", evidence_bundle.evidence_bundle_id if evidence_bundle else None),
                _dict_ref("agent_answer_draft", answer_draft.draft_id if answer_draft else None),
            ],
            relation_refs=[
                {"type": "creates_evidence_bundle"},
                {"type": "creates_answer_draft"},
                {"type": "assembles_agent_response"},
                {"type": "defers_response_emission_to_v0_25_7"},
            ],
            trace_status="recorded" if assembled_response else "failed",
        )


class AgentResponseAssemblyFindingService:
    BLOCKED_ATTEMPTS = {
        "raw_provider_output_inline_attempted",
        "raw_secret_output_detected",
        "credential_exposure_detected",
        "private_full_path_output_detected",
        "provider_invocation_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "ask_execution_attempted_too_early",
        "repl_execution_attempted_too_early",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
        "external_provider_adapter_detected",
        "external_agent_adapter_detected",
        "opencode_runtime_dependency_detected",
        "openclaw_runtime_dependency_detected",
        "hermes_runtime_dependency_detected",
        "schumpeter_split_detected",
        "growthkernel_dependency_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        request: AgentResponseAssemblyRequest,
        evidence_bundle: AgentEvidenceBundle | None,
        answer_draft: AgentAnswerDraft | None,
        assembled_response: AgentAssembledResponse | None,
        provider_report: AgentProviderInvocationReport | None = None,
        safety_gate_report: AgentSafetyGateReport | None = None,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentResponseAssemblyFinding]:
        subject_id = request.request_id
        findings = [self._finding("info", "ok", "Response assembly and evidence binding were evaluated.", subject_id)]
        if provider_report is None and not request.evidence_seed_id:
            findings.append(self._finding("warning", "missing_provider_evidence_seed", "Provider evidence seed is missing.", subject_id))
        if safety_gate_report is None and not request.gate_outcome_envelope_id:
            findings.append(self._finding("warning", "missing_gate_outcome", "Gate outcome envelope is missing.", subject_id))
        if provider_report is None and safety_gate_report is None:
            findings.append(self._finding("error", "missing_response_source", "No provider evidence seed or gate outcome is available.", subject_id))
        if evidence_bundle is not None:
            findings.append(self._finding("info", "evidence_bundle_created", "Evidence bundle was created.", evidence_bundle.evidence_bundle_id))
            if evidence_bundle.bundle_status in {"warning", "failed"}:
                findings.append(self._finding("warning", "insufficient_evidence", "Evidence is partial or insufficient.", evidence_bundle.evidence_bundle_id))
        if answer_draft:
            if any(claim.unsupported for claim in answer_draft.claims):
                findings.append(self._finding("warning", "unsupported_claim_detected", "Unsupported claim is marked unsupported.", answer_draft.draft_id))
            if answer_draft.uncertainty_notes:
                findings.append(self._finding("warning", "uncertainty_note_created", "Uncertainty note was created.", answer_draft.draft_id))
            if answer_draft.limitation_notes:
                findings.append(self._finding("warning", "limitation_note_created", "Limitation note was created.", answer_draft.draft_id))
            response_finding = {
                "provider_backed_answer": "provider_backed_answer_created",
                "no_action_response": "no_action_response_created",
                "clarification_response": "clarification_response_created",
                "needs_more_input_response": "needs_more_input_response_created",
                "blocked_response": "blocked_response_created",
                "deferred_response": "deferred_response_created",
            }.get(answer_draft.response_mode)
            if response_finding:
                findings.append(self._finding("info", response_finding, f"{answer_draft.response_mode} was created.", answer_draft.draft_id))
        if assembled_response is not None:
            findings.append(self._finding("info", "response_assembled", "Response artifact was assembled without emission.", assembled_response.assembled_response_id))
            findings.append(self._finding("info", "final_response_emission_deferred", "Final response emission is deferred to v0.25.7.", assembled_response.assembled_response_id))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_ATTEMPTS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected.", subject_id))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentResponseAssemblyFinding:
        return AgentResponseAssemblyFinding(
            finding_id=f"agent_response_assembly_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the condition is removed or explicitly deferred by response assembly policy.",
        )


class AgentResponseAssemblyReportService:
    def build_request(
        self,
        provider_report: AgentProviderInvocationReport | None,
        safety_gate_report: AgentSafetyGateReport | None,
    ) -> AgentResponseAssemblyRequest:
        evidence_seed = provider_report.evidence_seed if provider_report else None
        gate_envelope = safety_gate_report.outcome_envelope if safety_gate_report else None
        turn_envelope_id = None
        if provider_report and provider_report.request:
            turn_envelope_id = provider_report.request.turn_envelope_id
        elif safety_gate_report and safety_gate_report.request:
            turn_envelope_id = safety_gate_report.request.turn_envelope_id
        return AgentResponseAssemblyRequest(
            request_id=f"agent_response_assembly_request:{_safe_id(provider_report.report_id if provider_report else safety_gate_report.report_id if safety_gate_report else None)}",
            provider_invocation_report_id=provider_report.report_id if provider_report else None,
            evidence_seed_id=evidence_seed.evidence_seed_id if evidence_seed else None,
            safety_gate_report_id=safety_gate_report.report_id if safety_gate_report else provider_report.request.safety_gate_report_id if provider_report and provider_report.request else None,
            gate_outcome_envelope_id=gate_envelope.outcome_envelope_id if gate_envelope else None,
            turn_envelope_id=turn_envelope_id,
            source_refs=[
                _dict_ref("agent_provider_invocation_report", provider_report.report_id if provider_report else None),
                _dict_ref("agent_safety_gate_report", safety_gate_report.report_id if safety_gate_report else None),
            ],
        )

    def build_report(
        self,
        request_text: str = "Explain the project structure",
        provider_report: AgentProviderInvocationReport | None = None,
        safety_gate_report: AgentSafetyGateReport | None = None,
        use_provider_report: bool = True,
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentResponseAssemblyReport:
        policy = AgentResponseAssemblyPolicyService().build_policy()
        evidence_policy = AgentEvidenceBindingPolicyService().build_policy()
        source_provider_report = provider_report if provider_report is not None else (AgentProviderInvocationReportService().build_report(request_text=request_text) if use_provider_report else None)
        source_safety_report = safety_gate_report
        if source_safety_report is None and source_provider_report is None:
            source_safety_report = AgentSafetyGateReportService().build_report(request_text=request_text)
        request = self.build_request(source_provider_report, source_safety_report)
        source_refs = AgentEvidenceSourceRefService().build_source_refs(source_provider_report, source_safety_report)
        evidence_items = AgentEvidenceItemService().build_evidence_items(source_refs, source_provider_report, source_safety_report)
        evidence_bundle = AgentEvidenceBundleService().build_bundle(evidence_items)
        answer_draft = AgentAnswerDraftService().build_answer_draft(request, evidence_bundle, source_provider_report, source_safety_report)
        assembled_response = AgentAssembledResponseService().build_assembled_response(request, answer_draft)
        trace = AgentResponseAssemblyTraceService().build_trace(request, evidence_bundle, answer_draft, assembled_response)
        findings = AgentResponseAssemblyFindingService().build_findings(
            request,
            evidence_bundle,
            answer_draft,
            assembled_response,
            source_provider_report,
            source_safety_report,
            attempt_flags,
        )
        report_status = self._report_status(evidence_bundle, answer_draft, findings)
        unsupported_count = sum(1 for claim in answer_draft.claims if claim.unsupported)
        return AgentResponseAssemblyReport(
            report_id=f"agent_response_assembly_report:{_safe_id(request.request_id)}",
            created_at=utc_now_iso(),
            policy=policy,
            request=request,
            evidence_binding_policy=evidence_policy,
            evidence_bundle=evidence_bundle,
            answer_draft=answer_draft,
            assembled_response=assembled_response,
            assembly_trace=trace,
            findings=findings,
            report_status=report_status,
            ready_for_v0_25_7=assembled_response is not None and report_status in {"passed", "warning"},
            response_assembled=assembled_response.response_assembled,
            evidence_bound=evidence_bundle.bundle_status in {"ready", "warning"},
            unsupported_claim_count=unsupported_count,
            uncertainty_note_count=len(answer_draft.uncertainty_notes),
            limitation_note_count=len(answer_draft.limitation_notes),
            limitations=[
                "v0.25.6 assembles response artifacts only; final response emission is deferred to v0.25.7.",
                "Provider evidence is represented by sanitized result references, not raw provider output.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.25.6 emits ask/REPL responses, invokes providers, executes commands, reads files directly, inlines raw provider output, or uses an LLM judge.",
            ],
        )

    def build_all_parts(
        self,
        request_text: str = "Explain the project structure",
        use_provider_report: bool = True,
    ) -> dict[str, Any]:
        report = self.build_report(request_text=request_text, use_provider_report=use_provider_report)
        return {
            "report": report,
            "policy": report.policy,
            "request": report.request,
            "evidence_policy": report.evidence_binding_policy,
            "evidence_bundle": report.evidence_bundle,
            "evidence_items": report.evidence_bundle.evidence_items if report.evidence_bundle else [],
            "answer_draft": report.answer_draft,
            "assembled_response": report.assembled_response,
            "trace": report.assembly_trace,
            "findings": report.findings,
        }

    def _report_status(
        self,
        evidence_bundle: AgentEvidenceBundle,
        answer_draft: AgentAnswerDraft,
        findings: list[AgentResponseAssemblyFinding],
    ) -> str:
        if any(item.severity == "critical" for item in findings) or evidence_bundle.bundle_status == "blocked" or answer_draft.draft_status == "blocked":
            return "blocked"
        if any(item.severity == "error" for item in findings) or evidence_bundle.bundle_status == "failed" or answer_draft.draft_status == "failed":
            return "failed"
        if any(item.severity == "warning" for item in findings) or answer_draft.draft_status == "warning":
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_RESPONSE_ASSEMBLY_VERSION,
            "layer": "agent_surface",
            "subject": "response_assembly_evidence_binder",
            "principles": [
                "response assembly is not ask/repl emission",
                "evidence binding is not raw provider output dump",
                "provider result is not automatically a fact",
                "observation, inference, uncertainty, and limitation must be separated",
                "no-action response must include rationale",
                "clarification response must ask specific missing-input questions",
                "blocked response must include policy-grounded reason and safe alternative when possible",
                "conclusion should appear once",
                "ask/repl surface is deferred to v0.25.7",
            ],
            "safety_boundary": {
                "response_assembled": "conditional",
                "final_response_emitted": False,
                "evidence_bound": "conditional",
                "provider_invoked": False,
                "local_command_executed": False,
                "ask_executed": False,
                "repl_started": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_provider_output_inline": False,
                "llm_judge_enabled": False,
            },
            "future_direction": {
                "v0.25": "bounded agent surface",
                "v0.26": "workspace agent workbench",
                "v0.27": "memory candidate and continuity",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "next_step": AGENT_RESPONSE_ASSEMBLY_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_response_assembled_evidence_bound",
            "version": AGENT_RESPONSE_ASSEMBLY_VERSION,
            "source_read_models": [
                "AgentProviderInvocationReportState",
                "AgentProviderResultBundleState",
                "AgentProviderEvidenceSeedState",
                "AgentGateOutcomeState",
                "AgentSafetyGateState",
                "AgentTurnEnvelopeState",
            ],
            "target_read_models": [
                "AgentEvidenceBundleState",
                "AgentClaimState",
                "AgentClaimSupportState",
                "AgentAnswerDraftState",
                "AgentAssembledResponseState",
                "AgentResponseAssemblyTraceState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_RESPONSE_ASSEMBLY_EFFECT_TYPES,
        }


def render_agent_response_cli(parts: dict[str, Any], section: str) -> str:
    report: AgentResponseAssemblyReport = parts["report"]
    draft = report.answer_draft
    assembled = report.assembled_response
    lines = [
        f"version={report.version}",
        "layer=agent_surface",
        f"response_assembled={str(report.response_assembled).lower()}",
        f"final_response_emitted={str(report.final_response_emitted).lower()}",
        f"evidence_bound={str(report.evidence_bound).lower()}",
        f"unsupported_claim_count={report.unsupported_claim_count}",
        f"uncertainty_note_count={report.uncertainty_note_count}",
        f"limitation_note_count={report.limitation_note_count}",
        f"ready_for_v0_25_7={str(report.ready_for_v0_25_7).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"repl_started={str(report.repl_started).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_provider_output_inline={str(report.raw_provider_output_inline).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "assemble":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
        lines.append(f"response_mode={draft.response_mode if draft else 'missing'}")
    elif section == "evidence":
        bundle = report.evidence_bundle
        lines.append(f"evidence_bundle_id={bundle.evidence_bundle_id if bundle else 'missing'}")
        lines.append(f"evidence_count={bundle.evidence_count if bundle else 0}")
        lines.append(f"provider_evidence_count={bundle.provider_evidence_count if bundle else 0}")
    elif section == "draft":
        lines.append(f"draft_id={draft.draft_id if draft else 'missing'}")
        lines.append(f"draft_status={draft.draft_status if draft else 'missing'}")
        if draft:
            for claim in draft.claims:
                lines.append(f"- claim={claim.claim_type}:{claim.confidence}:unsupported={str(claim.unsupported).lower()}")
    elif section == "assembled":
        lines.append(f"assembled_response_id={assembled.assembled_response_id if assembled else 'missing'}")
        lines.append(f"response_status={assembled.response_status if assembled else 'missing'}")
    elif section == "findings":
        for finding in report.findings:
            lines.append(f"- {finding.finding_type}: {finding.severity}")
    else:
        lines.append(f"report_id={report.report_id}")
    return "\n".join(lines)
