---
change: agent-workflow-dag-and-grill
cabbage_stage: tests
change_type: feature
---

# Strategy

Verify the DAG task parser, dependency resolution, topological readiness calculation, and CLI command execution across structured DAG files and legacy flat checklists.

| Level | Scope | Test seam | Owner |
|---|---|---|---|
| Unit | Core Markdown DAG parser | `core.parse_tasks_markdown()` | Test Team |
| Integration | CLI command execution | `cli.cmd_tasks()` | CLI Team |

# Test Environment and Data

Standard Python 3.10+ unittest execution without mocking. Isolated string fixtures mimicking complex Mermaid diagrams and multi-task dependencies.

# Cases

| ID | Scenario | Level | Expected result | Priority |
|---|---|---|---|---|
| T-1 | Parse rich DAG with completed, ready, and blocked tasks | Unit | Accurate task counts and readiness status flags | High |
| T-2 | Generate subagent dispatch plan for unblocked tasks | Unit | Ready tasks grouped by parallel_group with SOP steps | High |
| T-3 | Fallback parsing for legacy flat checkbox lists | Integration | Flat checklists parsed into tasks with clean defaults | High |

# Regression Coverage

Existing test suites `test_cabbage.py`, `test_templates.py`, and `test_adopt.py` ensure all prior CLI commands, template validations, and git operations remain fully functional.

# Non-functional Testing

| Quality attribute | Method | Threshold |
|---|---|---|
| Performance | Execute full test suite `python3 -m unittest discover tests` | Entire suite runs in < 3.0 seconds |

# Entry and Exit Criteria

- Entry: Working implementation in `cabbage_cli/core.py` and `cabbage_cli/cli.py`.
- Exit: All 32 automated tests pass with 0 failures and 0 errors.

# Risks

- None. Local in-memory execution with no external network dependencies.
