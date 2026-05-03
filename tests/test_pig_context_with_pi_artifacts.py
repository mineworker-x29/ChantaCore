from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.pig.assimilation import HumanPIAssimilator
from chanta_core.pig.feedback import PIGFeedbackService
from tests.test_ocel_store import make_record


def test_pig_context_includes_pi_artifacts_when_enabled(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_context_artifacts.sqlite")
    store.append_record(make_record())
    artifact_store = PIArtifactStore(tmp_path / "pi_artifacts.jsonl")
    HumanPIAssimilator(store=artifact_store).assimilate_text(
        "This is a deliberately long PI artifact body that should not be dumped "
        "fully into prompt context because only title and confidence are needed.",
        artifact_type="recommendation",
        title="Review repeated skill failures",
        scope={"session_id": "session-test"},
        confidence=0.6,
    )
    service = PIGFeedbackService(
        ocpx_loader=OCPXLoader(store=store),
        artifact_store=artifact_store,
    )

    context = service.build_recent_context(include_pi_artifacts=True)

    assert len(context.pi_artifacts) == 1
    assert "Human / External PI" in context.context_text
    assert "[recommendation] Review repeated skill failures - confidence 0.60" in (
        context.context_text
    )
    assert "deliberately long PI artifact body" not in context.context_text


def test_pig_context_excludes_pi_artifacts_when_disabled(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_context_no_artifacts.sqlite")
    store.append_record(make_record())
    artifact_store = PIArtifactStore(tmp_path / "pi_artifacts.jsonl")
    HumanPIAssimilator(store=artifact_store).assimilate_text(
        "Human PI note.",
        title="Human PI note",
    )
    service = PIGFeedbackService(
        ocpx_loader=OCPXLoader(store=store),
        artifact_store=artifact_store,
    )

    context = service.build_recent_context(include_pi_artifacts=False)

    assert context.pi_artifacts == []
    assert "Human / External PI" not in context.context_text
