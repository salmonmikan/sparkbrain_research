# SparkBrain Fast Forge — scope allocator component-replacement probe

- schema_version: 2
- generation_id: `FORGE-20260927T223910+0900-SCOPE-ALLOCATOR-COMPONENT-REPLACEMENT-CI-CLEAN`
- produced_at: `2026-09-27T22:39:10+09:00`
- forge_id: `FORGE-SCOPE-ALLOCATOR-COMPONENT-REPLACEMENT-A`
- status: `FORGE_INTERESTING`
- recommended_handoff: `SYSTEM_BUILD_INPUT`
- branch: `forge/20260927-scope-allocator-component-replacement-a`
- exact_prototype_head: `e74940775ef6b098abfbc1a80e96a558bc2d5474`
- ci_run: `36319888813`
- ci_result: `SUCCESS`
- evidentiary_status: `NON_EVIDENTIARY_NONCANONICAL_FORGE`
- scientific_credit: 0
- new_scientific_result: false

The fixed-radius nearest-centroid allocator was replaced, on the same bounded scope-to-revision fixture, with a standard observation-only two-component Gaussian-mixture reference allocator. On the prior within-reuse-radius collision, the batch reference formed two components, routed the A and B queries to separate scope-local revision accumulators, recovered A/B, and rejected the exact midpoint at posterior mass 0.5. With identical observations carrying conflicting labels, the model declared the two-component surface unidentifiable, committed no evidence and abstained.

The result localizes the previous failure to the fixed-radius router on this synthetic fixture. It also confirms Theory R11's boundary: when observation vectors are identical, downstream revision cannot reconstruct a distinction that routing did not represent.

Local validation passed the focused five-file chain 36/36, all Forge tests 120/120, Ruff, compileall, readiness and bundle validation. Exact prototype head `e74940775ef6b098abfbc1a80e96a558bc2d5474` passed GitHub CI run `36319888813` on Python 3.11 and 3.13, including lint, readiness, full tests and bundle validation.

This reduces to batch two-component Gaussian-mixture clustering with posterior rejection plus per-key evidence accumulation. It fixes component count at two and uses the complete stream before routing, so it has model-cardinality and future-context advantages over the online fixed-radius arm. It is not a fair system comparator and does not establish learned latent organization, general robustness, composition contribution, comparative superiority or scientific novelty.

RD006 v4 and its exposed result, SB001, MAIN/Relay ownership and all scientific refs remain untouched. The handoff is optional future SYSTEM_BUILD input only.

History: `reports/fast_forge/history/2026-09-27/2239-scope-allocator-component-replacement-ci-clean.md`
