import json
import os
import tempfile
from pathlib import Path
from typing import Any


class HistoryStore:
    """Persist successful move batches as JSON without partially-written files."""

    def __init__(self, path: str | Path):
        self.path = Path(path)

    def append(self, operations: list[dict[str, str]]) -> None:
        history = self.read()
        history.append(operations)
        self._write(history)

    def pop_last(self) -> list[dict[str, str]] | None:
        history = self.read()
        if not history:
            return None
        operations = history.pop()
        self._write(history)
        return operations

    def _write(self, history: list[list[dict[str, str]]]) -> None: # A list of batches, where each batch is a list of moves dictionaries
        self.path.parent.mkdir(parents=True, exist_ok=True)
        handle, temporary_name = tempfile.mkstemp(
            dir=self.path.parent,
            prefix=f".{self.path.name}.",
            text=True,
        )
        try:
            with os.fdopen(handle, "w", encoding="utf-8") as file:
                json.dump(history, file, indent=2)
                file.write("\n")
            os.replace(temporary_name, self.path)
        except BaseException:
            os.close(handle)
            Path(temporary_name).unlink(missing_ok=True)
            raise

    def read(self) -> list[list[dict[str, str]]]:
        if not self.path.exists():
            return []
        with self.path.open("r", encoding="utf-8") as file:
            value: Any = json.load(file)
        if not isinstance(value, list) or any(not isinstance(batch, list) for batch in value):
            raise ValueError(f"History file '{self.path}' has an invalid format.")
        return value
