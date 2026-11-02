"""The CompileContext class."""
from typing import Any

class CompileContext:
    """Everything the stages of a single compilation share.

    ``enforce``        whether ``--enforce`` runtime checks are generated
    ``taken``          every identifier already used in the source, so the
                       names the compiler invents never collide with them
    ``uses_any``       set when generated code needs ``from typing import Any``
    ``needs_runtime``  set when generated code needs the runtime package
    ``runtime_calls``  how many runtime checks were generated
    ``trace``          human-readable notes about each stage (``--veritasium``)
    """

    def __init__(self: CompileContext, filename: str='<typy>', enforce: bool=False, names: Any=()) -> None:
        self.filename = filename
        self.enforce = enforce
        self.taken = set(names)
        self.uses_any = False
        self.needs_runtime = False
        self.runtime_calls = 0
        self.trace = []
        self._counters = {}

    def fresh_name(self: CompileContext, prefix: str) -> str:
        """A new identifier ``<prefix><n>`` that appears nowhere in the file.

        Used for the hidden helpers generated code needs: ``_typy_ch1`` for
        optional-chaining temporaries, ``_typy_state_1`` for ``any`` bindings.
        """
        number: Any = self._counters.get(prefix, 0)
        while True:
            number += 1
            candidate: str = f'{prefix}{number}'
            if candidate not in self.taken:
                break
        self._counters[prefix] = number
        self.taken.add(candidate)
        return candidate

    def note(self: CompileContext, message: str) -> None:
        """Record one line of ``--veritasium`` commentary about this compilation."""
        self.trace.append(message)
