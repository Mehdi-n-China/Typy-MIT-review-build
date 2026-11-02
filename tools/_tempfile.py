"""tempfile facade: staging directories for all-or-nothing builds."""
import tempfile
import types
TemporaryDirectory: type = tempfile.TemporaryDirectory
mkdtemp: types.FunctionType = tempfile.mkdtemp
