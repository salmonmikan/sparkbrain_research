# Utility Result — CTRL-20260919-2250-TOPK-CROSS-SEED-SUPPORT

- status: `COMPLETED`
- assignment_id: `CTRL-20260919-2250-TOPK-CROSS-SEED-SUPPORT`
- source_request: `EVA-20260919-1943-TOPK-CROSS-SEED-SUPPORT`
- target: `CAND-TOPK-PA-01` completed Architecture Study cycles 1 and 2
- mode: `READ_ONLY_ARCHITECTURE_CROSS_SEED_SUPPORT`
- evidentiary_status: `NON_EVIDENTIARY_METHODOLOGY_ARCHITECTURE_DIAGNOSTIC`
- diagnostic_classification: `MIXED`
- recommendation: `ADD_MORE_ARCHITECTURE_SUPPORT`
- run_count: `1 / 1`

## Executive conclusion

The replicated local signal is **real at the descriptive Architecture level but narrow**. Both independent DEV seeds retain the existing local `PERSISTENCE_COUPLED_DELAYED_AMPLIFICATION_SIGNAL` label because the `magnitude=0.10` turnover stratum independently clears the existing support and ratio gates in both cycles. Leave-one-seed stability is therefore positive.

However, the signal is not broadly support-robust across magnitudes or episode composition. Lower-magnitude strata are sparse or unsupported, the `0.10` result is necessary for the local label, and turnover support is episode-clustered — especially in seed 42. This is enough to keep the line scientifically interesting, but **not enough to jump to PRE_FORMAL planning from this diagnostic alone**. The next useful step, if Evidence Analyst elects to continue, should be a **fresh prospective Architecture object aimed at the ordinary reduction question** (hard switching / branch-basin selection / recurrent hysteresis), not a Top-k cycle-3 rescue or repetition.

## Provenance / exact inputs

No scientific workflow was rerun. Only the two already-produced DEV artifacts were read.

| Cycle | Workflow | Producing head | Artifact | SHA-256 digest |
|---|---:|---|---|---|
| 1 | `35432088902` | `97f542d86dcd3a609cd039379fcda41ba61e0909` | `topk-persistent-amplification-cycle1` | `62ee402e9e7c5a1cd41e65eebcbbe183d2be0625e4e66c2157ae207317f93f83` |
| 2 | `35435714352` | `04ced2b97ed088bb2cdb086d164a86212741e601` | `topk-persistent-amplification-cycle2` | `31820e1be709068e51aac00d9df17aa1df642b9a58245d44800065a1dd409500` |

Current `main` observed during this run: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`.

The moving research branch is no longer present in the current branch search, so the workflow producing heads above are used as the exact immutable analysis anchors for the already-produced artifacts. The artifacts themselves remain available and their GitHub digests match the downloaded bytes used here.

## Contract note

The existing artifacts do **not** contain a literal `no-top-k` arm. The paired conditions are `full` and `no_persistent_state`; the selected-set turnover indicator is identical across each pair. Therefore this diagnostic can assess support robustness of the existing persistent-top-K Architecture contrast, but it cannot make a new direct `top-k vs no-top-k` claim.

## Per-seed / per-magnitude support inventory

Existing descriptive signal thresholds were read only, not changed: probability AUC ratio `>=1.5`, state AUC ratio `>=2.0`, turnover support `>=20`.

| Seed | Magnitude | Turnover pairs | Supported episodes | Median probability ratio | Median state ratio | Existing local gate |
|---:|---:|---:|---:|---:|---:|---|
| 41 | 0.01 | 1 | 1 | 35.504 | 2.030 | under-supported |
| 41 | 0.05 | 11 | 4 | 10.126 | 1.465 | under-supported + state threshold not met |
| 41 | 0.10 | 25 | 9 | 7.819 | 2.033 | **passes** |
| 42 | 0.01 | 0 | 0 | n/a | n/a | no support / not assessable |
| 42 | 0.05 | 2 | 1 | 21.732 | 4.288 | under-supported |
| 42 | 0.10 | 26 | 5 | 15.392 | 4.421 | **passes** |

All turnover cases that exist have probability-ratio and state-ratio sign `>1`; the problem in the lower strata is primarily **support**, plus the seed-41 `0.05` aggregate state ratio not reaching the pre-existing 2.0 signal threshold.

### Lack of signal vs lack of support

- `0.10`: **replicated supported signal** under the current descriptive Architecture contract — 25 and 26 turnover pairs in the two seeds, with both ratio thresholds met.
- `0.05`: **not a clean lack-of-signal result**. Probability amplification is directionally strong in both seeds, but seed 42 has only `n=2`; seed 41 has `n=11` and its median state ratio is only `1.465`. This stratum is under-supported / mixed, not a negative result.
- `0.01`: **lack of support, not lack of signal**. Seed 41 has one turnover pair and seed 42 has none, so cross-seed signal cannot be assessed.

## Cross-seed agreement

### Leave-one-seed

The existing local signal survives either seed by itself because each seed independently has a supported `0.10` stratum:

- seed 41 alone: `n=25`, probability ratio `7.819`, state ratio `2.033` -> passes;
- seed 42 alone: `n=26`, probability ratio `15.392`, state ratio `4.421` -> passes.

Result: **leave-one-seed stable**.

### Leave-one-magnitude stratum

- remove `0.01`: signal retained via `0.10`;
- remove `0.05`: signal retained via `0.10`;
- remove `0.10`: signal is lost in both seeds.

Result: the replicated label is **high-magnitude-stratum dependent**. This is not a contradiction, but it prevents interpreting the current result as broad magnitude-general persistence amplification.

## Prospective support-threshold sensitivity (descriptive only)

The predeclared diagnostic family `n>=3`, `n>=5`, `n>=10` was applied without changing the canonical rule or selecting a replacement threshold.

For a magnitude to survive cross-seed support sensitivity here, each seed must independently meet the support threshold and the existing ratio thresholds.

| Magnitude | n>=3 | n>=5 | n>=10 | existing n>=20 |
|---:|---|---|---|---|
| 0.01 | fails | fails | fails | fails |
| 0.05 | fails | fails | fails | fails |
| 0.10 | **survives both seeds** | **survives both seeds** | **survives both seeds** | **survives both seeds** |

Thus the high-magnitude signal is not an artifact of choosing `n>=20`; it survives all of the predeclared lower support cutoffs. The breadth problem is instead that only `0.10` has replicated support.

## Episode-cluster robustness

The pair counts are not independent episode counts, so cluster concentration matters.

### Seed 41 / magnitude 0.10

- 25 turnover pairs across 9 episodes;
- largest episode contributes 7 pairs; largest two contribute 13/25;
- episode-balanced median probability ratio: `8.361`;
- episode-balanced median state ratio: `3.466`;
- 5/9 supported episodes individually clear both ratio thresholds;
- deterministic leave-one-episode recomputation retains the local signal in `10/12` episode removals.
- the two failures occur because removing a high-support episode reduces turnover support below 20 (to 19 or 18); one also moves the state median below 2.0.

### Seed 42 / magnitude 0.10

- 26 turnover pairs across only 5 episodes;
- largest episode contributes 10 pairs; largest two contribute 18/26;
- episode-balanced median probability ratio: `5.385`;
- episode-balanced median state ratio: `5.570`;
- 5/5 supported episodes individually clear both ratio thresholds;
- deterministic leave-one-episode recomputation retains the local signal in `10/12` episode removals.
- the two failures are driven by removal of the two large support clusters, reducing turnover support to 16 or 18.

This is **positive directional cluster evidence but material support concentration**. The seed-42 pair count of 26 corresponds to only 5 independent supported episodes.

## Episode/world composition difference

At `magnitude=0.10`:

- seed 41 support: 8 goal-conflict pairs across 3 episodes + 17 multi-object pairs across 6 episodes;
- seed 42 support: all 26 turnover pairs are from goal-conflict episodes; multi-object turnover support is zero.

For seed 41, goal-conflict turnover cases have median probability/state ratios `5.725 / 2.760`, while multi-object turnover cases have `8.652 / 1.920`. Seed 42 goal-conflict cases have `15.392 / 4.421`.

So the strongest genuinely cross-seed supported regime is the **goal-conflict / high-magnitude** region. Multi-object generality is not replicated across the two DEV seeds.

## Collision / ownership check

Latest Evidence Analyst state observed during this run has MAIN allocated to `ASSEMBLY_PROTOTYPE_LOCKIN_ARCHITECTURE_STUDY_CYCLE1`; SUB remains independent Discovery. `CAND-TOPK-PA-01` is separately held pending this read-only support result. This Utility assignment therefore does not collide with the active MAIN/SUB critical path, and MAIN does not need to wait for it.

## Classification and recommendation

### Diagnostic classification: `MIXED`

Reason:

- **positive:** independent seed replication at `0.10`, leave-one-seed stable, strong directional ratios, and survival under every predeclared `n>=3/5/10` support sensitivity as well as the existing `n>=20` gate;
- **limiting:** all replicated support is concentrated in the `0.10` magnitude, seed 42 support is clustered in only 5 episodes and entirely in one world family, lower magnitudes are under-supported, and the current label is not leave-one-`0.10`-stratum robust.

### Recommendation: `ADD_MORE_ARCHITECTURE_SUPPORT`

This does **not** mean rerun Top-k cycle 3 or tune the same object. Same-object continuation remains unauthorized. If Evidence Analyst continues the line, the useful next object is a **fresh prospectively specified ordinary-reduction Architecture question** targeted at the supported high-magnitude regime, explicitly testing whether hard switching / branch-basin selection / recurrent WTA hysteresis or related ordinary mechanisms explain the residual. PRE_FORMAL planning should wait until that reduction question is answered or a genuinely independent mechanistic residual survives it.

No follow-up Utility request was self-issued; fresh allocation belongs to Evidence Analyst / Control Brain.

## Integrity record

- scientific/model workflow rerun: `false`
- workflow dispatch: `false`
- training/probe rerun: `false`
- official TEST accessed: `false`
- formal/consumed raw evidence accessed: `false`
- research/main branch mutated: `false`
- immutable evidence mutated: `false`
- scheduler mutated: `false`
- threshold/metric/horizon/comparator/seed changed: `false`
- canonical cycle result reclassified: `false`
- PRE_FORMAL/FORMAL authority created: `false`

Stop reason: `COMPLETED_ONE_BOUNDED_RESULT_MAX_RUNS_REACHED`.