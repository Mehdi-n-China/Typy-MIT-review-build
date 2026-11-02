"""
Names the compiler itself puts into generated code.

None of them can collide with user code: ``typy`` and ``__`` are reserved
terms, ``CHAIN_GUARD`` is rejected by the lexer if the user writes it, and
the runtime module names start with an underscore that user code has no
business importing.
"""
CHAIN_GUARD: str = '__typyg__'
REPEAT_VARIABLE: str = '__'
RUNTIME_MODULE: str = '_typy_runtime'
RUNTIME_ALIAS: str = 'typy'
MONITOR_MODULE: str = '_typy_monitor'
