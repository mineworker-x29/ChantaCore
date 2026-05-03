from chanta_core.ocpx.variant import OCPXVariantSummary
from chanta_core.pig.artifacts import PIArtifact
from chanta_core.pig.guidance import PIGGuidanceService


def variant(
    *,
    activity_sequence: list[str],
    failure_count: int,
    success_count: int,
) -> OCPXVariantSummary:
    return OCPXVariantSummary(
        variant_key=">".join(activity_sequence),
        activity_sequence=activity_sequence,
        trace_count=1,
        success_count=success_count,
        failure_count=failure_count,
        skill_ids=[],
        example_process_instance_ids=["process_instance:test"],
        variant_attrs={},
    )


def test_failure_variant_creates_inspection_guidance() -> None:
    guidance = PIGGuidanceService().build_from_variant_summary(
        variant(
            activity_sequence=["start_process_run_loop", "fail_process_instance"],
            failure_count=1,
            success_count=0,
        )
    )

    assert any(item.suggested_skill_id == "skill:inspect_ocel_recent" for item in guidance)
    assert guidance[0].target_scope["variant_key"]
    assert guidance[0].guidance_attrs["variant_failure_count"] == 1


def test_clean_successful_variant_does_not_create_strong_guidance() -> None:
    guidance = PIGGuidanceService().build_from_variant_summary(
        variant(
            activity_sequence=["start_process_run_loop", "complete_process_instance"],
            failure_count=0,
            success_count=1,
        )
    )

    assert all(item.score_delta == 0.0 for item in guidance)


def test_trace_oriented_variant_suggests_trace_summary() -> None:
    guidance = PIGGuidanceService().build_from_variant_summary(
        variant(
            activity_sequence=["start_process_run_loop", "summarize_process_trace"],
            failure_count=0,
            success_count=1,
        )
    )

    assert any(
        item.suggested_skill_id == "skill:summarize_process_trace"
        for item in guidance
    )


def test_human_pi_with_variant_evidence_remains_advisory() -> None:
    artifact = PIArtifact(
        artifact_id="pi_artifact:variant",
        artifact_type="recommendation",
        source_type="human_pi",
        title="Inspect variant",
        content="Variant has suspicious failures.",
        scope={"variant_key": "a>b>c"},
        evidence_refs=[{"ref_type": "variant", "ref_id": "a>b>c", "attrs": {}}],
        object_refs=[],
        confidence=0.95,
        status="active",
        created_at="2026-05-03T00:00:00Z",
        artifact_attrs={
            "suggested_skill_id": "skill:inspect_ocel_recent",
            "variant_key": "a>b>c",
        },
    )

    guidance = PIGGuidanceService().build_from_artifacts([artifact])

    assert guidance[0].confidence == 0.8
    assert guidance[0].guidance_attrs["advisory"] is True
    assert guidance[0].guidance_attrs["hard_policy"] is False
    assert guidance[0].guidance_attrs["variant_key"] == "a>b>c"
