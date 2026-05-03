from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class DecisionPolicy:
    min_guidance_confidence: float = 0.45
    max_guidance_boost_per_skill: float = 0.50
    fallback_skill_id: str = "skill:llm_chat"
    tie_break_order: list[str] = field(
        default_factory=lambda: [
            "skill:llm_chat",
            "skill:inspect_ocel_recent",
            "skill:summarize_process_trace",
            "skill:echo",
            "skill:summarize_text",
            "skill:ingest_human_pi",
            "skill:summarize_pi_artifacts",
        ]
    )

    def validate(self) -> None:
        if not 0.0 <= self.min_guidance_confidence <= 1.0:
            raise ValueError("min_guidance_confidence must be between 0.0 and 1.0")
        if self.max_guidance_boost_per_skill < 0.0:
            raise ValueError("max_guidance_boost_per_skill must be >= 0.0")
        if not self.fallback_skill_id:
            raise ValueError("fallback_skill_id must not be empty")
        if not self.tie_break_order:
            raise ValueError("tie_break_order must not be empty")
