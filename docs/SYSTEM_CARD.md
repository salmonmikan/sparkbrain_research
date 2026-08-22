# SparkBrain system card

## Intended use

Local, inspectable research on explicit belief competition, evidence provenance, revision, no-ignition, event routing, and causal intervention.

## Out of scope

Human-impact decisions, autonomous deployment, medical or safety-critical use, claims of consciousness/AGI/biological equivalence, and energy-efficiency claims.

## Components and boundary

- Dependency-free deterministic CPU reference engine.
- Optional localhost Brain Lab; no non-loopback bind, CDN, analytics, or SaaS login.
- Optional learned PyTorch and reduced snnTorch hybrid backends.
- External evaluation text remains in an explicit gitignored local cache.

## Known limitations

Most evidence is controlled synthetic. Matched C05 baselines, final C06 external execution, and C08 structural-plasticity evidence are pending in this candidate. The owner license decision blocks public release.

## Observability

Traces expose active paths, evidence IDs/sources, Coalitions, ignition, Workspace, and counters. Inspection must not mutate dynamics. Exports are local and may include sensitive user-supplied event text; users control retention and deletion.
