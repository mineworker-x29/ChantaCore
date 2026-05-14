from chanta_core.observation_digest import ObservationDigestionEcosystemConsolidationService


def test_safety_boundary_defaults_all_dangerous_capabilities_false() -> None:
    service = ObservationDigestionEcosystemConsolidationService()
    service.consolidate()
    safety = service.last_safety_report

    assert safety is not None
    assert safety.external_harness_execution_allowed is False
    assert safety.external_script_execution_allowed is False
    assert safety.shell_allowed is False
    assert safety.network_allowed is False
    assert safety.write_allowed is False
    assert safety.mcp_allowed is False
    assert safety.plugin_allowed is False
    assert safety.memory_mutation_allowed is False
    assert safety.persona_mutation_allowed is False
    assert safety.overlay_mutation_allowed is False


def test_executable_external_candidate_fixture_creates_high_finding() -> None:
    service = ObservationDigestionEcosystemConsolidationService(
        external_candidate_fixtures=[{"candidate_id": "external_candidate:public", "execution_enabled": True}],
    )
    snapshot = service.create_ecosystem_snapshot()

    assert snapshot.executable_external_candidate_count == 1
    assert any(
        item.finding_type == "executable_external_candidate_detected" and item.severity == "high"
        for item in service.last_findings
    )

