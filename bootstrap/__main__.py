"""``python -m typy.bootstrap [--check]``: rebuild Typy with itself."""
from .. import tools
from ._rebuild import rebuild
if __name__ == '__main__':
    tools.sys.exit(rebuild('--check' in tools.sys.argv[1:]))
