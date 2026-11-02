"""The literal categories Typy can check at compile time (spec §8)."""
LITERAL_TYPES: frozenset = frozenset({'int', 'float', 'str', 'bool', 'None', 'list', 'tuple', 'set', 'dict', 'bytes', 'complex', 'Ellipsis'})
