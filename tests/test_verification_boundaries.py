from pathlib import Path


FORBIDDEN_IDENTIFIERS = [
    "subprocess",
    "requests",
    "httpx",
    "socket",
    "os.path.exists(",
    "Path.exists(",
    "shutil.which",
    "PermissionGrant",
    "sandbox",
    "block_tool",
    "outcome_score",
    "process_outcome",
    "read_only_verification_skill",
    "embedding",
    "vector",
]


def test_verification_package_avoids_boundary_violations() -> None:
    root = Path("src/chanta_core/verification")
    core_files = [
        path
        for path in root.glob("*.py")
        if path.name != "read_only_skills.py"
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in core_files)

    for identifier in FORBIDDEN_IDENTIFIERS:
        assert identifier not in text


def test_no_read_only_verification_skill_module_exists() -> None:
    skill_root = Path("src/chanta_core/skills/builtin")
    names = {path.name for path in skill_root.glob("*.py")}

    assert "verify_file_exists.py" not in names
    assert "verify_tool_availability.py" not in names
    assert "runtime_diagnostics.py" not in names
