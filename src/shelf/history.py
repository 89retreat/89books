"""Pure planning for local shelf snapshots.

Callers provide time and directory metadata. This module only decides managed names and retention;
it never reads a folder, asks the clock, prints or mutates anything.
"""

import re
from dataclasses import dataclass
from datetime import datetime

_MANAGED = re.compile(r"^shelf-\d{4}-\d{2}-\d{2}-\d{4}(?:-\d{2,})?\.yaml$")


@dataclass(frozen=True)
class HistoryEntry:
    name: str
    modified_at: float
    size: int


@dataclass(frozen=True)
class SnapshotPlan:
    name: str
    remove: tuple[str, ...]


def is_managed_name(name: str) -> bool:
    """Whether a basename belongs to the history created by this product."""
    return bool(_MANAGED.fullmatch(name))


def plan_snapshot(entries: list[HistoryEntry], now: datetime, limit: int = 20) -> SnapshotPlan:
    """Chooses a collision-safe name and managed entries to remove after adding it."""
    occupied = {entry.name for entry in entries}
    stem = now.strftime("shelf-%Y-%m-%d-%H%M")
    name = f"{stem}.yaml"
    sequence = 2
    while name in occupied:
        name = f"{stem}-{sequence:02d}.yaml"
        sequence += 1

    managed = sorted(
        (entry for entry in entries if is_managed_name(entry.name)),
        key=lambda entry: (entry.modified_at, entry.name),
    )
    excess = max(0, len(managed) + 1 - limit)
    return SnapshotPlan(name, tuple(entry.name for entry in managed[:excess]))
