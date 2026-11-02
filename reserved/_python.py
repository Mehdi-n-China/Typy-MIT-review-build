"""
Python-native keywords, hard and soft (``match``, ``case``, ``type``, ``_``).

Soft keywords are only keywords in certain positions, so most code should
prefer ``PY_HARD_KEYWORDS``; this set exists for the places that really do
want every word Python gives special treatment.
"""
from .. import tools
PY_KEYWORDS: frozenset = frozenset(tools.keyword.kwlist) | frozenset(tools.keyword.softkwlist)
