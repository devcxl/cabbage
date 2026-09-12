---
change: unify-cli-guides
cabbage_stage: tests
---
# Strategy

Reproduce guide stage-name errors and seven source/snapshot differences before correction. Run repository contract tests, the full Python suite and the documentation build after correction.

# Cases

- Published concrete verify stage IDs exist in shipped workflows.
- All snapshot files, including hidden site configuration, match source bytes.
- Existing init and vendored execution regressions continue passing.
- Project workflows and user-owned untracked files are not modified.
