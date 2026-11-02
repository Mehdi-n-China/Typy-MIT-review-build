"""
Typy: a Python-compatible language that compiles to Python.

This package is the compiler. Run it from the directory that *contains* it:

    python -m Typy build my_project/ --enforce

Package map (every sub-package is documented in ``docs/architecture.md``):

    lexer / parser / tree      source text -> Typy AST
    semantics / enforcement    checks and runtime-check injection
    lowering / codegen         Typy AST -> Python source
    runtime                    support code shipped with compiled output
    builder / cli / archive    project builds, commands, .typyexp archives
    tools / errors / logger    shared plumbing
"""
