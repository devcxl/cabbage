import contextlib
import io
import unittest
from cabbage_cli.cli import cmd_tasks
from cabbage_cli.core import CabbageError, parse_tasks_markdown

PLAIN_CHECKLIST_MD = """# Goal

Add user login.

# Design

Minimal change.

# Tasks

- [ ] Write failing test
- [ ] Implement login

# Verification

Pending.
"""


def export_dag_error(markdown):
    """Run the real command against a throwaway change and report its error, if any."""
    import argparse
    from pathlib import Path
    from tempfile import TemporaryDirectory
    from cabbage_cli.scaffold import init_project

    with TemporaryDirectory() as td:
        root = Path(td)
        init_project(root, vendor_cli=False)
        workspace = root / '.cabbage/changes/demo'
        workspace.mkdir(parents=True)
        (workspace / 'change.yaml').write_text('id: demo\ntype: bugfix\nstatus: active\nimpact: {}\n')
        (workspace / 'tasks.md').write_text(markdown)
        import os
        previous = os.getcwd()
        os.chdir(root)
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                cmd_tasks(argparse.Namespace(change='demo', export_dag=True, json=False))
            return None
        except CabbageError as exc:
            return str(exc)
        finally:
            os.chdir(previous)

SAMPLE_DAG_MD = """# Preparation

```mermaid
flowchart TD
    Task1["Task 1: Core Engine"] --> Task2["Task 2: Parallel Extension A"]
    Task1 --> Task3["Task 3: Parallel Extension B"]
    Task2 --> Task4["Task 4: Integration"]
    Task3 --> Task4
```

- [x] Baseline test suite checked

# Tasks

## Task 1: Core Engine Slice
- **Builds**: Core parsing and validation logic
- **Blocked By**: None
- **Parallel Group**: Phase 1
- **Verification**: `pytest tests/test_core.py`
- **Standard Operating Procedure (Task SOP)**:
  1. *[RED]* Define failing test for parser
  2. *[GREEN]* Implement minimal parser logic
  3. *[REFACTOR]* Format and lint code
  4. *[VERIFY]* Assert parser tests pass
- [x] Implement parser behavior
- [x] Add green unit test

## Task 2: Parallel Extension A
- **Builds**: CLI command integration
- **Blocked By**: Task 1
- **Parallel Group**: Phase 2
- **Verification**: `pytest tests/test_cli.py`
- **Standard Operating Procedure (Task SOP)**:
  1. *[RED]* Define CLI execution failure test
  2. *[GREEN]* Hook command into parser
  3. *[REFACTOR]* Clean flags and options
  4. *[VERIFY]* Assert CLI tests pass
- [ ] Implement CLI command binding
- [ ] Verify help text

## Task 3: Parallel Extension B
- **Builds**: Export schema formatting
- **Blocked By**: Task 1
- **Parallel Group**: Phase 2
- **Verification**: `pytest tests/test_export.py`
- **Standard Operating Procedure (Task SOP)**:
  1. *[RED]* Define export schema fixture
  2. *[GREEN]* Implement serializer
  3. *[REFACTOR]* Clean models
  4. *[VERIFY]* Assert schema validation
- [ ] Implement export serializer
- [ ] Add schema assertions

## Task 4: Integration & Convergence
- **Builds**: End-to-end integration and release gate
- **Blocked By**: Task 2, Task 3
- **Parallel Group**: Phase 3
- **Verification**: `pytest tests/test_e2e.py`
- [ ] Full end-to-end integration test

# Verification

- [ ] Run full test suite
"""

class TestTasksDAG(unittest.TestCase):
    def test_parse_rich_dag_tasks(self):
        data = parse_tasks_markdown(SAMPLE_DAG_MD)
        self.assertEqual(data["total_tasks"], 4)
        self.assertEqual(data["completed_tasks"], 1) # Task 1 is completed
        self.assertEqual(data["ready_tasks"], 2)     # Task 2 and Task 3 are ready because Task 1 is done
        self.assertEqual(data["blocked_tasks"], 1)   # Task 4 is blocked by Task 2 and Task 3

        # Check Task 1
        t1 = data["tasks"][0]
        self.assertEqual(t1["task_id"], "Task 1")
        self.assertEqual(t1["status"], "done")
        self.assertTrue(t1["is_completed"])
        self.assertFalse(t1["is_ready"])
        self.assertEqual(len(t1["sop"]), 4)

        # Check Task 2 & 3 readiness
        t2 = data["tasks"][1]
        self.assertEqual(t2["task_id"], "Task 2")
        self.assertEqual(t2["status"], "ready")
        self.assertTrue(t2["is_ready"])
        self.assertEqual(t2["parallel_group"], "Phase 2")

        t3 = data["tasks"][2]
        self.assertEqual(t3["task_id"], "Task 3")
        self.assertEqual(t3["status"], "ready")
        self.assertTrue(t3["is_ready"])
        self.assertEqual(t3["parallel_group"], "Phase 2")

        # Check Task 4 blocked
        t4 = data["tasks"][3]
        self.assertEqual(t4["task_id"], "Task 4")
        self.assertEqual(t4["status"], "blocked")
        self.assertFalse(t4["is_ready"])
        self.assertIn("Task 2", t4["unresolved_deps"])
        self.assertIn("Task 3", t4["unresolved_deps"])

        # Check subagent dispatch plan
        dispatch = data["subagent_dispatch_plan"]
        self.assertEqual(len(dispatch), 1) # Phase 2 has ready tasks
        phase2_plan = dispatch[0]
        self.assertEqual(phase2_plan["parallel_group"], "Phase 2")
        self.assertEqual(len(phase2_plan["tasks"]), 2)
        task_ids = [item["task_id"] for item in phase2_plan["tasks"]]
        self.assertIn("Task 2", task_ids)
        self.assertIn("Task 3", task_ids)

    def test_plain_checklist_is_not_structured(self):
        data = parse_tasks_markdown(PLAIN_CHECKLIST_MD)
        self.assertEqual(2, data["total_tasks"])
        self.assertFalse(data["structured"])
        self.assertIsNone(data["mermaid"])

    def test_plain_checklist_produces_no_dispatch_plan(self):
        data = parse_tasks_markdown(PLAIN_CHECKLIST_MD)
        self.assertEqual([], data["subagent_dispatch_plan"])

    def test_structured_tasks_are_flagged_as_structured(self):
        data = parse_tasks_markdown(SAMPLE_DAG_MD)
        self.assertTrue(data["structured"])

    def test_export_dag_refuses_plain_checklist(self):
        error = export_dag_error(PLAIN_CHECKLIST_MD)
        self.assertIsNotNone(error, "plain checklists must not produce a dispatch plan")
        self.assertIn("no structured DAG", error)

    def test_export_dag_allows_structured_tasks(self):
        self.assertIsNone(export_dag_error(SAMPLE_DAG_MD))


if __name__ == "__main__":
    unittest.main()
