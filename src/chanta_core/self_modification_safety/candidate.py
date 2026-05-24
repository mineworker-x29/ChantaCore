from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.self_awareness.workspace_awareness import SelfWorkspacePathPolicyService
from chanta_core.self_modification_safety.registry import SelfModificationRegistryService
from chanta_core.utility.time import utc_now_iso


SELF_MODIFICATION_REQUEST_CANDIDATE_VERSION = "v0.22.1"
SELF_MODIFICATION_REQUEST_CANDIDATE_STATE = "self_modification_request_patch_candidate_created"
REQUEST_CREATE_SKILL_ID = "skill:self_modification_request_create"
PATCH_CANDIDATE_CREATE_SKILL_ID = "skill:self_modification_patch_candidate_create"
CONTRACT_ONLY_FOLLOWUP_SKILL_IDS: list[str] = []

ALLOWED_INTENT_TYPES = {"bugfix", "refactor", "docs", "test", "config", "cleanup", "unknown"}
SECRET_FILE_NAMES = {".env", ".env.local", "id_rsa", "id_dsa", "known_hosts"}
SECRET_SUFFIXES = {".pem", ".key", ".pfx", ".p12", ".crt"}
GENERATED_PARTS = {"generated", "dist", "build", ".cache"}
BINARY_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".ico", ".pdf", ".zip", ".gz", ".7z", ".exe", ".dll"}


@dataclass(frozen=True)
class SelfModificationRequestCreateRequest:
    goal_text: str
    target_paths: list[str] = field(default_factory=list)
    target_refs: list[dict[str, Any]] = field(default_factory=list)
    requested_patch_type: str | None = None
    requester_type: str = "operator"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    allow_no_action: bool = True
    allow_needs_more_input: bool = True
    max_target_files: int = 1
    strictness: str = "standard"

    def normalized(self) -> "SelfModificationRequestCreateRequest":
        return SelfModificationRequestCreateRequest(
            goal_text=str(self.goal_text or "").strip(),
            target_paths=[str(item).strip() for item in self.target_paths if str(item).strip()],
            target_refs=[dict(item) for item in self.target_refs],
            requested_patch_type=self.requested_patch_type,
            requester_type=self.requester_type or "operator",
            source_refs=[dict(item) for item in self.source_refs],
            constraints=[str(item) for item in self.constraints],
            allow_no_action=bool(self.allow_no_action),
            allow_needs_more_input=bool(self.allow_needs_more_input),
            max_target_files=max(1, int(self.max_target_files)),
            strictness=self.strictness or "standard",
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal_text": self.goal_text,
            "target_paths": list(self.target_paths),
            "target_refs": [dict(item) for item in self.target_refs],
            "requested_patch_type": self.requested_patch_type,
            "requester_type": self.requester_type,
            "source_refs": [dict(item) for item in self.source_refs],
            "constraints": list(self.constraints),
            "allow_no_action": self.allow_no_action,
            "allow_needs_more_input": self.allow_needs_more_input,
            "max_target_files": self.max_target_files,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class ModificationTargetRef:
    target_id: str
    target_type: str
    root_id: str | None
    relative_path: str | None
    path_status: str
    file_kind: str | None
    current_state_ref: dict[str, Any] | None
    private_boundary_risk: bool
    secret_file_risk: bool
    generated_file_risk: bool
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "target_type": self.target_type,
            "root_id": self.root_id,
            "relative_path": self.relative_path,
            "path_status": self.path_status,
            "file_kind": self.file_kind,
            "current_state_ref": dict(self.current_state_ref) if self.current_state_ref else None,
            "private_boundary_risk": self.private_boundary_risk,
            "secret_file_risk": self.secret_file_risk,
            "generated_file_risk": self.generated_file_risk,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class PatchIntentDescriptor:
    intent_id: str
    goal_text: str
    intent_type: str
    requested_patch_type: str | None
    allowed_patch_type_candidate: str | None
    forbidden_patch_type_detected: bool
    requires_file_content: bool
    requires_diff_generation: bool
    requires_operator_clarification: bool
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "goal_text": self.goal_text,
            "intent_type": self.intent_type,
            "requested_patch_type": self.requested_patch_type,
            "allowed_patch_type_candidate": self.allowed_patch_type_candidate,
            "forbidden_patch_type_detected": self.forbidden_patch_type_detected,
            "requires_file_content": self.requires_file_content,
            "requires_diff_generation": self.requires_diff_generation,
            "requires_operator_clarification": self.requires_operator_clarification,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class PatchScopeDescriptor:
    scope_id: str
    target_count: int
    max_target_files: int
    target_refs: list[ModificationTargetRef]
    scope_status: str
    scope_risk_reasons: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "target_count": self.target_count,
            "max_target_files": self.max_target_files,
            "target_refs": [item.to_dict() for item in self.target_refs],
            "scope_status": self.scope_status,
            "scope_risk_reasons": list(self.scope_risk_reasons),
        }


@dataclass(frozen=True)
class PatchConstraintDescriptor:
    constraint_id: str
    constraint_type: str
    description: str
    severity: str
    source_ref: dict[str, Any] | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "constraint_id": self.constraint_id,
            "constraint_type": self.constraint_type,
            "description": self.description,
            "severity": self.severity,
            "source_ref": dict(self.source_ref) if self.source_ref else None,
        }


@dataclass(frozen=True)
class PatchPreliminaryRiskAssessment:
    risk_id: str
    risk_level: str
    target_risks: list[str]
    policy_risks: list[str]
    boundary_risks: list[str]
    forbidden_patch_risks: list[str]
    requires_review: bool = True
    safe_to_generate_diff: bool = False
    safe_to_apply: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_id": self.risk_id,
            "risk_level": self.risk_level,
            "target_risks": list(self.target_risks),
            "policy_risks": list(self.policy_risks),
            "boundary_risks": list(self.boundary_risks),
            "forbidden_patch_risks": list(self.forbidden_patch_risks),
            "requires_review": self.requires_review,
            "safe_to_generate_diff": self.safe_to_generate_diff,
            "safe_to_apply": self.safe_to_apply,
        }


@dataclass(frozen=True)
class SelfModificationRequest:
    request_id: str
    created_at: str
    goal_text: str
    requester_type: str
    target_refs: list[ModificationTargetRef]
    intent: PatchIntentDescriptor
    scope: PatchScopeDescriptor
    constraints: list[PatchConstraintDescriptor]
    source_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    request_status: str
    review_status: str = "request_only"
    file_write_enabled: bool = False
    apply_patch_enabled: bool = False
    diff_generated: bool = False
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "created_at": self.created_at,
            "goal_text": self.goal_text,
            "requester_type": self.requester_type,
            "target_refs": [item.to_dict() for item in self.target_refs],
            "intent": self.intent.to_dict(),
            "scope": self.scope.to_dict(),
            "constraints": [item.to_dict() for item in self.constraints],
            "source_refs": [dict(item) for item in self.source_refs],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "request_status": self.request_status,
            "review_status": self.review_status,
            "file_write_enabled": self.file_write_enabled,
            "apply_patch_enabled": self.apply_patch_enabled,
            "diff_generated": self.diff_generated,
            "applied": self.applied,
        }


@dataclass(frozen=True)
class PatchCandidateFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    target_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "target_ref": dict(self.target_ref) if self.target_ref else None,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class PatchCandidate:
    candidate_id: str
    request_id: str
    created_at: str
    title: str
    goal_text: str
    target_refs: list[ModificationTargetRef]
    intent: PatchIntentDescriptor
    scope: PatchScopeDescriptor
    constraints: list[PatchConstraintDescriptor]
    preliminary_risk: PatchPreliminaryRiskAssessment
    findings: list[PatchCandidateFinding]
    evidence_refs: list[dict[str, Any]]
    lifecycle_state: str = "candidate_created"
    candidate_status: str = "candidate_only"
    review_status: str = "pending_review"
    requires_diff_preview: bool = True
    requires_static_safety_check: bool = True
    requires_dry_run: bool = True
    requires_human_review: bool = True
    requires_apply_gate: bool = True
    requires_rollback_plan: bool = True
    requires_post_apply_verification: bool = True
    diff_generated: bool = False
    dry_run_checked: bool = False
    review_approved: bool = False
    apply_gate_opened: bool = False
    applied: bool = False
    file_write_enabled: bool = False
    apply_patch_enabled: bool = False
    materialized: bool = False
    execution_enabled: bool = False
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "request_id": self.request_id,
            "created_at": self.created_at,
            "title": self.title,
            "goal_text": self.goal_text,
            "target_refs": [item.to_dict() for item in self.target_refs],
            "intent": self.intent.to_dict(),
            "scope": self.scope.to_dict(),
            "constraints": [item.to_dict() for item in self.constraints],
            "preliminary_risk": self.preliminary_risk.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "lifecycle_state": self.lifecycle_state,
            "candidate_status": self.candidate_status,
            "review_status": self.review_status,
            "requires_diff_preview": self.requires_diff_preview,
            "requires_static_safety_check": self.requires_static_safety_check,
            "requires_dry_run": self.requires_dry_run,
            "requires_human_review": self.requires_human_review,
            "requires_apply_gate": self.requires_apply_gate,
            "requires_rollback_plan": self.requires_rollback_plan,
            "requires_post_apply_verification": self.requires_post_apply_verification,
            "diff_generated": self.diff_generated,
            "dry_run_checked": self.dry_run_checked,
            "review_approved": self.review_approved,
            "apply_gate_opened": self.apply_gate_opened,
            "applied": self.applied,
            "file_write_enabled": self.file_write_enabled,
            "apply_patch_enabled": self.apply_patch_enabled,
            "materialized": self.materialized,
            "execution_enabled": self.execution_enabled,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


@dataclass(frozen=True)
class SelfModificationNoActionCandidate:
    candidate_id: str
    request_id: str
    reason: str
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "no_action"
    candidate_status: str = "candidate_only"
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "request_id": self.request_id,
            "reason": self.reason,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "recommended_review_decision": self.recommended_review_decision,
            "candidate_status": self.candidate_status,
            "applied": self.applied,
        }


@dataclass(frozen=True)
class SelfModificationNeedsMoreInputCandidate:
    candidate_id: str
    request_id: str
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "needs_more_input"
    candidate_status: str = "candidate_only"
    applied: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "request_id": self.request_id,
            "reason": self.reason,
            "missing_inputs": list(self.missing_inputs),
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "recommended_review_decision": self.recommended_review_decision,
            "candidate_status": self.candidate_status,
            "applied": self.applied,
        }


@dataclass(frozen=True)
class SelfModificationRequestCandidateResult:
    request: SelfModificationRequest
    patch_candidate: PatchCandidate | None
    no_action_candidate: SelfModificationNoActionCandidate | None
    needs_more_input_candidate: SelfModificationNeedsMoreInputCandidate | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "request": self.request.to_dict(),
            "patch_candidate": self.patch_candidate.to_dict() if self.patch_candidate else None,
            "no_action_candidate": self.no_action_candidate.to_dict() if self.no_action_candidate else None,
            "needs_more_input_candidate": self.needs_more_input_candidate.to_dict()
            if self.needs_more_input_candidate
            else None,
        }


class ModificationTargetResolver:
    def __init__(self, *, path_policy_service: SelfWorkspacePathPolicyService | None = None) -> None:
        self.path_policy_service = path_policy_service or SelfWorkspacePathPolicyService()

    def resolve_targets(self, request: SelfModificationRequestCreateRequest) -> list[ModificationTargetRef]:
        normalized = request.normalized()
        targets: list[ModificationTargetRef] = []
        for raw_path in normalized.target_paths:
            targets.append(self._resolve_one(raw_path))
        for ref in normalized.target_refs:
            ref_path = str(ref.get("relative_path") or ref.get("path") or "").strip()
            if ref_path:
                targets.append(self._resolve_one(ref_path))
        return targets

    def _resolve_one(self, raw_path: str) -> ModificationTargetRef:
        resolution = self.path_policy_service.resolve_path(raw_path)
        display_path = resolution.normalized_path if not resolution.blocked else None
        evidence = [
            {
                "ref_type": "workspace_path_policy",
                "path_status": "blocked" if resolution.blocked else "checked",
                "finding_type": resolution.finding_type,
            }
        ]
        if resolution.blocked:
            return ModificationTargetRef(
                target_id=f"modification_target_ref:{uuid4()}",
                target_type="unknown",
                root_id=resolution.root_id,
                relative_path=display_path,
                path_status="blocked",
                file_kind=None,
                current_state_ref=None,
                private_boundary_risk=resolution.finding_type in {"private_boundary", "absolute_path_not_allowed"},
                secret_file_risk=_looks_like_secret_path(raw_path),
                generated_file_risk=_looks_like_generated_path(raw_path),
                evidence_refs=evidence,
            )
        path_obj = Path(resolution.canonical_path)
        path_exists = path_obj.exists()
        target_type = "workspace_directory" if path_obj.is_dir() else "workspace_file" if path_obj.is_file() else "unknown"
        relative_path = resolution.normalized_path
        file_kind = _file_kind(relative_path, target_type)
        return ModificationTargetRef(
            target_id=f"modification_target_ref:{uuid4()}",
            target_type=target_type,
            root_id=resolution.root_id,
            relative_path=relative_path,
            path_status="verified" if path_exists else "not_found",
            file_kind=file_kind,
            current_state_ref={
                "ref_type": "workspace_path_metadata",
                "relative_path": relative_path,
                "exists": path_exists,
                "target_type": target_type,
            },
            private_boundary_risk=False,
            secret_file_risk=_looks_like_secret_path(relative_path),
            generated_file_risk=_looks_like_generated_path(relative_path),
            evidence_refs=evidence,
        )


class PatchIntentClassifier:
    def __init__(self, *, registry_service: SelfModificationRegistryService | None = None) -> None:
        self.registry_service = registry_service or SelfModificationRegistryService()

    def classify(self, request: SelfModificationRequestCreateRequest) -> PatchIntentDescriptor:
        normalized = request.normalized()
        goal = normalized.goal_text
        lower_goal = goal.casefold()
        intent_type = "unknown"
        if any(token in lower_goal for token in ["doc", "readme", "restore", "markdown"]):
            intent_type = "docs"
        elif any(token in lower_goal for token in ["test", "fixture", "unit check"]):
            intent_type = "test"
        elif any(token in lower_goal for token in ["config", "setting", "toml", "yaml", "ini"]):
            intent_type = "config"
        elif any(token in lower_goal for token in ["refactor", "restructure", "cleanup architecture"]):
            intent_type = "refactor"
        elif any(token in lower_goal for token in ["bug", "fix", "failure", "error"]):
            intent_type = "bugfix"
        elif any(token in lower_goal for token in ["cleanup", "tidy", "format"]):
            intent_type = "cleanup"
        policy = self.registry_service.build_contract().allowed_patch_policy
        requested = normalized.requested_patch_type
        forbidden = bool(requested and requested in policy.forbidden_patch_types)
        allowed = requested if requested in policy.allowed_patch_types else None
        return PatchIntentDescriptor(
            intent_id=f"patch_intent:{uuid4()}",
            goal_text=goal,
            intent_type=intent_type if intent_type in ALLOWED_INTENT_TYPES else "unknown",
            requested_patch_type=requested,
            allowed_patch_type_candidate=allowed,
            forbidden_patch_type_detected=forbidden,
            requires_file_content=False,
            requires_diff_generation=True,
            requires_operator_clarification=not bool(goal),
            notes=[
                "Deterministic classifier only.",
                "No LLM patch generator or LLM judge is used.",
                "Diff generation is deferred to v0.22.2.",
            ],
        )


class PatchScopeBuilder:
    def build_scope(
        self,
        targets: list[ModificationTargetRef],
        request: SelfModificationRequestCreateRequest,
    ) -> PatchScopeDescriptor:
        normalized = request.normalized()
        reasons: list[str] = []
        status = "ok"
        if not targets:
            status = "needs_more_input"
            reasons.append("missing_target_path")
        if len(targets) > normalized.max_target_files:
            status = "blocked"
            reasons.append("target_scope_exceeds_limit")
        for target in targets:
            if target.path_status == "blocked":
                status = "blocked"
                reasons.append("target_path_blocked")
            elif target.path_status == "not_found" and status != "blocked":
                status = "needs_more_input"
                reasons.append("target_not_found")
            if target.private_boundary_risk:
                status = "blocked"
                reasons.append("private_boundary_risk")
            if target.secret_file_risk:
                status = "blocked"
                reasons.append("secret_file_risk")
            if target.generated_file_risk and status == "ok":
                status = "warning"
                reasons.append("generated_file_risk")
        return PatchScopeDescriptor(
            scope_id=f"patch_scope:{uuid4()}",
            target_count=len(targets),
            max_target_files=normalized.max_target_files,
            target_refs=list(targets),
            scope_status=status,
            scope_risk_reasons=_unique(reasons),
        )


class PatchConstraintBuilder:
    def build_constraints(
        self,
        request: SelfModificationRequestCreateRequest,
        targets: list[ModificationTargetRef],
    ) -> list[PatchConstraintDescriptor]:
        _ = request, targets
        constraint_types = [
            ("no_file_write_in_v0_22_1", "v0.22.1 may create request and candidate state only.", "hard_block"),
            ("no_apply_patch_in_v0_22_1", "Patch application is not enabled in v0.22.1.", "hard_block"),
            ("diff_generation_deferred_to_v0_22_2", "Patch drafts and diff preview are deferred.", "hard_block"),
            ("requires_workspace_path_policy", "Targets must pass workspace-relative path policy.", "hard_block"),
            ("requires_diff_preview", "A later diff preview is required before apply.", "warning"),
            ("requires_static_safety_check", "A static safety check is required before apply.", "warning"),
            ("requires_dry_run", "A dry-run result is required before apply.", "warning"),
            ("requires_human_review", "Human review is required before apply.", "warning"),
            ("requires_apply_gate", "An explicit apply gate is required before mutation.", "hard_block"),
            ("requires_rollback_plan", "A rollback plan is required before mutation.", "hard_block"),
            ("requires_post_apply_verification", "Post-apply verification is required after mutation.", "warning"),
        ]
        return [
            PatchConstraintDescriptor(
                constraint_id=f"patch_constraint:{uuid4()}",
                constraint_type=constraint_type,
                description=description,
                severity=severity,
                source_ref={"ref_type": "self_modification_safety_contract", "version": "v0.22.0"},
            )
            for constraint_type, description, severity in constraint_types
        ]


class PatchPreliminaryRiskService:
    def assess(
        self,
        request: SelfModificationRequestCreateRequest,
        targets: list[ModificationTargetRef],
        intent: PatchIntentDescriptor,
        scope: PatchScopeDescriptor,
        constraints: list[PatchConstraintDescriptor],
    ) -> PatchPreliminaryRiskAssessment:
        _ = request, constraints
        target_risks: list[str] = []
        boundary_risks: list[str] = []
        forbidden_patch_risks: list[str] = []
        policy_risks = ["diff_generation_deferred", "apply_not_allowed"]
        for target in targets:
            if target.path_status in {"blocked", "not_found", "ambiguous"}:
                target_risks.append(target.path_status)
            if target.private_boundary_risk:
                boundary_risks.append("private_boundary_risk")
            if target.secret_file_risk:
                boundary_risks.append("secret_file_risk")
            if target.generated_file_risk:
                target_risks.append("generated_file_risk")
        if intent.forbidden_patch_type_detected:
            forbidden_patch_risks.append("forbidden_patch_type_requested")
        if scope.scope_status == "blocked" or boundary_risks or forbidden_patch_risks:
            level = "blocked"
        elif scope.scope_status == "needs_more_input":
            level = "medium"
        elif target_risks:
            level = "medium"
        else:
            level = "low"
        return PatchPreliminaryRiskAssessment(
            risk_id=f"patch_preliminary_risk:{uuid4()}",
            risk_level=level,
            target_risks=_unique(target_risks),
            policy_risks=_unique(policy_risks),
            boundary_risks=_unique(boundary_risks),
            forbidden_patch_risks=_unique(forbidden_patch_risks),
            requires_review=True,
            safe_to_generate_diff=False,
            safe_to_apply=False,
        )


class PatchCandidateFindingService:
    def evaluate(
        self,
        request: SelfModificationRequestCreateRequest,
        targets: list[ModificationTargetRef],
        intent: PatchIntentDescriptor,
        scope: PatchScopeDescriptor,
        risk: PatchPreliminaryRiskAssessment,
    ) -> list[PatchCandidateFinding]:
        _ = request
        findings: list[PatchCandidateFinding] = []
        if not targets:
            findings.append(_finding("warning", "missing_target_path", "Target path is required.", None))
        if scope.target_count > scope.max_target_files:
            findings.append(_finding("error", "target_scope_exceeds_limit", "Target count exceeds max target files.", None))
        for target in targets:
            target_ref = target.to_dict()
            if target.path_status == "blocked":
                findings.append(_finding("error", "target_path_blocked", "Target path is blocked by policy.", target_ref))
            if target.path_status == "not_found":
                findings.append(_finding("warning", "target_not_found", "Target path was not found.", target_ref))
            if target.path_status == "ambiguous":
                findings.append(_finding("warning", "ambiguous_target_path", "Target path is ambiguous.", target_ref))
            if target.private_boundary_risk:
                findings.append(_finding("critical", "private_boundary_risk", "Target crosses private boundary risk.", target_ref))
            if target.secret_file_risk:
                findings.append(_finding("critical", "secret_file_risk", "Target resembles a secret-bearing file.", target_ref))
            if target.generated_file_risk:
                findings.append(_finding("warning", "generated_file_risk", "Target appears generated or build output.", target_ref))
        if intent.forbidden_patch_type_detected:
            findings.append(_finding("error", "forbidden_patch_type_requested", "Requested patch type is forbidden.", None))
        if risk.risk_level == "blocked":
            findings.append(_finding("error", "apply_not_allowed", "Candidate cannot be applied in v0.22.1.", None))
        if scope.scope_status == "needs_more_input" or intent.requires_operator_clarification:
            findings.append(_finding("warning", "requires_more_input", "More operator input is required.", None))
        findings.append(_finding("info", "diff_generation_deferred", "Diff generation is deferred to v0.22.2.", None))
        if not findings:
            findings.append(_finding("info", "ok", "Patch candidate is candidate-only and ready for later diff preview.", None))
        return findings


class SelfModificationRequestPolicyService:
    def decide(
        self,
        request: SelfModificationRequestCreateRequest,
        scope: PatchScopeDescriptor,
        intent: PatchIntentDescriptor,
        risk: PatchPreliminaryRiskAssessment,
    ) -> str:
        normalized = request.normalized()
        if risk.risk_level == "blocked" or scope.scope_status == "blocked" or intent.forbidden_patch_type_detected:
            return "no_action" if normalized.allow_no_action else "blocked"
        if scope.scope_status == "needs_more_input" or intent.requires_operator_clarification:
            return "needs_more_input" if normalized.allow_needs_more_input else "blocked"
        return "candidate_created"


class SelfModificationRequestCandidateService:
    def __init__(
        self,
        *,
        target_resolver: ModificationTargetResolver | None = None,
        intent_classifier: PatchIntentClassifier | None = None,
        scope_builder: PatchScopeBuilder | None = None,
        constraint_builder: PatchConstraintBuilder | None = None,
        risk_service: PatchPreliminaryRiskService | None = None,
        finding_service: PatchCandidateFindingService | None = None,
        policy_service: SelfModificationRequestPolicyService | None = None,
    ) -> None:
        self.target_resolver = target_resolver or ModificationTargetResolver()
        self.intent_classifier = intent_classifier or PatchIntentClassifier()
        self.scope_builder = scope_builder or PatchScopeBuilder()
        self.constraint_builder = constraint_builder or PatchConstraintBuilder()
        self.risk_service = risk_service or PatchPreliminaryRiskService()
        self.finding_service = finding_service or PatchCandidateFindingService()
        self.policy_service = policy_service or SelfModificationRequestPolicyService()

    def create_request_and_candidate(
        self,
        request: SelfModificationRequestCreateRequest,
    ) -> SelfModificationRequestCandidateResult:
        normalized = request.normalized()
        created_at = utc_now_iso()
        targets = self.target_resolver.resolve_targets(normalized)
        intent = self.intent_classifier.classify(normalized)
        scope = self.scope_builder.build_scope(targets, normalized)
        constraints = self.constraint_builder.build_constraints(normalized, targets)
        risk = self.risk_service.assess(normalized, targets, intent, scope, constraints)
        findings = self.finding_service.evaluate(normalized, targets, intent, scope, risk)
        decision = self.policy_service.decide(normalized, scope, intent, risk)
        request_model = SelfModificationRequest(
            request_id=f"self_modification_request:{uuid4()}",
            created_at=created_at,
            goal_text=normalized.goal_text,
            requester_type=normalized.requester_type,
            target_refs=targets,
            intent=intent,
            scope=scope,
            constraints=constraints,
            source_refs=normalized.source_refs,
            evidence_refs=_evidence_refs(targets),
            request_status=decision,
            review_status="request_only",
            file_write_enabled=False,
            apply_patch_enabled=False,
            diff_generated=False,
            applied=False,
        )
        if decision == "candidate_created":
            return SelfModificationRequestCandidateResult(
                request=request_model,
                patch_candidate=self._build_patch_candidate(request_model, risk, findings, created_at),
                no_action_candidate=None,
                needs_more_input_candidate=None,
            )
        if decision == "needs_more_input":
            return SelfModificationRequestCandidateResult(
                request=request_model,
                patch_candidate=None,
                no_action_candidate=None,
                needs_more_input_candidate=SelfModificationNeedsMoreInputCandidate(
                    candidate_id=f"self_modification_needs_more_input_candidate:{uuid4()}",
                    request_id=request_model.request_id,
                    reason="More input is required before a patch candidate can proceed.",
                    missing_inputs=_missing_inputs(normalized, targets, intent),
                    evidence_refs=request_model.evidence_refs,
                    recommended_review_decision="needs_more_input",
                    candidate_status="candidate_only",
                    applied=False,
                ),
            )
        return SelfModificationRequestCandidateResult(
            request=request_model,
            patch_candidate=None,
            no_action_candidate=SelfModificationNoActionCandidate(
                candidate_id=f"self_modification_no_action_candidate:{uuid4()}",
                request_id=request_model.request_id,
                reason="Request is blocked or not actionable under v0.22.1 safety policy.",
                evidence_refs=request_model.evidence_refs,
                recommended_review_decision="no_action",
                candidate_status="candidate_only",
                applied=False,
            ),
            needs_more_input_candidate=None,
        )

    def _build_patch_candidate(
        self,
        request: SelfModificationRequest,
        risk: PatchPreliminaryRiskAssessment,
        findings: list[PatchCandidateFinding],
        created_at: str,
    ) -> PatchCandidate:
        target_summary = ", ".join(item.relative_path or "<blocked>" for item in request.target_refs) or "unspecified target"
        title = f"Candidate-only modification request for {target_summary}"
        return PatchCandidate(
            candidate_id=f"patch_candidate:{uuid4()}",
            request_id=request.request_id,
            created_at=created_at,
            title=title,
            goal_text=request.goal_text,
            target_refs=list(request.target_refs),
            intent=request.intent,
            scope=request.scope,
            constraints=list(request.constraints),
            preliminary_risk=risk,
            findings=list(findings),
            evidence_refs=list(request.evidence_refs),
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "report_name": "Self-Modification Request/Patch Candidate PIG Report",
            "version": SELF_MODIFICATION_REQUEST_CANDIDATE_VERSION,
            "layer": "self_modification_safety",
            "subject": "modification_request_patch_candidate",
            "principles": [
                "modification request is not file mutation",
                "patch candidate is not patch draft",
                "patch candidate is not diff preview",
                "patch candidate is not patch apply",
                "no_action and needs_more_input are valid outcomes",
            ],
            "file_write_enabled": False,
            "apply_patch_enabled": False,
            "diff_generation_enabled": False,
            "patch_apply_enabled": False,
            "llm_patch_generation_enabled": False,
            "llm_judge_enabled": False,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "projection_name": "Self-Modification Request/Patch Candidate OCPX Projection",
            "state": SELF_MODIFICATION_REQUEST_CANDIDATE_STATE,
            "version": SELF_MODIFICATION_REQUEST_CANDIDATE_VERSION,
            "source_read_models": [
                "SelfModificationSafetyContractState",
                "SelfModificationPatchPolicyState",
                "SelfModificationLifecyclePolicyState",
                "SelfCapabilityTruthState",
                "SelfRuntimeBoundaryState",
                "SelfPolicyGateState",
                "SelfTraceIntegrityState",
                "SelfCandidateMemoryBoundaryState",
            ],
            "target_read_models": [
                "SelfModificationRequestState",
                "PatchCandidateState",
                "PatchPreliminaryRiskState",
                "PatchCandidateFindingState",
            ],
            "effect_types": ["read_only_observation", "state_candidate_created"],
        }

    def render_result_cli(self, result: SelfModificationRequestCandidateResult) -> str:
        request = result.request
        candidate = result.patch_candidate
        fallback = result.no_action_candidate or result.needs_more_input_candidate
        candidate_id = candidate.candidate_id if candidate else fallback.candidate_id if fallback else "none"
        lifecycle_state = candidate.lifecycle_state if candidate else request.request_status
        targets = ",".join(item.relative_path or "<blocked>" for item in request.target_refs) or "<none>"
        risk_level = candidate.preliminary_risk.risk_level if candidate else "blocked_or_needs_more_input"
        return "\n".join(
            [
                "Self-Modification Request/Patch Candidate",
                "version=v0.22.1",
                "layer=self_modification_safety",
                f"request_id={request.request_id}",
                f"candidate_id={candidate_id}",
                f"request_status={request.request_status}",
                f"target_paths={targets}",
                f"lifecycle_state={lifecycle_state}",
                "candidate_status=candidate_only",
                f"risk_level={risk_level}",
                "diff_generated=false",
                "dry_run_checked=false",
                "review_approved=false",
                "apply_gate_opened=false",
                "applied=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "safe_to_generate_diff=false",
                "safe_to_apply=false",
                "next_required_step=v0.22.2 Patch Draft / Diff Preview",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_list_cli(self) -> str:
        return "\n".join(
            [
                "Self-Modification Candidate List",
                "version=v0.22.1",
                "layer=self_modification_safety",
                "candidate_count=0",
                "storage=not_persisted_in_v0.22.1",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_view_cli(self, *, object_id: str, object_type: str) -> str:
        return "\n".join(
            [
                f"Self-Modification {object_type.title()} View",
                "version=v0.22.1",
                "layer=self_modification_safety",
                f"{object_type}_id={object_id}",
                "status=not_persisted_in_v0.22.1",
                "candidate_status=candidate_only",
                "diff_generated=false",
                "applied=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "next_required_step=v0.22.2 Patch Draft / Diff Preview",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_risks_cli(self, *, candidate_id: str) -> str:
        return "\n".join(
            [
                "Self-Modification Candidate Risks",
                "version=v0.22.1",
                "layer=self_modification_safety",
                f"candidate_id={candidate_id}",
                "risk_level=unknown_without_persisted_candidate",
                "safe_to_generate_diff=false",
                "safe_to_apply=false",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        return "\n".join(
            [
                "Self-Modification Request/Patch Candidate PIG Report",
                "version=v0.22.1",
                "layer=self_modification_safety",
                f"subject={report['subject']}",
                "status=candidate_only",
                f"principles={','.join(report['principles'])}",
                f"file_write_enabled={str(report['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(report['apply_patch_enabled']).lower()}",
                f"diff_generation_enabled={str(report['diff_generation_enabled']).lower()}",
                f"patch_apply_enabled={str(report['patch_apply_enabled']).lower()}",
                f"llm_patch_generation_enabled={str(report['llm_patch_generation_enabled']).lower()}",
                f"llm_judge_enabled={str(report['llm_judge_enabled']).lower()}",
                "no_file_mutation_occurred=true",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Self-Modification Request/Patch Candidate OCPX Projection",
                "version=v0.22.1",
                "layer=self_modification_safety",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "no_file_mutation_occurred=true",
                "No file mutation occurred.",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    target_ref: dict[str, Any] | None,
) -> PatchCandidateFinding:
    return PatchCandidateFinding(
        finding_id=f"patch_candidate_finding:{uuid4()}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        target_ref=target_ref,
        evidence_refs=[{"ref_type": "self_modification_safety_policy", "version": "v0.22.1"}],
        withdrawal_condition="Withdraw if v0.22.1 writes files, generates diffs, or applies patches.",
    )


def _evidence_refs(targets: list[ModificationTargetRef]) -> list[dict[str, Any]]:
    refs = [{"ref_type": "self_modification_safety_contract", "version": "v0.22.0"}]
    for target in targets:
        refs.extend(target.evidence_refs)
    return refs


def _missing_inputs(
    request: SelfModificationRequestCreateRequest,
    targets: list[ModificationTargetRef],
    intent: PatchIntentDescriptor,
) -> list[str]:
    missing: list[str] = []
    if not request.goal_text:
        missing.append("goal_text")
    if not targets:
        missing.append("target_path")
    if any(target.path_status == "not_found" for target in targets):
        missing.append("existing_workspace_target")
    if intent.intent_type == "unknown":
        missing.append("clear_patch_intent")
    return _unique(missing) or ["operator_clarification"]


def _looks_like_secret_path(relative_path: str) -> bool:
    path = Path(relative_path)
    lowered_name = path.name.casefold()
    lowered_parts = {part.casefold() for part in path.parts}
    return (
        lowered_name in SECRET_FILE_NAMES
        or path.suffix.casefold() in SECRET_SUFFIXES
        or "secret" in lowered_parts
        or "secrets" in lowered_parts
    )


def _looks_like_generated_path(relative_path: str) -> bool:
    path = Path(relative_path)
    lowered_parts = {part.casefold() for part in path.parts}
    return bool(lowered_parts & GENERATED_PARTS) or path.suffix.casefold() in {".lock", ".pyc"}


def _file_kind(relative_path: str, target_type: str) -> str | None:
    if target_type == "workspace_directory":
        return "directory"
    suffix = Path(relative_path).suffix.casefold()
    if suffix in BINARY_SUFFIXES:
        return "binary"
    if suffix in {".md", ".markdown", ".rst", ".txt"}:
        return "docs"
    if suffix in {".py", ".js", ".ts", ".tsx", ".jsx", ".rs", ".go"}:
        return "source"
    if suffix in {".toml", ".yaml", ".yml", ".json", ".ini", ".cfg"}:
        return "config"
    return "unknown"


def _unique(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
