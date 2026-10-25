import argparse

from filemaster import commands

def build_parser():
    parser = argparse.ArgumentParser(
        description="FileMaster - A file management CLI tool"
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan a directory"
    )
    scan_parser.add_argument("path")
    scan_parser.add_argument(
        "--recursive",
        action="store_true"
    )
    scan_parser.set_defaults(func=commands.handle_scan)

    # organize
    organize_parser = subparsers.add_parser(
        "organize",
        help="Organize files"
    )
    organize_parser.add_argument("path")
    organize_parser.add_argument(
        "--category",
        choices=["extension", "size", "date"],
        default="extension"
    )
    organize_parser.set_defaults(func=commands.handle_organize)

    # clean
    clean_parser = subparsers.add_parser(
        "clean",
        help="Clean temporary files (demo only)"
    )
    clean_parser.add_argument("path")
    clean_parser.add_argument(
        "--dry-run",
        action="store_true"
    )
    clean_parser.set_defaults(func=commands.handle_clean)

    # stats
    stats_parser = subparsers.add_parser(
        "stats",
        help="Show directory statistics"
    )
    stats_parser.add_argument("path")
    stats_parser.set_defaults(func=commands.handle_stats)

    # info
    info_parser = subparsers.add_parser(
        "info",
        help="Show directory information"
    )
    info_parser.add_argument("path")
    info_parser.add_argument(
        "--show-hidden",
        action="store_true"
    )
    info_parser.set_defaults(func=commands.handle_info)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)

