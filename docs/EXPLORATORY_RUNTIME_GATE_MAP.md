# Runtime gate reachability and the next integrated question

Status: **SOURCE AUDIT / EXPLORATORY / NON_EVIDENTIARY**.
Source pin: `3cb955cd42474b36d2d37617e5390d08656c06f1` (main after PR #166).
Date: 2026-10-01 UTC. No runtime execution, parameter tuning, runtime edit, or new scientific result is reported here.

## Decision

The PR #166 event-clock result applies to a still-exposed legacy reference path, including the standard demo and benchmark. It does **not** describe the gate executed inside Integrated M1. Stop expanding that legacy grid merely as a proxy for current integration.

The strongest next bounded question is whether M1 can accept a fresh, opposite-sign later outcome when its current routing features exactly repeat an earlier observation. The source predicts an intentional SB002 identity/consistency guard will reject that outcome and roll back the entire M1 revision. A near-identical feature vector may cross that exact-identity boundary without changing the assigned route. This is a source-derived boundary hypothesis, not an executed finding or a defect determination.

## Three different meanings of "gate"

All source links below are pinned to the audited commit.

1. **Legacy engine gate.** `sparkbrain.engine.SparkBrain` calls its inline `_evaluate_coalitions` after hypothesis-target events or Spark firing, then `_maybe_ignite`. These are methods, not a `CoalitionManager` or `Workspace` class. This is the path tested by PR #166: [event dispatch](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/engine.py#L280-L310), [scoring and ignition](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/engine.py#L386-L541).
2. **Versioned v03/v032 gate.** `IntegratedV03Brain` constructs `v03_seed.CoalitionGate` and calls its `evaluate` method. That method defaults to `LEGACY_MODE = "legacy_v03_seed"`; this is a different implementation from item 1. Its bounded C14 mode is available but is not selected by this call. [Construction](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v03/runtime.py#L256-L267), [call](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v03/runtime.py#L737-L749), [mode dispatch](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v03_seed/coalition.py#L104-L116).
3. **M1 decision rule.** M1 acts when an explicit predictive-bank decision and a route-local candidate agree. Its outer action is not selected by either item 1 or the v03 reference action. [M1 observation/action rule](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L390-L443).

### Entry points that still reach the PR #166 implementation

- `from sparkbrain import SparkBrain` exports `engine.SparkBrain`: [package export](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/__init__.py#L5-L6)
- `scripts/run_demo.py` calls `worlds.run_scenario` with the canonical SwitchWorld: [demo](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/scripts/run_demo.py#L10-L18)
- `scripts/run_benchmark.py` calls the benchmark writer; its SparkBrain arms construct the reference brain and call `run_scenario`. Baseline arms are separate models, not additional confirmations of the legacy gate: [runner](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/scripts/run_benchmark.py#L6-L20), [SparkBrain arm](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/benchmark.py#L28-L46), [arm list](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/benchmark.py#L117-L145)
- The hybrid spiking backend also owns the reference engine and calls its event processor. This does not make fully spiking dynamics equivalent to the legacy engine: [backend construction](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/spiking.py#L49-L66), [event forwarding](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/spiking.py#L245-L257)

These paths make PR #166 relevant to compatibility/reference behavior. They do not establish the frequency or effect of its constructed padding condition in ordinary workloads.


### Additional paths and naming traps

- The legacy `/api/runs/*` Brain Lab uses `LabRun`, builds the reference brain and calls its `run` method. The module CLI `python -m sparkbrain.evaluation.run_suite` also uses this reference adapter: [Lab](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/lab/service.py#L124-L150), [evaluation adapter](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/evaluation/runner.py#L113-L177)
- The separate `/api/v03/runs` Lab constructs `IntegratedV03Brain`: [v03 Lab](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/lab/v03_service.py#L117-L137). The v03 evaluator variant named `legacy` means the whole-hash frontend, not `engine.SparkBrain`: [explicit variant definition](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v03/evaluation.py#L450-L454)
- `IntegratedV04Brain` owns a distinct cascade/spike `IgnitionGate`: [construction and execution](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v04/brain.py#L91-L155), [gate](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v04/dynamics.py#L193-L245)
- `IntegratedV05Brain` executes its v04 base but chooses mature, unsuppressed Assembly activations separately; its final selection is not gated by the base ignition list: [v05 episode and selection](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v05/brain.py#L154-L209)
- Learned and structural backends reuse common schemas but use the learned probability/confidence/margin decision, not `SparkBrain._maybe_ignite`: [learned gate](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/learned/backend.py#L107-L142), [structural inheritance](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/structural/backend.py#L19-L35)
- Visualizers serialize supplied traces or evaluation payloads; viewing an artifact does not execute the gate. Likewise, loading the package root can import the legacy module without executing legacy dynamics. Import reachability alone is insufficient evidence of behavioral reachability

## Exact M1 dataflow

Successful M1 processing is:

1. `IntegratedM1Session.cycle` requests the current observation, calls `pilot.observe`, resolves the chosen action in the world, and calls `pilot.apply_outcome`. [Session](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L633-L663)
2. `PredictiveRevisionPilot.observe` reads the raw sensory values into its own context and executes `reference_brain.step(sample)`. The v032 facade directly executes v03. [SB001 observation](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/predictive_revision.py#L250-L299), [v032 facade](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v032/runtime.py#L91-L159)
3. SB001 chooses among explicit predictive hypotheses by context distance and an ambiguity rule. `reference_action` and `reference_state_hash` are returned as additional fields; they are not arguments to this selection.
4. M1 reads the predictive decision/scalar/state ID and the independently queried route-local candidate. It does not read `prediction.reference_action` or `prediction.reference_state_hash` when constructing `M1Action`. [Agreement rule](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L407-L439)
5. Later outcome first updates or splits one explicit predictive hypothesis. It then supplies an alpha/beta candidate, derived from the outcome sign, to SB002. SB002 selects route-local hypotheses using clipped accumulated supports, softmax confidence and margin, without calling either legacy Coalition gate. [Predictive revision](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/predictive_revision.py#L362-L433), [scope selection](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/causal_scope_revision.py#L482-L537), [M1 outcome bridge](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L475-L525)

The v03 component is executed and checkpointed, not a mock. Its state affects inspection/hash/checkpoint contents, and an exception can prevent a successful M1 transaction. Therefore the precise conclusion is **no successful-decision data dependency on the reference action in this code**, not "the whole reference component is irrelevant" or "removing it is behaviorally equivalent."

The code already labels composition contribution as unestablished; this audit makes that boundary explicit rather than changing its scientific status. [Existing boundary](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/docs/SYSTEM_BUILD_M1.md#L99-L117)

## Why the exact-observation outcome question is more useful

SB002 first deduplicates evidence by its evidence ID. Separately, it hashes only the routing-feature vector and binds that digest to a candidate. Even with a fresh evidence ID, a different candidate for an existing digest returns `identical_observation_conflict` before router revision. [Two distinct identity checks](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/causal_scope_revision.py#L539-L614)

M1 maps nonnegative outcomes to alpha and negative outcomes to beta. If SB002 rejects the fresh receipt, M1 raises and restores the pre-outcome predictive, scoped and pending state. [Sign mapping and rejection](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L477-L525)

The built-in world uses only signal 0.0 or 0.45 and outcomes +0.8 or -0.8 respectively, modified by at most 0.1 by the action. Action effects therefore never reverse the sign for a given routing vector. [World](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L571-L592)

Consequently, repeated deterministic-world success does not answer whether M1 can revise through an opposite outcome at exactly the same observed routing context. The guard is explicitly tested at the SB002 component level; the missing question is its integrated-pilot effect on selective revision, pending-event liveness and exact-versus-near-identical input boundaries. No existing guard is to be weakened merely to make this diagnostic succeed.

Important API boundary: direct `IntegratedM1Pilot.apply_outcome` restores the pre-outcome pending state, whereas `IntegratedM1Session.cycle` catches an exception and restores both pilot and world from the pre-cycle checkpoint. The normal session route therefore does not retain that pending observation. Any pending-event blockage measured by the proposed direct-pilot driver is a Pilot-API observation, not a demonstrated session deadlock or system-wide liveness failure. [Outer rollback](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/integrated_m1.py#L643-L663)

## Proposed next protocol, not executed

Task-local label: `exploratory-m1-outcome-aliasing-20261001`. This is not a canonical candidate, build allocation, FORMAL identity, or request to reopen one.

### Scope and fixed matrix

Use public `IntegratedM1Pilot` observation/outcome APIs in an independent diagnostic driver. Leave runtime sources, default config, existing tests, built-in world and acceptance contracts unchanged.

Eight deterministic cases:
- Two target contexts: routing/sensory scalar 0.0 with baseline outcome +0.8, or 0.45 with baseline outcome -0.8
- Start each case with a fresh default `IntegratedM1Pilot`. Bootstrap scalar 0.0 / outcome +0.8 first, then scalar 0.45 / outcome -0.8, using fresh event and receipt IDs at times 0 and 1
- Four probe arms at time 2:
  1. exact target routing features, same-sign outcome (original control)
  2. exact target routing features, opposite-sign outcome (reversal)
  3. target routing features plus 0.000001, opposite-sign outcome (near-alias)
  4. target routing features plus 0.000001, same-sign outcome (null perturbation control)
- Keep the probe's sensory scalar at the exact target value in all four arms. Only the routing input receives the fixed offset. This isolates exact routing identity from SB001 context distance
- Use magnitude 0.8 for every receipt. All three event IDs and three receipt IDs per case are fresh and unique. Do not label a fresh contradictory observation as redelivery

### Fixed budget and observations

Each case attempts three observation/outcome pairs. Capture the JSON-safe pilot inspection and state hash before and after every call, all inputs/actions/revisions, exact exceptions and reasons, predictive hypotheses, scope supports/evidence/identity bindings, sequence and pending state.

Inspection hashes alone are insufficient for a full-rollback claim: the nested v03 inspection omits CoalitionGate stability/signatures, RNG and other internals. Also retain and compare the supported canonical component checkpoints from `PilotCheckpointManager.save` (including `reference-brain.json` from the direct v032 serializer) and `ScopeRevisionCheckpointManager.save`, alongside all compositor pending/event/receipt/trace/sequence fields from inspection. Use fresh no-clobber directories; compare parsed canonical payloads without discarding semantic fields. Repeated serialization must be state-neutral. If only inspection snapshots can be captured, narrow the report to inspection-visible rollback and mark complete serialized-state verification blocked. [Inspection boundary](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/v03/runtime.py#L362-L393), [predictive checkpoint](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/predictive_revision.py#L593-L615), [scope checkpoint](https://github.com/salmonmikan/sparkbrain_research/blob/3cb955cd42474b36d2d37617e5390d08656c06f1/src/sparkbrain/system_build/causal_scope_revision.py#L903-L920)

Then perform two fixed integrity probes:
1. Re-deliver the exact probe receipt once. On successful first delivery it should be idempotent; after rejection it is a retry of an uncommitted receipt, not duplicate committed evidence
2. Attempt a fourth fresh observation at time 3, with the same exact target sensory/routing features, and record acceptance or pending-event rejection. Do not supply a fourth outcome; stop the case

Thus the attempted call budget is four observations and four outcome deliveries per case, 32 of each across eight cases. Committed work is allowed to differ and must be reported; equal attempted calls are not a claim of equal computational work.

Keep failing cases and raw snapshots. No failed receipt may be dropped or replaced by a convenient same-sign outcome to continue the case. No threshold or offset search. Do not compute accuracy or success rates from this constructed matrix.

### Expected checks and falsifiers

Source-derived predictions:
- Original and null controls commit the probe
- Exact reversals reject through `identical_observation_conflict`, preserve the complete pre-outcome state and leave the original pending observation unresolved in this direct-Pilot-API driver
- A 0.000001 routing offset avoids the exact digest match while remaining in the original routing neighborhood; whether the whole integrated commit succeeds must be observed, not assumed
- If exact reversal commits, or rejection changes any pre-outcome state, preserve the result and stop for source/contract reconciliation
- If the near-alias changes route, hits another guard or fails differently, report that boundary instead of adjusting the offset

A near-alias commit must not be mistaken for successful adaptation: opposite support can leave the scope probabilities tied and the next predictive observation ambiguous. Record the fourth action and reason as well as whether its call succeeded.

The primary result is a transaction/identity boundary and its direct-Pilot-API pending-event consequence. The independent scripted driver does not execute `IntegratedM1Session.cycle` or establish its liveness under a modified world. This is not yet evidence of adaptation quality, route learning, robustness under natural noise or comparative performance.

### Reproducibility, authority and stopping condition

Before execution, freeze the driver and machine-readable matrix in a new durable checkpoint, pin runtime blobs, add focused driver tests for successful and failed records, and verify readback. Run in the cloud CPU workspace with no remote runtime dependencies. Retain every case, failure and environment/source hash. A second fresh process with a different `PYTHONHASHSEED` may check reproducibility; it is not independent scientific evidence.

Stop this bounded study after the complete fixed matrix, one reproducibility comparison and the exact-versus-near-identity interpretation. If the predicted boundary is confirmed, do not expand the grid automatically. The next decision is a contract/architecture question: whether exact-feature candidate consistency is the intended M1 capability boundary, and what a separately authorized fresh integration design should do with genuine changed outcomes. No automatic runtime repair, canonical promotion or scientific claim follows.

## Preflight and collision boundary

- Authoritative directive index: `ops/human-directives` head `8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, index blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`, freshly fetched 2026-10-01
- HUMAN-20260928-001 explicitly prioritizes integrated capability/interface gaps and permits non-colliding causal diagnostics, component-replacement tooling and synthetic-world work while preserving zero scientific credit and prospective science boundaries
- Analyst R177 retains 35/35 terminal scientific objects and no new scientific execution. Its assigned M1 robustness integration is PR #164; this audit does not execute that acceptance contract, repair its branch, reconcile authority, or alter its hold
- Current open PR scan found #164, #151, #149 and #148. #151 is explicitly a do-not-merge diagnostic. This task does not touch those PRs
- The prior event-clock report and its results remain unchanged
- This dedicated report owns its own status. Shared `PROJECT_STATUS.md` and result/authority ledgers are left untouched to avoid the PR #164 status-file conflict
- No scheduler, scheduler registry, Control/Analyst state, protected evidence, scientific identity or formal ref changes

## Verification status

This is a source-only report and prospective design, not a runtime result. No M1 study, full test suite, benchmark or new acceptance run was executed to produce it. Before running the next protocol, recheck the relevant current directive/ownership state and preserve the separate driver checkpoint.
