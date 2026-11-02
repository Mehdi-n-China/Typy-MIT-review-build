"""``typy export`` / ``typy import`` and the .typyexp format."""

import hashlib
import json
import unittest
import zipfile

from ..archive import extract_archive
from ..errors import TypyArchiveError
from ._support import make_project, run_cli


class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.root = make_project({
            "main.typy": "print(1)\n", "assets/a.txt": "a", ".typyignore": "*.log\n", "x.log": "no",
            "__pycache__/junk.pyc": "", "output/old.py": "",
        })

    def test_round_trip(self):
        self.assertEqual(run_cli("export", self.root)[0], 0)
        archive = self.root.parent / "project.typyexp"
        destination = self.root.parent / "copy"
        self.assertEqual(run_cli("import", archive, "-o", destination)[0], 0)
        found = sorted(p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file())
        self.assertEqual(found, [".typyignore", "assets/a.txt", "main.typy"])

    def test_both_directions_refuse_to_overwrite(self):
        run_cli("export", self.root)
        self.assertEqual(run_cli("export", self.root)[0], 1)
        self.assertEqual(run_cli("export", self.root, "--override")[0], 0)
        archive = self.root.parent / "project.typyexp"
        target = self.root.parent / "again"
        run_cli("import", archive, "-o", target)
        self.assertEqual(run_cli("import", archive, "-o", target)[0], 1)
        (target / "extra.txt").write_text("gone after override")
        self.assertEqual(run_cli("import", archive, "-o", target, "--override")[0], 0)
        self.assertFalse((target / "extra.txt").exists())

    def _rewrite(self, transform):
        run_cli("export", self.root)
        source = self.root.parent / "project.typyexp"
        tampered = self.root.parent / "tampered.typyexp"
        with zipfile.ZipFile(source) as zin, zipfile.ZipFile(tampered, "w") as zout:
            for item in zin.infolist():
                name, data = transform(item.filename, zin.read(item.filename))
                if name:
                    zout.writestr(name, data)
        return tampered

    def test_tampering_is_detected(self):
        tampered = self._rewrite(lambda n, d: (n, b"evil" if n.endswith("main.typy") else d))
        target = self.root.parent / "t1"
        target.mkdir()
        with self.assertRaises(TypyArchiveError):
            extract_archive(tampered, target)

    def test_unlisted_files_are_rejected(self):
        tampered = self._rewrite(lambda name, data: (name, data))
        with zipfile.ZipFile(tampered, "a") as archive:
            archive.writestr("project/stowaway.py", "import os")
        target = self.root.parent / "t2"
        target.mkdir()
        with self.assertRaises(TypyArchiveError):
            extract_archive(tampered, target)

    def test_zip_slip_is_blocked(self):
        evil = self.root.parent / "evil.typyexp"
        with zipfile.ZipFile(evil, "w") as archive:
            digest = hashlib.sha256(b"x").hexdigest()
            archive.writestr("typyexp.json", json.dumps({"format": 1, "typy": "2.3.9", "files": [{"path": "../escape.txt", "size": 1, "sha256": digest}]}))
            archive.writestr("project/../escape.txt", b"x")
        target = self.root.parent / "t3"
        target.mkdir()
        with self.assertRaises(TypyArchiveError):
            extract_archive(evil, target)
        self.assertFalse((self.root.parent / "escape.txt").exists())

    def test_not_an_archive(self):
        bogus = self.root.parent / "bogus.typyexp"
        bogus.write_text("not a zip")
        code, _, err = run_cli("import", bogus)
        self.assertEqual(code, 1)
        self.assertIn("not a valid", err)
