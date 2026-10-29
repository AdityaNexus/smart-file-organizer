from main import main, parse_arguments

if __name__ == "__main__":
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