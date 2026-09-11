# RV02-RD004 relative-probe-clock hidden-eligibility preregistration

Date: 2026-09-11  
Status: **PREREGISTERED_DEVELOPMENT_ONLY / IMPLEMENTATION_NOT_STARTED**

## Why a new identity is required

The frozen first execution of `rv02-rd003-online-hidden-eligibility-v1` is preserved as attempt 001 and is consumed. It produced 0/18 complete cells. Fifteen cells reached the probe stage and failed because the inherited RD002 helper scheduled its cue at absolute `100 ms` after online training had already advanced the Field clock beyond that timestamp. All three opposing-reversal cells instead hit the preregistered native `max_events_per_run` guard during training.

No E0/E1/ES cell produced a complete probe set and no selective-organization score is scientifically available from RD003 attempt 001. The failure is not repaired or rerun under the RD003 identity.

RD004 is a new development diagnostic that changes only the **probe temporal anchor and failure accounting needed to make the preregistered probe executable after online training**. It does not tune the mechanism from observed behavioral outcomes.

## Inherited mechanism — unchanged

RD004 inherits the RD003 mechanism and scientific parameters without modification:

- same exposed RV02 development worlds;
- same scales `1, 3, 10`;
- same visible-to-hidden boundary gain `4.0`;
- same Field threshold and dynamics;
- same `DirectFieldPlasticityConfig` constants;
- same E0 / E1 / ES arms;
- same external-gated hidden-return rule;
- same deterministic, outcome-independent shuffled hidden-source assignment;
- same no-reward/no-correct-action/no-route-label/no-task-score learner boundary;
- same 40-ms probe horizon;
- same continuation metrics and paired hidden-boundary-cut logic;
- same native event/spike/resource limits.

RD004 must **not** raise the native limits to rescue opposing-reversal or any other cell. A native-guard failure is retained as an incomplete cell.

## Fixed training procedure

The online E0/E1/ES training procedure is inherited from RD003. Every external route event remains the authoritative teaching observation. Runtime hidden activity may create transient local eligibility only in E1/ES, and only a later external observation may commit a physical update.

E1 and ES must consume the same hidden eligibility-event count, timestamps, magnitudes and observed hidden-unit identities. ES may differ only in the deterministic assigned hidden source according to the preregistered permutation. Each arm's actual runtime hidden spikes remain retained separately.

## Corrected probe clock contract

RD002's absolute cue timestamp is not reused. For every arm and route probe, the probe is constructed as follows.

1. **Training-tail completion** — after the final external training observation, advance the trained Field through the already inherited eligibility lifetime (`maximum_lag_ms`, currently 6.5 ms). No new external teaching observation is added.
2. **Fixed washout** — from that completed training-tail state, advance the unmodified Field by exactly **100.0 ms** with no external input and no learning. This relative 100-ms interval is the prospective analogue of RD002's absolute `100 ms` cue anchor and is fixed before RD004 implementation/execution.
3. If the training-tail or washout hits a native event/spike guard, the cell is incomplete. Limits are not changed.
4. **Shared pre-probe snapshot** — after washout, capture one exact state snapshot. Natural and hidden-boundary-cut probe arms are cloned from this same snapshot.
5. **Boundary intervention timing** — only after the shared snapshot, the cut arm zeros crossing hidden/visible boundary edges. The natural arm is unchanged.
6. **Cue anchor** — schedule the external probe cue at exactly the shared snapshot's current Field clock. Scheduling in the past is forbidden.
7. **Probe horizon** — run exactly 40.0 ms after that cue.
8. **Probe scoring window** — only spikes emitted strictly after the cue anchor are supplied to continuation scoring. Washout activity is never counted as probe behavior. Hidden units remain non-symbolic.
9. Probe execution must not modify connection state. Natural and cut probes must retain the same observer/reference noninterference checks used by RD002/RD003.

The 100-ms washout is fixed for all families, scales and arms. It may not be shortened or lengthened after seeing RD004 results.

## Cell statuses and matrix accounting

All 18 family/scale cells must be attempted exactly once under the frozen RD004 development source. Each cell must end in one of these fail-closed classes:

- `complete` — all E0/E1/ES natural and cut probes completed and are independently reconstructable;
- `incomplete_native_guard_training` — a native event/spike/resource guard was reached during online training;
- `incomplete_native_guard_washout` — a guard was reached during the fixed 100-ms no-input washout;
- `incomplete_native_guard_probe` — a guard was reached during a 40-ms probe;
- `incomplete_integrity_failure` — retained evidence cannot reconstruct the fixed schedule, eligibility budget, update locus, probe score or state identities;
- `incomplete_execution_failure` — any other execution exception.

Incomplete cells remain part of the preserved raw matrix but cannot contribute scientific metrics. A failure in one cell must not cause the runner to silently omit later planned cells.

RD004 does not require all 18 cells to be scientifically complete in order to preserve the diagnostic. Any interpretation is strictly scoped to individually complete family/scale cells. No global RV02 utility claim may be made from a matrix with incomplete families.

## Scientific readout — unchanged in substance

For any complete family/scale cell, a useful selective-organization signal requires the preregistered conjunction:

1. E1 improves strict exact-route recovery or reduces off-route contamination relative to both E0 and ES without reducing ordered retention;
2. the relevant improving probe contains retained hidden eligibility activity;
3. the paired hidden-boundary cut removes or reverses the relevant visible behavioral improvement;
4. ES fails to reproduce the same improvement despite its matched eligibility-event budget.

If E1 and ES are equivalent, causal hidden assignment is not supported. More hidden activity or subthreshold state change alone is not a useful result. No average may compensate for a required per-probe regression.

## Prohibited RD004 adaptations

After the first RD004 execution begins, do not under the same identity:

- change gain, thresholds, Field dynamics or plasticity rates;
- change the 100-ms washout or 40-ms probe horizon;
- increase event/spike/resource limits;
- change E1/ES budget matching or permutation construction;
- add reward, correctness or task outcome information;
- change family/scale inclusion;
- redefine continuation scoring;
- reinterpret an incomplete native-guard cell as a negative behavioral score.

Any such change requires another diagnostic identity.

## Execution boundary

RD004 is development-only. Before execution:

- implementation and unit tests must match this document;
- the complete runner and offline verifier must pass repository CI;
- an exact development source SHA must be frozen on a new immutable `freeze/*` ref;
- execution must use that exact SHA and preserve raw evidence even on failure.

No held-out or formal capability is authorized by RD004.
