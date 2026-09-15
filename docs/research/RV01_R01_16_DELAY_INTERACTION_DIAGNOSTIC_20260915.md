# RV01 R01-16 post-hoc delay interaction diagnostic — 2026-09-15

## Scope

This note records a **post-hoc mechanistic diagnostic derived only from already-consumed, immutable R01-16 exposed-development capability evidence**. It does not rerun R01-16, create a new experiment identity, modify a frozen protocol, open a held-out result, or grant confirmatory/formal authority.

The diagnostic is intended to sharpen the next **distinct exploratory/development successor**. It must not be used to retune or rerun the consumed R01-16 capability identity.

## Bound evidence

- Authoritative RV01 source commit: `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99`
- Capability identity: `rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af`
- Capability preserve ref: `preserve/rv01-r01-16-capability-20260915`
- Preserve commit inspected: `0a25eac227d7ac0e8dbd5532d450ed2d50efa105`
- Capability result: `artifacts/rv01/r01-16/capability/rv01-r01-16-capability-02b3d80744d0eb10-65ebe33d70af/capability_result.json`
- Preserved raw artifact SHA-256: `e3b6e8c7ed6db423919c4360a5291ac207544566beb4656954be344cb253f335`
- Capability suite hash (immutable result provenance): `b1b4d555d30630d1051482563696981261619143099216ab893bbea481d69392d`
- Capability source/package manifest SHA-256: `bc36c7da23f4d6b8fa1ee7d4d8c7bacdfd5970818482e146a188837247332582`
- Retained history registry SHA-256: `232f4fb23b74662d10adca2990e1b030bbb1c74e45fb67f607982738570795bd`

## Factor-arm semantics

The frozen `R01_16FactorizationConstruction.arm_inventory()` defines the four arms from the same trained checkpoint as follows:

| Arm | Weight state | Delay state |
| --- | --- | --- |
| `F0` | learned/post-training | learned/post-training |
| `FW` | reset/pre-training | learned/post-training |
| `FD` | learned/post-training | reset/pre-training |
| `FWD` | reset/pre-training | reset/pre-training |

Therefore:

- `F0_vs_FW_different` asks whether resetting learned **weight** changes behavior while learned delay remains present.
- `FD_vs_FWD_different` asks whether resetting learned **weight** changes behavior after delay is already reset.
- `F0_vs_FD_different` asks whether resetting learned **delay** changes behavior while learned weight remains present.
- `FW_vs_FWD_different` asks whether resetting learned **delay** changes behavior after weight is already reset.

The preregistered delay classifier requires both delay contrasts to move together for support; one true and one false is `DELAY_DISCORDANT`.

## Preserved contrast counts

Across the 100 eligible development probe cells, the immutable capability result records:

| Contrast | Different cells |
| --- | ---: |
| `F0_vs_FW_different` | 100 / 100 |
| `FD_vs_FWD_different` | 100 / 100 |
| `F0_vs_FD_different` | 46 / 100 |
| `FW_vs_FWD_different` | 0 / 100 |
| `F0_vs_FWD_different` | 100 / 100 |

The frozen aggregate classifications are unchanged:

- Weight: `WEIGHT_SUPPORTED` — 100 support / 0 negative / 0 discordant.
- Delay: `DELAY_MIXED` — 0 support / 54 negative / 46 discordant.
- Combined: `COMBINED_SUPPORTED` — 100 support / 0 negative.

Because `F0_vs_FD_different = 46` and `FW_vs_FWD_different = 0`, all 46 delay-discordant cells have the same directional structure: **resetting delay changes the behavioral signature when learned weight is present, while resetting delay has no detectable effect after learned weight has been reset**.

Equivalently, among cells where the retained learned-delay state is behaviorally visible under learned weight, the observed delay contribution survives weight reset in `0 / 46` cells.

Derived post-hoc diagnostic:

- delay-visible with learned weight retained: **46 / 100**
- incremental delay-visible after weight reset: **0 / 100**
- survival of the visible delay contribution after weight reset: **0 / 46 = 0%**
- loss of that visible delay contribution after weight reset: **46 / 46 = 100%**

At the same time, the weight contrasts are different in **100 / 100** cells both with learned delay retained and with delay reset (`F0_vs_FW = 100`, `FD_vs_FWD = 100`).

## Interpretation

The strongest evidence-consistent interpretation is an **asymmetric, weight-conditioned expression of the learned-delay contribution at the frozen behavioral endpoint**:

1. the learned-weight state is behaviorally consequential throughout the complete eligible development grid;
2. the learned-delay state is behaviorally consequential in a substantial subset (46/100) when learned weight is retained;
3. the learned-delay contrast becomes behaviorally invisible in every cell once learned weight is reset;
4. resetting both factors remains different from the fully learned state in all 100 cells, consistent with the robust learned-weight contribution.

This is more informative than the aggregate label `DELAY_MIXED`: the mixed result is not an arbitrary balance of opposite discordances. The observed discordance is one-sided and points to a conditional interaction at the measured behavioral signature.

### What this does **not** establish

This post-hoc diagnostic does **not** prove that weight biophysically suppresses, causes, or directly gates delay plasticity. The factorization manipulates expression-time connection states and observes a behavioral signature; multiple downstream nonlinearities could produce the same conditional pattern. It also does not turn R01-16 into a confirmatory result. All R01-16 capability outputs remain exposed-development evidence.

## Highest-information successor question

A distinct prospective successor should discriminate between at least these mechanisms on **fresh identities/worlds/seeds**:

1. **weight-conditioned delay expression:** learned-delay effects require the learned-weight state to influence propagation;
2. **decision-boundary convergence:** delay still changes latent timing/trajectory after weight reset, but the frozen R01-16 behavioral signature cannot see it;
3. **route-level interaction:** delay changes which route wins only when weight differences create sufficient competition, rather than acting as an independent propagation factor.

The successor should therefore preregister both the existing route/behavior signature and an orthogonal timing/trajectory-sensitive endpoint before execution. It must use a new exploratory/development identity; the consumed R01-16 construction/capability identities may not be rerun or retuned.

## Integrity status

- New experiment execution: **none**
- New one-way identity consumed: **none**
- Frozen/preserved evidence modified: **none**
- Held-out/formal evidence opened: **none**
- Classification: **post-hoc diagnostic derived from immutable development evidence**
