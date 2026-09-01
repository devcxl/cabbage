# cabbage CLI reference

```text
cabbage init [--force] [--no-vendor-cli]
cabbage adopt [--json]
cabbage new <type> <change-id>
cabbage status [change-id] [--json]
cabbage next <change-id> [--json]
cabbage impact <change-id> [--set field=true|false] [--json]
cabbage validate <change-id> | --all [--json]
cabbage verify <change-id> <stage>
cabbage sync <change-id> [--json]
cabbage gate <change-id> implementation|merge|archive [--json]
cabbage archive <change-id>
cabbage ci --base <git-ref>
cabbage docs install|dev|build
```

Exit codes:

- `0`: allowed / valid / verified
- `1`: gate or CI validation failure
- `2`: command/config/workflow error

`adopt` actions (see `references/adoption.md`):

- `keep`: document already lives in the standard current-state tree
- `migrate`: current-state document proposed to move into the standard tree
- `import`: historical record (ADR/RFC/incident) proposed to archive as-is
- `review`: unclassified; requires a human decision

`status` values:

- `pending`: not verified
- `done`: verified and signature is current
- `stale`: verified before an upstream/artifact/workflow change
- `skipped`: disabled by current impact conditions
