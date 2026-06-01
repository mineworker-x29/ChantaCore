# v0.27.x Memory Candidate & Continuity

`v0.27.x` is the Memory Candidate & Continuity track.

This release line starts from the `v0.26.9` Workspace Agent Workbench Foundation
v1 handoff. It must use refs, summaries, evidence, event quality, trace
coverage, redaction metadata, approval records, command candidates, failure
cause refs, human intervention refs, PIG guidance refs, and OCEL/OCPX projections
as visible source material. It must not start from raw transcripts.

## Releases

- `v0.27.0` - Memory Candidate & Continuity Contract.
- `v0.27.1` - Memory Source / Ref Boundary.
- `v0.27.2` - Memory Candidate Extraction.
- `v0.27.3` - Memory Evidence Binder & Scoring.
- `v0.27.4` - Memory Promotion Gate.
- `v0.27.5` - Durable Memory Record & Registry.
- `v0.27.6` - Session Continuity Context Builder.
- `v0.27.7` - Continuity Injection Boundary.
- `v0.27.8` - Memory Audit / Update / Revoke / Forget.
- `v0.27.9` - Memory Candidate & Continuity Consolidation.

## Boundary

`v0.27.0` is contract-only. It declares the source boundary, candidate policy,
evidence policy, scoring policy, promotion gate policy, durable memory policy,
session continuity policy, continuity injection policy, audit, privacy,
governance, PIG guidance, safety boundary, release prerequisite policy, and the
full `v0.27.x` roadmap. It does not extract memory candidates, score memory,
promote memory, write persistent or durable memory, create session continuity
contexts, inject continuity, mutate persona or behavior policy, persist raw
transcripts or provider outputs as memory, treat PIG as memory, invoke providers,
execute commands, bypass safety gates, add external adapters, introduce
Schumpeter split, expose secrets or credentials, or use an LLM judge.

`v0.26.10` Release Hygiene / Governance Hardening is recommended before
implementation-heavy memory work and required before `v0.27.5` persistent memory
write or durable registry work.
`v0.27.1` creates source/ref-boundary artifacts only. It creates source category
catalogs, refs, bundles, registry views, eligibility rules/evaluations/decisions,
redaction views, quality reports, forbidden-source reports, and candidate
readiness boundaries. It does not create memory candidates, score memory,
promote memory, write persistent or durable memory, inject continuity, mutate
persona or behavior policy, invoke providers, execute commands, bypass safety
gates, implement external adapters, introduce Schumpeter split, expose raw
secrets or credentials, or use an LLM judge. The next step is `v0.27.2` Memory
Candidate Extraction.

`v0.27.2` creates memory candidates from eligible `v0.27.1` source refs. A
memory candidate is not memory. Candidate extraction is not scoring, promotion,
persistent memory write, durable memory write, registry update, or continuity
injection. Candidate claims remain sanitized and ref-supported; they are not
asserted truth. Candidate context is not runtime continuity injection. PIG
guidance may be attached as a signal, but PIG guidance is not memory and cannot
promote memory. The next step is `v0.27.3` Memory Evidence Binder & Scoring.

`v0.27.3` binds evidence and scores memory candidates. Evidence binding is not
promotion. Scoring is not promotion. High score is not automatic memory. Score is
evidence for the future `v0.27.4` promotion gate, not a gate result. Evidence
strength is not truth, contradiction check is not automatic deletion, and
privacy risk is not automatic rejection by itself. PIG guidance may inform
scoring but is not memory and cannot promote memory. `v0.27.3` may mark
candidates as scored, but it does not promote candidates, write persistent or
durable memory, update durable registry, inject continuity, mutate persona or
behavior policy, invoke providers, execute commands, bypass safety gates,
implement external adapters, introduce Schumpeter split, expose secrets, or use
an LLM judge as sole scoring authority. The next step is `v0.27.4` Memory
Promotion Gate.

`v0.27.4` records promotion gate decisions. Promotion gate is not durable memory
registry. Promotion decision is not persistent memory write. Promote decision is
authorization metadata for future durable memory, not memory itself. Reject
decision is not source deletion, defer decision is not silent memory storage,
mark-ephemeral is not durable memory, and mark-archive-only is not active memory.
High score cannot bypass the promotion gate and PIG guidance cannot promote
memory. `v0.27.4` may record promote/reject/defer/more-evidence/user-confirmation
and ephemeral/archive-only decisions, but it does not create durable memory
records, update durable registry, write persistent memory, inject continuity,
mutate persona or behavior policy, invoke providers, execute commands, bypass
safety gates, implement external adapters, introduce Schumpeter split, expose
secrets, or use an LLM judge as sole promotion authority. The next step is
`v0.27.5` Durable Memory Record & Registry.

`v0.27.5` creates the gated durable memory record and registry layer. Durable
memory record requires a prior promotion decision, but promote decision alone is
not durable memory. Durable memory registry is not persona and is not behavior
policy. Persistent memory write requires a write gate, including release hygiene
and runtime data hygiene gates. No write, blocked write, and dry-run are valid
outcomes. Durable records are refs-only, scoped, evidenced, versioned,
auditable, revocable, forgettable, and OCEL-visible. `v0.27.5` does not write
raw transcript/provider output/secret/credential memory, inject continuity,
mutate persona or behavior policy, treat PIG as memory authority, invoke
providers, execute commands, bypass safety gates, implement external adapters,
introduce Schumpeter split, or use an LLM judge as sole durable memory authority.
The next step is `v0.27.6` Session Continuity Context Builder.

`v0.27.6` builds refs-only session continuity context artifacts. Session
continuity context is not raw transcript replay. Continuity context pack is not
runtime injection. Continuity context item is not behavior override, memory
retrieval is not command execution, and relevance score is not authority. Stale
memory must be surfaced, contradictory memory must be surfaced, privacy-filtered
memory must remain filtered, and revoked/forgotten/expired/blocked memory must
not be used as active continuity context. `v0.27.6` may create source views,
eligibility rules, memory refs, relevance scores, recency/staleness warnings,
conflict reports, privacy filters, context items, context packs, previews,
audit trails, and build reports, but it does not inject continuity, mutate
runtime/session/policy surfaces, update/revoke/forget memory, write persistent
or durable memory, mutate persona or behavior policy, treat PIG as authority,
invoke providers, execute commands, bypass safety gates, implement external
adapters, introduce Schumpeter split, or use an LLM judge as sole continuity
authority. The next step is `v0.27.7` Continuity Injection Boundary.

`v0.27.7` defines the continuity injection boundary. Continuity injection
boundary is not runtime injection, injection preview is not applied context, and
injection bundle is not behavior override. Memory context is guidance, not
authority; explicit user instruction outranks memory; safety gate and permission
boundary must remain active. Contradictory memory must be surfaced, stale memory
must be warned, privacy-filtered memory must remain filtered, and memory must
not trigger provider invocation or command execution. `v0.27.7` may create
target catalogs, compatibility rules, eligibility evaluations, priority rules,
safety/permission rules, refs-only context bindings, future handoff bundles,
previews, decision records, boundary traces, and audit trails. It does not
perform runtime injection, mutate Default Agent, DecisionService, SkillRouter,
SafetyGate, PermissionPolicy, memory, persona, or behavior policy, replay raw
content, use PIG as authority, invoke providers, execute commands, mutate files,
bypass safety or permissions, implement external adapters, introduce Schumpeter
split, or use an LLM judge as sole injection authority. The next step is
`v0.27.8` Memory Audit / Update / Revoke / Forget.

`v0.27.8` implements memory lifecycle control. Memory review is not mutation,
memory update candidate is not update execution, revoke removes active use, and
forget removes active use and recallable memory content without deleting source
data by default. Archive is not active memory, expiration is not deletion,
conflict resolution must be recorded, no-op is a valid lifecycle decision, and
PIG guidance is not lifecycle authority. `v0.27.8` may create lifecycle
policies, source views, operation gates, review/update/supersede/revoke/forget
records, forget tombstones, archive/expiration records, conflict resolution
records, no-op decisions, registry update previews/records, audit trails, and
reports. It does not silently overwrite memory, perform unlogged deletion,
delete source data by default, restore raw transcript/provider output, mutate
persona or behavior policy, use PIG as authority, invoke providers, execute
commands, bypass safety, inject continuity, implement external adapters,
introduce Schumpeter split, or use an LLM judge as sole lifecycle authority.
The next step is `v0.27.9` Memory Candidate & Continuity Consolidation.

`v0.27.9` consolidates `v0.27.0` through `v0.27.8` into Memory Candidate &
Continuity Foundation v1. Consolidation is not new memory feature
implementation, Memory Foundation release readiness is not public alpha
readiness, and `v0.28` readiness is not `v0.28` implementation. Durable memory
registry is not persona, continuity context is not runtime injection, lifecycle
control is not silent mutation, and PIG guidance is not memory authority.
`v0.27.9` may create foundation snapshots, capability maps, coverage matrices,
safety/privacy/stage consolidation reports, process-intelligence feedback
reports, Default Agent readiness reports, release hygiene dependency reports,
`v0.28` readiness reports, public alpha handoff packets, release manifests, and
consolidation reports. It does not create new memory candidates, score or
promote memory, write durable memory, update durable registry, execute memory
lifecycle mutations, inject continuity, mutate Default Agent, DecisionService,
SkillRouter, SafetyGate, PermissionPolicy, persona, or behavior policy, replay
raw content, use PIG as memory authority, invoke providers, execute commands,
mutate files, bypass safety or permissions, implement external adapters,
introduce Schumpeter split, or use an LLM judge as sole consolidation authority.
The next step is `v0.28.0` Public Alpha / Schumpeter Split Preparation Contract.
