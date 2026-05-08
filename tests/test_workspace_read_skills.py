from dataclasses import dataclass

from chanta_core.ocel.store import OCELStore
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
from chanta_core.skills.registry import SkillRegistry
from chanta_core.traces.trace_service import TraceService


@dataclass(frozen=True)
class _Settings:
    provider: str = "fake"
    model: str = "fake"


class _LLM:
    settings = _Settings()


def _context(tmp_path, relative_path=".") -> SkillExecutionContext:
    return SkillExecutionContext(
        process_instance_id="process_instance:workspace-read",
        session_id="session:workspace-read",
        agent_id="agent:test",
        user_input="workspace read",
        system_prompt=None,
        context_attrs={"root_path": str(tmp_path), "relative_path": relative_path},
    )


def test_workspace_read_skills_return_structured_output(tmp_path) -> None:
    (tmp_path / "doc.md").write_text("# Main\nBody", encoding="utf-8")
    store = OCELStore(tmp_path / "skills.sqlite")
    executor = SkillExecutor(llm_client=_LLM(), trace_service=TraceService(ocel_store=store))
    registry = SkillRegistry()

    listed = executor.execute(registry.require("skill:list_workspace_files"), _context(tmp_path))
    read = executor.execute(registry.require("skill:read_workspace_text_file"), _context(tmp_path, "doc.md"))
    summary = executor.execute(registry.require("skill:summarize_workspace_markdown"), _context(tmp_path, "doc.md"))

    assert listed.success is True
    assert listed.output_attrs["entries"]
    assert read.success is True
    assert read.output_attrs["content"].replace("\r\n", "\n") == "# Main\nBody"
    assert summary.success is True
    assert summary.output_attrs["title"] == "Main"
    assert summary.output_attrs["result_attrs"]["uses_llm"] is False
    assert store.fetch_objects_by_type("workspace_read_root")
