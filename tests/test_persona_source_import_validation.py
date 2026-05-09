from chanta_core.persona import PersonaSourceStagedImportService
from chanta_core.persona.source_import import safe_read_text_file
from chanta_core.persona.errors import PersonaSourceImportError


def test_validates_sources_and_candidates() -> None:
    service = PersonaSourceStagedImportService()
    source = service.register_source_from_text(
        source_name="profile.md",
        text="identity: public dummy",
        source_ref="profile.md",
        media_type="text/markdown",
    )
    manifest = service.create_manifest(manifest_name="dummy", source_root=".", sources=[source])
    candidate = service.create_ingestion_candidate(manifest=manifest, sources=[source])

    validation = service.validate_source(source, candidate_id=candidate.candidate_id)
    candidate_validations = service.validate_candidate(candidate, [source])

    assert validation.status == "valid"
    assert candidate_validations[0].status == "valid"


def test_safe_read_rejects_outside_oversize_binary_and_extension(tmp_path) -> None:
    root = tmp_path / "root"
    root.mkdir()
    good = root / "profile.md"
    good.write_text("identity: public dummy", encoding="utf-8")
    assert safe_read_text_file(good, source_root=root) == "identity: public dummy"

    outside = tmp_path / "outside.md"
    outside.write_text("outside", encoding="utf-8")
    try:
        safe_read_text_file(outside, source_root=root)
    except ValueError:
        pass
    else:
        raise AssertionError("outside source root should be rejected")

    bad_extension = root / "profile.bin"
    bad_extension.write_text("text", encoding="utf-8")
    try:
        safe_read_text_file(bad_extension, source_root=root)
    except PersonaSourceImportError:
        pass
    else:
        raise AssertionError("unsupported extension should be rejected")

    binary = root / "binary.md"
    binary.write_bytes(b"abc\x00def")
    try:
        safe_read_text_file(binary, source_root=root)
    except PersonaSourceImportError:
        pass
    else:
        raise AssertionError("binary file should be rejected")

    try:
        safe_read_text_file(good, source_root=root, max_bytes=2)
    except PersonaSourceImportError:
        pass
    else:
        raise AssertionError("oversize file should be rejected")
