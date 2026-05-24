from __future__ import annotations

from chanta_core.internal_dominion import (
    DominionMigrationAuditService,
    DominionMigrationRemediationService,
)


def test_migration_audit_detects_legacy_self_execution_language() -> None:
    service = DominionMigrationAuditService()
    text = "v0.23.0 OCEL-native Self-Execution Safety Contract uses self_execution_request_create."

    findings = service.detect_self_execution_legacy(text=text, file_ref="sample.md")

    assert {item.finding_type for item in findings} == {"self_execution_legacy"}
    assert any(item.matched_text == "Self-Execution Safety" for item in findings)
    assert any(item.matched_text == "self_execution_request_create" for item in findings)
    assert all("v0.24.x Local Runtime Provider" in item.recommended_change for item in findings)


def test_migration_audit_detects_growthkernel_active_dependency_wording() -> None:
    service = DominionMigrationAuditService()
    text = "This release requires GrowthKernel and has a GrowthKernel runtime dependency."

    findings = service.detect_growthkernel_active_dependency(text=text, file_ref="sample.md")

    assert findings
    assert all(item.finding_type == "growthkernel_active_dependency" for item in findings)
    assert all("future consumer" in item.recommended_change for item in findings)


def test_migration_audit_detects_vendor_hardcoding_and_allows_future_examples() -> None:
    service = DominionMigrationAuditService()

    active = service.detect_vendor_hardcoding(text="A360 runtime logic is core Dominion.", file_ref="core.py")
    future = service.detect_vendor_hardcoding(
        text="A360 and UiPath are future external provider adapter examples.",
        file_ref="docs.md",
    )

    assert active[0].finding_type == "vendor_hardcoding"
    assert active[0].fixed is False
    assert active[0].severity == "high"
    assert all(item.fixed is True for item in future)


def test_migration_audit_detects_provider_bypass_risk() -> None:
    service = DominionMigrationAuditService()
    text = "A provider direct run would be a dispatch without gate and control without authorization."

    findings = service.detect_provider_gate_bypass_risk(text=text, file_ref="sample.md")

    assert {item.finding_type for item in findings} == {"provider_gate_bypass_risk"}
    assert any(item.severity == "critical" for item in findings)


def test_migration_remediation_marks_findings_fixed_without_runtime_side_effects() -> None:
    audit = DominionMigrationAuditService()
    remediation = DominionMigrationRemediationService()
    findings = audit.detect_self_execution_legacy(
        text="Self-Execution Safety self_execution_bounded_run",
        file_ref="sample.md",
    )

    remediated = remediation.apply_safe_renames_and_deprecations(findings)

    assert remediated
    assert all(item.fixed is True for item in remediated)
    assert all("v0.24.x Local Runtime Provider" in item.recommended_change for item in remediated)
