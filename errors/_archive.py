"""Problems with .typyexp archives."""
from ._base import TypyBaseError

class TypyArchiveError(TypyBaseError):
    """A .typyexp archive could not be created, read or trusted."""
