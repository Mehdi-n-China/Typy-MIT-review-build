"""The file handler behind the crash/event log."""
from typing import Any
from .. import tools

def create_file_handler(log_file: tools.path.Path) -> tools.logs.FileHandler:
    """Open ``log_file`` (creating its folders) and wrap it in a handler."""
    log_file.parent.mkdir(parents=True, exist_ok=True)
    handler: Any = tools.logs.FileHandler(log_file, encoding='utf-8')
    handler.setFormatter(tools.logs.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S'))
    return handler
