---
change: unify-cli-guides
cabbage_stage: implementation
---
# Tasks

- [x] Reproduce invalid guide stage IDs and stale snapshot assets.
- [x] Correct commands and document actual sync, archive and CI behavior.
- [x] Regenerate the snapshot from its sole source and add regression checks.

# Verification

Run `python -m unittest discover tests`, `python -m cabbage_cli validate --all`, `git diff --check`, and `pnpm --dir docs run build` before delivery. Results are recorded in the current testing guide.
