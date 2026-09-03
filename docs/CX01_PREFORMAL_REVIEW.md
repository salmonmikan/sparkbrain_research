# CX01 Pre-Formal Source / Fidelity / Fairness Review

Status: **SOURCE-FREEZE CANDIDATE — formal capability remains unopened**

This report closes the CX01 Wave 1 pre-formal engineering/scientific review. It does **not** constitute an independent execution seal, does not consume a formal candidate, and does not authorize a STARTED marker by itself.

## 1. Reviewed lineage

Historical evidence base:

- v0.6.1 candidate-003 report source: `6eed66c88ce5656d761b62c8b9d02b184e699313`
- candidate-003 is consumed historical evidence and is permanently non-reusable for CX01 formal evidence.

CX01 parent before this review:

- branch: `research/cx01-comparator-extension`
- reviewed base SHA: `30bd2ffa98508961942d060dd30d6f4fa4e8dd9a`
- PR: #17

Comparator-specific source branches inspected before review:

| Track | Branch | Remote head at review start |
|---|---|---|
| G6 | `research/cx01-g6-vomm` | `deff667d9f88b72feb6b1442c65b2b053d9897d4` |
| G7 | `research/cx01-g7-htm` | `01cae25d95725bf43cd2a7f0acfb0293a094f4fe` |
| G8 | `research/cx01-g8-stm` | `c9a61309e04a01d73ba7c9fd4e0bdf3bf59bda22` |

Those individual branches were not modified during this review. Shared pre-formal corrections were isolated in:

- branch: `research/cx01-preformal-boundary-review`
- PR: #19

Default-branch dispatch registration is intentionally isolated from model/source work:

- branch: `research/cx01-formal-dispatch-registration`
- PR: #20
- content: one fail-closed workflow registration stub only.

## 2. Scope lock

The review intentionally did **not** change the CX01 world generator.

`src/sparkbrain/comparison/cx01/worlds.py` has the same blob identity on the parent base and the review branch:

```text
e9397a9f093c68592cc809849b4ada6aee1980d3
```

No rapid contingency-cycle world, exposure count, or target sequence was modified to improve development results.

The family pass gates remain unchanged:

```text
HIGH_ORDER  exact probe discrimination
TIMING      exact timing-conditioned discrimination
CYCLE       correct_fraction >= 0.80 AND maximum_reacquisition <= 2
BRANCH      top1 exact AND Brier <= 0.10 AND log_loss <= 1.20
SELECTIVITY selective_effect >= 0.50
LOOP        valid output AND self_confirmation_violations == 0
```

The only scoring-code change in this review canonicalizes token summation order for Brier/cross-entropy so byte-level floating-point evidence is stable. It does not change the metric definition or any threshold.

## 3. Pre-formal blockers found and closed

### B1 — evaluation prefixes could update learned parameters

Before review, the same `observe_external()` learning path was used for training events and held-out/query prefix events.

Closed by:

- `observe_external(event, learn=...)` in the shared comparator contract;
- inference-only probe/cue observations for HIGH_ORDER, TIMING, BRANCH, and SELECTIVITY;
- learned-state hash invariant before/after every non-adaptive evaluation family;
- CYCLE remains intentionally online: phase exposure learns, cue-only readout does not;
- LOOP cue/generated proposal does not learn, later external consequence may learn.

### B2 — G4 final training episode committed at first probe boundary

G4 sequence learning previously retained its last training episode until the next `episode_start`, which could be the first evaluation event.

Closed by:

- explicit `finalize_episode()` across the common contract;
- `_train()` finalizes training before the first evaluation probe;
- a dedicated G4 boundary test verifies no pending training episode remains.

### B3 — G8 fidelity wording exceeded implemented causal mechanism

Local G8 prediction uses explicit recent token/timing associations. Its membrane/population state is not causal to the scoring path.

Closed by narrowing the claim to:

```text
G8-P = timing-context prediction capability reference
G8-R = same local association substrate + explicit replay/excitability privilege
```

No claim is made that CX01 G8 reproduces NEST/NESTML sTM dynamics, dendritic prediction, structural rewiring, homeostasis, or biophysical spiking causality.

### B4 — G7 exposed inert HTM-like configuration surface

Unused HTM-like parameters were removed so the local comparator does not imply mechanisms that are not implemented.

The retained claim is an **independent HTM-style high-order sparse-context capability reference**, not an official HTM implementation benchmark.

### B5 — evidence metrics had process-order last-bit drift

Brier score previously iterated an unordered token set. A prior rerun differed only at about `1e-18` in three G7 BRANCH rows.

Closed by:

- canonical sorted token accumulation in Brier and cross-entropy;
- deterministic metric insertion-order unit test;
- `PYTHONHASHSEED=0` in audited development workflow;
- exact Python 3.11.16 for the audited development matrix.

### B6 — formal source SHA did not fully constrain package-install environment

The former formal workflow performed editable installation, permitting future build-tool dependency resolution despite an exact source SHA.

Closed by:

- direct frozen-source execution through `PYTHONPATH=<source>/src`;
- no project/package installation before formal capability;
- exact CPython 3.11.16;
- `ubuntu-24.04` runner family;
- pinned checkout/setup-python/upload-artifact action revisions;
- environment preflight artifact before capability.

### B7 — GitHub manual dispatch path was not registered on the default branch

The repository default branch is `main`, while the formal workflow implementation lives in the CX01 research source. GitHub requires a `workflow_dispatch` workflow to exist on the default branch before manual/REST dispatch can be received.

Closed structurally by:

- PR #20: a default-branch registration stub at the same workflow path;
- the stub is fail-closed and always refuses formal capability on `main`;
- formal execution is required to use a dedicated freeze tag as the workflow dispatch `ref`;
- the frozen workflow fails before capability unless `GITHUB_SHA == source_sha`.

Therefore the workflow definition used for capability is itself bound to the frozen source revision rather than a moving branch or the registration stub.

## 4. Fidelity verdicts

### G3

Historical first-order token transition anchor. Historical `recurrent` naming must not be interpreted as GRU/LSTM/RNN fidelity.

### G6

```text
variable-order / longest-supported-suffix capability: PASS
CTW / PPM / PST implementation fidelity: NOT CLAIMED
```

The critical comparison remains G3 first-order versus G6 higher-order recent context.

### G7

```text
sparse high-order context / Temporal-Memory-style capability: PASS
official/full HTM algorithm fidelity: NOT CLAIMED
official HTM performance benchmark: NOT CLAIMED
```

### G8-P / G8-R

```text
timing-conditioned context capability: PASS
prediction/replay privilege separation: PASS
published sTM implementation fidelity: NOT CLAIMED
biophysical spiking-dynamics causal fidelity: NOT CLAIMED
2026 element-specific timing extension reproduction: NOT CLAIMED
```

The literature boundary is recorded in `docs/CX01_PRIOR_ART.md`.

## 5. Fairness verdict

The development artifact generator fails closed unless every world has:

- exactly seven comparator conditions;
- one identical architecture-neutral training transcript hash across all conditions.

Latest audited matrix reports:

```text
world_count                         30
complete_world_count                30
matching_transcript_world_count     30
incomplete_worlds                   []
transcript_mismatch_worlds          []
architecture_count                   7
```

Result:

```text
FAIRNESS TRANSCRIPT GATE = PASS
```

## 6. Development matrix after boundary corrections

The full matrix remains:

```text
30 worlds × 7 comparators = 210 development executions
```

| Comparator | BRANCH | CYCLE | HIGH_ORDER | LOOP | SELECTIVITY | TIMING | Total |
|---|---:|---:|---:|---:|---:|---:|---:|
| G3 first-order | 5/5 | 0/5 | 0/5 | 5/5 | 5/5 | 0/5 | 15/30 |
| G4 Assembly | 0/5 | 0/5 | 5/5 | 5/5 | 5/5 | 0/5 | 15/30 |
| G5 typed | 5/5 | 0/5 | 0/5 | 5/5 | 5/5 | 0/5 | 15/30 |
| G6 variable-order | 5/5 | 0/5 | 5/5 | 5/5 | 5/5 | 0/5 | 20/30 |
| G7 HTM-style TM | 5/5 | 0/5 | 5/5 | 5/5 | 5/5 | 0/5 | 20/30 |
| G8-P timing prediction | 5/5 | 0/5 | 5/5 | 5/5 | 0/5 | 5/5 | 20/30 |
| G8-R replay | 5/5 | 0/5 | 5/5 | 5/5 | 5/5 | 5/5 | 25/30 |

Rapid contingency-cycle remains **0/5 for every comparator**. This negative development result was retained without world or threshold tuning.

## 7. Outcome-invariance audit against previous audited development artifact

Previous audited artifact used for direct comparison:

- artifact ID: `9904068703`
- zip digest: `sha256:8585d3a0d461ec21462c31a88cf0e50812eb9ac5ce0f5896d04d0ea3954b4631`

Pre-formal audited artifact used for the 210-row invariance comparison:

- workflow run: `33783183869`
- artifact ID: `9904403063`
- artifact name: `cx01-development-02d5f5f39bfc82cbf2d901acd828b365c4a2b24b`
- zip digest: `sha256:2c9fc2b7ddc93dbc4968a098ff0d105ed17ae9d8dc59c46413d891ec5d08b219`

A record-by-record comparison of all 210 executions found:

```text
decision                    210 / 210 identical
evidence                    210 / 210 identical
family                      210 / 210 identical
kind                        210 / 210 identical
seed                        210 / 210 identical
world_hash                  210 / 210 identical
training_transcript_hash    210 / 210 identical
```

Resource measurements are intentionally not required to be byte-identical because wall clock, CPU time, and traced memory are descriptive-only runtime measurements.

Result:

```text
BOUNDARY-CORRECTION OUTCOME INVARIANCE = PASS
```

A final audited development artifact must still be retained for the exact source-freeze SHA after PR #19 is merged into the parent.

## 8. Formal control-plane review

The source includes fail-closed controls for:

- fresh formal generation namespace;
- historical/development/test/fixture seed exclusion;
- outcome-blind declaration bundle;
- exact source/candidate/grid/declaration/privilege/schedule/scoring/schema hashes;
- freeze-builder identity;
- independent reviewer seal identity distinct from builder;
- persistent committed STARTED marker;
- candidate-spec-hash + source-SHA workflow identity;
- freeze-tag dispatch whose `GITHUB_SHA` must equal source SHA;
- fail-closed default-branch workflow registration stub;
- supplemental duplicate Actions-history scan;
- local exclusive STARTED marker before capability;
- per-execution atomic raw cells + checksums;
- partial raw retention and `RUN_FAILED.json`;
- `RAW_COMPLETE.json` only after full raw verification;
- semantic execution hash excluding descriptive runtime timing/memory;
- scoring only after raw lock;
- frozen non-compensatory scorer.

Important limitation:

> The assistant that performed this source/fidelity review is **not** a scientifically independent execution reviewer. A different reviewer must inspect the frozen bundle and issue the independent seal. Merely using a different reviewer string does not establish independence.

## 9. Seed boundary

Permanent non-formal ranges include:

```text
100..109       historical qualification
1000..1009     candidate-002
2000..2009     candidate-003
3000..5999     CX01 development/test/fixture band
```

No `cx01 6000` usage was found in the repository search at this review stage. A final search must still be performed immediately before selecting a formal seed band after the exact source SHA is frozen.

## 10. Pre-formal decision

At this review stage:

```text
source contract review             PASS
fidelity claim boundary            PASS
world semantics unchanged          PASS
scoring thresholds unchanged       PASS
training transcript fairness       PASS
train/eval isolation               PASS
outcome invariance                 PASS
formal control-plane static review PASS
default-branch dispatch stub       PENDING PR #20 MERGE
independent execution seal         NOT YET AVAILABLE
formal candidate capability        UNOPENED
```

Therefore:

> **CX01 becomes SOURCE-FREEZE READY only after PR #19 is merged into the parent, PR #20 is merged into `main`, and the exact merged parent SHA passes both repository CI and the 210-execution audited development workflow.**

Do not create STARTED or execute formal capability until a genuine independent seal exists.
