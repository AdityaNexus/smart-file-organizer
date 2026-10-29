import argparse
import json
from pathlib import Path

from organizer import Organizer
from logger.logging_config import configure_logging


def main(
    source_directory: str | Path = "Downloads",
    destination_directory: str | Path | None = None,
    dry_run: bool = False,
    output_json: bool = False,
    assume_yes: bool = False,
    undo: bool = False,
    show_history: bool = False,
) -> None:
    configure_logging()
    source_directory = Path(source_directory)
    if not source_directory.is_dir():
        raise SystemExit(
            f"Error: Source directory '{source_directory}' does not exist "
            "or is not a directory."
        )
    organizer = Organizer(
        source_directory,
        output_directory=destination_directory,
    )
    if show_history:
        history = organizer.history.read()
        print(json.dumps(history, indent=2) if output_json else history)
        return
    if undo:
        organizer.undo_last_persistent_batch()
        return
    operations = organizer.build_plan()
    organizer.preview_plan(operations)
    if not operations:
        if output_json:
            print(json.dumps({"operations": [], "status": "nothing_to_do"}))
        return

    if dry_run:
        if output_json:
            print(json.dumps({
                "operations": [
                    {
                        "source": str(operation.source),
                        "destination": str(operation.destination),
                    }
                    for operation in operations
                ],
                "status": "dry_run",
            }))
        print("\nDry run complete. No files were moved.")
        return

    choice = "y" if assume_yes else input("Do you want to execute the plan? (y/n): ")
    if choice.lower() == "y":
        results = organizer.execute_plan(operations)
        if output_json:
            print(json.dumps({
                "status": "completed",
                "results": [
                    {
                        "source": str(result.source),
                        "destination": str(result.destination),
                        "status": result.status,
                        "message": result.message,
                    }
                    for result in results
                ],
            }))

    else:
        print("Plan execution canceled.")


def cli() -> None:
    arguments = parse_arguments()
    main(
        arguments.source,
        arguments.destination,
        arguments.dry_run,
        arguments.json,
        arguments.yes,
        arguments.undo,
        arguments.history,
    )


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preview and organize files from a source directory."
    )
    parser.add_argument(
        "source_positional",
        nargs="?",
        help="Legacy positional source directory.",
    )
    parser.add_argument(
        "destination_positional",
        nargs="?",
        help="Legacy positional destination directory.",
    )
    parser.add_argument(
        "--source",
        dest="source_option", #In Python's argparse, dest stands for destination. It specifies the exact variable name (attribute), 
                             # used to store the parsed value on the args object returned by parser.parse_args().
        type=Path,
        help="Directory to scan (default: Downloads).",
    )
    parser.add_argument(
        "--output",
        dest="output_option",
        type=Path,
        help="Destination directory. Defaults to <source>\\organized.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview the plan without moving files.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit a machine-readable result in addition to the human preview.",
    )
    parser.add_argument(
        "--yes",
        action="store_true",
        help="Execute without an interactive confirmation prompt.",
    )
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument(
        "--undo",
        action="store_true",
        help="Undo the most recently persisted successful move batch.",
    )
    actions.add_argument(
        "--history",
        action="store_true",
        help="Show persisted move history.",
    )
    arguments = parser.parse_args()

    if arguments.source_option is not None and arguments.source_positional is not None:
        parser.error("use either --source or a positional source, not both")

    if arguments.output_option is not None and arguments.destination_positional is not None:
        parser.error("use either --output or a positional destination, not both")

    arguments.source = (
        arguments.source_option
        or arguments.source_positional
        or Path("Downloads")
    )
    arguments.destination = (
        arguments.output_option
        or arguments.destination_positional
    )
    return arguments


if __name__ == "__main__":
    cli()