"""Tests for textstats.py.

Some of these currently FAIL on purpose — each failure corresponds to a bug
you'll file as a GitHub issue for @claude to fix. Run `pytest -q` locally
or check the "Tests" GitHub Actions workflow to see which ones are red.
"""

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "textstats.py"


def run_cli(args):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        capture_output=True,
        text=True,
    )


@pytest.fixture
def sample_file(tmp_path):
    p = tmp_path / "sample.txt"
    p.write_text(
        "the quick brown fox jumps over the lazy dog the fox runs"
    )
    return p


def test_top_words_orders_by_frequency(sample_file):
    """The most frequent word ('the', count 3) should be listed first."""
    result = run_cli([str(sample_file), "-n", "1", "--min-length", "0"])
    assert "the: 3" in result.stdout


def test_empty_file_does_not_crash(tmp_path):
    """An empty input file should print sensible stats, not crash."""
    empty = tmp_path / "empty.txt"
    empty.write_text("")
    result = run_cli([str(empty)])
    assert result.returncode == 0
    assert "ZeroDivisionError" not in result.stderr


def test_negative_top_returns_no_words(sample_file):
    """A negative --top should behave like 0 (show nothing), not a Python slice quirk."""
    result = run_cli([str(sample_file), "-n", "-1"])
    lines_after_header = result.stdout.split("words:")[-1].strip()
    assert lines_after_header == ""


def test_min_length_filters_short_words(sample_file):
    """--min-length should exclude shorter words from all stats."""
    result = run_cli([str(sample_file), "--min-length", "4"])
    assert "Total words: 6" in result.stdout


def test_min_length_default_is_five(sample_file):
    """With no --min-length given, words shorter than 5 chars are excluded by default."""
    result = run_cli([str(sample_file)])
    assert "Total words: 3" in result.stdout
