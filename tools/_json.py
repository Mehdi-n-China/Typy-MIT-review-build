"""json facade: stats counters and archive manifests are stored as JSON."""
import json
import types
load: types.FunctionType = json.load
dump: types.FunctionType = json.dump
loads: types.FunctionType = json.loads
dumps: types.FunctionType = json.dumps
JSONDecodeError: type = json.JSONDecodeError
