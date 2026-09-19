# EXPLORATORY / NON_EVIDENTIARY — SUB v0.5 topology config binding cycle 1

Candidate: `CAND-V05-TOPOLOGY-CONFIG-BINDING-01`
Mode: `DISCOVERY`
Exploration cycle: `1/3` (bounded to one cycle by Evidence Analyst)
Base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`

## Prospective question

Do public/configured `V05BrainConfig.width`, `height`, and `receptor_rows` values bind the actual topology constructed by `IntegratedV05Brain`, or does the explicit `layered_reservoir_topology(seed=...)` injection leave those dimension fields informational/redundant?

This is a configuration/API-semantics question only. It is not a rescue of `CAND-TOPOLOGY-FANOUT-ALIAS-01` and will not probe resonant stride-11 functional behavior.

## Fixed bounded check

Inspect current `main` constructor/callsites/docs/tests and instantiate development-only configurations with two deliberately different dimension triples:

- default declaration: `(width=8, height=8, receptor_rows=1)`
- alternate declaration: `(width=12, height=10, receptor_rows=2)`

Record, without training or retained datasets:

- accepted stored config values;
- nested v0.4 config values;
- actual field unit count;
- actual receptor count;
- actual reservoir count;
- topology/state equality where appropriate.

No production-code changes are allowed in this cycle. No repository dataset, retained confirmatory/formal TEST surface, consumed preserve, scorer, STARTED, or evidence ref may be used.

## Prospective interpretation

- If current docs/tests clearly establish intentional fixed topology independent of the dimension fields, return `REJECT/NO_ACTION` and keep a documentation/engineering note only.
- If alternate dimension values are accepted and persisted as configuration but actual integrated topology remains fixed despite the dimension-like public configuration surface, return an Architecture/engineering promotion proposal for fresh Analyst review.
- If intended semantics are genuinely ambiguous, return `HOLD`; do not tune or extend the experiment to obtain a preferred answer.
