from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.editing import EditProposalService, EditProposalStore
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "sample.txt"
        target.write_text("old\n", encoding="utf-8")
        service = EditProposalService(
            workspace_inspector=WorkspaceInspector(WorkspaceConfig(workspace_root=root)),
            store=EditProposalStore(root / "proposals.jsonl"),
        )
        proposal = service.propose_text_replacement(
            target_path="sample.txt",
            proposed_text="new\n",
            title="Sample replacement",
            rationale="Smoke test proposal.",
        )
        print(f"proposal_id={proposal.proposal_id}")
        print(f"target={proposal.target_path}")
        print(f"status={proposal.status}")
        print((proposal.proposed_diff or "")[:200])
        file_unchanged = target.read_text(encoding="utf-8") == "old\n"
        print(f"file_unchanged={file_unchanged}")


if __name__ == "__main__":
    main()
