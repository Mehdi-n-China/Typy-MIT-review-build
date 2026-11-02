"""random facade: ``rng.int(a, b)`` is an inclusive random integer."""
import random
import types
int: types.MethodType = random.randint
