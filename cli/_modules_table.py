"""Formatting ``typy version --modules``."""
from typing import Any
from ..registry import MODULES, installed_dependencies

def format_modules() -> list:
    """Every Typy module with its summary and introducing version, followed
    by the third-party dependencies and their installed versions."""
    width: Any = max((len(info.name) for info in MODULES))
    lines: list = ['', 'Modules:']
    for info in MODULES:
        lines.append(f'  {info.name:<{width}}  since {info.since:<6}  {info.summary}')
    lines += ['', 'Dependencies:']
    for name, version in installed_dependencies():
        lines.append(f"  {name:<{width}}  {version or 'NOT INSTALLED'}")
    return lines
