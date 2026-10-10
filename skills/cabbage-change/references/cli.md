# Cabbage CLI Reference

Comprehensive command-line interface specification for Cabbage document lifecycle management.

## Syntax & Exit Codes

```bash
cabbage <command> [arguments] [options]
```

### Exit Codes

- `0` (`SUCCESS`): Command completed successfully, validation passed, or gate allowed.
- `1`: `validate`, `gate`, or `ci` reported errors.
- `2`: Argument parsing or a handled `CabbageError`, including a failed `verify`.
  `next` also returns `2` when work remains but no stage is currently actionable.
- `130`: Interrupted execution. `docs` forwards the pnpm process exit code; unexpected exceptions are not normalized.

---

## Command Matrix

### 1. Environment & Initialization

#### `cabbage doctor [--json]`
Diagnose runtime environment and project dependencies.
- **Checks**: Python (>= 3.10), PyYAML, Git CLI, pnpm CLI, Cabbage project integrity.
- **Flags**: `--json` output structured diagnostic report.

```bash
cabbage doctor
```

#### `cabbage init [--force] [--no-vendor-cli]`
Initialize a greenfield project with `.cabbage/` configuration, workflows, and `docs/` VitePress documentation site.
- **Flags**:
  - `--force`: Overwrite existing `.cabbage/` configuration and templates.
  - `--no-vendor-cli`: Skip bundling the CLI script into `.cabbage/tooling/`.

```bash
cabbage init
```

#### `cabbage adopt [--apply] [--json]`
Inventory and optionally migrate existing project documentation outside the `docs/` directory.
- **Flags**:
  - `--apply`: Automatically apply suggested moves (`migrate` and `import`) by moving files on disk.
  - `--json`: Output inventory JSON.
- **Reference**: See `references/adoption.md` for the complete 7-phase adoption guide.

```bash
cabbage adopt
cabbage adopt --apply
```

---

### 2. Change Lifecycle Management

#### `cabbage new <type> <change-id>`
Create a new active change workspace under `.cabbage/changes/<change-id>/`.
- **Arguments**:
  - `<type>`: `feature` | `architecture` | `bugfix` | `hotfix` | `refactor` | `migration` | `integration` | `incident`
  - `<change-id>`: Unique identifier in kebab-case (e.g., `user-oauth-login`).
- **Behavior**: Creates `change.yaml` and enabled workflow artifacts. `state.json` is created on first successful verification. New projects use one `tasks.md` for `feature`, `bugfix`, and `refactor`; risk flags add only related specialist documents. Existing project workflows are not automatically upgraded. Use `status` or `next` to inspect actual stages.

```bash
cabbage new feature user-oauth-login
```

#### `cabbage status [change-id] [--json]`
Display the progress and verification status of a specific change or all active changes.
Without `--json` it prints human-readable text; `--json` keeps the structured shape unchanged.
- **Stage Statuses**: `pending` / `done` / `stale` / `skipped`; definitions and the state machine are in `lifecycle.md`.

```bash
cabbage status user-oauth-login
cabbage status --json
```

#### `cabbage next <change-id> [--json]`
Inspect ready (unblocked) stages and blocked stages based on workflow dependency graph.
Without `--json` it prints human-readable text; `--json` keeps the structured shape unchanged.

```bash
cabbage next user-oauth-login
```

#### `cabbage impact <change-id> [--set field=true|false] [--json]`
Inspect or mutate the impact analysis matrix of a change.
- **Available Fields**: the project's `impact_fields`, which new projects default to `product`, `architecture`, `api`, `database`, `security`, `testing`, `deployment`, `operations`, `performance`.
- **Behavior**: Updates `change.yaml`, generates enabled conditional artifacts, and updates an existing impact table. Affected verified stages derive `stale` status from changed signatures; unrelated stages need not become stale.
  Without `--json` it prints one `field` and `Yes`/`No` line per impact field; `--json` keeps the structured shape unchanged.

```bash
cabbage impact user-oauth-login --set api=true --set database=true
```

#### `cabbage tasks <change-id> [--export-dag] [--json]`
Inspect checklist progress and, for structured tasks, dependencies and parallel readiness.
- **Behavior**: A plain `# Tasks` checklist is the default and needs no DAG. Only
  `## Task <id>: <title>` sections (with `Builds`, `Blocked By`, `Parallel Group`,
  `Verification`) form a structured DAG; anything else is reported as a plain checklist.
- **Flags**:
  - `--json`: Output parsed tasks and parallel groups as structured JSON (includes `structured`).
  - `--export-dag`: Output a subagent dispatch plan for unblocked tasks. Exits with an error
    when `tasks.md` has no structured sections, because a plain checklist declares no
    dependencies or verification commands. It emits data only; it never executes tasks.

```bash
cabbage tasks user-oauth-login
cabbage tasks user-oauth-login --export-dag
cabbage tasks user-oauth-login --json
```

#### `cabbage discard <change-id>`
Delete an active change workspace and clean up its pending artifacts.

```bash
cabbage discard user-oauth-login
```

---

### 3. Verification & Quality Gates

#### `cabbage verify <change-id> <stage>`
Verify a single stage artifact, check content completeness, ensure no placeholders or unchecked tasks, and record the cryptographic signature in `state.json`.
- **Checks**: upstream dependencies are `done`, artifact/frontmatter/headings are valid, no placeholders or unchecked tasks remain, local links and Mermaid fences resolve. See `validation.md` for the full automatic-check scope.

```bash
# Use stage IDs returned by `next`, not artifact filenames.
# A new project's ordinary feature needs only this after implementation and tests:
cabbage verify user-oauth-login implementation
# If api=true, verify `api` before starting implementation, then verify implementation again.
```

#### `cabbage validate [<change-id> | --all] [--json]`
Validate Markdown integrity, frontmatter, heading structures, and link resolution across one or all active changes.

```bash
cabbage validate user-oauth-login
cabbage validate --all
```

#### `cabbage gate <change-id> <target> [--json]`
Evaluate readiness for specific milestones in the software development lifecycle.
- **Targets**: `implementation` covers the enabled stages before it; `merge` and `archive` require every enabled stage and do not inspect Git merge status. The full gate table is in `lifecycle.md`.

```bash
cabbage gate user-oauth-login implementation
cabbage gate user-oauth-login merge
cabbage gate user-oauth-login archive
```

---

### 4. Sync, Archive & CI

#### `cabbage sync <change-id> [--json]`
Copy enabled, existing artifacts with a configured mapping into `docs/`. This command does not check verification status or semantically merge specifications; run `gate merge` first when publishing final documents. Default filenames use the change ID, not an auto-assigned ADR number.

```bash
cabbage sync user-oauth-login
```

#### `cabbage archive <change-id>`
Validate the `archive` gate, sync final specifications to `docs/`, mark status as `archived`, and move the workspace to `.cabbage/archive/<YEAR>/<change-id>/`.

```bash
cabbage archive user-oauth-login
```

#### `cabbage ci --base <git-ref>`
Inspect `<base>...HEAD`, require an active changed change record for code changes, and validate changed active records, their merge gates, and configured current-document paths. New lightweight workflows declare `record_covers: [product, testing]`, so these two areas need no duplicate docs-path changes. Other impact rules remain enforced, and old workflows retain their existing rules. It neither validates every unchanged active record nor runs a documentation build; run `validate --all` and `docs build` separately.

```bash
cabbage ci --base origin/main
```

---

### 5. Documentation Site Operations

#### `cabbage docs <install|dev|build>`
Manage the embedded VitePress documentation site under `docs/`.
- `install`: Run `pnpm install` in `docs/`.
- `dev`: Launch local live-reload VitePress development server.
- `build`: Execute static production build (`docs/.vitepress/dist/`).

```bash
cabbage docs install
cabbage docs dev
cabbage docs build
```
