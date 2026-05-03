from __future__ import annotations

from chanta_core.ocel.external_import import ExternalOCELIngestionService
from chanta_core.ocel.external_source import ExternalOCELSource
from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader


def main() -> None:
    store = OCELStore()
    source = ExternalOCELSource(
        source_id="script-source",
        source_name="Script Source",
        source_type="manual_test_log",
        source_format="chanta_ocel_json",
        source_attrs={},
    )
    raw_record = {
        "event": {
            "event_id": "evt-script-1",
            "event_activity": "external_script_event",
            "event_timestamp": "2026-05-03T00:00:00Z",
            "event_attrs": {},
        },
        "objects": [
            {
                "object_id": "case-script-1",
                "object_type": "case",
                "object_attrs": {"display_name": "Script case"},
            }
        ],
        "relations": [
            {
                "relation_kind": "event_object",
                "source_id": "evt-script-1",
                "target_id": "case-script-1",
                "qualifier": "case_context",
                "relation_attrs": {},
            }
        ],
    }
    result = ExternalOCELIngestionService(store=store).ingest_records(
        source,
        [raw_record],
    )
    view = OCPXLoader(store).load_recent_view(limit=5)

    print("ingestion_result:", result.to_dict())
    print("event_count:", store.fetch_event_count())
    print("object_count:", store.fetch_object_count())
    print("recent_activities:", OCPXEngine().activity_sequence(view))


if __name__ == "__main__":
    main()
