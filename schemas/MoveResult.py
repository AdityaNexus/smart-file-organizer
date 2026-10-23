from dataclasses import dataclass
from pathlib import Path

from typing import Literal

MoveStatus = Literal["Moved", "Skipped", "Failed"]

@dataclass
class MoveResult:
    source: Path
    destination: Path
    status: MoveStatus
    message: str = ""