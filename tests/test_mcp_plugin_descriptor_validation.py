from chanta_core.external import MCPPluginDescriptorSkeletonService
from chanta_core.external.ids import new_external_descriptor_skeleton_id
from chanta_core.external.mcp_plugin import ExternalDescriptorSkeleton
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


def _service(tmp_path) -> MCPPluginDescriptorSkeletonService:
    return MCPPluginDescriptorSkeletonService(
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "mcp_plugin_validation.sqlite"))
    )


def _skeleton() -> ExternalDescriptorSkeleton:
    return ExternalDescriptorSkeleton(
        skeleton_id=new_external_descriptor_skeleton_id(),
        skeleton_type="plugin",
        source_id=None,
        external_descriptor_id=None,
        mcp_server_id=None,
        plugin_id="plugin_descriptor:test",
        normalized_name="sample_plugin",
        normalized_kind="python",
        declared_permission_categories=["network_access"],
        declared_risk_categories=["network_access"],
        review_status="pending_review",
        activation_status="disabled",
        execution_enabled=False,
        created_at=utc_now_iso(),
        skeleton_attrs={"entrypoint_ref": "sample_plugin:register"},
    )


def test_valid_skeleton_passes(tmp_path) -> None:
    service = _service(tmp_path)
    validation = service.validate_skeleton(skeleton=_skeleton())

    assert validation.status == "passed"
    assert "name_present" in validation.passed_checks
    assert "kind_present" in validation.passed_checks
    assert "entrypoint_metadata_only" in validation.passed_checks


def test_missing_name_yields_failed_validation(tmp_path) -> None:
    service = _service(tmp_path)
    skeleton = _skeleton()
    object.__setattr__(skeleton, "normalized_name", None)

    validation = service.validate_skeleton(skeleton=skeleton)

    assert validation.status == "failed"
    assert "name_present" in validation.failed_checks


def test_enabled_fixture_fails_validation_without_mutation(tmp_path) -> None:
    service = _service(tmp_path)
    skeleton = _skeleton()
    object.__setattr__(skeleton, "execution_enabled", True)

    validation = service.validate_skeleton(skeleton=skeleton)

    assert validation.status == "failed"
    assert "execution_disabled" in validation.failed_checks
    assert skeleton.execution_enabled is True


def test_active_fixture_fails_validation_without_mutation(tmp_path) -> None:
    service = _service(tmp_path)
    skeleton = _skeleton()
    object.__setattr__(skeleton, "activation_status", "active")

    validation = service.validate_skeleton(skeleton=skeleton)

    assert validation.status == "failed"
    assert "activation_disabled" in validation.failed_checks
    assert skeleton.activation_status == "active"
