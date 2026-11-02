"""os facade: environment variables and the Windows-only ``startfile``."""
from typing import Any
import os
import types
environ: Any = os.environ
getenv: types.FunctionType = os.getenv
startfile: Any = getattr(os, 'startfile', None)
walk: types.FunctionType = os.walk
