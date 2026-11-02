"""subprocess facade: launching the system media player for ``--notify``."""
import subprocess
import types
Popen: type = subprocess.Popen
run: types.FunctionType = subprocess.run
DEVNULL: int = subprocess.DEVNULL
