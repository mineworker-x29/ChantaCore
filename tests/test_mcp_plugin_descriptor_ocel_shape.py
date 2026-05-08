from chanta_core.external import MCPPluginDescriptorSkeletonService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_mcp_plugin_descriptor_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "mcp_plugin_shape.sqlite")
    service = MCPPluginDescriptorSkeletonService(trace_service=TraceService(ocel_store=store))
    external_descriptor_id = "external_capability_descriptor:test"
    server = service.import_mcp_server_descriptor(
        raw_descriptor={"name": "sample_mcp_server", "transport": "stdio"},
        external_descriptor_id=external_descriptor_id,
    )
    tool = service.import_mcp_tool_descriptor(
        raw_tool_descriptor={"name": "read_resource"},
        mcp_server_id=server.mcp_server_id,
        external_descriptor_id=external_descriptor_id,
    )
    plugin = service.import_plugin_descriptor(
        raw_descriptor={"name": "sample_plugin", "type": "python"},
        external_descriptor_id=external_descriptor_id,
    )
    service.import_plugin_entrypoint_descriptor(
        raw_entrypoint={"name": "register", "ref": "sample_plugin:register"},
        plugin_id=plugin.plugin_id,
    )
    skeleton = service.create_skeleton_from_mcp_server(mcp_server=server)
    validation = service.validate_skeleton(skeleton=skeleton)
    object.__setattr__(skeleton, "normalized_kind", "")
    failed = service.validate_skeleton(skeleton=skeleton)

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "mcp_server_descriptor_imported",
        "mcp_tool_descriptor_imported",
        "plugin_descriptor_imported",
        "plugin_entrypoint_descriptor_imported",
        "external_descriptor_skeleton_created",
        "external_descriptor_skeleton_validated",
        "external_descriptor_skeleton_validation_failed",
        "mcp_plugin_descriptor_linked_to_external_descriptor",
        "mcp_plugin_descriptor_marked_non_executable",
    }.issubset(activities)
    assert store.fetch_objects_by_type("mcp_server_descriptor")
    assert store.fetch_objects_by_type("mcp_tool_descriptor")
    assert store.fetch_objects_by_type("plugin_descriptor")
    assert store.fetch_objects_by_type("plugin_entrypoint_descriptor")
    assert store.fetch_objects_by_type("external_descriptor_skeleton")
    assert store.fetch_objects_by_type("external_descriptor_skeleton_validation")
    assert store.fetch_object_object_relations_for_object(tool.mcp_tool_id)
    assert store.fetch_object_object_relations_for_object(skeleton.skeleton_id)
    assert store.fetch_object_object_relations_for_object(validation.validation_id)
    assert failed.status == "failed"
