# ChantaCore v0.17.3 Restore Document

Version name: ChantaCore v0.17.3 - Capability-aware Skill Proposal Router

## Purpose

v0.17.3 adds a generic Skill Proposal Router. It can analyze a user prompt with deterministic heuristics and produce a reviewable Explicit Skill Invocation proposal.

The router is proposal-only. It does not execute skills, grant permissions, write files, execute shell/network operations, connect MCP, load plugins, call an LLM classifier, or infer private content.

Initial proposal targets are read-only workspace read skills:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

Unsupported shell, network, write, MCP, plugin, and external capability requests produce controlled unsupported proposal results.

## Implemented Files

- `src/chanta_core/skills/proposal.py`
- `src/chanta_core/skills/ids.py`
- `src/chanta_core/skills/errors.py`
- `src/chanta_core/skills/history_adapter.py`
- `src/chanta_core/skills/__init__.py`
- `src/chanta_core/cli/main.py`
- `src/chanta_core/pig/reports.py`
- `tests/test_skill_proposal_models.py`
- `tests/test_skill_proposal_router_service.py`
- `tests/test_skill_proposal_heuristics.py`
- `tests/test_skill_proposal_cli.py`
- `tests/test_skill_proposal_history_adapter.py`
- `tests/test_skill_proposal_ocel_shape.py`
- `tests/test_skill_proposal_boundaries.py`
- `tests/test_imports.py`
- `pyproject.toml`
- `src/chanta_core/__init__.py`

## Public API / Model Surface

New models:

- `SkillProposalIntent`
- `SkillProposalRequirement`
- `SkillInvocationProposal`
- `SkillProposalDecision`
- `SkillProposalReviewNote`
- `SkillProposalResult`

New service:

- `SkillProposalRouterService`

New ID helpers:

- `new_skill_proposal_intent_id`
- `new_skill_proposal_requirement_id`
- `new_skill_invocation_proposal_id`
- `new_skill_proposal_decision_id`
- `new_skill_proposal_review_note_id`
- `new_skill_proposal_result_id`

## Service Behavior

`SkillProposalRouterService.propose_from_prompt` follows a proposal-only flow:

1. Create a `SkillProposalIntent`.
2. Extract deterministic requirements from prompt text and optional caller-provided root/path hints.
3. Generate a candidate `SkillInvocationProposal`.
4. Record a `SkillProposalDecision`.
5. Record review notes for missing input, unsupported operation, or explicit invocation requirements.
6. Return a `SkillProposalResult` and optional suggested CLI command preview.

The service may suggest a command such as:

```powershell
chanta-cli skill run skill:read_workspace_text_file --input-json "{\"root_path\":\"<ROOT_PATH>\",\"relative_path\":\"docs/example.md\"}"
```

The command is a preview only. The proposal router does not run it.

## CLI Surface

The CLI includes:

```powershell
chanta-cli skill propose "read file docs/example.md" --root <WORKSPACE_ROOT>
```

Options:

- `--root`
- `--path`
- `--recursive`
- `--json`

The command prints a proposal summary or JSON result. It does not call the explicit invocation execution path.

## OCEL Shape

Object types:

- `skill_proposal_intent`
- `skill_proposal_requirement`
- `skill_invocation_proposal`
- `skill_proposal_decision`
- `skill_proposal_review_note`
- `skill_proposal_result`

Events:

- `skill_proposal_intent_created`
- `skill_proposal_requirement_recorded`
- `skill_invocation_proposal_created`
- `skill_proposal_decision_recorded`
- `skill_proposal_review_note_recorded`
- `skill_proposal_result_recorded`
- `skill_proposal_rendered`

Relations:

- requirement belongs to intent
- proposal belongs to intent and requirement
- decision belongs to proposal and intent
- review note belongs to proposal and intent
- result includes proposals, decisions, and review notes

## Context History

New adapters use `source="skill_proposal"`:

- `skill_proposal_intents_to_history_entries`
- `skill_invocation_proposals_to_history_entries`
- `skill_proposal_results_to_history_entries`
- `skill_proposal_review_notes_to_history_entries`

Unsupported requests and missing input notes receive higher priority. Read-only proposal availability is medium priority.

## PIG / OCPX Report Support

The PIG skill usage summary includes:

- `skill_proposal_intent_count`
- `skill_proposal_requirement_count`
- `skill_invocation_proposal_count`
- `skill_proposal_decision_count`
- `skill_proposal_review_note_count`
- `skill_proposal_result_count`
- `skill_proposal_available_count`
- `skill_proposal_incomplete_count`
- `skill_proposal_unsupported_count`
- `skill_proposal_needs_review_count`
- `skill_proposal_by_skill_id`
- `skill_proposal_by_requested_operation`

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_skill_proposal_models.py tests\test_skill_proposal_router_service.py tests\test_skill_proposal_heuristics.py tests\test_skill_proposal_cli.py tests\test_skill_proposal_history_adapter.py tests\test_skill_proposal_ocel_shape.py tests\test_skill_proposal_boundaries.py
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

- read-file prompt proposes `skill:read_workspace_text_file`
- list-files prompt proposes `skill:list_workspace_files`
- markdown summary prompt proposes `skill:summarize_workspace_markdown`
- missing root/path produces incomplete proposal
- unsupported shell/network/write/MCP/plugin requests produce controlled unsupported results
- suggested CLI command is preview only
- CLI propose command does not run a skill
- no LLM classifier
- no shell/network/MCP/plugin/write execution
- no permission grant creation
- OCEL objects/events/relations
- ContextHistory adapters
- PIG/OCPX lightweight counts

## Known Limitations

- No proposal-to-execution approval flow yet.
- No permission-aware execution gate yet.
- No general autonomous tool routing.
- Heuristics are deterministic and intentionally conservative.

## Future Work

- v0.17.4: permission-aware read-only execution gate.
- v0.17.5: execution provenance envelope.
- Later: optional reviewed proposal-to-execution flow.

## Checklist

- [x] Public terminology uses generic Skill Proposal concepts.
- [x] Deterministic heuristics are implemented.
- [x] Read-only workspace skill proposals are supported.
- [x] Missing input creates incomplete proposal.
- [x] Unsupported operations are controlled.
- [x] Suggested CLI command is preview only.
- [x] No skill execution occurs.
- [x] No permission grant creation occurs.
- [x] No LLM/shell/network/MCP/plugin/write execution is added.
- [x] OCEL shape added.
- [x] ContextHistory adapter added.
- [x] PIG/OCPX lightweight report support added.
- [x] Public tests use dummy data only.
