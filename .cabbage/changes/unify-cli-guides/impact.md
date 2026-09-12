---
change: unify-cli-guides
cabbage_stage: impact
---
# Impact Matrix

Guides, regression tests and the generated CLI snapshot change. Existing workflows, configuration and history remain unchanged.

# Risks

Incorrect stage examples mislead users; a stale snapshot creates different scaffold behavior depending on the entry point. Regeneration must not overwrite project workflows.
