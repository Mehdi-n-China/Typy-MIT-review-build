"""
Typy error classes.

Every failure the compiler can report is a ``TypyBaseError`` subclass, so the
command line can catch one type, print a clean message and exit with a
non-zero status instead of dumping a traceback on the user.

    syntax            TypySyntaxError, TypyIndentationError, TypyChainError
    semantics         TypyReservedIdentifierError, TypyUndeclaredVariableError,
                      TypyTypeMismatchError, TypyVoidError
    whole-file        TypyCompilationError (several diagnostics at once)
    build / projects  TypyFlagConflict, TypyNotAllowedToOverride,
                      TypyProjectError, TypyArchiveError
    compiler bugs     TypyInternalError

Since: 1.2.0 (typed errors), extended in 2.1.0 (semantic diagnostics).
"""
from ._archive import TypyArchiveError
from ._base import TypyBaseError
from ._chain import TypyChainError
from ._compilation import TypyCompilationError
from ._declaration import TypyTypeMismatchError, TypyUndeclaredVariableError
from ._flags import TypyFlagConflict
from ._internal import TypyInternalError
from ._override import TypyNotAllowedToOverride
from ._project import TypyProjectError
from ._semantic import TypyReservedIdentifierError, TypySemanticError
from ._syntax import TypyIndentationError, TypySyntaxError
from ._void import TypyVoidError
