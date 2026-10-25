
def handle_scan(args):
    print(f"Scanning directory: {args.path}")
    print(f"Recursive: {args.recursive}")


def handle_organize(args):
    print(f"Organizing directory: {args.path}")
    print(f"Category: {args.category}")


def handle_clean(args):
    print(f"Cleaning directory: {args.path}")
    print(f"Dry run: {args.dry_run}")


def handle_stats(args):
    print(f"Showing statistics for: {args.path}")


def handle_info(args):
    print(f"Directory: {args.path}")
    print(f"Show hidden files: {args.show_hidden}")
