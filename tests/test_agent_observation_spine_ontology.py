from chanta_core.observation import (
    ACTION_TYPES,
    CONFIDENCE_CLASSES,
    EFFECT_TYPES,
    OBJECT_TYPES,
    RELATION_TYPES,
    AgentObservationSpineService,
)


def test_default_movement_ontology_terms_registered() -> None:
    service = AgentObservationSpineService()
    terms = service.register_movement_ontology_terms()
    by_kind = {term.term_kind for term in terms}
    values = {term.term_value for term in terms}

    assert {"action_type", "object_type", "effect_type", "relation_type", "confidence_class"}.issubset(by_kind)
    assert set(ACTION_TYPES).issubset(values)
    assert set(OBJECT_TYPES).issubset(values)
    assert set(EFFECT_TYPES).issubset(values)
    assert set(RELATION_TYPES).issubset(values)
    assert set(CONFIDENCE_CLASSES).issubset(values)
