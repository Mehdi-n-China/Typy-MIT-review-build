"""
The Typy AST.

As of 2.1.0 Typy has its own, officially supported syntax tree. It is
*Python's* ``ast`` extended rather than replaced: every ordinary Python
construct is still an ordinary ``ast`` node, and every construct that exists
only in Typy is an instance of one of the classes below. They subclass
``ast.stmt`` / ``ast.expr`` / ``ast.AST``, so ``ast.walk``, ``ast.dump`` and
``ast.NodeVisitor`` all work on a mixed tree, and a Typy node can sit
anywhere a Python node of the same kind can.

    statements    TypedDeclaration  FunctionDeclaration  Conditional
                  UntilLoop  ForeverLoop  RepeatLoop  InitializedLoop
    expressions   OptionalChain
    auxiliary     TypeRef  Parameter  Signature  Branch  LoopBinding  ChainLink
    root          Program

The tree is built by ``Typy.parser``, checked by ``Typy.semantics``, optionally
rewritten by ``Typy.enforcement`` and finally *lowered* to plain Python nodes
by ``Typy.lowering``. Nothing Typy-specific survives lowering. See
``docs/ast.md`` for the full node reference.

Since: 2.1.0
"""
from ._branch import Branch
from ._chain_link import ChainLink
from ._child_blocks import child_blocks, is_scope_node
from ._conditional import Conditional
from ._forever_loop import ForeverLoop
from ._function_declaration import FunctionDeclaration
from ._initialized_loop import InitializedLoop
from ._loop_binding import LoopBinding
from ._map_blocks import map_blocks
from ._optional_chain import OptionalChain
from ._parameter import Parameter, ParameterKind
from ._place import place
from ._program import Program
from ._render_default import render_default
from ._repeat_loop import RepeatLoop
from ._signature import Signature
from ._type_ref import TypeRef
from ._typed_declaration import TypedDeclaration
from ._until_loop import UntilLoop
