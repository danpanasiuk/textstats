# Practice task: Claude Code + GitHub Actions ("@claude, fix this")

**Goal:** get a real "comment `@claude` on an issue → Claude opens a PR
that fixes it" loop working end to end, on a repo you fully control.

You'll do the GitHub/Actions steps yourself (that's the point of the
exercise) — bring back what happens at each step and I'll check it against
what's expected.

---

## 0. What you're starting with

This folder (`textstats/`) is a tiny Python CLI with three intentional
bugs, already exposed by three failing tests:

- `test_top_words_orders_by_frequency` — the "top words" list is sorted
  alphabetically instead of by frequency.
- `test_empty_file_does_not_crash` — an empty input file causes a
  `ZeroDivisionError` instead of printing `0.00`.
- `test_negative_top_returns_no_words` — `--top -1` returns all-but-one
  words (a Python slicing quirk) instead of showing nothing.

There's also a `tests.yml` Actions workflow that runs `pytest` on every
push/PR, so you'll be able to watch CI go red → green.

## 1. Create the GitHub repo

1. Create a new **public** repo on your GitHub account (e.g. `textstats-practice`). Public is required for the free Claude Code Actions usage tier discussed in the docs, and it's a throwaway practice repo anyway.
2. From inside this `textstats/` folder:
   ```
   git init
   git add .
   git commit -m "Initial commit: textstats CLI with a few bugs"
   git branch -M main
   git remote add origin <your repo URL>
   git push -u origin main
   ```
3. Confirm on GitHub that the "Tests" workflow ran automatically and is **failing** (red X) — that's expected, it's showing you the 3 bugs.

## 2. Install the Claude GitHub App

From your terminal, inside this repo, run your local Claude Code CLI and use the built-in installer:

```
claude
/install-github-app
```

Follow the prompts:
- It installs the Claude GitHub App on this repo (needs your admin access).
- Choose an auth method — **API key** is simplest for this exercise (paste a key from console.anthropic.com). If you're a Claude Pro/Max subscriber and want to use that instead, you can run `claude setup-token` and use the OAuth token option.
- It opens a PR adding `.github/workflows/claude.yml`.

Review and merge that PR. (There's also a `claude.yml.example` already in this repo as a reference/fallback, in case you'd rather wire the workflow up by hand — but let the installer do it first.)

**Checkpoint — tell me:**
- Did `/install-github-app` complete without errors?
- What auth method did you pick?
- Paste (or screenshot) the generated `claude.yml` — I'll sanity-check the permissions and triggers.

## 3. File your first issue and trigger Claude

Open a new GitHub issue on the repo, titled something like:

> Top words are sorted alphabetically instead of by frequency

Body:

> `top_words()` in `textstats.py` should return the most frequent words
> first. Right now it just sorts alphabetically. See the failing test
> `tests/test_textstats.py::test_top_words_orders_by_frequency` for the
> expected behavior.
>
> @claude please fix this and open a PR.

Then watch the **Actions** tab — a `Claude Code` workflow run should start within a few seconds of the comment/issue being created.

**Checkpoint — tell me:**
- How long did it take for the workflow to pick up the mention?
- Did Claude comment on the issue with a progress update?
- Did it open a PR? Paste the PR link/diff.

## 4. Validate the PR

Before merging:
- Check the PR's own CI run (the `tests.yml` workflow) — does it go green?
- Skim the diff — is the fix actually sorting by frequency (highest count first, e.g. via `sorted(..., key=..., reverse=True)` or similar), or did Claude do something suspicious (e.g. hardcode the test's expected output)?

If it looks right, merge it. Confirm `main`'s Tests workflow is green afterward (should now show 2 remaining failures — bugs 2 and 3).

## 5. Repeat for the other two bugs

File two more issues the same way, one at a time:

**Issue 2:**
> Empty input file crashes with ZeroDivisionError
>
> Running `textstats.py` on an empty file crashes instead of printing
> `Average word length: 0.00`. See
> `tests/test_textstats.py::test_empty_file_does_not_crash`.
>
> @claude please fix this and open a PR.

**Issue 3:**
> `--top -1` shows all-but-one words instead of nothing
>
> Negative values for `--top`/`-n` should behave like `--top 0` (show no
> words), not fall through to a raw Python list slice. See
> `tests/test_textstats.py::test_negative_top_returns_no_words`.
>
> @claude please fix this and open a PR.

Same checkpoint each time: did it open a PR, does CI pass, does the diff make sense. Merge each one before filing the next, so Claude is always working from a clean `main`.

## 6. (Stretch) One feature request instead of a bug

File a 4th issue that asks for something new rather than a fix, to see how
Claude handles net-new scope, e.g.:

> Add a `--min-length` flag
>
> Add a `--min-length N` option that excludes words shorter than N
> characters from all stats (total/unique/average/top words). Default: no
> filtering.
>
> @claude please implement this, including a test, and open a PR.

This one has no pre-written failing test, so it's a good check on whether
Claude also adds test coverage unprompted.

## 7. Wrap-up / validation

Once all issues are closed, all three original tests should pass and
`main`'s Tests workflow should be fully green. Report back with:
- Links to the merged PRs
- Anything that surprised you (slow trigger, wrong fix, Claude asking a
  clarifying question in a comment, etc.)

I'll review the final `textstats.py` + workflow files against what's
expected and flag anything worth understanding better.

---

## Where to go next (once this works)

Same building blocks (`anthropics/claude-code-action@v1`), different
trigger + prompt, as separate `.yml` files in `.github/workflows/`:

- **Automated PR review** — trigger on `pull_request`, have Claude leave
  review comments instead of writing code.
- **Issue triage/labeling** — trigger on `issues: [opened]`, have Claude
  summarize and label new issues without opening a PR.
- **Scheduled task** — trigger on `schedule` (cron), e.g. a nightly repo
  health report.

When you're ready to try one of these, ask me and I'll compose the next
task the same way.
