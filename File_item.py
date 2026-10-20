from pathlib import Path

class FileItem:
    def __init__(self,path:str):
        self.path = Path(path)

    def check_exits(self):
        return self.path.is_dir()

    def is_file(self):
        return self.path.is_file()

    def extract_file_name(self):
        return self.path.name

    def get_extension(self):
        return self.path.suffix

    def get_file_size(self):
        """Return the file size in bytes.

        Raises:
            FileNotFoundError: If the file does not exist.
            IsADirectoryError: If the path points to a directory.
        """

        if not self.path.is_file():
            raise FileNotFoundError(f"The file '{self.path}' does not exist or is not a file.")

        if not self.path.exists():
            raise IsADirectoryError(f"The path '{self.path}' points to a directory, not a file.")

        return self.path.stat().st_size

    def formated_size(self):
        size_bytes = self.get_file_size()

        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 ** 2:
            return f"{size_bytes / 1024:.2f} KB"
        elif size_bytes < 1024 ** 3:
            return f"{size_bytes / (1024 ** 2):.2f} MB"
        else:
            return f"{size_bytes / (1024 ** 3):.2f} GB"

    def __str__(self)->str:
       return (
           f"file: {self.extract_file_name()} |"
           f" extension: {self.get_extension()} |"
           f" size: {self.formated_size()}"
       )