from __future__ import annotations

from chanta_core.runtime.decision.context import DecisionContext
from chanta_core.runtime.decision.policy import DecisionPolicy


class DecisionScorer:
    def base_scores(self, context: DecisionContext) -> dict[str, float]:
        scores = {skill_id: 0.0 for skill_id in context.available_skill_ids}
        user_input = context.user_input.lower()

        self._add(scores, "skill:llm_chat", 0.1)
        if any(item in user_input for item in ("trace", "process", "history", "variant")):
            self._add(scores, "skill:summarize_process_trace", 0.3)
        if any(item in user_input for item in ("ocel", "event", "relation", "object")):
            self._add(scores, "skill:inspect_ocel_recent", 0.3)
        if "echo" in user_input:
            self._add(scores, "skill:echo", 0.5)
        if "summarize" in user_input:
            self._add(scores, "skill:summarize_text", 0.3)
        return scores

    def apply_guidance(
        self,
        scores: dict[str, float],
        context: DecisionContext,
        policy: DecisionPolicy,
    ) -> tuple[dict[str, float], dict[str, object]]:
        updated = dict(scores)
        boost_by_skill = {skill_id: 0.0 for skill_id in context.available_skill_ids}
        applied_guidance_ids: list[str] = []
        ignored_guidance: list[dict[str, str]] = []
        capped_skills: list[str] = []
        for guidance in context.pig_guidance:
            if guidance.status != "active":
                ignored_guidance.append(
                    {"guidance_id": guidance.guidance_id, "reason": "inactive"}
                )
                continue
            suggested_skill_id = guidance.suggested_skill_id
            if not suggested_skill_id:
                ignored_guidance.append(
                    {"guidance_id": guidance.guidance_id, "reason": "no_suggested_skill"}
                )
                continue
            if guidance.confidence < policy.min_guidance_confidence:
                ignored_guidance.append(
                    {
                        "guidance_id": guidance.guidance_id,
                        "reason": "confidence_below_threshold",
                    }
                )
                continue
            if suggested_skill_id not in updated:
                ignored_guidance.append(
                    {
                        "guidance_id": guidance.guidance_id,
                        "reason": "skill_not_available",
                    }
                )
                continue
            requested_boost = guidance.score_delta * guidance.confidence
            remaining = (
                policy.max_guidance_boost_per_skill
                - boost_by_skill.get(suggested_skill_id, 0.0)
            )
            applied_boost = max(0.0, min(requested_boost, remaining))
            if applied_boost < requested_boost and suggested_skill_id not in capped_skills:
                capped_skills.append(suggested_skill_id)
            updated[suggested_skill_id] += applied_boost
            boost_by_skill[suggested_skill_id] = (
                boost_by_skill.get(suggested_skill_id, 0.0) + applied_boost
            )
            applied_guidance_ids.append(guidance.guidance_id)
        return updated, {
            "applied_guidance_ids": applied_guidance_ids,
            "ignored_guidance": ignored_guidance,
            "capped_skills": sorted(capped_skills),
            "boost_by_skill": {
                skill_id: boost
                for skill_id, boost in sorted(boost_by_skill.items())
                if boost > 0.0
            },
        }

    def select_best(
        self,
        scores: dict[str, float],
        policy: DecisionPolicy,
    ) -> tuple[str, dict[str, object]]:
        if not scores:
            return policy.fallback_skill_id, {
                "tie_break_used": False,
                "tie_candidates": [],
                "fallback_used": True,
                "selected_skill_id": policy.fallback_skill_id,
            }
        max_score = max(scores.values())
        tie_candidates = sorted(
            skill_id for skill_id, score in scores.items() if score == max_score
        )
        tie_break_used = len(tie_candidates) > 1
        selected_skill_id = tie_candidates[0]
        if tie_break_used:
            for skill_id in policy.tie_break_order:
                if skill_id in tie_candidates:
                    selected_skill_id = skill_id
                    break
        fallback_used = selected_skill_id == policy.fallback_skill_id and all(
            score == 0.0
            for skill_id, score in scores.items()
            if skill_id != policy.fallback_skill_id
        )
        return selected_skill_id, {
            "tie_break_used": tie_break_used,
            "tie_candidates": tie_candidates if tie_break_used else [],
            "fallback_used": fallback_used,
            "selected_skill_id": selected_skill_id,
        }

    @staticmethod
    def _add(scores: dict[str, float], skill_id: str, delta: float) -> None:
        if skill_id in scores:
            scores[skill_id] += delta
