from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.deep_self_introspection.mapping import (
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
)
from chanta_core.deep_self_introspection.registry import (
    DEEP_SELF_INTROSPECTION_SEED_SKILL_IDS,
    DEEP_SELF_INTROSPECTION_SEED_SUBJECT_IDS,
    DeepSelfIntrospectionRegistryService,
)


@dataclass(frozen=True)
class DeepSelfIntrospectionConformanceReport:
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


class DeepSelfIntrospectionConformanceService:
    def __init__(self, registry_service: DeepSelfIntrospectionRegistryService | None = None) -> None:
        self.registry_service = registry_service or DeepSelfIntrospectionRegistryService()
        self.last_report: DeepSelfIntrospectionConformanceReport | None = None

    def run_conformance(self) -> DeepSelfIntrospectionConformanceReport:
        findings: list[str] = []
        contract = self.registry_service.build_contract()
        subjects = self.registry_service.list_subjects()
        seed_skills = self.registry_service.list_seed_skill_ids()
        subject_ids = {item.subject_id for item in subjects}
        for expected in DEEP_SELF_INTROSPECTION_SEED_SUBJECT_IDS:
            if expected not in subject_ids:
                findings.append(f"missing subject: {expected}")
        if set(seed_skills) != set(DEEP_SELF_INTROSPECTION_SEED_SKILL_IDS):
            findings.append("seed skill ids must match v0.21.0 contract")
        for subject in subjects:
            if subject.status not in {"contract_only", "stub"}:
                findings.append(f"{subject.subject_id}: status must be contract_only or stub")
            if not subject.ocel_object_types or not subject.ocel_event_types or not subject.ocel_relation_types:
                findings.append(f"{subject.subject_id}: OCEL mapping is required")
            if not subject.required_source_objects:
                findings.append(f"{subject.subject_id}: required_source_objects is required")
            if not subject.required_read_models:
                findings.append(f"{subject.subject_id}: required_read_models is required")
        findings.extend(self.assert_read_only_contract(raise_on_error=False))
        findings.extend(self.assert_ocel_native_contract(raise_on_error=False))
        report = DeepSelfIntrospectionConformanceReport(
            report_id="deep_self_introspection_conformance_report:v0.21.0",
            version="v0.21.0",
            layer=contract.layer,
            status="failed" if findings else "passed",
            checked_subject_count=len(subjects),
            checked_skill_count=len(seed_skills),
            findings=findings,
        )
        self.last_report = report
        return report

    def assert_read_only_contract(self, *, raise_on_error: bool = True) -> list[str]:
        contract = self.registry_service.build_contract()
        risk = contract.risk_profile
        gate = contract.gate_contract
        findings: list[str] = []
        denied = {
            "mutates_workspace": risk.mutates_workspace,
            "mutates_memory": risk.mutates_memory,
            "mutates_persona": risk.mutates_persona,
            "mutates_overlay": risk.mutates_overlay,
            "mutates_capability_registry": risk.mutates_capability_registry,
            "mutates_policy": risk.mutates_policy,
            "grants_permission": risk.grants_permission,
            "creates_task": risk.creates_task,
            "materializes_candidate": risk.materializes_candidate,
            "promotes_candidate": risk.promotes_candidate,
            "uses_shell": risk.uses_shell,
            "uses_network": risk.uses_network,
            "uses_mcp": risk.uses_mcp,
            "loads_plugin": risk.loads_plugin,
            "executes_external_harness": risk.executes_external_harness,
            "uses_llm_judge": risk.uses_llm_judge,
            "dangerous_capability": risk.dangerous_capability,
        }
        if not risk.read_only:
            findings.append("risk_profile.read_only must be true")
        findings.extend(f"{name} must be false" for name, value in denied.items() if value)
        if not gate.requires_read_only_gate:
            findings.append("read-only gate is required")
        if not gate.deny_if_mutation_requested:
            findings.append("mutation demand must be denied")
        if not gate.deny_if_permission_escalation_requested:
            findings.append("permission escalation demand must be denied")
        if findings and raise_on_error:
            raise AssertionError("; ".join(findings))
        return findings

    def assert_ocel_native_contract(self, *, raise_on_error: bool = True) -> list[str]:
        contract = self.registry_service.build_contract()
        findings: list[str] = []
        if not contract.risk_profile.ocel_read_only:
            findings.append("ocel_read_only must be true")
        if not contract.risk_profile.uses_existing_self_awareness_graph:
            findings.append("existing self-awareness graph must be used")
        if "read_only_observation" not in contract.ocel_mapping.effect_types:
            findings.append("read_only_observation effect type is required")
        if "state_candidate_created" not in contract.ocel_mapping.effect_types:
            findings.append("state_candidate_created effect type is required")
        required_sets = [
            contract.ocel_mapping.object_types,
            contract.ocel_mapping.event_types,
            contract.ocel_mapping.relation_types,
        ]
        if not all(required_sets):
            findings.append("object/event/relation mapping must be nonempty")
        if "deep_self_introspection_contract" not in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES:
            findings.append("deep_self_introspection_contract object type is missing")
        if "deep_self_introspection_contract_checked" not in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES:
            findings.append("deep_self_introspection_contract_checked event type is missing")
        if "derived_from_self_awareness_consolidation" not in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES:
            findings.append("derived_from_self_awareness_consolidation relation type is missing")
        if findings and raise_on_error:
            raise AssertionError("; ".join(findings))
        return findings

    def render_conformance_cli(self) -> str:
        report = self.last_report or self.run_conformance()
        return "\n".join(
            [
                "Deep Self-Introspection Conformance",
                "layer=deep_self_introspection",
                f"status={report.status}",
                f"checked_subject_count={report.checked_subject_count}",
                f"checked_skill_count={report.checked_skill_count}",
                "read_only=True",
                "ocel_native=True",
                "mutation_enabled=False",
                "execution_enabled=False",
                "permission_escalation_enabled=False",
                "llm_judge_enabled=False",
                "canonical_store=ocel",
            ]
        )
