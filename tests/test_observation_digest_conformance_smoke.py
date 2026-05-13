import json

from chanta_core.skills.observation_digest_conformance import ObservationDigestConformanceService


def _write_smoke_fixtures(root):
    (root / "trace.jsonl").write_bytes(
        (
            json.dumps({"role": "user", "content": "inspect this trace"})
            + "\n"
            + json.dumps({"role": "assistant", "content": "inspection started"})
            + "\n"
        ).encode("utf-8")
    )
    skill_dir = root / "external_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(
        "# Generic External Skill\n\nDescription: public smoke fixture.\n".encode("utf-8")
    )


def test_smoke_cases_are_generated_for_all_10_skills():
    service = ObservationDigestConformanceService()

    cases = service.build_required_smoke_cases(fixture_root="fixture")

    assert len(cases) == 10
    assert {case.skill_id for case in cases} == set(service.create_default_policy().required_skill_ids)


def test_agent_trace_observe_smoke_passes_with_generic_jsonl_fixture(tmp_path):
    _write_smoke_fixtures(tmp_path)
    service = ObservationDigestConformanceService()

    results = service.run_smoke(skill_id="skill:agent_trace_observe", fixture_root=str(tmp_path))

    assert len(results) == 1
    assert results[0].passed is True
    assert results[0].envelope_id


def test_external_skill_static_digest_smoke_passes_with_skill_md_fixture(tmp_path):
    _write_smoke_fixtures(tmp_path)
    service = ObservationDigestConformanceService()

    results = service.run_smoke(skill_id="skill:external_skill_static_digest", fixture_root=str(tmp_path))

    assert results[0].passed is True
    assert results[0].envelope_id


def test_external_skill_assimilate_smoke_preserves_candidate_safety():
    service = ObservationDigestConformanceService()

    results = service.run_smoke(skill_id="skill:external_skill_assimilate")
    candidate = service.invocation_service.digestion_service.last_candidate

    assert results[0].passed is True
    assert candidate.review_status == "pending_review"
    assert candidate.canonical_import_enabled is False
    assert candidate.execution_enabled is False
