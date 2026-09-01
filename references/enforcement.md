# Enforcement and tamper resistance

CLI checks are only authoritative if the repository protects the checks themselves.

Recommended repository policy:

1. Make the GitHub Actions `cabbage` job a required status check for the protected branch.
2. Require pull requests; disallow direct pushes to the protected branch.
3. Require human review for changes to:
   - `.cabbage/config.yaml`
   - `.cabbage/workflows/**`
   - `.cabbage/tooling/**`
   - `.github/workflows/cabbage.yml`
4. Use CODEOWNERS or equivalent repository rules for those paths.
5. Treat changes to workflow schemas or the vendored CLI as policy changes, not ordinary feature changes.
6. Do not let an Agent disable, bypass, or rewrite the required CI gate as part of a feature PR.

Without branch protection, any repository-local guard can be modified by an actor that already has unrestricted write access.
