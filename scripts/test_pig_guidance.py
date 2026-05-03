from __future__ import annotations

from chanta_core.pig.guidance import PIGGuidanceService


def main() -> None:
    guidance = PIGGuidanceService().build_recent_guidance(limit=20)

    print("guidance_count:", len(guidance))
    for item in guidance:
        print(
            {
                "title": item.title,
                "type": item.guidance_type,
                "suggested_skill_id": item.suggested_skill_id,
                "score_delta": item.score_delta,
                "confidence": item.confidence,
            }
        )


if __name__ == "__main__":
    main()
