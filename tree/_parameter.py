"""One entry of a typed parameter list."""
from typing import Any
from ._base import TypyNode
from ._render_default import render_default

class ParameterKind:
    """What a parameter-list entry is.

    ``NORMAL``  ``TYPE name [= default]``
    ``SLASH``   the ``/`` marker: everything before it is positional-only
    ``STAR``    the bare ``*`` marker: everything after it is keyword-only
    ``VARARG``  ``*TYPE name``: collects extra positional arguments
    ``KWARG``   ``**TYPE name``: collects extra keyword arguments
    """
    NORMAL: str = 'normal'
    SLASH: str = 'slash'
    STAR: str = 'star'
    VARARG: str = 'vararg'
    KWARG: str = 'kwarg'

class Parameter(TypyNode):
    """A parameter of a typed function signature.

    ``type`` is a ``TypeRef`` (``None`` for the ``/`` and ``*`` markers, which
    are not typed). ``default`` is an expression node or ``None``. For
    ``VARARG`` / ``KWARG`` the type is the type of each *element*, exactly as
    in a Python annotation ``*args: int``.
    """
    _fields: tuple = ('name', 'type', 'default', 'kind')

    def __init__(self: Parameter, name: Any=None, type: Any=None, default: Any=None, kind: Any=ParameterKind.NORMAL) -> None:
        self.name = name
        self.type = type
        self.default = default
        self.kind = kind

    @property
    def is_marker(self: Parameter) -> bool:
        return self.kind in (ParameterKind.SLASH, ParameterKind.STAR)

    @property
    def formatted(self: Parameter) -> Any:
        """Python-side rendering: ``name: type`` plus `` = default`` if any."""
        if self.is_marker:
            return self.name
        prefix: Any = {ParameterKind.VARARG: '*', ParameterKind.KWARG: '**'}.get(self.kind, '')
        text: str = f'{prefix}{self.name}: {self.type.text}'
        if self.default is not None:
            text += f' = {render_default(self.default)}'
        return text

    def __add__(self: Parameter, other: Any) -> Any:
        """``parameter + parameter`` builds a ``ParameterVector`` (see
        ``Typy.formatting``), a convenient way to assemble signatures."""
        from ..formatting import ParameterVector
        return ParameterVector([self]) + other

    def __repr__(self: Parameter) -> str:
        return f'Parameter({self.formatted!r})'
