---
change: lightweight-change-records
cabbage_stage: requirement
---
# Goal

Reduce the default cognitive and documentation cost of ordinary features, fixes and refactors to one human-written Markdown record.

# Scope

Apply lightweight defaults only to newly initialized projects. Preserve existing project workflows, configuration, history and verification state. Reuse existing risk flags, gates and archive behavior; retain specialist workflows and optional DAG export.

# Acceptance Criteria

Ordinary changes generate only tasks.md. Architecture, API, database, security and high-risk deployment each activate only the relevant specialist document and pre-implementation gate. Product and testing evidence in the record do not require duplicate current documents. High-risk document rules and old workflow behavior remain enforced. Published new-project examples execute successfully.
