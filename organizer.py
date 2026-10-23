from pathlib import Path
from FIle_scanner import FileScanner
from Rule_engine import RuleEngine
from move_planner import MovePlanner
from file_mover import FileMover
from undo_manager import UndoManager

class Organizer:
    def __init__(self,
                 root_directory: str | Path,
                 output_folder: str | Path = "organized",
                 output_directory: str | Path | None = None):
        self.root_directory = Path(root_directory)
        self.output_directory = (Path(output_directory).resolve() if output_directory is not None else self.root_directory / output_folder)
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
        self.print_report(results)
        return results

    
    def undo_last_move(self):
        return self.undo_manager.undo()
    
    
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



        