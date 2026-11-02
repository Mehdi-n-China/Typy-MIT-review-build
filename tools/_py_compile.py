"""py_compile facade: ``--bytecode`` turns generated source into .pyc files."""
import py_compile
import types
compile: types.FunctionType = py_compile.compile
PyCompileError: type = py_compile.PyCompileError
