"""The monitor itself."""
from typing import Any
import sys
import time

def _name_of(kind: str) -> str:
    return 'established' if kind is None else kind.__name__

class EnforcementMonitor:
    """Counts and prints every enforcement event it is handed."""

    def __init__(self: EnforcementMonitor, entry_point: str, stream: Any=None) -> None:
        self.entry_point = entry_point
        self.stream = stream or sys.stderr
        self.total = self.passed = self.failed = 0
        self.by_name = {}
        self.started = time.time()

    def _line(self: EnforcementMonitor, text: str) -> None:
        print(text, file=self.stream)

    def start(self: EnforcementMonitor) -> None:
        self.started = time.time()
        self._line(f'=== Typy enforcement monitor -- entry point: {self.entry_point} ===')

    def __call__(self: EnforcementMonitor, event: dict) -> None:
        """Called by the runtime for every check."""
        self.total += 1
        stats: dict = self.by_name.setdefault(event['name'], {'checks': 0, 'failures': 0})
        stats['checks'] += 1
        verdict: str = 'ok  '
        if event['ok']:
            self.passed += 1
        else:
            self.failed += 1
            stats['failures'] += 1
            verdict = 'FAIL'
        self._line(f"  {verdict}  {event['name']:<22} kind={event['kind']:<8} expected={_name_of(event['expected']):<12} got={event['actual'].__name__}")

    def finish(self: EnforcementMonitor) -> None:
        """Print the summary (registered to run when the interpreter exits)."""
        self._line('=== enforcement summary ===')
        self._line(f'  checks performed : {self.total}')
        self._line(f'  passed           : {self.passed}')
        self._line(f'  failed           : {self.failed}')
        self._line(f'  elapsed          : {time.time() - self.started:.4f}s')
        failing: list = sorted(((name, s) for name, s in self.by_name.items() if s['failures']), key=lambda item: -item[1]['failures'])
        if failing:
            self._line('  names with failures:')
            for name, stats in failing:
                self._line(f"    {name}: {stats['failures']} of {stats['checks']} check(s) failed")
