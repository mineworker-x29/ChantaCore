from pathlib import Path

from chanta_core.external import MCPPluginDescriptorSkeletonService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    db_path = Path(".pytest-tmp") / "mcp_plugin_descriptor_skeleton_script.sqlite"
    service = MCPPluginDescriptorSkeletonService(
        trace_service=TraceService(ocel_store=OCELStore(db_path)),
    )
    mcp_server = service.import_mcp_server_descriptor(
        raw_descriptor={
            "name": "sample_mcp_server",
            "transport": "stdio",
            "command": "sample-mcp-server",
            "tools": [{"name": "read_resource", "input_schema": {}, "output_schema": {}}],
            "permissions": ["read_file"],
            "risks": ["filesystem_read"],
        }
    )
    plugin = service.import_plugin_descriptor(
        raw_descriptor={
            "name": "sample_plugin",
            "type": "python",
            "entrypoints": [{"name": "register", "ref": "sample_plugin:register"}],
            "permissions": ["network"],
            "risks": ["network_access"],
        }
    )
    mcp_skeleton = service.create_skeleton_from_mcp_server(mcp_server=mcp_server)
    plugin_skeleton = service.create_skeleton_from_plugin(plugin=plugin)
    mcp_validation = service.validate_skeleton(skeleton=mcp_skeleton)
    plugin_validation = service.validate_skeleton(skeleton=plugin_skeleton)

    print(f"mcp_server_id={mcp_server.mcp_server_id} transport={mcp_server.transport}")
    print(f"plugin_id={plugin.plugin_id} plugin_type={plugin.plugin_type}")
    print(
        "mcp_skeleton_id="
        f"{mcp_skeleton.skeleton_id} activation_status={mcp_skeleton.activation_status} "
        f"execution_enabled={mcp_skeleton.execution_enabled}"
    )
    print(
        "plugin_skeleton_id="
        f"{plugin_skeleton.skeleton_id} activation_status={plugin_skeleton.activation_status} "
        f"execution_enabled={plugin_skeleton.execution_enabled}"
    )
    print(f"mcp_validation_id={mcp_validation.validation_id} status={mcp_validation.status}")
    print(f"plugin_validation_id={plugin_validation.validation_id} status={plugin_validation.status}")
    assert mcp_skeleton.execution_enabled is False
    assert plugin_skeleton.execution_enabled is False
    assert mcp_skeleton.activation_status == "disabled"
    assert plugin_skeleton.activation_status == "disabled"


if __name__ == "__main__":
    main()
