---
name: repo-health
description: Runs a nightly repo health check (tests, stale issues/PRs) and creates or updates a pinned "Repo Health Report" issue with findings.
argument-hint: ""
allowed-tools: [Bash(pip install:*), Bash(pip3 install:*), Bash(python -m pip install:*), Bash(python3 -m pip install:*), Bash(python -m pytest:*), Bash(python3 -m pytest:*), Bash(pytest:*), Bash(gh issue list:*), Bash(gh issue view:*), Bash(gh issue edit:*), Bash(gh issue create:*), Bash(gh issue comment:*), Bash(gh pr list:*)]
disable-model-invocation: false
---

# Repo Health Report

The context above this invocation includes `REPO`.

## Instructions

Run a nightly repo health check:

1. Install pytest with pip if it's missing, then run the test suite
   (`pytest -q`) and note pass/fail counts.
2. Check for stale or long-open issues and PRs via `gh issue list` and
   `gh pr list`.
3. Search for an existing OPEN issue titled exactly "Repo Health Report"
   via `gh issue list --search "Repo Health Report in:title" --state open`.
   If one exists, post your findings as a new comment on it via
   `gh issue comment`. If none exists, create one via `gh issue create`
   titled "Repo Health Report" with your findings as the body.

Always summarize: test results, stale issues/PRs worth attention, and any
other notable repo health signals.

You are strictly read/report-only: never push commits, never open or
modify pull requests, never edit files.
