# Project context: Claude Code GitHub Actions practice

This file exists so a fresh Claude Code session (VS Code extension, CLI,
etc.) started in this folder picks up where a separate Cowork/claude.ai
conversation left off. Claude Code and Cowork are different products with
separate session histories — this file is the hand-off mechanism.

## What this project is

A learning exercise: get the official Claude Code GitHub Actions
integration working end to end — commenting `@claude` on a GitHub issue
or PR should make Claude open/review a pull request automatically.

The vehicle is a tiny Python CLI, `textstats.py` (word count / top-N
frequent words / average word length), seeded with **three intentional
bugs**, each backed by a failing pytest test in `tests/test_textstats.py`:

1. `top_words()` sorts alphabetically instead of by frequency.
2. `average_word_length()` raises `ZeroDivisionError` on an empty file.
3. `--top`/`-n` with a negative value falls through to a raw Python list
   slice instead of returning no words.

Full step-by-step exercise instructions live in `TASK.md` at the project
root — read that for the authoritative task list.

## Repo / Actions setup status

- [x] Local scaffold created (`textstats.py`, tests, `README.md`,
      `TASK.md`, `.gitignore`, `.github/workflows/tests.yml`,
      `.github/workflows/claude.yml.example`).
- [ ] Public GitHub repo created and scaffold pushed (repo name discussed:
      `textstats-practice`, not yet confirmed created as of this note).
- [ ] Claude GitHub App installed via `/install-github-app` (generates the
      real `.github/workflows/claude.yml`, replacing/confirming the
      `.example` reference copy).
- [ ] Issues filed one at a time for bugs 1–3, each fixed via a
      Claude-authored PR, reviewed, and merged.
- [ ] Stretch: a 4th issue requesting a new `--min-length` feature (no
      pre-written test — checks whether Claude adds test coverage
      unprompted).
- [ ] Stretch: try `@claude review this PR` as a plain comment on a PR's
      conversation tab (should already work off the single installed
      `claude.yml` — see note below) before building a separate
      always-on review workflow.

## Notes / gotchas learned so far

- The device bridge used from Cowork could not write directly into
  `.github/workflows/` (protected path) — those two files were staged to
  a sibling `workflows-to-move/` folder and moved into place manually.
- GitHub treats a PR's conversation tab as an "issue" under the hood, so
  the default installed workflow's `issue_comment` trigger already fires
  for a plain `@claude ...` comment on a PR, not just on issues. A
  dedicated always-on review workflow (trigger: `pull_request: [opened,
  synchronize]`, no `@claude` mention needed) is a separate, later
  exercise, not required to test manual PR-review comments.
- Recommended auth for this solo learning setup: `ANTHROPIC_API_KEY` repo
  secret (simplest); `CLAUDE_CODE_OAUTH_TOKEN` via `claude setup-token` is
  the alternative if billing against a Pro/Max subscription is preferred.

## Where to go next after the core loop works

Same `anthropics/claude-code-action@v1` action, new trigger + prompt, as
additional `.github/workflows/*.yml` files:
- Always-on PR review (`pull_request` trigger)
- Issue triage/labeling (`issues: [opened]` trigger)
- Scheduled report (`schedule`/cron trigger)
