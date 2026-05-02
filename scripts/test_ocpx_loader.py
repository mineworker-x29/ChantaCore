from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader


def main() -> None:
    loader = OCPXLoader()
    view = loader.load_recent_view(limit=20)
    engine = OCPXEngine()
    print("view_id:", view.view_id)
    print("event_count:", len(view.events))
    print("object_count:", len(view.objects))
    print("activity_counts:", engine.count_events_by_activity(view))


if __name__ == "__main__":
    main()
