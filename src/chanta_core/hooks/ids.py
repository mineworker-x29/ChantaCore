from uuid import uuid4


def new_hook_definition_id() -> str:
    return f"hook_definition:{uuid4()}"


def new_hook_invocation_id() -> str:
    return f"hook_invocation:{uuid4()}"


def new_hook_result_id() -> str:
    return f"hook_result:{uuid4()}"


def new_hook_policy_id() -> str:
    return f"hook_policy:{uuid4()}"

