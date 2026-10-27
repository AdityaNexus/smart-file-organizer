import argparse
from pathlib import Path

from organizer import Organizer
from logger.logging_config import configure_logging

def parse_args():
    parser = argparse.ArgumentParser(
        description = "Smart File Organizer with undo"
    )

    parser.add_argument(
        "--source",
        type = Path,
        default = Path("Downloads"),
        help = "Directory to scan (default: Downloads)."
    )

    parser.add_argument(
        "--output",
        default = "organized",
        help = "Destination directory. Defaults to <source>\\organized."
    )

    parser.add_argument(
        "--dry-run",
        action = "store_true",
        help = "Preview the plan without moving files."
    )

    return parser.parse_args()

def main():
    args = parse_args()
    configure_logging()
    if not args.source.is_dir():
        raise SystemExit(f"Error: Source directory '{args.source}' does not exist or is not a directory.")

    organizer = Organizer(
        root_directory=args.source,
        output_folder=args.output
    )

    operations = organizer.build_plan()
    organizer.preview_plan(operations)

    if args.dry_run or not operations:
        if args.dry_run:
          print("\nDry run complete. No files were moved.")
        return 

    choice = input("Do you want to execute the plan? (y/n): ")
    if choice.lower() == "y":
        organizer.execute_plan(operations)
    else:
        print("Plan execution canceled.")


if __name__ == "__main__":
    main()    