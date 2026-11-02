"""Typy is written in Typy: the package is its own sources, compiled by itself."""

import contextlib
import importlib
import io
import unittest

from ._support import PACKAGE, PACKAGE_DIR


class SelfHostingTests(unittest.TestCase):
    def test_package_is_a_fixpoint_of_its_sources(self):
        """Compiling ``source/`` with the running compiler reproduces every
        module of the package byte for byte, and no module lacks a source."""
        rebuild = importlib.import_module(f"{PACKAGE}.bootstrap._rebuild").rebuild
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            status = rebuild(check=True)
        self.assertEqual(status, 0, out.getvalue() + err.getvalue())

    def test_sources_contain_no_python_definitions(self):
        for path in (PACKAGE_DIR / "source").rglob("*.typy"):
            with self.subTest(source=path.relative_to(PACKAGE_DIR).as_posix()):
                for line in path.read_text(encoding="utf-8").splitlines():
                    self.assertFalse(line.lstrip().startswith(("def ", "async def ")), line)

    def test_stage_zero_is_still_retired(self):
        self.assertEqual((PACKAGE_DIR / "bootstrap" / "_stage0.py").read_text(), "# so long nerds\n")
        self.assertFalse((PACKAGE_DIR / "source" / "bootstrap" / "_stage0.typy").exists())
