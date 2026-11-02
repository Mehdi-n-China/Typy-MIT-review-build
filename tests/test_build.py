"""``typy build`` end to end."""

import subprocess
import sys
import unittest

from ._support import make_project, python_env, run_cli

_MAIN = "import pkg.util\nint value = pkg.util.double(21)\nprint(value)\n"
_UTIL = "int double(int n):\n    return n * 2\n"


class BuildTests(unittest.TestCase):
    def project(self, **extra):
        files = {"main.typy": _MAIN, "pkg/util.typy": _UTIL, "assets/data.txt": "data\n", ".typyignore": "*.log\n", "debug.log": "x"}
        files.update(extra)
        return make_project(files)

    def run_output(self, path):
        done = subprocess.run([sys.executable, str(path)], capture_output=True, text=True, env=python_env())
        return done.returncode, done.stdout, done.stderr

    def test_project_build(self):
        root = self.project()
        code, out, _ = run_cli("build", root)
        self.assertEqual(code, 0, out)
        files = sorted(p.relative_to(root / "output").as_posix() for p in (root / "output").rglob("*") if p.is_file())
        self.assertEqual(files, ["__init__.py", "assets/data.txt", "main.py", "pkg/__init__.py", "pkg/util.py"])
        self.assertEqual(self.run_output(root / "output" / "main.py")[1].strip(), "42")

    def test_override_protection(self):
        root = self.project()
        run_cli("build", root)
        code, _, err = run_cli("build", root)
        self.assertEqual(code, 1)
        self.assertIn("--override", err)
        self.assertEqual(run_cli("build", root, "--override")[0], 0)

    def test_failed_build_writes_nothing(self):
        root = self.project(**{"broken.typy": "x = 1\n", "also.typy": "def f():\n    pass\n"})
        code, _, err = run_cli("build", root)
        self.assertEqual(code, 1)
        self.assertIn("2 errors in 2 file(s)", err)
        self.assertFalse((root / "output").exists())

    def test_lightweight(self):
        root = self.project()
        run_cli("build", root, "--lightweight")
        self.assertFalse((root / "output" / "assets").exists())

    def test_single_file_and_shorthand(self):
        root = make_project({"one.typy": 'print("solo")\n'})
        self.assertEqual(run_cli(root / "one.typy")[0], 0)
        self.assertEqual(self.run_output(root / "output" / "one.py")[1].strip(), "solo")

    def test_enforce_ships_the_runtime(self):
        root = self.project()
        run_cli("build", root, "--enforce")
        self.assertTrue((root / "output" / "_typy_runtime" / "_check.py").is_file())
        self.assertFalse((root / "output" / "_typy_monitor").exists())
        self.assertEqual(self.run_output(root / "output" / "main.py")[1].strip(), "42")

    def test_bytecode(self):
        root = self.project()
        run_cli("build", root, "--bytecode")
        self.assertTrue((root / "output" / "main.pyc").is_file())
        self.assertFalse((root / "output" / "main.py").exists())
        self.assertEqual(self.run_output(root / "output" / "main.pyc")[1].strip(), "42")

    def test_standalone(self):
        root = self.project()
        code, out, _ = run_cli("build", root, "--standalone", "--enforce")
        self.assertEqual(code, 0, out)
        archive = root / "output" / "project.pyz"
        self.assertEqual([p.name for p in (root / "output").iterdir()], ["project.pyz"])
        self.assertEqual(self.run_output(archive)[1].strip(), "42")

    def test_standalone_needs_an_entry_point(self):
        root = make_project({"lib.typy": "int x = 1\n"})
        code, _, err = run_cli("build", root, "--standalone")
        self.assertEqual(code, 1)
        self.assertIn("entry point", err)

    def test_bytecode_and_standalone_conflict(self):
        code, _, err = run_cli("build", self.project(), "--bytecode", "--standalone")
        self.assertEqual(code, 1)
        self.assertIn("--bytecode, --standalone", err)

    def test_typy_and_py_with_the_same_name_conflict(self):
        root = self.project(**{"pkg/util.py": "x = 1\n"})
        code, _, err = run_cli("build", root)
        self.assertEqual(code, 1)
        self.assertIn("would overwrite", err)

    def test_bad_targets(self):
        root = self.project()
        for target in (root / "assets" / "data.txt", root / "missing", make_project({"a.txt": "x"})):
            with self.subTest(target=target):
                self.assertEqual(run_cli("build", target)[0], 1)

    def test_veritasium_reports_every_stage(self):
        _, out, _ = run_cli("build", self.project(), "--veritasium", "--enforce")
        for fragment in ("[veritasium] compiling main.typy", "function int double(int n)", "runtime check(s) generated", "installed the runtime"):
            self.assertIn(fragment, out)

    def test_gui_monitor_observes_every_file(self):
        root = self.project()
        run_cli("build", root, "--enforce", "--gui")
        code, out, err = self.run_output(root / "output" / "main.py")
        self.assertEqual(out.strip(), "42")
        self.assertIn("Typy enforcement monitor", err)
        self.assertIn("double() return", err)  # a check made inside pkg/util.py
        self.assertIn("enforcement summary", err)

    def test_gui_without_enforce_is_ignored_with_a_note(self):
        root = self.project()
        _, out, _ = run_cli("build", root, "--gui")
        self.assertIn("ignoring --gui", out)
        self.assertFalse((root / "output" / "_typy_monitor").exists())
