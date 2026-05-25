from chanta_core.internal_provider.gated_local_runtime_execution import (
    BoundedLocalCommandRunner,
    LocalRuntimeExecutionAuthorization,
    LocalRuntimeExecutionAuthorizationService,
    LocalRuntimeExecutionBoundaryReportService,
    LocalRuntimeExecutionGateRequest,
    LocalRuntimeOutputCaptureService,
    LocalRuntimeProcessSpec,
    LocalRuntimeProcessSpecService,
)


def test_v0247_process_spec_blocks_compileall_network_package_and_destructive() -> None:
    auth = LocalRuntimeExecutionAuthorization(
        authorization_id="auth",
        gate_id="gate",
        candidate_id="candidate",
        eligibility_id="eligibility",
        scope={},
        created_at="2026-05-24T00:00:00Z",
    )
    for argv in [
        ["python", "-m", "compileall", "src"],
        ["curl", "https://example.invalid"],
        ["pip", "install", "x"],
        ["git", "reset", "--force"],
    ]:
        spec = LocalRuntimeProcessSpec(
            process_spec_id="spec",
            candidate_id="candidate",
            authorization_id=auth.authorization_id,
            argv=argv,
            cwd_ref={"kind": "workspace_root", "label": "."},
            sanitized_cwd_label=".",
            timeout_seconds=1,
            max_stdout_bytes=10,
            max_stderr_bytes=10,
            env_policy_ref={"env_values_materialized": False},
        )
        assert LocalRuntimeProcessSpecService().validate_process_spec(spec) is False
        run, stdout, stderr = BoundedLocalCommandRunner().run(spec)
        assert run.run_status == "blocked"
        assert run.command_executed is False
        assert run.process_spawned is False
        assert stdout == ""
        assert stderr == ""


def test_v0247_output_capture_redacts_truncates_and_sanitizes_paths() -> None:
    capture = LocalRuntimeOutputCaptureService().capture_and_truncate_output(
        "run",
        "stdout",
        "token=abcd C:\\Users\\private\\secret\\file.txt extra output",
        24,
    )
    assert capture.truncated is True
    assert capture.redacted is True
    assert capture.raw_secret_output is False
    assert capture.private_full_path_output is False
    assert "abcd" not in capture.text_excerpt


def test_v0247_report_without_gate_input_does_not_use_unrestricted_shell() -> None:
    report = LocalRuntimeExecutionBoundaryReportService().build_report(LocalRuntimeExecutionGateRequest())
    assert report.shell_used is False
    assert report.network_accessed is False
    assert report.package_installed is False
    assert report.destructive_command_executed is False
    assert report.external_provider_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False


def test_v0247_authorization_already_consumed_blocks_second_consume() -> None:
    auth = LocalRuntimeExecutionAuthorization(
        authorization_id="auth",
        gate_id="gate",
        candidate_id="candidate",
        eligibility_id="eligibility",
        scope={},
        created_at="2026-05-24T00:00:00Z",
    )
    service = LocalRuntimeExecutionAuthorizationService()
    assert service.consume_authorization_exactly_once(auth) is True
    assert service.consume_authorization_exactly_once(auth) is False
