from tempfile import TemporaryDirectory

from chanta_core.external import ExternalOCELImportCandidateService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def main() -> int:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = OCELStore(f"{temp_dir}/external_ocel_script.sqlite")
        service = ExternalOCELImportCandidateService(trace_service=TraceService(ocel_store=store))
        source = service.register_source(
            source_name="script provided dict",
            source_type="provided_dict",
            trust_level="untrusted",
        )
        descriptor, validation, preview, candidate = service.register_as_candidate(
            payload={
                "events": [
                    {"id": "e1", "activity": "start", "timestamp": "2026-01-01T00:00:00Z"},
                    {"id": "e2", "activity": "finish", "timestamp": "2026-01-01T00:01:00Z"},
                ],
                "objects": [{"id": "o1", "type": "case"}],
                "relations": [{"type": "event_object", "event_id": "e1", "object_id": "o1"}],
            },
            source=source,
            payload_name="script external ocel",
        )

        assert candidate.candidate_status == "pending_review"
        assert candidate.review_status == "pending_review"
        assert candidate.merge_status == "not_merged"
        assert candidate.canonical_import_enabled is False
        print("descriptor", descriptor.descriptor_id, descriptor.payload_kind)
        print("validation", validation.validation_id, validation.status)
        print("preview", preview.preview_id, preview.event_count, preview.object_count, preview.relation_count)
        print("candidate", candidate.candidate_id, candidate.merge_status, candidate.canonical_import_enabled)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
