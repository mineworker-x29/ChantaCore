from chanta_core.instructions import InstructionService


def main() -> None:
    service = InstructionService()
    instruction = service.register_instruction_artifact(
        instruction_type="project",
        title="OCEL persistence rule",
        body="Canonical persistence must be OCEL-based.",
        session_id="session:script-instruction",
    )
    rule = service.register_project_rule(
        rule_type="constraint",
        text="Do not create canonical Markdown memory stores.",
        source_instruction_id=instruction.instruction_id,
    )
    preference = service.register_user_preference(
        preference_key="report_style",
        preference_value="evidence-first",
        session_id="session:script-instruction",
    )

    print(f"instruction_id={instruction.instruction_id}")
    print(f"project_rule_id={rule.rule_id}")
    print(f"user_preference_id={preference.preference_id}")


if __name__ == "__main__":
    main()
