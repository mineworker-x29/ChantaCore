# v0.44.0 ULW Notepad

Skills selected:
- omo:ulw-loop: requested explicitly; used for evidence-bound delivery workflow.
- omo:programming: Python files will be created/edited; Python reference read before edits.
- omo:lsp: changed Python files need diagnostics if server is available.
- omo:review-work: significant implementation; final review gate required after implementation.

Tier: HEAVY.
Justification: new contract module/domain model and safety/permissions boundary for controlled workspace read, plus TUI command surface and docs.

Success criteria:
1. Contract/data/document surface defines v0.44.0 design-only controlled workspace read, PI observation, OCEL/OCPM-ready export, baseline diagnostics, and PI-RD-001 while keeping actual read/search/shell/git/edit/provider/subagent/memory/production flags closed.
2. Tests prove design contracts, forbidden runtime patterns, and integrated document requirements.
3. TUI user surface shows workspace/observation/research/v044 commands as preview/not opened and does not perform actual reads.
4. Regression tests requested by minero are run where present; missing tests are reported.
5. Manual acceptance is driven through the TUI or a faithful CLI/tmux surface and captured.

ULW CLI status: checking cached CLI after PATH returned ULW_MISSING.

Evidence plan:
- RED: pytest tests/test_v0440_controlled_workspace_read_design_contract.py before implementation, captured to .omo/ulw-loop/evidence/v0440-red.txt.
- GREEN: targeted test and requested regression outputs captured under .omo/ulw-loop/evidence/.
- Manual QA: tmux transcript or equivalent CLI/TUI transcript captured under .omo/ulw-loop/evidence/v0440-manual-tui.txt.
- Forbidden scan: rg patterns captured under .omo/ulw-loop/evidence/v0440-forbidden-scan.txt.
