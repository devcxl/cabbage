---
change: lightweight-change-records
cabbage_stage: tests
---
# Strategy

Confirm failing lightweight expectations before changing assets. Exercise new defaults using real temporary projects and CLI subprocesses, and continue running the original tests against a frozen legacy workflow. Validate all template contracts, generated snapshot bytes, concrete guide stage IDs and executable README examples.

# Cases

- Three ordinary change types generate exactly one Markdown record.
- Each of five risks adds just its related document; combined risks all block until verified.
- Placeholders, incomplete checklists and stale signatures block merge.
- Small-change Git CI succeeds without duplicate product/testing docs.
- API risk still fails CI without current docs and succeeds after publishing them.
- Archive retains the change record; tasks can inspect a plain checklist without DAG markup.
- Refreshing the CLI preserves old config, workflow bytes and state signatures.
- Old feature workflows still require product and testing document updates.

# Evidence

Initial targeted run failed 19 lightweight expectations. After implementation the full suite passed 41 tests. VitePress build succeeded with its existing large-chunk warning. Re-run before delivery and verify remote CI and Pages deployment after pushing.
