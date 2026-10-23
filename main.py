import argparse
from pathlib import Path

from organizer import Organizer
from logger.logging_config import configure_logging


def main(
    source_directory: str | Path = "Downloads",
    destination_directory: str | Path | None = None,
    dry_run: bool = False,
) -> None:
    configure_logging()
    organizer = Organizer(
        source_directory,
        output_directory=destination_directory,
    )
    operations = organizer.build_plan()
    organizer.preview_plan(operations)
    if not operations:
        return

    if dry_run:
        print("\nDry run complete. No files were moved.")
        return

    choice = input("Do you want to execute the plan? (y/n): ")
    if choice.lower() == "y":
        organizer.execute_plan(operations)

    else:
        print("Plan execution canceled.")


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
        dest="source_option",
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
    arguments = parse_arguments()
    main(arguments.source, arguments.destination, arguments.dry_run)