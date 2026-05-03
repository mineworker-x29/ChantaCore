from dataclasses import dataclass

from chanta_core.editing import APPROVAL_PHRASE, EditProposalService, EditProposalStore
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
from chanta_core.skills.registry import SkillRegistry
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake"
    model: str = "fake"


class FakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(self, *_args, **_kwargs) -> str:
        return "unused"


def make_context(tmp_path, proposal_id: str, *, allow_approved_writes: bool):
    return SkillExecutionContext(
        process_instance_id="process_instance:apply-approved-patch",
        session_id="session-apply-approved-patch",
        agent_id="chanta_core_default",
        user_input="apply approved patch",
        system_prompt=None,
        context_attrs={
            "workspace_root": str(tmp_path),
            "edit_proposal_store_path": str(tmp_path / "proposals.jsonl"),
            "patch_application_store_path": str(tmp_path / "patches.jsonl"),
            "proposal_id": proposal_id,
            "approved_by": "test-operator",
            "approval_text": APPROVAL_PHRASE,
            "allow_approved_writes": allow_approved_writes,
        },
    )


def create_proposal(tmp_path) -> str:
    (tmp_path / "app.py").write_text("old\n", encoding="utf-8")
    store = EditProposalStore(tmp_path / "proposals.jsonl")
    service = EditProposalService(
        workspace_inspector=WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path)),
        store=store,
    )
    proposal = service.propose_text_replacement(
        target_path="app.py",
        proposed_text="new\n",
        title="Replace app.py",
        rationale="Skill approval path test.",
    )
    return proposal.proposal_id


def test_apply_approved_patch_skill_respects_policy_default(tmp_path) -> None:
    proposal_id = create_proposal(tmp_path)

    result = SkillExecutor(llm_client=FakeLLMClient()).execute(
        SkillRegistry().require("skill:apply_approved_patch"),
        make_context(tmp_path, proposal_id, allow_approved_writes=False),
    )

    assert result.success is False
    assert result.output_attrs["requires_approval"] is True
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "old\n"


def test_apply_approved_patch_skill_applies_only_when_policy_allows(tmp_path) -> None:
    proposal_id = create_proposal(tmp_path)

    result = SkillExecutor(llm_client=FakeLLMClient()).execute(
        SkillRegistry().require("skill:apply_approved_patch"),
        make_context(tmp_path, proposal_id, allow_approved_writes=True),
    )

    assert result.success is True
    assert result.output_attrs["patch_application_id"].startswith("patch_application:")
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "new\n"
