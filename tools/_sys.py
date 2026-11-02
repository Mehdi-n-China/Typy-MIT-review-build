"""
sys facade: a *live* view of the ``sys`` module.

``sys.stderr``, ``sys.argv`` and friends get reassigned at runtime (tests and
shells redirect them), so binding them to names at import time would freeze
the original objects. Module-level ``__getattr__`` forwards every lookup to
the real module instead, so ``tools.sys.stderr`` is always current.
"""
from typing import Any
import sys as _sys

def __getattr__(name: str) -> Any:
    return getattr(_sys, name)
