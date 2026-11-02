"""atexit facade: callbacks that run when the interpreter shuts down."""
import atexit
import types
register: types.BuiltinFunctionType = atexit.register
