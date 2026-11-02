"""platform facade: which interpreter and operating system we are on."""
import platform
import types
system: types.FunctionType = platform.system
python_version: types.FunctionType = platform.python_version
python_implementation: types.FunctionType = platform.python_implementation
