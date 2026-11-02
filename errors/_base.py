"""Typy base error."""
from typing import Any
from ..logger import logger

class TypyBaseError(Exception):
    """Root of every error the compiler raises on purpose.

    Carries an optional source location (``filename``, ``line``, ``col``) and
    an optional ``hint`` telling the user how to fix the problem. ``line`` is
    1-based and ``col`` is 0-based, matching Python's own tokenizer and
    ``ast`` conventions; ``__str__`` shows the column 1-based like an editor.
    Errors that are not about source code (a flag clash, an existing output
    folder) carry no location and print as the bare message.

    Creating an error also writes it to the crash log, which is what feeds
    ``typy stats`` and makes post-mortems possible.
    """

    def __init__(self: Any, message: str, line: Any=None, col: Any=None, filename: Any=None, hint: Any=None) -> None:
        self.message = message
        self.line = line
        self.col = col
        self.filename = filename
        self.hint = hint
        logger.crash(message)
        super().__init__(str(self))

    def __str__(self: Any) -> str:
        text: str = self.message
        if self.filename is not None or self.line is not None:
            error_path: Any = self.filename or '<typy>'
            if self.line is not None:
                error_path += f':line-{self.line}'
                if self.col is not None:
                    error_path += f':col-{self.col + 1}'
            text = f'{error_path}: {self.message}'
        if self.hint:
            text += f'\n  hint: {self.hint}'
        return text
