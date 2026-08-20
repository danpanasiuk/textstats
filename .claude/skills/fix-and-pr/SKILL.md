---
name: fix-and-pr
description: Use when implementing a fix or feature requested via an @claude mention on an issue or PR comment. Covers installing pytest if missing before running the test suite, and opening the pull request yourself with gh pr create rather than just posting a compare link.
allowed-tools: [Bash(gh pr create:*), Bash(pip install:*), Bash(pip3 install:*), Bash(python -m pip install:*), Bash(python3 -m pip install:*), Bash(python -m pytest:*), Bash(python3 -m pytest:*), Bash(pytest:*)]
disable-model-invocation: false
---

# Fix and open a PR

You have `gh` CLI access authenticated via `GH_TOKEN`, and Bash permission
for `gh pr create`.

## Instructions

- If pytest is missing, install it with pip before running the test suite
  — don't skip tests because the dependency isn't there.
- After implementing the requested change and pushing your fix branch,
  actually run `gh pr create` yourself (base `main`, head your branch)
  instead of only posting a compare link.
