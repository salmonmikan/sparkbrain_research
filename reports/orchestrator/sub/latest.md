# SparkBrain Research Orchestrator SUB — 2026-09-20 04:49 JST

## Mode / allocation

- mode: `discovery`
- final Evidence Analyst authority: `493573eb3b8c38d88f251db7c04dfe1a586c6ff0`
- authoritative stable main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- main_lane: `V05_UNIT_SUPPRESSION_TRANSIENT_CONTRACT_ARCHITECTURE_STUDY_CYCLE1`
- sub_lane: `BOUNDED_SECONDARY_DISCOVERY`
- sub_fallback: `NO_OP_WITH_OBSERVABLE_LEVEL_DUPLICATION_OR_LOW_VALUE_REASON` (not used)
- exploratory_target: `ASSEMBLY_CASCADE_FALLBACK_BRIDGING_DISCOVERY_CYCLE1`
- candidate_pool_id: `NONE_SELF_SELECTED`
- exploration_cycle: `1/3`; stopped after one bounded cycle for fresh Analyst review
- evidentiary_status: `NON_EVIDENTIARY`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Authority reconciliation / MAIN frontier avoided

The final fresh Analyst handoff appeared after the initial same-run SUB snapshot but leaves the allocation materially unchanged: Discovery remains open to SUB for at most one independent bounded question, while MAIN exclusively owns `CAND-V05-UNIT-SUPPRESSION-TRANSIENT-SEMANTICS-01` static contract characterization. The new handoff explicitly confirms MAIN has not yet started that object and does not classify this newly completed SUB result yet.

SUB did not continue the promoted suppression object, replay the prior suppression pulse diagnostic, take MAIN blockers, continue v0.5 config binding / Temporal / Top-k / H7, or touch FORMAL/TEST/scoring/identity/preserve/evidence surfaces. `blocked_until` keeps dynamic MAIN continuation, PRE_FORMAL, and FORMAL gated behind their respective fresh prospective authorities. `do_not_touch` was respected for consumed identities, immutable evidence/control/preserve refs, completed topology-config/Temporal/Top-k/H5/NI01/C19/PD01 artifacts/outcomes, official TEST/formal scorer surfaces, scheduler definitions, and PR #148/#149 governance work.

## Discovery question / implementation

Because the named Analyst pool contained no independent executable SUB object, SUB used the permitted one-question self-selection path. On non-authoritative branch `research/exploratory-sub-assembly-cascade-fallback-bridging-20260920`, created from exact stable main, SUB prospectively bound the question in `3af7c2388e4af35dd53984d3c48cb08513bed320`, added a deterministic diagnostic in `828a8090c748be1f2ea61e037964f26b2f3bc4c6`, and recorded the handoff on exact research head `373f7d52af3b46a23ae976863a2eb5d73d982b5f`.

Question: when one episode contains multiple temporally separated cascades, each with only one eligible non-receptor spike after receptor exclusion, does `patterns_from_step(...)` synthesize one fallback `ActivityPattern` spanning those distinct cascades even though no individual cascade can form a pattern?

Fixed synthetic diagnostic: two explicit cascades separated by 20 ms; each contains one receptor spike (`unit 0`) and one reservoir spike (`unit 101` at 1 ms; `unit 102` at 21 ms). Excluding the receptor leaves one eligible internal spike per cascade. A control adds a second eligible internal spike to the first cascade. A separate assembly-facing check passes the fallback through `TemporalAssemblyMemory(mature_episodes=3)` for three distinct synthetic episode IDs.

No production source was modified. No repository dataset, trained checkpoint, retained/confirmatory/held-out TEST input, formal raw result, official scorer, consumed identity, or MAIN outcome artifact was opened or used.

## Observations

Each sparse cascade independently fails the two-spike minimum. Because no cascade-local pattern exists, current source falls back to `pattern_from_spikes(...)` over all eligible internal spikes in the step. The fixed diagnostic therefore emits exactly one pattern with `source_cascade_id=None`, `ordered_units=(101, 102)`, `unit_ids=(101, 102)`, `start_ms=1.0`, and `end_ms=21.0`: one assembly-facing representation spans two explicitly separate cascade windows.

The matched control shows that once a cascade has two eligible internal spikes, cascade-specific extraction succeeds and the cross-cascade fallback is not invoked. The assembly-facing check shows this is not merely provenance/hash bookkeeping: `TemporalAssemblyMemory` accepts the bridged fallback normally, and repetition across three synthetic episode IDs matures the candidate at `episode_count=3`. `IntegratedV05Brain.process_episode()` likewise forwards returned patterns above `min_pattern_spikes` into assembly memory.

The effect is completely reduced to existing extractor control flow (`if not patterns` -> build one fallback from all eligible step spikes); no new memory mechanism is required. The unresolved issue is architecture/segmentation semantics: sparse responses from distinct cascades can be collapsed into one episode-level representation before memory formation.

Exact-head ordinary CI `35465287304` completed `success` for `373f7d52af3b46a23ae976863a2eb5d73d982b5f`; Python 3.11 and 3.13 both passed lint, local readiness, tests, and bundle validation. CI has no evidentiary role.

## Handoff / stop

Evidentiary status remains `NON_EVIDENTIARY`. Recommendation to Evidence Analyst: `PROMOTE_TO_ARCHITECTURE_STUDY`, specifically `ARCHITECTURE_STUDY_ASSEMBLY_SEGMENTATION_SEMANTICS`, not PRE_FORMAL or FORMAL promotion.

Reduce to `REJECT/ENGINEERING_NOTE_ONLY` if the supported contract intentionally permits episode-global fallback composites across cascades and a fresh DEV-only boundary-preserving comparator yields no meaningful difference in assembly candidate formation or downstream prediction/action observables. Also reduce if supported runtime states cannot produce the sparse multi-cascade condition.

A fresh prospective Architecture object should fix a DEV-only matched family with identical internal spikes but different segmentation, compare current fallback against a boundary-preserving comparator, and pre-bind candidate/maturation plus one downstream functional observable. SUB does not continue to cycle 2 without fresh Analyst promotion.

Scientific/semantic choices still open: cascade-local vs episode-global `ActivityPattern` semantics, interpretation of `source_cascade_id=None`, handling of sparse per-cascade partials, and whether downstream behavior differs enough to warrant architecture work rather than documentation only.

Utility request: none. Consumed identities: none. New formal results: zero. Blocker: fresh Evidence Analyst classification and prospective assembly-segmentation Architecture contract only.

Completion target: `ACHIEVED_ONE_BOUNDED_INDEPENDENT_ASSEMBLY_SEGMENTATION_DISCOVERY_CYCLE_AND_RETURNED_ARCHITECTURE_PROMOTION_CANDIDATE` — achieved.

SUB persistence history: preliminary same-run snapshot `reports/orchestrator/history/2026-09-20/0447-sub.md` at `0b18c8ff3a39d5b6a4d9bf7757276e4fa71ad233`; final authority-reconciled append-only snapshot `reports/orchestrator/history/2026-09-20/0449-sub.md` at `70ee6ef3364d1abd6d5c6196b31b7b9fded02067`. No MAIN or legacy shared latest/state file was modified; no force-push was used.