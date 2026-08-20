# textstats

A tiny CLI that prints basic statistics (word count, unique words, average
word length, top N most frequent words) about a text file.

```
python textstats.py sample.txt
python textstats.py sample.txt --top 3
python textstats.py sample.txt --min-length 4
```

This repo doubles as a **practice ground for the Claude Code GitHub Actions
integration** — see `TASK.md` for the exercise. It ships with a few
intentional bugs (see the failing tests in `tests/test_textstats.py`) that
are meant to be fixed by filing GitHub issues and letting `@claude` open
pull requests against them.
