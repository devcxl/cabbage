---
origin_change: agent-workflow-dag-and-grill
change_type: feature
cabbage_stage: adr
synced_at: '2026-09-03T22:00:40.422056+00:00'
---

# Status

Accepted on 2025-09-02 by Cabbage Architecture Review.

# Context

To scale complex multi-subagent autonomous workflows while preventing human cognitive fatigue, the system must separate autonomous micro-decisions from strategic human gate decisions, while formalizing a deterministic 4-step task SOP protocol.

# Decision Drivers

- Cognitive offloading: Protect human frontal-lobe bandwidth.
- Deterministic subagent execution: Guarantee every task executes via RED -> GREEN -> REFACTOR -> VERIFY.
- Zero-dependency CLI integration: Retain lightweight Python standard library runtime.

# Considered Options

| Option | Benefits | Drawbacks | Outcome |
|---|---|---|---|
| Native DAG Parser & Asymmetric Decision Model | High speed, no dependencies, clear human/AI boundaries | Requires explicit markdown structure | Selected |
| External Workflow Engine Integration | Rich graph features | Heavyweight runtime dependencies | Rejected |

# Decision

Adopt the Asymmetric Decision Model (AI Autonomous vs. Human Gate) across PRD and Tech-Spec templates, enforce the 4-step Task SOP across all DAG tasks, and provide `cabbage tasks` for native DAG inspection and dispatch plan export.

# Consequences

## Positive

- Clear separation of concerns between AI exploration and human governance.
- Subagents receive self-contained task contracts with targeted verification commands.
- High velocity through parallel branch execution.

## Negative

- Tasks markdown must strictly adhere to the structured task format to unlock DAG export features.

## Risks

- Minor formatting variations handled through graceful fallback parsing.

# Validation

Validated via `tests/test_tasks_dag.py` and real-world execution on active Cabbage changes.
