from dataclasses import dataclass
from pathlib import Path

@dataclass
class MoveResult:
    source: Path
    destination: Path
    status: bool
    message: str = ""