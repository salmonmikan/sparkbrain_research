# SparkBrain Evidence Analyst — 2026-09-20 02:58 JST

## Executive decision

No new FORMAL scientific evidence exists. Authoritative `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; exactly five annotated `evidence/*` tags remain; tag-based `formal/*`, `sealed/*`, and `freeze/*` remain empty; thirteen legacy `freeze/*` branches remain preserved.

The material lower-funnel update is SUB's completed `V05_TOPOLOGY_DIMENSION_BINDING_DISCOVERY_CYCLE1`. The observation is real and current-path relevant: `V05BrainConfig.width`, `height`, and `receptor_rows` are public configuration fields, copied into the nested v0.4 config and serialized into v0.5 checkpoints, while `IntegratedV05Brain` constructs the actual field using an explicit `layered_reservoir_topology(seed=...)` whose geometry defaults to 16 receptors plus an 8x6 reservoir. A non-default `(12,10,2)` configuration was accepted and retained yet produced the same realized 64-unit topology and connection structure as `(8,8,1)`. Exact-head CI `35458809766` succeeded on `research/exploratory-sub-v05-topology-config-binding-20260920@ddd80443dd670698397683b95742428045c74932`.

SUB Discovery review classification: **`PROMOTE_TO_ARCHITECTURE_STUDY`**. This is not evidence of a new computational principle or mechanistic distinctness. It is a fresh Architecture/API-correctness question about declared configuration, realized geometry, checkpoint semantics, and reproducibility. The exploratory branch/result remains strictly NON_EVIDENTIARY and is not relabeled as Architecture evidence.

MAIN is therefore activated on one new prospectively defined NON_EVIDENTIARY Architecture cycle, `V05_TOPOLOGY_CONFIG_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`. SUB returns to the default independent bounded-Discovery role and must not work on the promoted MAIN object.

## Authoritative repository state

- `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, unprotected.
- authoritative `evidence/*`: 5 annotated tags, unchanged.
- tag-based `formal/*`: 0; `sealed/*`: 0; `freeze/*`: 0.
- legacy `freeze/*` branches: 13, unchanged.
- repository rulesets: 0.
- Issue #139 remains open and accurately records the five evidence tags plus the protection gap.
- PR #148 and #149 remain open/unmerged governance work; neither is a scientific blocker.
- H5 STARTED/raw-preserve remain `058e90227cd48e1c10c6ecbaed01efdec1217d0e` / `ce5797eb584344db7a512e585506fb6c59ea475b`.
- NI01 STARTED/raw-preserve remain `d3e4a5d6349e7e69f21ffc3554998aa72f1f9d3d` / `8a39cf70e397bb7588f948910f01ec58672ac814`.

No new STARTED authority, consumed identity, formal score, raw/scored preserve, immutable evidence anchor, or scientific tag appeared.

## SUB Discovery review — v0.5 topology configuration binding

Latest SUB mode is `discovery`; candidate `CAND-V05-TOPOLOGY-CONFIG-BINDING-01`; exact research head `ddd80443dd670698397683b95742428045c74932`; workflow `35458809766` completed `success`. The branch is exactly three commits ahead of stable main and changes only the prospective Discovery note, one exploratory test, and the Discovery result note; production source is unchanged.

Independent source reconciliation on current `main` confirms the mechanism:

- `V05BrainConfig` publicly exposes `width=8`, `height=8`, `receptor_rows=1`.
- `IntegratedV05Brain` copies those fields into `V04BrainConfig` but passes an explicit `layered_reservoir_topology(seed=self.config.topology_seed)` into `IntegratedV04Brain`.
- `IntegratedV04Brain` uses a supplied topology instead of constructing `grid_topology(width, height, receptor_rows, ...)`.
- `layered_reservoir_topology` defaults to `receptor_count=16`, `reservoir_width=8`, `reservoir_height=6`; therefore realized geometry is not parameterized by the three v0.5 fields on the current integrated path.
- `configs/v05_reference.json` persists `width`, `height`, and `receptor_rows` as configuration values.
- v0.5 `state_dict()` serializes the public config, and `load_checkpoint()` reconstructs `V05BrainConfig(**payload["config"])` before replacing the nested field from the checkpoint. Thus declared geometry-like values participate in checkpoint identity even though current construction does not bind them to initial layered topology geometry.

The Discovery result does not rescue the rejected stride-11 aliasing candidate. Its motivation is API/configuration consistency on the current integrated runtime.

Review classification: **`PROMOTE_TO_ARCHITECTURE_STUDY`**.

Promotion boundary: start a NEW prospective Architecture object. Do not treat the Discovery's `(8,8,1)` versus `(12,10,2)` comparison as already-established Architecture evidence, and do not use the rejected resonant stride-11 behavior as a success criterion.

## Prospective MAIN Architecture object

`main_lane = V05_TOPOLOGY_CONFIG_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`

Purpose: characterize whether public v0.5 geometry-like configuration, realized topology, and checkpoint round-trip semantics form a coherent supported API contract. Claim type is architecture/system integration, engineering correctness, and research/testbed reproducibility only.

### Fixed source/runtime binding

- source: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- `src/sparkbrain/v05/brain.py` blob `652552f8dc6a53a68e441f593e9bfd82cebb9f7c`
- `src/sparkbrain/v05/topology.py` blob `d9d292bdedc1288a929d1e53f03b9fc182b45a36`
- `src/sparkbrain/v04/brain.py` blob `25fd56b082168a9ea71f313023451858d00b6184`
- `configs/v05_reference.json` blob `d3c82d0279c3bce09d76ddf0ad2df1ec74bc2d7f`
- runtime: ordinary local reference runtime only; no dataset, trained checkpoint, official TEST, retained confirmatory input, scorer, or consumed evidence.

### Fixed diagnostic matrix

Use topology seed `41` and the following factorized development-only configs, chosen prospectively to separate the three exported fields rather than tune against the Discovery result:

1. baseline `(width=8, height=8, receptor_rows=1)`
2. width-only `(12,8,1)`
3. height-only `(8,10,1)`
4. receptor-only `(8,8,2)`
5. combined `(12,10,2)`

For every config, record before any interpretation:

- declared v0.5 config tuple and nested v0.4 config tuple;
- realized total-unit count, receptor count/IDs, reservoir count, coordinate extents, and connection count;
- whether construction emits any error/warning for the non-default geometry fields;
- checkpoint payload config and nested field/topology state metadata;
- save/load round-trip declared config plus realized field topology metadata after reload;
- whether checkpoint round-trip preserves or repairs any declared-vs-realized mismatch.

Also perform a read-only contract audit over current docs/tests/callsites for an explicit statement that these fields are intentionally non-operative compatibility metadata or that v0.5 geometry is fixed. Do not invent a replacement geometry formula: whether `width/height` should mean total field dimensions, reservoir dimensions, or unsupported compatibility fields is intentionally left as a semantic branch, not inferred from outcome.

### Fixed Architecture classification

- `INTENTIONAL_FIXED_TOPOLOGY_EXPLICIT_CONTRACT`: current supported docs/tests explicitly define fixed v0.5 geometry and non-operative compatibility fields, and runtime/checkpoint behavior is consistent with that contract. Stop; candidate becomes `REJECT/NO_ACTION` scientifically, with documentation/engineering cleanup only if useful.
- `SILENT_DECLARED_REALIZED_GEOMETRY_DIVERGENCE`: non-default geometry-like fields are accepted/persisted without an explicit fixed-topology contract, realized geometry remains unbound, and checkpoint round-trip preserves the contradictory declared/realized state. Stop; record an Architecture/API correctness signal and return for fresh review. No same-run code fix.
- `PARTIAL_BINDING_OR_INCONSISTENT_ROUNDTRIP`: only some exported fields bind or checkpoint/runtime metadata disagree in another deterministic way. Stop for fresh Analyst review.
- `AMBIGUOUS_CONTRACT`: behavior is observable but supported semantics cannot be determined from current canonical source/docs/tests. Stop and HOLD; do not probe until a desired answer emerges.
- `INVALID_DIAGNOSTIC`: binding mismatch, unexpected access to forbidden surfaces, or inability to compare the fixed matrix without changing semantics. Discard and stop.

Any valid outcome stops after cycle 1. Architecture success does not authorize PRE_FORMAL or FORMAL work; any implementation/deprecation/backward-compatibility fix is a separate fresh engineering/Architecture decision.

Methodology fidelity requirement applies prospectively: if a workflow artifact is produced, durable MAIN/Analyst handoffs must bind exact workflow/head, artifact ID/archive digest, embedded contract identity/digest, raw digest if present, mapped outcome, and each machine-summary field actually narrated. Any mismatch fails closed for successor design until reconciled.

## External inputs

### Literature

Latest Literature remains `2026-09-20 00:30 JST`; no newer literature result was found. Its material finding remains Temporal-specific: batch partition effects are first reduced by non-anticipation, event-time versus processing-time, discrete-event chronology, and partition-invariance semantics. It does not change the new v0.5 config-contract allocation and does not reopen Temporal.

### Independent Audit

Latest independent Audit remains H5 (`ROBUST_SO_FAR`). The exact registered `FAIL_NO_USEFUL_WORK_REDUCTION` result and one-way integrity remain supported, while globally eager all-edge eligibility maintenance limits programme-level generalization. H5 stays consumed and closed; no allocation change.

### Methodology Calibration

Latest Methodology Calibration (`02:20 JST`) remains `MIXED_CALIBRATION`: core scientific gates and four-layer funnel are sound, but artifact-to-handoff value fidelity still lacks a demonstrated systemic guard. Control Brain has now ACCEPTED its request and assigned `CTRL-20260920-0250-ARTIFACT-HANDOFF-FIDELITY`, one bounded read-only NON_EVIDENTIARY consistency audit, with Temporal mandatory and Top-k/Assembly optional. The assignment is active and nonblocking for MAIN science. This changes process requirements, not scientific claims.

### Repository Steward

Latest Steward (`01:50 JST`) is consumed as governance advisory only. Its material facts were independently rechecked: five evidence tags, thirteen legacy freeze branches, zero repository rulesets, unprotected `main`, open Issue #139, and open/unmerged PR #148/#149. Its Temporal fidelity finding is a control-plane defect, not a scientific or immutable-ref incident.

## Research-layer state

| Layer | State | Owner / rule |
|---|---|---|
| `DISCOVERY` | `OPEN` | SUB default; one genuinely independent bounded synthetic/dev/read-only question per run, NON_EVIDENTIARY |
| `ARCHITECTURE_STUDY` | `ACTIVE_PENDING_PROSPECTIVE_BINDING` | MAIN: `CAND-V05-TOPOLOGY-CONFIG-BINDING-01` fresh API/config-contract cycle 1 |
| `PRE_FORMAL` | `EMPTY_HOLD` | no fresh mechanistic/reduction object with sufficient lower-layer support |
| `FORMAL` | `EMPTY_HOLD` | no fresh identity / STARTED / TEST / scorer / preserve / evidence authority |

## Candidate pool

1. `CAND-V05-TOPOLOGY-CONFIG-BINDING-01` — **`ARCHITECTURE_STUDY`**. Question: are exported v0.5 geometry-like fields coherently bound to realized topology and checkpoint semantics, or silently accepted while runtime geometry remains fixed? Not a rescue: it is a current integrated API/reproducibility issue and uses neither stride-11 resonance nor a consumed result. Expected information gain `HIGH`, implementation distance `NEAR`. Ordinary reductions: intentional fixed-topology contract, compatibility metadata, configuration/documentation mismatch. Open choices are semantic ownership of width/height/receptor_rows and any future deprecation/binding behavior; cycle 1 does not choose a fix. Exploration counts: `DISCOVERY=1`, `ARCHITECTURE_STUDY=0`. Promote no further automatically; a deterministic mismatch returns for fresh engineering/Architecture review, explicit fixed semantics closes the candidate, ambiguity HOLDs.
2. `CAND-TEMPORAL-BATCH-PARTITION-01` — **`HOLD`**, `ARCHITECTURE_STUDY`; counts `DISCOVERY=1`, `ARCHITECTURE_STUDY=1`. Current question is complete and ordinarily reducible to event-time/partition semantics. Any successor must be a fresh partition-invariance/reliability object; no cycle 2 rescue.
3. `CAND-TOPK-PA-01` — **`HOLD`**, `ARCHITECTURE_STUDY`; counts `DISCOVERY=1`, `ARCHITECTURE_STUDY=2`, `UTILITY_READ_ONLY=1`. Replicated `0.10` signal is narrow and mixed; no cycle 3. A successor requires a fresh switching/basin/hysteresis/recurrent-transient reduction discriminator.
4. `CAND-H7-RESP-01` — **`HOLD`**, prospective `PRE_FORMAL`. Very high information value only if a genuinely native online/local responsibility-sensitive mechanism independently appears. Do not engineer one to rescue consumed negative lines.
5. `CAND-TOPOLOGY-FANOUT-ALIAS-01` — **`REJECT`**, `DISCOVERY=1`. Physical stride-11 modular aliasing is real but exact/reducible and outside the current integrated default geometry path; retain only as an engineering scaling constraint.

## MAIN / SUB allocation

`main_lane = V05_TOPOLOGY_CONFIG_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`.

MAIN owns the entire critical path for this fresh Architecture object: prospective contract, research branch/harness, source/runtime binding, CI/preflight, checkpoint diagnostic, instrumentation, artifact provenance, candidate-specific defects, interpretation, and any science-invariant pre-diagnostic fixes. SUB must not take any of those blockers or fixes.

`sub_lane = BOUNDED_SECONDARY_DISCOVERY`.

SUB may select at most one genuinely independent synthetic/development/read-only Discovery question. It must not continue the promoted v0.5 config-binding object, Temporal, Top-k, H7 construction, rejected fanout/Assembly/Structural/rescue work, the Methodology Utility assignment, or any consumed/formal/TEST/scoring/preserve/evidence surface.

`sub_fallback = NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON`.

MAIN must not absorb reserved SUB Discovery merely for utilization; SUB must not take MAIN critical-path work.

## Real blockers / blocked until

- v0.5 config contract: the repository currently exposes geometry-like fields and fixed layered construction but does not yet supply a prospectively adjudicated supported semantic contract; cycle 1 is designed to characterize this, not choose a post-outcome fix.
- PRE_FORMAL: no fresh mechanistic/reduction object with adequate lower-layer support.
- FORMAL: no fresh high-value object, fresh collision-free identity, complete source/package/runtime/input/protocol/comparator/scorer/preserver binding, pre-START review, or exactly-once STARTED authority.
- Top-k: fresh reduction question required; same-object cycle 3 prohibited.
- Temporal: fresh independent invariance/reliability question required; current object cannot be retuned.
- H7: native mechanism absent.
- Methodology: artifact-to-handoff consistency audit is active but nonblocking; disputed machine fields would fail closed until resolved.

## Top 3

1. **MAIN — `CAND-V05-TOPOLOGY-CONFIG-BINDING-01` fresh Architecture/API-contract cycle 1** — `HIGH / NEAR`. Characterize factorized config binding and checkpoint round-trip under a fixed prospectively bound matrix, then stop.
2. **Utility — `CTRL-20260920-0250-ARTIFACT-HANDOFF-FIDELITY`** — `HIGH / VERY_NEAR / READ_ONLY`, already assigned by Control and nonblocking. Determine whether the prior Temporal transcription defect is isolated or systemic across completed NON_EVIDENTIARY Architecture handoffs.
3. **SUB — independent bounded Discovery or explicit no-op** — `MEDIUM / OPTIONAL`. Prefer a genuinely new observable over utilization.

## #1 GO / STOP

**GO** for one NON_EVIDENTIARY MAIN Architecture Study cycle only after the new contract has fixed the source blobs, factorized config matrix, topology seed, checkpoint-roundtrip diagnostic schema, result categories, and artifact-fidelity fields before outcome-bearing diagnostics are viewed. Exact-head ordinary CI/readiness must be green. No formal identity or STARTED is created.

**STOP** immediately if official TEST/retained confirmatory/consumed raw is needed, if a geometry formula or correctness criterion must be chosen after seeing the diagnostic, if source/runtime/config matrix changes after outcome visibility, or if a semantic decision is needed that current canonical source/docs/tests cannot answer. A pre-diagnostic science-invariant lint/import/harness defect may be fixed by MAIN with exact-head CI recheck. Any valid result category also stops for fresh Analyst review. No same-run code fix, Architecture cycle 2, PRE_FORMAL, or FORMAL escalation.

## Prospective contingency tree

`V05_TOPOLOGY_CONFIG_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`

- `PRE_START_CONTRACT_COMPLETE + CI_GREEN` -> run exactly one fixed development-only diagnostic cycle.
- `PRE_START_MECHANICAL_BLOCKER` -> MAIN may repair only science-invariant lint/build/import/harness defects, rebind exact head, rerun ordinary CI, and continue unchanged.
- `PRE_START_SEMANTIC_OR_PROTOCOL_GAP` -> STOP; no outcome-driven contract completion.
- `INTENTIONAL_FIXED_TOPOLOGY_EXPLICIT_CONTRACT` -> STOP; `REJECT/NO_ACTION` scientifically, optional fresh engineering/docs cleanup later.
- `SILENT_DECLARED_REALIZED_GEOMETRY_DIVERGENCE` -> STOP; Architecture/API correctness signal only; fresh review before any implementation/deprecation decision.
- `PARTIAL_BINDING_OR_INCONSISTENT_ROUNDTRIP` -> STOP; fresh review.
- `AMBIGUOUS_CONTRACT` -> STOP/HOLD; obtain a semantic contract rather than probe for a preferred answer.
- `INVALID_DIAGNOSTIC` -> discard + STOP.
- `POST_DIAGNOSTIC_FAILURE` -> STOP; do not change matrix, seed, checkpoint semantics, metrics, or result mapping after outcome-bearing rows are visible.
- FORMAL `PASS / FAIL / INCONCLUSIVE / INVALID_EVIDENCE / PRE_START_BLOCKER / POST_START_FAILURE` remain `UNARMED_NO_FORMAL_OBJECT`.

Same-run continuation is authorized only for the pre-specified science-invariant mechanical repair branch; every valid scientific/Architecture outcome returns to Analyst.

## Do not touch / consumed identities

Do not rerun, retune, rescore, relabel, or post-outcome repair:

- `c19-external-v2-official-v4`
- `c19-r1-revision-authority-official-v1`
- `c19-r1-revision-authority-official-v2`
- `c19-r2-fsa-state-tracker-official-v1`
- `pd01-long-history-fading-memory-official-v1`
- `ni01-no-ignition-selective-prediction-official-v1`
- `h5-event-routing-work-reduction-official-v1`

Neither worker may mutate immutable/freeze/sealed/formal/evidence/control/preserve refs, access official TEST without fresh FORMAL authority, merge research PRs, change scheduler definitions, reinterpret completed Temporal/Top-k/consumed outcomes by new thresholds, or use the SUB Discovery result as formal/Architecture evidence.

## Governance advisory

Issue #139 remains the correct operational tracker for server-side tag protection. `main` is still unprotected and rulesets remain zero; this is a real but currently deferred governance gap, not a reason to delay the lower-funnel Architecture cycle. PR #148/#149 remain open/unmerged and deferred pending their existing correctness fixes. No preservation mapping or evidence tag should absorb lower-funnel, Utility, or Methodology outputs.

## Utility

No new Utility request is created. The previously proposed Methodology fidelity audit has already been accepted and assigned by Control as `CTRL-20260920-0250-ARTIFACT-HANDOFF-FIDELITY`; creating a duplicate request would add no information. Its result is methodology input only and cannot mutate scientific evidence or allocation without a fresh Analyst/Control decision.

## Handoff

MAIN takes the v0.5 topology configuration-contract Architecture cycle and owns **all** critical-path fixes. SUB returns to independent bounded Discovery and must not touch the promoted object or MAIN blockers. The active Utility fidelity audit remains separate and nonblocking. Neither worker touches consumed identities, FORMAL/TEST/scoring/preserve/evidence surfaces, immutable refs, research PR merges, or scheduler definitions.

Repartition only on fresh evidence: a valid config-contract cycle result returns here before any engineering fix; a genuinely independent SUB Discovery returns here before promotion; a Utility fidelity result may tighten handoff provenance requirements but does not itself promote scientific work; a fresh native H7-like mechanism or other high-value central object requires new prospective admission. No current result branch authorizes same-run PRE_FORMAL or FORMAL continuation.