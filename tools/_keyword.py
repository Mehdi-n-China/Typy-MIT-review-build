"""keyword facade: the set of words Python itself reserves."""
import keyword
import types
kwlist: list = keyword.kwlist
softkwlist: list = keyword.softkwlist
iskeyword: types.BuiltinFunctionType = keyword.iskeyword
