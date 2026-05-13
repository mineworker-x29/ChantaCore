from chanta_core.skills.registry_view import SkillRegistryViewService


def test_registry_view_keeps_skills_inactive():
    service = SkillRegistryViewService()

    view = service.build_registry_view()
    service.record_result(command_name="list", entries=service.last_entries)

    assert view.view_attrs["skills_executed"] is False
    assert view.view_attrs["skills_enabled"] is False
    assert view.view_attrs["dynamic_registration_used"] is False
    assert service.last_result.result_attrs["skills_executed"] is False
    assert service.last_result.result_attrs["skills_enabled"] is False
    assert all(item.enabled is False for item in service.last_entries)
    assert all(item.execution_enabled is False for item in service.last_entries)


def test_registry_view_has_no_permission_grants_or_runtime_registration():
    service = SkillRegistryViewService()

    view = service.build_registry_view()

    assert view.view_attrs["permission_grants_created"] is False
    assert all(item.entry_attrs.get("runtime_registered") is not True for item in service.last_entries)
