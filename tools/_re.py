"""re facade: pattern matching for dotted names and version strings."""
import re
import types
compile: types.FunctionType = re.compile
fullmatch: types.FunctionType = re.fullmatch
Pattern: type = re.Pattern
