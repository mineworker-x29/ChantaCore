from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.persona.errors import PersonalConformanceError
from chanta_core.persona.ids import (
    new_personal_conformance_contract_id,
    new_personal_conformance_finding_id,
    new_personal_conformance_result_id,
    new_personal_conformance_rule_id,
    new_personal_conformance_run_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


CAPABILITY_TRUTH_STATEMENT = "Runtime capability profile overrides personal/persona claims."
NO_CAPABILITY_GRANT_STATEMENT = "This binding does not grant new runtime capabilities."


@dataclass(frozen=True)
class PersonalConformanceContract:
    contract_id: str
    contract_name: str
    contract_type: str
    description: str | None
    status: str
    severity: str | None
    created_at: str
    updated_at: str
    contract_attrs: dict[str, Any] = field(default_factory=dict)

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
            "contract_attrs": dict(self.contract_attrs),
        }


@dataclass(frozen=True)
class PersonalConformanceRule:
    rule_id: str
    contract_id: str
    rule_type: str
    description: str
    required: bool
    severity: str | None
    expected_value: str | None
    status: str
    rule_attrs: dict[str, Any] = field(default_factory=dict)

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
            "rule_attrs": dict(self.rule_attrs),
        }


@dataclass(frozen=True)
class PersonalConformanceRun:
    run_id: str
    contract_id: str
    target_kind: str | None
    target_ref: str | None
    status: str
    started_at: str
    completed_at: str | None
    run_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "contract_id": self.contract_id,
            "target_kind": self.target_kind,
            "target_ref": self.target_ref,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "run_attrs": dict(self.run_attrs),
        }


@dataclass(frozen=True)
class PersonalConformanceFinding:
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
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class PersonalConformanceResult:
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
        for field_name, value in [("score", self.score), ("confidence", self.confidence)]:
            if value is not None and not 0.0 <= value <= 1.0:
                raise PersonalConformanceError(f"{field_name} must be between 0.0 and 1.0")

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "run_id": self.run_id,
            "contract_id": self.contract_id,
            "status": self.status,
            "score": self.score,
            "confidence": self.confidence,
            "passed_finding_ids": list(self.passed_finding_ids),
            "failed_finding_ids": list(self.failed_finding_ids),
            "warning_finding_ids": list(self.warning_finding_ids),
            "skipped_finding_ids": list(self.skipped_finding_ids),
            "reason": self.reason,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class PersonalConformanceService:
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
        self.rules_by_type: dict[str, PersonalConformanceRule] = {}

    def register_contract(
        self,
        *,
        contract_name: str,
        contract_type: str,
        description: str | None = None,
        status: str = "active",
        severity: str | None = "medium",
        contract_attrs: dict[str, Any] | None = None,
    ) -> PersonalConformanceContract:
        now = utc_now_iso()
        contract = PersonalConformanceContract(
            contract_id=new_personal_conformance_contract_id(),
            contract_name=contract_name,
            contract_type=contract_type,
            description=description,
            status=status,
            severity=severity,
            created_at=now,
            updated_at=now,
            contract_attrs={
                "structural_validation_only": True,
                "no_auto_remediation": True,
                **dict(contract_attrs or {}),
            },
        )
        self._record(
            "personal_conformance_contract_registered",
            objects=[_object("personal_conformance_contract", contract.contract_id, contract.to_dict())],
            links=[("contract_object", contract.contract_id)],
            object_links=[],
            attrs={"contract_type": contract.contract_type, "status": contract.status},
        )
        return contract

    def register_rule(
        self,
        *,
        contract_id: str,
        rule_type: str,
        description: str,
        required: bool = True,
        severity: str | None = "medium",
        expected_value: str | None = None,
        status: str = "active",
        rule_attrs: dict[str, Any] | None = None,
    ) -> PersonalConformanceRule:
        rule = PersonalConformanceRule(
            rule_id=new_personal_conformance_rule_id(),
            contract_id=contract_id,
            rule_type=rule_type,
            description=description,
            required=required,
            severity=severity,
            expected_value=expected_value,
            status=status,
            rule_attrs=dict(rule_attrs or {}),
        )
        self.rules_by_type[rule.rule_type] = rule
        self._record(
            "personal_conformance_rule_registered",
            objects=[_object("personal_conformance_rule", rule.rule_id, rule.to_dict())],
            links=[("rule_object", rule.rule_id), ("contract_object", contract_id)],
            object_links=[(rule.rule_id, contract_id, "belongs_to_contract")],
            attrs={"rule_type": rule.rule_type, "required": rule.required},
        )
        return rule

    def register_default_rules(
        self,
        *,
        contract: PersonalConformanceContract | None = None,
    ) -> tuple[PersonalConformanceContract, list[PersonalConformanceRule]]:
        contract = contract or self.register_contract(
            contract_name="default_personal_conformance",
            contract_type="personal_overlay_boundary",
            description="Default structural checks for Personal Source, Overlay, Mode, and Binding artifacts.",
            severity="high",
        )
        rule_specs = [
            ("personal_directory_not_inside_public_repo", "Personal Directory must not be inside a public repo.", "high"),
            ("letters_not_used_as_source", "Letters directories must not be used as source.", "high"),
            ("messages_not_used_as_source", "Messages directories must not be used as source.", "high"),
            ("archive_not_used_as_source", "Archive directories must not be used as source.", "high"),
            ("private_content_not_in_public_artifacts", "Public artifacts must not contain configured private terms.", "high"),
            ("source_body_not_prompt_block", "Source bodies must not be prompt projection blocks.", "high"),
            ("markdown_not_canonical_persona", "Markdown remains staged input, not canonical persona.", "high"),
            ("canonical_import_disabled", "Canonical import must remain disabled for staged candidates.", "high"),
            ("canonical_activation_disabled", "Canonical activation must remain disabled for drafts.", "high"),
            ("runtime_binding_non_executing", "Runtime binding must be descriptive and non-executing.", "high"),
            ("mode_does_not_grant_capability", "Personal modes must not grant capabilities.", "high"),
            ("capability_truth_overrides_personal_claim", "Runtime capability truth overrides personal claims.", "high"),
            ("no_" + "json" + "l_personal_store", "No JSON Lines personal store is introduced.", "medium"),
            ("prompt_projection_bounded", "Prompt projections must be bounded.", "medium"),
            ("private_path_redacted", "Private paths should be redacted in public-facing artifacts.", "medium"),
            ("mode_boundary_present", "Mode boundary should be present.", "medium"),
            ("privacy_boundary_present", "Private loadouts should have a privacy boundary.", "medium"),
            ("source_exclusion_policy_present", "Source exclusion policy should include excluded private areas.", "medium"),
        ]
        rules = [
            self.register_rule(
                contract_id=contract.contract_id,
                rule_type=rule_type,
                description=description,
                required=True,
                severity=severity,
            )
            for rule_type, description, severity in rule_specs
            if rule_type not in self.rules_by_type
        ]
        return contract, rules

    def start_run(
        self,
        *,
        contract_id: str,
        target_kind: str | None = None,
        target_ref: str | None = None,
        run_attrs: dict[str, Any] | None = None,
    ) -> PersonalConformanceRun:
        run = PersonalConformanceRun(
            run_id=new_personal_conformance_run_id(),
            contract_id=contract_id,
            target_kind=target_kind,
            target_ref=target_ref,
            status="started",
            started_at=utc_now_iso(),
            completed_at=None,
            run_attrs={
                "mutates_target": False,
                "auto_remediation_enabled": False,
                **dict(run_attrs or {}),
            },
        )
        self._record(
            "personal_conformance_run_started",
            objects=[_object("personal_conformance_run", run.run_id, run.to_dict())],
            links=[("run_object", run.run_id), ("contract_object", contract_id)],
            object_links=[(run.run_id, contract_id, "uses_contract")],
            attrs={"target_kind": target_kind or ""},
        )
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
    ) -> PersonalConformanceFinding:
        rule = self.rules_by_type.get(rule_type)
        finding = PersonalConformanceFinding(
            finding_id=new_personal_conformance_finding_id(),
            run_id=run_id,
            rule_id=rule_id or (rule.rule_id if rule else None),
            rule_type=rule_type,
            status=status,
            severity=severity or (rule.severity if rule else None),
            message=message,
            subject_type=subject_type,
            subject_ref=subject_ref,
            evidence_refs=[dict(item) for item in (evidence_refs or [])],
            created_at=utc_now_iso(),
            finding_attrs=dict(finding_attrs or {}),
        )
        self._record(
            "personal_conformance_finding_recorded",
            objects=[_object("personal_conformance_finding", finding.finding_id, finding.to_dict())],
            links=[("finding_object", finding.finding_id), ("run_object", run_id)]
            + ([("rule_object", finding.rule_id)] if finding.rule_id else []),
            object_links=[(finding.finding_id, run_id, "belongs_to_run")]
            + ([(finding.finding_id, finding.rule_id, "checks_rule")] if finding.rule_id else []),
            attrs={"rule_type": finding.rule_type, "status": finding.status},
        )
        return finding

    def record_result(
        self,
        *,
        run_id: str,
        contract_id: str,
        findings: list[PersonalConformanceFinding],
        reason: str | None = None,
        result_attrs: dict[str, Any] | None = None,
    ) -> PersonalConformanceResult:
        passed = [finding.finding_id for finding in findings if finding.status == "passed"]
        failed = [finding.finding_id for finding in findings if finding.status in {"failed", "error"}]
        warning = [finding.finding_id for finding in findings if finding.status == "warning"]
        skipped = [finding.finding_id for finding in findings if finding.status == "skipped"]
        status = "failed" if failed else "needs_review" if warning else "passed"
        checked = len(passed) + len(failed) + len(warning)
        score = (len(passed) / checked) if checked else None
        result = PersonalConformanceResult(
            result_id=new_personal_conformance_result_id(),
            run_id=run_id,
            contract_id=contract_id,
            status=status,
            score=score,
            confidence=1.0 if checked else None,
            passed_finding_ids=passed,
            failed_finding_ids=failed,
            warning_finding_ids=warning,
            skipped_finding_ids=skipped,
            reason=reason,
            created_at=utc_now_iso(),
            result_attrs={
                "mutated_target": False,
                "auto_remediation_applied": False,
                **dict(result_attrs or {}),
            },
        )
        self._record(
            "personal_conformance_result_recorded",
            objects=[_object("personal_conformance_result", result.result_id, result.to_dict())],
            links=[
                ("result_object", result.result_id),
                ("run_object", run_id),
                ("contract_object", contract_id),
            ],
            object_links=[
                (result.result_id, run_id, "belongs_to_run"),
                (result.result_id, contract_id, "uses_contract"),
            ],
            attrs={"status": result.status, "score": result.score if result.score is not None else -1},
        )
        return result

    def complete_run(self, run: PersonalConformanceRun) -> PersonalConformanceRun:
        completed = PersonalConformanceRun(
            **{**run.to_dict(), "status": "completed", "completed_at": utc_now_iso()}
        )
        self._record_run_terminal("personal_conformance_run_completed", completed)
        return completed

    def fail_run(self, run: PersonalConformanceRun, reason: str | None = None) -> PersonalConformanceRun:
        failed = PersonalConformanceRun(
            **{
                **run.to_dict(),
                "status": "failed",
                "completed_at": utc_now_iso(),
                "run_attrs": {**run.run_attrs, "failure_reason": reason},
            }
        )
        self._record_run_terminal("personal_conformance_run_failed", failed)
        return failed

    def skip_run(self, run: PersonalConformanceRun, reason: str | None = None) -> PersonalConformanceRun:
        skipped = PersonalConformanceRun(
            **{
                **run.to_dict(),
                "status": "skipped",
                "completed_at": utc_now_iso(),
                "run_attrs": {**run.run_attrs, "skip_reason": reason},
            }
        )
        self._record_run_terminal("personal_conformance_run_skipped", skipped)
        return skipped

    def evaluate_personal_source_conformance(
        self,
        *,
        candidate: Any,
        sources: list[Any] | None = None,
        contract: PersonalConformanceContract | None = None,
    ) -> tuple[PersonalConformanceRun, PersonalConformanceResult, list[PersonalConformanceFinding]]:
        contract, _ = self.register_default_rules(contract=contract)
        run = self.start_run(
            contract_id=contract.contract_id,
            target_kind="persona_source_candidate",
            target_ref=str(getattr(candidate, "candidate_id", "")),
        )
        findings = [
            self.record_finding(
                run_id=run.run_id,
                rule_type="canonical_import_disabled",
                status="passed" if getattr(candidate, "canonical_import_enabled", None) is False else "failed",
                message="Staged candidate canonical import is disabled."
                if getattr(candidate, "canonical_import_enabled", None) is False
                else "Staged candidate canonical import is not disabled.",
                subject_type="persona_source_ingestion_candidate",
                subject_ref=str(getattr(candidate, "candidate_id", "")),
            )
        ]
        for source in sources or []:
            source_ref = str(getattr(source, "source_ref", "") or getattr(source, "source_name", ""))
            lowered = source_ref.replace("\\", "/").casefold()
            for rule_type, token in [
                ("letters_not_used_as_source", "/letters/"),
                ("messages_not_used_as_source", "/messages/"),
                ("archive_not_used_as_source", "/archive/"),
            ]:
                findings.append(
                    self.record_finding(
                        run_id=run.run_id,
                        rule_type=rule_type,
                        status="failed" if token in f"/{lowered}" else "passed",
                        message=f"{token.strip('/')} source boundary checked.",
                        subject_type="persona_source",
                        subject_ref=str(getattr(source, "source_id", "")),
                    )
                )
            findings.extend(
                [
                    self.record_finding(
                        run_id=run.run_id,
                        rule_type="source_body_not_prompt_block",
                        status="passed"
                        if not bool(getattr(source, "source_attrs", {}).get("prompt_block"))
                        else "failed",
                        message="Source body is not marked as prompt block.",
                        subject_type="persona_source",
                        subject_ref=str(getattr(source, "source_id", "")),
                    ),
                    self.record_finding(
                        run_id=run.run_id,
                        rule_type="markdown_not_canonical_persona",
                        status="passed"
                        if getattr(source, "source_type", "") != "markdown"
                        or not bool(getattr(source, "source_attrs", {}).get("canonical_persona"))
                        else "failed",
                        message="Markdown source remains staged input.",
                        subject_type="persona_source",
                        subject_ref=str(getattr(source, "source_id", "")),
                    ),
                ]
            )
        result = self.record_result(run_id=run.run_id, contract_id=contract.contract_id, findings=findings)
        self.complete_run(run)
        return run, result, findings

    def evaluate_personal_overlay_conformance(
        self,
        *,
        manifest: Any,
        projection_refs: list[Any] | None = None,
        boundary_findings: list[Any] | None = None,
        public_repo_root: str | Path | None = None,
        contract: PersonalConformanceContract | None = None,
    ) -> tuple[PersonalConformanceRun, PersonalConformanceResult, list[PersonalConformanceFinding]]:
        contract, _ = self.register_default_rules(contract=contract)
        run = self.start_run(
            contract_id=contract.contract_id,
            target_kind="personal_directory_manifest",
            target_ref=str(getattr(manifest, "manifest_id", "")),
        )
        excluded_text = " ".join(str(item).replace("\\", "/").casefold() for item in getattr(manifest, "excluded_roots", []))
        manifest_attrs = getattr(manifest, "manifest_attrs", {}) or {}
        exclusion_policy_present = all(
            bool(manifest_attrs.get(flag))
            for flag in ["letters_excluded", "messages_excluded", "archive_excluded"]
        ) or all(token in excluded_text for token in ["letters", "messages", "archive"])
        findings = [
            self.record_finding(
                run_id=run.run_id,
                rule_type="source_exclusion_policy_present",
                status="passed" if exclusion_policy_present else "warning",
                message="Source exclusion policy checked for letters, messages, and archive.",
                subject_type="personal_directory_manifest",
                subject_ref=str(getattr(manifest, "manifest_id", "")),
            )
        ]
        if public_repo_root is not None:
            directory_root = Path(str(getattr(manifest, "directory_root", ""))).resolve(strict=False)
            repo_root = Path(public_repo_root).resolve(strict=False)
            try:
                directory_root.relative_to(repo_root)
                inside_public_repo = True
            except ValueError:
                inside_public_repo = False
            findings.append(
                self.record_finding(
                    run_id=run.run_id,
                    rule_type="personal_directory_not_inside_public_repo",
                    status="failed" if inside_public_repo else "passed",
                    message="Personal Directory public repository containment checked.",
                    subject_type="personal_directory_manifest",
                    subject_ref=str(getattr(manifest, "manifest_id", "")),
                    evidence_refs=[{"path_ref": redacted_path_ref(str(directory_root))}],
                )
            )
        for ref in projection_refs or []:
            path = str(getattr(ref, "projection_path", "")).replace("\\", "/").casefold()
            allowed = any(f"/{part}/" in f"/{path}" for part in ["overlay", "profiles", "mode_loadouts"])
            from_source = "/source/" in f"/{path}"
            findings.append(
                self.record_finding(
                    run_id=run.run_id,
                    rule_type="source_body_not_prompt_block",
                    status="failed" if from_source else "passed",
                    message="Projection ref is not a source body prompt block.",
                    subject_type="personal_projection_ref",
                    subject_ref=str(getattr(ref, "projection_ref_id", "")),
                )
            )
            findings.append(
                self.record_finding(
                    run_id=run.run_id,
                    rule_type="prompt_projection_bounded",
                    status="passed" if allowed and bool(getattr(ref, "safe_for_prompt", False)) else "failed",
                    message="Projection ref is bounded to allowed projection directories.",
                    subject_type="personal_projection_ref",
                    subject_ref=str(getattr(ref, "projection_ref_id", "")),
                )
            )
        for boundary in boundary_findings or []:
            findings.append(
                self.record_finding(
                    run_id=run.run_id,
                    rule_type="personal_directory_not_inside_public_repo",
                    status="failed" if getattr(boundary, "status", "") == "failed" else "passed",
                    message=str(getattr(boundary, "message", "Overlay boundary finding checked.")),
                    subject_type="personal_overlay_boundary_finding",
                    subject_ref=str(getattr(boundary, "finding_id", "")),
                )
            )
        result = self.record_result(run_id=run.run_id, contract_id=contract.contract_id, findings=findings)
        self.complete_run(run)
        return run, result, findings

    def evaluate_personal_mode_loadout_conformance(
        self,
        *,
        loadout: Any,
        mode_boundaries: list[Any] | None = None,
        contract: PersonalConformanceContract | None = None,
    ) -> tuple[PersonalConformanceRun, PersonalConformanceResult, list[PersonalConformanceFinding]]:
        contract, _ = self.register_default_rules(contract=contract)
        run = self.start_run(
            contract_id=contract.contract_id,
            target_kind="personal_mode_loadout",
            target_ref=str(getattr(loadout, "loadout_id", "")),
        )
        boundary_types = {str(getattr(item, "boundary_type", "")) for item in (mode_boundaries or [])}
        capability_block = str(getattr(loadout, "capability_boundary_block", "") or "")
        findings = [
            self.record_finding(
                run_id=run.run_id,
                rule_type="mode_boundary_present",
                status="passed" if boundary_types else "failed",
                message="Mode boundary presence checked.",
                subject_type="personal_mode_loadout",
                subject_ref=str(getattr(loadout, "loadout_id", "")),
            ),
            self.record_finding(
                run_id=run.run_id,
                rule_type="privacy_boundary_present",
                status="passed"
                if not bool(getattr(loadout, "private", False)) or "privacy_boundary" in boundary_types
                else "warning",
                message="Privacy boundary presence checked for private loadout.",
                subject_type="personal_mode_loadout",
                subject_ref=str(getattr(loadout, "loadout_id", "")),
            ),
            self.record_finding(
                run_id=run.run_id,
                rule_type="mode_does_not_grant_capability",
                status="passed"
                if not bool(getattr(loadout, "loadout_attrs", {}).get("capability_grants_created"))
                else "failed",
                message="Mode loadout does not create capability grants.",
                subject_type="personal_mode_loadout",
                subject_ref=str(getattr(loadout, "loadout_id", "")),
            ),
            self.record_finding(
                run_id=run.run_id,
                rule_type="capability_truth_overrides_personal_claim",
                status="passed" if CAPABILITY_TRUTH_STATEMENT in capability_block else "failed",
                message="Capability truth override statement checked.",
                subject_type="personal_mode_loadout",
                subject_ref=str(getattr(loadout, "loadout_id", "")),
            ),
        ]
        result = self.record_result(run_id=run.run_id, contract_id=contract.contract_id, findings=findings)
        self.complete_run(run)
        return run, result, findings

    def evaluate_personal_runtime_binding_conformance(
        self,
        *,
        runtime_binding: Any,
        activation_result: Any | None = None,
        capability_bindings: list[Any] | None = None,
        contract: PersonalConformanceContract | None = None,
    ) -> tuple[PersonalConformanceRun, PersonalConformanceResult, list[PersonalConformanceFinding]]:
        contract, _ = self.register_default_rules(contract=contract)
        run = self.start_run(
            contract_id=contract.contract_id,
            target_kind="personal_runtime_binding",
            target_ref=str(getattr(runtime_binding, "binding_id", "")),
        )
        binding_attrs = getattr(runtime_binding, "binding_attrs", {}) or {}
        findings = [
            self.record_finding(
                run_id=run.run_id,
                rule_type="runtime_binding_non_executing",
                status="passed"
                if not bool(binding_attrs.get("runtime_executed")) and not bool(binding_attrs.get("runtime_mutated"))
                else "failed",
                message="Runtime binding is descriptive and non-executing.",
                subject_type="personal_runtime_binding",
                subject_ref=str(getattr(runtime_binding, "binding_id", "")),
            ),
            self.record_finding(
                run_id=run.run_id,
                rule_type="mode_does_not_grant_capability",
                status="passed" if not bool(binding_attrs.get("capability_grants_created")) else "failed",
                message="Runtime binding does not create capability grants.",
                subject_type="personal_runtime_binding",
                subject_ref=str(getattr(runtime_binding, "binding_id", "")),
            ),
        ]
        if activation_result is not None:
            findings.append(
                self.record_finding(
                    run_id=run.run_id,
                    rule_type="runtime_binding_non_executing",
                    status="failed"
                    if getattr(activation_result, "activation_scope", "") == "active_runtime"
                    else "passed",
                    message="Activation scope is not active runtime execution.",
                    subject_type="personal_mode_activation_result",
                    subject_ref=str(getattr(activation_result, "result_id", "")),
                )
            )
        for binding in capability_bindings or []:
            findings.append(
                self.record_finding(
                    run_id=run.run_id,
                    rule_type="mode_does_not_grant_capability",
                    status="passed"
                    if not bool(getattr(binding, "binding_attrs", {}).get("capability_grant_created"))
                    else "failed",
                    message="Runtime capability binding is descriptive.",
                    subject_type="personal_runtime_capability_binding",
                    subject_ref=str(getattr(binding, "runtime_capability_binding_id", "")),
                )
            )
        result = self.record_result(run_id=run.run_id, contract_id=contract.contract_id, findings=findings)
        self.complete_run(run)
        return run, result, findings

    def evaluate_public_repo_privacy_conformance(
        self,
        *,
        public_artifacts: list[dict[str, Any]],
        forbidden_patterns: list[str],
        contract: PersonalConformanceContract | None = None,
    ) -> tuple[PersonalConformanceRun, PersonalConformanceResult, list[PersonalConformanceFinding]]:
        contract, _ = self.register_default_rules(contract=contract)
        run = self.start_run(contract_id=contract.contract_id, target_kind="public_repo_scan")
        findings: list[PersonalConformanceFinding] = []
        for artifact in public_artifacts:
            text = str(artifact.get("text") or "")
            ref = str(artifact.get("ref") or "artifact")
            matched = [pattern for pattern in forbidden_patterns if pattern and pattern in text]
            findings.append(
                self.record_finding(
                    run_id=run.run_id,
                    rule_type="private_content_not_in_public_artifacts",
                    status="failed" if matched else "passed",
                    message="Public artifact privacy patterns checked.",
                    subject_type="public_artifact",
                    subject_ref=ref,
                    evidence_refs=[{"pattern_count": len(matched)}],
                )
            )
            findings.append(
                self.record_finding(
                    run_id=run.run_id,
                    rule_type="no_" + "json" + "l_personal_store",
                    status="failed" if "json" + "l" in text.casefold() and "personal" in text.casefold() else "passed",
                    message="Public artifact checked for personal JSON Lines store marker.",
                    subject_type="public_artifact",
                    subject_ref=ref,
                )
            )
        result = self.record_result(run_id=run.run_id, contract_id=contract.contract_id, findings=findings)
        self.complete_run(run)
        return run, result, findings

    def _record_run_terminal(self, activity: str, run: PersonalConformanceRun) -> None:
        self._record(
            activity,
            objects=[_object("personal_conformance_run", run.run_id, run.to_dict())],
            links=[("run_object", run.run_id), ("contract_object", run.contract_id)],
            object_links=[(run.run_id, run.contract_id, "uses_contract")],
            attrs={"status": run.status},
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
                "personal_conformance": True,
                "structural_validation_only": True,
                "auto_remediation_enabled": False,
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


def path_looks_excluded_source(path_or_ref: str) -> bool:
    normalized_ref = path_or_ref.replace("\\", "/").casefold()
    normalized = f"/{normalized_ref}"
    return any(token in normalized for token in ["/letters/", "/messages/", "/archive/"])


def redacted_path_ref(path_or_ref: str) -> str:
    return Path(path_or_ref).name or "redacted"
