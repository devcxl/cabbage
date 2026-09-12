---
origin_change: lightweight-change-records
change_type: feature
cabbage_stage: design
synced_at: '2026-09-12T09:42:25.201924+00:00'
---

# Context

Ordinary changes previously generated four or five documents even when they had no specialist risks. Guides additionally required DAGs and repeated task procedures.

# Design

The new feature, bugfix and refactor assets share a compact stage layout: conditional adr/api/database/security/release stages, followed by implementation using the change-record template. The record has Goal, Design, Tasks and Verification. Existing gate ordering, checklist validation, dependency signatures and archive retention are reused.

Workflow record_covers declares product and testing evidence inline, so CI skips only the redundant docs-path requirements declared by those workflows. Existing workflows have no such declaration and keep their rules. No automatic migration or alternate engine is added.

# Failure Modes

Unfinished or modified records block merge. Any enabled specialist stage blocks implementation until verified. Specialist document changes invalidate dependent implementation. CI still requires current-document updates for high-risk impacts. Plans are reviewed before implementation; actual results belong in the record.

# Rollout

Only shipped initialization assets change; this repository's .cabbage/workflows remains untouched. Freeze an old feature fixture for existing regression suites. Regenerate the CLI snapshot with the shared script and update current guides without rewriting historical ADRs.
