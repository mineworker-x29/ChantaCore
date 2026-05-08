import pytest

from chanta_core.external.errors import ExternalDescriptorSkeletonError
from chanta_core.external.ids import (
    new_external_descriptor_skeleton_id,
    new_external_descriptor_skeleton_validation_id,
    new_mcp_server_descriptor_id,
    new_mcp_tool_descriptor_id,
    new_plugin_descriptor_id,
    new_plugin_entrypoint_descriptor_id,
)
from chanta_core.external.mcp_plugin import (
    ExternalDescriptorSkeleton,
    ExternalDescriptorSkeletonValidation,
    MCPServerDescriptor,
    MCPToolDescriptor,
    PluginDescriptor,
    PluginEntrypointDescriptor,
)
from chanta_core.utility.time import utc_now_iso


def test_mcp_plugin_descriptor_models_to_dict() -> None:
    now = utc_now_iso()
    server = MCPServerDescriptor(
        mcp_server_id=new_mcp_server_descriptor_id(),
        server_name="sample_mcp_server",
        transport="stdio",
        command="sample-mcp-server",
        url=None,
        env_keys=["API_KEY"],
        declared_tool_ids=["read_resource"],
        declared_capabilities=["tools"],
        declared_permissions=["filesystem_read"],
        declared_risks=["filesystem_read"],
        source_id="external_capability_source:test",
        external_descriptor_id="external_capability_descriptor:test",
        status="declared",
        created_at=now,
        descriptor_attrs={},
    )
    tool = MCPToolDescriptor(
        mcp_tool_id=new_mcp_tool_descriptor_id(),
        mcp_server_id=server.mcp_server_id,
        tool_name="read_resource",
        description="Read resource metadata.",
        input_schema={},
        output_schema={},
        declared_permissions=["filesystem_read"],
        declared_risks=["filesystem_read"],
        external_descriptor_id=server.external_descriptor_id,
        status="declared",
        created_at=now,
        descriptor_attrs={},
    )
    plugin = PluginDescriptor(
        plugin_id=new_plugin_descriptor_id(),
        plugin_name="sample_plugin",
        plugin_type="python",
        provider="provider",
        version="1.0",
        description="Plugin metadata.",
        declared_entrypoint_ids=["register"],
        declared_permissions=["network_access"],
        declared_risks=["network_access"],
        source_id=server.source_id,
        external_descriptor_id=server.external_descriptor_id,
        status="declared",
        created_at=now,
        descriptor_attrs={},
    )
    entrypoint = PluginEntrypointDescriptor(
        entrypoint_id=new_plugin_entrypoint_descriptor_id(),
        plugin_id=plugin.plugin_id,
        entrypoint_name="register",
        entrypoint_ref="sample_plugin:register",
        entrypoint_type="python_module",
        declared_inputs={},
        declared_outputs={},
        declared_permissions=["network_access"],
        declared_risks=["network_access"],
        status="declared",
        created_at=now,
        entrypoint_attrs={},
    )
    skeleton = ExternalDescriptorSkeleton(
        skeleton_id=new_external_descriptor_skeleton_id(),
        skeleton_type="plugin",
        source_id=plugin.source_id,
        external_descriptor_id=plugin.external_descriptor_id,
        mcp_server_id=None,
        plugin_id=plugin.plugin_id,
        normalized_name=plugin.plugin_name,
        normalized_kind=plugin.plugin_type,
        declared_permission_categories=plugin.declared_permissions,
        declared_risk_categories=plugin.declared_risks,
        review_status="pending_review",
        activation_status="disabled",
        execution_enabled=False,
        created_at=now,
        skeleton_attrs={},
    )
    validation = ExternalDescriptorSkeletonValidation(
        validation_id=new_external_descriptor_skeleton_validation_id(),
        skeleton_id=skeleton.skeleton_id,
        status="passed",
        passed_checks=["execution_disabled"],
        failed_checks=[],
        warning_checks=[],
        validation_messages=[],
        created_at=now,
        validation_attrs={},
    )

    assert server.to_dict()["mcp_server_id"].startswith("mcp_server_descriptor:")
    assert tool.to_dict()["mcp_tool_id"].startswith("mcp_tool_descriptor:")
    assert plugin.to_dict()["plugin_id"].startswith("plugin_descriptor:")
    assert entrypoint.to_dict()["entrypoint_id"].startswith("plugin_entrypoint_descriptor:")
    assert skeleton.to_dict()["skeleton_id"].startswith("external_descriptor_skeleton:")
    assert validation.to_dict()["validation_id"].startswith("external_descriptor_skeleton_validation:")
    assert skeleton.execution_enabled is False
    assert skeleton.activation_status == "disabled"


def test_skeleton_rejects_active_or_enabled_defaults() -> None:
    now = utc_now_iso()
    with pytest.raises(ExternalDescriptorSkeletonError):
        ExternalDescriptorSkeleton(
            skeleton_id=new_external_descriptor_skeleton_id(),
            skeleton_type="plugin",
            source_id=None,
            external_descriptor_id=None,
            mcp_server_id=None,
            plugin_id="plugin_descriptor:test",
            normalized_name="sample",
            normalized_kind="python",
            declared_permission_categories=[],
            declared_risk_categories=[],
            review_status="pending_review",
            activation_status="active",
            execution_enabled=False,
            created_at=now,
            skeleton_attrs={},
        )
