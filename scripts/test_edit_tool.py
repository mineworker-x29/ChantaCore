from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.editing import EditProposalService, EditProposalStore
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "sample.txt"
        target.write_text("old\n", encoding="utf-8")
        inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=root))
        edit_service = EditProposalService(
            workspace_inspector=inspector,
            store=EditProposalStore(root / "proposals.jsonl"),
        )
        context = ToolExecutionContext(
            process_instance_id="process_instance:script-edit-tool",
            session_id="script-edit-tool",
            agent_id="chanta_core_default",
        )
        result = ToolDispatcher(edit_service=edit_service).dispatch(
            ToolRequest.create(
                tool_id="tool:edit",
                operation="propose_text_replacement",
                process_instance_id=context.process_instance_id,
                session_id=context.session_id,
                agent_id=context.agent_id,
                input_attrs={
                    "target_path": "sample.txt",
                    "proposed_text": "new\n",
                    "title": "Sample replacement",
                    "rationale": "Tool smoke test proposal.",
                },
            ),
            context,
        )
        print(f"success={result.success}")
        print(f"proposal_id={result.output_attrs.get('proposal_id')}")
        file_unchanged = target.read_text(encoding="utf-8") == "old\n"
        print(f"file_unchanged={file_unchanged}")


if __name__ == "__main__":
    main()
