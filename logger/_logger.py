"""The Logger class."""
from typing import Any
from .. import tools
from ._handler import create_file_handler
from ._paths import new_log_path, stats_directory
from ._stats_file import bump_stat

class Logger:
    """Event log plus usage counters.

    The log file is created lazily, on the first message, and the counters
    live in ``stats.json`` next to the ``logs/`` folder.
    """

    def __init__(self: Logger) -> None:
        self._logger = tools.logs.getLogger('typy')
        self._logger.setLevel(tools.logs.INFO)
        self._logger.propagate = False
        self._attached = False

    def _emit(self: Logger, level: Any, message: str) -> None:
        if not self._attached:
            self._attached = True
            try:
                self._logger.addHandler(create_file_handler(new_log_path(stats_directory())))
            except OSError:
                return
        self._logger.log(level, message)

    def log(self: Logger, message: str) -> None:
        """Record an ordinary event."""
        self._emit(tools.logs.INFO, message)

    def crash(self: Logger, message: str) -> None:
        """Record an error."""
        self._emit(tools.logs.ERROR, message)

    def increment_stat(self: Logger, name: str, amount: int=1) -> None:
        """Bump the usage counter ``name`` by ``amount``."""
        bump_stat(stats_directory() / 'stats.json', name, amount)
