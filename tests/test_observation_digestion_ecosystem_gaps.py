from chanta_core.observation_digest import ObservationDigestionEcosystemConsolidationService


def test_gap_register_includes_future_tracks() -> None:
    service = ObservationDigestionEcosystemConsolidationService()
    service.consolidate()
    names = {item.gap_name for item in service.last_gap_registers}

    assert "full external adapters" in names
    assert "sidecar observer" in names
    assert "event bus collector" in names
    assert "enterprise collector" in names
    assert "write safety track" in names
    assert "shell safety track" in names
    assert "network safety track" in names
    assert "MCP safety track" in names
    assert "plugin safety track" in names

