"""traceback facade: crash reports for unexpected internal errors."""
import traceback
import types
format_exc: types.FunctionType = traceback.format_exc
