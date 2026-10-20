from pathlib import Path
from File_item import FileItem
from Rule_engine import RuleEngine


def test_pdf_is_classified_as_document():
    file_itme = FileItem(Path("test.pdf"))
    rule_engine = RuleEngine()

    assert rule_engine.get_category(file_itme) == "Documents"


def test_python_file_as_code():
    file_item = FileItem(Path("script.py"))
    rule_engine = RuleEngine()

    assert rule_engine.get_category(file_item) == "Code"

def test_unknown_extension_is_classified_as_others():
    file_item = FileItem(Path("data.xyz"))

    engine = RuleEngine()

    assert engine.get_category(file_item) == "Others"


def test_grp_files():
    files = [FileItem(Path("test.pdf")),
             FileItem(Path("script.py")),
             FileItem(Path("data.xyz")),
             ]
    engine = RuleEngine()
    categories = engine.group_files(files)
    assert len(categories["Documents"]) == 1
    assert len(categories["Code"]) == 1
    assert len(categories["Others"]) == 1