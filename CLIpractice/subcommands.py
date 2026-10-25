import argparse

def handle_scan(args):
    print(f"scanning drectory: {args.path}")
    print(f"recursive: {args.recursive}")

def handle_organize(args):
    print(f"organizing directory; {args.path}")
    print(f"category: {args.category}")


def handle_clean(args):
    print(f"Cleaning directory: {args.path}")
    print(f"Dry run: {args.dry_run}")


def handle_stats(args):
    print(f"Showing statistics for: {args.path}")

def handle_info(args):
    print(f"Directory: {args.path}")
    print(f"show hidden files: {args.show_hidden}")

def main():
    parser = argparse.ArgumentParser(
        description = "FIleMaster - file management CLI"
    )

    subparsers = parser.add_subparsers(    # creates a subparser object that allows you to define multiple subcommands for the CLI application.
        dest = "command",
        required = True,
    )

    scan_parser = subparsers.add_parser( # creates a subparser for the "scan" command, allowing the user to specify options and arguments specific to this command.
        "scan",
        help = "Scan a directory"
    )

    scan_parser.add_argument(
        "path",
        help = "Directory to scan"
    )
    scan_parser.add_argument(
        "--recursive",
        action = "store_true",
        help = "Scan directories recursively"
    )
    scan_parser.set_defaults(func = handle_scan)

    organize_parser = subparsers.add_parser(
        "organize",
        help = "Organize files in a directory"
    )

    organize_parser.add_argument(
        "path",
        help = "Directory to organize"
    )

    organize_parser.add_argument(
        "--category",
        choices = ["extension","size","date"],
        default = "extension"
    )

    organize_parser.set_defaults(func = handle_organize)


    clean_parser = subparsers.add_parser(
        "clean",
        help="Clean temporary files (demo only)"
    )
    clean_parser.add_argument("path", help="Directory to clean")
    clean_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without deleting files"
    )
    clean_parser.set_defaults(func=handle_clean)

    # Command 4: stats
    stats_parser = subparsers.add_parser(
        "stats",
        help="Show directory statistics"
    )
    stats_parser.add_argument("path", help="Directory to inspect")
    stats_parser.set_defaults(func=handle_stats)

    # Command 5: info
    info_parser = subparsers.add_parser(
        "info",
        help="Show detailed information about a directory"
    )
    info_parser.add_argument("path", help="Directory to inspect")
    info_parser.add_argument(
        "--show-hidden",
        action="store_true",
        help="Show hidden files"
    )
    info_parser.set_defaults(func=handle_info)

    args = parser.parse_args()

    args.func(args)


if __name__ == "__main__":
    main()

