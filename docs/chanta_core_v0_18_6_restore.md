# ChantaCore v0.18.6 Restore Notes

Version name: ChantaCore v0.18.6 - Internal Skill Onboarding Contract

## Scope

Internal Skill Onboarding defines the contract for future internal skills. It is a diagnostic and conformance layer for describing a capability before it can be treated as a proper internal skill.

A skill is not fully integrated unless it has all of these contracts:

- Skill Descriptor
- Skill Input Contract
- Skill Output Contract
- Skill Risk Profile
- Skill Gate Contract
- Skill Observability Contract

## Mandatory Contract Rules

- OCEL observability is mandatory.
- Execution envelope support is mandatory.
- PIG/OCPX visibility is mandatory.
- Audit visibility and workbench visibility must be declared.
- Accepted onboarding results remain disabled by default.

## Boundaries

- v0.18.6 does not execute skills during onboarding.
- v0.18.6 does not enable write, shell, network, MCP, or plugin skills.
- v0.18.6 does not dynamically register executable tools.
- v0.18.6 does not create permission grants.
- v0.18.6 does not mutate ToolDispatcher or SkillExecutor dynamically.

## CLI

The diagnostic CLI surface is:

- `chanta-cli skills onboarding list`
- `chanta-cli skills onboarding show <skill_id>`
- `chanta-cli skills onboarding check --skill-id <skill_id>`
- `chanta-cli skills onboarding validate --descriptor-json-file <path>`

These commands inspect descriptors and validate onboarding contracts. They do not execute skills, register runtime tools, or grant permissions.

## Future Work

- v0.19.0 read-only internal skill pack.
- Internal skill registry view.
- Skill conformance and smoke tests.

No private content is included in this public restore note.
