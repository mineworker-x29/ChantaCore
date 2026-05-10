import inspect

import chanta_core.execution.envelope_service as envelope_module
from chanta_core.execution import ExecutionEnvelopeService


def test_envelope_service_does_not_execute_skills() -> None:
    source = inspect.getsource(ExecutionEnvelopeService)

    assert "invoke_explicit_skill(" not in source
    assert "gate_explicit_invocation(" not in source
    assert "ToolDispatcher" not in source
    assert "SkillExecutor" not in source


def test_envelope_source_avoids_disallowed_runtime_paths() -> None:
    source = inspect.getsource(envelope_module)
    blocked_terms = [
        "envelope_" + "executes_skill",
        "auto_" + "execute_from_envelope",
        "complete_" + "text",
        "complete_" + "json",
        "sub" + "process",
        "os." + "system",
        "request" + "s.",
        "http" + "x.",
        "socket" + ".",
        "connect_" + "mcp",
        "load_" + "plugin",
        "write_" + "text",
        "jso" + "nl",
    ]

    for term in blocked_terms:
        assert term not in source


def test_envelope_defaults_do_not_store_full_payloads() -> None:
    service = ExecutionEnvelopeService()
    envelope = service.create_envelope(
        execution_kind="test",
        execution_subject_id="subject:test",
        skill_id=None,
        status="skipped",
        execution_allowed=False,
        execution_performed=False,
        blocked=False,
    )
    input_snapshot = service.record_input_snapshot(envelope=envelope, input_payload={"value": "public"})
    output_snapshot = service.record_output_snapshot(envelope=envelope, output_payload={"value": "public"})

    assert input_snapshot.full_input_stored is False
    assert output_snapshot.full_output_stored is False
