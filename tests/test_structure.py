"""House rules for the code base itself."""

import ast
import unittest

from ..parser import parse_source
from ..tree import FunctionDeclaration
from ._support import PACKAGE_DIR

_SKIP_DIRS = {"__pycache__", "example_project", "tests", ".idea", "source"}


def _modules():
    for path in sorted(PACKAGE_DIR.rglob("*.py")):
        relative = path.relative_to(PACKAGE_DIR)
        if _SKIP_DIRS & set(relative.parts) or relative.as_posix() == "test.py":
            continue
        yield relative, path.read_text(encoding="utf-8")


def _sources():
    for path in sorted((PACKAGE_DIR / "source").rglob("*.typy")):
        yield path.relative_to(PACKAGE_DIR), path.read_text(encoding="utf-8")


class StructureTests(unittest.TestCase):
    def test_at_most_two_functions_per_typy_source(self):
        """The rule is about the code people edit: the Typy sources."""
        for relative, text in _sources():
            program, _ = parse_source(text, relative.as_posix())
            functions = [n.name for n in program.body if isinstance(n, FunctionDeclaration)]
            with self.subTest(source=relative.as_posix()):
                self.assertLessEqual(len(functions), 2, functions)

    def test_every_typy_source_has_a_docstring_or_is_tiny(self):
        for relative, text in _sources():
            program, _ = parse_source(text, relative.as_posix())
            first = program.body[0] if program.body else None
            documented = isinstance(first, ast.Expr) and isinstance(getattr(first, "value", None), ast.Constant)
            with self.subTest(source=relative.as_posix()):
                self.assertTrue(documented or len(text.splitlines()) <= 12)

    def test_at_most_two_functions_per_file(self):
        for relative, text in _modules():
            tree = ast.parse(text)
            functions = [n.name for n in tree.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
            with self.subTest(module=relative.as_posix()):
                self.assertLessEqual(len(functions), 2, functions)

    def test_every_module_has_a_docstring_or_is_tiny(self):
        for relative, text in _modules():
            tree = ast.parse(text)
            with self.subTest(module=relative.as_posix()):
                self.assertTrue(ast.get_docstring(tree) or len(text.splitlines()) <= 12 or not tree.body)

    def test_python_310_compatible_grammar(self):
        for relative, text in _modules():
            with self.subTest(module=relative.as_posix()):
                ast.parse(text, feature_version=(3, 10))

    def test_runtime_does_not_import_the_compiler(self):
        for relative, text in _modules():
            if relative.parts[0] != "runtime":
                continue
            for node in ast.walk(ast.parse(text)):
                if isinstance(node, ast.ImportFrom) and node.level and node.level > 1:
                    self.fail(f"{relative} reaches outside the runtime package")
