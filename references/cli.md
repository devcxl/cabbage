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
  - `--apply`: Automatically apply suggested moves (`migrate` and `import`) using Git.
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
- **Behavior**: Creates `change.yaml` and enabled workflow artifacts. `state.json` is created on first successful verification. Use `status` or `next` to inspect stages.

```bash
cabbage new feature user-oauth-login
```

#### `cabbage status [change-id] [--json]`
Display the progress and verification status of a specific change or all active changes.
- **Stage Statuses**:
  - `pending`: Artifact template created but not yet verified.
  - `done`: Verified with valid SHA-256 signature and all dependencies satisfied.
  - `stale`: Upstream dependency, workflow definition, or artifact was modified after verification.
  - `skipped`: Deactivated by current impact matrix settings.

```bash
cabbage status user-oauth-login
cabbage status --json
```

#### `cabbage next <change-id> [--json]`
Inspect ready (unblocked) stages and blocked stages based on workflow dependency graph.

```bash
cabbage next user-oauth-login
```

#### `cabbage impact <change-id> [--set field=true|false] [--json]`
Inspect or mutate the impact analysis matrix of a change.
- **Available Fields**: `product`, `architecture`, `api`, `database`, `security`, `testing`, `deployment`, `operations`, `data`, `performance`.
- **Behavior**: Updates `change.yaml`, generates enabled conditional artifacts, and updates an existing impact table. Affected verified stages derive `stale` status from changed signatures; unrelated stages need not become stale.

```bash
cabbage impact user-oauth-login --set api=true --set database=true
```

#### `cabbage tasks <change-id> [--export-dag] [--json]`
Inspect DAG task topology, checklist progress, dependencies, and readiness for parallel execution.
- **Flags**:
  - `--json`: Output full parsed task objects, DAG topology, and parallel groups as structured JSON.
  - `--export-dag`: Output machine-readable subagent dispatch plan with unblocked tasks and execution prompts for parallel worker threads.

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
- **Checks**:
  - All upstream dependencies are in `done` state.
  - Artifact file exists and frontmatter matches change ID and stage.
  - Required section headings are present.
  - No legacy placeholders or `TODO` / `TBD` / `FIXME` / `CABBAGE` markers remain.
  - No unchecked tasks (`- [ ]`) remain in task-oriented stages.
  - Markdown local links and anchor references resolve.
  - Mermaid diagram syntax fences are closed.

```bash
# Use the stage IDs returned by `cabbage next`, not artifact filenames.
cabbage verify user-oauth-login requirement
# After required dependencies and implementation work are complete:
cabbage verify user-oauth-login implementation
```

#### `cabbage validate [<change-id> | --all] [--json]`
Validate Markdown integrity, frontmatter, heading structures, and link resolution across one or all active changes.

```bash
cabbage validate user-oauth-login
cabbage validate --all
```

#### `cabbage gate <change-id> <target> [--json]`
Evaluate readiness for specific milestones in the software development lifecycle.
- **Targets**:
  - `implementation`: Requires enabled stages listed before `implementation` in the project workflow to be verified. It does not verify the implementation checklist in advance.
  - `merge`: Enforces that all active workflow stages (testing, release, documentation) are verified before merging PR.
  - `archive`: Like `merge`, requires every enabled stage to be verified. Git merge status is not checked.

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
Inspect `<base>...HEAD`, require an active changed change record for code changes, and validate changed active records, their merge gates, and configured current-document paths. It neither validates every unchanged active record nor runs a documentation build; run `validate --all` and `docs build` separately.

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
