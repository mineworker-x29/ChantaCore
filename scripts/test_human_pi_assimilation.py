from __future__ import annotations

from chanta_core.pig.assimilation import HumanPIAssimilator
from chanta_core.pig.feedback import PIGFeedbackService


def main() -> None:
    artifact = HumanPIAssimilator().assimilate_text(
        "Repeated fail_skill_execution suggests reviewing the selected skill before the next run.",
        artifact_type="diagnostic",
        title="Review repeated skill failure",
        confidence=0.7,
    )
    context = PIGFeedbackService().build_recent_context(include_pi_artifacts=True)

    print("artifact:", artifact.to_dict())
    print(context.context_text)


if __name__ == "__main__":
    main()
