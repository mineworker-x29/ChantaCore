from __future__ import annotations

from uuid import uuid4


def new_delegation_packet_id() -> str:
    return f"delegation_packet:{uuid4()}"


def new_delegated_process_run_id() -> str:
    return f"delegated_process_run:{uuid4()}"


def new_delegation_result_id() -> str:
    return f"delegation_result:{uuid4()}"


def new_delegation_link_id() -> str:
    return f"delegation_link:{uuid4()}"


def new_sidechain_context_id() -> str:
    return f"sidechain_context:{uuid4()}"


def new_sidechain_context_entry_id() -> str:
    return f"sidechain_context_entry:{uuid4()}"


def new_sidechain_context_snapshot_id() -> str:
    return f"sidechain_context_snapshot:{uuid4()}"


def new_sidechain_return_envelope_id() -> str:
    return f"sidechain_return_envelope:{uuid4()}"


def new_delegation_conformance_contract_id() -> str:
    return f"delegation_conformance_contract:{uuid4()}"


def new_delegation_conformance_rule_id() -> str:
    return f"delegation_conformance_rule:{uuid4()}"


def new_delegation_conformance_run_id() -> str:
    return f"delegation_conformance_run:{uuid4()}"


def new_delegation_conformance_finding_id() -> str:
    return f"delegation_conformance_finding:{uuid4()}"


def new_delegation_conformance_result_id() -> str:
    return f"delegation_conformance_result:{uuid4()}"
