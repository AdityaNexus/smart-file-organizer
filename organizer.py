from pathlib import Path
from FIle_scanner import FileScanner
from Rule_engine import RuleEngine
from move_planner import MovePlanner
from file_mover import FileMover
from undo_manager import UndoManager

class Organizer:
    def __init__(self,
                 root_directory: str | Path,
                 output_folder: str ="organized"):
        self.root_directory = Path(root_directory)
        self.output_directory = self.root_directory / output_folder

        self.scanner = FileScanner(self.root_directory, exclude_dir=[self.output_directory])
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
        moved = sum(r.status == "Moved" for r in results)
        skipped = sum(r.status == "Skipped" for r in results)
        failed = sum(r.status == "Failed" for r in results)

        for r in results:
            if r.status!="Moved":
                print(f"[{r.status.upper()}], {r.message}")

        print(f"\nSummary: {moved} files moved, {skipped} files skipped, {failed} files failed.")
        return results
    

    def undo_last_move(self):
        return self.undo_manager.undo()
    



        