# ChantaCore v0.7 Restore Notes

ChantaCore v0.7 introduces internal built-in tool gateways for process
intelligence-native runtime work.

ChantaCore is not a generic LLM/tool harness. OCEL, OCPX, and PIG are built-in
runtime intelligence layers and are exposed as stable internal tools:

- `tool:ocel`
- `tool:ocpx`
- `tool:pig`
- `tool:echo`

The tool surface is intentionally small. Concrete behavior is represented as an
operation inside a gateway tool, not as many tiny duplicated tools. For example,
`query_recent_events` is an operation of `tool:ocel`, and
`compute_activity_sequence` is an operation of `tool:ocpx`.

Skills remain semantic, user-facing capabilities. Tools are internal execution
gateways used by skills.

The tool foundation includes:

- `Tool`
- `ToolRequest`
- `ToolResult`
- `ToolExecutionContext`
- `ToolRegistry`
- `ToolPolicy`
- `ToolDispatcher`

`ToolPolicy` is a lightweight deny-first safety placeholder. It allows readonly
and internal ChantaCore compute/intelligence tools:

- `readonly`
- `internal_readonly`
- `internal_compute`
- `internal_intelligence`

It denies write, network, shell, dangerous, and unknown levels.

Tool lifecycle is recorded to OCEL with canonical event activities:

- `create_tool_request`
- `authorize_tool_request`
- `dispatch_tool`
- `execute_tool_operation`
- `complete_tool_operation`
- `fail_tool_operation`
- `observe_tool_result`

Tool lifecycle records use canonical OCEL event/object/relation shapes and add
`tool`, `tool_request`, `tool_result`, and `error` objects where relevant.

v0.7 does not add file write tools, shell execution, network fetch, MCP/plugin
systems, async tool execution, a sandbox, a permission dialog system, a worker
queue, MissionLoop, GoalLoop, or source-code self-modification.
