---
name: pr-review
description: Reviews a pull request's diff for correctness, test coverage, and style. Default posts a formal GitHub PR review with inline comments; --comment posts a single summary comment instead.
argument-hint: [--comment]
allowed-tools: [Bash(gh pr diff:*), Bash(gh pr view:*), Bash(gh pr review:*), Bash(gh pr comment:*), mcp__github_inline_comment__create_inline_comment]
disable-model-invocation: false
---

# PR Review

The context above this invocation includes `REPO` and `PR NUMBER`. The user
invoked this skill with: $ARGUMENTS

## Arguments

Parse `$ARGUMENTS` for a `--comment` flag:
- **No `--comment` flag (default):** submit your findings as a single
  formal GitHub PR review via `gh pr review` (approve, comment, or
  request-changes as appropriate), using
  `mcp__github_inline_comment__create_inline_comment` (with
  `confirmed: true`) to highlight specific lines.
- **With `--comment`:** skip the formal review and instead post a single
  top-level summary via `gh pr comment`.

## Instructions

Review this pull request's diff for correctness bugs, missing or weak test
coverage, and style consistency with the rest of `textstats.py`.

Note: the PR branch is already checked out in the current working
directory.

Only post GitHub comments/reviews — don't just print review text as a
message. If the PR looks correct and well-tested, approve it (or comment,
under `--comment`) with a short note saying so.

You are strictly read/comment-only: never push commits, never open a new
PR, never edit files.
