"""``--notify`` (never actually opens a media player or rings the bell)."""

import importlib
import unittest
from pathlib import Path
from unittest import mock

from ._support import PACKAGE


class NotificationTests(unittest.TestCase):
    def setUp(self):
        self.module = importlib.import_module(f"{PACKAGE}.notifications.notify")

    def test_normal_roll_beeps(self):
        with mock.patch.object(self.module, "beep") as beep, mock.patch.object(self.module, "play_file") as play:
            self.module.notify(roll=lambda: 42)
        beep.assert_called_once()
        play.assert_not_called()

    def test_rare_roll_plays_the_video(self):
        with mock.patch.object(self.module, "beep") as beep, mock.patch.object(self.module, "play_file", return_value=True) as play:
            self.module.notify(roll=lambda: 1)
        play.assert_called_once()
        beep.assert_not_called()

    def test_missing_video_falls_back_to_the_beep(self):
        with mock.patch.object(self.module, "beep") as beep, mock.patch.object(self.module, "play_file", return_value=False):
            self.module.notify(roll=lambda: 1)
        beep.assert_called_once()

    def test_play_file_refuses_missing_files(self):
        player = importlib.import_module(f"{PACKAGE}.notifications._play_file")
        self.assertFalse(player.play_file(Path("/definitely/not/here.mp4")))
