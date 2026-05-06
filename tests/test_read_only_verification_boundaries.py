from pathlib import Path


FORBIDDEN_IDENTIFIERS = [
    "subprocess",
    "os.system",
    "requests",
    "httpx",
    "socket",
    "write_text",
    "open(",
    "unlink",
    "chmod",
    "mkdir",
    "rmdir",
    "PermissionGrant",
    "sandbox",
    "ToolDispatcher.dispatch",
    "outcome_score",
    "process_outcome",
    "load_mcp",
    "load_plugin",
    "importlib",
]


def test_read_only_verification_skills_avoid_forbidden_behavior() -> None:
    text = Path("src/chanta_core/verification/read_only_skills.py").read_text(encoding="utf-8")

    for identifier in FORBIDDEN_IDENTIFIERS:
        assert identifier not in text
