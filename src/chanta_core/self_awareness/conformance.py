from __future__ import annotations

from chanta_core.self_awareness.models import SelfAwarenessConformanceReport, SelfAwarenessSkillContract
from chanta_core.self_awareness.registry import SelfAwarenessRegistryService


class SelfAwarenessConformanceService:
    def __init__(self, registry_service: SelfAwarenessRegistryService | None = None) -> None:
        self.registry_service = registry_service or SelfAwarenessRegistryService()
        self.last_report: SelfAwarenessConformanceReport | None = None

    def run_conformance(self) -> SelfAwarenessConformanceReport:
        contracts = self.registry_service.list_contracts()
        findings: list[str] = []
        failed: list[str] = []
        for contract in contracts:
            contract_findings = _contract_findings(contract)
            if contract_findings:
                failed.append(contract.skill_id)
                findings.extend(f"{contract.skill_id}: {item}" for item in contract_findings)
        report = SelfAwarenessConformanceReport(
            report_id="self_awareness_conformance_report:v0.20.9",
            passed=not failed,
            total_contract_count=len(contracts),
            checked_contract_count=len(contracts),
            dangerous_capability_count=sum(1 for item in contracts if item.risk_profile.dangerous_capability),
            workspace_mutation_count=sum(1 for item in contracts if item.risk_profile.mutates_workspace),
            memory_mutation_count=sum(1 for item in contracts if item.risk_profile.mutates_memory),
            persona_mutation_count=sum(1 for item in contracts if item.risk_profile.mutates_persona),
            overlay_mutation_count=sum(1 for item in contracts if item.risk_profile.mutates_overlay),
            shell_usage_count=sum(1 for item in contracts if item.risk_profile.uses_shell),
            network_usage_count=sum(1 for item in contracts if item.risk_profile.uses_network),
            mcp_usage_count=sum(1 for item in contracts if item.risk_profile.uses_mcp),
            plugin_loading_count=sum(1 for item in contracts if item.risk_profile.loads_plugin),
            external_harness_execution_count=sum(1 for item in contracts if item.risk_profile.executes_external_harness),
            execution_enabled_count=sum(1 for item in contracts if item.execution_enabled),
            canonical_mutation_enabled_count=sum(1 for item in contracts if item.canonical_mutation_enabled),
            failed_contract_ids=failed,
            findings=findings,
            report_attrs={
                "layer": "self_awareness",
                "state": "self_awareness_foundation_v1_consolidated",
                "skills_executed": False,
                "canonical_store": "ocel",
            },
        )
        self.last_report = report
        return report

    def assert_no_dangerous_capabilities(self) -> None:
        report = self.run_conformance()
        if not report.passed:
            raise AssertionError("; ".join(report.findings))

    def render_conformance_cli(self, report: SelfAwarenessConformanceReport | None = None) -> str:
        item = report or self.last_report or self.run_conformance()
        lines = [
            "Self-Awareness Conformance",
            "layer=self_awareness",
            f"state={item.report_attrs.get('state', 'self_awareness_foundation_v1_consolidated')}",
            f"status={item.status}",
            f"contract_count={item.total_contract_count}",
            f"dangerous_capability_count={item.dangerous_capability_count}",
            f"execution_enabled_count={item.execution_enabled_count}",
            f"canonical_mutation_enabled_count={item.canonical_mutation_enabled_count}",
            f"write_mutation_count={item.workspace_mutation_count}",
            f"shell_usage_count={item.shell_usage_count}",
            f"network_usage_count={item.network_usage_count}",
            f"mcp_usage_count={item.mcp_usage_count}",
            f"plugin_loading_count={item.plugin_loading_count}",
            f"external_harness_execution_count={item.external_harness_execution_count}",
            f"memory_mutation_count={item.memory_mutation_count}",
            f"persona_mutation_count={item.persona_mutation_count}",
            f"overlay_mutation_count={item.overlay_mutation_count}",
        ]
        return "\n".join(lines)


def _contract_findings(contract: SelfAwarenessSkillContract) -> list[str]:
    findings: list[str] = []
    risk = contract.risk_profile
    if contract.layer != "self_awareness":
        findings.append("layer must be self_awareness")
    if contract.execution_enabled:
        findings.append("execution_enabled must remain false")
    if contract.canonical_mutation_enabled:
        findings.append("canonical_mutation_enabled must remain false")
    if not risk.read_only:
        findings.append("risk_profile.read_only must remain true")
    denied = {
        "mutates_workspace": risk.mutates_workspace,
        "mutates_memory": risk.mutates_memory,
        "mutates_persona": risk.mutates_persona,
        "mutates_overlay": risk.mutates_overlay,
        "uses_shell": risk.uses_shell,
        "uses_network": risk.uses_network,
        "uses_mcp": risk.uses_mcp,
        "loads_plugin": risk.loads_plugin,
        "executes_external_harness": risk.executes_external_harness,
        "dangerous_capability": risk.dangerous_capability,
    }
    findings.extend(f"{name} must remain false" for name, value in denied.items() if value)
    if not contract.gate_contract.evidence_refs_required:
        findings.append("evidence_refs_required must remain true")
    if not contract.gate_contract.execution_envelope_required:
        findings.append("execution_envelope_required must remain true")
    read_only_gate_execution = (
        contract.implementation_status == "implemented"
        and contract.effect_type == "read_only_observation"
        and contract.gate_contract.gate_attrs.get("execution_route") == "explicit_read_only_gate"
    )
    if contract.gate_contract.allow_skill_execution and not read_only_gate_execution:
        findings.append("gate contract must not allow skill execution")
    if contract.gate_contract.allow_canonical_mutation:
        findings.append("gate contract must not allow canonical mutation")
    return findings
