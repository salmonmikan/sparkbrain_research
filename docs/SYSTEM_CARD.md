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

Most evidence is controlled synthetic. C05 produced a negative reduced matched-baseline result, C06 produced a negative official zero-shot external result, and C08 produced a negative specialization result. The owner license decision is the remaining public-release gate.

## Observability

Traces expose active paths, evidence IDs/sources, Coalitions, ignition, Workspace, and counters. Inspection must not mutate dynamics. Exports are local and may include sensitive user-supplied event text; users control retention and deletion.
