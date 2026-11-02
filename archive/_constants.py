"""Fixed names of the .typyexp format (format version 1)."""
ARCHIVE_SUFFIX: str = '.typyexp'
MANIFEST_NAME: str = 'typyexp.json'
PAYLOAD_DIR: str = 'project'
FORMAT_VERSION: int = 1
EXCLUDED_DIRECTORIES: frozenset = frozenset({'__pycache__', '.git', '.hg', '.svn', '.idea', '.vscode', '.venv', 'venv', 'node_modules', '.mypy_cache', '.pytest_cache'})
