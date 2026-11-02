"""
Builder: turning a ``.typy`` file or a project directory into ``output/``.

A build is all-or-nothing. Every file is compiled first and any error stops
the build before the disk is touched; the output is then assembled in a
temporary staging folder and only copied into place once it is complete.

    _plan                  what to build (files, output folder)
    _walk_project          finding project files, honouring .typyignore
    _compile_files         compile everything, collect every error
    _stage_*               write compiled code and copy resources
    _install_runtime       ship the runtime (and monitor) with the output
    _publish               move the finished build into output/
    _run_build             the sequence above; what ``typy build`` runs

Since: 1.2.0 (staged, atomic builds since 2.0.1)
"""
from ._run_build import run_build
