from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.persona.personal_mode_loadout import PersonalModeLoadoutService
from chanta_core.persona.personal_prompt_activation import PersonalPromptActivationService
from chanta_core.pig.reports import PIGReportService


def _explicit_loadout(store):
    loadouts = PersonalModeLoadoutService(ocel_store=store)
    core = loadouts.register_core_profile(
        profile_name="public_safe_profile",
        profile_type="test",
        identity_statement="Public-safe identity.",
    )
    mode = loadouts.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="public_safe_mode",
        mode_type="test",
        role_statement="Public-safe role.",
    )
    boundary = loadouts.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="capability_boundary",
        boundary_text="Runtime capability profile overrides personal claims.",
    )
    return loadouts.create_mode_loadout(core_profile=core, mode_profile=mode, boundaries=[boundary])


def test_personal_prompt_activation_records_ocel_shape(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadout = _explicit_loadout(store)
    service = PersonalPromptActivationService(ocel_store=store)

    result = service.activate_for_prompt_context(explicit_loadout=loadout)

    assert store.fetch_objects_by_type("personal_prompt_activation_config")
    assert store.fetch_objects_by_type("personal_prompt_activation_request")
    assert store.fetch_objects_by_type("personal_prompt_activation_block")
    assert store.fetch_objects_by_type("personal_prompt_activation_result")
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    assert "personal_prompt_activation_config_loaded" in events
    assert "personal_prompt_activation_requested" in events
    assert "personal_prompt_activation_block_created" in events
    assert "personal_prompt_activation_attached" in events
    relations = store.fetch_object_object_relations_for_object(result.result_id)
    assert any(item["qualifier"] == "belongs_to_activation_request" for item in relations)


def test_personal_prompt_activation_pig_summary_counts(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadout = _explicit_loadout(store)
    service = PersonalPromptActivationService(ocel_store=store)
    service.activate_for_prompt_context(explicit_loadout=loadout)

    object_type_counts = {}
    objects = []
    for object_type in [
        "personal_prompt_activation_config",
        "personal_prompt_activation_request",
        "personal_prompt_activation_block",
        "personal_prompt_activation_result",
        "personal_prompt_activation_finding",
    ]:
        rows = store.fetch_objects_by_type(object_type)
        object_type_counts[object_type] = len(rows)
        for row in rows:
            objects.append(
                type(
                    "Obj",
                    (),
                    {
                        "object_id": row["object_id"],
                        "object_type": row["object_type"],
                        "object_attrs": row["object_attrs"],
                    },
                )()
            )
    event_activity_counts = {}
    for event in store.fetch_recent_events(limit=100):
        activity = event["event_activity"]
        event_activity_counts[activity] = event_activity_counts.get(activity, 0) + 1
    view = OCPXProcessView(
        view_id="view:test",
        source="test",
        session_id=None,
        events=[],
        objects=objects,
    )

    summary = PIGReportService._persona_summary(object_type_counts, event_activity_counts, view)

    assert summary["personal_prompt_activation_config_count"] == 1
    assert summary["personal_prompt_activation_request_count"] == 1
    assert summary["personal_prompt_activation_block_count"] >= 1
    assert summary["personal_prompt_activation_attached_count"] == 1
    assert summary["personal_prompt_activation_prompt_context_only_count"] == 1
