# Workflow decision tree

```text
Change
├─ New capability → feature
├─ System boundary/runtime/storage/topology change → architecture
├─ Defect without incident → bugfix
├─ Urgent production patch → hotfix
├─ Internal structure only → refactor
├─ DB/data/platform movement → migration
├─ Third-party connection → integration
└─ Production incident → incident
```

After selecting a type, run impact analysis. Conditional documents are enabled from impact flags, not by intuition alone.
