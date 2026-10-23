from pathlib import Path
from File_item import FileItem


class FileScanner:
    def __init__(self, directory: str | Path , exclude_dir : set[str] | None = None):
        self.exclude = (exclude_dir if exclude_dir is not None else {"organized"})
        self.directory = Path(directory)

    def is_dir(self) -> bool:
        return self.directory.is_dir()

    def scan_files(self) -> list[FileItem]:
        if not self.is_dir():
            raise NotADirectoryError(
                f"Not a valid directory: {self.directory}"
            )

        files = []

        for item in self.directory.rglob("*"):
            relative_parts = item.relative_to(self.directory).parts

            if any(part in self.exclude for part in relative_parts):
                continue

            if item.is_file():
                files.append(FileItem(item))

        return files