# Document Types & Template Specifications

This reference specifies the purpose, required sections, lifecycle policy, and anti-rot rules for every document type managed by Cabbage.

---

## Document Specification Matrix

| Document | Purpose | Target Path | Required Headings | Lifecycle Rule |
|---|---|---|---|---|
| **PRD** (`prd.md`) | Product vision, scope, functional requirements, and acceptance criteria | `.cabbage/changes/<id>/prd.md` -> `docs/01-product/` | `## Background & Goals`, `## User Stories`, `## Functional Requirements`, `## Non-Functional Requirements`, `## Acceptance Criteria` | Current state |
| **Tech Spec** (`tech-spec.md`) | High-level technical architecture, component design, failure modes | `.cabbage/changes/<id>/tech-spec.md` -> `docs/03-architecture/system-design/` | `## Context & Problem Statement`, `## Architecture & Component Design`, `## Data Flow & Sequence`, `## Failure Handling & Resilience` | Current state |
| **Tasks** (`tasks.md`) | Discrete, verifiable implementation steps & checkboxes | `.cabbage/changes/<id>/tasks.md` | `## Phase 1`, `## Phase 2`, checklist items `- [ ]` | Change workspace |
| **ADR** (`adr.md`) | Architectural decision records with rationale, options, and consequences | `.cabbage/changes/<id>/adr.md` -> `docs/03-architecture/adr/ADR-<num>-<title>.md` | `## Context`, `## Decision`, `## Consequences` (Positive & Negative) | Immutable historical (supersede if changed) |
| **RFC** (`rfc.md`) | Design proposal for cross-team feedback and review | `.cabbage/changes/<id>/rfc.md` -> `docs/03-architecture/rfc/RFC-<num>-<title>.md` | `## Summary`, `## Motivation`, `## Detailed Design`, `## Drawbacks & Alternatives` | Immutable historical |
| **API Design** (`api-design.md`) | REST/gRPC/GraphQL endpoints, request/response models, error codes | `.cabbage/changes/<id>/api-design.md` -> `docs/05-api/` | `## Overview`, `## Endpoints / Schema`, `## Authentication & Headers`, `## Error Codes & Handling` | Current state |
| **Database Design** (`database-design.md`) | Schema changes, indexes, constraints, migration & rollback steps | `.cabbage/changes/<id>/database-design.md` -> `docs/04-data/database-design/` | `## Schema Changes`, `## Indexes & Constraints`, `## Migration Strategy`, `## Rollback & Data Safety` | Current state |
| **Security Review** (`security-review.md`) | Threat modeling, permission boundary, PII, secrets handling | `.cabbage/changes/<id>/security-review.md` -> `docs/09-security/` | `## Attack Surface & Threat Model`, `## Authentication & Authorization`, `## Sensitive Data & Encryption`, `## Mitigations` | Current state |
| **Test Plan** (`test-plan.md`) | Test matrix, unit/integration/E2E coverage, edge cases | `.cabbage/changes/<id>/test-plan.md` -> `docs/08-testing/` | `## Test Strategy & Scope`, `## Test Cases & Scenarios`, `## Regression & Non-Functional Testing` | Change workspace |
| **Release Plan** (`release-plan.md`) | Deployment ordering, environment config, verification, rollback triggers | `.cabbage/changes/<id>/release-plan.md` -> `docs/12-release/` | `## Deployment Sequence`, `## Configuration & Environment`, `## Verification Steps`, `## Rollback Procedure` | Change workspace |
| **Runbook** (`runbook.md`) | Actionable step-by-step operational and troubleshooting guide | `docs/13-operations/runbooks/` | `## Overview`, `## Prerequisites`, `## Step-by-Step Execution`, `## Verification`, `## Troubleshooting & Rollback` | Current state |
| **Incident Postmortem** (`postmortem.md`) | Post-incident analysis, 5-Why root cause, systemic corrective actions | `.cabbage/changes/<id>/postmortem.md` -> `docs/15-incidents/` | `## Summary & Impact`, `## Timeline`, `## Root Cause (5-Why Analysis)`, `## Corrective & Preventative Actions` | Immutable historical |

---

## Anti-Rot & Verification Rules

1. **No Placeholders**: Never leave `TODO`, `TBD`, `FIXME`, or default scaffold placeholder text in any document. `cabbage verify` strictly fails on placeholder detection.
2. **Checked Tasks for Merge**: All `- [ ]` checkboxes in `tasks.md` must be marked as completed (`- [x]`) before `gate merge` can pass.
3. **Diagram Standard**: Diagrams inside architecture and tech specs must use Mermaid rather than static images whenever possible.
4. **Immutable vs. Current-State**:
   - Current-state docs (`docs/01-product/`, `docs/05-api/`, `docs/13-operations/`) are updated in-place.
   - Historical records (`ADR`, `RFC`, `Postmortem`) must never be edited retroactively; write a new ADR/RFC that explicitly supersedes the prior record.
