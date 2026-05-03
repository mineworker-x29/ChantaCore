from chanta_core.editing import (
    APPROVAL_PHRASE,
    EditProposalService,
    EditProposalStore,
    PatchApplicationService,
    PatchApplicationStore,
)
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.policy import ToolPolicy
from chanta_core.tools.request import ToolRequest
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def setup(tmp_path):
    (tmp_path / "app.py").write_text("old\n", encoding="utf-8")
    inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))
    proposal_store = EditProposalStore(tmp_path / "proposals.jsonl")
    proposal = EditProposalService(inspector, proposal_store).propose_text_replacement(
        target_path="app.py",
        proposed_text="new\n",
        title="Replace",
        rationale="Test",
    )
    patch_service = PatchApplicationService(
        workspace_inspector=inspector,
        proposal_store=proposal_store,
        patch_store=PatchApplicationStore(tmp_path / "patches.jsonl"),
    )
    return proposal, patch_service


def context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:patch-tool",
        session_id="session-patch-tool",
        agent_id="chanta_core_default",
    )


def request(proposal_id: str, approval_text: str = "", approved_by: str = "tester") -> ToolRequest:
    return ToolRequest.create(
        tool_id="tool:edit",
        operation="apply_approved_proposal",
        process_instance_id="process_instance:patch-tool",
        session_id="session-patch-tool",
        agent_id="chanta_core_default",
        input_attrs={
            "proposal_id": proposal_id,
            "approved_by": approved_by,
            "approval_text": approval_text,
        },
    )


def test_without_approval_text_does_not_execute(tmp_path) -> None:
    proposal, patch_service = setup(tmp_path)

    result = ToolDispatcher(patch_application_service=patch_service).dispatch(
        request(proposal.proposal_id),
        context(),
    )

    assert result.success is False
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "old\n"


def test_valid_approval_default_policy_still_does_not_write(tmp_path) -> None:
    proposal, patch_service = setup(tmp_path)

    result = ToolDispatcher(patch_application_service=patch_service).dispatch(
        request(proposal.proposal_id, APPROVAL_PHRASE),
        context(),
    )

    assert result.success is False
    assert result.output_attrs["requires_approval"] is True
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "old\n"


def test_valid_approval_and_allowed_policy_applies_patch(tmp_path) -> None:
    proposal, patch_service = setup(tmp_path)

    result = ToolDispatcher(
        policy=ToolPolicy(allow_approved_writes=True),
        patch_application_service=patch_service,
    ).dispatch(request(proposal.proposal_id, APPROVAL_PHRASE), context())

    assert result.success is True
    assert result.output_attrs["patch_application_id"].startswith("patch_application:")
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "new\n"
