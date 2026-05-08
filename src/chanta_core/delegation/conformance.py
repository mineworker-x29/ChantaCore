from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any
from uuid import uuid4

from chanta_core.delegation.errors import (
    DelegationConformanceContractError,
    DelegationConformanceFindingError,
    DelegationConformanceResultError,
    DelegationConformanceRuleError,
    DelegationConformanceRunError,
)
from chanta_core.delegation.ids import (
    new_delegation_conformance_contract_id,
    new_delegation_conformance_finding_id,
    new_delegation_conformance_result_id,
    new_delegation_conformance_rule_id,
    new_delegation_conformance_run_id,
)
from chanta_core.delegation.models import DelegatedProcessRun, DelegationPacket
from chanta_core.delegation.sidechain import SidechainContext, SidechainReturnEnvelope
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


CONTRACT_TYPES = {
    "delegation_structure",
    "sidechain_context",
    "permission_boundary",
    "transcript_boundary",
    "return_envelope",
    "safety_reference",
    "manual",
    "other",
}
LIFECYCLE_STATUSES = {"active", "draft", "deprecated", "archived", "withdrawn"}
SEVERITIES = {"info", "low", "medium", "high", "critical"}
RULE_TYPES = {
    "packet_exists",
    "delegated_run_uses_packet",
    "sidechain_derived_from_packet",
    "no_full_parent_transcript",
    "no_permission_inheritance",
    "summary_only_return",
    "no_full_child_transcript",
    "safety_refs_preserved",
    "allowed_capabilities_respected",
    "parent_child_link_exists",
    "required_packet_fields_present",
    "return_envelope_exists",
    "isolation_mode_allowed",
    "manual",
    "other",
}
RUN_STATUSES = {"started", "completed", "failed", "skipped", "error"}
FINDING_STATUSES = {"passed", "failed", "warning", "skipped", "inconclusive", "error"}
RESULT_STATUSES = {"passed", "failed", "needs_review", "inconclusive", "skipped", "error"}
DEFAULT_RULE_TYPES = [
    "packet_exists",
    "delegated_run_uses_packet",
    "sidechain_derived_from_packet",
    "no_full_parent_transcript",
    "no_permission_inheritance",
    "summary_only_return",
    "no_full_child_transcript",
    "safety_refs_preserved",
    "required_packet_fields_present",
]


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


def _require_optional_value(value: str | None, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value is not None:
        _require_value(value, allowed, error_type, field_name)


def _require_probability(value: float | None, error_type: type[Exception], field_name: str) -> None:
    if value is None:
        return
    if value < 0.0 or value > 1.0:
        raise error_type(f"{field_name} must be between 0.0 and 1.0")


@dataclass(frozen=True)
class DelegationConformanceContract:
    contract_id: str
    contract_name: str
    contract_type: str
    description: str | None
    status: str
    severity: str | None
    created_at: str
    updated_at: str
    contract_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.contract_name:
            raise DelegationConformanceContractError("contract_name is required")
        _require_value(self.contract_type, CONTRACT_TYPES, DelegationConformanceContractError, "contract_type")
        _require_value(self.status, LIFECYCLE_STATUSES, DelegationConformanceContractError, "status")
        _require_optional_value(self.severity, SEVERITIES, DelegationConformanceContractError, "severity")

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "contract_name": self.contract_name,
            "contract_type": self.contract_type,
            "description": self.description,
            "status": self.status,
            "severity": self.severity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "contract_attrs": self.contract_attrs,
        }


@dataclass(frozen=True)
class DelegationConformanceRule:
    rule_id: str
    contract_id: str
    rule_type: str
    description: str
    required: bool
    severity: str | None
    expected_value: str | None
    status: str
    rule_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.rule_type, RULE_TYPES, DelegationConformanceRuleError, "rule_type")
        _require_value(self.status, LIFECYCLE_STATUSES, DelegationConformanceRuleError, "status")
        _require_optional_value(self.severity, SEVERITIES, DelegationConformanceRuleError, "severity")

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule_id": self.rule_id,
            "contract_id": self.contract_id,
            "rule_type": self.rule_type,
            "description": self.description,
            "required": self.required,
            "severity": self.severity,
            "expected_value": self.expected_value,
            "status": self.status,
            "rule_attrs": self.rule_attrs,
        }


@dataclass(frozen=True)
class DelegationConformanceRun:
    run_id: str
    contract_id: str
    packet_id: str | None
    delegated_run_id: str | None
    sidechain_context_id: str | None
    return_envelope_id: str | None
    status: str
    started_at: str
    completed_at: str | None
    run_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, RUN_STATUSES, DelegationConformanceRunError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "contract_id": self.contract_id,
            "packet_id": self.packet_id,
            "delegated_run_id": self.delegated_run_id,
            "sidechain_context_id": self.sidechain_context_id,
            "return_envelope_id": self.return_envelope_id,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "run_attrs": self.run_attrs,
        }


@dataclass(frozen=True)
class DelegationConformanceFinding:
    finding_id: str
    run_id: str
    rule_id: str | None
    rule_type: str
    status: str
    severity: str | None
    message: str
    subject_type: str | None
    subject_ref: str | None
    evidence_refs: list[dict[str, Any]]
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.rule_type, RULE_TYPES, DelegationConformanceFindingError, "rule_type")
        _require_value(self.status, FINDING_STATUSES, DelegationConformanceFindingError, "status")
        _require_optional_value(self.severity, SEVERITIES, DelegationConformanceFindingError, "severity")

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "run_id": self.run_id,
            "rule_id": self.rule_id,
            "rule_type": self.rule_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "subject_type": self.subject_type,
            "subject_ref": self.subject_ref,
            "evidence_refs": self.evidence_refs,
            "created_at": self.created_at,
            "finding_attrs": self.finding_attrs,
        }


@dataclass(frozen=True)
class DelegationConformanceResult:
    result_id: str
    run_id: str
    contract_id: str
    status: str
    score: float | None
    confidence: float | None
    passed_finding_ids: list[str]
    failed_finding_ids: list[str]
    warning_finding_ids: list[str]
    skipped_finding_ids: list[str]
    reason: str | None
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, RESULT_STATUSES, DelegationConformanceResultError, "status")
        _require_probability(self.score, DelegationConformanceResultError, "score")
        _require_probability(self.confidence, DelegationConformanceResultError, "confidence")

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "run_id": self.run_id,
            "contract_id": self.contract_id,
            "status": self.status,
            "score": self.score,
            "confidence": self.confidence,
            "passed_finding_ids": self.passed_finding_ids,
            "failed_finding_ids": self.failed_finding_ids,
            "warning_finding_ids": self.warning_finding_ids,
            "skipped_finding_ids": self.skipped_finding_ids,
            "reason": self.reason,
            "created_at": self.created_at,
            "result_attrs": self.result_attrs,
        }


class DelegationConformanceService:
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

    def register_contract(
        self,
        *,
        contract_name: str,
        contract_type: str,
        description: str | None = None,
        status: str = "active",
        severity: str | None = None,
        contract_attrs: dict[str, Any] | None = None,
    ) -> DelegationConformanceContract:
        now = utc_now_iso()
        contract = DelegationConformanceContract(
            contract_id=new_delegation_conformance_contract_id(),
            contract_name=contract_name,
            contract_type=contract_type,
            description=description,
            status=status,
            severity=severity,
            created_at=now,
            updated_at=now,
            contract_attrs=dict(contract_attrs or {}),
        )
        self._record_event(
            "delegation_conformance_contract_registered",
            contract=contract,
            event_attrs={"contract_type": contract.contract_type, "status": contract.status},
            event_relations=[("contract_object", contract.contract_id)],
            object_relations=[],
        )
        return contract

    def register_rule(
        self,
        *,
        contract_id: str,
        rule_type: str,
        description: str,
        required: bool = True,
        severity: str | None = None,
        expected_value: str | None = None,
        status: str = "active",
        rule_attrs: dict[str, Any] | None = None,
    ) -> DelegationConformanceRule:
        rule = DelegationConformanceRule(
            rule_id=new_delegation_conformance_rule_id(),
            contract_id=contract_id,
            rule_type=rule_type,
            description=description,
            required=required,
            severity=severity,
            expected_value=expected_value,
            status=status,
            rule_attrs=dict(rule_attrs or {}),
        )
        self._record_event(
            "delegation_conformance_rule_registered",
            rule=rule,
            event_attrs={"rule_type": rule.rule_type, "required": rule.required},
            event_relations=[("rule_object", rule.rule_id), ("contract_object", contract_id)],
            object_relations=[(rule.rule_id, contract_id, "belongs_to_contract")],
        )
        return rule

    def register_default_rules(self, *, contract_id: str) -> list[DelegationConformanceRule]:
        descriptions = {
            "packet_exists": "A delegation packet must be present.",
            "delegated_run_uses_packet": "Delegated run must reference the packet.",
            "sidechain_derived_from_packet": "Sidechain context must derive from the packet.",
            "no_full_parent_transcript": "Sidechain context must exclude full parent transcript.",
            "no_permission_inheritance": "Delegated run and sidechain must not inherit permissions.",
            "summary_only_return": "Return envelope must be summary-only.",
            "no_full_child_transcript": "Return envelope must not contain full child transcript.",
            "safety_refs_preserved": "Packet safety references should be preserved in sidechain context.",
            "required_packet_fields_present": "Required packet fields must be present.",
        }
        severities = {
            "packet_exists": "critical",
            "delegated_run_uses_packet": "high",
            "sidechain_derived_from_packet": "high",
            "no_full_parent_transcript": "critical",
            "no_permission_inheritance": "critical",
            "summary_only_return": "high",
            "no_full_child_transcript": "critical",
            "safety_refs_preserved": "medium",
            "required_packet_fields_present": "high",
        }
        return [
            self.register_rule(
                contract_id=contract_id,
                rule_type=rule_type,
                description=descriptions[rule_type],
                required=True,
                severity=severities[rule_type],
                expected_value="true",
            )
            for rule_type in DEFAULT_RULE_TYPES
        ]

    def start_run(
        self,
        *,
        contract_id: str,
        packet_id: str | None = None,
        delegated_run_id: str | None = None,
        sidechain_context_id: str | None = None,
        return_envelope_id: str | None = None,
        run_attrs: dict[str, Any] | None = None,
    ) -> DelegationConformanceRun:
        run = DelegationConformanceRun(
            run_id=new_delegation_conformance_run_id(),
            contract_id=contract_id,
            packet_id=packet_id,
            delegated_run_id=delegated_run_id,
            sidechain_context_id=sidechain_context_id,
            return_envelope_id=return_envelope_id,
            status="started",
            started_at=utc_now_iso(),
            completed_at=None,
            run_attrs={**dict(run_attrs or {}), "runtime_effect": False},
        )
        self._record_run_event("delegation_conformance_run_started", run=run, event_attrs={})
        return run

    def record_finding(
        self,
        *,
        run_id: str,
        rule_type: str,
        status: str,
        message: str,
        rule_id: str | None = None,
        severity: str | None = None,
        subject_type: str | None = None,
        subject_ref: str | None = None,
        evidence_refs: list[dict[str, Any]] | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> DelegationConformanceFinding:
        finding = DelegationConformanceFinding(
            finding_id=new_delegation_conformance_finding_id(),
            run_id=run_id,
            rule_id=rule_id,
            rule_type=rule_type,
            status=status,
            severity=severity,
            message=message,
            subject_type=subject_type,
            subject_ref=subject_ref,
            evidence_refs=list(evidence_refs or []),
            created_at=utc_now_iso(),
            finding_attrs=dict(finding_attrs or {}),
        )
        event_relations = [
            ("finding_object", finding.finding_id),
            ("run_object", run_id),
            *self._optional_relation("rule_object", rule_id),
            *self._subject_relation(subject_type, subject_ref),
        ]
        object_relations = [(finding.finding_id, run_id, "belongs_to_run")]
        if rule_id:
            object_relations.append((finding.finding_id, rule_id, "checks_rule"))
        self._record_event(
            "delegation_conformance_finding_recorded",
            finding=finding,
            event_attrs={"rule_type": rule_type, "status": status},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return finding

    def record_result(
        self,
        *,
        run_id: str,
        contract_id: str,
        status: str,
        score: float | None = None,
        confidence: float | None = None,
        passed_finding_ids: list[str] | None = None,
        failed_finding_ids: list[str] | None = None,
        warning_finding_ids: list[str] | None = None,
        skipped_finding_ids: list[str] | None = None,
        reason: str | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> DelegationConformanceResult:
        result = DelegationConformanceResult(
            result_id=new_delegation_conformance_result_id(),
            run_id=run_id,
            contract_id=contract_id,
            status=status,
            score=score,
            confidence=confidence,
            passed_finding_ids=list(passed_finding_ids or []),
            failed_finding_ids=list(failed_finding_ids or []),
            warning_finding_ids=list(warning_finding_ids or []),
            skipped_finding_ids=list(skipped_finding_ids or []),
            reason=reason,
            created_at=utc_now_iso(),
            result_attrs=dict(result_attrs or {}),
        )
        finding_relations = [
            ("finding_object", finding_id)
            for finding_id in [
                *result.passed_finding_ids,
                *result.failed_finding_ids,
                *result.warning_finding_ids,
                *result.skipped_finding_ids,
            ]
        ]
        self._record_event(
            "delegation_conformance_result_recorded",
            result=result,
            event_attrs={"status": status, "score": score, "confidence": confidence},
            event_relations=[
                ("result_object", result.result_id),
                ("run_object", run_id),
                ("contract_object", contract_id),
                *finding_relations,
            ],
            object_relations=[
                (result.result_id, run_id, "result_of_run"),
                (result.result_id, contract_id, "uses_contract"),
            ],
        )
        return result

    def complete_run(
        self,
        *,
        run: DelegationConformanceRun,
        reason: str | None = None,
    ) -> DelegationConformanceRun:
        updated = replace(run, status="completed", completed_at=utc_now_iso())
        self._record_run_event("delegation_conformance_run_completed", run=updated, event_attrs={"reason": reason})
        return updated

    def fail_run(
        self,
        *,
        run: DelegationConformanceRun,
        failure: dict[str, Any] | None = None,
        reason: str | None = None,
    ) -> DelegationConformanceRun:
        updated = replace(
            run,
            status="failed",
            completed_at=utc_now_iso(),
            run_attrs={**run.run_attrs, "failure": dict(failure or {})},
        )
        self._record_run_event(
            "delegation_conformance_run_failed",
            run=updated,
            event_attrs={"reason": reason, "failure": failure},
        )
        return updated

    def skip_run(
        self,
        *,
        run: DelegationConformanceRun,
        reason: str | None = None,
    ) -> DelegationConformanceRun:
        updated = replace(run, status="skipped", completed_at=utc_now_iso())
        self._record_run_event("delegation_conformance_run_skipped", run=updated, event_attrs={"reason": reason})
        return updated

    def evaluate_delegation_conformance(
        self,
        *,
        contract: DelegationConformanceContract,
        rules: list[DelegationConformanceRule],
        packet: DelegationPacket | None = None,
        delegated_run: DelegatedProcessRun | None = None,
        sidechain_context: SidechainContext | None = None,
        return_envelope: SidechainReturnEnvelope | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> DelegationConformanceResult:
        run = self.start_run(
            contract_id=contract.contract_id,
            packet_id=packet.packet_id if packet else None,
            delegated_run_id=delegated_run.delegated_run_id if delegated_run else None,
            sidechain_context_id=sidechain_context.sidechain_context_id if sidechain_context else None,
            return_envelope_id=return_envelope.envelope_id if return_envelope else None,
            run_attrs={"structural_check_only": True},
        )
        findings = [
            self._evaluate_rule(
                run=run,
                rule=rule,
                packet=packet,
                delegated_run=delegated_run,
                sidechain_context=sidechain_context,
                return_envelope=return_envelope,
            )
            for rule in rules
            if rule.status == "active"
        ]
        result_status, score, reason = self._derive_result(rules=rules, findings=findings)
        result = self.record_result(
            run_id=run.run_id,
            contract_id=contract.contract_id,
            status=result_status,
            score=score,
            confidence=score if score is not None else None,
            passed_finding_ids=[item.finding_id for item in findings if item.status == "passed"],
            failed_finding_ids=[item.finding_id for item in findings if item.status == "failed"],
            warning_finding_ids=[item.finding_id for item in findings if item.status == "warning"],
            skipped_finding_ids=[item.finding_id for item in findings if item.status in {"skipped", "inconclusive"}],
            reason=reason,
            result_attrs={**dict(result_attrs or {}), "structural_check_only": True},
        )
        self.complete_run(run=run, reason="delegation conformance evaluation completed")
        return result

    def _evaluate_rule(
        self,
        *,
        run: DelegationConformanceRun,
        rule: DelegationConformanceRule,
        packet: DelegationPacket | None,
        delegated_run: DelegatedProcessRun | None,
        sidechain_context: SidechainContext | None,
        return_envelope: SidechainReturnEnvelope | None,
    ) -> DelegationConformanceFinding:
        evaluators = {
            "packet_exists": self._check_packet_exists,
            "delegated_run_uses_packet": self._check_delegated_run_uses_packet,
            "sidechain_derived_from_packet": self._check_sidechain_derived_from_packet,
            "no_full_parent_transcript": self._check_no_full_parent_transcript,
            "no_permission_inheritance": self._check_no_permission_inheritance,
            "summary_only_return": self._check_summary_only_return,
            "no_full_child_transcript": self._check_no_full_child_transcript,
            "safety_refs_preserved": self._check_safety_refs_preserved,
            "required_packet_fields_present": self._check_required_packet_fields_present,
        }
        evaluator = evaluators.get(rule.rule_type)
        if evaluator is None:
            status, message, subject_type, subject_ref, evidence_refs = (
                "skipped",
                f"Rule {rule.rule_type} is not implemented in the default structural evaluator.",
                None,
                None,
                [],
            )
        else:
            status, message, subject_type, subject_ref, evidence_refs = evaluator(
                packet=packet,
                delegated_run=delegated_run,
                sidechain_context=sidechain_context,
                return_envelope=return_envelope,
            )
        return self.record_finding(
            run_id=run.run_id,
            rule_id=rule.rule_id,
            rule_type=rule.rule_type,
            status=status,
            severity=rule.severity,
            message=message,
            subject_type=subject_type,
            subject_ref=subject_ref,
            evidence_refs=evidence_refs,
            finding_attrs={"required": rule.required},
        )

    @staticmethod
    def _check_packet_exists(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        packet = subjects["packet"]
        if packet is None:
            return "failed", "Delegation packet is missing.", "delegation_packet", None, []
        return "passed", "Delegation packet is present.", "delegation_packet", packet.packet_id, []

    @staticmethod
    def _check_delegated_run_uses_packet(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        packet = subjects["packet"]
        delegated_run = subjects["delegated_run"]
        if packet is None or delegated_run is None:
            return "inconclusive", "Packet or delegated run is missing.", "delegated_process_run", None, []
        if delegated_run.packet_id == packet.packet_id:
            return "passed", "Delegated run references the packet.", "delegated_process_run", delegated_run.delegated_run_id, []
        return (
            "failed",
            "Delegated run references a different packet.",
            "delegated_process_run",
            delegated_run.delegated_run_id,
            [{"expected_packet_id": packet.packet_id, "actual_packet_id": delegated_run.packet_id}],
        )

    @staticmethod
    def _check_sidechain_derived_from_packet(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        packet = subjects["packet"]
        sidechain_context = subjects["sidechain_context"]
        if packet is None or sidechain_context is None:
            return "inconclusive", "Packet or sidechain context is missing.", "sidechain_context", None, []
        if sidechain_context.packet_id == packet.packet_id:
            return "passed", "Sidechain context derives from the packet.", "sidechain_context", sidechain_context.sidechain_context_id, []
        return (
            "failed",
            "Sidechain context references a different packet.",
            "sidechain_context",
            sidechain_context.sidechain_context_id,
            [{"expected_packet_id": packet.packet_id, "actual_packet_id": sidechain_context.packet_id}],
        )

    @staticmethod
    def _check_no_full_parent_transcript(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        sidechain_context = subjects["sidechain_context"]
        if sidechain_context is None:
            return "inconclusive", "Sidechain context is missing.", "sidechain_context", None, []
        if sidechain_context.contains_full_parent_transcript is False:
            return "passed", "Sidechain context excludes the full parent transcript.", "sidechain_context", sidechain_context.sidechain_context_id, []
        return "failed", "Sidechain context contains full parent transcript.", "sidechain_context", sidechain_context.sidechain_context_id, []

    @staticmethod
    def _check_no_permission_inheritance(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        delegated_run = subjects["delegated_run"]
        sidechain_context = subjects["sidechain_context"]
        if delegated_run is None and sidechain_context is None:
            return "inconclusive", "Delegated run and sidechain context are both missing.", None, None, []
        inherited = []
        if delegated_run is not None and delegated_run.inherited_permissions is not False:
            inherited.append(("delegated_process_run", delegated_run.delegated_run_id))
        if sidechain_context is not None and sidechain_context.inherited_permissions is not False:
            inherited.append(("sidechain_context", sidechain_context.sidechain_context_id))
        if inherited:
            subject_type, subject_ref = inherited[0]
            return "failed", "Permission inheritance is present.", subject_type, subject_ref, []
        subject_type = "delegated_process_run" if delegated_run else "sidechain_context"
        subject_ref = delegated_run.delegated_run_id if delegated_run else sidechain_context.sidechain_context_id
        return "passed", "Permissions are not inherited.", subject_type, subject_ref, []

    @staticmethod
    def _check_summary_only_return(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        return_envelope = subjects["return_envelope"]
        if return_envelope is None:
            return "inconclusive", "Return envelope is missing.", "sidechain_return_envelope", None, []
        if return_envelope.contains_full_child_transcript is False:
            return "passed", "Return envelope is summary-only.", "sidechain_return_envelope", return_envelope.envelope_id, []
        return "failed", "Return envelope includes full child transcript.", "sidechain_return_envelope", return_envelope.envelope_id, []

    @staticmethod
    def _check_no_full_child_transcript(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        return DelegationConformanceService._check_summary_only_return(**subjects)

    @staticmethod
    def _check_safety_refs_preserved(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        packet = subjects["packet"]
        sidechain_context = subjects["sidechain_context"]
        if packet is None:
            return "inconclusive", "Packet is missing.", "delegation_packet", None, []
        packet_refs = DelegationConformanceService._packet_safety_refs(packet)
        if not packet_refs:
            return "passed", "Packet has no safety references to preserve.", "delegation_packet", packet.packet_id, []
        if sidechain_context is None:
            return "warning", "Packet has safety references but sidechain context is missing.", "delegation_packet", packet.packet_id, []
        present_refs = set(sidechain_context.safety_ref_ids or [])
        missing_refs = sorted(set(packet_refs) - present_refs)
        if not missing_refs:
            return "passed", "Packet safety references are represented in sidechain context.", "sidechain_context", sidechain_context.sidechain_context_id, []
        return (
            "warning",
            "Packet safety references are missing from sidechain context.",
            "sidechain_context",
            sidechain_context.sidechain_context_id,
            [{"missing_ref_id": item} for item in missing_refs],
        )

    @staticmethod
    def _check_required_packet_fields_present(**subjects: Any) -> tuple[str, str, str | None, str | None, list[dict[str, Any]]]:
        packet = subjects["packet"]
        if packet is None:
            return "failed", "Delegation packet is missing required fields.", "delegation_packet", None, []
        if packet.goal:
            return "passed", "Delegation packet required fields are present.", "delegation_packet", packet.packet_id, []
        return "failed", "Delegation packet goal is missing.", "delegation_packet", packet.packet_id, []

    @staticmethod
    def _derive_result(
        *,
        rules: list[DelegationConformanceRule],
        findings: list[DelegationConformanceFinding],
    ) -> tuple[str, float | None, str]:
        active_rules_by_type = {rule.rule_type: rule for rule in rules if rule.status == "active"}
        required_findings = [item for item in findings if active_rules_by_type.get(item.rule_type, None) and active_rules_by_type[item.rule_type].required]
        passed_required = sum(1 for item in required_findings if item.status == "passed")
        total_required = len(required_findings)
        score = round(passed_required / total_required, 6) if total_required else None
        if any(item.status == "failed" for item in required_findings):
            return "failed", score, "At least one required conformance finding failed."
        if any(item.status in {"warning", "error"} for item in findings):
            return "needs_review", score, "Conformance produced warnings or errors."
        if any(item.status == "inconclusive" for item in required_findings):
            return "inconclusive", score, "Required conformance checks were inconclusive."
        if required_findings and all(item.status == "passed" for item in required_findings):
            return "passed", score, "All required conformance checks passed."
        return "skipped", score, "No active required conformance checks were evaluated."

    def _record_run_event(
        self,
        event_activity: str,
        *,
        run: DelegationConformanceRun,
        event_attrs: dict[str, Any],
    ) -> None:
        event_relations, object_relations = self._run_context_relations(run)
        self._record_event(
            event_activity,
            run=run,
            event_attrs={"status": run.status, **event_attrs},
            event_relations=[("run_object", run.run_id), ("contract_object", run.contract_id), *event_relations],
            object_relations=[(run.run_id, run.contract_id, "uses_contract"), *object_relations],
        )

    def _record_event(
        self,
        event_activity: str,
        *,
        contract: DelegationConformanceContract | None = None,
        rule: DelegationConformanceRule | None = None,
        run: DelegationConformanceRun | None = None,
        finding: DelegationConformanceFinding | None = None,
        result: DelegationConformanceResult | None = None,
        event_attrs: dict[str, Any],
        event_relations: list[tuple[str, str | None]],
        object_relations: list[tuple[str, str, str]],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "source_runtime": "chanta_core",
                "observability_only": True,
                "delegation_conformance_structural_only": True,
                "runtime_effect": False,
                "enforcement_enabled": False,
            },
        )
        objects = self._objects_for_event(contract=contract, rule=rule, run=run, finding=finding, result=result)
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in event_relations
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source, target_object_id=target, qualifier=qualifier)
            for source, target, qualifier in object_relations
            if source and target
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))

    def _objects_for_event(
        self,
        *,
        contract: DelegationConformanceContract | None,
        rule: DelegationConformanceRule | None,
        run: DelegationConformanceRun | None,
        finding: DelegationConformanceFinding | None,
        result: DelegationConformanceResult | None,
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if contract is not None:
            objects.append(self._contract_object(contract))
        if rule is not None:
            objects.append(self._rule_object(rule))
        if run is not None:
            objects.append(self._run_object(run))
        if finding is not None:
            objects.append(self._finding_object(finding))
        if result is not None:
            objects.append(self._result_object(result))
        return objects

    @staticmethod
    def _contract_object(contract: DelegationConformanceContract) -> OCELObject:
        return OCELObject(
            object_id=contract.contract_id,
            object_type="delegation_conformance_contract",
            object_attrs={**contract.to_dict(), "object_key": contract.contract_id, "display_name": contract.contract_name},
        )

    @staticmethod
    def _rule_object(rule: DelegationConformanceRule) -> OCELObject:
        return OCELObject(
            object_id=rule.rule_id,
            object_type="delegation_conformance_rule",
            object_attrs={**rule.to_dict(), "object_key": rule.rule_id, "display_name": rule.rule_type},
        )

    @staticmethod
    def _run_object(run: DelegationConformanceRun) -> OCELObject:
        return OCELObject(
            object_id=run.run_id,
            object_type="delegation_conformance_run",
            object_attrs={**run.to_dict(), "object_key": run.run_id, "display_name": run.status},
        )

    @staticmethod
    def _finding_object(finding: DelegationConformanceFinding) -> OCELObject:
        return OCELObject(
            object_id=finding.finding_id,
            object_type="delegation_conformance_finding",
            object_attrs={**finding.to_dict(), "object_key": finding.finding_id, "display_name": finding.rule_type},
        )

    @staticmethod
    def _result_object(result: DelegationConformanceResult) -> OCELObject:
        return OCELObject(
            object_id=result.result_id,
            object_type="delegation_conformance_result",
            object_attrs={**result.to_dict(), "object_key": result.result_id, "display_name": result.status},
        )

    def _run_context_relations(self, run: DelegationConformanceRun) -> tuple[list[tuple[str, str]], list[tuple[str, str, str]]]:
        event_relations: list[tuple[str, str]] = []
        object_relations: list[tuple[str, str, str]] = []
        if run.packet_id:
            event_relations.append(("packet_object", run.packet_id))
            object_relations.append((run.run_id, run.packet_id, "checks_packet"))
        if run.delegated_run_id:
            event_relations.append(("delegated_run_object", run.delegated_run_id))
            object_relations.append((run.run_id, run.delegated_run_id, "checks_delegated_run"))
        if run.sidechain_context_id:
            event_relations.append(("sidechain_context_object", run.sidechain_context_id))
            object_relations.append((run.run_id, run.sidechain_context_id, "checks_sidechain_context"))
        if run.return_envelope_id:
            event_relations.append(("return_envelope_object", run.return_envelope_id))
            object_relations.append((run.run_id, run.return_envelope_id, "checks_return_envelope"))
        return event_relations, object_relations

    @staticmethod
    def _subject_relation(subject_type: str | None, subject_ref: str | None) -> list[tuple[str, str]]:
        if not subject_ref:
            return []
        qualifiers = {
            "delegation_packet": "packet_object",
            "delegated_process_run": "delegated_run_object",
            "sidechain_context": "sidechain_context_object",
            "sidechain_return_envelope": "return_envelope_object",
        }
        qualifier = qualifiers.get(str(subject_type or ""))
        if qualifier is None:
            return []
        return [(qualifier, subject_ref)]

    @staticmethod
    def _optional_relation(qualifier: str, object_id: str | None) -> list[tuple[str, str]]:
        if object_id:
            return [(qualifier, object_id)]
        return []

    @staticmethod
    def _packet_safety_refs(packet: DelegationPacket) -> list[str]:
        return [
            *packet.permission_request_ids,
            *packet.session_permission_resolution_ids,
            *packet.workspace_write_sandbox_decision_ids,
            *packet.shell_network_pre_sandbox_decision_ids,
            *packet.process_outcome_evaluation_ids,
        ]
