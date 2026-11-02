"""
Typy's test-suite (standard library ``unittest`` only).

Run it from the folder that *contains* the ``Typy`` package:

    python -m unittest discover -s Typy/tests -t .

Importing this package points Typy's logger at a throw-away directory, so
running the tests never writes logs or counters into the repository.
"""

import os as _os
import tempfile as _tempfile

_os.environ["TYPY_STATS_DIR"] = _tempfile.mkdtemp(prefix="typy_test_stats_")
