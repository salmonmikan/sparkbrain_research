# Fast Forge — FLY-0 semantic-surface checkpoint binding green

generation_id: FORGE-20260929T024200+0900-FLY0-SEMANTIC-CHECKPOINT-BINDING-GREEN
produced_at: 2026-09-29T02:42:00+09:00
forge_id: FORGE-FLY0-SEMANTIC-CHECKPOINT-BINDING
status: FORGE_INTERESTING
recommended_handoff: SYSTEM_BUILD_INPUT
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
new_scientific_result: false
scientific_credit: 0

## Why now

Methodology R146 accepted the repaired four-variant FLY-0 engineering surface and identified one bounded hardening gap for a future SB003 port: bind the semantic-surface contract/version and preferably topology identity into checkpoint provenance. Theory R19 independently proposed the same semantic-surface boundary. This work is isolated Forge preparation and does not alter M1-002.

## Exact implementation

Exact source head: `f93483b927470f48a311fe9ef711ca770648da7c`.

The composed FLY-0 causal-replacement checkpoint schema is advanced to v2 and now binds:
- semantic-surface contract version `fly0-semantic-surface-v1`;
- full task-facing semantic contract plus SHA-256 fingerprint `b09d5d2f3cc88c80fa6d0e785a18e8a402b8b149d9ed1d22543028c717798063`;
- topology fingerprint for structured / rewired / random_sparse variants;
- deterministic randomization seed for rewired (2801) and random_sparse (2802);
- replacement variant and controller identities;
- Observation / ascending-feedback cut settings;
- feedback-delay and event-budget settings;
- snapshot token.

Restore fails closed on semantic-contract, semantic-fingerprint, topology-fingerprint, randomization-seed, variant, controller, cut or budget mismatch.

The report now exposes the semantic contract/fingerprint and per-variant topology fingerprints. Reactive remains the ordinary non-topological replacement and therefore has no topology fingerprint.

## Verification

Exact-head CI run `36459501642` completed successfully on Python 3.11 and Python 3.13. Lint, local readiness, tests and bundle validation all passed.

The new tests explicitly tamper with semantic-surface contract and topology fingerprint and verify restore rejection. Existing four-way intact progression, exact replay, Observation cut and ascending-feedback cut tests remain green.

## Interpretation

This closes the specific Forge-level checkpoint/provenance hardening requested by Methodology R146 for the composed FLY-0 path. It does not allocate SB003; durable Evidence Analyst authority remains R168 and SB003 remains unallocated.

Strict reactive-vs-topology native activity/resource commensurability remains open and claim-typed. It is not required for ordinary NON_EVIDENTIARY SYSTEM_BUILD reuse, but strong efficiency or topology-superiority claims remain unsupported.

The result does not establish biological fidelity/equivalence, topology necessity/superiority, compute or energy efficiency, composition contribution, whole-system superiority, external validity or scientific novelty.

## Collision / authority

- Human Directive index identity unchanged: head recorded by durable authority `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, active-index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`.
- Durable Analyst: R168 at `266864682894af7745156ec899da3377cacc18fb`; SB003 unallocated.
- Durable Control append-only authority: R116 at branch head `5507f1d8588f112cad720c1d638e8675c8e8fac8`.
- MAIN: R181 / M1-002 exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e`; Relay unallocated; no collision.
- Methodology: R146 at `366c1d692ca74e01616d5957b489d852f795e144`.
- External Science: Theory R19 / Literature R48 branch head `2227cad77817a62a6e5fe624f5772b05b1c5572b`.

P0 `INC-GITHUB-MUTATION-RECURRENCE-20260928-001` remains OPEN. The source publication for this generation succeeded on the first bounded publication attempt.
