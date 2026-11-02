"""The ordinary completion beep."""
from .. import tools
from ._constants import BEEP_COUNT, BEEP_GAP_SECONDS

def beep() -> None:
    """Ring the terminal bell ``BEEP_COUNT`` times, pausing between rings
    (but not after the last one, so the command exits promptly)."""
    for ring in range(BEEP_COUNT):
        tools.sys.stdout.write('\x07')
        tools.sys.stdout.flush()
        if ring < BEEP_COUNT - 1:
            tools.clock.sleep(BEEP_GAP_SECONDS)
