from chanta_core.tools.registry import ToolRegistry
from chanta_core.tools.request import ToolRequest
from chanta_core.tools.risk import ToolRiskClassifier
from chanta_core.tools.tool import Tool


def request(tool_id: str, operation: str = "run", **attrs) -> ToolRequest:
    return ToolRequest.create(
        tool_id=tool_id,
        operation=operation,
        process_instance_id="process_instance:risk",
        session_id="session-risk",
        agent_id="agent-risk",
        input_attrs=attrs,
    )


def test_known_builtin_tool_risks() -> None:
    registry = ToolRegistry()
    classifier = ToolRiskClassifier()

    assert classifier.classify(registry.require("tool:echo"), request("tool:echo")).risk_level == "readonly"
    assert classifier.classify(registry.require("tool:ocel"), request("tool:ocel")).risk_level == "internal_readonly"
    assert classifier.classify(registry.require("tool:ocpx"), request("tool:ocpx")).risk_level == "internal_compute"
    assert classifier.classify(registry.require("tool:pig"), request("tool:pig")).risk_level == "internal_intelligence"
    assert classifier.classify(registry.require("tool:workspace"), request("tool:workspace")).risk_level == "internal_readonly"
    assert classifier.classify(registry.require("tool:repo"), request("tool:repo")).risk_level == "internal_readonly"
    assert classifier.classify(registry.require("tool:worker"), request("tool:worker")).risk_level == "internal_compute"


def test_unknown_tool_risk_unknown() -> None:
    tool = Tool("tool:unknown", "unknown", "Unknown", "custom", "unknown", ["run"])

    risk = ToolRiskClassifier().classify(tool, request("tool:unknown"))

    assert risk.risk_level == "unknown"


def test_risky_operation_names_classified() -> None:
    tool = Tool("tool:test", "test", "Test", "custom", "readonly", ["delete_file", "run_shell"])
    classifier = ToolRiskClassifier()

    assert classifier.classify(tool, request("tool:test", "delete_file")).risk_level == "dangerous"
    assert classifier.classify(tool, request("tool:test", "run_shell")).risk_level == "shell"


def test_explicit_risk_level_uses_stricter_risk() -> None:
    tool = Tool("tool:test", "test", "Test", "custom", "readonly", ["run"])

    risk = ToolRiskClassifier().classify(
        tool,
        request("tool:test", risk_level="write"),
    )

    assert risk.risk_level == "write"
