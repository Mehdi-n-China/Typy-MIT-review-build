"""time facade: pauses between notification beeps, build timing."""
import time
import types
sleep: types.BuiltinFunctionType = time.sleep
perf_counter: types.BuiltinFunctionType = time.perf_counter
