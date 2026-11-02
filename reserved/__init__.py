"""
Reserved words.

Four families of words are special to the compiler:

* ``RESERVED_TERMS``     identifiers user code may never *define* (spec §4)
* ``STATEMENT_KEYWORDS`` the words that open Typy-only statements
* ``PSEUDO_TYPES``       Typy's own types: ``any``, ``dyn``, ``void``
* ``PY_KEYWORDS`` / ``PY_HARD_KEYWORDS``  Python's own reserved words

plus the compiler-internal names in ``_internal`` that generated code uses.

Since: 0.1.0 (``__`` replaced ``_`` as the compiler-owned name in 2.2.0).
"""
from ._hard_python import PY_HARD_KEYWORDS
from ._internal import CHAIN_GUARD, MONITOR_MODULE, REPEAT_VARIABLE, RUNTIME_ALIAS, RUNTIME_MODULE
from ._pseudo import PSEUDO_TYPES
from ._python import PY_KEYWORDS
from ._statements import STATEMENT_KEYWORDS
from ._terms import RESERVED_TERMS
