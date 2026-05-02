from __future__ import annotations

import pytest

from chanta_core.skills.errors import SkillValidationError
from chanta_core.skills.skill import Skill


def valid_skill(**overrides) -> Skill:
    values = {
        "skill_id": "skill:test",
        "skill_name": "test",
        "description": "Test skill.",
        "execution_type": "test",
        "input_schema": {},
        "output_schema": {},
        "tags": ["test"],
        "skill_attrs": {},
    }
    values.update(overrides)
    return Skill(**values)


def test_valid_skill_passes_validation() -> None:
    valid_skill().validate()


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("skill_id", ""),
        ("skill_id", "test"),
        ("skill_name", ""),
        ("execution_type", ""),
        ("input_schema", []),
        ("output_schema", []),
        ("tags", ["ok", 1]),
        ("skill_attrs", []),
    ],
)
def test_invalid_skill_contract_fails(field: str, value) -> None:
    with pytest.raises(SkillValidationError):
        valid_skill(**{field: value}).validate()
