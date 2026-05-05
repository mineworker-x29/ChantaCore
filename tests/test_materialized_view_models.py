from chanta_core.materialized_views import (
    MaterializedView,
    MaterializedViewInputSnapshot,
    MaterializedViewRenderResult,
    hash_content,
    new_materialized_view_id,
)


def test_materialized_view_id_prefix_and_hash() -> None:
    assert new_materialized_view_id().startswith("materialized_view:")
    assert hash_content("view") == hash_content("view")


def test_materialized_view_to_dict_canonical_false() -> None:
    view = MaterializedView(
        view_id="materialized_view:test",
        view_type="memory",
        title="Memory",
        target_path=".chanta/MEMORY.md",
        content="content",
        content_hash=hash_content("content"),
        generated_at="2026-05-05T00:00:00Z",
        source_kind="ocel_materialized_projection",
        canonical=False,
    )

    data = view.to_dict()

    assert data["canonical"] is False
    assert data["content_hash"] == hash_content("content")


def test_input_snapshot_and_render_result_to_dict() -> None:
    snapshot = MaterializedViewInputSnapshot(snapshot_attrs={"source": "test"})
    view = MaterializedView(
        view_id="materialized_view:test",
        view_type="memory",
        title="Memory",
        target_path=".chanta/MEMORY.md",
        content="content",
        content_hash=hash_content("content"),
        generated_at="2026-05-05T00:00:00Z",
        source_kind="ocel_materialized_projection",
        canonical=False,
    )
    result = MaterializedViewRenderResult(
        view=view,
        written=False,
        target_path=view.target_path,
        skipped_reason="skip",
    )

    assert snapshot.to_dict()["snapshot_attrs"] == {"source": "test"}
    assert result.to_dict()["skipped_reason"] == "skip"
