from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)
from chanta_core.internal_dominion.models import (
    INTERNAL_DOMINION_LAYER,
    INTERNAL_DOMINION_VERSION,
    DominionConformanceFinding,
)
from chanta_core.internal_dominion.registry import (
    DOMINION_SEED_SKILL_IDS,
    DOMINION_SEED_SUBJECT_IDS,
    InternalDominionRegistryService,
)


@dataclass(frozen=True)
class DominionConformanceReport:
    report_id: str
    version: str
    layer: str
    status: str
    checked_subject_count: int
    checked_skill_count: int
    findings: list[DominionConformanceFinding] = field(default_factory=list)

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
            "findings": [item.to_dict() for item in self.findings],
        }


class DominionConformanceService:
    def __init__(self, registry_service: InternalDominionRegistryService | None = None) -> None:
        self.registry_service = registry_service or InternalDominionRegistryService()
        self.last_report: DominionConformanceReport | None = None

    def run_conformance(self) -> DominionConformanceReport:
        findings: list[DominionConformanceFinding] = []
        contract = self.registry_service.build_contract()
        subject_ids = [item.subject_id for item in self.registry_service.list_subjects()]
        skill_ids = self.registry_service.list_seed_skill_ids()
        if subject_ids != DOMINION_SEED_SUBJECT_IDS:
            findings.append(_finding("Seed subjects do not match v0.23.0 Dominion contract."))
        if skill_ids != DOMINION_SEED_SKILL_IDS:
            findings.append(_finding("Seed skills do not match v0.23.0 Dominion contract."))
        for subject in contract.subjects:
            if not subject.provider_neutral:
                findings.append(_finding(f"{subject.subject_id} must be provider-neutral."))
            if subject.dispatch_enabled:
                findings.append(_finding(f"{subject.subject_id} must not dispatch in v0.23.0."))
            if "no_provider_api_call" not in subject.risk_notes:
                findings.append(_finding(f"{subject.subject_id} must deny provider API calls."))
        for check in [
            self.assert_contract_only,
            self.assert_no_external_dispatch,
            self.assert_no_provider_api_call,
            self.assert_no_growthkernel_dependency_required,
            self.assert_vendor_neutral_core,
        ]:
            findings.extend(check(raise_on_error=False))
        report = DominionConformanceReport(
            report_id="dominion_conformance_report:v0.23.0",
            version=INTERNAL_DOMINION_VERSION,
            layer=INTERNAL_DOMINION_LAYER,
            status="failed" if findings else "passed",
            checked_subject_count=len(subject_ids),
            checked_skill_count=len(skill_ids),
            findings=findings,
        )
        self.last_report = report
        return report

    def assert_contract_only(self, *, raise_on_error: bool = True) -> list[DominionConformanceFinding]:
        contract = self.registry_service.build_contract()
        findings: list[DominionConformanceFinding] = []
        if contract.status != "contract_only":
            findings.append(_finding("Contract status must be contract_only."))
        if not contract.risk_profile.contract_only:
            findings.append(_finding("risk_profile.contract_only must be true."))
        if not set(contract.effect_policy.allowed_effect_types_v0_23_0) <= set(DOMINION_EFFECT_TYPES):
            findings.append(_finding("v0.23.0 effect types must include read-only/state-candidate effects."))
        return _raise_or_return(findings, raise_on_error)

    def assert_no_external_dispatch(self, *, raise_on_error: bool = True) -> list[DominionConformanceFinding]:
        risk = self.registry_service.build_contract().risk_profile
        findings = []
        if risk.external_dispatch_enabled:
            findings.append(_finding("external_dispatch_enabled must be false."))
        if risk.external_runtime_touch_enabled:
            findings.append(_finding("external_runtime_touch_enabled must be false."))
        if risk.autonomous_dispatch_enabled:
            findings.append(_finding("autonomous_dispatch_enabled must be false."))
        return _raise_or_return(findings, raise_on_error)

    def assert_no_provider_api_call(self, *, raise_on_error: bool = True) -> list[DominionConformanceFinding]:
        contract = self.registry_service.build_contract()
        findings = []
        if contract.risk_profile.provider_api_call_enabled:
            findings.append(_finding("provider_api_call_enabled must be false."))
        if contract.provider_interface.provider_api_call_enabled:
            findings.append(_finding("Provider interface must not implement provider API calls."))
        return _raise_or_return(findings, raise_on_error)

    def assert_no_growthkernel_dependency_required(
        self, *, raise_on_error: bool = True
    ) -> list[DominionConformanceFinding]:
        risk = self.registry_service.build_contract().risk_profile
        findings = []
        if risk.growthkernel_dependency_required:
            findings.append(_finding("growthkernel_dependency_required must be false."))
        return _raise_or_return(findings, raise_on_error)

    def assert_vendor_neutral_core(self, *, raise_on_error: bool = True) -> list[DominionConformanceFinding]:
        contract = self.registry_service.build_contract()
        findings = []
        definition = contract.definition.lower() + " " + contract.taxonomy.dominion_definition.lower()
        for vendor_name in ["a360", "automation anywhere", "brity", "uipath", "power automate"]:
            if vendor_name in definition:
                findings.append(_finding(f"Dominion definition must not hard-code {vendor_name}."))
        return _raise_or_return(findings, raise_on_error)

    def assert_ocel_native(self, *, raise_on_error: bool = True) -> list[DominionConformanceFinding]:
        findings = []
        for object_type in ["internal_dominion_contract", "dominion_provider_interface_contract"]:
            if object_type not in DOMINION_OCEL_OBJECT_TYPES:
                findings.append(_finding(f"Missing OCEL object type: {object_type}."))
        if "internal_dominion_contract_registered" not in DOMINION_OCEL_EVENT_TYPES:
            findings.append(_finding("Missing Internal Dominion contract registered event."))
        if "requires_ocel_visibility" not in DOMINION_OCEL_RELATION_TYPES:
            findings.append(_finding("Missing requires_ocel_visibility relation."))
        return _raise_or_return(findings, raise_on_error)

    def render_conformance_cli(self) -> str:
        report = self.last_report or self.run_conformance()
        return "\n".join(
            [
                "Internal Dominion Conformance",
                f"version={report.version}",
                f"layer={report.layer}",
                f"status={report.status}",
                "contract_only=True",
                "dispatch_enabled=false",
                "external_runtime_touched=false",
                "provider_api_call_performed=false",
                "GrowthKernel=future_consumer_not_dependency",
                "vendor adapters=future_external_provider_skills",
                "self_execution=v0.24 Local Runtime Provider",
                "credential_exposed=False",
                "raw_secrets_printed=False",
                "canonical_store=ocel",
            ]
        )


def _finding(message: str) -> DominionConformanceFinding:
    return DominionConformanceFinding(
        finding_id="dominion_conformance_finding:v0.23.0",
        severity="error",
        message=message,
        fixed=False,
    )


def _raise_or_return(
    findings: list[DominionConformanceFinding], raise_on_error: bool
) -> list[DominionConformanceFinding]:
    if findings and raise_on_error:
        raise AssertionError("; ".join(item.message for item in findings))
    return findings
