"""``typy stats``."""
from .. import tools
from ..logger._paths import stats_directory
from ..logger._stats_file import read_stats
from ._stats_table import format_stats

def cmd_stats(args: tools.args.Namespace) -> int:
    """Show (or reset) the usage counters Typy keeps on this machine."""
    stats_dir: tools.path.Path = stats_directory()
    stats_file: tools.path.Path = stats_dir / 'stats.json'
    if args.reset:
        stats_file.parent.mkdir(parents=True, exist_ok=True)
        stats_file.write_text('{}\n', encoding='utf-8')
        print('all counters reset')
        return 0
    stats: dict = read_stats(stats_file)
    if args.json:
        print(tools.json.dumps(stats, indent=4, sort_keys=True))
        return 0
    print('\n'.join(format_stats(stats, stats_dir)))
    return 0
