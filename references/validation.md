# Document & Workflow Validation Checklist

This checklist outlines the automated checks and manual validation criteria enforced by Cabbage.

---

## 1. Automated Validation Pipeline

When `cabbage verify <change> <stage>` or `cabbage validate` runs, the CLI enforces:

### Structural & Frontmatter Integrity
- [x] Frontmatter contains correct `change` and `stage` identifiers.
- [x] All mandatory headings defined in the workflow template exist in the file.
- [x] File is valid UTF-8 encoded Markdown.

### Content Completeness & Quality
- [x] **Zero Placeholders**: No residual `TODO`, `TBD`, `FIXME`, or default scaffold prompts.
- [x] **Completed Tasks**: In task-oriented stages (`tasks.md`), all checklist items must be checked (`- [x]`). Unchecked items (`- [ ]`) strictly fail verification.
- [x] **Diagram Syntax**: All ```mermaid fences are properly closed and valid.

### Link & Reference Integrity
- [x] Local file links resolve to real paths in the repository.
- [x] Anchor tags (`#heading-slug`) correspond to valid section titles.

### Cryptographic Signatures
- [x] Upstream dependencies are verified (`done`).
- [x] Stage signature (SHA-256) matches current artifact and dependency content.

---

## 2. CI & Git Diff Binding (`cabbage ci`)

In CI environments, `cabbage ci --base <ref>` enforces:

1. **Change Workspace Binding**: If code files under source directories are modified in a PR, a valid matching Cabbage change workspace must exist and pass verification.
2. **Clean VitePress Build**: `cabbage docs build` must compile without errors or dead links.
3. **No Stale Stages**: All required workflow stages for active changes must be in `done` state.

---

## 3. Manual Peer-Review Checklist

During code and documentation review in PRs:

- [ ] Does the PRD accurately capture customer/business intent?
- [ ] Are architectural decisions backed by an ADR with positive/negative consequences?
- [ ] Are API endpoints and database schema migrations complete and backwards-compatible?
- [ ] Are failure modes, observability, and rollback plans actionable?
- [ ] Are existing canonical docs updated in-place rather than cloned?
