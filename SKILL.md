---
name: project-docs-management
description: Enforce project documentation lifecycle, change workflows, architecture decisions, validation, VuePress preview, Mermaid diagrams, and CI gates using cabbage.
---

# Cabbage Skill

## When to use

Use this Skill whenever work changes product behavior, architecture, APIs, database schema, security boundaries, deployment, operations, tests, or production behavior.

## Mandatory operating rule

Before implementation work:

```bash
cabbage status <change> --json
cabbage next <change> --json
cabbage gate <change> implementation
```

If the gate fails, do not begin implementation. Create or update the required artifact, validate it, then run `cabbage verify`.

Before merge:

```bash
cabbage validate <change>
cabbage sync <change>
cabbage gate <change> merge
cabbage docs build
```

CI should run:

```bash
cabbage ci --base <merge-base>
```

## Change types

- `feature`: user-visible or business capability
- `architecture`: system boundary, topology, runtime, storage, major dependency or communication model change
- `bugfix`: non-incident defect correction
- `hotfix`: urgent production correction
- `refactor`: internal structural change without intended product behavior change
- `migration`: database, data, platform or runtime migration
- `integration`: third-party/API/platform integration
- `incident`: production incident and corrective work

## Documentation model

Current-state documents describe the system as it exists now. Update them in place. Git stores fine-grained history.

Decision-history documents (`RFC`, `ADR`, postmortems) are immutable historical records. Supersede them; do not rewrite the decision history.

Avoid `final-v2-final.md`. Use stable paths and Git history.

## Change impact rule

Every change must explicitly evaluate:

- product / PRD
- architecture
- API
- database
- security
- testing
- deployment
- operations
- data
- performance

Use:

```bash
cabbage impact <change>
cabbage impact <change> --set architecture=true --set api=true
```

Changing impact synchronizes `impact.md`; that makes dependent completed stages stale, while conditional stages are activated or skipped from the new impact flags.

## Anti-rot rules

1. One source of truth per fact; other docs link to it.
2. API/schema/config/version information should be generated where possible.
3. Code and affected docs belong in the same PR.
4. Verifying an artifact records its content/dependency signature.
5. Editing an upstream artifact makes dependent completed artifacts stale.
6. Architecture decisions use ADR; proposals use RFC/tech-spec.
7. Obsolete current-state docs are updated or removed; historical decisions are superseded/archived.
8. Module ownership includes documentation ownership.
9. CI validates links, frontmatter, required headings, Mermaid fence integrity, workflow state, and docs build.
10. `cabbage sync` and `cabbage archive` automatically propagate verified change specs into `docs/` current-state documentation.
11. A code-changing PR without a bound change fails `cabbage ci` when strict mode is enabled.

## Mermaid

Prefer Mermaid for diagrams that should be reviewed with code:

- `flowchart` for flows
- `sequenceDiagram` for call chains
- `stateDiagram-v2` for state machines
- `classDiagram` for domain structure
- `erDiagram` for data relationships
- `gitGraph` for release/branch flows

Keep the Mermaid source in Markdown. Do not commit PNG screenshots as the primary architecture source when Mermaid is sufficient.

## VitePress

`cabbage init` scaffolds a standalone `docs/` VitePress site with Mermaid support.

```bash
cabbage docs install
cabbage docs dev
cabbage docs build
```

## Document placement

Read `references/directory-structure.md` and `references/document-types.md` before creating a new long-lived document.

## Adopting an existing project

If the project already has documentation outside the standard tree, read `references/adoption.md` and run `cabbage adopt` first. The command inventories existing documents and proposes actions (`keep`/`migrate`/`import`/`review`) without moving anything; complete the adoption as a change record before starting feature work.

## Workflow selection

Read `references/decision-tree.md`. Do not create every document for every change; activate conditional artifacts from impact analysis.

## Verification semantics

`cabbage verify <change> <stage>` succeeds only if:

- dependencies are complete and current;
- artifact exists;
- frontmatter identifies the correct change and stage;
- required headings exist;
- no `TODO`, `TBD`, `FIXME`, or `CABBAGE` placeholder prompts remain;
- local Markdown links resolve;
- Mermaid fences are balanced;
- implementation task lists contain no unchecked tasks when verifying implementation.

Never manually mark `.cabbage/changes/*/state.json` as complete. Treat it as CLI-owned metadata.

## Enforcement

Read `references/enforcement.md`. Repository branch protection and human review of policy files are required if the Agent has write access to the repository.
