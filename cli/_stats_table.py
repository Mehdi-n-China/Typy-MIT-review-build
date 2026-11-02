"""Formatting the ``typy stats`` report."""
from typing import Any
from .. import tools
from ._stat_labels import STAT_LABELS

def format_stats(stats: dict, stats_dir: tools.path.Path) -> list:
    """The report as a list of lines: known counters first in a fixed order,
    then any others, then a summary of the log files."""
    lines: list = [f'Typy usage statistics ({stats_dir})', '']
    names: list = [name for name in STAT_LABELS if name in stats] + sorted((n for n in stats if n not in STAT_LABELS))
    if not names:
        lines.append('  nothing recorded yet -- go build something')
    for name in names:
        label: Any = STAT_LABELS.get(name, name)
        lines.append(f"  {label + ' ':.<34} {stats[name]}")
    logs: list = sorted((stats_dir / 'logs').rglob('*.log')) if (stats_dir / 'logs').is_dir() else []
    size_kb: float = sum((log.stat().st_size for log in logs)) / 1024
    lines += ['', f"  {'log files ':.<34} {len(logs)} ({size_kb:.1f} KB)"]
    return lines
