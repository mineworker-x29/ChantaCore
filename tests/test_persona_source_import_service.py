from chanta_core.persona import (
    PersonaSourceStagedImportService,
    detect_source_type,
    hash_text,
    preview_text,
    strip_html_to_text,
)


def test_registers_md_txt_and_html_sources() -> None:
    service = PersonaSourceStagedImportService()

    md = service.register_source_from_text(
        source_name="profile.md",
        text="# Identity\n- identity: public dummy assistant",
        source_ref="profile.md",
        media_type="text/markdown",
    )
    txt = service.register_source_from_text(
        source_name="profile.txt",
        text="role: answer with care",
        source_ref="profile.txt",
        media_type="text/plain",
    )
    html = service.register_source_from_text(
        source_name="profile.html",
        text="<h1>Safety</h1><p>Do not auto activate.</p>",
        source_ref="profile.html",
        media_type="text/html",
    )

    assert md.source_type == "markdown"
    assert txt.source_type == "text"
    assert html.source_type == "html"
    assert "Safety" in html.content_preview
    assert "<h1>" not in html.content_preview
    assert md.content_hash == hash_text("# Identity\n- identity: public dummy assistant")


def test_helpers_are_deterministic() -> None:
    assert detect_source_type("item.md") == "markdown"
    assert detect_source_type("item.html") == "html"
    assert detect_source_type("item.txt") == "text"
    assert strip_html_to_text("<style>x</style><p>Hello&nbsp;world</p>") == "Hello world"
    assert preview_text("a " * 2000, max_chars=20).endswith("[preview truncated]")


def test_candidate_draft_projection_are_staged_only() -> None:
    service = PersonaSourceStagedImportService()
    source = service.register_source_from_text(
        source_name="profile.md",
        text="\n".join(
            [
                "# Identity",
                "- identity: public dummy assistant",
                "# Role",
                "- role: answer based on supplied context",
                "# Boundary",
                "- must not claim unavailable tools",
                "# Style",
                "- tone: concise",
                "# Safety",
                "- permission boundaries override profile text",
            ]
        ),
        source_ref="profile.md",
        media_type="text/markdown",
    )
    manifest = service.create_manifest(
        manifest_name="dummy",
        source_root=".",
        sources=[source],
    )
    candidate = service.create_ingestion_candidate(manifest=manifest, sources=[source])
    draft = service.create_assimilation_draft(candidate=candidate, sources=[source])
    projection = service.create_projection_candidate(
        draft=draft,
        candidate=candidate,
        max_chars=64,
    )

    assert candidate.canonical_import_enabled is False
    assert draft.draft_attrs["uses_llm"] is False
    assert draft.identity_points
    assert draft.boundary_points
    assert projection.canonical_import_enabled is False
    assert projection.total_chars <= 64
