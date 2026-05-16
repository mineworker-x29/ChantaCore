from chanta_core.self_awareness import (
    SELF_AWARENESS_OCEL_EVENT_TYPES,
    SELF_AWARENESS_OCEL_OBJECT_TYPES,
    SELF_AWARENESS_OCEL_RELATION_TYPES,
    SELF_AWARENESS_SEED_SKILL_IDS,
    SelfAwarenessConformanceService,
    SelfAwarenessRegistryService,
    SelfAwarenessReportService,
)


EXPECTED_SEED_SKILL_IDS = [
    "skill:self_awareness_workspace_inventory",
    "skill:self_awareness_path_verify",
    "skill:self_awareness_text_read",
    "skill:self_awareness_workspace_search",
    "skill:self_awareness_python_symbols",
    "skill:self_awareness_markdown_structure",
    "skill:self_awareness_project_structure",
    "skill:self_awareness_surface_verify",
    "skill:self_awareness_config_surface",
    "skill:self_awareness_test_surface",
    "skill:self_awareness_capability_registry",
    "skill:self_awareness_runtime_boundary",
    "skill:self_awareness_plan_candidate",
    "skill:self_awareness_todo_candidate",
]


def test_all_seed_skill_ids_are_registered() -> None:
    service = SelfAwarenessRegistryService()

    assert service.list_seed_skill_ids() == EXPECTED_SEED_SKILL_IDS
    assert SELF_AWARENESS_SEED_SKILL_IDS == EXPECTED_SEED_SKILL_IDS
    assert {item.skill_id for item in service.list_contracts()} == set(EXPECTED_SEED_SKILL_IDS)


def test_seed_contract_defaults_are_contract_only_and_read_only() -> None:
    service = SelfAwarenessRegistryService()

    for contract in service.list_contracts():
        risk = contract.risk_profile
        assert contract.layer == "self_awareness"
        assert contract.execution_enabled is False
        assert contract.canonical_mutation_enabled is False
        assert risk.read_only is True
        assert risk.mutates_workspace is False
        assert risk.mutates_memory is False
        assert risk.mutates_persona is False
        assert risk.mutates_overlay is False
        assert risk.uses_shell is False
        assert risk.uses_network is False
        assert risk.uses_mcp is False
        assert risk.loads_plugin is False
        assert risk.executes_external_harness is False
        assert risk.dangerous_capability is False
        assert contract.gate_contract.evidence_refs_required is True
        assert contract.gate_contract.execution_envelope_required is True


def test_conformance_passes_and_dangerous_capability_count_is_zero() -> None:
    service = SelfAwarenessConformanceService()

    report = service.run_conformance()

    assert report.passed is True
    assert report.status == "passed"
    assert report.dangerous_capability_count == 0
    assert report.execution_enabled_count == 0
    assert report.canonical_mutation_enabled_count == 0
    assert report.workspace_mutation_count == 0
    assert report.shell_usage_count == 0
    assert report.network_usage_count == 0
    assert report.mcp_usage_count == 0
    assert report.plugin_loading_count == 0
    assert report.external_harness_execution_count == 0


def test_pig_report_and_ocpx_projection_build() -> None:
    service = SelfAwarenessReportService()

    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["layer"] == "self_awareness"
    assert pig["state"] == "self_awareness_foundation_v1_consolidated"
    assert pig["safety_boundary_counts"]["dangerous_capability_count"] == 0
    assert pig["workspace_awareness_coverage"]["path_verification"] == "implemented"
    assert pig["workspace_awareness_coverage"]["text_read"] == "implemented_limited_preview"
    assert pig["workspace_awareness_coverage"]["workspace_search"] == "implemented_bounded_literal"
    assert pig["workspace_awareness_coverage"]["markdown_structure"] == "implemented_deterministic"
    assert pig["workspace_awareness_coverage"]["python_symbols"] == "implemented_deterministic"
    assert pig["workspace_awareness_coverage"]["project_structure"] == "implemented_surface_snapshot"
    assert pig["workspace_awareness_coverage"]["surface_verification"] == "implemented_evidence_boundary_candidate_checks"
    assert "Self-Awareness Foundation v1 consolidated" in pig["recommendation"]
    assert ocpx["layer"] == "self_awareness"
    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    assert ocpx["workspace_awareness_state"]["workspace_inventory"] == "implemented"
    assert ocpx["workspace_awareness_state"]["workspace_search"] == "implemented_bounded_literal"
    assert "self_awareness_layer" in ocpx["object_coverage"]
    assert "self_awareness_contract_registered" in ocpx["event_coverage"]
    assert "belongs_to_layer" in ocpx["relation_coverage"]


def test_ocel_mapping_constants_cover_required_surface() -> None:
    assert "self_awareness_skill_contract" in SELF_AWARENESS_OCEL_OBJECT_TYPES
    assert "runtime_boundary" in SELF_AWARENESS_OCEL_OBJECT_TYPES
    assert "self_awareness_conformance_report_created" in SELF_AWARENESS_OCEL_EVENT_TYPES
    assert "visible_in_ocpx_projection" in SELF_AWARENESS_OCEL_RELATION_TYPES
