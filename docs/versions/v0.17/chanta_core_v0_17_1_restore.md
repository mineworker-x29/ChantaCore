# ChantaCore v0.17.1 Restore Document

Version name: ChantaCore v0.17.1 - Personal Mode Prompt Activation

## Purpose

v0.17.1 adds a generic Personal Mode Prompt Activation framework. It attaches bounded Personal Mode loadout, Personal Runtime Binding, Personal Overlay Projection, Personal Conformance, and Personal Runtime Smoke Test summary blocks to prompt context.

Activation scope is `prompt_context_only`. It does not grant capabilities, execute tools, execute workspace reads, call an LLM, use shell/network, connect MCP, load plugins, or auto-select modes from natural language. Capability truth remains above personal claims.

## Implemented Files

- `src/chanta_core/persona/personal_prompt_activation.py`
- `src/chanta_core/persona/ids.py`
- `src/chanta_core/persona/errors.py`
- `src/chanta_core/persona/history_adapter.py`
- `src/chanta_core/persona/__init__.py`
- `src/chanta_core/runtime/agent_runtime.py`
- `src/chanta_core/session/prompt_renderer.py`
- `src/chanta_core/session/context_assembler.py`
- `src/chanta_core/pig/reports.py`
- `tests/test_personal_prompt_activation_models.py`
- `tests/test_personal_prompt_activation_service.py`
- `tests/test_personal_prompt_activation_rendering.py`
- `tests/test_personal_prompt_activation_ocel_shape.py`
- `tests/test_personal_prompt_activation_history_adapter.py`
- `tests/test_personal_prompt_activation_boundaries.py`
- `tests/test_agent_runtime_personal_prompt_activation_integration.py`
- `tests/test_imports.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

## Public API / Model Surface

New models:

- `PersonalPromptActivationConfig`
- `PersonalPromptActivationRequest`
- `PersonalPromptActivationBlock`
- `PersonalPromptActivationResult`
- `PersonalPromptActivationFinding`

New service:

- `PersonalPromptActivationService`

New ID helpers:

- `new_personal_prompt_activation_config_id`
- `new_personal_prompt_activation_request_id`
- `new_personal_prompt_activation_block_id`
- `new_personal_prompt_activation_result_id`
- `new_personal_prompt_activation_finding_id`

## Service Behavior

`PersonalPromptActivationService.load_activation_config` reads local env/config signals only:

- `CHANTA_PERSONAL_MODE`
- `CHANTA_PERSONAL_PROFILE`
- `CHANTA_PERSONAL_RUNTIME_KIND`
- `CHANTA_PERSONAL_DIRECTORY_ROOT`

Missing configuration returns inactive or missing-config records instead of crashing. The service can also accept explicit runtime inputs supplied by trusted callers in tests or runtime integration.

The service builds prompt blocks from:

- explicit `PersonalModeLoadout`
- explicit `PersonalRuntimeBinding`
- explicit safe `PersonalOverlayLoadResult`
- optional `PersonalConformanceResult`
- optional `PersonalSmokeTestResult`

It does not read Personal Source file bodies. It does not use `letters`, `messages`, or `archive` as prompt source. It does not create permission grants.

## AgentRuntime Integration

AgentRuntime now has a Personal Mode Prompt Activation slot in prompt assembly.

Prompt order:

1. system prompt
2. generic persona projection
3. Personal Mode Prompt Activation block
4. runtime capability decision surface
5. session context projection
6. current user message

If activation is skipped, prompt assembly continues normally. If activation is denied, no private block is inserted. Integration only inserts prompt context and does not mutate runtime behavior.

## OCEL Shape

Object types:

- `personal_prompt_activation_config`
- `personal_prompt_activation_request`
- `personal_prompt_activation_block`
- `personal_prompt_activation_result`
- `personal_prompt_activation_finding`

Events:

- `personal_prompt_activation_config_loaded`
- `personal_prompt_activation_requested`
- `personal_prompt_activation_block_created`
- `personal_prompt_activation_attached`
- `personal_prompt_activation_skipped`
- `personal_prompt_activation_denied`
- `personal_prompt_activation_finding_recorded`

Relations:

- activation result belongs to request
- activation result includes blocks
- activation finding belongs to request/result
- activation block references mode loadout/runtime binding/overlay load result/conformance/smoke when available

## Context History

New adapters use `source="personal_prompt_activation"`:

- `personal_prompt_activation_results_to_history_entries`
- `personal_prompt_activation_blocks_to_history_entries`
- `personal_prompt_activation_findings_to_history_entries`

Denied or unsafe findings receive high priority. Attached blocks are medium priority. Skipped activation is low to medium priority.

## PIG / OCPX Report Support

The PIG persona summary includes:

- `personal_prompt_activation_config_count`
- `personal_prompt_activation_request_count`
- `personal_prompt_activation_block_count`
- `personal_prompt_activation_result_count`
- `personal_prompt_activation_finding_count`
- `personal_prompt_activation_attached_count`
- `personal_prompt_activation_skipped_count`
- `personal_prompt_activation_denied_count`
- `personal_prompt_activation_prompt_context_only_count`
- `personal_prompt_activation_unsafe_finding_count`

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_personal_prompt_activation_models.py tests\test_personal_prompt_activation_service.py tests\test_personal_prompt_activation_rendering.py tests\test_personal_prompt_activation_ocel_shape.py tests\test_personal_prompt_activation_history_adapter.py tests\test_personal_prompt_activation_boundaries.py tests\test_agent_runtime_personal_prompt_activation_integration.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

4. Check public hygiene with generic private-boundary tokens only:

```powershell
rg -n "private_persona_name|private_user_name|<LOCAL_PRIVATE_ROOT>" src tests docs README.md pyproject.toml
```

Expected result: no public private-content matches.

## Test Coverage

Covered behavior:

- env absent -> skipped/missing-config
- explicit loadout -> attached with `prompt_context_only`
- runtime binding block states that it grants no capabilities
- overlay projection blocks exclude source bodies
- max character truncation
- unsafe overlay finding denies attachment
- conformance/smoke failure can deny when pass is required
- AgentRuntime prompt order when integrated
- capability truth override statement
- OCEL objects/events/relations
- ContextHistory adapters
- PIG/OCPX summary counts
- no private names/content in dummy data
- no LLM/tool/shell/network/MCP/plugin execution

## Known Limitations

- No explicit skill invocation surface yet.
- No skill proposal router yet.
- No read-only execution gate yet.
- No natural-language mode selection.
- No automatic parsing of private mode files into runtime capability grants.

## Future Work

- v0.17.2: explicit skill invocation surface.
- v0.17.3: skill proposal router.
- v0.17.4: read-only execution gate.

## Checklist

- [x] Public terminology uses generic Personal Mode Prompt Activation concepts.
- [x] Activation scope is `prompt_context_only` or `none`.
- [x] Activation does not grant capabilities.
- [x] Activation does not execute tools.
- [x] Activation does not auto-select mode from natural language.
- [x] Activation does not expose private source bodies.
- [x] Capability truth override statement is present.
- [x] AgentRuntime integration only inserts prompt blocks.
- [x] OCEL shape added.
- [x] ContextHistory adapter added.
- [x] PIG/OCPX lightweight report support added.
- [x] Public tests use dummy data only.
