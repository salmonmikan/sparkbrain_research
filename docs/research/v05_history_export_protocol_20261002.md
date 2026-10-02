# Prospective history-conditioned native export diagnostic

2026-10-02 UTC. **EXPLORATORY / NONCANONICAL / NON_EVIDENTIARY**, scientific credit 0.
Identity: `v05-history-export-20261002`. **Source-only proposal; no model has run.**

## Question and explicit design amendment

Can two fixed past histories with the same current Q observation produce different,
repeatable exports from the unchanged native acquired-assembly producer, while private
query copies leave their acquired owner intact? This checks a representation prerequisite.
It does not construct M1 or test predictions, actions, feedback, benefit or joint atomicity.

[PR174's design](assembly_m1_interface_design_20261001.md) fixed two coordinates and
required exactly two mature prototypes. Candidate count is not the causal requirement:
one candidate can distinguish match from no-match, while several candidates can select
the same output. This is a **new prospective amendment**, not a pass or reinterpretation
of PR174. It replaces the exact-two rule with all mature canonical prototype coordinates,
bound once after acquisition. It preserves native strongest selection, identity exclusion,
unchanged feature values and explicit capacity accounting. No favorable subset is selected.

The old [PR169 result](temporal_reuse_loop_results_20261001.md) supplies an input-design
reason, not a positive integration claim. Its paired cue direction varied with history,
but H/R beat S, its integration-proposal gate failed, and B shams could select a third
mature assembly. Its checkpoints are historical data, not a supported live ownership
fixture. [PR180](v05_acquired_ownership_results_20261001.md) covers acquired ownership
only for its paired-Q state and specified faults; it does not establish the present graph.

## Frozen exposure, independent of favorable outcomes

Source pin: `9b1179aa18060436e4a05f2ff21f4cffc098f79d`.
The [machine protocol](../../artifacts/research/v05_history_export_20261002/protocol.json)
pins all 157 runtime Python files, the complete twelve-part configuration, graph schema,
reuse sources and [literal inputs](../../artifacts/research/v05_history_export_20261002/inputs.jsonl).
Input SHA-256: `69a25de3c3aef84743d45494a1193df0eac695b4d0c8a0beb8f07fad5129ee39`.

Use **both** original PR169 nuisance seeds, 910071 then 910072, and each complete published
64-window A32/B32 acquisition prefix. This fixed inherited exposure avoids selecting a
successful seed, a favorable checkpoint, or an episode count after observing acquisition.
It is a development fixture with known historical motivation, not unseen evidence or two
independent statistical replicates. Each seed starts one fresh producer. No checkpoint is
loaded. No target, outcome or reward is delivered at any stage.

All raw pulses retain PR169's source-valid fields, source `probe-input`, positive polarity,
null location, zero supplied novelty/prediction error and empty metadata:

- A: A/F/C at relative 8/13/15 ms; B: C/F/A at the same times, magnitude 1.18
- Two nuisance pulses, sampled from H/I/J/K/L/M, magnitude 0.025, times in [0,36] ms
- Identical current Q at 40 ms, magnitude 1.18
- One call per 200 ms window; decision/end at +72 ms, after native 32 ms settling

The generator is the published PR169 recipe at
[`occurrence`](../../scripts/temporal_reuse_loop_probe.py): independent `random.Random`
seeded by the integer SHA-256 of `seed|key|index`. For each window, draw a nuisance channel
with `randrange(6)`, then its uniform time, twice. Prefix keys/indices are `prefix`, 0..63;
the first 32 use A, then 32 B, with exact cue timing. Query key/index is `probe`, 0; after
the four nuisance draws, draw three cue jitters uniformly in [-0.35,+0.35] ms. The same
draws are reused for A/B and their repeats. No interleaved cue bit is drawn. Only A/C order
differs across each paired query; F, Q, time multiset, amplitudes and nuisance rows agree.

Literal file records contain audit-only seed/phase/branch identifiers outside `observation`.
Only `occurrence_id`, `start_ms` and `pulses` are passed to the producer. Fresh opaque IDs
are allocated monotonically and contain no seed, cue or outcome. The four independent
queries for a seed use the same occurrence ID and the same start 12,800 ms; expected end
is 12,872 ms. They do not form a sequential four-window suffix.

## Native learning and freeze

The producer follows PR169 S's topology seed 41, native assembly cap 32 and default
receptor/field/assembly/plasticity/homeostasis settings. Acquisition enables native
assembly, weight, delay and homeostatic learning. Prediction, action and reward modulation
are disabled; no `learn_outcome` call occurs. This is deliberately an unlabeled acquisition
fixture, not a reproduction of PR169's trained count predictor. Source
[`learn_outcome`](../../src/sparkbrain/v05/brain.py) confines prediction/action/reward updates
to those switched paths; no old wrapper or runner is imported or executed.

After all 64 prefix calls, record every candidate, prototype, episode set and configuration.
Native maturity requires three distinct episode IDs; 64 calls alone do not certify any
particular candidate count. Preserve the actual outcome, including no mature candidate.
Then freeze acquisition and field/homeostatic learning via
`learn_assembly=False, learn_field=False, explore_action=False, metadata={}` on all queries.
Receptors, membrane/adaptation, queues, traces and result retention still evolve normally.

## Exact export rule and negative outcomes

The dictionary consists of **every** mature candidate at the frozen boundary. Canonical
prototype content is the tuple `(ordered_units, relative_bins, unit_ids, spike_count,
source_kind)`, in that order. Lexicographically sort those tuples. Retain the complete
content and SHA-256 binding, with native IDs only as audit references. Assembly/pattern/
cascade/episode IDs, absolute times and outcome information do not define coordinates.
Equal canonical tuples belonging to different candidates are a collision, not grounds to
choose by ID or silently deduplicate. Dictionary size N is fixed for all queries of that
seed and remains bounded by the unchanged native cap 32.

For every accepted internal pattern, recompute the native candidate similarities without
changing the bank. Preserve all scores and exact best-score ties, including immature
candidates. Also retain all ties on the strongest selector's `(similarity, episode_count)`
before its assembly-ID tie-break. Any such tie withholds an accepted export; no epsilon,
alternative winner, tolerance tuning or label-based resolution is allowed. Source:
[`best_match`/`observe`](../../src/sparkbrain/v05/assemblies.py) and
[`process_episode`](../../src/sparkbrain/v05/brain.py).

Use the actual native `pending_activation`, checking its identity against the returned
activation and frozen binding. If it is mature and unsuppressed and maps to coordinate j,
emit its **unchanged native similarity** at j and zero at every other coordinate. Otherwise
emit the all-zero length-N vector with an explicit `no_match` status. No clipping, scaling,
normalization, counter feature or confidence calibration is added. Reject nonfinite or
out-of-[0,1] values. Missing bindings and canonical collisions withhold accepted exports.
For an empty dictionary, record `no_mature_dictionary`; an empty vector is not usable context.

The detached primitive export has exactly `schema`, `occurrence_id`, `decision_ms`,
`accepted`, `status`, `features` and `binding`. Version is `v05-history-export-1`; status
distinguishes accepted match/no-match from missing dictionary, canonical collision, either
native tie, binding error or value error. Accepted features have length N; a rejected export
has an empty diagnostic list and cannot be consumed as context. The binding carries the
projection version, source pin, N, ordered canonical prototype contents and their digest.
The digest excludes identity and absolute-time fields; native IDs stay in raw audit records.
Receipt ID and decision time are metadata only. Branch labels, counters and resource/timing
samples stay outside this deterministic export. Nothing in the binding is a numerical feature.

For each seed run four copies in fixed order: A, B, A-repeat, B-repeat. Compare the complete
native graph and detached export within each repeat pair. A producer contrast is observed
only if both pairs reproduce exactly, all ownership guards pass, both exports are accepted,
and A/B vectors differ. Match versus no-match may qualify; it is not fabricated confidence.
Report a single-candidate contrast if it occurs, and aliasing if it does not. Preserve
missing, tie, collision, resource and ownership outcomes separately from an alias result.
There is no additional query, episode, seed, changed projection or retry after any result.

Record the Euclidean distance and dictionary dimension. M1's default route has eight
dimensions and its predictive input has 64 scalars; retaining one original coordinate in
each leaves at most seven new coordinates. This is a **future consumer-capacity annotation**,
not a producer candidate-count target. A dictionary above seven still receives the bounded
producer-only queries and is reported `future_m1_capacity_blocked`. Do not truncate it or
raise M1's limits. Actual injected configurations must be checked before a future adapter
advances either component. The default 0.25 scope-birth distance is a source-only geometric
reference; exceeding it does not demonstrate a learned route, prediction or action.

## Ordinary information comparator

For every acquisition/query record, retain the original PR169 raw raster: all ten channels
A,C,F,H,I,J,K,L,M,Q, 41 bins at 1 ms, linear floor/ceil pulse splitting, divided by total
observed magnitude. Exact-integer times occupy one bin. It includes the same nuisance and
current-Q observations through the same 40 ms raw-input cutoff. It receives no assembly,
outcome, future or privileged fields. Record paired L1 differences and exact repeat equality.

This outcome-blind 410-cell raster is the ordinary-information comparator input, not an M1
adapter. PR169's supervised H/R p1 values must not be used as temporal features. A later
comparison still needs a prospectively fixed bounded raw-history encoder and separately,
equally trained M1 consumers with matching history/cutoff/feedback access. No assembly
advantage is inferred from export separation alone, especially given PR169's negative result.

## Actual ownership boundary and finite budget

For each seed, use the complete supported typed/reference graph audit from PR176/180,
attributed and source-bound; do not import the old probes. Audit all owned state, including
caches, retained results/traces, aliases and inactive base components. Unknown fields,
objects, copy hooks or external handles stop before copying, without omissions or a native
serialization fallback. Native state hashes are not the completeness oracle.

Make all four whole-brain copies with separate deepcopy memos from the same unchanged root
before processing a query. Require exact full graph equality and all ten root/copy pairwise
mutable-identity intersections to be empty. A private copy receives detached pulse objects;
the caller's six actual pulse metadata dictionaries remain external. Every query must leave
the original graph exact, and frozen weights/delays/thresholds/candidate contents unchanged.
Its primitive export must share no mutable object with candidate state or caller inputs.

Preserve raw output/export and the candidate graph first. Then mutate the six real caller
metadata dictionaries, the detached export's feature list and its binding dictionary,
exactly once each. Compare the candidate and acquired-root complete graphs again. A blocked
export still has detached diagnostic lists/dictionaries; its mutation check cannot turn it
into an accepted feature. Stop processing that copy afterward. There is no owner-pointer
commit, injected fault, native restore, outcome update or M1 operation in this diagnostic.
This checks ownership compatibility for these actual query graphs, not general transactions.

Maximum work across both seeds: **2 fresh roots, 128 acquisition calls, 8 query calls,
816 raw pulses, 8 whole-brain copies and 64 external-object mutations**. No candidate-count
condition adds work or chooses another seed. A fatal source/schema/resource/ownership error
stops with partial evidence; ordinary representation failures remain recorded for both seeds
within the fixed plan.

Bounds: process CPU 120 s, hard wall 180 s, address space 512 MiB, evidence 96 MiB. Reserve
3 CPU seconds, 10 wall seconds and 4 MiB for finalization **inside** those limits. These
are caps, not performance expectations; exhaustion is a recorded failure with no enlarged
budget or retry. Python audit network denial is not OS isolation, and a hard kill may prevent
finalization. Record timing origins, exact launch arguments, environment/source pins, actual
counts and incomplete writes truthfully.

Retain complete raw results/errors per call, all candidate/maturity/matching inputs, exact
input/raster/export bytes, ownership graphs and alias witnesses, copy/gate/mutation records,
resource observations and a hash manifest. Check raw writes before interpreting results.
Publish an exact implementation/test/source freeze and obtain independent review before
any producer import, construction or execution. This proposal does not authorize a run.

## Consequence

An observed contrast would establish only that this native learned export carries a
repeatable distinction for these fixed histories under the stated ownership checks. It
would justify a separately reviewed consumer connection with pending-receipt binding,
pre-mutation capacity checks, complete joint rollback, same-state swap/sham controls and
ordinary equal-information alternatives. It would not establish M1 contribution, benefit,
physical-unit specificity, biological equivalence or novelty.

Active directive source checked at `ops/human-directives` head
`8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, index blob
`1ba1e173344f36e14d0e21e6f3e823254e031f7d`. No scheduler, scientific status, acceptance,
existing ledger entry or role-owned PR is changed by this proposal.
