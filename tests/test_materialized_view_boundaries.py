import chanta_core.materialized_views.service as service_module
from chanta_core.materialized_views import render_generated_warning


FORBIDDEN_NAMES = [
    "import_memory_from_markdown",
    "load_memory_from_markdown_as_canonical",
    "sync_markdown_to_memory",
    "overwrite_ocel_from_markdown",
    "markdown_as_canonical_memory",
    "markdown_as_source_of_truth",
]


def test_no_direct_markdown_to_ocel_overwrite_functions_exist() -> None:
    for name in FORBIDDEN_NAMES:
        assert not hasattr(service_module, name)


def test_generated_warning_is_explicitly_non_canonical() -> None:
    warning = render_generated_warning(view_type="memory")

    assert "Generated materialized view" in warning
    assert "Canonical source: OCEL" in warning
    assert "not canonical memory" in warning
    assert "Do not treat edits to this file as canonical updates" in warning
