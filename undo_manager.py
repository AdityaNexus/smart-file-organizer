import shutil
from pathlib import Path
from file_mover import FileMover

class UndoManager:
    def __init__(self, mover: FileMover):
        self.mover = mover

    def undo(self):
        if not self.mover.completed_moves:
            print("No moves to undo.")
            return False
        last_move = self.mover.completed_moves[-1]

        if not last_move.destination.is_file():
            print("Cannot undo move: destination is not a file.")
            return False

        if  last_move.source.exists():
            print("Cannot undo move: source file already exists.")
            return False

        try:
            last_move.source.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(last_move.destination), str(last_move.source))
            self.mover.completed_moves.pop()
            print(f"Undo successful: Moved {last_move.destination} back to {last_move.source}")
            return True
        except (OSError, shutil.Error) as error:
            print(f"Failed to undo move: {error}")
            return False