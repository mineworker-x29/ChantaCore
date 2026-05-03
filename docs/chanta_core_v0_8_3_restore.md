# ChantaCore v0.8.3 — Safe Tool Permission Skeleton

## Purpose

v0.8.3 adds a safe tool permission skeleton before any edit, write, shell, or network capability exists.

This version creates deterministic authorization structures only. It does not add dangerous execution capability.

## Implemented Scope

- `ToolPermissionDecision`
- `ToolRiskClassifier`
- `ToolOperationRisk`
- `ToolPermissionRule`
- `ToolPermissionRuleSet`
- mode-aware `ToolPolicy`
- dispatcher handling for denied and `approval_required` decisions

Permission modes:

- `readonly`
- `safe_internal`
- `approval_required`
- `deny_all`

## Deny-First Behavior

Permission rules are evaluated deny-first:

1. matching `deny` rules win
2. matching `approval_required` rules win over allow
3. matching `allow` applies only if no deny or approval-required rule matched

Default behavior:

- readonly/internal read-only/compute/intelligence tools are allowed
- write risk is `approval_required` only in approval-required mode
- shell/network/dangerous risk is denied
- deny_all denies everything

## Approval Required State

`approval_required` is a state, not a prompt.

v0.8.3 does not include:

- interactive permission UI
- approval token
- sandbox
- write/edit tools
- shell tools
- network tools

If a request requires approval, `ToolDispatcher` returns `ToolResult(success=False)` and does not execute the tool handler.

## OCEL Trace

Authorization decisions are recorded through the existing `authorize_tool_request` lifecycle event.

The event attrs include:

- `decision`
- `allowed`
- `requires_approval`
- `risk_level`
- `permission_mode`
- `reason`

Denied or approval-required requests do not record `execute_tool_operation` or `complete_tool_operation`.

## Guardrails

v0.8.3 does not implement:

- write/edit/patch functionality
- shell execution
- network/web fetch
- MCP/plugin system
- worker queue
- scheduler
- MissionLoop or GoalLoop
- interactive permission dialogs
- async runtime
- external dependencies

## Future Work

This permission skeleton is a prerequisite for:

- v0.8.4 edit proposal objects
- v0.8.5 approved patch application

Remaining limitations:

- no interactive permission UI
- no approval token
- no sandbox
- no write/edit tools yet
- no shell/network tools yet
