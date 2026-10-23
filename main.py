import argparse

from organizer import Organizer
from logger.logging_config import configure_logging


def main(source_directory: str = "Downloads", destination_directory: str | None = None):
    configure_logging()
    organizer = Organizer(
        source_directory,
        output_directory=destination_directory,
    )
    operations = organizer.build_plan()
    organizer.preview_plan(operations)
    if not operations:
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
        "source",
        nargs="?",
        default="Downloads",
        help="Directory to scan (default: Downloads).",
    )
    parser.add_argument(
        "destination",
        nargs="?",
        default=None,
        help="Directory where category folders are created. "
        "Defaults to <source>\\organized.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments.source, arguments.destination)