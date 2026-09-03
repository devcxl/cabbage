---
origin_change: agent-workflow-dag-and-grill
change_type: feature
cabbage_stage: requirement
synced_at: '2026-09-03T22:00:40.420517+00:00'
---

# Goal

Enhance Cabbage workflow with pre-flight Grill-Me context alignment, architectural multi-proposal comparisons, asymmetric human-AI decision boundaries, and standardized task DAG SOP execution.

## Grill-Me Alignment Summary

- **Core Problem & Value**: Engineering agents frequently suffer from ambiguous scope, shallow single-proposal designs, and chaotic unguided task execution. Introducing pre-flight grilling and DAG SOPs creates a deterministic path from requirement exploration to multi-subagent dispatch.
- **Assumptions Validated**: Human decision bandwidth is constrained (frontal-lobe bottleneck); micro-technical choices should be resolved autonomously by AI while strategic business and architectural gates remain with humans.

# Users and Use Cases

| User or actor | Need | Primary use case |
|---|---|---|
| AI Orchestrator / Main Agent | Structured DAG dispatch payload | Parse `tasks.md` and delegate independent slices to worker subagents |
| Human Engineer / Reviewer | Less cognitive fatigue on minor details | Focus reviews on architecture options, public contracts, and gates |
| Worker Subagent | Deterministic task execution standard | Follow 4-step SOP (RED -> GREEN -> REFACTOR -> VERIFY) without deviation |

# Scope

## In Scope

- Pre-flight Grill-Me protocol guidance in SKILL and PRD templates.
- Architecture Options Comparison matrix in technical specifications.
- Asymmetric decision boundaries (AI Autonomous vs. Human Gate).
- Task SOP standard operating procedure definition in DAG tasks.
- CLI command `cabbage tasks <change-id>` supporting DAG inspection, `--json`, and `--export-dag`.

## Out of Scope

- Bi-directional interactive web forms inside VitePress documentation site (static site remains read-only).
- Direct process spawning or execution daemon for subagents (Cabbage remains an orchestration and gate system).

## Decision Boundaries

- **AI Autonomous Decisions**: Regex parser optimization, internal AST structure, terminal ANSI rendering, unit test fixtures.
- **Human Gate Decisions**: CLI command syntax, schema specification for `--export-dag`, workflow gate criteria.

# Requirements

| ID | Requirement (SHALL/MUST) | Priority | Rationale |
|---|---|---|---|
| R-1 | CLI SHALL provide `cabbage tasks <change-id>` to parse tasks DAG. | Must | Enables visibility into DAG topology and task dependencies. |
| R-2 | CLI SHALL support `--export-dag` to emit machine-readable dispatch plans. | Must | Enables multi-subagent orchestration and parallel worker threads. |
| R-3 | Templates MUST include Grill-Me, Decision Boundaries, and Task SOP sections. | Must | Standardizes engineering lifecycle artifacts across the repository. |

# Acceptance Criteria

### Scenario 1: DAG Inspection and Subagent Export
- **GIVEN**: A change with valid `tasks.md` containing Mermaid DAG and task slices
- **WHEN**: Operator runs `cabbage tasks <change-id> --export-dag`
- **THEN**: CLI outputs structured JSON with summary, parallel groups, and ready tasks with SOP prompts
- [x] Verified via `tests/test_tasks_dag.py` and integration runs

# Success Metrics

| Metric | Baseline | Target | Measurement window |
|---|---|---|---|
| DAG parsing test coverage | 0% | 100% core coverage | Immediate upon commit |
| CLI command latency | N/A | < 150ms | Every CLI run |

# Dependencies and Constraints

- Requires Python 3.10+ standard library (`re`, `json`, `pathlib`, `argparse`).
- Zero external runtime dependencies beyond PyYAML.

# Risks

| Risk | Impact | Mitigation |
|---|---|---|
| Irregular markdown formatting in tasks.md | Incomplete DAG extraction | Robust fallback to checklist items when structured headers are absent |

# Open Questions

- N/A
