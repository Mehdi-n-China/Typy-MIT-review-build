"""Printing function signatures."""
from typing import Any
from ..tree import FunctionDeclaration, ParameterKind, render_default
from ._parameter_vector import ParameterVector

class Formatter:
    """Static helpers that print signatures."""

    @staticmethod
    def function(name: str, parameters: Any, return_type: Any, is_async: bool=False) -> str:
        """The Python header the compiler generates for a typed function:
        ``def add(a: int, b: int = 5) -> int``."""
        vector: Any = parameters if isinstance(parameters, ParameterVector) else ParameterVector(parameters)
        keyword: str = 'async def' if is_async else 'def'
        return f'{keyword} {name}({vector.formatted}) -> {_python_return(return_type)}'

    @staticmethod
    def signature(declaration: FunctionDeclaration) -> str:
        """A ``FunctionDeclaration`` in Typy's own syntax:
        ``int add(int a, int b = 5)``."""
        parts: list = []
        for parameter in declaration.signature.parameters:
            if parameter.is_marker:
                parts.append(parameter.name)
                continue
            star: Any = {ParameterKind.VARARG: '*', ParameterKind.KWARG: '**'}.get(parameter.kind, '')
            text: str = f'{star}{parameter.type.text} {parameter.name}'
            if parameter.default is not None:
                text += f' = {render_default(parameter.default)}'
            parts.append(text)
        prefix: str = 'async ' if declaration.is_async else ''
        return f"{prefix}{declaration.signature.returns.text} {declaration.name}({', '.join(parts)})"

def _python_return(return_type: Any) -> str:
    """``void`` has no Python spelling; it is printed as ``None``."""
    text: Any = return_type.text if hasattr(return_type, 'text') else str(return_type)
    return 'None' if text == 'void' else text
