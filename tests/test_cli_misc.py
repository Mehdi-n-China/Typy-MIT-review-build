"""``typy version``, ``typy stats`` and command-line plumbing."""

import json
import unittest

from .. import __version__
from ..cli._shorthand import inject_default_command
from ._support import make_project, run_cli


class CliTests(unittest.TestCase):
    def test_version(self):
        code, out, _ = run_cli("version")
        self.assertEqual(code, 0)
        self.assertIn(f"Typy {__version__.version}", out)

    def test_version_modules(self):
        _, out, _ = run_cli("version", "--modules")
        for fragment in ("Modules:", "parser", "since 2.1.0", "Dependencies:", "pathspec"):
            self.assertIn(fragment, out)

    def test_stats_reset_count_and_json(self):
        run_cli("stats", "--reset")
        run_cli("build", make_project({"a.typy": "int x = 1\n"}))
        _, out, _ = run_cli("stats", "--json")
        stats = json.loads(out)
        self.assertEqual(stats["builds"], 1)
        _, out, _ = run_cli("stats")
        self.assertIn("builds completed", out)

    def test_shorthand(self):
        self.assertEqual(inject_default_command(["proj/"]), ["build", "proj/"])
        self.assertEqual(inject_default_command(["build", "proj/"]), ["build", "proj/"])
        self.assertEqual(inject_default_command(["--help"]), ["--help"])
        self.assertEqual(inject_default_command(["stats"]), ["stats"])
