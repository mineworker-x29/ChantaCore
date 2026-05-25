from __future__ import annotations

import subprocess
import sys

from chanta_core.internal_dominion import (
    DOMINION_SEED_SKILL_IDS,
    DOMINION_SEED_SUBJECT_IDS,
    INTERNAL_DOMINION_LAYER,
    INTERNAL_DOMINION_TRACK,
    INTERNAL_DOMINION_VERSION,
    INTERNAL_DOMINION_VERSION_NAME,
    DominionConformanceService,
    InternalDominionRegistryService,
    InternalDominionReportService,
)


def test_v0_23_0_internal_dominion_doc_records_policy_change() -> None:
    text = open("docs/versions/v0.23/v0.23.0_internal_dominion_contract.md", encoding="utf-8").read()

    assert "OCEL-native Internal Dominion Contract" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "v0.23.x is no longer Self-Execution Safety" in text
    assert "Self-Execution Safety is reclassified to v0.24.x Local Runtime Provider" in text
    assert "No provider API call, external runtime touch, dispatch, local command" in text
    assert "Schumpeter split" in text
    assert "GrowthKernel is a future consumer / future optimizer" in text


def test_internal_dominion_contract_builds() -> None:
    contract = InternalDominionRegistryService().build_contract()

    assert contract.version == INTERNAL_DOMINION_VERSION
    assert contract.version_name == INTERNAL_DOMINION_VERSION_NAME
    assert contract.track == INTERNAL_DOMINION_TRACK
    assert contract.layer == INTERNAL_DOMINION_LAYER
    assert contract.status == "contract_only"
    assert "Self-Execution Safety" not in contract.track


def test_internal_skill_taxonomy_includes_observation_digestion_dominion() -> None:
    taxonomy = InternalDominionRegistryService().build_contract().taxonomy

    assert taxonomy.categories == ["observation", "digestion", "dominion"]
    assert "vendor-neutral" in taxonomy.dominion_definition.lower()
    assert "gated control grammar" in taxonomy.dominion_definition
    assert taxonomy.dominion_is_vendor_adapter is False
    assert taxonomy.dominion_is_self_execution is False
    assert taxonomy.dominion_dispatch_enabled_by_default is False


def test_seed_subjects_are_registered_provider_neutral_and_non_dispatching() -> None:
    registry = InternalDominionRegistryService()
    subjects = registry.list_subjects()

    assert [item.subject_id for item in subjects] == DOMINION_SEED_SUBJECT_IDS
    for subject in subjects:
        assert subject.provider_neutral is True
        assert subject.dispatch_enabled is False
        if subject.subject_id in {"subject:control_plan", "subject:target_binding"}:
            assert subject.status == "plan_only"
        elif subject.subject_id == "subject:dominion_static_safety":
            assert subject.status == "static_rule_only"
        elif subject.subject_id == "subject:runtime_preflight":
            assert subject.status == "foundation_preflight_only"
        elif subject.subject_id == "subject:dominion_review_gate":
            assert subject.status == "review_gate_only"
        elif subject.subject_id == "subject:dominion_authorization":
            assert subject.status == "gate_authorization_only"
        elif subject.subject_id in {"subject:dominion_workbench", "subject:dominion_consolidation"}:
            assert subject.status == "consolidation_only"
        else:
            assert subject.status in {"contract_only", "future_stub", "boundary_only"}
        assert "no_provider_api_call" in subject.risk_notes
        assert "no_external_runtime_touch" in subject.risk_notes


def test_seed_skills_are_registered_as_read_only_or_contract_stubs() -> None:
    registry = InternalDominionRegistryService()

    assert registry.list_seed_skill_ids() == DOMINION_SEED_SKILL_IDS
    contracts = registry.list_skill_contracts()
    assert {item["skill_id"] for item in contracts} == set(DOMINION_SEED_SKILL_IDS)
    for item in contracts:
        if item["skill_id"] in {
            "skill:dominion_contract_view",
            "skill:dominion_runtime_inventory",
            "skill:dominion_capability_observe",
            "skill:dominion_capability_digest",
        }:
            assert item["status"] == "read_only"
            assert item["read_only"] is True
        elif item["skill_id"] in {"skill:dominion_control_request_create", "skill:dominion_action_candidate_create"}:
            assert item["status"] == "candidate_only"
            assert item["candidate_only"] is True
            assert item["read_only"] is True
        elif item["skill_id"] in {"skill:dominion_control_plan_create", "skill:dominion_target_binding"}:
            assert item["status"] == "plan_only"
            assert item["plan_only"] is True
            assert item["read_only"] is True
        elif item["skill_id"] == "skill:dominion_static_safety_check":
            assert item["status"] == "static_rule_only"
            assert item["static_rule_only"] is True
            assert item["read_only"] is True
        elif item["skill_id"] == "skill:dominion_runtime_preflight":
            assert item["status"] == "foundation_preflight_only"
            assert item["foundation_preflight_only"] is True
            assert item["read_only"] is True
        elif item["skill_id"] == "skill:dominion_review_gate":
            assert item["status"] == "review_gate_only"
            assert item["review_gate_only"] is True
            assert item["read_only"] is True
        elif item["skill_id"] == "skill:dominion_authorization_create":
            assert item["status"] == "gate_authorization_only"
            assert item["gate_authorization_only"] is True
            assert item["read_only"] is True
        elif item["skill_id"] in {
            "skill:dominion_bounded_dispatch",
            "skill:dominion_run_status_track",
            "skill:dominion_run_output_fetch",
            "skill:dominion_outcome_record",
        }:
            assert item["status"] == "boundary_only"
            assert item["boundary_only"] is True
            assert item["read_only"] is True
            assert item["actual_dispatch_enabled"] is False
            assert item["authorization_consumption_enabled"] is False
            assert item["live_status_tracking_enabled"] is False
            assert item["live_output_fetch_enabled"] is False
            assert item["real_external_outcome_record_enabled"] is False
        elif item["skill_id"] in {"skill:dominion_workbench_view", "skill:dominion_consolidation_view"}:
            assert item["status"] == "consolidation_only"
            assert item["consolidation_only"] is True
            assert item["read_only"] is True
            assert item["mutation_performed"] is False
        else:
            assert item["status"] == "contract_only"
            assert item["stub"] is True
        assert item["non_dispatching"] is True
        assert item["external_dispatch_enabled"] is False
        assert item["external_runtime_touch_enabled"] is False
        assert item["provider_api_call_enabled"] is False


def test_risk_provider_gate_and_effect_defaults() -> None:
    contract = InternalDominionRegistryService().build_contract()
    risk = contract.risk_profile
    provider = contract.provider_interface
    gate = contract.gate_contract
    effect = contract.effect_policy

    assert risk.contract_only is True
    assert risk.external_dispatch_enabled is False
    assert risk.external_runtime_touch_enabled is False
    assert risk.provider_api_call_enabled is False
    assert risk.credential_materialization_enabled is False
    assert risk.network_enabled is False
    assert risk.mcp_enabled is False
    assert risk.plugin_enabled is False
    assert risk.shell_enabled is False
    assert risk.local_command_enabled is False
    assert risk.production_action_enabled is False
    assert risk.autonomous_dispatch_enabled is False
    assert risk.memory_mutation_enabled is False
    assert risk.persona_mutation_enabled is False
    assert risk.overlay_mutation_enabled is False
    assert risk.growthkernel_dependency_required is False
    assert risk.llm_judge_enabled is False
    assert risk.dangerous_capability is False

    assert {
        "local_runtime",
        "rpa_runtime",
        "agent_runtime",
        "workflow_engine",
        "browser_automation",
        "enterprise_api",
        "database_or_etl",
        "custom_system",
    } <= set(provider.provider_types)
    assert {
        "discover_runtimes",
        "list_capabilities",
        "describe_capability",
        "validate_action",
        "preflight",
        "dispatch",
        "get_status",
        "fetch_output",
        "cancel_or_stop",
        "map_outcome",
    } <= set(provider.required_methods)
    assert provider.provider_cannot_bypass_gate is True
    assert provider.provider_cannot_store_credentials_in_output is True
    assert provider.provider_must_return_ocel_refs is True
    assert provider.provider_must_support_status_tracking is True
    assert provider.provider_must_support_outcome_mapping is True
    assert provider.contract_only is True
    assert provider.provider_api_call_enabled is False

    assert gate.requires_runtime_inventory is True
    assert gate.requires_capability_observation is True
    assert gate.requires_capability_digestion is True
    assert gate.requires_control_request is True
    assert gate.requires_action_candidate is True
    assert gate.requires_control_plan is True
    assert gate.requires_static_safety_check is True
    assert gate.requires_preflight_before_dispatch is True
    assert gate.requires_human_gate_for_mutating_action is True
    assert gate.requires_human_gate_for_production_action is True
    assert gate.requires_single_use_authorization is True
    assert gate.requires_idempotency_key is True
    assert gate.requires_rate_limit_policy is True
    assert gate.requires_cancel_or_stop_plan is True
    assert gate.requires_status_tracking is True
    assert gate.requires_outcome_record is True
    assert gate.deny_if_credential_exposure_risk is True
    assert gate.deny_if_provider_bypasses_gate is True
    assert gate.deny_if_runtime_not_allowlisted is True
    assert gate.deny_if_capability_not_allowlisted is True

    assert effect.allowed_effect_types_v0_23_0 == ["read_only_observation", "state_candidate_created"]
    assert "external_runtime_touched" in effect.future_effect_types
    assert "external_control_dispatched" in effect.future_effect_types
    assert "external_runtime_touched" in effect.forbidden_effect_types_v0_23_0
    assert "external_control_dispatched" in effect.forbidden_effect_types_v0_23_0


def test_reports_pig_ocpx_and_conformance_build() -> None:
    registry = InternalDominionRegistryService()
    conformance = DominionConformanceService(registry)
    reports = InternalDominionReportService(registry_service=registry, conformance_service=conformance)

    conformance_report = conformance.run_conformance()
    contract_report = reports.build_contract_report()
    pig = reports.build_pig_report()
    ocpx = reports.build_ocpx_projection()

    assert conformance_report.passed is True
    assert contract_report.status == "contract_only"
    assert pig["version"] == "v0.23.0"
    assert pig["layer"] == "internal_dominion"
    assert pig["subject"] == "internal_dominion_contract"
    assert pig["taxonomy"]["categories"] == ["observation", "digestion", "dominion"]
    assert pig["migration"]["self_execution_reclassified_to"] == "v0.24.x Local Runtime Provider"
    assert pig["migration"]["vendor_adapters_reclassified_to"] == "future external provider skills"
    assert pig["migration"]["growthkernel_dependency"] == "future_consumer_not_dependency"
    assert pig["safety_boundary"]["dispatch_enabled"] is False
    assert pig["safety_boundary"]["external_runtime_touched"] is False
    assert pig["safety_boundary"]["provider_api_call_performed"] is False
    assert pig["safety_boundary"]["credential_exposed"] is False
    assert ocpx["state"] == "internal_dominion_contract_registered"
    assert "InternalDominionContractState" in ocpx["target_read_models"]
    assert "DominionMigrationState" in ocpx["target_read_models"]
    assert {"read_only_observation", "state_candidate_created"} <= set(ocpx["effect_types"])


def test_dominion_cli_commands() -> None:
    for command in [
        "contract",
        "taxonomy",
        "subjects",
        "provider-interface",
        "migration-audit",
        "conformance",
        "pig-report",
        "ocpx-projection",
    ]:
        completed = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", "dominion", command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "layer=internal_dominion" in completed.stdout
        assert "provider_api_call_performed=false" in completed.stdout
        assert "external_runtime_touched=false" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout


def test_chantacore_cli_alias_supports_dominion_contract() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "chantacore.cli", "dominion", "contract"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert "layer=internal_dominion" in completed.stdout
    assert "self_execution=v0.24 Local Runtime Provider" in completed.stdout
