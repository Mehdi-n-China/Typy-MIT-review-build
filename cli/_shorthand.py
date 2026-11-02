"""``typy <target>`` as a shorthand for ``typy build <target>``."""
COMMANDS: frozenset = frozenset({'build', 'export', 'import', 'stats', 'version'})

def inject_default_command(argv: list) -> list:
    """Insert ``build`` when the first argument is a target, not a command.

    The spec shows ``typy program.typy`` and ``typy project/``; anything that
    is not a known command and not an option is taken as a build target, so
    ``typy build ...``, ``typy --help`` and friends are unaffected.
    """
    if argv and argv[0] not in COMMANDS and (not argv[0].startswith('-')):
        return ['build'] + list(argv)
    return list(argv)
