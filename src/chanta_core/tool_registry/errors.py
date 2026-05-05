class ToolRegistryError(Exception):
    pass


class ToolDescriptorError(ToolRegistryError):
    pass


class ToolRegistrySnapshotError(ToolRegistryError):
    pass


class ToolPolicyNoteError(ToolRegistryError):
    pass


class ToolRiskAnnotationError(ToolRegistryError):
    pass


class ToolRegistryViewError(ToolRegistryError):
    pass
