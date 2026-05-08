from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.workspace import WorkspaceReadService


def _service(tmp_path):
    store = OCELStore(tmp_path / "workspace_read.sqlite")
    service = WorkspaceReadService(trace_service=TraceService(ocel_store=store))
    root = service.register_read_root(tmp_path, root_name="test-root")
    return store, service, root


def test_workspace_text_read_inside_root_allowed(tmp_path) -> None:
    (tmp_path / "note.md").write_text("# Title\nBody", encoding="utf-8")
    _, service, root = _service(tmp_path)

    result = service.read_workspace_text_file(root=root, relative_path="note.md")

    assert result.denied is False
    assert result.content.replace("\r\n", "\n") == "# Title\nBody"
    assert result.content_hash


def test_workspace_read_rejects_absolute_and_traversal_paths(tmp_path) -> None:
    outside = tmp_path.parent / "outside.md"
    outside.write_text("outside", encoding="utf-8")
    _, service, root = _service(tmp_path)

    absolute = service.read_workspace_text_file(root=root, relative_path=str(outside))
    traversal = service.read_workspace_text_file(root=root, relative_path="../outside.md")

    assert absolute.denied is True
    assert traversal.denied is True
    assert traversal.violation_ids


def test_workspace_read_file_guards(tmp_path) -> None:
    (tmp_path / "bin.txt").write_bytes(b"a\x00b")
    (tmp_path / "large.txt").write_text("abcdef", encoding="utf-8")
    (tmp_path / "blocked.exe").write_text("text", encoding="utf-8")
    _, service, root = _service(tmp_path)

    binary = service.read_workspace_text_file(root=root, relative_path="bin.txt")
    large = service.read_workspace_text_file(root=root, relative_path="large.txt", max_bytes=3)
    extension = service.read_workspace_text_file(root=root, relative_path="blocked.exe")

    assert binary.denied is True
    assert large.denied is True
    assert extension.denied is True


def test_workspace_file_list_is_bounded(tmp_path) -> None:
    for name in ["a.md", "b.txt", "c.py"]:
        (tmp_path / name).write_text(name, encoding="utf-8")
    _, service, root = _service(tmp_path)

    result = service.list_workspace_files(root=root, max_results=2)

    assert result.total_entries == 2
    assert result.truncated is True
    assert all("relative_path" in entry for entry in result.entries)


def test_markdown_summary_is_deterministic_and_non_llm(tmp_path) -> None:
    (tmp_path / "doc.md").write_text("# Main\n\n## Part\nContent", encoding="utf-8")
    _, service, root = _service(tmp_path)

    result = service.summarize_workspace_markdown(root=root, relative_path="doc.md")

    assert result.denied is False
    assert result.title == "Main"
    assert result.heading_outline == ["# Main", "## Part"]
    assert "Title: Main" in result.summary
    assert result.result_attrs["uses_llm"] is False
