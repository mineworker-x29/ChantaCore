# ChantaCore v0.16.4 Restore Notes

Version: 0.16.4

Name: Personal / Overlay Validation & Conformance

## Purpose

ChantaCore v0.16.4 adds a generic Personal Conformance layer. The layer performs deterministic structural checks over Personal Source, Personal Overlay, Personal Mode Loadout, Personal Runtime Binding, and prompt projection artifacts.

The conformance layer is diagnostic only. It records contracts, rules, runs, findings, and results. It does not repair artifacts, activate profiles, import sources into canonical persona records, grant permissions, or change runtime behavior.

## Product Boundary

The public ChantaCore surface remains generic. The public concepts are Personal Directory, Personal Source, Personal Profile, Personal Overlay, Personal Projection, Personal Mode, Personal Runtime Binding, and Personal Conformance.

A Personal Directory may exist outside the repository and may contain local user material, but public ChantaCore code and docs must not depend on a specific local path or specific private identity. Capability truth remains authoritative: personal text can describe preferences and boundaries, but it cannot create runtime capabilities.

## Added Models

`PersonalConformanceContract` defines a named conformance contract. It records contract type, description, lifecycle status, severity, timestamps, and extra attributes.

`PersonalConformanceRule` defines one structural rule under a contract. Rules include a rule type, description, severity, required flag, expected value, and status.

`PersonalConformanceRun` records a single conformance evaluation run against a target kind and optional target reference.

`PersonalConformanceFinding` records the result of one rule check. Findings can pass, fail, warn, skip, remain inconclusive, or error. Evidence references are metadata only.

`PersonalConformanceResult` summarizes a run. It records passed, failed, warning, and skipped finding IDs, plus optional score and confidence values bounded to `0.0..1.0`.

## Default Rule Set

The default rule set covers:

- Personal Directory must not be inside a public repo.
- `letters/` must not be used as source.
- `messages/` must not be used as source.
- `archive/` must not be used as source.
- Public artifacts must not contain configured private terms.
- Source body content must not be used as prompt projection blocks.
- Markdown remains staged input and is not canonical persona.
- Canonical import must remain disabled for staged candidates.
- Canonical activation must remain disabled for mode drafts.
- Runtime binding must be descriptive and non-executing.
- Personal modes must not grant capabilities.
- Runtime capability truth must override personal claims.
- JSON Lines personal stores must not be introduced.
- Prompt projections must remain bounded.
- Private paths should be redacted in public-facing artifacts.
- Mode boundaries should be present.
- Private loadouts should include a privacy boundary.
- Source exclusion policy should include excluded local areas.

## Service Behavior

`PersonalConformanceService` provides:

- contract and rule registration;
- default rule registration;
- run lifecycle recording;
- finding and result recording;
- source candidate conformance checks;
- overlay manifest and projection reference checks;
- mode loadout checks;
- runtime binding checks;
- supplied public artifact privacy scans.

All checks are deterministic and structural. The service does not call an LLM, does not execute tools, does not use network access, and does not mutate checked objects.

## Evaluation Scope

Personal Source checks verify staged import boundaries. Candidates must keep canonical import disabled. Source references from `letters/`, `messages/`, or `archive/` fail boundary checks. Markdown sources remain readable staged input only.

Personal Overlay checks verify exclusion policy, prompt-safe projection references, and projection directory boundaries. Prompt projection refs should come from reviewed overlay/profile/loadout artifacts, not raw source bodies.

Personal Mode Loadout checks verify mode boundary presence, privacy boundary presence for private loadouts, capability boundary blocks, and the runtime capability override statement.

Personal Runtime Binding checks verify descriptive binding records. Activation scopes must not imply active runtime tool execution. Capability bindings are metadata unless the actual runtime capability profile says otherwise.

Public artifact privacy checks operate only on supplied paths or text snippets. They do not shell out, walk the repository by themselves, or use hidden runtime state.

## OCEL Shape

New OCEL object types:

- `personal_conformance_contract`
- `personal_conformance_rule`
- `personal_conformance_run`
- `personal_conformance_finding`
- `personal_conformance_result`

New OCEL events:

- `personal_conformance_contract_registered`
- `personal_conformance_rule_registered`
- `personal_conformance_run_started`
- `personal_conformance_run_completed`
- `personal_conformance_run_failed`
- `personal_conformance_run_skipped`
- `personal_conformance_finding_recorded`
- `personal_conformance_result_recorded`

Relations connect rules to contracts, runs to contracts, findings to runs and rules, and results to runs and contracts.

## Context History

Two adapters project conformance artifacts into context history:

- `personal_conformance_findings_to_history_entries`
- `personal_conformance_results_to_history_entries`

Failed and error findings receive high priority. Warning findings receive medium priority. Passing entries remain lower priority.

## PIG / OCPX Reporting

The Persona Projection section of the PIG report now includes lightweight Personal Conformance counts:

- contract, rule, run, finding, and result counts;
- passed, failed, needs-review, and inconclusive result counts;
- failed and warning finding counts;
- findings by rule type;
- average conformance score when available.

The report stays diagnostic and does not expose private paths or source bodies.

## Restore Checklist

After restoring this version, verify:

- package version is `0.16.4`;
- `PersonalConformanceService` imports from `chanta_core.persona`;
- default rules register successfully;
- source candidate checks keep canonical import disabled;
- overlay checks reject raw source prompt projection refs;
- mode loadout checks require capability boundary semantics;
- runtime binding checks remain non-executing;
- PIG report includes Personal Conformance counts;
- tests pass with public-safe dummy content only.

## Future Work

Likely next steps:

- operational smoke tests for a representative local Personal Directory;
- an optional read-only CLI conformance command;
- stricter conformance policy profiles;
- deeper mode/runtime conformance checks when controlled runtime mode activation is designed.
