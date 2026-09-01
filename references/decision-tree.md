# Workflow & Change Type Decision Tree

This guide defines how to classify changes and activate conditional artifacts in Cabbage.

## 1. Classification Decision Tree

```text
Change Intake
│
├── Adds new business capability or user-visible feature?
│   └── -> Type: `feature`
│
├── Alters system boundaries, runtime topology, major tech stack, or distributed protocols?
│   └── -> Type: `architecture`
│
├── Corrects a non-production-outage functional defect or regression?
│   └── -> -> Type: `bugfix`
│
├── Urgent production patch requiring rapid hot-patching?
│   └── -> Type: `hotfix`
│
├── Internal structural refactoring without external behavioral changes?
│   └── -> Type: `refactor`
│
├── Database schema evolution, data backfill, or platform/runtime migration?
│   └── -> Type: `migration`
│
├── Connecting with third-party APIs, webhooks, or external SaaS platforms?
│   └── -> Type: `integration`
│
└── Production incident response, post-mortem, and corrective action tracking?
    └── -> Type: `incident`
```

---

## 2. Change Type Overview

| Change Type | Primary Focus | Mandatory Artifacts | Typical Conditional Artifacts |
|---|---|---|---|
| `feature` | End-user or business capabilities | `prd`, `impact`, `tasks` | `tech-spec`, `api-design`, `database-design`, `security-review`, `test-plan`, `release-plan` |
| `architecture` | Structural & systemic topology | `impact`, `tech-spec`, `adr`, `tasks` | `security-review`, `test-plan`, `release-plan` |
| `bugfix` | Defect resolution & root cause fix | `impact`, `tasks` | `test-plan`, `release-plan` |
| `hotfix` | Fast-track urgent production patch | `impact`, `tasks` | `release-plan` |
| `refactor` | Code restructuring without feature change | `impact`, `tech-spec`, `tasks` | `test-plan`, `benchmark` |
| `migration` | Data model, schema, storage migration | `impact`, `database-design`, `tasks` | `release-plan`, `test-plan` |
| `integration`| External SaaS, API, protocol adapter | `impact`, `api-design`, `security-review`, `tasks` | `test-plan`, `release-plan` |
| `incident` | Production failure triage & postmortem | `incident`, `postmortem` | `tasks` (corrective actions) |

---

## 3. Impact Analysis Matrix & Conditional Activation

Impact analysis determines which conditional stages are activated. Run:

```bash
cabbage impact <change-id> --set <field>=true|false
```

| Impact Field | When to Enable (`true`) | Activated Artifact / Stage |
|---|---|---|
| `product` | Changes product behavior, user workflows, or UI/UX | `prd` |
| `architecture` | Introduces new components, alters boundaries, or introduces ADRs | `tech-spec`, `adr` |
| `api` | Modifies REST/GraphQL/gRPC interfaces, DTOs, or webhooks | `api-design` |
| `database` | Adds/modifies tables, fields, indexes, or requires data backfill | `database-design` |
| `security` | Touches auth, permissions, secrets, PII, or attack surface | `security-review` |
| `testing` | Requires special test scenarios, load testing, or E2E suites | `test-plan` |
| `deployment` | Involves infra changes, env vars, migrations, or release steps | `release-plan` |
| `operations` | Changes logging, alerting, metrics, or runbooks | `runbooks` |
| `data` | Alters data pipelines, ETL, caching, or event streaming | `data-flow` |
| `performance` | Performance-critical changes, latency/throughput requirements | `benchmark` |

---

## 4. Rule of Thumb

1. **When in doubt, run `cabbage impact <change>` first**; let the impact flags guide artifact generation.
2. **Never create redundant standalone docs**; activate conditional stages in the change workflow.
3. **Changing impact triggers cascading invalidation**; downstream completed stages will become `stale` and must be re-verified.
