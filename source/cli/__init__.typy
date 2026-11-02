"""
Typy command-line interface.

    typy build <target> [--enforce [--gui]] [--override] [--bytecode | --standalone]
                        [--lightweight] [--veritasium] [--notify]
        Compile a .typy file or a project directory into <target>/output/
        (a single file builds into the output/ folder next to it). All or
        nothing: if any file fails to compile, nothing is written. Refuses
        to replace an existing output/ unless --override is given.

    typy <target> [...]
        Shorthand for ``typy build <target> [...]``.

    typy export <project> [-o FILE] [--override]
        Package a project as <project>.typyexp for easier sharing.

    typy import <file.typyexp> [-o DIR] [--override]
        Unpack an archive back into a project folder, verifying every file.

    typy stats [--json] [--reset]
        Show what Typy has done on this machine.

    typy version [--modules]
        Show the installed Typy version (and every module with --modules).

Every command lives in its own module (``_build``, ``_export``...);
``cli.main`` parses arguments and turns Typy errors into clean messages and
exit codes (0 success, 1 error, 2 usage, 130 interrupted).

Since: 0.1.0 (export/import/stats/version since 2.2.0)
"""
