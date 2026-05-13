from chanta_core.observation_digest import DigestionService, ObservationService
from chanta_core.observation_digest.ids import new_agent_observation_batch_id


def _make_public_skill(tmp_path):
    skill_dir = tmp_path / "public_skill"
    skill_dir.mkdir()
    body = "\n".join(
        [
            "# Public Dummy Skill",
            "Description: deterministic read-only fixture for static digestion.",
            "Tools: none",
            "Inputs: root_path, relative_path",
            "Outputs: short summary",
            "Risks: filesystem read only",
            "Instructions: " + ("inspect public fixture metadata only. " * 40),
        ]
    )
    (skill_dir / "SKILL.md").write_bytes(body.encode("utf-8"))
    return skill_dir, body


def _make_observed_run():
    observation = ObservationService()
    source = observation.inspect_observation_source(
        root_path=".",
        relative_path="pyproject.toml",
        source_runtime="dummy_runtime",
        format_hint="generic_jsonl",
    )
    records = [{"id": "one", "tool": "read_file", "input": {"path": "fixture.txt"}}]
    events = observation.normalize_observation_records(
        records,
        batch_id=new_agent_observation_batch_id(),
        source_runtime="dummy_runtime",
        source_format="generic_jsonl",
    )
    batch = observation.create_observation_batch(
        source=source,
        raw_record_count=1,
        normalized_events=events,
    )
    return observation.create_observed_run(source=source, batch=batch, normalized_events=events), events


def test_external_skill_source_is_inspected_read_only(tmp_path):
    _skill_dir, _body = _make_public_skill(tmp_path)
    service = DigestionService()

    descriptor = service.inspect_external_skill_source(
        root_path=str(tmp_path),
        relative_path="public_skill",
        vendor_hint="dummy_vendor",
    )

    assert descriptor.detected_manifest_refs == ["SKILL.md"]
    assert descriptor.descriptor_attrs["read_only"] is True
    assert descriptor.descriptor_attrs["external_execution_used"] is False


def test_static_profile_uses_preview_without_full_raw_body(tmp_path):
    _skill_dir, body = _make_public_skill(tmp_path)
    service = DigestionService()
    descriptor = service.inspect_external_skill_source(
        root_path=str(tmp_path),
        relative_path="public_skill",
        vendor_hint="dummy_vendor",
    )

    profile = service.create_static_profile(
        source_descriptor=descriptor,
        root_path=str(tmp_path),
        relative_path="public_skill",
    )

    assert profile.declared_name == "Public Dummy Skill"
    assert profile.instruction_preview
    assert profile.instruction_preview != body
    assert profile.profile_attrs["full_raw_body_stored"] is False


def test_fingerprint_assimilation_and_adapter_defaults_are_safe(tmp_path):
    _skill_dir, _body = _make_public_skill(tmp_path)
    service = DigestionService()
    descriptor = service.inspect_external_skill_source(
        root_path=str(tmp_path),
        relative_path="public_skill",
        vendor_hint="dummy_vendor",
    )
    profile = service.create_static_profile(
        source_descriptor=descriptor,
        root_path=str(tmp_path),
        relative_path="public_skill",
    )
    run, events = _make_observed_run()

    fingerprint = service.create_behavior_fingerprint(observed_run=run, normalized_events=events)
    candidate = service.create_assimilation_candidate(
        static_profile=profile,
        behavior_fingerprint=fingerprint,
        source_runtime="dummy_runtime",
    )
    adapter = service.create_adapter_candidate(candidate=candidate)

    assert fingerprint.observed_event_count == 1
    assert candidate.review_status == "pending_review"
    assert candidate.canonical_import_enabled is False
    assert candidate.execution_enabled is False
    assert adapter.requires_review is True
    assert adapter.execution_enabled is False
