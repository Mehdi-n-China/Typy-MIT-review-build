"""One row of the module table."""

class ModuleInfo:
    """A Typy package: its ``name``, what it does, and the ``since`` version
    that introduced it."""

    def __init__(self: ModuleInfo, name: str, summary: str, since: str) -> None:
        self.name = name
        self.summary = summary
        self.since = since
