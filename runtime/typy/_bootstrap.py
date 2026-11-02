"""Starting the optional monitor."""
from typing import Any
import os
import sys

def _entry_label() -> str:
    """A readable name for the program's entry point."""
    main: Any = sys.modules.get('__main__')
    path: Any = getattr(main, '__file__', None) or (sys.argv[0] if sys.argv and sys.argv[0] else '<interactive>')
    label: Any = os.path.basename(path)
    if label == '__main__.py':
        label = os.path.basename(os.path.dirname(path)) or label
    return label

def start_monitor_if_configured(package_name: str) -> None:
    """If this build was made with ``--gui``, attach the monitor now.

    The monitor package ships next to the runtime as ``_typy_monitor``. Any
    problem is reported and ignored: monitoring never changes whether the
    program runs.
    """
    try:
        from . import _config
        if not _config.GUI:
            return
        import _typy_monitor
        _typy_monitor.attach(sys.modules[package_name], _entry_label())
    except Exception as error:
        print(f'typy: enforcement monitor unavailable ({error})', file=sys.stderr)
