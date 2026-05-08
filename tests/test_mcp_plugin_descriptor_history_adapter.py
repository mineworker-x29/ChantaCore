from chanta_core.external import (
    MCPPluginDescriptorSkeletonService,
    external_descriptor_skeleton_validations_to_history_entries,
    external_descriptor_skeletons_to_history_entries,
    mcp_server_descriptors_to_history_entries,
    mcp_tool_descriptors_to_history_entries,
    plugin_descriptors_to_history_entries,
    plugin_entrypoint_descriptors_to_history_entries,
)
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_mcp_plugin_history_adapters_include_refs(tmp_path) -> None:
    service = MCPPluginDescriptorSkeletonService(
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "mcp_plugin_history.sqlite"))
    )
    server = service.import_mcp_server_descriptor(raw_descriptor={"name": "sample_mcp_server", "transport": "stdio"})
    tool = service.import_mcp_tool_descriptor(raw_tool_descriptor={"name": "read_resource"}, mcp_server_id=server.mcp_server_id)
    plugin = service.import_plugin_descriptor(raw_descriptor={"name": "sample_plugin", "type": "python"})
    entrypoint = service.import_plugin_entrypoint_descriptor(
        raw_entrypoint={"name": "register", "ref": "sample_plugin:register"},
        plugin_id=plugin.plugin_id,
    )
    skeleton = service.create_skeleton_from_plugin(plugin=plugin)
    object.__setattr__(skeleton, "normalized_name", None)
    validation = service.validate_skeleton(skeleton=skeleton)

    server_entry = mcp_server_descriptors_to_history_entries([server])[0]
    tool_entry = mcp_tool_descriptors_to_history_entries([tool])[0]
    plugin_entry = plugin_descriptors_to_history_entries([plugin])[0]
    entrypoint_entry = plugin_entrypoint_descriptors_to_history_entries([entrypoint])[0]
    skeleton_entry = external_descriptor_skeletons_to_history_entries([skeleton])[0]
    validation_entry = external_descriptor_skeleton_validations_to_history_entries([validation])[0]

    assert server_entry.source == "mcp_plugin_descriptor_skeleton"
    assert server_entry.refs[0]["mcp_server_id"] == server.mcp_server_id
    assert tool_entry.refs[0]["mcp_tool_id"] == tool.mcp_tool_id
    assert plugin_entry.refs[0]["plugin_id"] == plugin.plugin_id
    assert entrypoint_entry.refs[0]["entrypoint_id"] == entrypoint.entrypoint_id
    assert skeleton_entry.refs[0]["skeleton_id"] == skeleton.skeleton_id
    assert validation_entry.refs[0]["validation_id"] == validation.validation_id
    assert validation_entry.priority >= 90
