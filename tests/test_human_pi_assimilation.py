from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.pig.assimilation import HumanPIAssimilator


def test_human_pi_assimilation_stores_advisory_artifact(tmp_path) -> None:
    store = PIArtifactStore(tmp_path / "pi_artifacts.jsonl")
    assimilator = HumanPIAssimilator(store=store)

    artifact = assimilator.assimilate_text(
        "Repeated fail_skill_execution suggests review_skill_failure before next run.",
        artifact_type="diagnostic",
        scope={"process_instance_id": "process_instance:test"},
        evidence_refs=[{"ref_type": "event", "ref_id": "evt:test", "attrs": {}}],
        object_refs=[{"ref_type": "skill", "ref_id": "skill:test", "attrs": {}}],
        confidence=0.7,
    )

    loaded = store.load_all()

    assert artifact.source_type == "human_pi"
    assert artifact.status == "active"
    assert artifact.confidence == 0.7
    assert artifact.scope["process_instance_id"] == "process_instance:test"
    assert artifact.evidence_refs
    assert artifact.object_refs
    assert artifact.artifact_attrs["advisory"] is True
    assert artifact.artifact_attrs["hard_policy"] is False
    assert loaded == [artifact]


def test_pi_artifact_store_skips_invalid_jsonl_rows(tmp_path) -> None:
    path = tmp_path / "pi_artifacts_invalid.jsonl"
    path.write_text("{not-json}\n", encoding="utf-8")
    store = PIArtifactStore(path)

    assert store.load_all() == []
    assert store.warnings
