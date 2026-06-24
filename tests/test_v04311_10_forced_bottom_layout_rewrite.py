from pathlib import Path

import pytest

from chanta_core.schumpeter_tui.display_width import assert_v0439_lines_within_width
from chanta_core.schumpeter_tui.fullscreen import create_v04311_textual_app, render_v04311_text_snapshot
from chanta_core.schumpeter_tui.testing.fake_runtime_adapter import V04311FakeRuntimeAdapter


ROOT = Path(__file__).resolve().parents[1]
FULLSCREEN_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "fullscreen.py"
STYLE_PATH = ROOT / "src" / "chanta_core" / "schumpeter_tui" / "styles" / "schumpeter.tcss"
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.11.10_forced_bottom_layout_rewrite_restore.md"
BOTTOM_FILES = (FULLSCREEN_PATH, STYLE_PATH)


def _bottom(widget) -> int:
    return widget.region.y + widget.region.height


async def _assert_bottom_geometry(pilot) -> None:
    await pilot.pause()
    input_region = pilot.app.query_one("#input-region")
    input_widget = pilot.app.query_one("#main-input")
    status_region = pilot.app.query_one("#status-region")
    assert _bottom(input_region) <= status_region.region.y
    assert input_widget.region.y >= input_region.region.y
    assert _bottom(input_widget) <= _bottom(input_region)
    assert _bottom(input_widget) <= status_region.region.y - 1


def test_builtin_textual_footer_not_mounted():
    text = FULLSCREEN_PATH.read_text(encoding="utf-8")
    assert "Footer(" not in text
    assert "yield Footer" not in text


def test_status_region_is_custom_normal_flow_widget():
    text = FULLSCREEN_PATH.read_text(encoding="utf-8")
    assert 'with Vertical(id="status-region")' in text
    assert 'id="status-bar"' in text


def test_status_region_does_not_use_dock_bottom():
    css = STYLE_PATH.read_text(encoding="utf-8")
    status_block = css[css.index("#status-region") : css.index("#status-bar")]
    assert "dock:" not in status_block
    assert "bottom" not in status_block


@pytest.mark.anyio
async def test_input_region_and_status_region_are_siblings_in_vertical_stack():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test(size=(120, 36)) as pilot:
        root = pilot.app.query_one("#app-root")
        child_ids = [child.id for child in root.children]
        assert child_ids == ["main-body", "palette-region", "help-modal", "about-modal", "input-region", "status-region"]


@pytest.mark.anyio
async def test_palette_region_above_input_region():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test(size=(120, 36)) as pilot:
        root = pilot.app.query_one("#app-root")
        child_ids = [child.id for child in root.children]
        assert child_ids.index("palette-region") < child_ids.index("input-region")


@pytest.mark.anyio
async def test_input_region_above_status_region():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test(size=(120, 36)) as pilot:
        input_region = pilot.app.query_one("#input-region")
        status_region = pilot.app.query_one("#status-region")
        assert _bottom(input_region) <= status_region.region.y


def test_input_region_min_height_at_least_four():
    css = STYLE_PATH.read_text(encoding="utf-8")
    input_block = css[css.index("#input-region") : css.index("#main-input")]
    assert "height: 5" in input_block
    assert "min-height: 5" in input_block


def test_input_widget_height_fits_border_and_cursor():
    css = STYLE_PATH.read_text(encoding="utf-8")
    input_block = css[css.index("#main-input") : css.index("#status-region")]
    assert "height: 3" in input_block
    assert "min-height: 3" in input_block
    assert "max-height: 3" in input_block


@pytest.mark.anyio
async def test_input_widget_bottom_above_status_top_with_clearance():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test(size=(120, 36)) as pilot:
        await _assert_bottom_geometry(pilot)


@pytest.mark.anyio
async def test_status_line_never_overlaps_input_region():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test(size=(120, 36)) as pilot:
        input_region = pilot.app.query_one("#input-region")
        status_region = pilot.app.query_one("#status-region")
        assert input_region.region.y != status_region.region.y
        assert _bottom(input_region) <= status_region.region.y


def test_no_negative_margin_in_bottom_layout_css():
    css = STYLE_PATH.read_text(encoding="utf-8")
    assert "margin-top: -" not in css
    assert "margin: -" not in css


def test_no_absolute_positioning_for_input_status_or_palette():
    css = STYLE_PATH.read_text(encoding="utf-8")
    for selector in ("#palette-region", "#input-region", "#main-input", "#status-region"):
        start = css.index(selector)
        next_start = min((css.find("\n#", start + 1) if css.find("\n#", start + 1) != -1 else len(css)), len(css))
        block = css[start:next_start]
        assert "position: absolute" not in block
        assert "dock:" not in block
        assert "offset-y" not in block


def test_input_text_visible_at_height_42():
    result = render_v04311_text_snapshot(120, 42, input_text="넌 누구야")
    assert "넌 누구야" in result.rendered_text


def test_input_text_visible_at_height_36():
    result = render_v04311_text_snapshot(120, 36, input_text="넌 누구야")
    assert "넌 누구야" in result.rendered_text


def test_input_text_visible_at_height_32():
    result = render_v04311_text_snapshot(120, 32, input_text="넌 누구야")
    assert "넌 누구야" in result.rendered_text


def test_input_text_visible_at_height_28():
    result = render_v04311_text_snapshot(120, 28, input_text="넌 누구야")
    assert "넌 누구야" in result.rendered_text


def test_input_text_visible_at_height_24():
    result = render_v04311_text_snapshot(80, 24, input_text="넌 누구야")
    assert "넌 누구야" in result.rendered_text


@pytest.mark.anyio
async def test_korean_input_visible_and_not_clipped():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test(size=(80, 24)) as pilot:
        input_widget = pilot.app.query_one("#main-input")
        input_widget.value = "넌 누구야"
        await _assert_bottom_geometry(pilot)
        assert input_widget.value == "넌 누구야"


@pytest.mark.anyio
async def test_palette_open_preserves_input_visibility():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test(size=(120, 36)) as pilot:
        pilot.app.action_toggle_palette()
        await _assert_bottom_geometry(pilot)
        assert not pilot.app.query_one("#slash-palette").has_class("hidden")


@pytest.mark.anyio
async def test_palette_filter_preserves_input_visibility():
    app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
    async with app.run_test(size=(120, 36)) as pilot:
        input_widget = pilot.app.query_one("#main-input")
        input_widget.value = "/s"
        await _assert_bottom_geometry(pilot)
        assert "/summary" in pilot.app.palette_plain


@pytest.mark.anyio
async def test_resize_preserves_input_status_separation():
    for height in (42, 36, 32, 28, 24):
        app = create_v04311_textual_app(V04311FakeRuntimeAdapter())
        async with app.run_test(size=(120, height)) as pilot:
            await _assert_bottom_geometry(pilot)


def test_snapshot_bottom_order_palette_input_status():
    result = render_v04311_text_snapshot(120, 36, include_palette=True, input_text="/s")
    rendered = result.rendered_text
    assert rendered.index("Commands") < rendered.index("InputRegion") < rendered.index("StatusRegion")


def test_snapshot_has_input_clearance_before_status():
    result = render_v04311_text_snapshot(80, 24, input_text="넌 누구야")
    lines = result.rendered_text.splitlines()
    input_line = next(index for index, line in enumerate(lines) if "넌 누구야" in line)
    status_line = next(index for index, line in enumerate(lines) if "StatusRegion" in line)
    assert status_line - input_line >= 2
    assert assert_v0439_lines_within_width(result.rendered_text, 80)


def test_no_provider_shell_repo_workspace_memory_side_effects_from_layout():
    result = render_v04311_text_snapshot(120, 36, include_palette=True, input_text="/s")
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.production_certified is False


def test_no_forbidden_runtime_call_patterns():
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
        "provider tool call",
        "function call",
        "workspace read",
        "repo search",
        "memory mutation",
        "CORE_MEMORY",
        "production_certified=True",
    )
    for path in BOTTOM_FILES:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text, f"{pattern} found in {path}"


def test_documentation_exists_with_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in (
        "Restore Purpose",
        "User-Observed Continued Input/Footer Failure",
        "Why Previous Patch Failed",
        "v0.43.11.10 Goal",
        "Bottom Layout Tree",
        "Footer Removal",
        "InputRegion / StatusRegion Geometry Contract",
        "Palette Anchoring Contract",
        "Widget Region Tests",
        "Snapshot Acceptance",
        "Manual Acceptance",
        "Safety Boundary",
        "Withdrawal Conditions",
        "v0.44 Gate Recommendation",
        "Copy-Paste Restore Prompt",
    ):
        assert f"## {section}" in text
