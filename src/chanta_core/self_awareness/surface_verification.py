from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

from chanta_core.self_awareness.workspace_awareness import READ_ONLY_OBSERVATION_EFFECT
from chanta_core.utility.time import utc_now_iso


SURFACE_VERIFICATION_EFFECTS = [READ_ONLY_OBSERVATION_EFFECT, "state_candidate_created"]
SURFACE_VERIFICATION_STATE = "self_surface_verification_awareness"
SUPPORTED_SURFACE_TARGET_TYPES = {
    "path_resolution",
    "workspace_inventory_report",
    "text_read_result",
    "workspace_search_result",
    "structure_summary_candidate",
    "project_structure_candidate",
    "surface_candidate",
    "directed_intention_candidate_bundle",
    "plan_candidate",
    "todo_candidate",
    "no_action_candidate",
    "needs_more_input_candidate",
    "redaction_report",
    "self_awareness_layer",
}
SUPPORTED_STRICTNESS = {"lenient", "standard", "strict"}
SECRET_PATTERNS = [
    re.compile(r"(?i)\b(password|api[_-]?key|secret|token)\s*[:=]\s*[^\s,;]+"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9_]{20,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]{20,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]


@dataclass(frozen=True)
class SelfSurfaceVerificationRequest:
    target_type: str
    target_id: str | None = None
    target_payload: dict[str, Any] | None = None
    root_id: str | None = None
    strictness: str = "standard"
    include_evidence_checks: bool = True
    include_boundary_checks: bool = True
    include_candidate_checks: bool = True

    def normalized(self) -> "SelfSurfaceVerificationRequest":
        strictness = self.strictness if self.strictness in SUPPORTED_STRICTNESS else "standard"
        return SelfSurfaceVerificationRequest(
            target_type=self.target_type,
            target_id=self.target_id,
            target_payload=dict(self.target_payload or {}),
            root_id=self.root_id,
            strictness=strictness,
            include_evidence_checks=bool(self.include_evidence_checks),
            include_boundary_checks=bool(self.include_boundary_checks),
            include_candidate_checks=bool(self.include_candidate_checks),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_type": self.target_type,
            "target_id": self.target_id,
            "target_payload": dict(self.target_payload or {}),
            "root_id": self.root_id,
            "strictness": self.strictness,
            "include_evidence_checks": self.include_evidence_checks,
            "include_boundary_checks": self.include_boundary_checks,
            "include_candidate_checks": self.include_candidate_checks,
        }


@dataclass(frozen=True)
class SelfSurfaceVerificationFinding:
    finding_id: str
    severity: Literal["info", "warning", "error", "critical"]
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
class EvidenceCoverageReport:
    target_id: str | None
    evidence_ref_count: int
    checked_ref_count: int
    missing_ref_count: int
    invalid_ref_count: int
    coverage_status: Literal["sufficient", "partial", "insufficient", "not_applicable"]
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "evidence_ref_count": self.evidence_ref_count,
            "checked_ref_count": self.checked_ref_count,
            "missing_ref_count": self.missing_ref_count,
            "invalid_ref_count": self.invalid_ref_count,
            "coverage_status": self.coverage_status,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class BoundaryConsistencyReport:
    target_id: str | None
    read_only_observation: bool
    state_candidate_created: bool
    mutates_workspace: bool
    mutates_memory: bool
    mutates_persona: bool
    mutates_overlay: bool
    uses_shell: bool
    uses_network: bool
    uses_mcp: bool
    loads_plugin: bool
    executes_external_harness: bool
    dangerous_capability: bool
    boundary_status: Literal["ok", "warning", "violation"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "read_only_observation": self.read_only_observation,
            "state_candidate_created": self.state_candidate_created,
            "mutates_workspace": self.mutates_workspace,
            "mutates_memory": self.mutates_memory,
            "mutates_persona": self.mutates_persona,
            "mutates_overlay": self.mutates_overlay,
            "uses_shell": self.uses_shell,
            "uses_network": self.uses_network,
            "uses_mcp": self.uses_mcp,
            "loads_plugin": self.loads_plugin,
            "executes_external_harness": self.executes_external_harness,
            "dangerous_capability": self.dangerous_capability,
            "boundary_status": self.boundary_status,
        }


@dataclass(frozen=True)
class CandidateSemanticsReport:
    target_id: str | None
    is_candidate: bool
    review_status: str | None
    canonical_promotion_enabled: bool
    promoted: bool
    memory_mutation_detected: bool
    persona_mutation_detected: bool
    overlay_mutation_detected: bool
    candidate_status: Literal["ok", "warning", "violation"]

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "is_candidate": self.is_candidate,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
            "memory_mutation_detected": self.memory_mutation_detected,
            "persona_mutation_detected": self.persona_mutation_detected,
            "overlay_mutation_detected": self.overlay_mutation_detected,
            "candidate_status": self.candidate_status,
        }


@dataclass(frozen=True)
class SelfSurfaceVerificationReport:
    report_id: str
    target_type: str
    target_id: str | None
    status: Literal["passed", "warning", "failed", "blocked"]
    strictness: str
    checked_at: str
    findings: list[SelfSurfaceVerificationFinding]
    evidence_coverage: dict[str, Any]
    boundary_status: dict[str, Any]
    candidate_status: dict[str, Any]
    limitations: list[str]
    review_status: str = "candidate_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False
    report_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "target_type": self.target_type,
            "target_id": self.target_id,
            "status": self.status,
            "strictness": self.strictness,
            "checked_at": self.checked_at,
            "findings": [item.to_dict() for item in self.findings],
            "evidence_coverage": dict(self.evidence_coverage),
            "boundary_status": dict(self.boundary_status),
            "candidate_status": dict(self.candidate_status),
            "limitations": list(self.limitations),
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
            "report_attrs": dict(self.report_attrs),
        }


class SelfSurfaceVerificationPolicyService:
    def decide(self, request: SelfSurfaceVerificationRequest) -> tuple[bool, list[SelfSurfaceVerificationFinding]]:
        normalized = request.normalized()
        if normalized.target_type not in SUPPORTED_SURFACE_TARGET_TYPES:
            return False, [
                _finding(
                    "error",
                    "unsupported_target_type",
                    "Target type is not supported for self-surface verification.",
                    normalized,
                )
            ]
        return True, []


class EvidenceConsistencyVerifier:
    def verify(self, request: SelfSurfaceVerificationRequest) -> tuple[EvidenceCoverageReport, list[SelfSurfaceVerificationFinding]]:
        payload = dict(request.target_payload or {})
        findings: list[SelfSurfaceVerificationFinding] = []
        evidence_refs = _list_of_dicts(payload.get("evidence_refs"))
        refs_required = request.target_type not in {"path_resolution", "self_awareness_layer", "redaction_report"}
        if refs_required and not evidence_refs:
            findings.append(_finding("warning", "missing_evidence_ref", "Required evidence_refs are missing.", request))
        invalid_ref_count = 0
        for ref in evidence_refs:
            if _invalid_line_ref(ref):
                invalid_ref_count += 1
                findings.append(_finding("warning", "invalid_line_ref", "Evidence ref has an invalid line reference.", request, [ref]))
        findings.extend(_target_specific_evidence_findings(request, payload))
        if request.strictness == "strict":
            findings = [_strict_finding(item) for item in findings]
        missing_count = 1 if refs_required and not evidence_refs else 0
        coverage = "not_applicable"
        if refs_required:
            coverage = "sufficient" if not missing_count and not invalid_ref_count else "partial" if evidence_refs else "insufficient"
        return (
            EvidenceCoverageReport(
                target_id=request.target_id,
                evidence_ref_count=len(evidence_refs),
                checked_ref_count=len(evidence_refs),
                missing_ref_count=missing_count,
                invalid_ref_count=invalid_ref_count,
                coverage_status=coverage,  # type: ignore[arg-type]
                notes=["structural_evidence_check_only"],
            ),
            findings,
        )


class BoundaryConsistencyVerifier:
    def verify(self, request: SelfSurfaceVerificationRequest) -> tuple[BoundaryConsistencyReport, list[SelfSurfaceVerificationFinding]]:
        payload = dict(request.target_payload or {})
        attrs = _merged_attrs(payload)
        effect_types = _effect_types(payload)
        findings: list[SelfSurfaceVerificationFinding] = []
        read_only = READ_ONLY_OBSERVATION_EFFECT in effect_types or payload.get("effect_type") == READ_ONLY_OBSERVATION_EFFECT
        if payload and not read_only:
            findings.append(_finding("warning", "unexpected_execution_flag", "read_only_observation effect is missing.", request))
        flag_map = {
            "mutates_workspace": "unexpected_mutation_flag",
            "mutates_memory": "unexpected_mutation_flag",
            "mutates_persona": "unexpected_mutation_flag",
            "mutates_overlay": "unexpected_mutation_flag",
            "uses_shell": "unexpected_execution_flag",
            "uses_network": "unexpected_execution_flag",
            "uses_mcp": "unexpected_execution_flag",
            "loads_plugin": "unexpected_execution_flag",
            "executes_external_harness": "unexpected_execution_flag",
            "dangerous_capability": "unexpected_execution_flag",
        }
        for key, finding_type in flag_map.items():
            if bool(attrs.get(key) or payload.get(key)):
                findings.append(_finding("error", finding_type, f"{key}=true is not allowed for self-awareness surfaces.", request))
        if _contains_secret_like(payload):
            findings.append(_finding("critical", "unredacted_secret_risk", "Secret-like returned content was detected.", request))
        status = "violation" if any(item.severity in {"error", "critical"} for item in findings) else "warning" if findings else "ok"
        return (
            BoundaryConsistencyReport(
                target_id=request.target_id,
                read_only_observation=read_only,
                state_candidate_created="state_candidate_created" in effect_types,
                mutates_workspace=bool(attrs.get("mutates_workspace") or payload.get("mutates_workspace")),
                mutates_memory=bool(attrs.get("mutates_memory") or payload.get("mutates_memory")),
                mutates_persona=bool(attrs.get("mutates_persona") or payload.get("mutates_persona")),
                mutates_overlay=bool(attrs.get("mutates_overlay") or payload.get("mutates_overlay")),
                uses_shell=bool(attrs.get("uses_shell") or payload.get("uses_shell")),
                uses_network=bool(attrs.get("uses_network") or payload.get("uses_network")),
                uses_mcp=bool(attrs.get("uses_mcp") or payload.get("uses_mcp")),
                loads_plugin=bool(attrs.get("loads_plugin") or payload.get("loads_plugin")),
                executes_external_harness=bool(attrs.get("executes_external_harness") or payload.get("executes_external_harness")),
                dangerous_capability=bool(attrs.get("dangerous_capability") or payload.get("dangerous_capability")),
                boundary_status=status,  # type: ignore[arg-type]
            ),
            findings,
        )


class CandidateSemanticsVerifier:
    def verify(self, request: SelfSurfaceVerificationRequest) -> tuple[CandidateSemanticsReport, list[SelfSurfaceVerificationFinding]]:
        payload = dict(request.target_payload or {})
        attrs = _merged_attrs(payload)
        is_candidate = request.target_type in {
            "structure_summary_candidate",
            "project_structure_candidate",
            "surface_candidate",
            "directed_intention_candidate_bundle",
            "plan_candidate",
            "todo_candidate",
            "no_action_candidate",
            "needs_more_input_candidate",
            "self_awareness_layer",
        } or "candidate_id" in payload or "report_id" in payload
        review_status = payload.get("review_status")
        canonical = bool(payload.get("canonical_promotion_enabled") or attrs.get("canonical_promotion_enabled"))
        promoted = bool(payload.get("promoted") or attrs.get("promoted"))
        memory = bool(attrs.get("memory_mutation_used") or payload.get("mutates_memory"))
        persona = bool(attrs.get("persona_mutation_used") or payload.get("mutates_persona"))
        overlay = bool(attrs.get("overlay_mutation_used") or payload.get("mutates_overlay"))
        findings: list[SelfSurfaceVerificationFinding] = []
        if is_candidate and review_status not in {None, "candidate_only"}:
            findings.append(_finding("warning", "candidate_promotion_violation", "Candidate review_status is not candidate_only.", request))
        if canonical:
            findings.append(_finding("error", "candidate_promotion_violation", "canonical_promotion_enabled=true is not allowed.", request))
        if promoted:
            findings.append(_finding("error", "candidate_promotion_violation", "promoted=true is not allowed.", request))
        for enabled, label in [(memory, "memory"), (persona, "persona"), (overlay, "overlay")]:
            if enabled:
                findings.append(_finding("error", "unexpected_mutation_flag", f"{label} mutation flag is enabled.", request))
        status = "violation" if any(item.severity in {"error", "critical"} for item in findings) else "warning" if findings else "ok"
        return (
            CandidateSemanticsReport(
                target_id=request.target_id,
                is_candidate=is_candidate,
                review_status=str(review_status) if review_status is not None else None,
                canonical_promotion_enabled=canonical,
                promoted=promoted,
                memory_mutation_detected=memory,
                persona_mutation_detected=persona,
                overlay_mutation_detected=overlay,
                candidate_status=status,  # type: ignore[arg-type]
            ),
            findings,
        )


class SelfSurfaceVerificationService:
    def __init__(self) -> None:
        self.policy_service = SelfSurfaceVerificationPolicyService()
        self.evidence_verifier = EvidenceConsistencyVerifier()
        self.boundary_verifier = BoundaryConsistencyVerifier()
        self.candidate_verifier = CandidateSemanticsVerifier()

    def verify_surface(self, request: SelfSurfaceVerificationRequest) -> SelfSurfaceVerificationReport:
        normalized = request.normalized()
        allowed, policy_findings = self.policy_service.decide(normalized)
        if not allowed:
            return _report(normalized, policy_findings, None, None, None, blocked=True)
        findings = list(policy_findings)
        evidence = EvidenceCoverageReport(normalized.target_id, 0, 0, 0, 0, "not_applicable", [])
        boundary = BoundaryConsistencyReport(
            normalized.target_id,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            "ok",
        )
        candidate = CandidateSemanticsReport(normalized.target_id, False, None, False, False, False, False, False, "ok")
        if normalized.include_evidence_checks:
            evidence, evidence_findings = self.evidence_verifier.verify(normalized)
            findings.extend(evidence_findings)
        if normalized.include_boundary_checks:
            boundary, boundary_findings = self.boundary_verifier.verify(normalized)
            findings.extend(boundary_findings)
        if normalized.include_candidate_checks:
            candidate, candidate_findings = self.candidate_verifier.verify(normalized)
            findings.extend(candidate_findings)
        if not findings:
            findings.append(_finding("info", "ok", "Surface verification checks passed.", normalized))
        return _report(normalized, findings, evidence, boundary, candidate, blocked=False)


class SelfSurfaceVerificationSkillService:
    def __init__(self) -> None:
        self.service = SelfSurfaceVerificationService()

    def verify_surface(self, request: SelfSurfaceVerificationRequest) -> SelfSurfaceVerificationReport:
        return self.service.verify_surface(request)


def _target_specific_evidence_findings(
    request: SelfSurfaceVerificationRequest,
    payload: dict[str, Any],
) -> list[SelfSurfaceVerificationFinding]:
    findings: list[SelfSurfaceVerificationFinding] = []
    if request.target_type == "workspace_search_result":
        for match in _list_of_dicts(payload.get("matches")):
            if not match.get("relative_path") or not _positive_int(match.get("line_number")):
                findings.append(_finding("error", "search_match_without_source", "Search match is missing source path or line number.", request))
    if request.target_type == "structure_summary_candidate":
        markdown = payload.get("markdown") if isinstance(payload.get("markdown"), dict) else {}
        for heading in _list_of_dicts(markdown.get("headings")):
            if not _positive_int(heading.get("line_number")):
                findings.append(_finding("warning", "invalid_line_ref", "Markdown heading is missing a valid line number.", request))
        python = payload.get("python") if isinstance(payload.get("python"), dict) else {}
        for key in ["imports", "top_level_functions", "top_level_classes", "top_level_assignments"]:
            for symbol in _list_of_dicts(python.get(key)):
                if not _positive_int(symbol.get("line_number")):
                    findings.append(_finding("warning", "invalid_line_ref", "Python symbol is missing a valid line number.", request))
    if request.target_type in {"project_structure_candidate", "surface_candidate"}:
        surfaces = _list_of_dicts(payload.get("surface_candidates")) or ([payload] if request.target_type == "surface_candidate" else [])
        for item in surfaces:
            if not item.get("reason") or not _list_of_dicts(item.get("evidence_refs")):
                findings.append(
                    _finding(
                        "warning",
                        "project_surface_candidate_weak_evidence",
                        "Project surface candidate is missing reason or evidence_refs.",
                        request,
                    )
                )
    if payload.get("truncated") is True and not _has_truncation_limitation(payload):
        findings.append(_finding("warning", "truncated_result_requires_limitation", "Truncated result lacks a truncation limitation.", request))
    return findings


def _report(
    request: SelfSurfaceVerificationRequest,
    findings: list[SelfSurfaceVerificationFinding],
    evidence: EvidenceCoverageReport | None,
    boundary: BoundaryConsistencyReport | None,
    candidate: CandidateSemanticsReport | None,
    *,
    blocked: bool,
) -> SelfSurfaceVerificationReport:
    status = _status(findings, blocked)
    return SelfSurfaceVerificationReport(
        report_id=f"self_surface_verification_report:{uuid4()}",
        target_type=request.target_type,
        target_id=request.target_id,
        status=status,
        strictness=request.strictness,
        checked_at=utc_now_iso(),
        findings=findings,
        evidence_coverage=(evidence or EvidenceCoverageReport(request.target_id, 0, 0, 0, 0, "not_applicable", [])).to_dict(),
        boundary_status=(boundary or BoundaryConsistencyReport(request.target_id, False, False, False, False, False, False, False, False, False, False, False, False, "warning")).to_dict(),
        candidate_status=(candidate or CandidateSemanticsReport(request.target_id, False, None, False, False, False, False, False, "warning")).to_dict(),
        limitations=["structural_surface_verification_only", "no_test_or_runtime_execution", "no_semantic_truth_verification"],
        report_attrs=_report_attrs(blocked=blocked),
    )


def _status(findings: list[SelfSurfaceVerificationFinding], blocked: bool) -> Literal["passed", "warning", "failed", "blocked"]:
    if blocked or any(item.finding_type == "unsupported_target_type" for item in findings):
        return "blocked"
    if any(item.severity in {"critical", "error"} for item in findings):
        return "failed"
    if any(item.severity == "warning" for item in findings):
        return "warning"
    return "passed"


def _finding(
    severity: str,
    finding_type: str,
    message: str,
    request: SelfSurfaceVerificationRequest,
    evidence_refs: list[dict[str, Any]] | None = None,
) -> SelfSurfaceVerificationFinding:
    return SelfSurfaceVerificationFinding(
        finding_id=f"self_surface_verification_finding:{uuid4()}",
        severity=severity,  # type: ignore[arg-type]
        finding_type=finding_type,
        message=message,
        target_ref={"target_type": request.target_type, "target_id": request.target_id},
        evidence_refs=[_safe_ref(item) for item in evidence_refs or []],
        withdrawal_condition="Withdraw this verification if a stronger bounded evidence owner contradicts this structural finding.",
    )


def _strict_finding(finding: SelfSurfaceVerificationFinding) -> SelfSurfaceVerificationFinding:
    if finding.severity != "warning":
        return finding
    return SelfSurfaceVerificationFinding(
        finding_id=finding.finding_id,
        severity="error",
        finding_type=finding.finding_type,
        message=finding.message,
        target_ref=finding.target_ref,
        evidence_refs=finding.evidence_refs,
        withdrawal_condition=finding.withdrawal_condition,
    )


def _list_of_dicts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        return []
    return [dict(item) for item in value if isinstance(item, dict)]


def _invalid_line_ref(ref: dict[str, Any]) -> bool:
    if "line_number" in ref and not _positive_int(ref.get("line_number")):
        return True
    if "line_range" in ref:
        value = ref.get("line_range")
        if not isinstance(value, list) or len(value) != 2:
            return True
        return not all(_positive_int(item) for item in value)
    return False


def _positive_int(value: Any) -> bool:
    return isinstance(value, int) and value > 0


def _merged_attrs(payload: dict[str, Any]) -> dict[str, Any]:
    attrs: dict[str, Any] = {}
    for key in ["candidate_attrs", "report_attrs", "result_attrs", "skill_attrs", "contract_attrs"]:
        item = payload.get(key)
        if isinstance(item, dict):
            attrs.update(item)
    return attrs


def _effect_types(payload: dict[str, Any]) -> set[str]:
    effect_types: set[str] = set()
    raw = payload.get("effect_types")
    if isinstance(raw, list):
        effect_types.update(str(item) for item in raw)
    attrs = _merged_attrs(payload)
    raw_attrs = attrs.get("effect_types")
    if isinstance(raw_attrs, list):
        effect_types.update(str(item) for item in raw_attrs)
    if payload.get("effect_type"):
        effect_types.add(str(payload["effect_type"]))
    if attrs.get("effect_type"):
        effect_types.add(str(attrs["effect_type"]))
    return effect_types


def _contains_secret_like(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_contains_secret_like(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_secret_like(item) for item in value)
    if not isinstance(value, str):
        return False
    return any(pattern.search(value) for pattern in SECRET_PATTERNS)


def _has_truncation_limitation(payload: dict[str, Any]) -> bool:
    limitations = payload.get("limitations")
    if not isinstance(limitations, list):
        return False
    return any("truncat" in str(item).casefold() for item in limitations)


def _safe_ref(value: dict[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key in ["relative_path", "path", "line_number", "line_range", "summary_mode", "finding_type", "candidate_type"]:
        if key in value:
            safe[key] = value[key]
    return safe


def _report_attrs(*, blocked: bool) -> dict[str, Any]:
    return {
        "effect_types": list(SURFACE_VERIFICATION_EFFECTS),
        "read_only": True,
        "policy_gated": True,
        "evidence_checking_only": True,
        "test_execution_used": False,
        "shell_execution_used": False,
        "network_access_used": False,
        "mcp_connection_used": False,
        "plugin_loading_used": False,
        "external_harness_execution_used": False,
        "model_judge_used": False,
        "semantic_truth_verification_used": False,
        "canonical_promotion_enabled": False,
        "promoted": False,
        "blocked": blocked,
        "workspace_write_used": False,
        "memory_mutation_used": False,
        "persona_mutation_used": False,
        "overlay_mutation_used": False,
    }
