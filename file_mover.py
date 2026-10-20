import shutil
from pathlib import Path
from move_planner import Move_operation
from schemas.MoveResult import MoveResult
class FileMover:
    def __init__(self):
        self.completed_moves :list[Move_operation] = []

    def move_file(self, move_operations: Move_operation)->MoveResult:
        source = move_operations.source
        destination = move_operations.destination

        if not source.is_file():
            return MoveResult(
                source=source,
                destination=destination,
                status="Failed",
                message=f"Source file {source} does not exist."
            )

        if destination.is_file():
            return MoveResult(
                source=source,
                destination=destination,
                status="Skipped",
                message=f"Destination file {destination} already exists. Skipping move."
                
            )

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(source), str(destination))
            self.completed_moves.append(move_operations)
            return MoveResult(
                source=source,
                destination=destination,
                status="Moved",
                message=f"Moved {source} to {destination}"
            )
        except (OSError, shutil.Error) as error:
            print(f"failed to move {source} to {destination}: {error}")
            return MoveResult(
                source=source,
                destination=destination,
                status="Failed",
                message=f"failed to move {source} to {destination}: {error}"
            )

    def execute_plan(self , operations : list[Move_operation])->list[MoveResult]:
        successful_moves = []
        for operation in operations:
            result = self.move_file(operation)
            successful_moves.append(result)
        return successful_moves