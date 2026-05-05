class HookError(Exception):
    pass


class HookDefinitionError(HookError):
    pass


class HookInvocationError(HookError):
    pass


class HookResultError(HookError):
    pass


class HookPolicyError(HookError):
    pass


class HookNotFoundError(HookError):
    pass
