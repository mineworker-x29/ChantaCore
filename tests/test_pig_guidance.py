from chanta_core.pig.artifacts import PIArtifact
from chanta_core.pig.context import PIGContext
from chanta_core.pig.guidance import PIGGuidance, PIGGuidanceService


def make_context(
    *,
    failure_count: int = 0,
    coverage_ratio: float = 1.0,
    activity_sequence: list[str] | None = None,
    pi_artifacts: list[dict] | None = None,
) -> PIGContext:
    return PIGContext(
        source="pig",
        scope="recent",
        process_instance_id=None,
        session_id=None,
        activity_sequence=activity_sequence or ["start_process_run_loop"],
        event_activity_counts={},
        object_type_counts={},
        relation_coverage={
            "events_total": 1,
            "events_with_related_objects": 1 if coverage_ratio == 1.0 else 0,
            "events_without_related_objects": 0 if coverage_ratio == 1.0 else 1,
            "coverage_ratio": coverage_ratio,
        },
        basic_variant={"variant_key": "", "activity_sequence": [], "event_count": 0},
        performance_summary={
            "start_timestamp": None,
            "end_timestamp": None,
            "duration_seconds": None,
            "event_count": 1,
            "llm_call_count": 0,
            "skill_execution_count": 0,
            "failure_count": failure_count,
        },
        guide={},
        diagnostics=[],
        recommendations=[],
        context_text="Process Intelligence Context:\n- Scope: recent",
        pi_artifacts=pi_artifacts or [],
        context_attrs={},
    )


def test_pig_guidance_to_dict() -> None:
    guidance = PIGGuidance(
        guidance_id="pig_guidance:test",
        guidance_type="skill_bias",
        title="Inspect first",
        target_scope={"scope": "recent"},
        suggested_skill_id="skill:inspect_ocel_recent",
        suggested_activity=None,
        score_delta=0.3,
        rationale="advisory",
        evidence_refs=[],
        confidence=0.6,
        status="active",
        guidance_attrs={"advisory": True},
    )

    assert guidance.to_dict()["guidance_id"] == "pig_guidance:test"
    assert guidance.to_dict()["confidence"] == 0.6


def test_guidance_service_builds_inspect_first_for_failures() -> None:
    guidance = PIGGuidanceService().build_from_context(
        make_context(failure_count=1),
    )

    assert any(item.guidance_type == "inspect_first" for item in guidance)
    assert any(item.suggested_skill_id == "skill:inspect_ocel_recent" for item in guidance)


def test_guidance_service_builds_relation_coverage_guidance() -> None:
    guidance = PIGGuidanceService().build_from_context(
        make_context(coverage_ratio=0.5),
    )

    assert any(item.guidance_type == "skill_bias" for item in guidance)
    assert any(item.score_delta == 0.2 for item in guidance)


def test_guidance_service_builds_artifact_suggested_skill_guidance() -> None:
    artifact = PIArtifact(
        artifact_id="pi_artifact:test",
        artifact_type="recommendation",
        source_type="human_pi",
        title="Inspect recent OCEL",
        content="Advisory only.",
        scope={"session_id": "session-test"},
        evidence_refs=[],
        object_refs=[],
        confidence=0.7,
        status="active",
        created_at="2026-05-03T00:00:00Z",
        artifact_attrs={
            "suggested_skill_id": "skill:inspect_ocel_recent",
            "score_delta": 0.4,
            "advisory": True,
            "hard_policy": False,
        },
    )

    guidance = PIGGuidanceService().build_from_artifacts([artifact])

    assert len(guidance) == 1
    assert guidance[0].suggested_skill_id == "skill:inspect_ocel_recent"
    assert guidance[0].score_delta == 0.4
    assert guidance[0].confidence == 0.7
    assert guidance[0].guidance_attrs["hard_policy"] is False


def test_guidance_service_builds_trace_artifact_guidance() -> None:
    artifact = PIArtifact(
        artifact_id="pi_artifact:trace",
        artifact_type="diagnostic",
        source_type="human_pi",
        title="Trace history needs review",
        content="The process variant changed.",
        scope={},
        evidence_refs=[],
        object_refs=[],
        confidence=0.9,
        status="active",
        created_at="2026-05-03T00:00:00Z",
        artifact_attrs={"advisory": True, "hard_policy": False},
    )

    guidance = PIGGuidanceService().build_from_artifacts([artifact])

    assert guidance[0].suggested_skill_id == "skill:summarize_process_trace"
    assert guidance[0].confidence == 0.6
