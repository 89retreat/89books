"""One terminal line that shows how far a slow step has gone and roughly how long is left.

Catalogue lookups take a second or two per book, so a shelf of 150 books spends minutes in silence
without it. Outside a terminal (a log file, a pipe) it writes nothing: a rewritten line only makes noise.
"""

import sys
import time
from collections.abc import Callable
from typing import TextIO

WIDTH = 72


class Progress:
    def __init__(
        self, out: TextIO | None = None, live: bool | None = None, clock: Callable[[], float] = time.monotonic
    ):
        self.out = out or sys.stderr
        self.live = self.out.isatty() if live is None else live
        self.clock = clock
        self.total = self.done = 0
        self.began = 0.0

    def start(self, total: int) -> None:
        self.total, self.done, self.began = total, 0, self.clock()

    def step(self, title: str) -> None:
        self.done += 1
        if not self.live:
            return
        line = f"  {self.done}/{self.total}{self._left()} · {title}"
        if len(line) > WIDTH:
            line = line[: WIDTH - 1] + "…"
        self.out.write(f"\r\x1b[K{line}")
        self.out.flush()

    def finish(self) -> None:
        if self.live:
            self.out.write("\r\x1b[K")
            self.out.flush()

    def _left(self) -> str:
        if self.done < 5:  # too few books to guess the pace
            return ""
        seconds = (self.clock() - self.began) / self.done * (self.total - self.done)
        if seconds < 60:
            return " · less than a minute left"
        return f" · about {round(seconds / 60)} min left"
