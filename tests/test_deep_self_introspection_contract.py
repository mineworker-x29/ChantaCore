import subprocess
import sys

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    DEEP_SELF_INTROSPECTION_SEED_SKILL_IDS,
    DEEP_SELF_INTROSPECTION_SEED_SUBJECT_IDS,
    DeepSelfIntrospectionRegistryService,
    DeepSelfIntrospectionReportService,
)


def test_deep_self_introspection_contract_builds() -> None:
    contract = DeepSelfIntrospectionRegistryService().build_contract()
    assert contract.version == "v0.21.0"
    assert contract.layer == "deep_self_introspection"
    assert contract.status == "contract_only"
    assert contract.pig_projection_required is True
    assert contract.ocpx_projection_required is True
    assert contract.workbench_visibility_required is True


def test_all_seed_subjects_and_seed_skills_are_registered() -> None:
    service = DeepSelfIntrospectionRegistryService()
    assert [item.subject_id for item in service.list_subjects()] == DEEP_SELF_INTROSPECTION_SEED_SUBJECT_IDS
    assert service.list_seed_skill_ids() == DEEP_SELF_INTROSPECTION_SEED_SKILL_IDS
    assert len(service.list_seed_skill_ids()) == 7


def test_seed_subjects_are_contract_only_and_ocel_mapped() -> None:
    subjects = DeepSelfIntrospectionRegistryService().list_subjects()
    for subject in subjects:
        assert subject.status == "contract_only"
        assert subject.ocel_object_types
        assert subject.ocel_event_types
        assert subject.ocel_relation_types
        assert subject.required_source_objects
        assert subject.required_read_models
        assert "no_actual_analysis_in_v0.21.0" in subject.risk_notes


def test_risk_profile_is_read_only_and_non_mutating() -> None:
    risk = DeepSelfIntrospectionRegistryService().build_contract().risk_profile
    assert risk.read_only is True
    assert risk.ocel_read_only is True
    assert risk.uses_existing_self_awareness_graph is True
    assert risk.mutates_workspace is False
    assert risk.mutates_memory is False
    assert risk.mutates_persona is False
    assert risk.mutates_overlay is False
    assert risk.mutates_capability_registry is False
    assert risk.mutates_policy is False
    assert risk.grants_permission is False
    assert risk.creates_task is False
    assert risk.materializes_candidate is False
    assert risk.promotes_candidate is False
    assert risk.uses_shell is False
    assert risk.uses_network is False
    assert risk.uses_mcp is False
    assert risk.loads_plugin is False
    assert risk.executes_external_harness is False
    assert risk.uses_llm_judge is False
    assert risk.dangerous_capability is False


def test_gate_and_observability_contracts_are_strict() -> None:
    contract = DeepSelfIntrospectionRegistryService().build_contract()
    gate = contract.gate_contract
    assert gate.requires_explicit_invocation is True
    assert gate.requires_read_only_gate is True
    assert gate.requires_execution_envelope is True
    assert gate.requires_ocel_source_refs is True
    assert gate.requires_subject_contract is True
    assert gate.deny_if_missing_ocel_source is True
    assert gate.deny_if_mutation_requested is True
    assert gate.deny_if_permission_escalation_requested is True
    assert gate.deny_if_external_execution_requested is True
    observability = contract.observability_contract
    assert observability.ocel_visible is True
    assert observability.pig_visible is True
    assert observability.ocpx_visible is True
    assert observability.workbench_visible is True
    assert observability.audit_visible is True
    assert observability.envelope_visible is True
    assert observability.evidence_refs_required is True
    assert observability.withdrawal_conditions_required is True
    assert observability.validity_horizon_required is True


def test_ocel_mapping_skeleton_contains_required_types() -> None:
    for object_type in [
        "deep_self_introspection_layer",
        "deep_self_introspection_contract",
        "deep_self_introspection_subject",
        "deep_self_introspection_skill_contract",
        "deep_self_introspection_risk_profile",
        "deep_self_introspection_gate_contract",
        "deep_self_introspection_observability_contract",
        "deep_self_introspection_report",
        "capability_registry_subject",
        "runtime_boundary_subject",
        "policy_gate_subject",
        "trace_integrity_subject",
        "context_projection_subject",
        "candidate_memory_boundary_subject",
        "self_claim_consistency_subject",
        "self_awareness_ecosystem_snapshot",
        "self_awareness_consolidation_report",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES
    for event_type in [
        "deep_self_introspection_layer_registered",
        "deep_self_introspection_contract_registered",
        "deep_self_introspection_subject_registered",
        "deep_self_introspection_contract_checked",
        "deep_self_introspection_conformance_report_created",
        "deep_self_introspection_pig_report_created",
        "deep_self_introspection_ocpx_projection_created",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES
    for relation_type in [
        "declares_introspection_subject",
        "maps_subject_to_ocel_object",
        "maps_subject_to_ocel_event",
        "maps_subject_to_ocel_relation",
        "requires_source_object",
        "requires_read_model",
        "requires_pig_projection",
        "requires_ocpx_projection",
        "checks_contract",
        "visible_in_workbench",
        "derived_from_self_awareness_consolidation",
        "recorded_in_envelope",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES


def test_pig_and_ocpx_skeletons_build() -> None:
    service = DeepSelfIntrospectionReportService()
    pig = service.build_pig_report()
    assert pig["version"] == "v0.21.0"
    assert pig["layer"] == "deep_self_introspection"
    assert pig["source_layer"] == "self_awareness"
    assert pig["requires_self_awareness_consolidation"] == "v0.20.9"
    assert set(pig["subjects"]) == set(DEEP_SELF_INTROSPECTION_SEED_SUBJECT_IDS)
    assert pig["safety_boundary"]["read_only"] is True
    assert pig["safety_boundary"]["mutation_enabled"] is False
    assert pig["safety_boundary"]["permission_escalation_enabled"] is False
    assert pig["safety_boundary"]["external_execution_enabled"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    ocpx = service.build_ocpx_projection()
    assert ocpx["state"] == "deep_self_introspection_contract_registered"
    assert "SelfAwarenessReleaseState" in ocpx["source_read_models"]
    assert "SelfAwarenessWorkbenchState" in ocpx["source_read_models"]
    assert "SelfCapabilityTruthState" in ocpx["target_read_models"]
    assert "SelfRuntimeBoundaryState" in ocpx["target_read_models"]
    assert "SelfPolicyGateState" in ocpx["target_read_models"]
    assert "SelfTraceIntegrityState" in ocpx["target_read_models"]
    assert "SelfContextProjectionState" in ocpx["target_read_models"]
    assert "SelfCandidateMemoryBoundaryState" in ocpx["target_read_models"]
    assert "SelfClaimConsistencyState" in ocpx["target_read_models"]
    assert "read_only_observation" in ocpx["effect_types"]
    assert "state_candidate_created" in ocpx["effect_types"]


def test_contract_report_is_report_only() -> None:
    report = DeepSelfIntrospectionReportService().build_contract_report()
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.withdrawal_conditions
    assert report.validity_horizon


def test_cli_deep_self_views_work() -> None:
    commands = [
        ["deep-self", "contract"],
        ["deep-self", "subjects"],
        ["deep-self", "show", "subject:capability_registry"],
        ["deep-self", "conformance"],
        ["deep-self", "pig-report"],
        ["deep-self", "ocpx-projection"],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=True,
            capture_output=True,
            text=True,
        )
        assert "layer=deep_self_introspection" in result.stdout
        assert "raw_secrets_printed" not in result.stdout or "raw_secrets_printed=False" in result.stdout


def test_no_jsonl_canonical_store_is_introduced() -> None:
    contract = DeepSelfIntrospectionRegistryService().build_contract()
    assert contract.ocel_mapping.to_dict()
    pig = DeepSelfIntrospectionReportService().build_pig_report()
    assert pig["canonical_store"] == "ocel"
