"""A large program mixing every kind of Python statement with Typy syntax."""

import contextlib
import io
import unittest
from pathlib import Path

from ._support import compile_ok, use_runtime

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "stress.typy"
_EXPECTED = [
    "5.0 6765 {'a': 2, 'b': 1} [0, 2, 4, 6] [0, 1, 4, 9]",
    "point at 5 list starting 1 (+2) origin something",
    "5 []",
]


class StressTests(unittest.TestCase):
    def run_fixture(self, enforce):
        result = compile_ok(_FIXTURE.read_text(encoding="utf-8"), enforce=enforce)
        compile(result.python_code, "stress.py", "exec")  # valid Python
        if result.needs_runtime:
            use_runtime()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile(result.python_code, str(_FIXTURE), "exec"), {"__name__": "__main__", "__file__": str(_FIXTURE)})
        return output.getvalue().splitlines()

    def test_runs_the_same_with_and_without_enforcement(self):
        plain = self.run_fixture(False)
        enforced = self.run_fixture(True)
        self.assertEqual(plain[:3], _EXPECTED)
        self.assertEqual(plain, enforced)
