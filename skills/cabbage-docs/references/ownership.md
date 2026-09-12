# Documentation Ownership & Governance

Documentation without clear ownership degrades quickly. In Cabbage, documentation ownership directly reflects system and module ownership.

---

## 1. Ownership Principles

1. **Code & Documentation Parity**: The engineering team or engineer that owns a service/module is responsible for its architecture, API, database schema, and runbook documentation.
2. **Atomic Ownership**: Keep existing module documentation accurate in the same PR. Small changes in new lightweight workflows record product intent and test evidence in `tasks.md`; do not create duplicate documents solely to satisfy process. High-risk and other configured impact rules still apply.
3. **Explicit Frontmatter Attribution**: Critical long-lived documentation should declare ownership in frontmatter:

```yaml
---
title: Payment Service Architecture
owner: team-billing
maintained-by:
  - "@alice"
  - "@bob"
last-reviewed: 2026-03-01
---
```

---

## 2. CODEOWNERS Integration

Repositories should leverage `.github/CODEOWNERS` to ensure document changes are reviewed by respective domain leads.
Document-review paths belong here; governance paths for Cabbage configuration, workflows, tooling and CI
are listed in the `cabbage-adopt` skill (`references/enforcement.md`) so there is one authoritative copy.

```text
# Architecture & ADRs require Principal / Architect review
/docs/03-architecture/ @lead-architect

# Security reviews require SecOps approval
/docs/09-security/ @security-team
```
