"""Printing errors for humans."""
from typing import Any
from .. import tools
from ..errors import TypyCompilationError

def report_error(error: Any) -> None:
    """Print ``error`` to stderr: one ``error:`` line per diagnostic, plus a
    count when a build produced several."""
    stream: Any = tools.sys.stderr
    if isinstance(error, TypyCompilationError):
        files: set = {item.filename for item in error.errors}
        count: int = len(error.errors)
        print(f"build failed: {count} error{'s' if count != 1 else ''} in {len(files)} file(s)", file=stream)
        for item in error.errors:
            print(f'error: {item}', file=stream)
        return
    print(f'error: {error}', file=stream)
