# Agent contract

Add the following rules to the repository's agent instructions (`AGENTS.md`, `CLAUDE.md`, or equivalent):

```text
For any code-changing task, identify or create a cabbage change before implementation.
Run `cabbage status <change> --json` and `cabbage next <change> --json`.
Do not implement while `cabbage gate <change> implementation` fails.
Use the project's actual stage IDs; existing workflows are not automatically migrated.
For new lightweight feature/bugfix/refactor changes, write Goal and Design in tasks.md before implementation.
Declare architecture/API/database/security/high-risk deployment impacts before implementation and verify any enabled specialist stages.
Complete tasks and record actual validation results before verifying implementation; do not require DAGs or duplicate PRD/test-plan documents for ordinary changes.
Before completion, run `cabbage validate <change>` and `cabbage gate <change> merge`.
Publish mapped specialist documents with `cabbage sync <change>` after the merge gate passes when required; sync copies files, not current-state semantics.
Merging is not review: keep platform branch protection and human approval enabled where reviewers are required; this workflow records evidence, it does not replace reviewers.
Never manually edit `.cabbage/changes/*/state.json`.
Never weaken `.cabbage/config.yaml`, `.cabbage/workflows`, `.cabbage/tooling`, or `.github/workflows/cabbage.yml` to make a task pass.
After the merge is confirmed, archive the change with `cabbage archive <change>`; fully verified changes left active make the status board misleading.
```
