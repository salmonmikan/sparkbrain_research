# CX01 Comparator Extension — Implementation-Ready Research Plan

Status: **PLANNING ONLY — implementation not started**  
Branch: `research/cx01-comparator-extension`  
Branch base: `v061-candidate-003-report-20260831@6eed66c88ce5656d761b62c8b9d02b184e699313`  
Historical formal source: `3177c2725f8fc08f23ca5fd2fa9bed4d5845bf5b`  
Historical formal candidate: `v06-confirmatory-candidate-003` — **CONSUMED / NO RERUN**

---

## 0. Purpose

CX01 is an isolated comparator-research track created after the complete v0.6.1 Candidate-003 confirmatory result.

Candidate-003 produced a complete immutable matrix:

```text
400 / 400 executions
3600 / 3600 evidence records
400 / 400 resource records
```

Its frozen scientific decision was:

```text
Primary SparkBrain: unsupported
G3 recurrent:        supported
G4 Assembly:         supported
G5 typed heads:      supported
```

Primary overall success was high, but failed independent frozen gates, most importantly lag-dispersion family performance, minimum selective effect, and the perfect control-contract requirement.

The most important comparator-side finding is that the existing `G3 recurrent` is not a neural RNN/GRU. It is a compact first-order token-to-token transition predictor with retention. Therefore Candidate-003 already shows that a simple explicit transition model can solve the present benchmark more robustly than the frozen Primary.

CX01 must answer the next question:

> Which additional capability, beyond first-order transition statistics, is actually required as the worlds become causally and temporally nontrivial?

CX01 is **not** a rescue attempt for Candidate-003 and must never modify or reinterpret Candidate-003 evidence.

---

# 1. Isolation rules

## 1.1 Branch isolation

CX01 lives only on:

```text
research/cx01-comparator-extension
```

It must not modify protected historical evidence or implementation on:

```text
v06
v061-candidate-003-20260831
v061-candidate-003-report-20260831
v061-timing-contract-correction-20260831
research/rv01-endogenous-transition
archive/*
```

## 1.2 No Candidate-003 reuse as confirmatory evidence

Candidate-003 worlds and results may be read for diagnosis and historical comparison, but:

- no G6/G7/G8 result on Candidate-003 may become confirmatory evidence;
- Candidate-003 seeds `2000..2009` are permanently exposed;
- no parameter may be selected because it improves a Candidate-003 outcome;
- Candidate-003 may be used only for retrospective diagnostics after an implementation is independently fixed.

## 1.3 No Primary modification

CX01 does not change the SparkBrain Primary architecture.

Primary architectural work belongs to RV01 or a later Primary branch. CX01 may define an adapter interface for a future frozen Primary, but it must not implement or tune that Primary.

## 1.4 No result-driven world repair

Worlds, thresholds, scoring, privileges, and tuning rules must be fixed before a fresh formal candidate is opened.

Failures are retained.

---

# 2. Comparator ladder

The comparator set is deliberately incremental. Each stage adds one major capability wherever practical.

```text
G3  first-order transition statistics
 ↓
G6  variable-order / high-order transition statistics
 ↓
G7  high-order sparse temporal memory
 ↓
G8  recurrent spiking temporal memory
```

G4 and G5 remain historical interpretive anchors.

| ID | Comparator | Core capability | Main falsification question |
|---|---|---|---|
| G3 | Frozen first-order transition predictor | `P(next | current)` | Is first-order transition state sufficient? |
| G4 | Explicit Assembly comparator | named sequence state | Is explicit Assembly state sufficient/required? |
| G5 | Typed functional-head comparator | prediction/action/memory/reward heads | Do human-predeclared functional categories explain success? |
| G6 | Variable-Order Markov predictor | high-order context / suffix backoff | Is longer statistical context sufficient? |
| G7 | HTM Temporal Memory comparator | sparse high-order contextual sequence state | Does an established brain-inspired sequence memory suffice? |
| G8-P | Spiking Temporal Memory predictive mode | recurrent spike dynamics + predictive state | Do spiking predictive dynamics suffice without dedicated replay? |
| G8-R | Spiking Temporal Memory replay mode | explicit autonomous replay privilege | Does a dedicated replay mechanism explain endogenous continuation? |

G9 predictive-plasticity SNN, G10 SORN, ESN/reservoir variants, and other comparators are explicitly deferred to CX02/Wave 2.

---

# 3. Frozen G3 anchor

## 3.1 Historical behavior

The historical G3 implementation is retained as an anchor and must not be silently upgraded.

Normative interpretation:

```text
state:     score[source][target]
update:    decay competing targets by retention, then increment observed target
prediction: argmax target score with deterministic tie-break
rollout:   predicted token becomes next source
learning:  external observations only
self-training from generated token: prohibited
```

Historical default:

```text
retention = 0.8
```

## 3.2 Naming

The evidence already calls this condition `g3-recurrent`; historical names are immutable.

CX01 documentation must additionally describe it as:

> first-order autoregressive transition-table comparator

It must not be described as a GRU, LSTM, neural RNN, or reservoir.

## 3.3 G3 anchor tests

Before implementing G6:

- reproduce historical G3 deterministic state update on isolated synthetic fixtures;
- reproduce deterministic tie-break;
- prove generated tokens do not alter learned state;
- prove absent history yields no generated continuation;
- retain exact learned-state serialization behavior where possible.

---

# 4. G6 — Variable-Order Markov Comparator

## 4.1 Scientific purpose

G6 isolates one change relative to G3:

```text
G3: P(next | current token)
G6: P(next | variable-length suffix of observed history)
```

The intended conclusion is not “G6 is a better AI”. It answers:

> Does high-order statistical context alone explain performance that first-order G3 cannot achieve?

## 4.2 Proposed class

```text
VariableOrderMarkovPredictor
```

Proposed source:

```text
src/sparkbrain/comparison/cx01/g6_vomm.py
```

## 4.3 Normative runtime contract

Initial development defaults:

```text
max_order = 8
retention = 0.8
minimum_support = 1
backoff = longest-supported-suffix
self_generated_learning = false
external_observation_only = true
explicit_context_id = false
explicit_episode_label = false
reward = none
assembly = none
typed_head = none
precise_timestamp_use = false
```

The model stores counts/scores over suffix contexts up to `max_order`.

For an observed sequence:

```text
A B C X
```

eligible updates include:

```text
C       -> X
B C     -> X
A B C   -> X
```

up to the configured order.

Prediction uses the longest suffix with eligible support, then backs off deterministically.

## 4.4 Determinism

All ties must use a canonical lexicographic or numeric token order independent of Python hash iteration.

State serialization must be canonical and replayable.

## 4.5 Critical equivalence gate

This is mandatory:

> `G6(max_order=1)` must be behaviorally equivalent to G3 on the shared compatibility fixture.

Required equivalence dimensions:

- emitted tokens;
- learned transition values within exact/declared numeric tolerance;
- observation count;
- generated count;
- intervention behavior;
- serialization/replay;
- no self-learning.

If equivalence cannot be demonstrated, G6 is not accepted as a clean higher-order extension and its interpretation must be weakened.

---

# 5. G7 — HTM Temporal Memory Comparator

## 5.1 Scientific purpose

G7 asks:

> Can an established sparse, context-sensitive, high-order temporal-memory architecture solve the CX01 worlds without SparkBrain Field dynamics?

## 5.2 Scope

Use **Temporal Memory only** for the principal comparator.

Do not include Spatial Pooler in the principal condition because CX01 already provides anonymous discrete external event identities. Adding a learned encoder would introduce another uncontrolled capability.

Pipeline:

```text
anonymous external token
        ↓
fixed anonymous SDR encoder
        ↓
Temporal Memory
        ↓
predictive cells / predicted token set
```

## 5.3 Anonymous SDR encoder

Requirements:

- deterministic;
- label-free;
- no semantic similarity encoded;
- no overlap unless a separate declared ablation explicitly studies overlap;
- encoder map frozen before development scoring.

Initial shape candidate:

```text
active_columns_per_token = 16
cells_per_column = 32
```

These are development candidates, not scientific claims.

## 5.4 Initial algorithm parameters

Development-start values may use conventional HTM-like defaults such as:

```text
activation_threshold
min_threshold
max_new_synapse_count
initial_permanence
connected_permanence
permanence_increment
permanence_decrement
predicted_segment_decrement
```

Exact values must be frozen only after an architecture-fidelity phase that does not use formal CX01 held-out results.

## 5.5 Fidelity gate before benchmark integration

Before G7 may enter CX01 development worlds, it must pass independent sequence-memory tests.

Required canonical fixture:

```text
A B C X
D B C Y
```

After training, context must support:

```text
A B C -> X
D B C -> Y
```

Additional fidelity tests:

- branching prediction;
- unexpected-input reset/burst behavior as defined by the selected TM specification;
- no semantic label leakage;
- deterministic checkpoint/restore;
- prediction does not count as external observation.

## 5.6 Implementation provenance

Preferred approach:

- implement the algorithm independently from published specification;
- cite exact source specification and parameter provenance;
- do not copy incompatible-license implementation code into SparkBrain;
- if implementation differs materially from canonical HTM TM, call it `HTM-inspired Temporal Memory`, not `HTM Temporal Memory`.

Naming is gated by fidelity evidence.

---

# 6. G8 — Spiking Temporal Memory Comparator

## 6.1 Scientific purpose

G8 asks two separate questions:

1. Can recurrent spiking predictive dynamics solve the task?
2. Is a dedicated replay-mode privilege required for autonomous continuation?

Therefore G8 is intentionally paired.

```text
G8-P prediction mode
G8-R replay mode
```

Both share one learned network state where the reference architecture permits this.

## 6.2 G8-P

Prediction condition:

- recurrent spiking dynamics;
- structural/local synaptic learning according to the selected reference model;
- inhibition/homeostatic behavior as required for fidelity;
- no global replay-mode switch;
- no generated-event self-confirmation;
- no scalar reward;
- no semantic label.

## 6.3 G8-R

Replay condition may explicitly use a dedicated replay privilege if the reference model requires it.

Privilege declaration must include:

```text
dedicated_replay_mode = true
global_excitability_switch = true|false   # exact implementation value
plasticity_during_replay = true|false     # exact implementation value
```

The difference between G8-P and G8-R must be reported as architecture evidence, not hidden as tuning.

## 6.4 Fidelity rule

Do not label a lightweight spike simulator as canonical `Spiking Temporal Memory` unless independent fidelity tests reproduce the reference behavior used for the scientific comparison.

If exact reproduction is impractical in the local-first environment, use:

```text
G8 = sTM-inspired recurrent spiking comparator
```

and preserve that weaker name in all claims.

## 6.5 Minimum fidelity tests

Before integration:

- stable sparse sequence-specific activity;
- context-sensitive branch discrimination;
- prediction before expected external continuation;
- autonomous replay only under the declared replay condition if required;
- replay does not train itself unless explicitly part of the reference algorithm;
- deterministic seeded reproduction within the simulator's declared numerical policy;
- checkpoint/restore equivalence.

---

# 7. Common CX01 architecture interface

Comparator adapters should receive the least privileged common event interface possible.

Preferred conceptual interface:

```text
observe_external(event)
advance(time)
generate()
intervene(handle)
snapshot()
restore()
```

A common external event contains only execution-level information required by the world contract:

```text
token_id
timestamp
event_origin = external
optional boundary direction
```

The adapter must not receive:

- correct next token;
- evaluator target;
- branch winner;
- semantic role;
- action label;
- memory label;
- reward unless the comparator explicitly declares that privilege;
- hidden world-state label;
- a convenient context ID that directly separates ambiguous histories.

If episode boundaries are supplied for practical reset semantics, this is a declared privilege and must be identical across comparable conditions.

---

# 8. Shared training schedule

The balanced chronological schedule introduced during v0.6 remains the conceptual default because the original development experiment showed that presentation order can create false architecture differences.

CX01 schedule requirements:

- architecture independent;
- branch exposures interleaved by round;
- traversal order alternates where appropriate;
- identical world event chronology across architectures;
- no comparator-specific reordering;
- schedule hash recorded;
- schedule frozen before held-out execution.

If an architecture requires dense continuous simulation between events, it receives the same external timestamps, not an alternate event order.

---

# 9. CX01 world families

The previous five v0.6 families remain historical evidence, but CX01 requires worlds where the discriminating architectural property is actually necessary.

CX01 Wave 1 defines six new families.

---

## 9.1 CX01-HO — High-Order Aliasing

Purpose:

> Separate first-order statistics from true history-conditioned prediction.

Canonical structure:

```text
A -> B -> C -> X
D -> B -> C -> Y
```

The current local transition `C -> ?` is ambiguous.

World-generation requirements:

- token frequency balanced so marginal frequency cannot reveal the answer;
- terminal targets balanced across seeds;
- no hidden context ID;
- current token and short suffix intentionally aliased;
- branch presentation order balanced.

Expected diagnostic pattern, not a pass requirement:

```text
G3: expected limitation
G6/G7/G8: capable in principle
```

Hard leakage check:

> A first-order oracle using only the same legal G3 information must not exceed the preregistered ambiguity ceiling.

---

## 9.2 CX01-TIME — Timing Aliasing

Purpose:

> Determine whether precise temporal structure provides useful information beyond token order.

Canonical structure:

```text
A -- short --> B -- long  --> C -> X
A -- long  --> B -- short --> C -> Y
```

Token order is identical. Timing differs.

Requirements:

- identical token sequence across alternatives;
- matched total sequence duration where possible, so one scalar duration is insufficient;
- timing pattern, not token identity, determines the target;
- timestamp-blind oracle must be at chance/ambiguity ceiling;
- no branch ID leak.

Comparator privilege interpretation:

```text
G3: timestamp blind
G6: timestamp blind in principal condition
G7: timestamp blind in principal condition
G8: precise-time capable
Future Primary: precise-time capable if its frozen contract permits it
```

Optional secondary ablations may give discretized timing bins to G6/G7, but they are separate conditions and must not replace the principal comparison.

---

## 9.3 CX01-CYCLE — Rapid Contingency Cycling

Purpose:

> Isolate reversal, forgetting, reacquisition, and re-entry under repeated changing relations.

Example:

```text
X -> Y -> X -> Z -> Y -> X
```

Requirements:

- cumulative historical majority must eventually conflict with current contingency;
- phase lengths vary independently of target identity;
- no explicit phase ID supplied;
- old relation recurrence included;
- short enough phases to expose inertia but long enough for at least one architecture to reacquire on development fixtures.

Primary metrics:

- contradiction-to-revision latency;
- reacquisition latency;
- stale-relation emission count;
- re-entry success after reacquisition;
- catastrophic overwrite / inability to return to an older relation.

Do not reduce this family to final-state top-1 accuracy.

---

## 9.4 CX01-BRANCH — Ambiguous Future Distribution

Purpose:

> Distinguish architectures that preserve multiple plausible futures from those that collapse immediately to one argmax path.

Example exposure:

```text
A B C X  x6
A B C Y  x5
A B C Z  x4
```

Required outputs may be architecture-neutral predicted-support/probability projections.

Metrics:

- top-1 correctness;
- negative log likelihood where calibrated probability is available;
- Brier score where probability is available;
- support recall for plausible branches;
- false support;
- branch-collapse index.

Architectures without native probabilities may expose normalized deterministic support scores through an observer adapter; this transformation must be frozen and cannot feed back into runtime.

---

## 9.5 CX01-SELECT — Selective Causal Interference

Purpose:

> Directly address the Candidate-003 failure where targeted and matched interventions were equally destructive in several lag-dispersion worlds.

Construct shared and disjoint causal paths with enough redundancy to distinguish local/selective damage from global collapse.

Required intervention groups:

```text
sham
targeted
matched-random or matched-control
disjoint-control-path
```

Primary effect:

```text
selective_effect = targeted_impairment - matched_impairment
```

Principal hard gate candidate:

```text
selective_effect >= 0.50
```

Exact threshold is preregistered before formal candidate generation.

Collateral damage is always retained as a separate metric.

---

## 9.6 CX01-LOOP — Reality / Provenance Loop

Purpose:

> Ensure internally generated predictions or replay events cannot become their own confirming evidence.

Structure:

```text
external history
      ↓
internal generation
      ↓
optional boundary/world effect
      ↓
new external event
      ↓
learning/revision
```

Integrity rule:

```text
internal generation != external observation
```

Hard gates:

- self-confirmation violations = 0;
- generated output alone cannot increase externally confirmed relation strength;
- contradiction must remain authoritative;
- provenance survives rollout/replay/boundary translation.

For G3/G6/G7/G8, this is primarily an adapter and learning-authority integrity assay.

---

# 10. World identifiability audit

Before any comparator is scored on development worlds, each family requires a pre-execution analytical or synthetic leakage audit.

Required checks include:

- HO cannot be solved above ceiling by first-order token state;
- TIME cannot be solved above ceiling without time information;
- CYCLE cannot be solved by global historical majority alone across the whole stream;
- BRANCH contains genuine multi-target support;
- SELECT targeted and matched intervention handles are exposure- and scale-matched;
- LOOP internal and external provenance are never conflated by the evaluator.

A world family that fails its identifiability audit is invalid even if SparkBrain performs well on it.

---

# 11. Fairness contract

## 11.1 Shared external evidence

Every architecture receives identical external event identities and chronology unless an architecture-specific privilege is explicitly declared.

## 11.2 Same exposure budget

Training exposures are identical by path/event count.

Architecture-internal computation may differ and is measured descriptively.

## 11.3 No architecture-specific task hints

Adapters cannot translate a world into architecture-specific correct answers.

Permitted translation is only representational, e.g. token -> fixed SDR for G7.

## 11.4 Development tuning boundary

Architecture tuning may use only declared development fixtures/seeds.

The tuning procedure itself is frozen:

- parameter search space;
- objective;
- tie-break;
- maximum trials;
- selected configuration.

Formal candidate results cannot trigger retuning.

## 11.5 Failure parity

Crash, nonfinite state, schema violation, privilege mismatch, and incomplete execution are execution failures under common policy.

---

# 12. Privilege inventory

CX01 extends privilege disclosure beyond v0.6.

Proposed architecture metadata:

```text
uses_explicit_assembly_state
uses_typed_functional_heads
uses_scalar_reward
uses_high_order_context
uses_precise_timestamps
uses_explicit_episode_segmentation
uses_external_readout
uses_global_mode_switch
uses_dedicated_replay_mode
self_generated_learning
prediction_reinjected_into_runtime
external_confirmation_required_for_positive_commit
generation_mechanism
```

Proposed generation mechanism enum:

```text
none
transition_autoregression
context_autoregression
predictive_state_readout
same_rule_recurrent_dynamics
dedicated_replay_mode
```

Privilege metadata is interpretive and integrity-critical, not a capability score bonus/penalty.

---

# 13. Resource accounting

Reuse the v0.6 normalized principle:

> Resource measurements are descriptive and do not alter capability pass/fail unless a future protocol explicitly preregisters a resource question.

Common measurements:

```text
wall clock
process CPU
peak traced memory
canonical execution bytes
external observations
internal generated events
mutable state entries
parameter/state entries
intervention count
```

Additional architecture descriptors:

```text
spike count
synaptic event count
active sparse cells
predictive sparse cells
context-node count
replay-mode activations
```

These architecture-specific counters must never be compared as if one unit were inherently equivalent to another architecture's event.

---

# 14. Scoring policy

CX01 must not allow a strong easy family to average away a failure on the exact capability under investigation.

Therefore family-specific hard gates are primary.

Proposed gate families:

| Family | Principal hard gate |
|---|---|
| HO | high-order discrimination above first-order ambiguity ceiling |
| TIME | timing-conditioned discrimination above timestamp-blind ceiling |
| CYCLE | bounded revision + reacquisition + re-entry criteria |
| BRANCH | branch support/distribution fidelity criterion |
| SELECT | selective causal effect threshold |
| LOOP | zero self-confirmation violations |

Secondary aggregate metrics:

- overall domain success;
- minimum family success;
- confidence/calibration metrics;
- resource descriptors.

Exact numerical thresholds are fixed after development qualification and before fresh candidate generation.

No threshold may be changed after formal candidate opening.

---

# 15. Experimental phases

CX01 is split into four evidence levels.

## Phase A — Architecture fidelity

No SparkBrain comparison claim.

Goals:

- G3 anchor validated;
- G6 order-1 equivalence validated;
- G7 canonical TM behavior validated;
- G8 canonical or explicitly `-inspired` behavior validated.

## Phase B — Development qualification

Use only development seeds with no overlap with historical or future formal candidate seeds.

Goals:

- adapter correctness;
- world identifiability;
- fairness;
- privilege disclosure;
- metric validity;
- intervention validity;
- parameter-freeze selection.

Any defect found here may be repaired and rerun because this is development-only.

## Phase C — Comparator freeze

Freeze:

- source SHA;
- comparator implementations;
- dependency versions;
- parameter configs;
- encoder maps/policy;
- event contract;
- world-generation algorithm;
- schedule;
- scoring;
- privileges;
- resource schema;
- artifact schema;
- candidate generation salt/range;
- execution command;
- artifact paths.

No capability run occurs before freeze.

## Phase D — Fresh formal comparison

Formal execution requires a fresh, disjoint candidate generation.

The final matrix should include the then-frozen Primary revision plus the comparator set selected by the protocol.

Candidate-003 is never reused.

One-way execution and no-rerun policy remain the preferred standard.

---

# 16. Candidate and seed policy

Reserved/exposed ranges include at least:

```text
100..109    historical qualification
1000..1009  retired candidate-002
2000..2009  consumed candidate-003
```

CX01 development and future formal seeds must be disjoint from all exposed ranges.

Suggested namespace strategy:

```text
CX01 development: dedicated high-range explicit IDs
CX01 formal:      generated only after freeze with a new salt and new range
```

Do not reserve the final formal seed range in executable world code until the protocol is ready to freeze unless required for schema-only construction.

---

# 17. Proposed source layout

CX01 must not grow inside `v06_*` confirmatory modules.

```text
src/sparkbrain/comparison/cx01/
    __init__.py
    contract.py
    events.py
    schedule.py
    worlds.py
    scoring.py
    interventions.py
    resources.py
    privilege.py

    g3_anchor.py
    g4_anchor.py
    g5_anchor.py
    g6_vomm.py
    g7_htm_tm.py
    g8_spiking_tm.py

    adapters.py
    fidelity.py
    development.py
    candidate.py
    freeze.py
```

Tests:

```text
tests/cx01/
    test_contract.py
    test_events.py
    test_worlds.py
    test_world_identifiability.py
    test_schedule.py

    test_g3_anchor.py
    test_g6_vomm.py
    test_g6_g3_equivalence.py

    test_g7_fidelity.py
    test_g7_high_order.py

    test_g8_fidelity.py
    test_g8_prediction.py
    test_g8_replay.py

    test_privilege.py
    test_interventions.py
    test_resources.py
    test_scoring.py
    test_freeze.py
```

Documents:

```text
docs/CX01_COMPARATOR_EXTENSION_PLAN.md
docs/CX01_COMPARATOR_PRIVILEGE_MATRIX.md
docs/CX01_PRIOR_ART.md
docs/CX01_DEVELOPMENT_REPORT.md
```

---

# 18. Implementation work packages

## CX01-00 — Protocol and source binding

Deliver:

- this plan accepted;
- Candidate-003 formal result pinned as historical motivation;
- branch/base/SHA binding documented;
- protected historical paths defined;
- non-goals and claim boundary frozen for implementation phase.

Acceptance:

```text
no runtime code added
no historical evidence modified
```

## CX01-01 — Common contract + six world families

Implement:

- common events;
- schedule;
- six world generators;
- identifiability audit;
- result schema;
- privilege schema draft.

Acceptance:

- deterministic reconstruction;
- no hidden labels;
- family-specific leakage tests pass;
- no comparator capability implementation required yet.

## CX01-02 — Frozen G3 anchor

Implement an adapter around historical G3 behavior without changing its algorithm.

Acceptance:

- compatibility fixtures pass;
- state/output deterministic;
- no self-training;
- canonical serialization.

## CX01-03 — G6 VOMM

Implement variable-order comparator.

Acceptance:

- `max_order=1` equivalence with G3;
- high-order canonical fixture passes at `max_order>1`;
- no timestamp use;
- no hidden context ID;
- no generated-event learning.

## CX01-04 — G7 fidelity implementation

Implement independent HTM TM or explicitly HTM-inspired equivalent.

Acceptance:

- canonical contextual alias fixture passes;
- branching behavior validated;
- deterministic checkpoint/restore;
- naming decision recorded from fidelity evidence.

## CX01-05 — G8 fidelity implementation

Implement canonical or explicitly inspired recurrent spiking temporal comparator.

Acceptance:

- prediction-mode fidelity tests;
- replay-mode fidelity tests;
- mode-switch privilege explicit;
- no hidden self-confirmation;
- deterministic seeded reproduction policy.

## CX01-06 — Development matrix

Run only development worlds.

Goals:

- validate all six families;
- find implementation/fairness defects;
- verify comparator adapters;
- validate interventions;
- collect resource descriptors.

Results are development-only and may trigger implementation fixes.

## CX01-07 — Fairness and privilege audit

Independent review of:

- input parity;
- exposure parity;
- timestamp privilege;
- episode-boundary privilege;
- replay-mode privilege;
- hidden context leakage;
- evaluator leakage;
- adapter transformations;
- intervention matching.

Any unresolved privilege mismatch blocks freeze.

## CX01-08 — Resource normalization + artifact contract

Finalize:

- resource schema;
- deterministic execution IDs;
- result records;
- raw artifact layout;
- checksums;
- atomic writes;
- partial-failure semantics.

Resource efficiency remains descriptive-only for Wave 1.

## CX01-09 — Fresh candidate generator

Only after comparator development is fixed.

Create:

- fresh RNG salt;
- disjoint seeds;
- new topology/token permutations;
- new timing values;
- new contingency schedules;
- schema-only candidate declaration.

No capability adapter may execute candidate worlds before freeze.

## CX01-10 — Freeze and seal

Bind:

- exact source SHA;
- dependency lock/environment;
- world grid;
- schedule;
- scoring;
- comparator inventory;
- privilege matrix;
- resource schema;
- result schema;
- execution command;
- output paths;
- independent approval.

Then cross:

```text
──────────── NO-CHANGE BOUNDARY ────────────
```

## CX01-11 — Formal comparison

Execute once against the fresh candidate generation.

Requirements:

- immutable raw evidence first;
- scoring only after raw lock;
- no same-candidate rerun;
- retain all Primary failures and comparator successes;
- retain all comparator failures and Primary successes;
- no post-hoc rescue.

---

# 19. Implementation sequencing

Normative order:

```text
CX01-00 plan
   ↓
CX01-01 contract/worlds
   ↓
CX01-02 G3 anchor
   ↓
CX01-03 G6
   ↓
CX01-04 G7 fidelity
   ↓
CX01-05 G8 fidelity
   ↓
CX01-06 development
   ↓
CX01-07 fairness audit
   ↓
CX01-08 resource/artifact contract
   ↓
CX01-09 fresh candidate
   ↓
CX01-10 freeze/seal
──────── no-change boundary ────────
CX01-11 one-way formal run
```

G7/G8 implementation may proceed in parallel only after CX01-01 common contracts are stable.

G6 should be implemented first because it provides the cleanest extension of already-supported G3 and establishes whether higher-order statistics alone explain the next benchmark tier.

---

# 20. Branch policy during implementation

Current planning branch:

```text
research/cx01-comparator-extension
```

Optional implementation subbranches after CX01-01 contract freeze:

```text
research/cx01-g6-vomm
research/cx01-g7-htm
research/cx01-g8-stm
```

If parallelized:

- all branch from the same CX01 contract checkpoint;
- no branch edits another comparator's implementation;
- common-contract changes require rebasing all comparator branches before further scientific execution;
- development artifacts never merge into formal candidate source unless explicitly reviewed.

Do not merge CX01 into RV01.

Do not rebase historical v0.6/v0.6.1 evidence branches onto CX01.

---

# 21. Definition of Ready for implementation

Implementation may begin when all are true:

- [x] dedicated CX01 branch exists;
- [x] Candidate-003 result is treated as immutable historical evidence;
- [x] G3 is correctly classified as first-order transition-table anchor;
- [x] G6/G7/G8 scientific roles are distinct;
- [x] six discriminating world families are specified;
- [x] no formal Candidate-003 reuse is permitted;
- [x] fairness and privilege principles are specified;
- [x] implementation order is specified;
- [ ] plan receives review acceptance;

No runtime implementation is included in CX01-00.

---

# 22. Definition of Done for Wave 1

CX01 Wave 1 is complete only when:

1. G3 anchor behavior is preserved;
2. G6 order-1 equivalence is demonstrated;
3. G6 high-order capability is fidelity-tested;
4. G7 naming/fidelity is justified;
5. G8 prediction/replay distinction is explicit and fidelity-tested;
6. all six world families pass identifiability audits;
7. comparator privileges are fully disclosed;
8. common schedule and exposure fairness are verified;
9. resource/accounting artifacts are complete;
10. development-only outcomes are preserved separately;
11. formal candidate generation is disjoint from all exposed seeds;
12. a freeze/seal boundary exists before formal execution;
13. one-way fresh formal evidence is retained without post-hoc rescue.

---

# 23. Claim boundaries

Even if CX01 comparators outperform or underperform a future Primary, Wave 1 alone does not establish:

- human-like cognition;
- semantic understanding;
- biological equivalence;
- consciousness;
- AGI;
- general superiority over neural networks;
- physical energy efficiency.

Permitted interpretation is narrower:

> Under controlled anonymous temporal worlds, the comparator ladder identifies which classes of statistical context, sparse temporal memory, and spiking/replay dynamics are sufficient or insufficient for the preregistered causal and temporal tasks relative to the frozen Primary revision.

---

# 24. Immediate next task

Upon review acceptance, start **CX01-01 only**:

```text
common event contract
six deterministic development world families
world identifiability audit
shared schedule contract
result/privilege schema skeleton
```

Do **not** implement G6/G7/G8 until CX01-01 is reviewed, because comparator code should bind to one stable common contract rather than drive the benchmark design.
