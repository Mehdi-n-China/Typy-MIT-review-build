"""Shipping the runtime with the build."""
from .. import tools
from ..reserved import MONITOR_MODULE, RUNTIME_MODULE
from ._reporter import Reporter
_RUNTIME_SOURCE: tools.path.Path = tools.path.Path(__file__).resolve().parent.parent / 'runtime'
_SKIP: tools.types.FunctionType = tools.fs.ignore_patterns('__pycache__', '*.pyc')

def install_runtime(staging: tools.path.Path, gui: bool, report: Reporter) -> None:
    """Copy the runtime into ``staging`` as ``_typy_runtime/``.

    With ``gui`` the build also ships the monitor as ``_typy_monitor/`` and
    flips the runtime's build-time switch (in the *copy*), so the monitor
    starts the moment the program first imports the runtime.
    """
    destination: tools.path.Path = staging / RUNTIME_MODULE
    tools.fs.copytree(_RUNTIME_SOURCE / 'typy', destination, ignore=_SKIP)
    report.step(f'installed the runtime as {RUNTIME_MODULE}/')
    if gui:
        (destination / '_config.py').write_text('GUI = True\n', encoding='utf-8')
        tools.fs.copytree(_RUNTIME_SOURCE / 'monitor', staging / MONITOR_MODULE, ignore=_SKIP)
        report.step(f'installed the enforcement monitor as {MONITOR_MODULE}/')
