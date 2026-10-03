# CI for writers

Copy-paste templates that run the Not Ai gate over documentation on every
push. The gate is advisory by design: without `--protect` it exits
non-zero only on empty input, so this workflow reports findings without
ever blocking prose style. Hard requirements (a literal that must appear)
use `--protect` and do block.

## GitHub Action (advisory on docs)

```yaml
name: prose-review
on: [push, pull_request]
jobs:
  gate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.10"
      - name: Advisory gate over docs
        run: |
          for f in docs/**/*.md; do
            echo "--- $f"
            python3 plugins/not-ai/tools/gate.py "$f" --genre readme || true
          done
      - name: Blocking protected literals (example)
        run: |
          python3 plugins/not-ai/tools/gate.py docs/launch-notes.md \
            --genre readme --protect "API v2"
```

Remove `|| true` from the advisory step only if you want review findings
to fail the build. Keep it while the team calibrates; findings are prompts,
not verdicts.

## Pre-commit hook

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: not-ai-gate
        name: not-ai advisory gate
        entry: python3 plugins/not-ai/tools/gate.py
        args: ["--genre", "readme", "--stdin"]
        language: system
        files: "^docs/.*\\.md$"
```

## Diagnose on changed files (review output, not a gate)

```bash
git diff --name-only main | grep '\.md$' | while read -r f; do
  python3 scripts/diagnose.py "$f" --genre readme
done
```
