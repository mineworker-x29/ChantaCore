from chanta_core.observation_digest.models import ExternalSkillAssimilationCandidate
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.registry_view import SkillRegistryEntry, SkillRegistryViewService
from chanta_core.utility.time import utc_now_iso


def test_registry_view_includes_observation_and_digestion_seed_skills():
    service = SkillRegistryViewService()

    view = service.build_registry_view()

    observation = [item for item in service.last_entries if item.skill_layer == "internal_observation"]
    digestion = [item for item in service.last_entries if item.skill_layer == "internal_digestion"]
    assert view.observation_skill_count == 5
    assert view.digestion_skill_count == 5
    assert len(observation) == 5
    assert len(digestion) == 5


def test_registry_filters_observation_and_digestion_layers():
    service = SkillRegistryViewService()
    service.build_registry_view()

    observation = service.apply_filter(skill_layer="internal_observation")
    digestion = service.apply_filter(skill_layer="internal_digestion")

    assert {item.skill_layer for item in observation} == {"internal_observation"}
    assert {item.skill_layer for item in digestion} == {"internal_digestion"}


def test_external_candidate_defaults_pending_review_and_disabled():
    candidate = ExternalSkillAssimilationCandidate(
        candidate_id="external_skill_assimilation_candidate:demo",
        source_runtime="dummy_runtime",
        source_skill_ref="dummy_source_skill",
        source_kind="external_skill",
        static_profile_id="external_skill_static_profile:demo",
        behavior_fingerprint_id=None,
        proposed_chantacore_skill_id="skill:dummy_source_skill",
        proposed_execution_type="review_only_candidate",
        adapter_candidate_ids=[],
        risk_class="read_only",
        confidence=0.5,
        evidence_refs=[],
        created_at=utc_now_iso(),
    )
    service = SkillRegistryViewService()

    view = service.build_registry_view(external_candidates=[candidate])
    external = [item for item in service.last_entries if item.skill_layer == "external_candidate"]

    assert view.external_candidate_count == 1
    assert external[0].status == "pending_review"
    assert external[0].enabled is False
    assert external[0].execution_enabled is False


def test_risk_and_observability_renderers_work():
    service = SkillRegistryViewService()
    service.build_registry_view()

    risk_text = service.render_registry_risk_view()
    observability_text = service.render_registry_observability_view()

    assert "read_only=10" in risk_text
    assert "ocel_observable=true" in observability_text
    assert "pig_visible=true" in observability_text


def test_missing_contract_and_unsafe_enabled_findings():
    service = SkillRegistryViewService()
    view = service.build_registry_view()
    bad_entry = SkillRegistryEntry(
        registry_entry_id="skill_registry_entry:bad",
        registry_view_id=view.registry_view_id,
        skill_id="skill:bad_fixture",
        skill_name="Bad Fixture",
        description="Public fixture entry.",
        skill_layer="internal_observation",
        skill_origin="test_fixture",
        capability_category="observation",
        risk_class="read_only",
        status="enabled",
        enabled=True,
        execution_enabled=False,
        proposal_enabled=True,
        review_required=False,
        gate_required=False,
        envelope_required=False,
        audit_visible=True,
        workbench_visible=True,
        ocel_observable=True,
        pig_visible=True,
        source_ref=None,
        created_at=utc_now_iso(),
    )

    service._check_entry_contract(bad_entry)

    finding_types = {item.finding_type for item in service.last_findings}
    assert "missing_contract" in finding_types
    assert "unsafe_enabled" in finding_types


def test_skill_registry_pig_counts_are_visible():
    view = OCPXProcessView(
        view_id="view:demo",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView(
                object_id="entry:observation",
                object_type="skill_registry_entry",
                object_attrs={
                    "skill_layer": "internal_observation",
                    "skill_origin": "chantacore_internal",
                    "risk_class": "read_only",
                    "status": "candidate",
                    "enabled": False,
                },
            ),
            OCPXObjectView(
                object_id="entry:digestion",
                object_type="skill_registry_entry",
                object_attrs={
                    "skill_layer": "internal_digestion",
                    "skill_origin": "chantacore_internal",
                    "risk_class": "read_only",
                    "status": "candidate",
                    "enabled": False,
                },
            ),
            OCPXObjectView(
                object_id="finding:demo",
                object_type="skill_registry_finding",
                object_attrs={"finding_type": "missing_contract"},
            ),
        ],
    )

    summary = PIGReportService._skill_registry_summary(
        {"skill_registry_entry": 2, "skill_registry_finding": 1},
        {"skill_registry_view_created": 1},
        view,
    )

    assert summary["skill_registry_entry_count"] == 2
    assert summary["skill_registry_observation_skill_count"] == 1
    assert summary["skill_registry_digestion_skill_count"] == 1
    assert summary["skill_registry_missing_contract_finding_count"] == 1
    assert summary["skill_registry_by_layer"]["internal_observation"] == 1
