"""Tunables of the notification."""
from .. import tools
RICKROLL_PATH: tools.path.Path = tools.path.Path(__file__).resolve().parent.parent / 'assets' / 'rickroll.mp4'
ROLL_SIDES: int = 69
BEEP_COUNT: int = 3
BEEP_GAP_SECONDS: float = 1.0
