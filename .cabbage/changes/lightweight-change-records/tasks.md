---
change: lightweight-change-records
cabbage_stage: implementation
---
# Tasks

- [x] Reproduce the excess-document defaults with failing regression tests.
- [x] Add a single record template and conditional high-risk prerequisites for three new-project workflows.
- [x] Keep product/testing evidence inline without weakening old or specialist CI rules.
- [x] Preserve old regression coverage with a frozen workflow fixture.
- [x] Update current guides and execute README commands in temporary projects.
- [x] Regenerate the CLI snapshot and run the complete tests and documentation build.

# Verification

Local verification: `python -m unittest discover tests` (41 tests passed), `python -m cabbage_cli validate --all`, `pnpm --dir docs run build`, and `git diff --check`. No existing project workflow or user-owned untracked record was migrated.
