from __future__ import annotations

from chanta_core.pig.feedback import PIGFeedbackService


def main() -> None:
    context = PIGFeedbackService().build_recent_context(limit=20)

    print(context.context_text)
    print("activity_sequence:", context.activity_sequence)
    print("relation_coverage:", context.relation_coverage)
    print("diagnostics:", context.diagnostics)
    print("recommendations:", context.recommendations)


if __name__ == "__main__":
    main()
