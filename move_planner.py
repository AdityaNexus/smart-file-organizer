from pathlib import Path
from File_item import FileItem

class Move_operation:
    def __init__(self,source: Path , destination: Path ):
        self.source = source
        self.destination = destination

    def __str__(self)->str:
        return f"Move {self.source} to {self.destination}"



class MovePlanner:
    def __init__(self, base_directory: str | Path):
        self.base_directory = Path(base_directory)


    def create_plan(self, categories: dict[str, list[FileItem]]) -> list[Move_operation]:
        plan = []
        destination_dirs = set()
        for category in sorted(categories):
            for f in sorted(categories[category], key=lambda item: item.path.name.lower()):
                source = f.path
                destination = self.base_directory / category / f.extract_file_name()
                if destination in destination_dirs:
                    # Handle duplicate file names 
                    counter = 1
                    new_destination = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
                    while new_destination in destination_dirs or new_destination.exists():
                        counter += 1
                        new_destination = destination.with_name(f"{destination.stem}_{counter}{destination.suffix}")
                    destination = new_destination
                destination_dirs.add(destination)
                plan.append(Move_operation(source , destination))
        return plan
