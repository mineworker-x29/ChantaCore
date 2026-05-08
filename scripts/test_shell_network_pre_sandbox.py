from __future__ import annotations

from tempfile import TemporaryDirectory
from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.sandbox import ShellNetworkRiskPreSandboxService
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    with TemporaryDirectory(ignore_cleanup_errors=True) as temp_dir:
        store = OCELStore(Path(temp_dir) / "shell_network_pre_sandbox.sqlite")
        service = ShellNetworkRiskPreSandboxService(trace_service=TraceService(ocel_store=store))

        safe_intent = service.create_shell_command_intent(command_text="echo hello", shell_type="powershell")
        safe_decision = service.evaluate_shell_command_intent(intent=safe_intent)

        destructive_intent = service.create_shell_command_intent(command_text="rm -rf ./data", shell_type="bash")
        destructive_decision = service.evaluate_shell_command_intent(intent=destructive_intent)

        network_intent = service.create_network_access_intent(url="https://example.com", method="GET")
        network_decision = service.evaluate_network_access_intent(intent=network_intent)

        print("safe_intent_id:", safe_intent.intent_id)
        print("safe_decision:", safe_decision.decision, safe_decision.risk_level, safe_decision.enforcement_enabled)
        print("destructive_intent_id:", destructive_intent.intent_id)
        print(
            "destructive_decision:",
            destructive_decision.decision,
            destructive_decision.risk_level,
            destructive_decision.enforcement_enabled,
        )
        print("destructive_violation_ids:", destructive_decision.violation_ids)
        print("network_intent_id:", network_intent.intent_id)
        print("network_decision:", network_decision.decision, network_decision.risk_level, network_decision.enforcement_enabled)


if __name__ == "__main__":
    main()
