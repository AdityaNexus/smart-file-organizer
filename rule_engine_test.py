from pathlib import Path

from File_item import FileItem
from Rule_engine import RuleEngine

engine = RuleEngine()

test_files = [
    FileItem(Path("report.pdf")),
    FileItem(Path("sales.csv")),
    FileItem(Path("video.mp4")),
    FileItem(Path("unknown.xyz")),
]

for item in test_files:
    print(item.extract_file_name(), "->", engine.get_category(item))