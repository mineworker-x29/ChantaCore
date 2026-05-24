from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any, Literal
from uuid import uuid4

from chanta_core.deep_self_introspection.capability_registry import SelfCapabilityRegistryAwarenessService
from chanta_core.deep_self_introspection.runtime_boundary import SelfRuntimeBoundaryAwarenessService
from chanta_core.utility.time import utc_now_iso


PolicyTruthStatus = Literal["passed", "warning", "failed", "blocked"]


@dataclass(frozen=True)
class SelfPolicyGateMapRequest:
    layer_filter: str | None = None
    capability_filter: str | None = None
    include_review_policy: bool = True
    include_permission_boundary: bool = True
    include_execution_gate: bool = True
    include_envelope_policy: bool = True
    include_promotion_gate: bool = True
    include_materialization_gate: bool = True
    include_hard_blocks: bool = True
    include_no_action_policy: bool = True
    include_claim_checks: bool = True
    max_items: int = 500

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class PolicyGateRuleDescriptor:
    rule_id: str
    rule_type: str
    target_scope: str
    target_capability_id: str | None
    target_skill_id: str | None
    condition: str
    decision: str
    priority: int
    source: str
    active: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "notes": list(self.notes)}


@dataclass(frozen=True)
class ReviewPolicyDescriptor:
    policy_id: str
    proposal_required: bool
    review_required: bool
    allowed_review_decisions: list[str]
    approval_implies_execution: bool
    no_action_is_valid: bool
    needs_more_input_is_valid: bool
    reviewer_note_supported: bool
    policy_status: str

    def to_dict(self) -> dict[str, Any]:
        return {**self.__dict__, "allowed_review_decisions": list(self.allowed_review_decisions)}


@dataclass(frozen=True)
class PermissionBoundaryDescriptor:
    boundary_id: str
    deny_by_default: bool
    permission_grant_creation_allowed: bool
    permission_escalation_allowed: bool
    external_permission_required: bool
    shell_permission_allowed: bool
    network_permission_allowed: bool
    mcp_permission_allowed: bool
    plugin_permission_allowed: bool
    external_harness_permission_allowed: bool
    boundary_status: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class ExecutionGateDescriptor:
    gate_id: str
    gate_type: str
    enabled: bool
    read_only_only: bool
    requires_review: bool
    requires_permission: bool
    requires_envelope: bool
    hard_blocked: bool
    reason: str | None
    gate_status: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class ExecutionEnvelopePolicyDescriptor:
    policy_id: str
    envelope_required: bool
    envelope_required_for_read_only: bool
    envelope_required_for_blocked_attempts: bool
    audit_visible: bool
    workbench_visible: bool
    ocel_visible: bool
    private_payload_redaction_required: bool
    raw_private_body_allowed: bool
    policy_status: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class PromotionGateDescriptor:
    gate_id: str
    candidate_promotion_enabled: bool
    auto_promotion_allowed: bool
    review_required: bool
    canonical_promotion_enabled: bool
    memory_promotion_allowed: bool
    persona_promotion_allowed: bool
    overlay_promotion_allowed: bool
    gate_status: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class MaterializationGateDescriptor:
    gate_id: str
    materialization_enabled: bool
    plan_materialization_allowed: bool
    todo_materialization_allowed: bool
    task_creation_allowed: bool
    scheduler_registration_allowed: bool
    file_write_materialization_allowed: bool
    gate_status: str

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class PolicyGateFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    target_ref: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "target_ref": dict(self.target_ref),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class SelfPolicyGateMapSnapshot:
    snapshot_id: str
    created_at: str
    request: SelfPolicyGateMapRequest
    rules: list[PolicyGateRuleDescriptor]
    review_policy: ReviewPolicyDescriptor
    permission_boundary: PermissionBoundaryDescriptor
    execution_gates: list[ExecutionGateDescriptor]
    envelope_policy: ExecutionEnvelopePolicyDescriptor
    promotion_gate: PromotionGateDescriptor
    materialization_gate: MaterializationGateDescriptor
    findings: list[PolicyGateFinding]
    limitations: list[str]
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "rules": [item.to_dict() for item in self.rules],
            "review_policy": self.review_policy.to_dict(),
            "permission_boundary": self.permission_boundary.to_dict(),
            "execution_gates": [item.to_dict() for item in self.execution_gates],
            "envelope_policy": self.envelope_policy.to_dict(),
            "promotion_gate": self.promotion_gate.to_dict(),
            "materialization_gate": self.materialization_gate.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
            "limitations": list(self.limitations),
            "read_only": self.read_only,
            "mutation_performed": self.mutation_performed,
        }


@dataclass(frozen=True)
class SelfPolicyGateTruthReport:
    report_id: str
    snapshot_id: str
    created_at: str
    status: PolicyTruthStatus
    findings: list[PolicyGateFinding]
    gate_truth_summary: dict[str, Any]
    unsafe_policy_claims_detected: int
    gate_violations_detected: int
    hard_blocks_confirmed: list[str]
    review_only_paths_confirmed: list[str]
    limitations: list[str]
    withdrawal_conditions: list[str]
    validity_horizon: str
    review_status: str = "report_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "snapshot_id": self.snapshot_id,
            "created_at": self.created_at,
            "status": self.status,
            "findings": [item.to_dict() for item in self.findings],
            "gate_truth_summary": dict(self.gate_truth_summary),
            "unsafe_policy_claims_detected": self.unsafe_policy_claims_detected,
            "gate_violations_detected": self.gate_violations_detected,
            "hard_blocks_confirmed": list(self.hard_blocks_confirmed),
            "review_only_paths_confirmed": list(self.review_only_paths_confirmed),
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


class PolicyGateSourceService:
    def __init__(
        self,
        *,
        capability_service: SelfCapabilityRegistryAwarenessService | None = None,
        runtime_service: SelfRuntimeBoundaryAwarenessService | None = None,
    ) -> None:
        self.capability_service = capability_service or SelfCapabilityRegistryAwarenessService()
        self.runtime_service = runtime_service or SelfRuntimeBoundaryAwarenessService()

    def load_rule_descriptors(self) -> list[PolicyGateRuleDescriptor]:
        capability_snapshot = self.capability_service.view_registry()
        runtime_snapshot = self.runtime_service.view_runtime_boundary()
        rules = [
            PolicyGateRuleDescriptor(
                rule_id="policy_gate_rule:read_only_requires_envelope",
                rule_type="allow",
                target_scope="read_only_invocation",
                target_capability_id=None,
                target_skill_id=None,
                condition="explicit read-only invocation with envelope visibility",
                decision="allowed_as_read_only_observation",
                priority=10,
                source="safety_policy",
                active=True,
                notes=["Read-only view is allowed only as observation."],
            ),
            PolicyGateRuleDescriptor(
                rule_id="policy_gate_rule:review_not_execution",
                rule_type="review_required",
                target_scope="proposal_review",
                target_capability_id=None,
                target_skill_id=None,
                condition="review decision exists",
                decision="does_not_imply_execution",
                priority=20,
                source="contract",
                active=True,
                notes=["Review approval is not execution permission."],
            ),
            PolicyGateRuleDescriptor(
                rule_id="policy_gate_rule:no_action_valid",
                rule_type="allow",
                target_scope="review_outcome",
                target_capability_id=None,
                target_skill_id=None,
                condition="operator selects no_action",
                decision="valid_terminal_policy_outcome",
                priority=30,
                source="contract",
                active=True,
                notes=["No-action is a valid policy outcome."],
            ),
        ]
        for gate_name in ["write", "shell", "network", "mcp", "plugin", "external_harness"]:
            enabled = bool(getattr(runtime_snapshot.execution_boundary, f"{gate_name}_enabled", False))
            rules.append(
                PolicyGateRuleDescriptor(
                    rule_id=f"policy_gate_rule:{gate_name}_hard_block",
                    rule_type="hard_block",
                    target_scope=gate_name,
                    target_capability_id=None,
                    target_skill_id=None,
                    condition=f"{gate_name} requested",
                    decision="deny_execution",
                    priority=100,
                    source="runtime_boundary",
                    active=not enabled,
                    notes=[f"{gate_name} remains disabled by runtime boundary."],
                )
            )
        if capability_snapshot.execution_enabled_count:
            rules.append(
                PolicyGateRuleDescriptor(
                    rule_id="policy_gate_rule:capability_execution_inconsistency",
                    rule_type="hard_block",
                    target_scope="capability_registry",
                    target_capability_id=None,
                    target_skill_id=None,
                    condition="capability registry reports execution enabled",
                    decision="treat_as_violation",
                    priority=1,
                    source="registry",
                    active=True,
                    notes=["Capability truth should keep execution disabled for this layer."],
                )
            )
        return rules

    def load_review_policy(self) -> ReviewPolicyDescriptor:
        return ReviewPolicyDescriptor(
            policy_id="review_policy:proposal_review_read_only",
            proposal_required=True,
            review_required=True,
            allowed_review_decisions=[
                "approved_for_explicit_invocation",
                "rejected",
                "revise_proposal",
                "no_action",
                "needs_more_input",
            ],
            approval_implies_execution=False,
            no_action_is_valid=True,
            needs_more_input_is_valid=True,
            reviewer_note_supported=True,
            policy_status="ok",
        )

    def load_permission_boundary(self) -> PermissionBoundaryDescriptor:
        return PermissionBoundaryDescriptor(
            boundary_id="permission_boundary:deny_by_default",
            deny_by_default=True,
            permission_grant_creation_allowed=False,
            permission_escalation_allowed=False,
            external_permission_required=True,
            shell_permission_allowed=False,
            network_permission_allowed=False,
            mcp_permission_allowed=False,
            plugin_permission_allowed=False,
            external_harness_permission_allowed=False,
            boundary_status="ok",
        )

    def load_execution_gates(self) -> list[ExecutionGateDescriptor]:
        return [
            ExecutionGateDescriptor(
                gate_id="execution_gate:read_only",
                gate_type="read_only",
                enabled=True,
                read_only_only=True,
                requires_review=False,
                requires_permission=False,
                requires_envelope=True,
                hard_blocked=False,
                reason="Read-only observation may pass through explicit gate and envelope.",
                gate_status="ok",
            ),
            *[
                ExecutionGateDescriptor(
                    gate_id=f"execution_gate:{gate_type}",
                    gate_type=gate_type,
                    enabled=False,
                    read_only_only=False,
                    requires_review=True,
                    requires_permission=True,
                    requires_envelope=True,
                    hard_blocked=True,
                    reason=f"{gate_type} execution is outside this layer.",
                    gate_status="ok",
                )
                for gate_type in ["write", "shell", "network", "mcp", "plugin", "external_harness"]
            ],
            ExecutionGateDescriptor(
                gate_id="execution_gate:promotion",
                gate_type="promotion",
                enabled=False,
                read_only_only=False,
                requires_review=True,
                requires_permission=True,
                requires_envelope=True,
                hard_blocked=True,
                reason="Promotion is disabled in policy/gate awareness.",
                gate_status="ok",
            ),
            ExecutionGateDescriptor(
                gate_id="execution_gate:materialization",
                gate_type="materialization",
                enabled=False,
                read_only_only=False,
                requires_review=True,
                requires_permission=True,
                requires_envelope=True,
                hard_blocked=True,
                reason="Materialization is disabled in policy/gate awareness.",
                gate_status="ok",
            ),
        ]

    def load_envelope_policy(self) -> ExecutionEnvelopePolicyDescriptor:
        return ExecutionEnvelopePolicyDescriptor(
            policy_id="execution_envelope_policy:read_only_and_blocked_attempts",
            envelope_required=True,
            envelope_required_for_read_only=True,
            envelope_required_for_blocked_attempts=True,
            audit_visible=True,
            workbench_visible=True,
            ocel_visible=True,
            private_payload_redaction_required=True,
            raw_private_body_allowed=False,
            policy_status="ok",
        )

    def load_promotion_gate(self) -> PromotionGateDescriptor:
        return PromotionGateDescriptor(
            gate_id="promotion_gate:candidate_only",
            candidate_promotion_enabled=False,
            auto_promotion_allowed=False,
            review_required=True,
            canonical_promotion_enabled=False,
            memory_promotion_allowed=False,
            persona_promotion_allowed=False,
            overlay_promotion_allowed=False,
            gate_status="ok",
        )

    def load_materialization_gate(self) -> MaterializationGateDescriptor:
        return MaterializationGateDescriptor(
            gate_id="materialization_gate:candidate_only",
            materialization_enabled=False,
            plan_materialization_allowed=False,
            todo_materialization_allowed=False,
            task_creation_allowed=False,
            scheduler_registration_allowed=False,
            file_write_materialization_allowed=False,
            gate_status="ok",
        )


class PolicyGateFindingService:
    def evaluate(
        self,
        snapshot: SelfPolicyGateMapSnapshot,
        optional_claims: list[dict[str, Any]] | None = None,
    ) -> list[PolicyGateFinding]:
        findings: list[PolicyGateFinding] = []
        findings.extend(_evaluate_review_policy(snapshot.review_policy))
        findings.extend(_evaluate_permission_boundary(snapshot.permission_boundary))
        findings.extend(_evaluate_execution_gates(snapshot.execution_gates))
        findings.extend(_evaluate_envelope_policy(snapshot.envelope_policy))
        findings.extend(_evaluate_promotion_gate(snapshot.promotion_gate))
        findings.extend(_evaluate_materialization_gate(snapshot.materialization_gate))
        findings.extend(_evaluate_claims(optional_claims or []))
        if not findings:
            findings.append(_finding("info", "ok", "Policy/gate truth check passed.", {}, []))
        return findings


class PolicyGateTruthCheckService:
    def __init__(self, finding_service: PolicyGateFindingService | None = None) -> None:
        self.finding_service = finding_service or PolicyGateFindingService()

    def check_truth(
        self,
        snapshot: SelfPolicyGateMapSnapshot,
        optional_claims: list[dict[str, Any]] | None = None,
    ) -> SelfPolicyGateTruthReport:
        findings = self.finding_service.evaluate(snapshot, optional_claims=optional_claims)
        status: PolicyTruthStatus = "passed"
        if any(item.severity in {"error", "critical"} for item in findings):
            status = "failed"
        elif any(item.severity == "warning" for item in findings):
            status = "warning"
        violations = sum(1 for item in findings if item.severity in {"error", "critical"})
        unsafe_claims = sum(1 for item in findings if item.finding_type == "policy_claim_exceeds_gate_truth")
        return SelfPolicyGateTruthReport(
            report_id=f"self_policy_gate_truth_report:{uuid4().hex}",
            snapshot_id=snapshot.snapshot_id,
            created_at=utc_now_iso(),
            status=status,
            findings=findings,
            gate_truth_summary={
                "proposal_created != execution_allowed": True,
                "review_approved != execution_performed": True,
                "no_action is valid": snapshot.review_policy.no_action_is_valid,
                "needs_more_input is valid": snapshot.review_policy.needs_more_input_is_valid,
                "deny_by_default": snapshot.permission_boundary.deny_by_default,
                "permission_grant_creation_allowed": snapshot.permission_boundary.permission_grant_creation_allowed,
                "permission_escalation_allowed": snapshot.permission_boundary.permission_escalation_allowed,
                "envelope_required": snapshot.envelope_policy.envelope_required,
                "promotion_enabled": snapshot.promotion_gate.candidate_promotion_enabled,
                "materialization_enabled": snapshot.materialization_gate.materialization_enabled,
            },
            unsafe_policy_claims_detected=unsafe_claims,
            gate_violations_detected=violations,
            hard_blocks_confirmed=[gate.gate_type for gate in snapshot.execution_gates if gate.hard_blocked],
            review_only_paths_confirmed=[
                "proposal_review",
                "candidate_promotion_review",
                "no_action",
                "needs_more_input",
            ],
            limitations=[
                "v0.21.3 creates read-only policy/gate maps only.",
                "No review decision, permission grant, skill invocation, or envelope execution is created.",
            ],
            withdrawal_conditions=[
                "Withdraw if policy/gate awareness mutates policy or gate state.",
                "Withdraw if it creates review decisions, grants permissions, invokes skills, or executes envelopes.",
            ],
            validity_horizon="Valid until v0.21.4 Self-Trace Integrity Awareness changes trace integrity assumptions.",
        )


class SelfPolicyGateAwarenessService:
    def __init__(
        self,
        *,
        source_service: PolicyGateSourceService | None = None,
        finding_service: PolicyGateFindingService | None = None,
        truth_service: PolicyGateTruthCheckService | None = None,
    ) -> None:
        self.source_service = source_service or PolicyGateSourceService()
        self.finding_service = finding_service or PolicyGateFindingService()
        self.truth_service = truth_service or PolicyGateTruthCheckService(self.finding_service)
        self.last_snapshot: SelfPolicyGateMapSnapshot | None = None
        self.last_truth_report: SelfPolicyGateTruthReport | None = None

    def view_policy_gate_map(
        self,
        request: SelfPolicyGateMapRequest | None = None,
    ) -> SelfPolicyGateMapSnapshot:
        request = request or SelfPolicyGateMapRequest()
        rules = self.source_service.load_rule_descriptors()[: max(0, request.max_items)]
        snapshot = SelfPolicyGateMapSnapshot(
            snapshot_id=f"self_policy_gate_snapshot:{uuid4().hex}",
            created_at=utc_now_iso(),
            request=request,
            rules=rules,
            review_policy=self.source_service.load_review_policy(),
            permission_boundary=self.source_service.load_permission_boundary(),
            execution_gates=self.source_service.load_execution_gates() if request.include_execution_gate else [],
            envelope_policy=self.source_service.load_envelope_policy(),
            promotion_gate=self.source_service.load_promotion_gate(),
            materialization_gate=self.source_service.load_materialization_gate(),
            findings=[],
            limitations=[
                "Policy/gate map is read-only.",
                "Missing data is represented as finding or limitation, not as implicit allow.",
                "No private full paths, raw file content, or raw secrets are emitted.",
            ],
        )
        snapshot = replace(snapshot, findings=self.finding_service.evaluate(snapshot))
        self.last_snapshot = snapshot
        return snapshot

    def truth_check(
        self,
        request: SelfPolicyGateMapRequest | None = None,
        optional_claims: list[dict[str, Any]] | None = None,
    ) -> SelfPolicyGateTruthReport:
        snapshot = self.view_policy_gate_map(request)
        report = self.truth_service.check_truth(snapshot, optional_claims=optional_claims)
        self.last_truth_report = report
        return report

    def build_pig_report(self) -> dict[str, Any]:
        snapshot = self.last_snapshot or self.view_policy_gate_map()
        hard_blocked = [gate.gate_type for gate in snapshot.execution_gates if gate.hard_blocked]
        return {
            "version": "v0.21.3",
            "layer": "deep_self_introspection",
            "subject": "policy_gate",
            "principles": [
                "proposal_created != execution_allowed",
                "review_approved != execution_performed",
                "no_action is valid",
                "gate truth > persona claim",
            ],
            "deny_by_default": snapshot.permission_boundary.deny_by_default,
            "permission_grant_creation_allowed": snapshot.permission_boundary.permission_grant_creation_allowed,
            "permission_escalation_allowed": snapshot.permission_boundary.permission_escalation_allowed,
            "approval_implies_execution": snapshot.review_policy.approval_implies_execution,
            "envelope_required": snapshot.envelope_policy.envelope_required,
            "blocked_attempts_auditable": snapshot.envelope_policy.envelope_required_for_blocked_attempts,
            "hard_blocked_gates": hard_blocked,
            "promotion_enabled": snapshot.promotion_gate.candidate_promotion_enabled,
            "materialization_enabled": snapshot.materialization_gate.materialization_enabled,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "self_policy_gate_awareness",
            "version": "v0.21.3",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfCapabilityTruthState",
                "SelfRuntimeBoundaryState",
                "DeepSelfIntrospectionContractState",
            ],
            "target_read_models": [
                "SelfPolicyGateState",
                "SelfReviewPolicyState",
                "SelfPermissionBoundaryState",
                "SelfExecutionGateState",
                "SelfEnvelopePolicyState",
                "SelfPromotionGateState",
                "SelfMaterializationGateState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "canonical_store": "ocel",
        }

    def render_cli(
        self,
        command: str,
        snapshot: SelfPolicyGateMapSnapshot | None = None,
        report: SelfPolicyGateTruthReport | None = None,
    ) -> str:
        snapshot = snapshot or self.last_snapshot or self.view_policy_gate_map()
        report = report or self.last_truth_report
        lines = [
            "Self-Policy/Gate Awareness",
            f"command={command}",
            f"policy_truth_status={report.status if report else 'not_checked'}",
            "proposal_created != execution_allowed=True",
            "review_approved != execution_performed=True",
            f"approval_implies_execution={snapshot.review_policy.approval_implies_execution}",
            f"no_action_is_valid={snapshot.review_policy.no_action_is_valid}",
            f"needs_more_input_is_valid={snapshot.review_policy.needs_more_input_is_valid}",
            f"deny_by_default={snapshot.permission_boundary.deny_by_default}",
            f"permission_grant_creation_allowed={snapshot.permission_boundary.permission_grant_creation_allowed}",
            f"permission_escalation_allowed={snapshot.permission_boundary.permission_escalation_allowed}",
            f"envelope_required={snapshot.envelope_policy.envelope_required}",
            f"envelope_required_for_blocked_attempts={snapshot.envelope_policy.envelope_required_for_blocked_attempts}",
            f"raw_private_body_allowed={snapshot.envelope_policy.raw_private_body_allowed}",
            f"hard_blocked_gates={','.join(gate.gate_type for gate in snapshot.execution_gates if gate.hard_blocked)}",
            f"promotion_enabled={snapshot.promotion_gate.candidate_promotion_enabled}",
            f"materialization_enabled={snapshot.materialization_gate.materialization_enabled}",
            f"unsafe_policy_claims_detected={report.unsafe_policy_claims_detected if report else 0}",
            "read_only=True",
            "mutation_performed=False",
            "review_decision_created=False",
            "permission_grant_created=False",
            "skill_invocation_created=False",
            "envelope_execution_created=False",
            "policy_mutated=False",
            "raw_file_content_printed=False",
            "private_full_paths_printed=False",
            "raw_secrets_printed=False",
        ]
        return "\n".join(lines)


def _evaluate_review_policy(policy: ReviewPolicyDescriptor) -> list[PolicyGateFinding]:
    findings: list[PolicyGateFinding] = []
    if policy.approval_implies_execution:
        findings.append(_finding("error", "approval_implies_execution_violation", "Review approval implies execution.", {"policy_id": policy.policy_id}))
    if not policy.no_action_is_valid:
        findings.append(_finding("error", "no_action_policy_missing", "No-action is not a valid policy outcome.", {"policy_id": policy.policy_id}))
    if not policy.needs_more_input_is_valid:
        findings.append(_finding("error", "needs_more_input_policy_missing", "Needs-more-input is not a valid policy outcome.", {"policy_id": policy.policy_id}))
    return findings


def _evaluate_permission_boundary(boundary: PermissionBoundaryDescriptor) -> list[PolicyGateFinding]:
    findings: list[PolicyGateFinding] = []
    if boundary.permission_grant_creation_allowed:
        findings.append(_finding("error", "permission_grant_allowed_violation", "Permission grant creation is allowed.", {"boundary_id": boundary.boundary_id}))
    if boundary.permission_escalation_allowed:
        findings.append(_finding("error", "permission_escalation_allowed_violation", "Permission escalation is allowed.", {"boundary_id": boundary.boundary_id}))
    for field_name in [
        "shell_permission_allowed",
        "network_permission_allowed",
        "mcp_permission_allowed",
        "plugin_permission_allowed",
        "external_harness_permission_allowed",
    ]:
        if bool(getattr(boundary, field_name)):
            findings.append(_finding("error", "permission_grant_allowed_violation", f"{field_name} is allowed.", {"boundary_id": boundary.boundary_id}))
    return findings


def _evaluate_execution_gates(gates: list[ExecutionGateDescriptor]) -> list[PolicyGateFinding]:
    findings: list[PolicyGateFinding] = []
    if not gates:
        findings.append(_finding("warning", "missing_execution_envelope_requirement", "No execution gates are visible.", {}))
        return findings
    for gate in gates:
        target = {"gate_id": gate.gate_id, "gate_type": gate.gate_type}
        if gate.gate_type == "read_only" and not gate.requires_envelope:
            findings.append(_finding("error", "missing_execution_envelope_requirement", "Read-only gate does not require envelope.", target))
        if gate.gate_type in {"write", "shell", "network", "mcp", "plugin", "external_harness"} and gate.enabled:
            findings.append(_finding("error", f"{gate.gate_type}_gate_enabled_violation", f"{gate.gate_type} gate is enabled.", target))
    return findings


def _evaluate_envelope_policy(policy: ExecutionEnvelopePolicyDescriptor) -> list[PolicyGateFinding]:
    findings: list[PolicyGateFinding] = []
    target = {"policy_id": policy.policy_id}
    if not policy.envelope_required or not policy.envelope_required_for_read_only:
        findings.append(_finding("error", "missing_execution_envelope_requirement", "Execution envelope is not required.", target))
    if not policy.envelope_required_for_blocked_attempts:
        findings.append(_finding("error", "missing_blocked_attempt_envelope", "Blocked attempts are not envelope-visible.", target))
    if policy.raw_private_body_allowed:
        findings.append(_finding("error", "raw_private_payload_allowed_violation", "Raw private payload is allowed.", target))
    return findings


def _evaluate_promotion_gate(gate: PromotionGateDescriptor) -> list[PolicyGateFinding]:
    flags = [
        gate.candidate_promotion_enabled,
        gate.auto_promotion_allowed,
        gate.canonical_promotion_enabled,
        gate.memory_promotion_allowed,
        gate.persona_promotion_allowed,
        gate.overlay_promotion_allowed,
    ]
    if any(flags):
        return [_finding("error", "promotion_gate_enabled_violation", "Promotion gate is enabled.", {"gate_id": gate.gate_id})]
    return []


def _evaluate_materialization_gate(gate: MaterializationGateDescriptor) -> list[PolicyGateFinding]:
    flags = [
        gate.materialization_enabled,
        gate.plan_materialization_allowed,
        gate.todo_materialization_allowed,
        gate.task_creation_allowed,
        gate.scheduler_registration_allowed,
        gate.file_write_materialization_allowed,
    ]
    if any(flags):
        return [_finding("error", "materialization_gate_enabled_violation", "Materialization gate is enabled.", {"gate_id": gate.gate_id})]
    return []


def _evaluate_claims(claims: list[dict[str, Any]]) -> list[PolicyGateFinding]:
    findings: list[PolicyGateFinding] = []
    for claim in claims:
        claim_type = str(claim.get("claim_type") or "")
        if claim_type in {
            "review_approval_implies_execution",
            "permission_grant_allowed",
            "promotion_allowed",
            "materialization_allowed",
            "dangerous_gate_enabled",
        } and claim.get("claimed_allowed", True):
            findings.append(
                _finding(
                    "error",
                    "policy_claim_exceeds_gate_truth",
                    "Optional policy claim exceeds gate truth.",
                    {"claim_type": claim_type},
                    [dict(claim)],
                )
            )
    return findings


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    target_ref: dict[str, Any],
    evidence_refs: list[dict[str, Any]] | None = None,
) -> PolicyGateFinding:
    return PolicyGateFinding(
        finding_id=f"policy_gate_finding:{uuid4().hex}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        target_ref=dict(target_ref),
        evidence_refs=[dict(item) for item in evidence_refs or [target_ref]],
        withdrawal_condition="Withdraw policy/gate judgment unless the policy evidence is corrected.",
    )
