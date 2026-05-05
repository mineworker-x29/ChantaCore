from tempfile import TemporaryDirectory
from pathlib import Path

from chanta_core.instructions import (
    InstructionArtifact,
    ProjectRule,
    UserPreference,
    hash_body,
)
from chanta_core.materialized_views import (
    MaterializedViewInputSnapshot,
    MaterializedViewService,
)
from chanta_core.memory import MemoryEntry, hash_content


def main() -> None:
    snapshot = MaterializedViewInputSnapshot(
        memories=[
            MemoryEntry(
                memory_id="memory:script",
                memory_type="semantic",
                title="Script Memory",
                content="Materialized views are generated from OCEL-native objects.",
                content_preview="Materialized views are generated from OCEL-native objects.",
                content_hash=hash_content(
                    "Materialized views are generated from OCEL-native objects."
                ),
                status="active",
                confidence=1.0,
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
                valid_from=None,
                valid_until=None,
                contradiction_status="none",
                source_kind="manual_entry",
                scope="project",
            )
        ],
        instructions=[
            InstructionArtifact(
                instruction_id="instruction:script",
                instruction_type="project",
                title="Script Instruction",
                body="Markdown views are not canonical.",
                body_preview="Markdown views are not canonical.",
                body_hash=hash_body("Markdown views are not canonical."),
                status="active",
                scope="project",
                priority=100,
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
                source_path=None,
            )
        ],
        project_rules=[
            ProjectRule(
                rule_id="project_rule:script",
                rule_type="constraint",
                text="Do not treat Markdown edits as OCEL updates.",
                status="active",
                priority=100,
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
                source_instruction_id="instruction:script",
            )
        ],
        user_preferences=[
            UserPreference(
                preference_id="user_preference:script",
                preference_key="format",
                preference_value="concise",
                status="active",
                confidence=1.0,
                source_kind="manual_entry",
                created_at="2026-05-05T00:00:00Z",
                updated_at="2026-05-05T00:00:00Z",
            )
        ],
    )

    with TemporaryDirectory() as temp_dir:
        service = MaterializedViewService(root=temp_dir)
        results = service.refresh_default_views(snapshot)
        for key in sorted(results):
            path = Path(results[key].target_path)
            print(f"{key}={path}")
            print("\n".join(path.read_text(encoding="utf-8").splitlines()[:5]))


if __name__ == "__main__":
    main()
