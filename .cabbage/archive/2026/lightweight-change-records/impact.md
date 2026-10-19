---
change: lightweight-change-records
cabbage_stage: impact
---
# Impact Matrix

| Area | Impact | Detail |
| --- | --- | --- |
| Product | Yes | New-project default becomes one record. |
| Architecture | Yes | Reuse stage engine with conditional specialist prerequisites. |
| Testing | Yes | Add lightweight, compatibility and executable guide regressions. |
| API | No | CLI argument syntax remains unchanged. |
| Database | No | No persistence schema migration. |
| Security | No | Existing repository permission boundary remains required. |
| Deployment | No | No pipeline or release behavior change. |

# Risks

Existing project signatures must not be invalidated by an implicit workflow upgrade. Risk declarations remain a human/agent responsibility. Guides must distinguish the new defaults from old project workflows and avoid implying that a content hash proves approval.
