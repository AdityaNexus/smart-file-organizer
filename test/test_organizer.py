import json

from organizer import Organizer


def test_scanner_excludes_output_and_plan_is_deterministic(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "b.txt").write_text("b", encoding="utf-8")
    (source / "a.PDF").write_text("a", encoding="utf-8")
    output = source / "organized"
    (output / "Documents").mkdir(parents=True)
    (output / "Documents" / "old.txt").write_text("old", encoding="utf-8")

    operations = Organizer(source).build_plan()

    assert [operation.source.name for operation in operations] == ["a.PDF", "b.txt"]
    assert all("old.txt" not in str(operation.source) for operation in operations)


def test_execute_records_history_and_respects_existing_destination(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    file_path = source / "report.txt"
    file_path.write_text("new", encoding="utf-8")
    output = tmp_path / "output"
    existing = output / "Documents"
    existing.mkdir(parents=True)
    (existing / "report.txt").write_text("old", encoding="utf-8")

    organizer = Organizer(source, output_directory=output)
    results = organizer.execute_plan(organizer.build_plan())

    assert results[0].status == "Skipped"
    assert file_path.exists()
    assert not (output / ".organizer-history.json").exists()


def test_history_is_written_for_successful_move(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    (source / "report.txt").write_text("new", encoding="utf-8")
    output = tmp_path / "output"

    organizer = Organizer(source, output_directory=output)
    organizer.execute_plan(organizer.build_plan())

    history = json.loads((output / ".organizer-history.json").read_text())
    assert history[0][0]["source"].endswith("report.txt")


def test_persistent_undo_restores_successful_batch(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    original = source / "report.txt"
    original.write_text("new", encoding="utf-8")
    output = tmp_path / "output"
    organizer = Organizer(source, output_directory=output)

    organizer.execute_plan(organizer.build_plan())
    assert not original.exists()
    assert organizer.undo_last_persistent_batch()
    assert original.read_text(encoding="utf-8") == "new"
