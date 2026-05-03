class ToolValidationError(ValueError):
    pass


class ToolRegistryError(RuntimeError):
    pass


class ToolAuthorizationError(RuntimeError):
    pass


class ToolDispatchError(RuntimeError):
    pass
