import inspect

from chanta_core.digestion import ObservationToDigestionAdapterBuilderService
from chanta_core.digestion import adapter_builder


def test_adapter_builder_has_no_external_execution_or_import_path() -> None:
    source = inspect.getsource(adapter_builder)

    forbidden = [
        "execute" + "_adapter",
        "enable" + "_adapter",
        "run" + "_external_harness",
        "execute" + "_external",
        "sub" + "process",
        "os" + ".system",
        "import " + "requests",
        "htt" + "px",
        "connect" + "_mcp",
        "complete" + "_text",
        "complete" + "_json",
        "update" + "_persona",
        "update" + "_overlay",
        "write" + "_memory",
        "mutate" + "_tool_dispatcher",
        "mutate" + "_skill_executor",
    ]
    for token in forbidden:
        assert token not in source

    policy = ObservationToDigestionAdapterBuilderService().create_default_policy()
    assert policy.allow_canonical_skill_import is False
    assert policy.allow_execution_enablement is False
