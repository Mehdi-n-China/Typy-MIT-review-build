# The `.typyexp` archive format (format 1)

A `.typyexp` file is a zip archive (deflate) with this layout:

```text
typyexp.json            the manifest
project/<path>          one entry per project file, "/" separators
```

## Manifest

```json
{
  "format": 1,
  "typy": "2.3.9",
  "name": "my_project",
  "created": "2026-10-29T14:03:11Z",
  "files": [
    {"path": "main.typy", "size": 120, "sha256": "9f2c..."}
  ]
}
```

| Field | Meaning |
| --- | --- |
| `format` | Archive format version; readers refuse formats they do not know. |
| `typy` | Version of Typy that wrote the archive. Importing an archive from a newer Typy prints a note. |
| `name` | The exported folder's name. |
| `created` | UTC time of the export (ISO 8601). |
| `files` | Every file in the payload: path relative to the project, size in bytes, SHA-256 of the contents. |

## Reading rules

`typy import` rejects an archive when:

- it is not a zip file, or `typyexp.json` is missing or malformed;
- a listed file is missing or its size or SHA-256 differs;
- the payload holds a file the manifest does not list;
- a path is absolute, contains `..`, a backslash or a drive letter, or would
  resolve outside the destination.

Extraction happens in a temporary folder; the destination is only created (or
replaced, with `--override`) after every check has passed.
