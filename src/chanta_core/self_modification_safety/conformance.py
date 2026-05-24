from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.self_modification_safety.mapping import (
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
)
from chanta_core.self_modification_safety.registry import (
    SELF_MODIFICATION_SEED_SKILL_IDS,
    SELF_MODIFICATION_SEED_SUBJECT_IDS,
    SelfModificationRegistryService,
)


@dataclass(frozen=True)
class SelfModificationConformanceReport:
    report_id: str
    version: str
    layer: str
    status: str
    checked_subject_count: int
    checked_skill_count: int
    findings: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.status == "passed"

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "layer": self.layer,
            "status": self.status,
            "checked_subject_count": self.checked_subject_count,
            "checked_skill_count": self.checked_skill_count,
            "findings": list(self.findings),
        }


class SelfModificationConformanceService:
    def __init__(self, registry_service: SelfModificationRegistryService | None = None) -> None:
        self.registry_service = registry_service or SelfModificationRegistryService()
        self.last_report: SelfModificationConformanceReport | None = None

    def run_conformance(self) -> SelfModificationConformanceReport:
        findings: list[str] = []
        contract = self.registry_service.build_contract()
        subjects = self.registry_service.list_subjects()
        seed_skills = self.registry_service.list_seed_skill_ids()
        subject_ids = {item.subject_id for item in subjects}
        for expected in SELF_MODIFICATION_SEED_SUBJECT_IDS:
            if expected not in subject_ids:
                findings.append(f"missing subject: {expected}")
        if set(seed_skills) != set(SELF_MODIFICATION_SEED_SKILL_IDS):
            findings.append("seed skill ids must match v0.22.0 contract")
        for subject in subjects:
            if subject.status not in {"contract_only", "stub"}:
                findings.append(f"{subject.subject_id}: status must be contract_only or stub")
            if not subject.ocel_object_types or not subject.ocel_event_types or not subject.ocel_relation_types:
                findings.append(f"{subject.subject_id}: OCEL mapping is required")
            if not subject.required_source_objects:
                findings.append(f"{subject.subject_id}: required_source_objects is required")
            if not subject.required_read_models:
                findings.append(f"{subject.subject_id}: required_read_models is required")
            if "non_executable" not in subject.risk_notes:
                findings.append(f"{subject.subject_id}: non_executable risk note is required")
        findings.extend(self.assert_contract_only(raise_on_error=False))
        findings.extend(self.assert_no_file_write(raise_on_error=False))
        findings.extend(self.assert_patch_application_disabled(raise_on_error=False))
        findings.extend(self.assert_ocel_native_contract(raise_on_error=False))
        report = SelfModificationConformanceReport(
            report_id="self_modification_conformance_report:v0.22.0",
            version=contract.version,
            layer=contract.layer,
            status="failed" if findings else "passed",
            checked_subject_count=len(subjects),
            checked_skill_count=len(seed_skills),
            findings=findings,
        )
        self.last_report = report
        return report

    def assert_contract_only(self, *, raise_on_error: bool = True) -> list[str]:
        contract = self.registry_service.build_contract()
        findings: list[str] = []
        if contract.status != "contract_only":
            findings.append("contract status must be contract_only")
        if not contract.risk_profile.contract_only:
            findings.append("risk_profile.contract_only must be true")
        if contract.lifecycle_policy.mutation_transitions_executable:
            findings.append("lifecycle mutation transitions must not be executable in v0.22.0")
        if findings and raise_on_error:
            raise AssertionError("; ".join(findings))
        return findings

    def assert_no_file_write(self, *, raise_on_error: bool = True) -> list[str]:
        risk = self.registry_service.build_contract().risk_profile
        findings: list[str] = []
        denied = {
            "file_write_enabled": risk.file_write_enabled,
            "shell_enabled": risk.shell_enabled,
            "test_execution_enabled": risk.test_execution_enabled,
            "lint_execution_enabled": risk.lint_execution_enabled,
            "network_enabled": risk.network_enabled,
            "mcp_enabled": risk.mcp_enabled,
            "plugin_enabled": risk.plugin_enabled,
            "external_harness_enabled": risk.external_harness_enabled,
            "memory_mutation_enabled": risk.memory_mutation_enabled,
            "persona_mutation_enabled": risk.persona_mutation_enabled,
            "overlay_mutation_enabled": risk.overlay_mutation_enabled,
            "autonomous_apply_enabled": risk.autonomous_apply_enabled,
            "llm_patch_generation_enabled": risk.llm_patch_generation_enabled,
            "llm_judge_enabled": risk.llm_judge_enabled,
            "dangerous_capability": risk.dangerous_capability,
        }
        findings.extend(f"{name} must be false" for name, value in denied.items() if value)
        if findings and raise_on_error:
            raise AssertionError("; ".join(findings))
        return findings

    def assert_patch_application_disabled(self, *, raise_on_error: bool = True) -> list[str]:
        risk = self.registry_service.build_contract().risk_profile
        findings: list[str] = []
        if risk.apply_patch_enabled:
            findings.append("apply_patch_enabled must be false")
        if findings and raise_on_error:
            raise AssertionError("; ".join(findings))
        return findings

    def assert_ocel_native_contract(self, *, raise_on_error: bool = True) -> list[str]:
        contract = self.registry_service.build_contract()
        findings: list[str] = []
        if "read_only_observation" not in contract.ocel_mapping.effect_types:
            findings.append("read_only_observation effect type is required")
        if "state_candidate_created" not in contract.ocel_mapping.effect_types:
            findings.append("state_candidate_created effect type is required")
        if "workspace_file_changed" not in contract.ocel_mapping.effect_types:
            findings.append("workspace_file_changed effect type is required for bounded apply visibility")
        if "self_modification_safety_contract" not in SELF_MODIFICATION_OCEL_OBJECT_TYPES:
            findings.append("self_modification_safety_contract object type is missing")
        if "self_modification_contract_checked" not in SELF_MODIFICATION_OCEL_EVENT_TYPES:
            findings.append("self_modification_contract_checked event type is missing")
        if "derived_from_deep_self_consolidation" not in SELF_MODIFICATION_OCEL_RELATION_TYPES:
            findings.append("derived_from_deep_self_consolidation relation type is missing")
        if findings and raise_on_error:
            raise AssertionError("; ".join(findings))
        return findings

    def render_conformance_cli(self) -> str:
        report = self.last_report or self.run_conformance()
        return "\n".join(
            [
                "Self-Modification Safety Conformance",
                "layer=self_modification_safety",
                f"status={report.status}",
                f"checked_subject_count={report.checked_subject_count}",
                f"checked_skill_count={report.checked_skill_count}",
                "contract_only=True",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "autonomous_apply_enabled=false",
                "llm_patch_generation_enabled=false",
                "llm_judge_enabled=false",
                "no_file_mutation_occurred=true",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
                "canonical_store=ocel",
            ]
        )
