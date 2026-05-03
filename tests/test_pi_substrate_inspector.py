from chanta_core.ocel.store import OCELStore
from chanta_core.pig.inspector import PISubstrateInspection, PISubstrateInspector
from tests.test_ocel_store import make_record


def test_pi_substrate_inspector_returns_readable_inspection(tmp_path) -> None:
    store = OCELStore(tmp_path / "pi_substrate.sqlite")
    store.append_record(make_record())

    inspection = PISubstrateInspector(ocel_store=store).inspect(limit=20)
    data = inspection.to_dict()

    assert isinstance(inspection, PISubstrateInspection)
    assert "PI Substrate" in inspection.inspection_text
    assert "event_count" in inspection.ocel_summary
    assert "object_count" in inspection.ocel_summary
    assert "activity_sequence" in inspection.ocpx_summary
    assert "skill_ids" in inspection.skill_summary
    assert "tool_ids" in inspection.tool_summary
    assert isinstance(inspection.warnings, list)
    assert data["inspection_text"] == inspection.inspection_text
