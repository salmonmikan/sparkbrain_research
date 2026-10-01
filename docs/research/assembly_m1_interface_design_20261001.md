# A minimal temporal representation inlet for M1

Date: 2026-10-01 UTC. **DESIGN / SOURCE AUDIT / NONCANONICAL / NON_EVIDENTIARY**.
Scientific credit: **0**. No model, fixture stream, or runtime test was executed here.

## Decision

The smallest plausible connection is a **bounded temporal-feature adapter before
`IntegratedM1Pilot.observe`**. It supplies the same history-derived feature vector to
M1's predictive context and its scope router. M1 continues to own prediction, action,
receipt identity, selective outcome updates, and the predictive/scope agreement gate.
Merely displaying v0.5 activations or copying its action into `reference_action` cannot
make assemblies contribute to the present M1 action rule.

This is an interface proposal, not a recommendation to deploy v0.5. The completed
[PR #169 diagnostic](temporal_reuse_loop_results_20261001.md) failed its prospective
integration-proposal gate: both raw-history alternatives beat S on both suffixes in
both seeds, and freezing weight/delay learning had lower Brier in all four comparisons.
Its initial recall and suppression effects establish narrower acquired-path dependence,
not incremental predictive benefit. This proposal does not overturn that decision.
It identifies the minimal connection and the first test that could reveal whether the
connection actually affects outputs; comparative usefulness remains a later question.

The initial adapter deliberately freezes acquired prototypes and model parameters.
M1's outcome associations continue learning. This is **frozen acquired features plus
online predictive/scope revision**, not online field-learning integration or an
independently persisting post-cue memory result.

## Scope, authority, and fixed sources

Source pin: `ff51abdc7f1f8ae777a9536494cd83d29b4bb769` (merged PR #169).
Human Directive index read from `ops/human-directives`, head
`8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, index blob
`1ba1e173344f36e14d0e21e6f3e823254e031f7d`.
[HUMAN-20260928-001](https://github.com/salmonmikan/sparkbrain_research/blob/ops/human-directives/ops/human_directives/history/2026-09-28/HUMAN-20260928-001-accelerated-integrated-sparkbrain-completion.md)
prioritizes the observation–state–selection–action–outcome–revision loop and its interface gaps.

This is separately requested cloud research, not an invocation of a scheduled role or
an allocated SYSTEM_BUILD milestone. AGENTS, common policy, scientific-integrity policy,
the active directive index, the integration directive, and current integration boundaries
were read. No scheduler/control state, role-owned PR #164, current plasticity experiment,
checkpoint experiment, shared status/claim/result ledger, historical acceptance, or
FORMAL/immutable identity is a write target. Runtime source and defaults remain unchanged.

## 1. Audited dataflow and the exact missing edge

All source links below use the fixed source pin; they describe source, not measured behavior.

| Existing edge | Source trace | Consequence |
|---|---|---|
| M1 observation to predictive context | [`_sensory_sample`, `observe`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/system_build/integrated_m1.py#L277-L285); [`_sample_context`, `_candidate_views`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/system_build/predictive_revision.py#L213-L250) | Sorted sensory scalars become nearest-prototype context; maximum 64 scalars and fixed channel schema |
| Wrapped v0.3.2 to diagnostics | [`PredictiveRevisionPilot.observe`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/system_build/predictive_revision.py#L252-L300) | `reference_action` is returned, but predictive-bank candidates determine pilot prediction |
| Two decision branches to actual action | [`IntegratedM1Pilot.observe`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/system_build/integrated_m1.py#L391-L450) | Predictive sign must agree with the scope candidate; otherwise abstain |
| Later receipt to both learned associations | [`apply_outcome`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/system_build/integrated_m1.py#L452-L537); [`feedback`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/system_build/predictive_revision.py#L362-L430) | One pending observation; exact receipt binding; predictive revision and scope revision commit together |
| Feature content to scope integrity | [`CausalScopeRevisionPilot.step`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/system_build/causal_scope_revision.py#L540-L660) | Exact feature content remains bound to a candidate; conflicting outcome sign is rejected |
| Pulses to v0.5 assemblies | [`process_episode`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/v05/brain.py#L132-L245) | Stateful receptors/field produce patterns and mature activations; strongest selection precedes prediction/action |
| v0.5 later association | [`learn_outcome`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/v05/brain.py#L247-L263) | Predictor counts and optional action reward update the current pending activation, without M1 receipt semantics |

**Missing edge:** no v0.5 representation crosses into either `M1Observation.sensory_values`
or `routing_features`. There is no shared adapter clock, coordinate manifest, pending-query
binding, or joint M1/v0.5 transaction. M1's existing session/checkpoint manager owns a fixed
world and two existing components; it does not already save an added temporal backend.

Adding temporal features only to sensory values leaves scope routing aliased. Adding them
only to routing leaves predictive context aliased. The proposed explicit duplication is
one representation entering two consumers, not two independent evidence sources.

## 2. Proposed typed boundary

These types are a **specification**, not implemented APIs. The accompanying
[JSON contract](../../artifacts/research/assembly_m1_interface_20261001/interface_contract.json)
is inspectable design data, not an executable experiment or validation certificate.

```python
@dataclass(frozen=True)
class CausalWindow:
    occurrence_id: str             # opaque key, excluded from new context features
    start_ms: int
    input_cutoff_ms: int
    decision_ms: int
    pulses: tuple[SignalPulse, ...] # observed inputs only, metadata empty
    current_values: tuple[tuple[str, float], ...]
    current_route: tuple[float, ...]

@dataclass(frozen=True)
class TemporalContext:
    dictionary_digest: str         # audit/binding only, never a feature
    coordinate_schema: str         # fixed for the lifetime of one M1 instance
    input_cutoff_ms: int
    decision_ms: int
    features: tuple[float, float]  # finite values in [0, 1]
    status: Literal['matched', 'no_match']
    backend_state_digest: str      # audit only; not proof of complete state

@dataclass(frozen=True)
class PendingBinding:
    occurrence_id: str
    raw_window_digest: str
    adapted_observation_digest: str
    dictionary_digest: str
    action: M1Action
    decision_ms: int

class TemporalContextBackend(Protocol):
    def advance(self, window: CausalWindow) -> TemporalContext: ...
    def inspect(self) -> object: ...  # pure; no stepping/counters/learning
```

The coordinator, not the backend, owns occurrence IDs, receipts, serial processing,
clock validation, pending binding, transaction rollback, and capacity enforcement.
The backend sees an opaque occurrence ID only when the v0.5 maturity bookkeeping API
requires it; numeric order, text, hashes, source IDs, receipt IDs, and dictionary digests
must never be encoded in the new temporal features, predictive-bank context or scope
vector. Renaming IDs with their ledger references must preserve those representations,
predictive/scope numeric state and M1 prediction/action, when the reference step completes.
This deliberately does not assert identity-neutrality for the entire existing runtime.

**Pre-existing exception discovered in review:** M1 forwards `event_id` as
`SensorySample.sample_id` without text metadata. The default wrapped I1 reference path
uses `text or sample.sample_id` as frontend content and derives a belief key from it
([`_interpret`](https://github.com/salmonmikan/sparkbrain_research/blob/ff51abdc7f1f8ae777a9536494cd83d29b4bb769/src/sparkbrain/v03/runtime.py#L613-L633)).
Different opaque ID text can therefore change reference belief grouping and state.
The reference action is unused by M1's action selector, but the reference step still runs
and can fail. Compare and report reference-state differences separately, and do not claim
whole-loop failure equivalence or global ID exclusion. Establishing a globally identity-neutral
reference path requires a separately scoped runtime contract change; this design does not
quietly substitute IDs, add text metadata, or bypass that path.

### Fixed representation coordinates

- K is exactly 2 in this first design. Acquisition uses permitted unlabeled history only.
  At freeze there must be exactly two mature candidates, with distinct canonical prototype
  content; otherwise stop `dictionary_ineligible`. No outcome-based selection or retry.
- Slot order is lexicographic canonical prototype content
  `(ordered_units, relative_bins, unit_ids, spike_count, source_kind)`. Exclude assembly,
  pattern, cascade and occurrence IDs and absolute times from ordering. Save the two
  slot-to-candidate bindings and full prototype hashes. Never recycle slots or silently
  reload an incompatible dictionary into an already trained M1.
- Extract the same strongest mature, non-suppressed activation as current v0.5 uses:
  maximum `(similarity, episode_count, assembly_id)`. `brain.pending_activation` is the
  existing carrier; verify its agreement with returned activations. Numeric assembly IDs
  are not coordinates. Native tie-breaking can depend on ID names; the first design
  therefore rejects a tie on `(similarity, episode_count)` before using an ID tie-break.
  Also audit every accepted pattern's native `best_match` against all frozen candidates,
  including immature candidates: equal best similarities can be resolved by assembly ID
  before an activation reaches the strongest selector. Reject these matching ties too.
  ID-renaming invariance is required on accepted windows; ties are a reported limitation.
- If strongest matches slot j, set `z[j] = similarity` and the other coordinate to zero.
  No mature usable activation gives `(0, 0)` and `no_match`. All-zero context is not a
  fabricated confident prediction and does not itself override M1's action rule.
- Freeze acquisition, field learning and homeostatic learning after the prefix:
  `process_episode(..., learn_assembly=False, learn_field=False, metadata={})`;
  construct the backend with `enable_prediction=False`, `enable_action=False`, and
  `enable_reward_modulation=False`. Do not call `learn_outcome`. Receptor, field,
  cascade and queue state still evolve; this is not a stateless transform.
- This deliberately retains strongest-selection limitations rather than adding a new
  pooling/readout mechanism to rescue the negative result. It does not measure the
  separate ongoing weight/delay experiment.

### The actual connection

With fixed, collision-checked channel names `temporal_0` and `temporal_1`:

```text
adapted.sensory_values = original current_values + {temporal_0: z0, temporal_1: z1}
adapted.routing_features = original current_route concatenated with (z0, z1)
adapted.event_id = occurrence_id
adapted.time = decision_ms / 1000
```

The original features are preserved, not overwritten. Their scale is prospectively fixed;
no epsilon, receipt digest, counter, label, regime flag, or post-outcome correction is added.
The physical-time adapter explicitly declares M1 time in seconds and v0.5 time in ms;
current M1 only validates nonnegative numeric time, so the coordinator enforces the conversion.
Two added route dimensions leave at most six original dimensions; two added sensory scalars
leave at most 62 originals. Fail before mutation if either cap or channel schema is violated.
No default threshold, evidence strength, candidate-sign mapping, router capacity or gate changes.
Start a **fresh M1 instance** with this expanded schema before its first observation;
`_sample_context` rejects a changed channel set, so this is not hot-pluggable into a
previously trained M1 instance. Migration of old associations is out of scope.

K=2 representation coordinates do not expand SB002's two-component capacity. Two original
regions crossed with two history contexts may need four joint regions and therefore fail.
The initial sentinel holds original features constant to isolate the wire. A real producer
test must record joint-region capacity failures rather than silently removing original
features, compressing labels into a coordinate, or increasing router capacity.

This change would expand input access from current features to declared causal history.
A future experiment must compare all arms under that expanded access; it cannot call the
change an improvement under the old current-only information contract.

## 3. Clock, delayed outcomes, and mutation ownership

The first adapter is **one fixed decision window at a time**, not an event-by-event API.
Raw pulse order is explicit; all pulses are at or before `input_cutoff_ms`. Pulse time,
channel, magnitude, polarity and optional location come from the permitted observation
stream. Use constant `source_id="temporal-input"`, empty metadata, and zero `novelty` and
`prediction_error`; those modulation fields must not smuggle evaluator feedback into the
field. The model may
settle internal dynamics after that cutoff, but no new external input is provided between
cutoff and `decision_ms`. Require the returned v0.5 `end_ms` to equal `decision_ms`; never
silently retime a late computation. The next window starts strictly after the prior
committed receipt time. One unresolved occurrence is permitted, matching current M1.

The coordinator accepts a separate envelope `(M1OutcomeReceipt, delivered_ms)` only after
`delivered_ms > decision_ms`. M1's receipt itself has no delivery timestamp. Delivery time
is audit/ordering data, not a context feature. The current outcome is unavailable to either
representation or M1 before its action; evaluator targets live outside these inputs.

| Transition | Permitted writes | Required stop/rollback |
|---|---|---|
| Prepare next window, no pending event | Coordinator validation only | Reject late/future pulses, malformed values, reused event ID or schema drift before mutation |
| Advance then `M1.observe` | Backend causal state; M1 observation state; one pending binding | Commit all three or restore all three to the pre-window state |
| Later receipt | M1 predictive/scope associations and receipt ledger; clear pending binding on commit | On rejection retain the exact pending state; no backend update, no new feature extraction |
| Identical committed receipt replay | Return previous M1 revision | No clock advance, new backend step or second learning weight |
| Conflicting/unknown receipt | None | Fail closed; do not switch to a fresh ID to bypass the conflict |
| Correction or out-of-order unresolved events | None | Unsupported by this version; require a separate supersession/multipending contract |
| Inspect/render | None | Outputs and operational state unchanged |

The exact feature vector used to predict is retained for outcome learning. It is never
recomputed after feedback. Outcome sign still maps to alpha/beta in existing M1.
If identical complete `(raw route, z)` content later needs the opposite candidate,
SB002 still returns `identical_observation_conflict`; retain that negative case. History
features can separate genuinely different observed histories, but cannot legitimize an
arbitrary context split or solve stationary stochastic conflicting outcomes.

### Transaction and persistence blocker

A wrapper cannot claim atomicity merely because M1 is transactional. Its snapshot must
also cover the backend's complete live state, dictionary, buffers, clocks and pending binding.
Native v0.5 checkpoint state omits transient cascade/burst caches and may reorder outgoing
edges on restoration; [PR #169](temporal_reuse_loop_contract_20261001.md#restricted-checkpoint-eligibility)
allowed only inspected quiet boundaries. `state_hash()` does not detect everything omitted.

For a future first wiring test, use independently reconstructed in-process prefixes/forks,
not unverified native v0.5 checkpoint forks. Before publishing a reusable adapter, demonstrate
exact complete-state clone/rollback and cold continuation, or restrict transaction boundaries
prospectively and fail closed when ineligible. This document does not specify a silent new
checkpoint format or authorize changes to the active checkpoint workstream. If complete
rollback cannot be provided without a runtime contract change, stop before integration.

## 4. Backend interchangeability without unfair privilege

The common boundary carries two bounded temporal features, never a direct action or label.
Use the identical M1 compositor/config, raw current features, adaptation code, outcome timing,
and ledger rules for all arms. Train each arm's M1 associations on the same permitted prefix;
do not transfer assembly-trained M1 prototypes to a differently encoded comparator and call
its resulting failure a performance comparison.

- **Zero context:** `(0, 0)` in both consumers, same original current inputs. It is an
  information-limitation control and may reject contradictory outcomes; report that.
- **Recent raw-history representation:** a fixed-budget history encoder of the same allowed
  pulses and times, with a two-coordinate output chosen without target access.
- **Retained raw prototypes:** an outcome-blind two-prototype history matcher with the same
  query cutoff and fixed output schema. This is the important reuse-capable replacement.
- **Acquired assemblies:** the exact frozen feature rule above.

Equal output width is not equal resources. Account separately for acquisition work,
backend live state, raw-history storage, dictionaries, M1 state, identity ledgers and all
copies used for forks. Stop at common predeclared byte/work/time limits. A restricted K=2
adapter does not inherit the PR #169 H/R algorithms or their measured performance.
Those remain serious prior alternatives, not implemented baselines in this design.

## 5. Smallest future test that answers the interface question

**No test below was executed. No seeds, inputs, runtime runner or scientific identity are
allocated by this design.** A fresh bounded offline implementation/fixture freeze and
applicable authority must precede execution. Do not reuse PR #169 suffixes as fresh evidence.

### A. Consumer wiring sentinel: can context actually change M1 output?

Build one public-API M1 prefix with original `current_values=(("signal", 0.0),)` and
`current_route=(0.0,)` throughout, default M1 component configs, two sentinel context
vectors `(1, 0)` and `(0, 1)`, and later outcomes `+1` and `-1`, respectively. Use one receipt
per fresh occurrence and increasing times, with no private-state injection. Exactly one
training occurrence of each vector is sufficient for the intended source-predicted fixture.
These sentinels are invented unit-test
inputs, not learned representations. From the same resulting M1 state, query identical
current inputs with each vector. Required predictions/actions are `+1 / act_alpha` and
`-1 / act_beta`; unchanged outputs mean the intended wire is absent or ineffective.

Then use independent forks of that same state for this fixed matrix:

1. **Sham:** copy the vector without changing it; prediction/action must match exactly.
2. **Counterfactual vector swap:** swap only z in both consumers; action must follow the
   donor sentinel. Do not change the occurrence, current raw input, receipt or M1 state.
3. **One-consumer swaps:** swap z only in predictive input or only in routing. Required
   result is `abstain` with `predictive_scope_disagreement`, demonstrating gate survival.
4. **Zero/remove representation:** zero z in both consumers; expected result is abstention
   from unsupported context/route, not forced choice.
5. **ID renaming:** bijectively rename occurrence/receipt keys and replay the public prefix;
   the new features, predictive-bank/scope numeric state and M1 predictions/actions must
   agree if both reference steps complete. Compare reference state separately and disclose
   differences or failures; pre-existing ID-derived reference semantics are not audit-only.
   Identity-bearing ledger/audit bytes may differ. Global identity neutrality remains blocked.
6. **Receipt/clock faults:** duplicate receipt adds no state/weight; conflicting and wrong
   event receipts, future pulse, and receipt at/before decision must reject without partial
   state. Inject failure after backend advance and after each M1 update; compare full state.
7. **Real observer removal:** disable actual renderer/export callbacks, not a duplicate sham
   label; compare outputs/state/work counters. If no such callback exists, report not applicable.

The sentinel proves wiring and gate integrity only. It establishes neither learned assembly
formation nor predictive gain, physical-unit specificity, reward improvement or novel theory.

### B. Producer-to-consumer bridge: does an acquired representation use that wire?

Use a fresh predeclared unlabeled acquisition prefix; stop if its two-candidate dictionary
or transaction guards are ineligible. Freeze parameters/coordinates. Use two permitted
histories with identical current observation but different past cue order. Emit z before
any corresponding outcome. Train M1 through the public interface with a fixed later-feedback
prefix, then fork its identical state for cue A, cue B, actual sham and cross-swapped z probes.

Retain raw pulses, cutoff, selected activation, both copies of z, both internal M1 candidate
views, route decision, final prediction/action, pending binding, delayed receipt and state
inventories. Report separately whether the producer changes z, whether M1's prediction changes,
whether its gate permits an action change, and whether a later outcome changes the next query.
At least one paired probe must show a producer-derived vector swap changing a downstream
prediction or action while the sham is invariant to establish this narrow connection.
If z collides, only prediction changes while all actions abstain, or receipt conflict prevents
learning, report that exact layer; do not add a cue, rescale z or weaken a gate after inspection.

A z swap intervenes on the representation-to-consumer connection, not the biological/physical
assembly mechanism. A same-coordinate selective assembly suppression plus size/activity-matched
control, frozen selection criteria, and measured collateral is needed before a stronger
assembly-specific claim. Any predictive-benefit test must additionally use the interchangeable
raw-history alternatives, prefix-matched resource accounting and prospective loss/coverage
criteria. PR #169 demonstrates why first-return success alone is insufficient.

## 6. Primary-source constraints, not novelty evidence

Retrieved 2026-10-01 UTC, focused interface reading rather than systematic novelty search.
No paper implementation was downloaded or run.

- Michael L. Littman, Richard S. Sutton, Satinder Singh, *Predictive Representations of State*,
  NIPS 2001. [Primary full paper](https://proceedings.neurips.cc/paper/2001/file/1e4d36177d71bbb3558e43af9577d70e-Paper.pdf),
  introductory discussion and §1. The publisher abstract metadata omits Singh, but the
  paper itself includes him. Source: predictive state is defined through action-conditional
  predictions and sufficiency for future tests. Design implication: an assembly activation
  vector must earn its predictive usefulness downstream; it is not a sufficient state merely
  because it persists. This adapter is not a PSR implementation and inherits no theorem.
- Luc Moreau and Paolo Missier (editors), *PROV-DM*, W3C Recommendation, 2013-04-30,
  [§5.2.2 revision and data model](https://www.w3.org/TR/2013/REC-prov-dm-20130430/).
  Source: revision is a derivation relation between entities. Design implication: occurrence,
  receipt, learned representation and correction lineage require separate types; a corrected
  receipt cannot be introduced as a new context feature. PROV specifies no learning rule.
- The earlier [PR #168 map](nonstationary_evidence_capability_map_20261001.md) covers
  McCallum's history-based state identification and Alegre et al.'s context model reuse.
  Those remain prior alternatives and motivate history-aware replacement controls. They are
  not new results or new literature searches here.

## 7. What is verified now, and the stop point

The [source audit](../../artifacts/research/assembly_m1_interface_20261001/source_audit.json)
records hashes and AST symbol ranges for the exact source files. Recheck without importing
SparkBrain or executing models:

```bash
python scripts/verify_assembly_m1_interface_design.py
```

This verifies unchanged source bindings and a few explicitly enumerated syntactic dataflow
facts. It is not a whole-program dependence proof, runtime reachability result, checkpoint
certificate, or verification that the proposed interface already exists. The separate
model-free tests exercise corruption rejection in that auditor only.

Local verification: the auditor passed for eight pinned source files and eight explicit
syntax facts; all 11 model-free auditor tests passed; scoped Ruff and `git diff --check`
passed. Full runtime tests, demo, benchmark and model execution were intentionally not run
in this source-only scope. Independent source-only peer review identified the pre-existing reference semantic-ID
path. The narrowed guard and explicit global-identity blocker above resolved that finding;
review reported no remaining blocking design issue. It independently reran the auditor
and all 11 model-free tests. Exact-head Codex review and CI remain publication gates.

The deliverable stops at this source-bound design and its audit, after peer review. The next useful
implementation is the small sentinel and then a fresh producer bridge test, subject to the
unresolved transaction contract and the negative integration evidence above. Runtime edits,
new M1 feature semantics, model execution, merged-build acceptance, and scientific promotion
are not authorized by publication of this document.
