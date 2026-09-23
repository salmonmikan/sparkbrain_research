# FAST FORGE latest — two bounded Assembly dead ends

- schema_version: `2`
- generation_id: `FORGE-20260923T123420+0900-ASSEMBLY-COMPLETION-ORDER`
- produced_at: `2026-09-23T12:34:20+09:00`
- worker_role: `FAST_FORGE`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- overall_status: `FORGE_DEAD_END`

## Freshness / independence

Evidence Analyst R92 remains current at `a05ab3f655a23eabd84c910ba337d64a948c168a`. Stable main used for source inspection is `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`. Forge explicitly avoided canonical candidate #34 temporal-route work, candidate #35 queue-free physical-state work, H7 FORMAL/provenance/preserve work, and all protected/frozen/evidence identities.

Recent context checked: Literature `d5a2fe3fd085017a1f4e4352c3d019c57ff02647`, Methodology `269fdfc699053318f8babbea09c007cbe9932cae`, Independent Audit `6755579f5f21b19ca90788c948d8126529b648c6`, Utility `15c5b130c868f7a37ab03582ca0225f001c651f7`.

No Forge branch was required; both probes were read-only source inspection plus synthetic reproduction of the stable matching rule.

## Probe 1 — partial completion is recognition, not physical regeneration

Using the stable `pattern_similarity` rule, a full prototype `(1,2,3,4)` versus an ordered 3/4 partial `(1,3,4)` scores `0.8000`, above the `0.66` match threshold. An unordered same-set variant scores about `0.6103`, a wrong-unit partial about `0.5208`, a 2/4 partial `0.50`, and a 1/4 partial `0.325`.

Source inspection shows Assembly activation is computed downstream of the physical Field/spike dynamics. There is no feedback path from an Assembly match that generates the missing physical spikes/units.

Disposition: `FORGE_DEAD_END`. The current behavior is similarity-based recognition/classification, not recurrent physical completion or regeneration. No promotion proposed.

## Probe 2 — frozen first exemplar makes maturation order-sensitive

Stable Assembly candidates retain the first observed activation as their prototype; later observations increment the candidate but do not replace the prototype with a centroid.

For exact-timing patterns `A=(1,2,3)`, `B=(1,2,4)`, `C=(1,3,4)`, the reproduced stable scores are `A-B=0.6916666666666667`, `B-C=0.6916666666666667`, and `A-C=0.5083333333333333`. Thus `A,B,C` yields two candidates and no three-observation mature Assembly, while `B,A,C` yields one candidate that reaches three observations and matures; `C,B,A` again yields two candidates.

Disposition: `FORGE_DEAD_END`. The order effect follows directly from ordinary online threshold clustering with an immutable first exemplar. It is an implementation property, not a distinct mechanism. No promotion proposed.

## Boundaries / metrics

No Utility request. No branch mutation or merge. No PRE_FORMAL/FORMAL identity, STARTED, official scoring, protected held-out access, preserve/evidence mutation, or immutable-ref mutation occurred.

R92 FAST_FORGE cumulative metrics: runs `2`, prototypes `4`, dead ends `4`, retained interesting objects `0`, promotion proposals `0`, later admissions `0`, duplicate/rescue rejects `0`, ownership collisions `0`, ordinary-reduction rejects `4`.
