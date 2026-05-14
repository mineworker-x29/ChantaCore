import inspect

from chanta_core.observation_digest import ecosystem
from chanta_core.observation_digest import ObservationDigestionEcosystemConsolidationService


def test_ecosystem_consolidation_has_no_execution_boundary_tokens() -> None:
    source = inspect.getsource(ecosystem)
    forbidden = [
        "invoke" + "_explicit_skill(",
        "gate" + "_explicit_invocation(",
        "execute" + "_external",
        "run" + "_external_harness",
        "run" + "_script",
        "start" + "_sidecar",
        "connect" + "_event_bus",
        "sub" + "process",
        "os" + ".system",
        "req" + "uests",
        "htt" + "px",
        "sock" + "et",
        "connect" + "_mcp",
        "load" + "_plugin",
        "write" + "_text",
        "complete" + "_text",
        "complete" + "_json",
        "update" + "_persona",
        "update" + "_overlay",
        "write" + "_memory",
    ]
    for token in forbidden:
        assert token not in source

    service = ObservationDigestionEcosystemConsolidationService()
    service.consolidate()
    assert service.last_snapshot.executable_external_candidate_count == 0
    assert all(item.execution_enabled is False for item in service.last_capability_maps)

