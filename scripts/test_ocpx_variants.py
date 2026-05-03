from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader


def main() -> None:
    store = OCELStore()
    view = OCPXLoader(store).load_recent_view(limit=20)
    variant = OCPXEngine().compute_variant_summary(view)

    print("variant_key:", variant.variant_key)
    print("event_count:", len(variant.activity_sequence))
    print("trace_count:", variant.trace_count)
    print("success_count:", variant.success_count)
    print("failure_count:", variant.failure_count)
    print("skill_ids:", variant.skill_ids)
    print("example_process_instance_ids:", variant.example_process_instance_ids)


if __name__ == "__main__":
    main()
