"""Shared helpers for the tests."""

import contextlib
import importlib
import io
import os
import sys
import tempfile
from pathlib import Path

from ..cli import cli
from ..compiler import compile_source

PACKAGE = __package__.rsplit(".", 1)[0]          # "Typy" (or whatever the folder is called)
PACKAGE_DIR = Path(__file__).resolve().parent.parent


def use_runtime():
    """Make ``import _typy_runtime`` resolve to this checkout's runtime."""
    sys.modules["_typy_runtime"] = importlib.import_module(f"{PACKAGE}.runtime.typy")


def compile_ok(source, enforce=False):
    """Compile ``source`` and fail loudly if it does not compile."""
    result = compile_source(source, "test.typy", enforce)
    if not result.ok:
        raise AssertionError("unexpected compile error:\n" + "\n".join(str(e) for e in result.errors))
    return result


def compile_errors(source, enforce=False):
    """Compile ``source`` and return the error messages (empty if it compiled)."""
    return [str(error) for error in compile_source(source, "test.typy", enforce).errors]


def run_typy(source, enforce=False):
    """Compile and execute ``source``; return the resulting namespace."""
    result = compile_ok(source, enforce)
    if result.needs_runtime:
        use_runtime()
    namespace = {"__name__": "__typy_test__"}
    exec(compile(result.python_code, "test.py", "exec"), namespace)
    return namespace


def run_cli(*argv):
    """Run ``typy`` in-process; return ``(exit_code, stdout, stderr)``."""
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        code = cli.main([str(arg) for arg in argv])
    return code, out.getvalue(), err.getvalue()


def make_project(files):
    """A temporary project folder holding ``files`` ({relative path: text})."""
    root = Path(tempfile.mkdtemp(prefix="typy_test_")) / "project"
    for relative, text in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return root


def python_env():
    """Environment for running built programs in a subprocess."""
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    return env
