"""Tests for textstats.py.

Some of these currently FAIL on purpose — each failure corresponds to a bug
you'll file as a GitHub issue for @claude to fix. Run `pytest -q` locally
or check the "Tests" GitHub Actions workflow to see which ones are red.
"""

import json
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
    result = run_cli([str(sample_file), "-n", "1"])
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
    """--min-length should exclude short words from all stats, not just top words."""
    result = run_cli([str(sample_file), "--min-length", "4", "-n", "5"])
    # "the" (x3) and "fox" (x2) are shorter than 4 chars and must be excluded entirely.
    assert "the:" not in result.stdout
    assert "fox:" not in result.stdout
    assert "quick: 1" in result.stdout
    assert "Total words: 6" in result.stdout
    assert "Unique words: 6" in result.stdout


def test_min_length_default_does_not_filter(sample_file):
    """With no --min-length, behavior should be unchanged (no filtering)."""
    result = run_cli([str(sample_file), "-n", "1"])
    assert "the: 3" in result.stdout
    assert "Total words: 12" in result.stdout


def test_json_flag_outputs_valid_json(sample_file):
    """--json should print a single JSON object with all stats."""
    result = run_cli([str(sample_file), "--json", "-n", "2"])
    data = json.loads(result.stdout)
    assert data["total_words"] == 12
    assert data["unique_words"] == 9
    assert data["average_word_length"] == pytest.approx(3.75)
    assert data["top_words"] == [
        {"word": "the", "count": 3},
        {"word": "fox", "count": 2},
    ]


def test_json_flag_respects_min_length(sample_file):
    """--json output should reflect --min-length filtering like the text output."""
    result = run_cli([str(sample_file), "--json", "--min-length", "4", "-n", "5"])
    data = json.loads(result.stdout)
    assert data["total_words"] == 6
    assert data["unique_words"] == 6
    words = [item["word"] for item in data["top_words"]]
    assert "the" not in words
    assert "fox" not in words


def test_json_flag_empty_file_does_not_crash(tmp_path):
    """--json on an empty file should not crash and should report zeroed stats."""
    empty = tmp_path / "empty.txt"
    empty.write_text("")
    result = run_cli([str(empty), "--json"])
    assert result.returncode == 0
    data = json.loads(result.stdout)
    assert data["total_words"] == 0
    assert data["unique_words"] == 0
    assert data["average_word_length"] == 0.0
    assert data["top_words"] == []


def test_default_output_unchanged_without_json_flag(sample_file):
    """Without --json, output should remain the human-readable text format."""
    result = run_cli([str(sample_file), "-n", "1"])
    assert "Total words: 12" in result.stdout
    assert "the: 3" in result.stdout
    with pytest.raises(json.JSONDecodeError):
        json.loads(result.stdout)
