---
change: unify-cli-guides
cabbage_stage: design
---
# Context

The guides use artifact names as stage IDs, while the vendored package retains VuePress assets after the source migrated to VitePress.

# Design

Keep CLI stage IDs stable. Correct instructions to follow project workflows and next output. Reuse one snapshot generator for init and the repository maintenance script. Compare every source and snapshot file in regression tests.

# Failure Modes

Snapshot drift fails tests with differing paths. Self-copy from a vendored package fails explicitly rather than deleting its own source.

# Rollout

Regenerate only the package snapshot. Existing configuration, active change signatures and workflows are not migrated.
