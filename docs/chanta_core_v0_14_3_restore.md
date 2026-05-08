# ChantaCore v0.14.3 Restore Notes

## Version

ChantaCore v0.14.3 adds MCP / Plugin Descriptor Skeleton.

This version models MCP server descriptors, MCP tool descriptors, plugin descriptors, plugin entrypoint descriptors, and disabled external descriptor skeletons. It records descriptor metadata and structural validation results as OCEL event, object, and relation records.

v0.14.3 is metadata-only. It does not connect to MCP servers, list MCP tools, load plugins, import plugin entrypoints, or activate any runtime capability.

## Architectural Boundary

Canonical persistence remains OCEL-based.

MCP/plugin descriptor skeleton state is represented by OCEL event, object, and relation records. JSONL is not introduced as canonical descriptor persistence. Markdown remains a human-readable materialized view only and is not a descriptor source.

Descriptor command, URL, and entrypoint fields are stored as metadata only. They are never used to perform runtime connection, loading, or execution in this version.

## Package Extension

The implementation extends `src/chanta_core/external/`.

New file:

- `mcp_plugin.py`

Updated files:

- `__init__.py`
- `ids.py`
- `errors.py`
- `history_adapter.py`

Reporting support is extended in:

- `src/chanta_core/pig/reports.py`
- `src/chanta_core/pig/inspector.py`

## New Models

`MCPServerDescriptor` records MCP server metadata.

Key fields:

- `mcp_server_id`
- `server_name`
- `transport`
- `command`
- `url`
- `env_keys`
- `declared_tool_ids`
- `declared_capabilities`
- `declared_permissions`
- `declared_risks`
- `source_id`
- `external_descriptor_id`
- `status`
- `created_at`
- `descriptor_attrs`

`command` and `url` are metadata only.

`MCPToolDescriptor` records MCP tool metadata.

Key fields:

- `mcp_tool_id`
- `mcp_server_id`
- `tool_name`
- `description`
- `input_schema`
- `output_schema`
- `declared_permissions`
- `declared_risks`
- `external_descriptor_id`
- `status`
- `created_at`
- `descriptor_attrs`

`PluginDescriptor` records plugin package metadata.

Key fields:

- `plugin_id`
- `plugin_name`
- `plugin_type`
- `provider`
- `version`
- `description`
- `declared_entrypoint_ids`
- `declared_permissions`
- `declared_risks`
- `source_id`
- `external_descriptor_id`
- `status`
- `created_at`
- `descriptor_attrs`

`PluginEntrypointDescriptor` records plugin entrypoint metadata.

Key fields:

- `entrypoint_id`
- `plugin_id`
- `entrypoint_name`
- `entrypoint_ref`
- `entrypoint_type`
- `declared_inputs`
- `declared_outputs`
- `declared_permissions`
- `declared_risks`
- `status`
- `created_at`
- `entrypoint_attrs`

`entrypoint_ref` is metadata only.

`ExternalDescriptorSkeleton` records a disabled review/design skeleton derived from MCP/plugin metadata.

Key fields:

- `skeleton_id`
- `skeleton_type`
- `source_id`
- `external_descriptor_id`
- `mcp_server_id`
- `plugin_id`
- `normalized_name`
- `normalized_kind`
- `declared_permission_categories`
- `declared_risk_categories`
- `review_status`
- `activation_status`
- `execution_enabled`
- `created_at`
- `skeleton_attrs`

In v0.14.3:

- `execution_enabled=False`
- `activation_status=disabled`
- active skeletons are not created

`ExternalDescriptorSkeletonValidation` records structural validation results.

Key fields:

- `validation_id`
- `skeleton_id`
- `status`
- `passed_checks`
- `failed_checks`
- `warning_checks`
- `validation_messages`
- `created_at`
- `validation_attrs`

## Deterministic Helpers

`mcp_plugin.py` provides metadata extraction and normalization helpers:

- `extract_mcp_server_name`
- `extract_mcp_transport`
- `extract_mcp_tool_descriptors`
- `extract_plugin_name`
- `extract_plugin_type`
- `extract_plugin_entrypoints`
- `normalize_descriptor_permission`
- `normalize_descriptor_risk`

These helpers perform pure dict/list/string processing. They do not contact external systems.

## OCEL Objects

v0.14.3 introduces these OCEL object types:

- `mcp_server_descriptor`
- `mcp_tool_descriptor`
- `plugin_descriptor`
- `plugin_entrypoint_descriptor`
- `external_descriptor_skeleton`
- `external_descriptor_skeleton_validation`

Descriptor OCEL objects include `execution_enabled: false`.

Skeleton OCEL objects include:

- `review_status`
- `activation_status`
- `execution_enabled: false`
- normalized kind/name
- declared permission categories
- declared risk categories

## OCEL Events

The service records these event activities:

- `mcp_server_descriptor_imported`
- `mcp_tool_descriptor_imported`
- `plugin_descriptor_imported`
- `plugin_entrypoint_descriptor_imported`
- `external_descriptor_skeleton_created`
- `external_descriptor_skeleton_validated`
- `external_descriptor_skeleton_validation_failed`
- `mcp_plugin_descriptor_linked_to_external_descriptor`
- `mcp_plugin_descriptor_marked_non_executable`

Object relation intent:

- MCP server descriptor from source
- MCP server descriptor derived from external descriptor
- MCP tool descriptor belongs to MCP server
- MCP tool descriptor derived from external descriptor
- plugin descriptor from source
- plugin descriptor derived from external descriptor
- plugin entrypoint descriptor belongs to plugin
- skeleton represents MCP server or plugin
- skeleton derived from external descriptor
- validation validates skeleton

## Service Behavior

`MCPPluginDescriptorSkeletonService` supports:

- `import_mcp_server_descriptor`
- `import_mcp_tool_descriptor`
- `import_plugin_descriptor`
- `import_plugin_entrypoint_descriptor`
- `create_skeleton_from_mcp_server`
- `create_skeleton_from_plugin`
- `validate_skeleton`

Descriptor import methods extract metadata only.

Skeleton creation creates disabled skeletons only:

- `review_status="pending_review"`
- `activation_status="disabled"`
- `execution_enabled=False`

Validation checks:

- `name_present`
- `kind_present`
- `execution_disabled`
- `activation_disabled`
- `entrypoint_metadata_only`
- `permissions_declared_or_empty`
- `risks_declared_or_empty`
- `review_required`

Validation records failed skeletons without mutating them.

## Explicit Non-Goals

v0.14.3 does not do the following:

- no MCP runtime connection
- no MCP tools/list call
- no MCP tool call
- no external tool execution
- no external skill execution
- no plugin dynamic loading
- no plugin entrypoint import
- no external code import
- no network call
- no URL fetch
- no git clone
- no pip or npm install
- no `ToolDispatcher` mutation
- no `SkillExecutor` mutation
- no `AgentRuntime` active capability integration
- no permission auto-grant
- no sandbox auto-creation
- no review decision auto-creation
- no candidate auto-enable
- no LLM classifier
- no LLM reviewer
- no Markdown descriptor import
- no canonical JSONL MCP/plugin descriptor store
- no async worker
- no UI

## Context History

`src/chanta_core/external/history_adapter.py` provides these adapters:

- `mcp_server_descriptors_to_history_entries`
- `mcp_tool_descriptors_to_history_entries`
- `plugin_descriptors_to_history_entries`
- `plugin_entrypoint_descriptors_to_history_entries`
- `external_descriptor_skeletons_to_history_entries`
- `external_descriptor_skeleton_validations_to_history_entries`

The adapter source is `mcp_plugin_descriptor_skeleton`.

Refs include MCP server IDs, MCP tool IDs, plugin IDs, entrypoint IDs, skeleton IDs, validation IDs, external descriptor IDs, and source IDs where available.

The adapter does not retrieve from OCEL automatically. It only adapts supplied objects.

## PIG/OCPX Report Support

PIG report attrs include MCP/plugin descriptor skeleton fields under `external_capability_summary`.

The summary includes:

- `mcp_server_descriptor_count`
- `mcp_tool_descriptor_count`
- `plugin_descriptor_count`
- `plugin_entrypoint_descriptor_count`
- `external_descriptor_skeleton_count`
- `external_descriptor_skeleton_validation_count`
- `mcp_descriptor_needs_review_count`
- `plugin_descriptor_needs_review_count`
- `skeleton_validation_passed_count`
- `skeleton_validation_failed_count`
- `skeleton_validation_needs_review_count`
- `mcp_plugin_execution_enabled_count`
- `mcp_plugin_activation_enabled_count`
- `mcp_plugin_descriptor_by_type`
- `mcp_plugin_risk_category_count`

For v0.14.3:

- `mcp_plugin_execution_enabled_count` should normally be `0`
- `mcp_plugin_activation_enabled_count` should normally be `0`

The PI substrate inspector surfaces descriptor skeleton count and MCP/plugin execution-enabled count.

## Tests

v0.14.3 adds:

- `tests/test_mcp_plugin_descriptor_models.py`
- `tests/test_mcp_plugin_descriptor_service.py`
- `tests/test_mcp_plugin_descriptor_validation.py`
- `tests/test_mcp_plugin_descriptor_history_adapter.py`
- `tests/test_mcp_plugin_descriptor_ocel_shape.py`
- `tests/test_mcp_plugin_descriptor_boundaries.py`

Existing tests updated:

- `tests/test_imports.py`
- `tests/test_pig_reports.py`

The optional script is:

- `scripts/test_mcp_plugin_descriptor_skeleton.py`

## Restore Procedure

1. Confirm version metadata:
   - `pyproject.toml` version is `0.14.3`.
   - `src/chanta_core/__init__.py` `__version__` is `0.14.3`.
2. Confirm `src/chanta_core/external/mcp_plugin.py` exists.
3. Confirm review queue support from v0.14.2 still exists:
   - `src/chanta_core/external/review.py`
4. Confirm exports from `chanta_core.external`:
   - `MCPServerDescriptor`
   - `MCPToolDescriptor`
   - `PluginDescriptor`
   - `PluginEntrypointDescriptor`
   - `ExternalDescriptorSkeleton`
   - `ExternalDescriptorSkeletonValidation`
   - `MCPPluginDescriptorSkeletonService`
5. Run MCP/plugin descriptor tests:
   - `tests/test_mcp_plugin_descriptor_models.py`
   - `tests/test_mcp_plugin_descriptor_service.py`
   - `tests/test_mcp_plugin_descriptor_validation.py`
   - `tests/test_mcp_plugin_descriptor_history_adapter.py`
   - `tests/test_mcp_plugin_descriptor_ocel_shape.py`
   - `tests/test_mcp_plugin_descriptor_boundaries.py`
6. Run `tests/test_imports.py` and `tests/test_pig_reports.py`.
7. Run `scripts/test_mcp_plugin_descriptor_skeleton.py`.
8. Confirm skeletons remain:
   - `execution_enabled=False`
   - `activation_status=disabled`
9. Confirm command, URL, and entrypoint refs are metadata only.
10. Confirm no generated runtime files are tracked.

## Future Work

- External OCEL Import Candidate
- Later activation only after an explicit safety and conformance layer
