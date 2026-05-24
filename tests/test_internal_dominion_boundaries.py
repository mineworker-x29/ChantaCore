from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    InternalDominionReportService,
)


def test_internal_dominion_ocel_mapping_entries_exist() -> None:
    for object_type in [
        "internal_dominion_layer",
        "internal_dominion_contract",
        "internal_skill_taxonomy",
        "dominion_subject",
        "dominion_skill_contract",
        "dominion_provider_interface_contract",
        "dominion_risk_profile",
        "dominion_gate_contract",
        "dominion_observability_contract",
        "dominion_effect_policy",
        "dominion_migration_policy",
        "internal_dominion_contract_report",
        "dominion_migration_finding",
        "dominion_conformance_finding",
        "external_runtime_subject",
        "external_agent_subject",
        "external_tool_subject",
        "external_control_surface_subject",
        "external_capability_subject",
        "control_request_subject",
        "external_action_candidate_subject",
        "control_plan_subject",
        "dominion_gate_subject",
        "dominion_authorization_subject",
        "bounded_control_dispatch_subject",
        "external_run_tracking_subject",
        "external_outcome_record_subject",
        "self_modification_consolidation_report",
        "deep_self_consolidation_report",
        "self_awareness_consolidation_report",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in DOMINION_OCEL_OBJECT_TYPES
    for event_type in [
        "internal_dominion_layer_registered",
        "internal_dominion_contract_registered",
        "internal_skill_taxonomy_updated",
        "dominion_subject_registered",
        "dominion_provider_interface_registered",
        "dominion_migration_audit_performed",
        "dominion_migration_remediation_performed",
        "dominion_conformance_checked",
        "internal_dominion_contract_report_created",
        "internal_dominion_pig_report_created",
        "internal_dominion_ocpx_projection_created",
    ]:
        assert event_type in DOMINION_OCEL_EVENT_TYPES
    for relation_type in [
        "declares_internal_dominion",
        "extends_internal_skill_taxonomy",
        "declares_dominion_subject",
        "declares_provider_interface",
        "separates_internal_dominion_from_external_provider",
        "reclassifies_self_execution_to_local_provider",
        "marks_growthkernel_as_future_consumer",
        "marks_vendor_adapter_as_future_external_skill",
        "requires_dominion_gate",
        "requires_single_use_authorization",
        "requires_external_outcome_record",
        "requires_ocel_visibility",
        "prevents_provider_gate_bypass",
        "prevents_credential_exposure",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_self_modification_consolidation",
        "derived_from_deep_self_consolidation",
        "derived_from_self_awareness_consolidation",
    ]:
        assert relation_type in DOMINION_OCEL_RELATION_TYPES


def test_internal_dominion_uses_only_contract_effects() -> None:
    projection = InternalDominionReportService().build_ocpx_projection()

    assert {"read_only_observation", "state_candidate_created"} <= set(DOMINION_EFFECT_TYPES)
    assert {"read_only_observation", "state_candidate_created"} <= set(projection["effect_types"])


def test_internal_dominion_runtime_has_no_dispatch_provider_or_command_implementation() -> None:
    source_root = Path("src/chanta_core/internal_dominion")
    source = "\n".join(path.read_text(encoding="utf-8") for path in source_root.rglob("*.py"))
    forbidden = [
        "requests.",
        "httpx",
        "urllib",
        "aiohttp",
        "mcp.connect",
        "plugin.load",
        "subprocess",
        "os.system",
        "shell=True",
        "external_runtime_touched=True",
        "provider_api_call_performed=True",
        "dispatch_enabled=True",
        "external_dispatch_enabled=True",
        "credential_exposed=True",
        "network_enabled=True",
        "mcp_enabled=True",
        "plugin_enabled=True",
        "shell_enabled=True",
        "local_command_enabled=True",
        "growthkernel_dependency_required=True",
        "llm_judge_enabled=True",
        "openai",
        "anthropic",
        "chat.completions",
        "exec(",
        "eval(",
    ]

    for token in forbidden:
        assert token not in source


def test_vendor_names_are_not_hardcoded_in_internal_dominion_runtime() -> None:
    source_root = Path("src/chanta_core/internal_dominion")
    runtime_paths = [
        path
        for path in source_root.rglob("*.py")
        if path.name not in {"migration.py"}
    ]
    source = "\n".join(path.read_text(encoding="utf-8") for path in runtime_paths)

    for vendor in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert vendor not in source
