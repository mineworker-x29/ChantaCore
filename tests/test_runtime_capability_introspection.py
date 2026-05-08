from chanta_core.runtime.capability_contract import (
    RuntimeCapabilityIntrospectionService,
    RuntimeCapabilitySnapshot,
)


def test_default_agent_snapshot_has_required_categories() -> None:
    snapshot = RuntimeCapabilityIntrospectionService().build_default_agent_snapshot()
    data = snapshot.to_dict()

    assert isinstance(snapshot, RuntimeCapabilitySnapshot)
    assert data["snapshot_id"].startswith("runtime_capability_snapshot:")
    assert data["agent_id"] == "chanta_core_default"
    for category in [
        "available_now",
        "metadata_only",
        "disabled_candidates",
        "requires_review",
        "requires_permission",
        "not_implemented",
    ]:
        assert isinstance(data[category], list)
        assert data[category]


def test_default_agent_current_capabilities_are_classified() -> None:
    snapshot = RuntimeCapabilityIntrospectionService().build_default_agent_snapshot()

    assert "configured local LLM chat" in snapshot.available_now
    assert "immediate-prompt response" in snapshot.available_now
    assert "OCEL/session/process event recording" in snapshot.available_now
    assert "skill:llm_chat" in snapshot.available_now
    assert "trace-aware local chat surface" in snapshot.available_now

    assert "external capability descriptors" in snapshot.metadata_only
    assert "external assimilation candidates" in snapshot.metadata_only
    assert "external OCEL payload descriptors" in snapshot.metadata_only
    assert "external OCEL import candidates" in snapshot.metadata_only
    assert "external OCEL preview snapshots" in snapshot.metadata_only
    assert "external assimilation candidates with execution_enabled=False" in (
        snapshot.disabled_candidates
    )
    assert "external OCEL import candidates" in snapshot.requires_review
    assert "canonical external OCEL merge" in snapshot.not_implemented
    assert "active external OCEL ingestion" in snapshot.not_implemented
    assert "external OCEL import candidates" not in snapshot.available_now


def test_unsafe_or_unimplemented_actions_are_not_available_now() -> None:
    snapshot = RuntimeCapabilityIntrospectionService().build_default_agent_snapshot()
    unavailable_items = {
        "workspace file read",
        "workspace file write",
        "shell execution",
        "network access",
        "tool dispatch",
        "MCP connection",
        "plugin loading",
        "arbitrary repository file read",
        "/Souls directory inspection",
        "active runtime registry updates",
        "autonomous Soul behavior",
    }

    assert unavailable_items.isdisjoint(set(snapshot.available_now))
    assert "workspace file read" in snapshot.requires_permission
    assert "shell execution" in snapshot.requires_permission
    assert "network access" in snapshot.requires_permission
    assert "MCP connection" in snapshot.not_implemented
    assert "plugin loading" in snapshot.not_implemented


def test_capability_snapshot_labels_inspection_scope() -> None:
    snapshot = RuntimeCapabilityIntrospectionService().build_default_agent_snapshot()

    assert "recent_global" in snapshot.inspection_scopes
    assert "persisted_store" in snapshot.inspection_scopes
    assert "current_session not enabled by default" in snapshot.inspection_scopes
    assert "current_process_instance not enabled by default" in snapshot.inspection_scopes
