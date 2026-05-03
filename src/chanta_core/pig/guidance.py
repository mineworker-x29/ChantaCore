from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.ocpx.variant import OCPXVariantSummary
from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.pig.artifacts import PIArtifact
from chanta_core.pig.context import PIGContext
from chanta_core.pig.feedback import PIGFeedbackService


def new_guidance_id() -> str:
    return f"pig_guidance:{uuid4()}"


@dataclass(frozen=True)
class PIGGuidance:
    guidance_id: str
    guidance_type: str
    title: str
    target_scope: dict[str, Any]
    suggested_skill_id: str | None
    suggested_activity: str | None
    score_delta: float
    rationale: str
    evidence_refs: list[dict[str, Any]]
    confidence: float
    status: str
    guidance_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("PIGGuidance confidence must be between 0.0 and 1.0")

    def to_dict(self) -> dict[str, Any]:
        return {
            "guidance_id": self.guidance_id,
            "guidance_type": self.guidance_type,
            "title": self.title,
            "target_scope": self.target_scope,
            "suggested_skill_id": self.suggested_skill_id,
            "suggested_activity": self.suggested_activity,
            "score_delta": self.score_delta,
            "rationale": self.rationale,
            "evidence_refs": self.evidence_refs,
            "confidence": self.confidence,
            "status": self.status,
            "guidance_attrs": self.guidance_attrs,
        }


class PIGGuidanceService:
    def __init__(
        self,
        *,
        feedback_service: PIGFeedbackService | None = None,
        artifact_store: PIArtifactStore | None = None,
    ) -> None:
        self.feedback_service = feedback_service or PIGFeedbackService(
            artifact_store=artifact_store,
        )
        self.artifact_store = artifact_store or self.feedback_service.artifact_store

    def build_recent_guidance(self, limit: int = 20) -> list[PIGGuidance]:
        context = self.feedback_service.build_recent_context(limit=limit)
        return self.build_from_context(context)

    def build_process_instance_guidance(
        self,
        process_instance_id: str,
    ) -> list[PIGGuidance]:
        context = self.feedback_service.build_process_instance_context(
            process_instance_id,
        )
        return self.build_from_context(context)

    def build_from_context(self, context: PIGContext) -> list[PIGGuidance]:
        guidance: list[PIGGuidance] = []
        failure_count = int(context.performance_summary.get("failure_count") or 0)
        activity_sequence = set(context.activity_sequence)
        target_scope = {
            "scope": context.scope,
            "process_instance_id": context.process_instance_id,
            "session_id": context.session_id,
        }

        if (
            failure_count > 0
            or "fail_skill_execution" in activity_sequence
            or "fail_process_instance" in activity_sequence
        ):
            guidance.append(
                self._guidance(
                    guidance_type="inspect_first",
                    title="Inspect trace after recent failure",
                    target_scope=target_scope,
                    suggested_skill_id="skill:inspect_ocel_recent",
                    score_delta=0.3,
                    confidence=0.6,
                    rationale=(
                        "Recent traces contain failures; inspect OCEL trace before "
                        "continuing."
                    ),
                    evidence_refs=[{"ref_type": "pig_context", "ref_id": context.scope}],
                )
            )

        coverage_ratio = float(context.relation_coverage.get("coverage_ratio") or 0.0)
        if coverage_ratio < 1.0:
            guidance.append(
                self._guidance(
                    guidance_type="skill_bias",
                    title="Inspect incomplete OCEL relation coverage",
                    target_scope=target_scope,
                    suggested_skill_id="skill:inspect_ocel_recent",
                    score_delta=0.2,
                    confidence=0.55,
                    rationale=(
                        "Some events lack related objects; inspect OCEL relation "
                        "coverage."
                    ),
                    evidence_refs=[{"ref_type": "pig_context", "ref_id": context.scope}],
                )
            )

        if self._scope_is_trace_oriented(target_scope) or self._artifacts_are_trace_oriented(
            context.pi_artifacts
        ):
            guidance.append(
                self._guidance(
                    guidance_type="summarize_trace_first",
                    title="Summarize trace-oriented context",
                    target_scope=target_scope,
                    suggested_skill_id="skill:summarize_process_trace",
                    score_delta=0.25,
                    confidence=0.6,
                    rationale="Current context appears process/trace-oriented.",
                    evidence_refs=[{"ref_type": "pig_context", "ref_id": context.scope}],
                )
            )

        guidance.extend(
            self.build_from_artifacts(
                [PIArtifact.from_dict(item) for item in context.pi_artifacts]
            )
        )
        return guidance

    def build_from_variant_summary(
        self,
        variant: OCPXVariantSummary,
    ) -> list[PIGGuidance]:
        guidance: list[PIGGuidance] = []
        target_scope = {
            "variant_key": variant.variant_key,
            "failure_count": variant.failure_count,
            "success_count": variant.success_count,
            "similarity_basis": "activity_sequence",
        }
        evidence_refs = [
            {
                "ref_type": "variant",
                "ref_id": variant.variant_key,
                "attrs": {
                    "example_process_instance_ids": (
                        variant.example_process_instance_ids
                    )
                },
            }
        ]
        if variant.failure_count > 0:
            guidance.append(
                self._guidance(
                    guidance_type="variant_skill_bias",
                    title="Inspect trace for failure-prone variant",
                    target_scope=target_scope,
                    suggested_skill_id="skill:inspect_ocel_recent",
                    score_delta=0.25,
                    confidence=0.6,
                    rationale=(
                        "This variant includes failed executions; inspect OCEL trace "
                        "before continuing."
                    ),
                    evidence_refs=evidence_refs,
                    guidance_attrs={
                        "variant_key": variant.variant_key,
                        "variant_failure_count": variant.failure_count,
                        "variant_success_count": variant.success_count,
                        "similarity_basis": "activity_sequence",
                        "confidence_basis": "variant_failure_count",
                    },
                )
            )

        activity_set = set(variant.activity_sequence)
        if activity_set.intersection(
            {
                "inspect_ocel_recent",
                "summarize_process_trace",
                "fail_skill_execution",
                "fail_process_instance",
            }
        ) or any(
            skill_id in {"skill:inspect_ocel_recent", "skill:summarize_process_trace"}
            for skill_id in variant.skill_ids
        ):
            guidance.append(
                self._guidance(
                    guidance_type="variant_skill_bias",
                    title="Summarize trace-oriented variant",
                    target_scope=target_scope,
                    suggested_skill_id="skill:summarize_process_trace",
                    score_delta=0.2,
                    confidence=0.55,
                    rationale="This variant appears trace/process-oriented.",
                    evidence_refs=evidence_refs,
                    guidance_attrs={
                        "variant_key": variant.variant_key,
                        "variant_failure_count": variant.failure_count,
                        "variant_success_count": variant.success_count,
                        "similarity_basis": "activity_sequence",
                        "confidence_basis": "variant_activity_sequence",
                    },
                )
            )
        return guidance

    def build_from_artifacts(self, artifacts: list[PIArtifact]) -> list[PIGGuidance]:
        guidance: list[PIGGuidance] = []
        for artifact in artifacts:
            if artifact.artifact_type in {
                "recommendation",
                "policy_hint",
                "diagnostic",
                "hypothesis",
            } and artifact.artifact_attrs.get("suggested_skill_id"):
                guidance.append(
                    self._guidance(
                        guidance_type="skill_bias",
                        title=f"Advisory PI suggests {artifact.artifact_attrs['suggested_skill_id']}",
                        target_scope=artifact.scope,
                        suggested_skill_id=str(
                            artifact.artifact_attrs["suggested_skill_id"]
                        ),
                        score_delta=float(artifact.artifact_attrs.get("score_delta", 0.2)),
                        confidence=min(float(artifact.confidence), 0.8),
                        rationale=(
                            "Human/external PI suggests this skill as advisory "
                            "guidance, not ground truth."
                        ),
                        evidence_refs=[
                            {
                                "ref_type": "pi_artifact",
                                "ref_id": artifact.artifact_id,
                                "attrs": {
                                    "source_type": artifact.source_type,
                                    "artifact_evidence_refs": artifact.evidence_refs,
                                },
                            }
                        ],
                        guidance_attrs={
                            "variant_key": artifact.artifact_attrs.get("variant_key"),
                            "confidence_basis": "pi_artifact_confidence",
                        },
                    )
                )
            elif self._is_trace_oriented(
                {
                    "content": artifact.content,
                    "title": artifact.title,
                    "scope": artifact.scope,
                }
            ):
                guidance.append(
                    self._guidance(
                        guidance_type="summarize_trace_first",
                        title="Advisory PI indicates trace-oriented review",
                        target_scope=artifact.scope,
                        suggested_skill_id="skill:summarize_process_trace",
                        score_delta=0.25,
                        confidence=min(float(artifact.confidence), 0.6),
                        rationale="Current context appears process/trace-oriented.",
                        evidence_refs=[
                            {
                                "ref_type": "pi_artifact",
                                "ref_id": artifact.artifact_id,
                                "attrs": {"source_type": artifact.source_type},
                            }
                        ],
                    )
                )
        return guidance

    @staticmethod
    def _guidance(
        *,
        guidance_type: str,
        title: str,
        target_scope: dict[str, Any],
        suggested_skill_id: str | None,
        score_delta: float,
        confidence: float,
        rationale: str,
        evidence_refs: list[dict[str, Any]],
        suggested_activity: str | None = None,
        guidance_attrs: dict[str, Any] | None = None,
    ) -> PIGGuidance:
        return PIGGuidance(
            guidance_id=new_guidance_id(),
            guidance_type=guidance_type,
            title=title,
            target_scope=target_scope,
            suggested_skill_id=suggested_skill_id,
            suggested_activity=suggested_activity,
            score_delta=score_delta,
            rationale=rationale,
            evidence_refs=evidence_refs,
            confidence=confidence,
            status="active",
            guidance_attrs={
                **(guidance_attrs or {}),
                "advisory": True,
                "hard_policy": False,
            },
        )

    @staticmethod
    def _is_trace_oriented(value: Any) -> bool:
        haystack = str(value).lower()
        return any(
            keyword in haystack
            for keyword in ("trace", "process", "history", "variant")
        )

    @classmethod
    def _scope_is_trace_oriented(cls, scope: dict[str, Any]) -> bool:
        return any(cls._is_trace_oriented(value) for value in scope.values() if value)

    @classmethod
    def _artifacts_are_trace_oriented(cls, artifacts: list[dict[str, Any]]) -> bool:
        return any(
            cls._is_trace_oriented(
                {
                    "title": artifact.get("title"),
                    "content": artifact.get("content"),
                    "scope": artifact.get("scope"),
                }
            )
            for artifact in artifacts
        )
