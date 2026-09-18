# SparkBrain Repository Steward — Latest

Timestamp: 2026-09-18 13:50 JST
Selected role: `REPOSITORY_STEWARD` from the 13:50 JST slot; no role inference required.

## Overall
Repository doctrine remains **partially compliant and scientifically well separated**. `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d` remains the stable shared substrate and remains unprotected. Active NI01 prospective work is isolated under `research/*`; NI01 is still preformal/unconsumed and no Steward action touched its scientific contract.

The material governance update since the prior Steward run is that **C19-R2 and PD01 have both terminalized and now have authoritative annotated `evidence/*` tags**, raising the authoritative evidence-tag count from 1 to 3. Issue #139 was updated to match this current remote state while remaining open because repository rulesets are still absent. The second major task this run was the Control-Brain-requested **read-only structural inventory of legacy comparator/comparison assets for possible future `main` promotion**. No research code was promoted or merged.

## Control-plane and remote reconciliation
Control-plane branches were treated only as mailboxes and reconciled against fresh remote repository state.

- Control Brain mailbox head consumed: `b9ce2adde261f5cca5691e03ab124aaaed971520`.
- Evidence Analyst mailbox head consumed: `938231f8acb714dfa832139383beef6bb8afb0c3`; latest analysis is 2026-09-18 13:03 JST.
- Orchestrator report branch observed: `9082d85db0341f9c0a1173f6d64a92c620be7809`.
- MAIN latest is 2026-09-18 13:47 JST, mode `RELAY`, on NI01 exact research head `2664951b65dd18883d3d80862e80b86ac66cf24f`.
- SUB latest is 2026-09-18 13:32 JST, mode `no_op`, with no formal or incubator lane.

Fresh remote facts:

- `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, `protected=false`.
- repository rulesets: **0**.
- legacy `freeze/*` branches: **13**, all present.
- open non-PR Issues: **#139 only**.
- open PRs: **#148 and #149**; both are mergeable one-file governance/helper PRs and their observed CI checks are green.
- authoritative annotated `evidence/*` tags: **3**:
  - C19-v4: tag object `4d6c0bd9a6c06c17352941d3fa730502e72b8540` -> evidence commit `a0f83318356ced1c84863737803080d0dc69d208`;
  - C19-R2: tag object `82b88f3e2ad524fed8b72300dcba46053c1f2c7e` -> evidence commit `6197fa801a78a0c5de4c2b6ff5d03216ac5539db`;
  - PD01: tag object `e4c4e6428d8ef9e09e92cae231041de0788162e2` -> evidence commit `fc5c8cda283360addddb7da482b14e69beaba1f7`.

Evidence Analyst records PD01 as terminal `FAIL_REDUCED_BY_FADING_MEMORY`, with its identity consumed/no-retry and raw-before-score/preservation chain complete. Stewardship does not reinterpret that result; its governance consequence is only that the new immutable evidence anchor must be tracked and left untouched.

Current NI01 remote reconciliation:

- research branch: `research/ni01-no-ignition-selective-prediction-spec-20260918@2664951b65dd18883d3d80862e80b86ac66cf24f`;
- proposed identity: `ni01-no-ignition-selective-prediction-official-v1`, still unreserved/unconsumed;
- dedicated preformal run `35308269458`: success on the exact head;
- ordinary CI `35308269286`: independently re-fetched after the MAIN checkpoint and is now `completed/success` on the same exact head;
- no formal STARTED, preserve, scoring, or evidence object is authorized by the current Analyst handoff.

The MAIN mailbox still records ordinary CI as in-progress because its report was written before the run completed. This is a normal mailbox timing lag, not a scientific or governance inconsistency. Stewardship did not advance NI01; the next action remains fresh Evidence Analyst review.

## Doctrine drift found / corrected / deferred

### Correct / compliant
- `main` has not absorbed NI01, PD01, C19-R2 scientific semantics, or SUB exploratory artifacts.
- Active unresolved science remains off `main` under research/control/preserve/evidence refs as appropriate.
- New terminal evidence is anchored with annotated `evidence/*` tags rather than new moving freeze branches.
- SUB correctly remains `no_op` rather than taking NI01 MAIN-critical work or inventing an outcome-rescue lane.
- Canonical scientific result/state remains git-managed; Issues remain operational governance tracking.

### Corrected this run
- **Issue #139 stale inventory corrected:** it previously said the repository had one authoritative evidence tag. It now records all three current annotated evidence tags and their peeled evidence commits. No acceptance criterion or scientific interpretation was changed.
- Stewardship state was advanced from the stale pre-R2 snapshot to current terminal C19-R2/PD01 plus preformal NI01 state.

### Deferred / non-blocking
- server-side tag update/delete protection remains absent (`rulesets=0`), and `main` remains unprotected;
- legacy freeze migration remains intentionally deferred until protected migration semantics exist;
- comparator/comparison assets reviewed below are **not ready for direct cherry-pick** from old divergent research branches; several exact historical heads are red or lack current CI, so any promotion must be a clean extraction onto current `main` with fresh tests;
- historical CX01/v0.6-specific workflow plumbing on `main` remains debt but is not on the current information path.

## Issue audit / changes

### #139 — updated, remains open
Updated only the factual inventory:

- authoritative annotated evidence tags: `1 -> 3`;
- added C19-R2 and PD01 tag objects / evidence commits;
- acceptance criterion for creation tooling now notes successful exercise by three authoritative tags.

The substantive governance gap is unchanged: repository rulesets remain zero, so routine server-side update/delete protection is still absent. Scheduled Stewardship made **no** ruleset or branch-protection mutation.

### No new scientific/operational Issue created
NI01 is preformal and awaiting fresh Analyst authority, so no Issue is needed. No Issue was created for PD01 or C19-R2 terminal scientific interpretation; their canonical git evidence is authoritative. No extraction/promotion Issue was created because the requested activity this run was an inventory, not authorization to start broad refactoring.

## Freeze branch -> tag migration / preservation mapping

- legacy `freeze/*` branches: **13**;
- all observed legacy freeze refs remain present and untouched;
- authoritative annotated evidence tags: **3**;
- new evidence tags since the prior Steward snapshot: **2** (C19-R2 and PD01);
- legacy branch-to-tag mirrors created this run: **0**;
- freeze branches moved/deleted/force-updated: **0**.

`reports/repository_steward/legacy_freeze_map.md` is specifically a legacy branch-to-tag mapping and therefore did not require a change: neither C19-R2 nor PD01 is a legacy-freeze mirror. Their annotated tags are already direct authoritative evidence anchors. Preserve/control/evidence identifiers are recorded in current Steward state, but no scientific mapping/ref was mutated.

## Tag protection / ruleset status
Read-only governance state remains **gap present**:

- authoritative annotated-tag creation workflow: available and exercised;
- authoritative `evidence/*` count: 3;
- repository rulesets: 0;
- `main` protection: disabled;
- `freeze/*`, `sealed/*`, `formal/*`, `evidence/*` server-side update/delete protection: absent.

Issue #139 remains the tracker. No ruleset/protection write was attempted.

## Main-promotion structural inventory
This inventory implements the accepted Control Brain directive to separate reusable infrastructure from scientific semantics. **No promotion was performed. No wholesale branch merge/cherry-pick is recommended.**

### A. Strongest candidates for a small neutral `main` extraction
These are structurally outcome-independent, but must be extracted from CX01/G3-G8 naming and revalidated on current `main` before promotion.

1. **Anonymous event + prediction-distribution primitives**
   - Source examined: `src/sparkbrain/comparison/cx01/events.py` on the comparator branches.
   - Reusable core: external/generated event origin, anonymous token/timestamp validation, generated-event boundary guard, normalized prediction distribution.
   - Classification: **MAIN_ELIGIBLE_AFTER_NEUTRAL_EXTRACTION_AND_FRESH_CI**.
   - Keep out: any CX01-specific world/expected-target semantics.

2. **Architecture-neutral comparator protocol shape**
   - Source examined: `src/sparkbrain/comparison/cx01/contract.py`.
   - Reusable core: `observe_external`, `advance`, `generate`, `distribution`, `suppress`, `snapshot/restore`, and descriptive resource counters.
   - Classification: **MAIN_ELIGIBLE_AFTER_SPLIT**.
   - Required split: the protocol interface is generic; `ComparatorKind` values `G3...G8` are research-program taxonomy and must remain research-local.

3. **Snapshot/restore contract and generic invariants**
   - Reusable idea appears consistently in G6/G7/G8 implementations.
   - Classification: **MAIN_ELIGIBLE_AS_INTERFACE/TEST_CONVENTION**, not by moving implementation-specific state schemas.
   - Candidate generic tests: deterministic round-trip, no hidden target/context fields, generated events do not mutate learned state unless explicitly allowed.

4. **Descriptive resource accounting**
   - Source examined: `src/sparkbrain/comparison/cx01/resources.py`.
   - Reusable core: wall/process CPU, traced peak memory, parameter/state counts, observed/generated event counts; existing `decision_use="descriptive-only"` guard is appropriate.
   - Classification: **MAIN_ELIGIBLE_AFTER_DECOUPLING** from `ComparatorKind` and the CX01 privilege lookup.

5. **Privilege-schema validation**
   - Source examined: `src/sparkbrain/comparison/cx01/privilege.py`.
   - Reusable core: explicit privilege declarations plus hard guards against generated-event self-training, evaluator-context visibility, and correct-target visibility.
   - Classification: **MAIN_ELIGIBLE_AFTER_SPLIT**.
   - Keep research-local: the exact G3-G8 privilege mapping and scientific judgement of which privilege each comparator has.

6. **Fairness/transcript hashing and validation**
   - Source examined: `src/sparkbrain/comparison/cx01/fairness.py`.
   - Reusable core: construct/validate an external-only chronological transcript before model instantiation; stable transcript hashing.
   - Classification: **MAIN_ELIGIBLE_AFTER_GENERICIZATION**.
   - Keep research-local: `CX01World`, balanced-exposure schedule, and experiment-specific episode semantics.

### B. Comparator assets that should remain research-local as implementations

- **G3 recurrent comparator** (`src/sparkbrain/baselines/v06/g3_recurrent.py`): the underlying token-to-token recurrent predictor is simple/reusable in isolation, but the file imports v0.6 confirmatory types and qualification worlds. **No direct promotion.** If independently useful, extract only a pure predictor class/config with neutral tests.
- **G4 assembly comparator** (`g4_assembly.py`): explicitly encodes Assembly IDs as the mechanism being contrasted. **RESEARCH_ONLY**; it is a scientific comparator, not shared substrate.
- **G5 typed functional-head comparator** (`g5_typed.py`): explicit prediction/action/reward/memory heads plus privileged scalar reward are the experimental contrast. **RESEARCH_ONLY**.
- **G6 VOMM** (`research/cx01-g6-vomm`): the variable-order suffix predictor is broadly reusable and well-factored around anonymous events, but the historical exact head's observed checks are red and it is coupled to CX01 protocol/kinds. **EXTRACTION_CANDIDATE, NOT DIRECT_PROMOTION**.
- **G7 HTM-inspired temporal memory** (`research/cx01-g7-htm`): explicitly a local reference implementation, not `htm.core`; fixed SDR/segment semantics are comparator science. Historical exact-head checks are red. **RESEARCH_ONLY**; only neutral interfaces/invariants should escape.
- **G8 spiking temporal memory** (`research/cx01-g8-stm`): explicitly a local reference comparator rather than a bit-for-bit published implementation; timing/replay semantics and global replay privilege are scientific contrast. Historical exact-head checks are red. **RESEARCH_ONLY**.

### C. Legacy v0.6 qualification harness
`src/sparkbrain/baselines/v06/common.py` hard-codes qualification families, seeds, world parameters, and confirmatory evidence types. It is **RESEARCH_ONLY**. The comparator-extension branch head also has no current check runs, so it cannot satisfy the stable/tested promotion doctrine as-is.

### D. Reusable tests/fixtures
Potentially main-eligible after neutral extraction:

- generated events do not update learned transition/association state;
- snapshot/restore round-trip preserves deterministic behavior;
- anonymous interface forbids evaluator context IDs/correct targets;
- event/transcript chronology and external-only validation;
- distribution uniqueness/normalization;
- descriptive resource records remain non-decisional.

Keep research-local:

- CX01 world generators, family-specific expected outputs, G3-G8 qualification thresholds, exact scientific score gates, frozen candidate/package bindings, and result-dependent fixtures.

### Promotion recommendation
If promotion is later authorized, the safest sequence is **one small neutral “comparison substrate” PR** containing only event/distribution primitives, neutral protocol/snapshot contract, and generic invariant tests; then separate optional PRs for resource/privilege/transcript helpers. Do not merge old research branches into `main` wholesale. Reimplement/extract against current `main`, require fresh CI, and keep G3-G8 implementations/taxonomy in research.

## Review of currently open PRs
- **PR #148 — human-directives repository skill:** structurally outcome-independent control-plane helper, one-file, mergeable, observed CI green. **MAIN_ELIGIBLE_FOR_ORDINARY_REVIEW**, but no merge was performed by this Steward run.
- **PR #149 — Git-backed scheduler-registry skill:** structurally outcome-independent control-plane helper, one-file, mergeable, observed CI green. **MAIN_ELIGIBLE_FOR_ORDINARY_REVIEW**, but no merge was performed by this Steward run.

These are independent of the comparator-inventory directive and do not justify bundling promotion work with them.

## Immutable refs / integrity
Verified untouched by Stewardship:

- all 13 legacy `freeze/*` branches;
- C19-v4 evidence tag/object/target;
- C19-R2 evidence tag/object/target;
- PD01 evidence tag/object/target;
- consumed C19-R1/R2 and PD01 STARTED/control/preserve refs;
- prior consumed A01/RV01/RV02/CX identities;
- NI01 prospective research object and its planned unconsumed identity.

Stewardship executed no experiment, dispatched no research workflow, consumed no identity, created no scientific freeze/evidence anchor, merged no research PR, and changed no formal scientific result.

## Deferred governance / next Steward priorities
1. Keep #139 open until authoritative tag namespaces receive server-side protection through an administrative path outside scheduled Stewardship.
2. Do not mass-mirror/delete legacy freeze branches before protected migration semantics exist.
3. Keep NI01 off `main`; after its exact-head CI/preformal success, wait for fresh Evidence Analyst authority rather than inferring formal GO from workflow status.
4. If Control Brain authorizes promotion after this inventory, extract only neutral comparator substrate in small reviewable PRs with fresh current-main CI; do not cherry-pick the old G3-G8 research branches wholesale.
5. Reconcile #148/#149 through ordinary human/repository review; they are structurally main-eligible but non-urgent relative to science.
