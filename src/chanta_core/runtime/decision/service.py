from __future__ import annotations

from chanta_core.pig.guidance import PIGGuidanceService
from chanta_core.runtime.decision.context import DecisionContext
from chanta_core.runtime.decision.decision import ProcessDecision
from chanta_core.runtime.decision.policy import DecisionPolicy
from chanta_core.runtime.decision.scoring import DecisionScorer
from chanta_core.skills.registry import SkillRegistry


class DecisionService:
    def __init__(
        self,
        *,
        skill_registry: SkillRegistry,
        guidance_service: PIGGuidanceService | None = None,
        scorer: DecisionScorer | None = None,
        policy: DecisionPolicy | None = None,
    ) -> None:
        self.skill_registry = skill_registry
        self.guidance_service = guidance_service
        self.scorer = scorer or DecisionScorer()
        self.policy = policy or DecisionPolicy()
        self.policy.validate()

    def decide_skill(self, context: DecisionContext) -> ProcessDecision:
        if (
            context.explicit_skill_id
            and context.explicit_skill_id in context.available_skill_ids
        ):
            return ProcessDecision(
                selected_skill_id=context.explicit_skill_id,
                decision_mode="explicit",
                base_scores={skill_id: 0.0 for skill_id in context.available_skill_ids},
                final_scores={skill_id: 0.0 for skill_id in context.available_skill_ids},
                applied_guidance_ids=[],
                rationale="Explicit skill_id was provided and is available.",
                evidence_refs=[],
                decision_attrs={
                    "advisory": True,
                    "hard_policy": False,
                    "ignored_guidance": [],
                    "capped_skills": [],
                    "boost_by_skill": {},
                    "tie_break_used": False,
                    "tie_candidates": [],
                    "fallback_used": False,
                    "policy": self._policy_attrs(),
                },
            )

        base_scores = self.scorer.base_scores(context)
        final_scores, guidance_diagnostics = self.scorer.apply_guidance(
            base_scores,
            context,
            self.policy,
        )
        selected_skill_id, selection_diagnostics = self.scorer.select_best(
            final_scores,
            self.policy,
        )
        if selected_skill_id not in context.available_skill_ids:
            selected_skill_id = self.policy.fallback_skill_id
            selection_diagnostics["fallback_used"] = True
            selection_diagnostics["selected_skill_id"] = selected_skill_id
        applied_guidance_ids = list(guidance_diagnostics["applied_guidance_ids"])

        if bool(selection_diagnostics.get("fallback_used")):
            decision_mode = "fallback"
            rationale = "No stronger route matched; using safe LLM chat fallback."
        elif bool(selection_diagnostics.get("tie_break_used")):
            decision_mode = "tie_break"
            rationale = "Deterministic tie-break order selected the skill."
        elif applied_guidance_ids and final_scores.get(selected_skill_id, 0.0) > base_scores.get(
            selected_skill_id,
            0.0,
        ):
            decision_mode = "guidance_bias"
            rationale = "Deterministic skill scoring applied advisory PIG guidance."
        elif final_scores.get(selected_skill_id, 0.0) > 0.0:
            decision_mode = "heuristic"
            rationale = "Deterministic skill scoring used user input heuristics."
        else:
            decision_mode = "fallback"
            rationale = "No stronger route matched; using safe LLM chat fallback."

        return ProcessDecision(
            selected_skill_id=selected_skill_id,
            decision_mode=decision_mode,
            base_scores=base_scores,
            final_scores=final_scores,
            applied_guidance_ids=applied_guidance_ids,
            rationale=rationale,
            evidence_refs=[
                ref
                for guidance in context.pig_guidance
                if guidance.guidance_id in applied_guidance_ids
                for ref in guidance.evidence_refs
            ],
            decision_attrs={
                "advisory": True,
                "hard_policy": False,
                **guidance_diagnostics,
                **selection_diagnostics,
                "policy": self._policy_attrs(),
            },
        )

    def _policy_attrs(self) -> dict[str, object]:
        return {
            "min_guidance_confidence": self.policy.min_guidance_confidence,
            "max_guidance_boost_per_skill": self.policy.max_guidance_boost_per_skill,
            "fallback_skill_id": self.policy.fallback_skill_id,
            "tie_break_order": self.policy.tie_break_order,
        }
