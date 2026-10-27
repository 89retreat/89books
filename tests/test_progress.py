from io import StringIO

from shelf.progress import Progress


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def test_a_terminal_sees_one_line_rewritten_with_count_and_time_left():
    out, clock = StringIO(), Clock()
    progress = Progress(out, live=True, clock=clock)
    progress.start(100)
    for done in range(1, 11):
        clock.now = done * 1.2
        progress.step("Torto Arado")
    text = out.getvalue()
    assert "\r" in text and "\n" not in text
    assert "10/100" in text and "Torto Arado" in text
    assert "about 2 min left" in text  # 90 books at 1.2 s each
    progress.finish()
    assert out.getvalue().endswith("\r\x1b[K")


def test_long_titles_are_cut_to_fit_one_line():
    out = StringIO()
    progress = Progress(out, live=True, clock=Clock())
    progress.start(2)
    progress.step("A" * 200)
    assert max(len(line) for line in out.getvalue().split("\r")) < 80


def test_a_log_file_gets_nothing():
    out = StringIO()
    progress = Progress(out, live=False, clock=Clock())
    progress.start(3)
    progress.step("Torto Arado")
    progress.finish()
    assert out.getvalue() == ""
