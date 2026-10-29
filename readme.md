# Smart File Organizer

A safe, preview-first command-line application that organizes files by
extension. It scans a source directory, builds a move plan, previews the
changes, and only moves files after confirmation.

> **Project status:** Early release

## Features

- Recursively scans a source directory.
- Excludes the selected output directory from future scans.
- Classifies files using case-insensitive extension rules.
- Creates category folders automatically.
- Previews every proposed move before execution.
- Never overwrites an existing destination.
- Handles duplicate names with suffixes such as `report_1.pdf`.
- Supports `--dry-run`, `--yes`, and optional JSON output.
- Persists successful move batches in an atomic JSON history file.
- Supports CLI history lookup and persistent undo.
- Provides an installable `smart-organizer` command.

## Categories

Rules are defined in [`config.json`](./config.json).

| Extensions | Category |
| --- | --- |
| `.pdf`, `.docx`, `.txt`, `.md` | `Documents` |
| `.png`, `.jpg`, `.jpeg`, `.gif` | `Images` |
| `.py`, `.java`, `.cpp`, `.js` | `Code` |
| `.zip`, `.rar`, `.7z` | `Archives` |
| `.csv`, `.xlsx`, `.xls` | `Spreadsheets` |
| `.mp4`, `.mkv`, `.avi` | `Videos` |
| Any other extension | `Others` |

## Requirements

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/) recommended

## Installation and development

Clone the repository and enter the project directory:

```powershell
git clone <your-repository-url>
cd "Smart file organizer"
```

Synchronize the development environment:

```powershell
uv sync --group dev
```

This installs the project and development tools such as pytest into the
project environment.

## Usage

The canonical command is:

```powershell
uv run smart-organizer
```

By default, it scans `Downloads` and writes categorized files to
`Downloads\organized`.

### Preview without moving files

```powershell
uv run smart-organizer --source Downloads --dry-run
```

### Preview as JSON

```powershell
uv run smart-organizer --source Downloads --dry-run --json
```

### Organize with confirmation

```powershell
uv run smart-organizer --source Downloads
```

Enter `y` after reviewing the proposed moves.

### Organize without a prompt

```powershell
uv run smart-organizer --source Downloads --yes
```

Use `--yes` carefully because it executes the plan automatically.

### Use custom source and output paths

Quote Windows paths that contain spaces:

```powershell
uv run smart-organizer `
    --source "C:\FilesToOrganize" `
    --output "C:\OrganizedFiles" `
    --dry-run
```

The output directory can be anywhere, including outside the source directory.
If it is inside the source directory, it is excluded from scanning.

### View persistent history

```powershell
uv run smart-organizer `
    --source "C:\FilesToOrganize" `
    --output "C:\OrganizedFiles" `
    --history `
    --json
```

History is stored at:

```text
<output>\.organizer-history.json
```

Always use the same `--output` path that was used for the original move.

### Undo the latest successful batch

```powershell
uv run smart-organizer `
    --source "C:\FilesToOrganize" `
    --output "C:\OrganizedFiles" `
    --undo
```

Undo validates that destination files still exist and that the original source
paths are free before moving files back.

### Legacy entry points

The canonical command is preferred, but these forms remain supported:

```powershell
uv run python main.py --source Downloads --dry-run
uv run python main2.py --source Downloads --dry-run
```

`main2.py` delegates to the same implementation as `main.py`.

## Python API

```python
from organizer import Organizer

organizer = Organizer(
    root_directory=r"C:\FilesToOrganize",
    output_directory=r"C:\OrganizedFiles",
)
operations = organizer.build_plan()
organizer.preview_plan(operations)
```

## Testing

Run the complete test suite:

```powershell
uv run python -m pytest
```

Run one test file:

```powershell
uv run python -m pytest test/test_organizer.py
```

GitHub Actions also runs the tests on Python 3.10, 3.11, 3.12, and 3.13.
The workflow is [`ci.yml`](./.github/workflows/ci.yml).

## Building and installing

Build distributable artifacts:

```powershell
uv build
```

The wheel and source archive are written to `dist/`. To test-install the
wheel locally:

```powershell
uv pip install .\dist\smart_file_organizer-0.1.0-py3-none-any.whl
```

The project is configured in [`pyproject.toml`](./pyproject.toml), which
defines the package metadata, build backend, included modules, dependencies,
and `smart-organizer` console command.

## Project structure

```text
.
├── main.py                 # Canonical CLI entry point
├── main2.py                # Compatibility entry point
├── organizer.py            # Coordinates the workflow
├── FIle_scanner.py         # Recursively discovers files
├── File_item.py            # File metadata wrapper
├── Rule_engine.py          # Maps extensions to categories
├── config.json             # Extension-to-category rules
├── move_planner.py         # Builds proposed moves
├── file_mover.py           # Executes moves and reports results
├── history.py              # Persists successful move batches
├── undo_manager.py         # In-process undo support
├── pyproject.toml          # Packaging and tool configuration
├── uv.lock                 # Locked development dependencies
├── .github/
│   └── workflows/
│       └── ci.yml          # GitHub Actions CI workflow
├── schemas/
│   └── MoveResult.py       # Move result model
└── test/                   # Automated tests
```

## Safety behavior and limitations

The default behavior is conservative:

- A plan is shown before files are moved.
- Confirmation is required unless `--yes` is supplied.
- Existing destinations are skipped rather than overwritten.
- Failed operations are reported and logged.
- The output tree is excluded from future scans.
- Persistent undo refuses to overwrite an existing source file.

Classification is extension-based and does not inspect file contents. The
project is designed for ordinary personal directories; very large trees should
be benchmarked before using it as a batch service.

## License

The project metadata declares the MIT License. Add the full MIT license text
to a `LICENSE` file before redistributing the project publicly.
