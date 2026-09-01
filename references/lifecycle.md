# Lifecycle

Artifact states are derived by `cabbage`: `pending`, `done`, `stale`, `skipped`.

A stage becomes stale when its artifact, workflow definition, impact context, or any dependency signature changes.

Change lifecycle: `active → archived`. Run `cabbage sync <change>` to push verified specs to current-state docs. `cabbage archive` automatically syncs specs into `docs/` before archiving. Archive only after `gate archive` succeeds.
