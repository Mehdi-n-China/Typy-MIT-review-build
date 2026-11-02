"""pathlib facade: every filesystem path in the compiler is a ``Path``."""
import pathlib
Path: type = pathlib.Path
PurePosixPath: type = pathlib.PurePosixPath
