---
change: lightweight-change-records
cabbage_stage: adr
---
# Context

The user approved shrinking ordinary changes to one record while retaining risk-based specialist review and old-project compatibility. Earlier DAG and full-lifecycle decisions remain historical, but their methods are no longer mandatory for every new ordinary change.

# Decision

Use one implementation record for new feature/bugfix/refactor workflows. Reuse conditional stages and impact flags instead of adding complexity levels or a separate workflow engine. Declare product/testing evidence covered by the record, retain other current-document rules, and do not automatically migrate old project workflows. Keep DAG export available but optional.

Alternatives rejected: keeping four documents for every fix preserves the original burden; automatically replacing old workflows invalidates existing verification; a new lightweight command adds an unnecessary user choice.

# Consequences

New users maintain one document unless risks require more. Product and testing records stay in change history rather than being duplicated into docs. High-risk release plans move before implementation in the new workflows; actual execution evidence is recorded afterward in tasks.md. Old projects keep their larger workflow until an explicitly reviewed migration. This change reduces compulsory documentation, not the need for tests or truthful current documents.
