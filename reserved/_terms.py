"""
Typy reserved terms (spec §4).

User code can never *define* one of these names: no assignment target, no
parameter, no function or class name, no loop variable, and so on. Merely
*referencing* them is allowed, which is why Python's builtin ``any(...)``
keeps working even though ``any`` is reserved as a Typy type.

``__`` (two underscores) is compiler-owned: ``repeat N:`` lowers to
``for __ in range(N):``. A single ``_`` is an ordinary identifier again
(``for _ in range(3)``, ``x, _ = pair`` and friends all work), which is the
whole reason ``__`` took over this job in 2.2.0. Longer names such as
``_temp`` or ``__internal`` were never affected.
"""
RESERVED_TERMS: frozenset = frozenset({'__', 'any', 'dyn', 'void', 'repeat', 'unless', 'elunless', 'forever', 'until', 'typy'})
