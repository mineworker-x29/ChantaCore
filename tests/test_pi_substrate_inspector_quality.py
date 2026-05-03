from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.inspector import PISubstrateInspector


def test_pi_substrate_inspector_text_has_operator_sections(tmp_path) -> None:
    store = OCELStore(tmp_path / "inspection.sqlite")
    inspector = PISubstrateInspector(
        ocel_store=store,
        ocpx_loader=OCPXLoader(store=store),
    )

    inspection = inspector.inspect(limit=10)

    for section in [
        "OCEL",
        "OCPX",
        "PIG",
        "Skills",
        "Tools",
        "Worker Queue",
        "Scheduler",
        "Editing / Patch",
        "Conformance",
        "Warnings",
    ]:
        assert section in inspection.inspection_text
    assert isinstance(inspection.warnings, list)
    assert inspection.to_dict()["inspection_attrs"]["read_only"] is True
