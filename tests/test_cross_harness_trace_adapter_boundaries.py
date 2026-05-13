from chanta_core.observation import CrossHarnessTraceAdapterService


def test_safe_path_rejects_traversal(tmp_path):
    service = CrossHarnessTraceAdapterService()

    inspection = service.inspect_trace_source(root_path=str(tmp_path), relative_path="../outside.jsonl")

    assert inspection.inspection_attrs["status"] == "blocked"
    assert inspection.supported_by_adapter is False
    assert any(finding.finding_type == "workspace_boundary_violation" for finding in service.last_findings)


def test_stub_adapter_returns_controlled_finding_without_live_connection():
    service = CrossHarnessTraceAdapterService()
    service.create_default_policy()
    contracts = service.register_adapter_contracts()
    stub = next(item for item in contracts if item.adapter_name == "CodexTaskLogAdapter")

    assert stub.implemented is False
    assert stub.supports_runtime_hook is False
    assert stub.supports_event_bus is False

    inspection = service.inspect_trace_source(root_path=".", relative_path="missing.jsonl", runtime_hint="codex_task_log")
    assert inspection.selected_adapter_name == "CodexTaskLogAdapter"
    assert any(finding.finding_type in {"adapter_not_implemented", "workspace_boundary_violation"} for finding in service.last_findings)


def test_relations_do_not_make_causal_claims(tmp_path):
    trace_file = tmp_path / "trace.jsonl"
    trace_file.write_bytes(
        b'{"id":"u1","role":"user","content":"input"}\n{"id":"a1","role":"assistant","content":"output"}\n'
    )
    service = CrossHarnessTraceAdapterService()

    service.normalize_file(root_path=str(tmp_path), relative_path="trace.jsonl", runtime_hint="generic_jsonl")

    assert service.spine_service.last_relations
    assert all(relation.causal_claim is False for relation in service.spine_service.last_relations)
