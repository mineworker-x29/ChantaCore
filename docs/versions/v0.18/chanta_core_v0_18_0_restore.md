# ChantaCore v0.18.0 Restore Document

Version name: ChantaCore v0.18.0 - Skill Proposal Review Contract

## Purpose

v0.18.0 adds a generic Skill Proposal Review Contract. It turns a `SkillInvocationProposal` into a human-in-the-loop review workflow state.

The review layer does not execute proposals. It does not call explicit invocation, does not call the read-only execution gate, and does not create permission grants.

## Scope

Implemented public concepts:

- Skill Proposal Review Contract
- Skill Proposal Review Request
- Skill Proposal Review Decision
- Skill Proposal Review Finding
- Skill Proposal Review Result
- Skill Proposal Review Service
- CLI review surface for proposal JSON files
- OCEL object/event/relation support
- ContextHistory adapter support
- PIG/OCPX lightweight report counts

## Decisions

Supported review decisions:

- `approved_for_explicit_invocation`
- `rejected`
- `needs_more_input`
- `revise_proposal`
- `no_action`
- `needs_review`
- `error`

CLI aliases include `approve`, `reject`, `revise`, `no-action`, `more-input`, and `needs-review`.

## Default Contract

The default contract supports only read-only workspace proposal skills:

- `skill:list_workspace_files`
- `skill:read_workspace_text_file`
- `skill:summarize_workspace_markdown`

Denied categories:

- `write`
- `shell`
- `network`
- `mcp`
- `plugin`
- `external_capability`

The default contract requires an explicit reviewer and requires a reason for approval.

## Bridge Candidate Boundary

An approved review result may set `bridge_candidate=True` only when the proposal is complete and uses a supported read-only skill.

This is metadata only. It is not execution. The actual reviewed proposal-to-execution bridge is deferred to a future version, expected as v0.18.1.

Missing input, rejected, no-action, revise, needs-review, unsupported, and error outcomes set `bridge_candidate=False`.

## CLI

Proposal persistence is not yet available. The testable CLI path is:

```powershell
chanta-cli skill review --from-proposal-json-file proposal.json --decision approve --reason "complete read-only proposal"
```

If only a proposal id is supplied, the CLI returns a controlled diagnostic explaining that proposal persistence is not available.

## OCEL Shape

Object types:

- `skill_proposal_review_contract`
- `skill_proposal_review_request`
- `skill_proposal_review_decision`
- `skill_proposal_review_finding`
- `skill_proposal_review_result`

Events:

- `skill_proposal_review_contract_registered`
- `skill_proposal_review_requested`
- `skill_proposal_review_decision_recorded`
- `skill_proposal_review_finding_recorded`
- `skill_proposal_review_result_recorded`
- `skill_proposal_review_approved`
- `skill_proposal_review_rejected`
- `skill_proposal_review_no_action_selected`
- `skill_proposal_review_needs_more_input`

Relations include request-to-proposal, request-to-contract, decision-to-request, result-to-request, result-to-decision, and finding-to-request links.

## PIG/OCPX Report Keys

Added skill usage summary keys:

- `skill_proposal_review_contract_count`
- `skill_proposal_review_request_count`
- `skill_proposal_review_decision_count`
- `skill_proposal_review_finding_count`
- `skill_proposal_review_result_count`
- `skill_proposal_review_approved_count`
- `skill_proposal_review_rejected_count`
- `skill_proposal_review_no_action_count`
- `skill_proposal_review_needs_more_input_count`
- `skill_proposal_review_bridge_candidate_count`
- `skill_proposal_review_by_skill_id`
- `skill_proposal_review_by_decision`

## Boundary Guarantees

- Review does not execute skills.
- Review does not call `ExplicitSkillInvocationService`.
- Review does not call `SkillExecutionGateService`.
- Review does not create permission grants.
- Review does not infer execution from natural language.
- Review does not support write, shell, network, MCP, plugin, or external capability execution.
- Review does not use an LLM classifier.
- Review does not mutate `ToolDispatcher`.
- Review does not mutate `SkillExecutor`.
- Review does not create a JSONL canonical review store.
- Review does not include private content.

## Restore Procedure

1. Install the package in editable mode:

```powershell
.\.venv\Scripts\python.exe -m pip install -e .
```

2. Run targeted tests:

```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_skill_proposal_review_models.py tests\test_skill_proposal_review_service.py tests\test_skill_proposal_review_cli.py tests\test_skill_proposal_review_history_adapter.py tests\test_skill_proposal_review_ocel_shape.py tests\test_skill_proposal_review_boundaries.py
```

3. Run the full suite:

```powershell
.\.venv\Scripts\python.exe -m pytest
```

## Known Limitations

- No reviewed proposal-to-execution bridge exists yet.
- No automatic execution exists.
- No proposal persistence store exists yet.
- No write, shell, network, MCP, plugin, or external capability execution exists in this review layer.

## Checklist

- [x] SkillProposalReview models added.
- [x] SkillProposalReviewService added.
- [x] Default read-only review contract added.
- [x] approve/reject/revise/no_action/needs_more_input decisions covered.
- [x] Approved complete read-only proposals become bridge candidates only.
- [x] Missing input blocks bridge candidates.
- [x] Unsupported skill categories are rejected.
- [x] No explicit invocation or execution gate call is made.
- [x] OCEL support added.
- [x] ContextHistory adapter support added.
- [x] PIG/OCPX counts added.
- [x] CLI review surface added for proposal JSON files.
- [x] Public-safe tests added.
