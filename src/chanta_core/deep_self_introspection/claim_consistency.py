from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

from chanta_core.deep_self_introspection.candidate_memory_boundary import (
    SelfCandidateMemoryBoundaryAwarenessService,
)
from chanta_core.deep_self_introspection.capability_registry import (
    SelfCapabilityRegistryAwarenessService,
)
from chanta_core.deep_self_introspection.context_projection import (
    SelfContextProjectionAwarenessService,
)
from chanta_core.deep_self_introspection.policy_gate import SelfPolicyGateAwarenessService
from chanta_core.deep_self_introspection.runtime_boundary import SelfRuntimeBoundaryAwarenessService
from chanta_core.deep_self_introspection.trace_integrity import SelfTraceIntegrityAwarenessService
from chanta_core.utility.time import utc_now_iso


ClaimConsistencyStatus = Literal["passed", "warning", "failed", "blocked"]

HIGH_RISK_CLAIM_TYPES = {
    "capability_claim",
    "execution_claim",
    "read_claim",
    "search_claim",
    "verification_claim",
    "promotion_claim",
    "memory_claim",
    "materialization_claim",
    "runtime_boundary_claim",
    "policy_claim",
    "external_contact_claim",
    "canonical_truth_claim",
}


@dataclass(frozen=True)
class SelfClaimConsistencyRequest:
    source_type: str = "payload"
    source_id: str | None = None
    claim_payload: dict[str, Any] | None = None
    include_capability_truth: bool = True
    include_runtime_boundary: bool = True
    include_policy_gate: bool = True
    include_trace_integrity: bool = True
    include_context_projection: bool = True
    include_candidate_memory_boundary: bool = True
    strictness: str = "standard"
    max_claims: int = 200
    max_findings: int = 300

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class SelfClaimSourceRef:
    source_id: str
    source_type: str
    source_ref: dict[str, Any]
    redacted: bool
    raw_content_included: bool
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_type": self.source_type,
            "source_ref": dict(self.source_ref),
            "redacted": self.redacted,
            "raw_content_included": self.raw_content_included,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class SelfClaim:
    claim_id: str
    claim_type: str
    claim_text: str | None
    normalized_claim: str
    subject: str | None
    predicate: str
    object_ref: dict[str, Any] | None
    source_ref: SelfClaimSourceRef
    confidence: str
    requires_evidence: bool
    supported_claim_types: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim_id": self.claim_id,
            "claim_type": self.claim_type,
            "claim_text": self.claim_text,
            "normalized_claim": self.normalized_claim,
            "subject": self.subject,
            "predicate": self.predicate,
            "object_ref": dict(self.object_ref or {}),
            "source_ref": self.source_ref.to_dict(),
            "confidence": self.confidence,
            "requires_evidence": self.requires_evidence,
            "supported_claim_types": list(self.supported_claim_types),
        }


@dataclass(frozen=True)
class ClaimEvidenceRequirement:
    requirement_id: str
    claim_id: str
    required_evidence_type: str
    required_object_types: list[str]
    required_event_types: list[str]
    required_relation_types: list[str]
    required_report_types: list[str]
    allow_report_only: bool
    allow_candidate_only: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "claim_id": self.claim_id,
            "required_evidence_type": self.required_evidence_type,
            "required_object_types": list(self.required_object_types),
            "required_event_types": list(self.required_event_types),
            "required_relation_types": list(self.required_relation_types),
            "required_report_types": list(self.required_report_types),
            "allow_report_only": self.allow_report_only,
            "allow_candidate_only": self.allow_candidate_only,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class ClaimEvidenceMatch:
    match_id: str
    claim_id: str
    requirement_id: str
    matched: bool
    evidence_refs: list[dict[str, Any]]
    missing_evidence_types: list[str]
    contradiction_refs: list[dict[str, Any]]
    match_status: str
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "match_id": self.match_id,
            "claim_id": self.claim_id,
            "requirement_id": self.requirement_id,
            "matched": self.matched,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "missing_evidence_types": list(self.missing_evidence_types),
            "contradiction_refs": [dict(item) for item in self.contradiction_refs],
            "match_status": self.match_status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class SelfClaimConsistencyFinding:
    finding_id: str
    severity: str
    finding_type: str
    claim_id: str | None
    message: str
    claim_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    contradiction_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "claim_id": self.claim_id,
            "message": self.message,
            "claim_ref": dict(self.claim_ref or {}),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "contradiction_refs": [dict(item) for item in self.contradiction_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class ContradictionRegisterEntry:
    entry_id: str
    claim_id: str
    contradiction_type: str
    severity: str
    claim_summary: str
    contradicted_by: list[dict[str, Any]]
    source_ref: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    status: str
    recommended_followup: str | None
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "claim_id": self.claim_id,
            "contradiction_type": self.contradiction_type,
            "severity": self.severity,
            "claim_summary": self.claim_summary,
            "contradicted_by": [dict(item) for item in self.contradicted_by],
            "source_ref": dict(self.source_ref),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "status": self.status,
            "recommended_followup": self.recommended_followup,
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class SelfContradictionRegister:
    register_id: str
    created_at: str
    entries: list[ContradictionRegisterEntry]
    open_count: int
    critical_count: int
    error_count: int
    warning_count: int
    info_count: int
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "register_id": self.register_id,
            "created_at": self.created_at,
            "entries": [item.to_dict() for item in self.entries],
            "open_count": self.open_count,
            "critical_count": self.critical_count,
            "error_count": self.error_count,
            "warning_count": self.warning_count,
            "info_count": self.info_count,
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


@dataclass(frozen=True)
class SelfClaimConsistencyReport:
    report_id: str
    created_at: str
    request: SelfClaimConsistencyRequest
    source_refs: list[SelfClaimSourceRef]
    claims: list[SelfClaim]
    requirements: list[ClaimEvidenceRequirement]
    evidence_matches: list[ClaimEvidenceMatch]
    findings: list[SelfClaimConsistencyFinding]
    contradiction_register_id: str | None
    checked_claim_count: int
    supported_claim_count: int
    unsupported_claim_count: int
    contradicted_claim_count: int
    unverifiable_claim_count: int
    status: ClaimConsistencyStatus
    limitations: list[str]
    withdrawal_conditions: list[str]
    validity_horizon: str
    review_status: str = "report_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "source_refs": [item.to_dict() for item in self.source_refs],
            "claims": [item.to_dict() for item in self.claims],
            "requirements": [item.to_dict() for item in self.requirements],
            "evidence_matches": [item.to_dict() for item in self.evidence_matches],
            "findings": [item.to_dict() for item in self.findings],
            "contradiction_register_id": self.contradiction_register_id,
            "checked_claim_count": self.checked_claim_count,
            "supported_claim_count": self.supported_claim_count,
            "unsupported_claim_count": self.unsupported_claim_count,
            "contradicted_claim_count": self.contradicted_claim_count,
            "unverifiable_claim_count": self.unverifiable_claim_count,
            "status": self.status,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


class SelfClaimSourceService:
    def load_sources(self, request: SelfClaimConsistencyRequest) -> list[SelfClaimSourceRef]:
        if request.source_type not in {"payload", "report", "workbench", "projection", "candidate", "assistant_message"}:
            return [
                _source_ref(
                    "source:unsupported",
                    request.source_type,
                    {"source_status": "blocked", "reason": "unsupported_source_type"},
                    True,
                    [{"source_blocked": True}],
                )
            ]
        if _payload_private(request.claim_payload):
            return [
                _source_ref(
                    request.source_id or "source:private_payload",
                    request.source_type,
                    {"source_status": "blocked", "reason": "private_payload_risk"},
                    True,
                    [{"private_payload_blocked": True}],
                )
            ]
        source_ref = {
            "source_status": "loaded",
            "source_kind": request.source_type,
            "source_id": request.source_id,
            "raw_body_available": False,
        }
        return [_source_ref(request.source_id or f"source:{request.source_type}", request.source_type, source_ref, True, [{"read_only": True}])]


class SelfClaimExtractor:
    def extract_claims(
        self,
        sources: list[SelfClaimSourceRef],
        request: SelfClaimConsistencyRequest,
    ) -> list[SelfClaim]:
        if any(item.source_ref.get("source_status") == "blocked" for item in sources):
            return []
        claims_payload = request.claim_payload or {}
        raw_claims = claims_payload.get("claims", [])
        if isinstance(raw_claims, dict):
            raw_claims = [raw_claims]
        if not isinstance(raw_claims, list):
            raw_claims = []
        source = sources[0] if sources else _source_ref("source:empty", request.source_type, {}, True, [])
        claims: list[SelfClaim] = []
        for index, item in enumerate(raw_claims[: max(0, request.max_claims)]):
            if not isinstance(item, dict):
                continue
            claim_type = str(item.get("claim_type") or "unsupported_claim")
            normalized = _safe_summary(str(item.get("normalized_claim") or item.get("claim") or claim_type))
            claims.append(
                SelfClaim(
                    claim_id=str(item.get("claim_id") or f"claim:{index + 1}"),
                    claim_type=claim_type,
                    claim_text=_safe_summary(str(item["claim_text"])) if item.get("claim_text") else None,
                    normalized_claim=normalized,
                    subject=str(item.get("subject")) if item.get("subject") is not None else None,
                    predicate=str(item.get("predicate") or _default_predicate(claim_type)),
                    object_ref=dict(item.get("object_ref") or {}),
                    source_ref=source,
                    confidence=str(item.get("confidence") or "unknown"),
                    requires_evidence=bool(item.get("requires_evidence", True)),
                    supported_claim_types=[str(value) for value in item.get("supported_claim_types", []) if isinstance(value, str)],
                )
            )
        return claims


class ClaimEvidenceRequirementMapper:
    def map_requirements(self, claims: list[SelfClaim]) -> list[ClaimEvidenceRequirement]:
        return [_requirement_for_claim(claim) for claim in claims]


class ClaimEvidenceMatcher:
    def __init__(
        self,
        *,
        capability_service: SelfCapabilityRegistryAwarenessService | None = None,
        runtime_service: SelfRuntimeBoundaryAwarenessService | None = None,
        policy_gate_service: SelfPolicyGateAwarenessService | None = None,
        trace_integrity_service: SelfTraceIntegrityAwarenessService | None = None,
        context_projection_service: SelfContextProjectionAwarenessService | None = None,
        candidate_boundary_service: SelfCandidateMemoryBoundaryAwarenessService | None = None,
    ) -> None:
        self.capability_service = capability_service or SelfCapabilityRegistryAwarenessService()
        self.runtime_service = runtime_service or SelfRuntimeBoundaryAwarenessService()
        self.policy_gate_service = policy_gate_service or SelfPolicyGateAwarenessService()
        self.trace_integrity_service = trace_integrity_service or SelfTraceIntegrityAwarenessService()
        self.context_projection_service = context_projection_service or SelfContextProjectionAwarenessService()
        self.candidate_boundary_service = candidate_boundary_service or SelfCandidateMemoryBoundaryAwarenessService()

    def match_evidence(
        self,
        claims: list[SelfClaim],
        requirements: list[ClaimEvidenceRequirement],
        request: SelfClaimConsistencyRequest | None = None,
    ) -> list[ClaimEvidenceMatch]:
        catalog = self._catalog(request or SelfClaimConsistencyRequest())
        requirement_by_claim = {item.claim_id: item for item in requirements}
        return [self._match_one(claim, requirement_by_claim[claim.claim_id], catalog) for claim in claims]

    def _catalog(self, request: SelfClaimConsistencyRequest) -> dict[str, Any]:
        catalog: dict[str, Any] = {}
        if request.include_capability_truth:
            snapshot = self.capability_service.view_registry()
            catalog["capabilities"] = {record.skill_id: record for record in snapshot.records if record.skill_id}
        if request.include_runtime_boundary:
            runtime = self.runtime_service.view_runtime_boundary()
            catalog["runtime"] = runtime.execution_boundary
        if request.include_policy_gate:
            policy = self.policy_gate_service.view_policy_gate_map()
            catalog["policy"] = policy
        if request.include_trace_integrity:
            trace_report = self.trace_integrity_service.check_trace_integrity()
            catalog["trace"] = trace_report
        if request.include_context_projection:
            context_report = self.context_projection_service.truth_check()
            catalog["context"] = context_report
        if request.include_candidate_memory_boundary:
            boundary_report = self.candidate_boundary_service.truth_check()
            catalog["candidate_boundary"] = boundary_report
        return catalog

    def _match_one(
        self,
        claim: SelfClaim,
        requirement: ClaimEvidenceRequirement,
        catalog: dict[str, Any],
    ) -> ClaimEvidenceMatch:
        obj = claim.object_ref or {}
        refs: list[dict[str, Any]] = []
        missing: list[str] = []
        contradictions: list[dict[str, Any]] = []
        status = "unsupported"

        if not claim.requires_evidence:
            status = "not_applicable"
        elif claim.claim_type == "capability_claim":
            status, refs, missing, contradictions = self._match_capability(claim, obj, catalog)
        elif claim.claim_type == "execution_claim":
            status, refs, missing, contradictions = _match_required_pair(
                obj,
                "execution_envelope",
                "ocel_event",
                "envelope_id",
                "ocel_event_id",
                "execution_claim_without_envelope",
                "execution_claim_without_ocel_event",
            )
        elif claim.claim_type == "read_claim":
            status, refs, missing, contradictions = _match_required_values(
                obj,
                ["self_text_read_completed", "text_slice", "workspace_file"],
                "read_claim_without_text_read_event",
            )
        elif claim.claim_type == "search_claim":
            status, refs, missing, contradictions = _match_required_values(
                obj,
                ["workspace_search_result", "workspace_search_match"],
                "search_claim_without_search_result",
            )
        elif claim.claim_type == "verification_claim":
            status, refs, missing, contradictions = _match_required_values(
                obj,
                ["verification_report_id"],
                "verification_claim_without_report",
            )
        elif claim.claim_type == "promotion_claim":
            status, refs, missing, contradictions = self._match_disabled_boundary(
                obj,
                catalog,
                "promotion_claim_contradicts_boundary",
                "candidate_boundary",
            )
        elif claim.claim_type == "memory_claim":
            status, refs, missing, contradictions = self._match_disabled_boundary(
                obj,
                catalog,
                "memory_claim_contradicts_boundary",
                "candidate_boundary",
            )
        elif claim.claim_type == "materialization_claim":
            status, refs, missing, contradictions = self._match_disabled_boundary(
                obj,
                catalog,
                "materialization_claim_contradicts_boundary",
                "candidate_boundary",
            )
        elif claim.claim_type == "external_contact_claim":
            status, refs, missing, contradictions = _contradicted("external_contact_claim_contradicts_runtime", "runtime_boundary")
        elif claim.claim_type == "canonical_truth_claim":
            target_status = str(obj.get("target_status") or obj.get("source_status") or "")
            if target_status in {"candidate_only", "report_only", "projection_only"} or obj.get("candidate_only") or obj.get("report_only") or obj.get("projection_only"):
                status, refs, missing, contradictions = _contradicted("canonical_truth_claim_on_candidate", target_status or "candidate_only")
            elif obj.get("canonical_truth") is True:
                status = "supported"
                refs = [{"evidence_type": "canonical_truth_evidence", "source": "ocel"}]
            else:
                missing = ["canonical_truth_evidence"]
        elif claim.claim_type == "policy_claim":
            status, refs, missing, contradictions = self._match_policy_claim(obj, catalog)
        elif claim.claim_type == "runtime_boundary_claim":
            status, refs, missing, contradictions = self._match_runtime_claim(obj, catalog)
        elif claim.claim_type == "raw_transcript_claim":
            status, refs, missing, contradictions = _contradicted("raw_transcript_claim_without_process_state", "context_projection")
        elif claim.claim_type == "no_action_claim":
            status = "supported" if obj.get("policy_ref") or claim.predicate == "no_action_valid" else "unsupported"
            refs = [{"evidence_type": "policy_gate_truth_report", "supports_no_action": True}] if status == "supported" else []
            missing = [] if status == "supported" else ["policy_ref"]
        else:
            status = "unverifiable" if claim.confidence in {"low", "unknown"} else "unsupported"
            missing = [requirement.required_evidence_type]

        return ClaimEvidenceMatch(
            match_id=f"claim_evidence_match:{uuid4().hex}",
            claim_id=claim.claim_id,
            requirement_id=requirement.requirement_id,
            matched=status == "supported",
            evidence_refs=refs,
            missing_evidence_types=missing,
            contradiction_refs=contradictions,
            match_status=status,
            notes=["LLM statement alone is not evidence.", "Evidence matching is deterministic and read-only."],
        )

    def _match_capability(
        self,
        claim: SelfClaim,
        obj: dict[str, Any],
        catalog: dict[str, Any],
    ) -> tuple[str, list[dict[str, Any]], list[str], list[dict[str, Any]]]:
        skill_id = obj.get("skill_id") or obj.get("capability_id")
        capabilities = catalog.get("capabilities") or {}
        record = capabilities.get(skill_id)
        if record is None:
            return _contradicted("capability_claim_without_registry", str(skill_id or "unknown"))
        claimed_status = obj.get("claimed_status") or obj.get("status") or "implemented"
        if claimed_status == "implemented" and record.status != "implemented":
            return _contradicted("capability_claim_exceeds_truth", str(skill_id))
        if obj.get("execution_enabled") and not record.execution_enabled:
            return _contradicted("capability_claim_exceeds_truth", str(skill_id))
        return "supported", [{"evidence_type": "capability_record", "skill_id": skill_id}, {"evidence_type": "capability_truth_report"}], [], []

    def _match_disabled_boundary(
        self,
        obj: dict[str, Any],
        catalog: dict[str, Any],
        contradiction_type: str,
        evidence_type: str,
    ) -> tuple[str, list[dict[str, Any]], list[str], list[dict[str, Any]]]:
        if obj.get("promoted") or obj.get("materialized") or obj.get("memory_entry_id") or obj.get("promotion_event_id"):
            return "unsupported", [], ["explicit_supported_boundary_event"], []
        boundary = catalog.get("candidate_boundary")
        return _contradicted(contradiction_type, evidence_type if boundary else "candidate_memory_boundary_unavailable")

    def _match_policy_claim(
        self,
        obj: dict[str, Any],
        catalog: dict[str, Any],
    ) -> tuple[str, list[dict[str, Any]], list[str], list[dict[str, Any]]]:
        unsafe = any(
            obj.get(key)
            for key in [
                "approval_implies_execution",
                "permission_grant_creation_allowed",
                "permission_escalation_allowed",
                "write_gate_enabled",
                "shell_gate_enabled",
                "network_gate_enabled",
            ]
        )
        if unsafe:
            return _contradicted("policy_claim_contradicts_gate", "policy_gate_truth_report")
        return "supported", [{"evidence_type": "policy_gate_truth_report"}], [], []

    def _match_runtime_claim(
        self,
        obj: dict[str, Any],
        catalog: dict[str, Any],
    ) -> tuple[str, list[dict[str, Any]], list[str], list[dict[str, Any]]]:
        unsafe = any(obj.get(key) for key in ["shell_enabled", "network_enabled", "mcp_enabled", "plugin_enabled", "external_harness_enabled"])
        if unsafe:
            return _contradicted("runtime_claim_contradicts_boundary", "runtime_boundary_truth_report")
        return "supported", [{"evidence_type": "runtime_boundary_truth_report"}], [], []


class SelfClaimConsistencyFindingService:
    def evaluate(
        self,
        claims: list[SelfClaim],
        matches: list[ClaimEvidenceMatch],
        request: SelfClaimConsistencyRequest,
        sources: list[SelfClaimSourceRef],
    ) -> list[SelfClaimConsistencyFinding]:
        findings: list[SelfClaimConsistencyFinding] = []
        if any(source.source_ref.get("source_status") == "blocked" for source in sources):
            findings.append(_finding("critical", "source_blocked", None, "Claim source is blocked to avoid private/raw payload exposure.", [], []))
            return findings
        claim_by_id = {item.claim_id: item for item in claims}
        for match in matches:
            claim = claim_by_id.get(match.claim_id)
            if claim is None:
                continue
            claim_ref = {"claim_id": claim.claim_id, "claim_type": claim.claim_type, "normalized_claim": claim.normalized_claim}
            if match.match_status == "supported":
                findings.append(
                    _finding("info", "claim_supported", claim.claim_id, "Claim is supported by OCEL/deep-self evidence.", match.evidence_refs, [], claim_ref)
                )
            elif match.match_status == "contradicted":
                findings.append(
                    _finding(
                        "error",
                        _finding_type_for_claim(claim, match),
                        claim.claim_id,
                        "Claim contradicts current OCEL/deep-self truth state.",
                        match.evidence_refs,
                        match.contradiction_refs,
                        claim_ref,
                    )
                )
            elif match.match_status == "unverifiable":
                severity = "warning"
                findings.append(
                    _finding(severity, "claim_unverifiable", claim.claim_id, "Claim is unverifiable without deterministic evidence.", [], [], claim_ref)
                )
            elif match.match_status == "unsupported":
                severity = "error" if claim.claim_type in HIGH_RISK_CLAIM_TYPES or claim.confidence == "high" else "warning"
                findings.append(
                    _finding(severity, "claim_unsupported", claim.claim_id, "Claim lacks required OCEL/deep-self evidence.", [], match.contradiction_refs, claim_ref)
                )
            elif match.match_status == "not_applicable":
                findings.append(_finding("info", "ok", claim.claim_id, "Claim does not require evidence.", [], [], claim_ref))
        if not claims and not findings:
            findings.append(_finding("info", "ok", None, "No claims were supplied for consistency checking.", [], []))
        return findings[: request.max_findings]


class SelfContradictionRegisterService:
    def build_register(
        self,
        findings: list[SelfClaimConsistencyFinding],
        claims: list[SelfClaim],
    ) -> SelfContradictionRegister:
        claim_by_id = {item.claim_id: item for item in claims}
        entries: list[ContradictionRegisterEntry] = []
        for finding in findings:
            if finding.severity not in {"error", "critical"}:
                continue
            claim = claim_by_id.get(finding.claim_id or "")
            entries.append(
                ContradictionRegisterEntry(
                    entry_id=f"contradiction_register_entry:{uuid4().hex}",
                    claim_id=finding.claim_id or "claim:unknown",
                    contradiction_type=finding.finding_type,
                    severity=finding.severity,
                    claim_summary=claim.normalized_claim if claim else finding.message,
                    contradicted_by=[dict(item) for item in finding.contradiction_refs],
                    source_ref=claim.source_ref.to_dict() if claim else {},
                    evidence_refs=[dict(item) for item in finding.evidence_refs],
                    status="open",
                    recommended_followup="Review the OCEL evidence gap; no automatic correction is performed.",
                    withdrawal_condition=finding.withdrawal_condition,
                )
            )
        return SelfContradictionRegister(
            register_id=f"self_contradiction_register:{uuid4().hex}",
            created_at=utc_now_iso(),
            entries=entries,
            open_count=sum(1 for item in entries if item.status == "open"),
            critical_count=sum(1 for item in entries if item.severity == "critical"),
            error_count=sum(1 for item in entries if item.severity == "error"),
            warning_count=sum(1 for item in entries if item.severity == "warning"),
            info_count=sum(1 for item in entries if item.severity == "info"),
        )


class SelfClaimConsistencyService:
    def __init__(
        self,
        *,
        source_service: SelfClaimSourceService | None = None,
        extractor: SelfClaimExtractor | None = None,
        requirement_mapper: ClaimEvidenceRequirementMapper | None = None,
        evidence_matcher: ClaimEvidenceMatcher | None = None,
        finding_service: SelfClaimConsistencyFindingService | None = None,
        register_service: SelfContradictionRegisterService | None = None,
    ) -> None:
        self.source_service = source_service or SelfClaimSourceService()
        self.extractor = extractor or SelfClaimExtractor()
        self.requirement_mapper = requirement_mapper or ClaimEvidenceRequirementMapper()
        self.evidence_matcher = evidence_matcher or ClaimEvidenceMatcher()
        self.finding_service = finding_service or SelfClaimConsistencyFindingService()
        self.register_service = register_service or SelfContradictionRegisterService()
        self.last_report: SelfClaimConsistencyReport | None = None
        self.last_register: SelfContradictionRegister | None = None

    def check_claim_consistency(
        self,
        request: SelfClaimConsistencyRequest | None = None,
    ) -> SelfClaimConsistencyReport:
        request = request or SelfClaimConsistencyRequest()
        sources = self.source_service.load_sources(request)
        claims = self.extractor.extract_claims(sources, request)
        requirements = self.requirement_mapper.map_requirements(claims)
        matches = self.evidence_matcher.match_evidence(claims, requirements, request)
        findings = self.finding_service.evaluate(claims, matches, request, sources)
        register = self.register_service.build_register(findings, claims)
        self.last_register = register
        status = _status_from_findings(findings)
        report = SelfClaimConsistencyReport(
            report_id=f"self_claim_consistency_report:{uuid4().hex}",
            created_at=utc_now_iso(),
            request=request,
            source_refs=sources,
            claims=claims,
            requirements=requirements,
            evidence_matches=matches,
            findings=findings,
            contradiction_register_id=register.register_id if register.entries else None,
            checked_claim_count=len(claims),
            supported_claim_count=sum(1 for item in matches if item.match_status == "supported"),
            unsupported_claim_count=sum(1 for item in matches if item.match_status == "unsupported"),
            contradicted_claim_count=sum(1 for item in matches if item.match_status == "contradicted"),
            unverifiable_claim_count=sum(1 for item in matches if item.match_status == "unverifiable"),
            status=status,
            limitations=[
                "Claim extraction is deterministic and structured-source first.",
                "Raw source bodies, raw transcripts, raw memory, and private payloads are not emitted.",
                "Unsupported free-form claims are not LLM judged.",
            ],
            withdrawal_conditions=[
                "Withdraw if LLM judgment is used as the sole claim truth source.",
                "Withdraw if claims are rewritten or automatically corrected.",
                "Withdraw if evidence sources, traces, memory, persona, overlay, or candidates are mutated.",
            ],
            validity_horizon="Valid until v0.21.8 Deep Self-Introspection Workbench changes claim visibility assumptions.",
        )
        self.last_report = report
        return report

    def build_contradiction_register(
        self,
        request: SelfClaimConsistencyRequest | None = None,
    ) -> SelfContradictionRegister:
        self.check_claim_consistency(request)
        return self.last_register or self.register_service.build_register([], [])

    def build_pig_report(self) -> dict[str, Any]:
        report = self.last_report or self.check_claim_consistency()
        return {
            "version": "v0.21.7",
            "layer": "deep_self_introspection",
            "subject": "self_claim_consistency",
            "principles": [
                "LLM statement is not evidence",
                "claim without OCEL evidence is not truth",
                "contradiction register is not auto-correction",
                "claim consistency check is not claim rewriting",
            ],
            "checks_capability_claims": True,
            "checks_execution_claims": True,
            "checks_memory_promotion_claims": True,
            "checks_canonical_truth_claims": True,
            "rewrites_claims": False,
            "mutates_memory": False,
            "uses_llm_judge": False,
            "status": report.status,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "self_claim_consistency_awareness",
            "version": "v0.21.7",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfCandidateMemoryBoundaryState",
                "SelfContextProjectionState",
                "SelfTraceIntegrityState",
                "SelfPolicyGateState",
                "SelfRuntimeBoundaryState",
                "SelfCapabilityTruthState",
            ],
            "target_read_models": [
                "SelfClaimConsistencyState",
                "SelfContradictionRegisterState",
                "SelfClaimEvidenceState",
                "SelfUnsupportedClaimState",
                "SelfUnverifiableClaimState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "canonical_store": "ocel",
        }

    def render_cli(
        self,
        command: str,
        report: SelfClaimConsistencyReport | None = None,
        register: SelfContradictionRegister | None = None,
        claim_id: str | None = None,
    ) -> str:
        report = report or self.last_report or self.check_claim_consistency()
        register = register or self.last_register or self.register_service.build_register(report.findings, report.claims)
        summaries = [
            _safe_summary(claim.normalized_claim)
            for claim in report.claims
            if claim_id is None or claim.claim_id == claim_id
        ][:10]
        lines = [
            "Self-Claim Consistency & Contradiction Register",
            f"command={command}",
            f"status={report.status}",
            f"checked_claim_count={report.checked_claim_count}",
            f"supported_claim_count={report.supported_claim_count}",
            f"unsupported_claim_count={report.unsupported_claim_count}",
            f"contradicted_claim_count={report.contradicted_claim_count}",
            f"unverifiable_claim_count={report.unverifiable_claim_count}",
            f"contradiction_register_open_count={register.open_count}",
            f"contradiction_register_error_count={register.error_count}",
            f"contradiction_register_critical_count={register.critical_count}",
            f"normalized_claim_summaries={'; '.join(summaries)}",
            "No claim rewrite performed.",
            "No memory mutation performed.",
            "No prompt mutation performed.",
            "No candidate promotion performed.",
            "No trace repair performed.",
            "raw_prompt_body_printed=False",
            "raw_transcript_printed=False",
            "raw_memory_persona_private_material_printed=False",
            "private_full_paths_printed=False",
            "raw_file_content_printed=False",
            "raw_secrets_printed=False",
        ]
        return "\n".join(lines)


def _source_ref(
    source_id: str,
    source_type: str,
    source_ref: dict[str, Any],
    redacted: bool,
    evidence_refs: list[dict[str, Any]],
) -> SelfClaimSourceRef:
    return SelfClaimSourceRef(
        source_id=source_id,
        source_type=source_type,
        source_ref=source_ref,
        redacted=redacted,
        raw_content_included=False,
        evidence_refs=evidence_refs,
    )


def _payload_private(payload: dict[str, Any] | None) -> bool:
    if not payload:
        return False
    return bool(payload.get("private_payload") or payload.get("raw_prompt_body") or payload.get("raw_transcript") or payload.get("raw_memory_content"))


def _safe_summary(value: str, *, limit: int = 160) -> str:
    compact = " ".join(value.replace("\r", " ").replace("\n", " ").split())
    return compact[:limit]


def _default_predicate(claim_type: str) -> str:
    return {
        "capability_claim": "implemented",
        "execution_claim": "executed",
        "read_claim": "read",
        "search_claim": "searched",
        "verification_claim": "verified",
        "promotion_claim": "promoted",
        "memory_claim": "memory_written",
        "materialization_claim": "materialized",
        "canonical_truth_claim": "is_canonical_truth",
        "policy_claim": "policy_allows",
        "runtime_boundary_claim": "runtime_allows",
        "external_contact_claim": "external_contact",
        "raw_transcript_claim": "raw_transcript_as_state",
        "no_action_claim": "no_action_valid",
    }.get(claim_type, "unsupported")


def _requirement_for_claim(claim: SelfClaim) -> ClaimEvidenceRequirement:
    object_types: list[str] = []
    event_types: list[str] = []
    relation_types: list[str] = []
    report_types: list[str] = []
    evidence_type = "ocel_evidence"
    allow_report_only = False
    allow_candidate_only = False
    if claim.claim_type == "capability_claim":
        object_types = ["capability_record"]
        report_types = ["capability_truth_report"]
        evidence_type = "capability_truth"
    elif claim.claim_type == "execution_claim":
        object_types = ["execution_envelope", "ocel_event_ref"]
        event_types = ["execution_event"]
        evidence_type = "execution_trace"
    elif claim.claim_type == "read_claim":
        object_types = ["text_slice", "workspace_file"]
        event_types = ["self_text_read_completed"]
        evidence_type = "read_trace"
    elif claim.claim_type == "search_claim":
        object_types = ["workspace_search_result", "workspace_search_match"]
        evidence_type = "search_trace"
    elif claim.claim_type == "verification_claim":
        report_types = ["verification_report"]
        allow_report_only = True
        evidence_type = "verification_report"
    elif claim.claim_type in {"promotion_claim", "memory_claim"}:
        object_types = ["candidate_ref", "memory_entry_ref"]
        event_types = ["promotion_event", "memory_write_event"]
        evidence_type = "explicit_boundary_event"
    elif claim.claim_type == "materialization_claim":
        event_types = ["materialization_event"]
        evidence_type = "materialization_event"
    elif claim.claim_type == "canonical_truth_claim":
        object_types = ["ocel_object_ref"]
        evidence_type = "canonical_truth_evidence"
    else:
        evidence_type = claim.claim_type
    return ClaimEvidenceRequirement(
        requirement_id=f"claim_evidence_requirement:{claim.claim_id}",
        claim_id=claim.claim_id,
        required_evidence_type=evidence_type,
        required_object_types=object_types,
        required_event_types=event_types,
        required_relation_types=relation_types,
        required_report_types=report_types,
        allow_report_only=allow_report_only,
        allow_candidate_only=allow_candidate_only,
        notes=["Claim without OCEL/deep-self evidence is not truth."],
    )


def _match_required_pair(
    obj: dict[str, Any],
    first_type: str,
    second_type: str,
    first_key: str,
    second_key: str,
    first_contradiction: str,
    second_contradiction: str,
) -> tuple[str, list[dict[str, Any]], list[str], list[dict[str, Any]]]:
    missing: list[str] = []
    contradictions: list[dict[str, Any]] = []
    refs: list[dict[str, Any]] = []
    if obj.get(first_key):
        refs.append({"evidence_type": first_type, first_key: obj[first_key]})
    else:
        missing.append(first_type)
        contradictions.append({"contradiction_type": first_contradiction, "missing": first_type})
    if obj.get(second_key):
        refs.append({"evidence_type": second_type, second_key: obj[second_key]})
    else:
        missing.append(second_type)
        contradictions.append({"contradiction_type": second_contradiction, "missing": second_type})
    if missing:
        return "contradicted", refs, missing, contradictions
    return "supported", refs, [], []


def _match_required_values(
    obj: dict[str, Any],
    keys: list[str],
    contradiction_type: str,
) -> tuple[str, list[dict[str, Any]], list[str], list[dict[str, Any]]]:
    missing = [key for key in keys if not obj.get(key)]
    refs = [{"evidence_type": key, key: obj[key]} for key in keys if obj.get(key)]
    if missing:
        return "contradicted", refs, missing, [{"contradiction_type": contradiction_type, "missing": ",".join(missing)}]
    return "supported", refs, [], []


def _contradicted(reason: str, source: str) -> tuple[str, list[dict[str, Any]], list[str], list[dict[str, Any]]]:
    return "contradicted", [], [], [{"contradiction_type": reason, "source": source}]


def _finding_type_for_claim(claim: SelfClaim, match: ClaimEvidenceMatch) -> str:
    if match.contradiction_refs:
        found = match.contradiction_refs[0].get("contradiction_type")
        if found:
            return str(found)
    return {
        "capability_claim": "capability_claim_exceeds_truth",
        "execution_claim": "execution_claim_without_envelope",
        "promotion_claim": "promotion_claim_contradicts_boundary",
        "memory_claim": "memory_claim_contradicts_boundary",
        "materialization_claim": "materialization_claim_contradicts_boundary",
        "external_contact_claim": "external_contact_claim_contradicts_runtime",
        "canonical_truth_claim": "canonical_truth_claim_on_candidate",
        "policy_claim": "policy_claim_contradicts_gate",
        "runtime_boundary_claim": "runtime_claim_contradicts_boundary",
    }.get(claim.claim_type, "claim_contradicted")


def _finding(
    severity: str,
    finding_type: str,
    claim_id: str | None,
    message: str,
    evidence_refs: list[dict[str, Any]],
    contradiction_refs: list[dict[str, Any]],
    claim_ref: dict[str, Any] | None = None,
) -> SelfClaimConsistencyFinding:
    return SelfClaimConsistencyFinding(
        finding_id=f"self_claim_consistency_finding:{uuid4().hex}",
        severity=severity,
        finding_type=finding_type,
        claim_id=claim_id,
        message=message,
        claim_ref=claim_ref,
        evidence_refs=evidence_refs,
        contradiction_refs=contradiction_refs,
        withdrawal_condition="Withdraw if claim classification rewrites claims or mutates evidence sources.",
    )


def _status_from_findings(findings: list[SelfClaimConsistencyFinding]) -> ClaimConsistencyStatus:
    if any(item.finding_type == "source_blocked" or item.severity == "critical" for item in findings):
        return "blocked"
    if any(item.severity == "error" for item in findings):
        return "failed"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed"
