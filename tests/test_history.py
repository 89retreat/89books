import ast
from datetime import datetime
from pathlib import Path

from shelf import history
from shelf.history import HistoryEntry, is_managed_name, plan_snapshot

MODULE = Path(history.__file__)


def at(minute=30):
    return datetime(2026, 10, 28, 19, minute)


def test_snapshot_uses_decided_timestamp_name_and_collision_suffixes():
    first = plan_snapshot([], at())
    second = plan_snapshot([HistoryEntry(first.name, at().timestamp(), 10)], at())
    third = plan_snapshot(
        [
            HistoryEntry(first.name, at().timestamp(), 10),
            HistoryEntry(second.name, at().timestamp() + 1, 10),
        ],
        at(),
    )
    assert first.name == "shelf-2026-10-28-1930.yaml"
    assert second.name == "shelf-2026-10-28-1930-02.yaml"
    assert third.name == "shelf-2026-10-28-1930-03.yaml"


def test_retention_removes_only_oldest_managed_entries_after_new_snapshot():
    entries = [HistoryEntry(f"shelf-2026-10-28-{hour:02d}00.yaml", hour, 10) for hour in range(20)]
    entries += [HistoryEntry("notes.yaml", -1, 10), HistoryEntry("portrait.txt", -2, 10)]
    result = plan_snapshot(entries, at(), limit=20)
    assert result.remove == ("shelf-2026-10-28-0000.yaml",)
    assert "notes.yaml" not in result.remove and "portrait.txt" not in result.remove


def test_managed_name_rejects_paths_and_similar_files():
    assert is_managed_name("shelf-2026-10-28-1930.yaml")
    assert is_managed_name("shelf-2026-10-28-1930-12.yaml")
    for name in (
        "../shelf-2026-10-28-1930.yaml",
        "/tmp/shelf-2026-10-28-1930.yaml",
        "shelf-2026-10-28.yaml",
        "notes.yaml",
        "shelf-2026-10-28-1930-2.yaml",
    ):
        assert not is_managed_name(name)


def test_history_planner_has_no_filesystem_clock_environment_or_terminal_access():
    tree = ast.parse(MODULE.read_text(encoding="utf-8"))
    calls = {
        node.func.attr
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
    }
    assert "now" not in calls
    imported = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported |= {alias.name for alias in node.names}
        elif isinstance(node, ast.ImportFrom):
            imported.add(node.module or "")
    forbidden = ("pathlib", "os", "sys", "time", "getpass", "shelf.cli", "shelf.config")
    assert not {module for module in imported if module.startswith(forbidden)}
