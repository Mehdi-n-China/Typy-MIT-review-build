"""
Typy-specific types.

``any``  the type is *immutable*: whatever type the first value has becomes
         the binding's type, and later assignments must match it exactly.
``dyn``  the type is *mutable*: anything may be assigned at any time and
         nothing is ever enforced.
``void`` a return type only; the function produces no value at all.
"""
PSEUDO_TYPES: frozenset = frozenset({'any', 'dyn', 'void'})
