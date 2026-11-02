"""zipapp facade: ``--standalone`` packs a build into one runnable archive."""
import zipapp
import types
create_archive: types.FunctionType = zipapp.create_archive
