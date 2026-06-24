from pathlib import Path

import pytest

from chanta_core.schumpeter_tui.display_width import assert_v0439_lines_within_width
from chanta_core.schumpeter_tui.fullscreen import create_v04311_textual_app, render_v04311_text_snapshot
from chanta_core.schumpeter_tui.testing.fake_runtime_adapter import V04311FakeRuntimeAdapter


ROOT = Path(__file__).resolve().parents[1]
FULLSCREEN_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "fullscreen.py"
STYLE_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "styles" / "schumpeter.tcss"
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.11.9_tui_input_footer_cursor_clearance_restore.md"


def test_bottom_regions_are_declared_in_compose_order():
    text = FULLSCREEN_PATH.read_text(encoding="utf-8")
    palette = text.index('id="palette-region"')
    input_region = text.index('id="input-region"')
    status = text.index('id="status-region"')
    assert palette < input_region < status
    assert 'id="main-input"' in text
    assert 'id="status-bar"' in text


def test_tcss_reserves_separate_rows_for_palette_input_and_status():
    text = STYLE_PATH.read_text(encoding="utf-8")
    assert "#palette-region" in text
    assert "#input-region" in text
    assert "height: 5" in text
    assert "min-height: 5" in text
    assert "#status-region" in text
    assert "height: 1" in text
    assert "#main-input" in text


def test_snapshot_shows_input_and_status_as_separate_regions():
    rendered = render_v04311_text_snapshot(140, 42, demo_conversation=True).rendered_text
    assert "InputRegion" in rendered
    assert "StatusRegion" in rendered
    assert rendered.index("InputRegion") < rendered.index("StatusRegion")
    assert "Ask Schumpeter anything" in rendered


def test_responsive_snapshots_keep_input_status_and_width_safe():
    for width, height in ((140, 42), (110, 32), (80, 24)):
        result = render_v04311_text_snapshot(width, height, demo_conversation=True)
        assert result.contains_input is True
        assert result.contains_status_bar is True
        assert "InputRegion" in result.rendered_text
        assert "StatusRegion" in result.rendered_text
        assert assert_v0439_lines_within_width(result.rendered_text, width)


@pytest.mark.anyio
async def test_textual_tree_mounts_bottom_regions_as_siblings_in_order():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        root = pilot.app.query_one("#app-root")
        child_ids = [child.id for child in root.children]
        assert child_ids.index("main-body") < child_ids.index("palette-region")
        assert child_ids.index("palette-region") < child_ids.index("input-region")
        assert child_ids.index("input-region") < child_ids.index("status-region")


@pytest.mark.anyio
async def test_korean_input_text_remains_in_input_widget_with_status_separate():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "넌 누구야"
        await pilot.pause()
        assert input_bar.value == "넌 누구야"
        assert pilot.app.query_one("#input-region") is not None
        assert pilot.app.query_one("#status-region") is not None
        assert pilot.app.query_one("#status-bar") is not None


@pytest.mark.anyio
async def test_command_palette_region_stays_above_input_region_when_open():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test() as pilot:
        input_bar = pilot.app.query_one("#main-input")
        input_bar.focus()
        input_bar.value = "/"
        await pilot.pause()
        assert not pilot.app.query_one("#slash-palette").has_class("hidden")
        root = pilot.app.query_one("#app-root")
        child_ids = [child.id for child in root.children]
        assert child_ids.index("palette-region") < child_ids.index("input-region")
        assert pilot.app.input_visible_with_palette is True


def test_rendering_side_effect_flags_remain_closed():
    result = render_v04311_text_snapshot(140, 42, demo_conversation=True)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.production_certified is False


def test_no_forbidden_runtime_call_patterns_in_layout_hotfix_files():
    forbidden = (
        "requests",
        "httpx",
        "urllib",
        "socket",
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "git status",
        "os.walk",
        "Path.rglob",
        ".rglob(",
        "CORE_MEMORY",
    )
    for path in (FULLSCREEN_PATH, STYLE_PATH):
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text, f"{pattern} found in {path}"


def test_documentation_exists_with_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in (
        "Restore Purpose",
        "User-Observed Input Clearance Problem",
        "v0.43.11.9 Goal",
        "Bottom Layout Contract",
        "Command Palette Region",
        "Input Region",
        "Footer Status Region",
        "Cursor Clearance",
        "Snapshot Tests",
        "Manual Acceptance",
        "Safety Boundary",
        "Withdrawal Conditions",
        "v0.44 Gate Recommendation",
        "Copy-Paste Restore Prompt",
    ):
        assert f"## {section}" in text
