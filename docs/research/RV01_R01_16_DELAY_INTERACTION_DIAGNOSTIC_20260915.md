# RV01 R01-16 post-hoc delay measurement-validity diagnostic — 2026-09-15

## Scope

This note records a **post-hoc mechanistic and measurement-validity diagnostic derived only from already-consumed, immutable R01-16 exposed-development capability evidence**. It does not rerun R01-16, create a new experiment identity, modify a frozen protocol, open a held-out result, or grant confirmatory/formal authority.

The diagnostic is intended to constrain the next **distinct exploratory/development successor**. It must not be used to retune or rerun the consumed R01-16 capability identity.

## Bound evidence

- Authoritative RV01 source commit: `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- Capability identity: `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af`
- Capability preserve ref: `preserve/rv01-r01-16-capability-20260915`
- Preserve commit inspected: `0a25eac227d7ac0e8dbd5532d450ed2d50efa105`
- Capability result: `artifacts/rv01/r01-16/capability/rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af/capability_result.json`
- Preserved raw artifact SHA-256: `e3b6e8c7ed6db423919c4360a5291ac207544566beb4656954be344cb253f335`
- Capability suite hash from immutable `COMPLETE.json`: `c5c5e32160b634680ff5cad726365c38ec3d06c266cc453fcf349d604ee48ffc`
- Capability source/package manifest SHA-256: `bc36c7da23f4d6b8fa1ee7d4d8c7bacdfd5970818482e146a188837247332582`
- Retained history registry SHA-256: `232f4fb23b74662d10adca2990e1b030bbb1c74e45fb67f607982738570795bd`

## Frozen factor-arm semantics and historical classifications

The frozen `R01_16FactorizationConstruction.arm_inventory()` defines the four arms from the same trained checkpoint as follows:

| Arm | Weight state | Delay state |
| --- | --- | --- |
| `F0` | learned/post-training | learned/post-training |
| `FW` | reset/pre-training | learned/post-training |
| `FD` | learned/post-training | reset/pre-training |
| `FWD` | reset/pre-training | reset/pre-training |

Across the 100 eligible development probe cells, the immutable capability result records:

| Contrast | Different cells |
| --- | ---: |
| `F0_vs_FW_different` | 100 / 100 |
| `FD_vs_FWD_different` | 100 / 100 |
| `F0_vs_FD_different` | 46 / 100 |
| `FW_vs_FWD_different` | 0 / 100 |
| `F0_vs_FWD_different` | 100 / 100 |

The frozen aggregate classifications remain historical facts and are **not rescored here**:

- Weight: `WEIGHT_SUPPORTED` — 100 support / 0 negative / 0 discordant.
- Delay: `DELAY_MIXED` — 0 support / 54 negative / 46 discordant.
- Combined: `COMBINED_SUPPORTED` — 100 support / 0 negative.

## Post-hoc measurement-validity audit

The historical `DELAY_MIXED` label does not by itself establish a meaningful learned-delay intervention. Inspection of the authoritative R01-16 source and preserved capability evidence exposes a stronger limitation:

1. the constructed physical connection delay is initialized from the same `world.lag_ms` used to space the pretraining pulses;
2. the pair-arrival plasticity rule moves delay only toward the observed pre/post lag when that lag differs from the current connection delay;
3. therefore the intended training schedule supplies essentially **zero nontrivial delay-learning error** in R01-16;
4. the R01-16 capability diagnostics mark a delay edge as changed with exact floating-point inequality (`post_delay != pre_delay`) rather than a scientifically meaningful tolerance.

A post-hoc scan of the preserved capability artifact found realized pre/post delay movement only at floating-point roundoff scale: maximum absolute movement about `1.03e-11 ms`, mean about `1.32e-12 ms`, and median about `6.95e-13 ms`. By contrast, learned weight changes are macroscopic relative to the `0.05` starting weight.

The 46 `F0_vs_FD` behavioral differences therefore must **not** be interpreted as evidence that a substantively learned delay contribution is expressed only when learned weight is retained. The safer interpretation is that those cells expose sensitivity of the frozen behavioral signature to microscopic timestamp/tie-order perturbations (or another downstream numerical/event-order effect) while the weight intervention remains genuinely large. The immutable historical classification stays `DELAY_MIXED`; its mechanistic meaning is narrowed by this diagnostic rather than rewritten.

## Current evidence-consistent interpretation

1. **Weight contribution:** development evidence remains strong. Resetting learned weight changes the behavioral signature in `100 / 100` eligible cells under either delay state.
2. **Delay contribution:** **unresolved by R01-16**. The experiment did not create a scientifically meaningful nonzero learned-delay displacement, so the 46/100 discordant cells cannot support a learned-delay mechanism.
3. **Combined classification:** historically `COMBINED_SUPPORTED`, but the interpretable support is dominated by the robust weight intervention; R01-16 does not independently validate a substantive delay-learning contribution.
4. **No causal gating claim:** the earlier phrase “weight-conditioned delay expression” is too strong for these data and is withdrawn as a scientific interpretation of R01-16.

This is a negative measurement-validity finding about the delay component, not a reason to edit, rerun, or silently repair the consumed R01-16 identity.

## Highest-information successor question

A distinct prospective successor should test a **real, preregistered nonzero delay-learning signal** on fresh identities/worlds/seeds. Before execution it should bind at least:

1. an initial physical connection delay intentionally separated from the training/observed lag by a meaningful margin;
2. a preregistered minimum realized delay-change magnitude for delay eligibility, with tolerance-aware comparisons rather than exact float inequality;
3. the existing route/behavior endpoint plus an orthogonal timing/trajectory-sensitive endpoint capable of distinguishing latent propagation changes from decision-boundary/tie-order changes;
4. fresh source/package/input identity and no reuse of the consumed R01-16 construction/capability identity.

A useful successor can then discriminate genuine learned-delay effects from weight-dominated behavior and numerical event-order sensitivity. It must be labeled **exploratory/development**, not confirmatory, because its design is informed by the exposed R01-16 result and this post-hoc audit.

## Integrity status

- New experiment execution: **none**
- New one-way identity consumed: **none**
- Frozen/preserved evidence modified: **none**
- Held-out/formal evidence opened: **none**
- Historical frozen classifications changed: **none**
- Classification of this note: **post-hoc development diagnostic / delay measurement-validity negative finding**
