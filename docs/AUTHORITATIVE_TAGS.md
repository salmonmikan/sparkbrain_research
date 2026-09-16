# Authoritative scientific tags

This repository uses moving `research/*` branches for active scientific development and immutable annotated Git tags for new authoritative point-in-time scientific identities when tooling permits.

## Allowed namespaces

New authoritative tags created by `.github/workflows/create-authoritative-tag.yml` must use one of:

- `freeze/*` — exact prospective source/protocol freeze identity
- `sealed/*` — sealed candidate or package identity
- `formal/*` — one-way formal execution identity when represented as a tag
- `evidence/*` — finalized immutable evidence snapshot identity

Existing legacy `freeze/*` branches are historical scientific anchors. They must not be deleted, rewritten, force-moved, or retargeted during migration. An exact-SHA tag mirror may be added later only when scientifically unambiguous and durably mapped.

## Creation contract

The authoritative-tag workflow requires:

- a namespace-qualified tag name;
- an exact 40-character target commit SHA;
- experiment/candidate identity;
- optional protocol and package identities;
- provenance text.

The workflow:

1. re-fetches repository branches and tags;
2. validates the namespace and Git ref format;
3. requires the target to resolve to an exact commit;
4. fails closed if the requested tag already exists;
5. creates an annotated tag containing target SHA, experiment/candidate identity, protocol/package identity, timestamp, provenance, and workflow-run URL;
6. pushes without `--force`;
7. re-reads the remote annotated tag and verifies that its peeled commit exactly equals the requested SHA.

An existing authoritative tag is never updated by this workflow. If metadata needs correction after creation, keep the authoritative tag unchanged and add a separate git-managed audit/provenance record.

## Scientific boundary

The workflow creates repository identity only. It does **not** decide whether an experiment is ready to freeze, execute experiments, consume one-way identities, alter protocols, score results, or reinterpret scientific evidence. Freeze timing and execution authority remain the Research Orchestrator's responsibility under the existing integrity contract.

## Protection gap

Annotated tags are immutable by convention only unless GitHub repository rules protect the namespaces. Repository rulesets should prevent update and deletion of `freeze/*`, `sealed/*`, `formal/*`, and `evidence/*` except through an explicit emergency preservation procedure.

The current workflow deliberately does not attempt to configure rulesets using `GITHUB_TOKEN`, because repository administration/ruleset permissions are separate from ordinary Actions `contents: write` permission. Until a ruleset is installed, the workflow's no-replacement/no-force behavior reduces accidental mutation but does not replace server-side tag protection.
