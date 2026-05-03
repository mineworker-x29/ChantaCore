from chanta_core.editing import APPROVAL_PHRASE
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.policy import ToolPolicy
from chanta_core.traces.trace_service import TraceService
from tests.test_edit_tool_patch_application import context, request, setup


def test_patch_application_lifecycle_trace(tmp_path) -> None:
    proposal, patch_service = setup(tmp_path)
    store = OCELStore(tmp_path / "patch_trace.sqlite")
    trace_service = TraceService(ocel_store=store)

    result = ToolDispatcher(
        policy=ToolPolicy(allow_approved_writes=True),
        trace_service=trace_service,
        ocel_store=store,
        patch_application_service=patch_service,
    ).dispatch(request(proposal.proposal_id, APPROVAL_PHRASE), context())

    assert result.success is True
    activities = [event["event_activity"] for event in store.fetch_events_by_session("session-patch-tool")]
    assert "execute_tool_operation" in activities
    assert "complete_tool_operation" in activities
    assert result.output_attrs["patch_application_id"]
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
