from __future__ import annotations

from chanta_core.self_awareness.surface_verification import (
    SURFACE_VERIFICATION_EFFECTS,
    SelfSurfaceVerificationRequest,
    SelfSurfaceVerificationSkillService,
)
from chanta_core.self_awareness.workspace_awareness import READ_ONLY_OBSERVATION_EFFECT
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_self_awareness_surface_verify_skill() -> Skill:
    return Skill(
        skill_id="skill:self_awareness_surface_verify",
        skill_name="self_awareness_surface_verify",
        description="Verify self-awareness output surfaces through deterministic evidence, boundary, and candidate checks.",
        execution_type="builtin",
        input_schema={
            "target_type": "str",
            "target_id": "str",
            "target_payload": "dict",
            "strictness": "str",
        },
        output_schema={"report": "SelfSurfaceVerificationReport"},
        tags=[
            "self_awareness",
            "surface_verification",
            "evidence",
            "boundary",
            "candidate_only",
            "read_only",
            "explicit",
        ],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "effect_types": list(SURFACE_VERIFICATION_EFFECTS),
            "evidence_checking_only": True,
            "canonical_promotion_enabled": False,
        },
    )


def execute_self_awareness_surface_verify_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        service = SelfSurfaceVerificationSkillService()
        report = service.verify_surface(
            SelfSurfaceVerificationRequest(
                target_type=_required(context, "target_type"),
                target_id=context.context_attrs.get("target_id"),
                target_payload=context.context_attrs.get("target_payload")
                if isinstance(context.context_attrs.get("target_payload"), dict)
                else {},
                root_id=context.context_attrs.get("root_id"),
                strictness=str(context.context_attrs.get("strictness") or "standard"),
                include_evidence_checks=bool(context.context_attrs.get("include_evidence_checks", True)),
                include_boundary_checks=bool(context.context_attrs.get("include_boundary_checks", True)),
                include_candidate_checks=bool(context.context_attrs.get("include_candidate_checks", True)),
            )
        )
        output = report.to_dict()
        blocked = report.status == "blocked"
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=not blocked,
            output_text=None,
            output_attrs={
                "execution_type": skill.execution_type,
                "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                "effect_types": list(SURFACE_VERIFICATION_EFFECTS),
                **output,
            },
            error=None if not blocked else "Surface verification request was blocked.",
        )
    except Exception as error:
        return _failure(skill, error)


def _required(context: SkillExecutionContext, key: str) -> str:
    value = context.context_attrs.get(key)
    if value is None or str(value) == "":
        raise ValueError(f"{key} is required for self-surface verification")
    return str(value)


def _failure(skill: Skill, error: Exception) -> SkillExecutionResult:
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=False,
        output_text=None,
        output_attrs={
            "execution_type": skill.execution_type,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "effect_types": list(SURFACE_VERIFICATION_EFFECTS),
            "exception_type": type(error).__name__,
            "read_only": True,
            "policy_gated": True,
            "workspace_write_used": False,
            "shell_execution_used": False,
            "network_access_used": False,
            "mcp_connection_used": False,
            "plugin_loading_used": False,
            "external_harness_execution_used": False,
        },
        error=str(error),
    )
