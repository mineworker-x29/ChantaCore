from pathlib import Path
from tempfile import TemporaryDirectory

from chanta_core.ocel.store import OCELStore
from chanta_core.tool_registry import ToolRegistryViewService
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        root = Path(tmp)
        store = OCELStore(root / "tool_registry_views.sqlite")
        service = ToolRegistryViewService(
            trace_service=TraceService(ocel_store=store),
            root=root,
        )
        verify = service.register_tool_descriptor(
            tool_name="verify_file_exists",
            tool_type="verification",
            description="Verify a path exists.",
            risk_level="read_only",
            capability_tags=["verify", "read"],
            source_kind="test",
        )
        read = service.register_tool_descriptor(
            tool_name="read_file",
            tool_type="builtin",
            description="Read file contents.",
            risk_level="read_only",
            capability_tags=["read"],
            source_kind="test",
        )
        write = service.register_tool_descriptor(
            tool_name="write_file",
            tool_type="builtin",
            description="Write file contents.",
            risk_level="high",
            capability_tags=["write"],
            source_kind="test",
        )
        snapshot = service.create_registry_snapshot(
            tools=[verify, read, write],
            snapshot_name="smoke",
            source_kind="test",
        )
        note = service.register_tool_policy_note(
            tool_id=write.tool_id,
            tool_name=write.tool_name,
            note_type="review_needed",
            text="Write tools require future permission model review.",
            priority=10,
            source_kind="test",
        )
        annotation = service.register_tool_risk_annotation(
            tool_id=write.tool_id,
            risk_level="high",
            risk_category="write",
            rationale="Writes can change workspace state.",
        )
        results = service.write_tool_views(
            tools=[verify, read, write],
            snapshot=snapshot,
            policy_notes=[note],
            risk_annotations=[annotation],
            root=root,
        )
        print(f"tools_path={results['tools']['target_path']}")
        print(f"tool_policy_path={results['tool_policy']['target_path']}")
        for key in ["tools", "tool_policy"]:
            path = Path(results[key]["target_path"])
            print(f"{path.name}:")
            for line in path.read_text(encoding="utf-8").splitlines()[:8]:
                print(line)


if __name__ == "__main__":
    main()
