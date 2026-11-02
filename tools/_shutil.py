"""shutil facade: copying and removing build output."""
import shutil
import types
copyfile: types.FunctionType = shutil.copyfile
copy2: types.FunctionType = shutil.copy2
copytree: types.FunctionType = shutil.copytree
rmtree: types.FunctionType = shutil.rmtree
move: types.FunctionType = shutil.move
ignore_patterns: types.FunctionType = shutil.ignore_patterns
