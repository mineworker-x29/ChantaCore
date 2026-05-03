from pathlib import Path

from chanta_core.repo import RepoSymbolScanner
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def scanner(tmp_path: Path) -> RepoSymbolScanner:
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "app.py").write_text(
        "class App:\n    pass\n\nasync def run_app():\n    pass\n",
        encoding="utf-8",
    )
    (tmp_path / "src" / "view.ts").write_text(
        "export class View {}\nexport function render() {}\nconst state = {}\n",
        encoding="utf-8",
    )
    (tmp_path / "README.md").write_text("# Overview\n## Usage\n", encoding="utf-8")
    return RepoSymbolScanner(WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path)))


def test_scan_symbols_finds_python_js_markdown(tmp_path) -> None:
    symbols = scanner(tmp_path).scan_symbols()
    names = {item.symbol_name for item in symbols}

    assert {"App", "run_app", "View", "render", "state", "Overview", "Usage"} <= names
    assert {item.attrs["parser"] for item in symbols} == {"lightweight_regex"}


def test_find_definitions_light(tmp_path) -> None:
    symbols = scanner(tmp_path).find_definitions_light("render")

    assert len(symbols) == 1
    assert symbols[0].symbol_name == "render"
    assert symbols[0].symbol_kind == "function"
    assert symbols[0].attrs["parser"] == "lightweight_regex"
