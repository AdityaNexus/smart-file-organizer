from pathlib import Path
from FIle_scanner import FileScanner
from Rule_engine import RuleEngine
from move_planner import MovePlanner
from file_mover import FileMover
from undo_manager import UndoManager
from history import HistoryStore

class Organizer:
    def __init__(self,
                 root_directory: str | Path,
                 output_folder: str | Path = "organized",
                 output_directory: str | Path | None = None):
        self.root_directory = Path(root_directory)
        self.root_directory = self.root_directory.resolve()
        self.output_directory = (
            Path(output_directory).resolve()
            if output_directory is not None
            else (self.root_directory / output_folder).resolve()
        )
        if self.root_directory == self.output_directory:
            raise ValueError("Root directory and output directory cannot be the same.")

        exclude_dirs = set()
        try:
            relative_output = self.output_directory.relative_to(self.root_directory) # Path.relative_to() raises ValueError if the output directory is not a subdirectory of the root directory

        except ValueError:
            relative_output = None

        if relative_output is not None and relative_output.parts:
            exclude_dirs.add(relative_output.parts[0])

        self.scanner = FileScanner(
            self.root_directory,
            exclude_dir=exclude_dirs,
        )
        self.rule_engine = RuleEngine()
        self.planner = MovePlanner(self.output_directory)
        self.mover = FileMover()
        self.undo_manager = UndoManager(self.mover)
        self.history = HistoryStore(self.output_directory / ".organizer-history.json")

    def build_plan(self):
        files = self.scanner.scan_files()
        categories = self.rule_engine.group_files(files)
        return self.planner.create_plan(categories)

    def preview_plan(self,operations):
        if not operations:
            print(f"No files to organize")
            return 
        print("\n Proposed file moves: ")
        for op in operations:
            print(op)


    def execute_plan(self, operations):
        results = self.mover.execute_plan(operations)
        moved = [
            {"source": str(result.source), "destination": str(result.destination)}
            for result in results
            if result.status == "Moved"
        ]
        if moved:
            self.history.append(moved)
        self.print_report(results)
        return results

    
    def undo_last_move(self):
        return self.undo_manager.undo()

    def undo_last_persistent_batch(self) -> bool:
        history = self.history.read()
        batch = history[-1] if history else None
        if not batch:
            print("No persistent moves to undo.")
            return False

        for operation in reversed(batch):
            source = Path(operation["source"])
            destination = Path(operation["destination"])
            if not destination.is_file() or source.exists():
                print(f"Cannot undo move safely: {destination} -> {source}")
                return False

        for operation in reversed(batch):
            source = Path(operation["source"])
            destination = Path(operation["destination"])
            source.parent.mkdir(parents=True, exist_ok=True)
            destination.replace(source)

        self.history.pop_last()
        print(f"Undid {len(batch)} move(s).")
        return True
    
    
    def print_report(self, results):
        moved = sum(r.status == "Moved" for r in results)
        skipped = sum(r.status == "Skipped" for r in results)
        failed = sum(r.status == "Failed" for r in results)

        print("\n========== ORGANIZER REPORT ==========")
        print(f"Total operations : {len(results)}")
        print(f"Moved            : {moved}")
        print(f"Skipped          : {skipped}")
        print(f"Failed           : {failed}")
        print("======================================")



        