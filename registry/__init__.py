"""
The module registry behind ``typy version --modules``.

A single table listing every Typy package with a one-line summary and the
release that introduced it, plus the third-party packages Typy depends on.

Since: 2.2.0
"""
from ._dependencies import installed_dependencies
from ._module_info import ModuleInfo
from ._modules import MODULES
