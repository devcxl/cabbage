# Validation checklist

`cabbage validate` verifies workflow artifacts. `cabbage ci` additionally checks Git diff binding.

Manual review should still ask:

1. Is the file in the correct long-lived location?
2. Is an existing document the source of truth?
3. Was an existing document updated instead of duplicated?
4. Are ADR/RFC statuses correct?
5. Does PRD match the technical design?
6. Are API/database/security/deployment effects represented?
7. Are obsolete current-state docs removed or updated?
8. Does the docs site build?
