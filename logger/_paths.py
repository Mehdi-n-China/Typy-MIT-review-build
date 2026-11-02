"""Where Typy keeps its logs and counters."""
from typing import Any
from .. import tools

def stats_directory() -> tools.path.Path:
    """Directory holding ``stats.json`` and the ``logs/`` tree.

    Defaults to ``stats/`` next to the package; set ``TYPY_STATS_DIR`` to put
    it somewhere else (the test-suite does, to keep the repository clean).
    """
    override: Any = tools.env.getenv('TYPY_STATS_DIR')
    if override:
        return tools.path.Path(override)
    return tools.path.Path(__file__).resolve().parent.parent / 'stats'

def new_log_path(stats_dir: tools.path.Path) -> tools.path.Path:
    """A fresh ``logs/YYYY/MM/DD/HH-MM-SS-ffffff.log`` path under ``stats_dir``."""
    now: Any = tools.date.now()
    return stats_dir / 'logs' / f'{now.year}' / f'{now.month:02d}' / f'{now.day:02d}' / f"{now.strftime('%H-%M-%S-%f')}.log"
