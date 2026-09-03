---
change: agent-workflow-dag-and-grill
cabbage_stage: impact
change_type: feature
---

# Change Summary

Upgrades Cabbage artifact templates, documentation guides, and CLI capabilities to include pre-flight Grill-Me protocols, Architecture Options comparisons, asymmetric decision boundaries, and DAG task SOP parsing with Subagent dispatch plan generation.

# Impact Matrix

| Area | Impact | Notes |
|---|---|---|
| Product | Yes | Workflow enhanced with pre-flight alignment and decision tiers |
| Architecture | Yes | Introduces asymmetric decision model and multi-proposal specs |
| API | Yes | Adds `cabbage tasks` command with `--export-dag` and `--json` |
| Database | No | No schema or database changes |
| Security | No | No security boundary alterations |
| Testing | Yes | Adds unit test suite `test_tasks_dag.py` covering DAG parser |
| Deployment | No | Standard client/CLI deployment unchanged |
| Operations | No | Operational processes unchanged |
| Data | No | No data format migration |
| Performance | No | Fast local parsing; negligible execution overhead |

# Impact Details

- **Product**: Developers and agents follow structured pre-flight grilling and explicit non-goals definition before authoring PRDs.
- **Architecture**: Tech specifications now formally evaluate 2 to 3 architectural options with documented trade-offs, separating AI autonomy from human gate approvals.
- **API**: CLI surface expanded with `cabbage tasks <change-id>` for terminal visualization and machine-readable subagent dispatch export.
- **Testing**: Added comprehensive DAG parsing test suite ensuring topological readiness and dependency resolution.

# Risks

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Malformed task checkboxes in tasks.md | Low | Low | Fallback parsing logic ensures flat task extraction | Cabbage Core Team |

# Documentation Updates

- Update `SKILL.md` with Pre-Flight Alignment, Architecture Options, Task SOP, and Subagent Orchestration.
- Update `README.md` and `references/cli.md` with `cabbage tasks` command.
- Update `references/document-types.md` with Task SOP and Architecture Options standards.
