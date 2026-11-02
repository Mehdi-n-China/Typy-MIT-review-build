"""Reading and updating the ``stats.json`` counters."""
from typing import Any
from .. import tools

def read_stats(stats_file: tools.path.Path) -> dict:
    """All counters as a dict; an absent or damaged file reads as empty."""
    try:
        with stats_file.open('r', encoding='utf-8') as handle:
            data: Any = tools.json.load(handle)
    except (OSError, tools.json.JSONDecodeError):
        return {}
    return data if isinstance(data, dict) else {}

def bump_stat(stats_file: tools.path.Path, name: str, amount: int=1) -> None:
    """Add ``amount`` to counter ``name``. Stats are best-effort: a read-only
    disk must never break a build, so write failures are swallowed."""
    stats: dict = read_stats(stats_file)
    stats[name] = stats.get(name, 0) + amount
    try:
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        with stats_file.open('w', encoding='utf-8') as handle:
            tools.json.dump(stats, handle, indent=4, sort_keys=True)
    except OSError:
        pass
