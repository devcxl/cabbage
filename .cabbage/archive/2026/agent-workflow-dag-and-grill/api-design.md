---
change: agent-workflow-dag-and-grill
cabbage_stage: api
change_type: feature
---

# Overview

Defines the CLI interface and JSON export schemas for `cabbage tasks <change-id>`.

# Contract

## Operations

| Method or event | Path or topic | Purpose | Authentication | Idempotency |
|---|---|---|---|---|
| CLI Command | `cabbage tasks <change-id>` | Display formatted terminal DAG dashboard | Local file system permissions | Idempotent |
| CLI Flag | `cabbage tasks <change-id> --json` | Output full parsed task tree and status as JSON | Local file system permissions | Idempotent |
| CLI Flag | `cabbage tasks <change-id> --export-dag` | Output subagent parallel dispatch plan | Local file system permissions | Idempotent |

## Inputs and Outputs

| Name | Location | Type | Required | Validation or semantics |
|---|---|---|---|---|
| `change` | CLI Argument | String | Yes | Must match an existing active change ID |
| `--export-dag` | CLI Option | Flag | No | Triggers subagent dispatch JSON emission |
| `--json` | CLI Option | Flag | No | Triggers full AST JSON emission |

### Example `--export-dag` JSON Schema

```json
{
  "change": "agent-workflow-dag-and-grill",
  "summary": {
    "total": 3,
    "completed": 0,
    "ready": 1,
    "blocked": 2
  },
  "parallel_groups": {
    "Group 1": [
      {
        "task_id": "Task 1",
        "title": "Core Engine",
        "builds": "Parser logic",
        "blocked_by": [],
        "verification": "pytest ...",
        "is_ready": true,
        "is_completed": false,
        "status": "ready"
      }
    ]
  },
  "subagent_dispatch_plan": [
    {
      "parallel_group": "Group 1",
      "tasks": [
        {
          "agent": "coder",
          "task_id": "Task 1",
          "title": "Core Engine",
          "builds": "Parser logic",
          "verification": "pytest ...",
          "sop": [
            "[RED] Test Seam",
            "[GREEN] Implement",
            "[REFACTOR] Clean",
            "[VERIFY] Validate"
          ],
          "prompt": "Execute Task 1 following SOP."
        }
      ]
    }
  ]
}
```

# Error Model

| Code or condition | Meaning | Client action | Retryable |
|---|---|---|---|
| Exit Code 2 | `tasks.md` missing or change ID not found | Verify change ID with `cabbage status` | Yes, with correct args |

# Compatibility

Fully backward-compatible. Older `tasks.md` files without structured `## Task` headings fall back cleanly to scanning checklist items under `# Tasks`.

# Security

CLI operates locally without network access. File path traversal is constrained to the Cabbage change directory.

# Observability

Errors write to stderr with prefix `cabbage:`. Exit code 0 indicates clean execution.
