from __future__ import annotations

from pathlib import Path

from chanta_core.internal_dominion import (
    DOMINION_EFFECT_TYPES,
    DominionRuntimeInventoryRequest,
    RuntimeInventoryReportService,
)


RUNTIME_SOURCE_ROOT = Path("src/chanta_core/internal_dominion")


def test_inventory_report_does_not_perform_provider_api_runtime_touch_or_dispatch() -> None:
    report = RuntimeInventoryReportService().build_report(DominionRuntimeInventoryRequest())
    snapshot = report.snapshot

    assert snapshot.dispatch_enabled is False
    assert snapshot.external_runtime_touched is False
    assert snapshot.provider_api_call_performed is False
    assert snapshot.credential_exposed is False
    assert snapshot.raw_secret_output is False
    assert all(runtime.dispatch_enabled is False for runtime in snapshot.runtimes)
    assert all(runtime.runtime_touched is False for runtime in snapshot.runtimes)
    assert all(runtime.provider_api_call_performed is False for runtime in snapshot.runtimes)
    assert all(surface.dispatch_enabled_v0_23_1 is False for surface in snapshot.control_surfaces)
    assert all(surface.provider_api_call_enabled_v0_23_1 is False for surface in snapshot.control_surfaces)
    assert all(boundary.credential_value_stored is False for boundary in snapshot.credential_boundaries)
    assert all(boundary.credential_value_output is False for boundary in snapshot.credential_boundaries)


def test_inventory_effects_remain_ocel_read_only_candidates() -> None:
    assert {"read_only_observation", "state_candidate_created"} <= set(DOMINION_EFFECT_TYPES)
    assert "external_runtime_touched" not in DOMINION_EFFECT_TYPES
    assert "external_control_dispatched" not in DOMINION_EFFECT_TYPES


def test_inventory_runtime_source_has_no_forbidden_positive_implementation_tokens() -> None:
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
        "external_control_dispatched",
        "external_runtime_touched=True",
        "runtime_touched=True",
        "provider_api_call_performed=True",
        "dispatch_enabled=True",
        "dispatch_enabled_v0_23_1=True",
        "provider_api_call_enabled_v0_23_1=True",
        "credential_value_stored=True",
        "credential_value_output=True",
        "credential_exposed=True",
        "raw_secret_output=True",
        "network_enabled=True",
        "mcp_enabled=True",
        "plugin_enabled=True",
        "shell_enabled=True",
        "local_command_enabled=True",
        "growthkernel_dependency_required=True",
        "llm_judge",
        "openai",
        "anthropic",
        "completion",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    runtime_text = (RUNTIME_SOURCE_ROOT / "inventory.py").read_text(encoding="utf-8")

    for token in forbidden:
        assert token not in runtime_text


def test_vendor_names_are_not_runtime_logic_in_inventory_core() -> None:
    inventory_text = (RUNTIME_SOURCE_ROOT / "inventory.py").read_text(encoding="utf-8")

    for token in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert token not in inventory_text
