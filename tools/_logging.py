"""logging facade: the crash/event log is written through these classes."""
import logging
import types
getLogger: types.FunctionType = logging.getLogger
FileHandler: type = logging.FileHandler
Formatter: type = logging.Formatter
INFO: int = logging.INFO
ERROR: int = logging.ERROR
