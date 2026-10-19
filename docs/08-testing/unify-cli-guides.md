---
origin_change: unify-cli-guides
change_type: refactor
cabbage_stage: tests
synced_at: '2026-10-19T01:04:32.802203+00:00'
---

# Strategy

Reproduce guide stage-name errors and seven source/snapshot differences before correction. Run repository contract tests, the full Python suite and the documentation build after correction.

# Cases

- Published concrete verify stage IDs exist in shipped workflows.
- All snapshot files, including hidden site configuration, match source bytes.
- Existing init and vendored execution regressions continue passing.
- Project workflows and user-owned untracked files are not modified.
