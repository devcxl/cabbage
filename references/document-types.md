# Document Types & Template Specifications

This reference specifies the purpose, required sections, structural rules, and anti-rot standards for every document type managed by Cabbage.

---

## 1. Document Specification Matrix

| Document | Purpose | Target Path | Required Headings | Lifecycle Rule |
|---|---|---|---|---|
| **PRD** (`prd.md`) | Product vision, user stories, functional scope, acceptance criteria | `.cabbage/changes/<id>/prd.md` -> `docs/01-product/` | `## Background & Goals`, `## User Stories`, `## Functional Requirements`, `## Non-Functional Requirements`, `## Acceptance Criteria` | Current state |
| **Tech Spec** (`tech-spec.md`) | Technical architecture, component boundaries, testing decisions, failure modes | `.cabbage/changes/<id>/tech-spec.md` -> `docs/03-architecture/system-design/` | `## Context & Problem Statement`, `## Architecture & Component Design`, `## Testing Decisions`, `## Data Flow & Sequence`, `## Failure Handling & Resilience` | Current state |
| **Tasks** (`tasks.md`) | Discrete, vertical tracer-bullet slices & checklist items | `.cabbage/changes/<id>/tasks.md` | `## Task Plan & DAG`, `## Phase 1`, `## Phase 2`, checklist items `- [ ]` | Change workspace |
| **ADR** (`adr.md`) | Architectural decision records with rationale, options, and consequences | `.cabbage/changes/<id>/adr.md` -> `docs/03-architecture/adr/ADR-<num>-<title>.md` | `## Context`, `## Decision`, `## Consequences` (Positive & Negative) | Immutable historical (supersede if changed) |
| **RFC** (`rfc.md`) | Design proposal for cross-team feedback and consensus | `.cabbage/changes/<id>/rfc.md` -> `docs/03-architecture/rfc/RFC-<num>-<title>.md` | `## Summary`, `## Motivation`, `## Detailed Design`, `## Drawbacks & Alternatives` | Immutable historical |
| **API Design** (`api-design.md`) | REST/gRPC/GraphQL endpoints, request/response models, error codes | `.cabbage/changes/<id>/api-design.md` -> `docs/05-api/` | `## Overview`, `## Endpoints / Schema`, `## Authentication & Headers`, `## Error Codes & Handling` | Current state |
| **Database Design** (`database-design.md`) | Schema changes, indexes, constraints, migration & rollback steps | `.cabbage/changes/<id>/database-design.md` -> `docs/04-data/database-design/` | `## Schema Changes`, `## Indexes & Constraints`, `## Migration Strategy`, `## Rollback & Data Safety` | Current state |
| **Security Review** (`security-review.md`) | Threat modeling, permission boundaries, PII, secrets handling | `.cabbage/changes/<id>/security-review.md` -> `docs/09-security/` | `## Attack Surface & Threat Model`, `## Authentication & Authorization`, `## Sensitive Data & Encryption`, `## Mitigations` | Current state |
| **Test Plan** (`test-plan.md`) | Test matrix, test seam verification, regression & non-functional coverage | `.cabbage/changes/<id>/test-plan.md` -> `docs/08-testing/` | `## Test Strategy & Scope`, `## Test Cases & Scenarios`, `## Regression & Non-Functional Testing` | Change workspace |
| **Release Plan** (`release-plan.md`) | Deployment ordering, environment config, verification, rollback triggers | `.cabbage/changes/<id>/release-plan.md` -> `docs/12-release/` | `## Deployment Sequence`, `## Configuration & Environment`, `## Verification Steps`, `## Rollback Procedure` | Change workspace |
| **Runbook** (`runbook.md`) | Actionable step-by-step operational and troubleshooting guide | `docs/13-operations/runbooks/` | `## Overview`, `## Prerequisites`, `## Step-by-Step Execution`, `## Verification`, `## Troubleshooting & Rollback` | Current state |
| **Incident Postmortem** (`postmortem.md`) | Post-incident analysis, 5-Why root cause, systemic corrective actions | `.cabbage/changes/<id>/postmortem.md` -> `docs/15-incidents/` | `## Summary & Impact`, `## Timeline`, `## Root Cause (5-Why Analysis)`, `## Corrective & Preventative Actions` | Immutable historical |

---

## 2. Deep Module & Testing Decisions Standards (Tech Spec)

Technical specifications must describe verifiable, testable system boundaries using the following design language:

- **Module**: A bounded component with a clear Interface and Implementation.
- **Interface**: The minimal contract required to use the Module (inputs, outputs, errors, side effects).
- **Test Seam**: A public interface boundary where behavior is observed or replaced during testing.
- **Depth**: A module is deep when its Interface is small and simple, but encapsulates significant complexity behind it. Avoid shallow "pass-through" layers.
- **No Mock-Driven Abstractions**: Do not introduce interfaces or adapter layers solely to facilitate unit test mocking when only a single production implementation exists.

### Mandatory `## Testing Decisions` Section

Every non-trivial `tech-spec.md` must declare:
1. **Target Behavior**: The specific capability or requirement to verify.
2. **Public Test Seam**: The exact public interface or entry point used to exercise the behavior.
3. **Observable Outcome**: The expected return value, state change, or output.
4. **Test Level**: Unit (isolated module), Integration (multi-module seam), or End-to-End.

---

## 3. Vertical Slices & Pre-Refactor Standards (Tasks)

Task breakdown in `tasks.md` must follow tracer-bullet engineering principles:

1. **Vertical Behavior Slices**: Each task must deliver a complete, observable slice of behavior across layers, rather than horizontal technical layers (e.g. avoid "Task 1: Create DB table", "Task 2: Write DAO", "Task 3: Write Controller").
2. **Fresh-Context Friendly**: Each task should be self-contained enough that a developer can implement and verify it without reading the entire historical thread.
3. **Behavior-Preserving Pre-Refactor**:
   - When existing codebase structures block a clean vertical slice, define an explicit Pre-Refactor task.
   - Pre-refactors must be behavior-preserving, verified against existing test suites, and focused strictly on removing the specific structural blocker (no speculative generalizations).
4. **Checked Tasks for Merge**: All `- [ ]` checklist items must be completed (`- [x]`) before `cabbage gate <change> merge` is allowed.

---

## 4. Anti-Rot & Verification Rules

1. **No Placeholders**: Never leave `TODO`, `TBD`, `FIXME`, or default scaffold placeholder text in any document. `cabbage verify` strictly fails on placeholder detection.
2. **Immutable vs. Current-State**:
   - Current-state docs are updated in-place to reflect reality.
   - Historical records (`ADR`, `RFC`, `Postmortem`) must never be edited retroactively; write a new ADR/RFC that explicitly supersedes the prior record.
3. **Mermaid Diagrams**: Architectural flow, state, and sequence diagrams must use Mermaid code blocks rather than static image assets.
