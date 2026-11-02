"""importlib.metadata facade: versions of installed third-party packages."""
from importlib import metadata
import types
version: types.FunctionType = metadata.version
PackageNotFoundError: type = metadata.PackageNotFoundError
