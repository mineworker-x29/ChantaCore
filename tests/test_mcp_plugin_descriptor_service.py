from chanta_core.external import MCPPluginDescriptorSkeletonService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_mcp_plugin_descriptor_service_records_flow(tmp_path) -> None:
    store = OCELStore(tmp_path / "mcp_plugin_service.sqlite")
    service = MCPPluginDescriptorSkeletonService(trace_service=TraceService(ocel_store=store))
    external_descriptor_id = "external_capability_descriptor:test"
    source_id = "external_capability_source:test"

    server = service.import_mcp_server_descriptor(
        raw_descriptor={
            "name": "sample_mcp_server",
            "transport": "stdio",
            "command": "sample-mcp-server",
            "tools": [{"name": "read_resource", "input_schema": {}, "output_schema": {}}],
            "permissions": ["read_file"],
            "risks": ["filesystem_read"],
        },
        source_id=source_id,
        external_descriptor_id=external_descriptor_id,
    )
    tool = service.import_mcp_tool_descriptor(
        raw_tool_descriptor={"name": "read_resource", "input_schema": {}, "output_schema": {}},
        mcp_server_id=server.mcp_server_id,
        external_descriptor_id=external_descriptor_id,
    )
    plugin = service.import_plugin_descriptor(
        raw_descriptor={
            "name": "sample_plugin",
            "type": "python",
            "entrypoints": [{"name": "register", "ref": "sample_plugin:register"}],
            "permissions": ["network"],
            "risks": ["network_access"],
        },
        source_id=source_id,
        external_descriptor_id=external_descriptor_id,
    )
    entrypoint = service.import_plugin_entrypoint_descriptor(
        raw_entrypoint={"name": "register", "ref": "sample_plugin:register", "type": "python_module"},
        plugin_id=plugin.plugin_id,
    )
    mcp_skeleton = service.create_skeleton_from_mcp_server(mcp_server=server)
    plugin_skeleton = service.create_skeleton_from_plugin(plugin=plugin)
    validation = service.validate_skeleton(skeleton=mcp_skeleton)

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "mcp_server_descriptor_imported",
        "mcp_tool_descriptor_imported",
        "plugin_descriptor_imported",
        "plugin_entrypoint_descriptor_imported",
        "external_descriptor_skeleton_created",
        "external_descriptor_skeleton_validated",
        "mcp_plugin_descriptor_linked_to_external_descriptor",
        "mcp_plugin_descriptor_marked_non_executable",
    }.issubset(activities)
    assert server.command == "sample-mcp-server"
    assert tool.mcp_server_id == server.mcp_server_id
    assert entrypoint.entrypoint_ref == "sample_plugin:register"
    assert mcp_skeleton.execution_enabled is False
    assert plugin_skeleton.activation_status == "disabled"
    assert validation.status == "passed"
