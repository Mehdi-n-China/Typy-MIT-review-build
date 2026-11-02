"""
Typy standard library (``tools``).

Every piece of the Python standard library the compiler touches is reached
through this package instead of being imported directly. The point is
indirection: compiler code says ``tools.path.Path`` or ``tools.json.load``
and never cares which implementation sits behind the name. When a
Typy-native replacement for one of these modules exists, only the facade
file changes.

Each facade lives in its own private module (``_name.py``) and is exposed
here under a short alias:

    tools.args      argparse            tools.fs        shutil
    tools.date      datetime            tools.zips      zipfile
    tools.io        io                  tools.hashes    hashlib
    tools.json      json                tools.clock     time
    tools.keyword   keyword             tools.env       os (environment)
    tools.logs      logging             tools.procs     subprocess
    tools.path      pathlib             tools.regex     re
    tools.rng       random              tools.temp      tempfile
    tools.sys       sys (live view)     tools.bytecode  py_compile
    tools.tokens    tokenize            tools.apps      zipapp
    tools.pyast     ast                 tools.modes     stat
    tools.copying   copy                tools.iters     itertools
    tools.exit      atexit              tools.trace     traceback
    tools.host      platform            tools.meta      importlib.metadata
    tools.types     types

Since: 1.5.0 (groundwork for self-hosting), extended through 2.3.0.
"""
from . import _argparse as args, _ast as pyast, _atexit as exit, _copy as copying, _datetime as date, _hashlib as hashes, _io as io, _itertools as iters, _json as json, _keyword as keyword, _logging as logs, _metadata as meta, _os as env, _pathlib as path, _platform as host, _py_compile as bytecode, _random as rng, _re as regex, _shutil as fs, _stat as modes, _subprocess as procs, _sys as sys, _tempfile as temp, _time as clock, _tokenize as tokens, _traceback as trace, _types as types, _zipapp as apps, _zipfile as zips
