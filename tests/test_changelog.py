"""The release history stays consistent with the code and the schedule."""

import ast
import datetime
import re
import unittest

from .. import __version__
from ..registry import MODULES
from ._support import PACKAGE_DIR

_HEADING = re.compile(r"^## \[(\d+\.\d+\.\d+)\] - (\d{4}-\d{2}-\d{2})(?: \(hotfix\))?$", re.M)
_SINCE = re.compile(r"^Since: (\d+\.\d+\.\d+)", re.M)


def _version(text):
    return tuple(int(part) for part in text.split("."))


def _releases():
    text = (PACKAGE_DIR / "CHANGELOG.md").read_text(encoding="utf-8")
    found = [(_version(v), datetime.date.fromisoformat(d), m.start()) for m in _HEADING.finditer(text) for v, d in [m.groups()]]
    sections = {}
    for index, (version, _, start) in enumerate(found):
        end = found[index + 1][2] if index + 1 < len(found) else len(text)
        sections[version] = text[start:end]
    return [(version, date) for version, date, _ in found], sections


class ChangelogTests(unittest.TestCase):
    def setUp(self):
        self.releases, self.sections = _releases()
        self.versions = {version for version, _ in self.releases}

    def test_latest_release_is_the_installed_version(self):
        version, date = self.releases[0]
        self.assertEqual(version, _version(__version__.version))
        self.assertEqual(date.isoformat(), __version__.released)

    def test_versions_and_dates_only_go_forward(self):
        ordered = list(reversed(self.releases))
        for (old_version, old_date), (new_version, new_date) in zip(ordered, ordered[1:]):
            self.assertLess(old_version, new_version)
            self.assertLess(old_date, new_date)

    def test_minor_releases_follow_the_quarterly_schedule(self):
        for version, date in self.releases:
            if version[2] == 0 and version != (2, 0, 0):
                with self.subTest(version=version):
                    self.assertEqual(date.day, 15)
                    self.assertIn(date.month, (3, 6, 9, 12))

    def test_every_quarter_had_a_release(self):
        dates = {date for _, date in self.releases}
        first, last = min(dates), max(dates)
        for year in range(first.year, last.year + 1):
            for month in (3, 6, 9, 12):
                quarter = datetime.date(year, month, 15)
                if first <= quarter <= last:
                    self.assertIn(quarter, dates, f"no release on {quarter}")

    def test_patches_sit_between_their_minor_and_the_next(self):
        minors = sorted((v, d) for v, d in self.releases if v[2] == 0)
        for version, date in self.releases:
            if version[2] == 0:
                continue
            base = dict(minors)[(version[0], version[1], 0)]
            following = [d for v, d in minors if v > version]
            with self.subTest(version=version):
                self.assertGreater(date, base)
                if following:
                    self.assertLess(date, min(following))

    def test_self_hosting(self):
        date = dict(self.releases)[(2, 0, 0)]
        self.assertEqual((date.month, date.day), (8, 1))
        self.assertIn("self-hosted", self.sections[(2, 0, 0)])
        self.assertEqual((PACKAGE_DIR / "bootstrap" / "_stage0.py").read_text(), "# so long nerds\n")

    def test_module_registry_matches_the_packages(self):
        packages = {
            path.parent.name for path in PACKAGE_DIR.glob("*/__init__.py")
            if path.parent.name not in ("tests", "example_project")
        }
        modules = {info.name for info in MODULES} - {"packaging"}  # packaging is a single module
        self.assertEqual(packages, modules)
        for info in MODULES:
            with self.subTest(module=info.name):
                self.assertIn(_version(info.since), self.versions)

    def test_since_notes_name_real_releases(self):
        for path in PACKAGE_DIR.glob("*/__init__.py"):
            docstring = ast.get_docstring(ast.parse(path.read_text(encoding="utf-8"))) or ""
            match = _SINCE.search(docstring)
            if path.parent.name in ("tests", "example_project"):
                continue
            with self.subTest(package=path.parent.name):
                self.assertIsNotNone(match, "package docstring has no 'Since:' line")
                self.assertIn(_version(match.group(1)), self.versions)
