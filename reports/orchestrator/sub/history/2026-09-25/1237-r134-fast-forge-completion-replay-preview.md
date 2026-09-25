# FAST FORGE — counterfactual Assembly replay preview

worker_role: FAST_FORGE
evidentiary_status: NON_EVIDENTIARY_NONCANONICAL_FORGE
forge_id: FORGE-20260925T123752+0900-R134-COMPLETION-REPLAY-PREVIEW
status: FORGE_PROTOTYPE
prototype_kind: INTEGRATION
new_scientific_result: false

## Freshness / ownership

Re-fetched before work:
- main: d16403414fc7abebd23075fc401240971b8eb91d
- Evidence Analyst: R134 @ ops/evidence-analyst-handoff@92a4f54f41688df063d801e62a3e0c4369160d0c; history blob 43c8a92adbe1c321efd8ee2d5d2d1766da626980
- Control: R73 @ ops/control-brain-handoff@c98b76c887edb0b727fa648735299dab3a66c530
- Theory: R5 NO_THEORY_PROPOSAL / NO_REVISIT_PROPOSAL @ 3933bd3f8f3ea963341332eea2eaa48d0b8457d3
- Literature: R44 selective-associative-revision reduction ladder @ a55899dc10db66b3cc741412f0fd61cf6d023fd0
- Independent Audit: R10 Candidate #35 INCONCLUSIVE treatment/readout support mismatch @ a89738c837b2e5bc2eab94adb1722bbb6daeb673
- Methodology: R121 SLIGHTLY_TOO_PERMISSIVE; build-specific lifecycle namespace required @ 7adc5be83e94adf278ae6284336373c93dc8b7cf
- Utility: IDLE @ ops/utility-orchestrator-requests@4fa2dafb418814f277ed19919956cec7e61b381d
- SYSTEM_BUILD: BUILD-SB-001-PREDICTIVE-STATE-REVISION-PILOT accepted bounded at exact head 5b86dfa6cad634312c81e579e5339b3b47cef6e0; exact-head CI 36060329063 success; lifecycle BUILD_ACCEPTED_BOUNDED_PENDING_INTEGRATION; composition contribution NOT_ESTABLISHED.
- canonical science: 35/35 terminal, active 0, queued 0.
- prior Forge durable state: FORGE-20260925T114511+0900-R134-COMPLETION-ACTION-PREVIEW, runs 44 / prototypes 26 / integration prototypes 5 / integration useful 5 / integration CI green 4.

R134 allocates MAIN to normal reviewed integration of the exact accepted SB001 head without feature mixing. No SB001 source, integration path, composition contract, scorer, runtime or workflow was touched by this Forge run.

## Question / target capability

Can the prior read-only Assembly completion proposal be connected back to the existing recurrent field in a way that:
1. never mutates the live field,
2. triggers only already-observed cue units,
3. never directly forces proposed missing units,
4. reports whether existing recurrence recruits the missing Assembly structure,
5. abstains on ambiguous completion?

This is a bounded integration question, not a scientific novelty probe.

why_now: R134 has accepted SB001 and separated its integration path; the prior Assembly completion object explicitly left feedback/re-injection as a distinct future Forge object. The target is independent of SB001 and directly addresses Assembly/internal-state completion/regeneration as an engineering unknown.

## Branch / prototype

branch: forge/20260925-completion-replay-preview-a
parent: forge/20260925-assembly-completion-a@dfc053332e95563b076f4e5e70b792710f696125
prototype_head: 7037e5024e791f8ecb545a0675637f39d3c41383

files:
- forge_prototypes/completion_replay_preview.py @ e982939502abd072bd7e27a534fa1d7472d6e2b1
- tests/test_forge_completion_replay_preview.py @ 97a0d7e3dc9aa46a462eef45d787aaae7d825689
- forge_prototypes/completion_replay_preview.md @ bf5599432006bffc1f5108c959617d04e10faeac

## Prototype behavior

The adapter reuses the Forge-only AssemblyCompletionProbe, clones TemporalExcitableField twice, runs one clone as a baseline, and on the replay clone injects current only into the cue's already-observed internal units. Proposed missing units are never directly stimulated. Recruitment, prototype recovery and spillover are read from the cloned recurrent dynamics. The live field state hash is compared before/after and is not committed.

Guards:
- ambiguous completion -> abstain
- missing prototype/cue field unit -> abstain
- receptor-containing prototype -> abstain
- excessive cue width -> abstain
- cue unit refractory at replay time -> abstain

## Development diagnostic

Source-matched deterministic diagnostic:
- mature prototype: (1,2,3,4), bins (0,1,2,3)
- partial cue: (1,3), bins (0,2)
- stable v0.5 pattern similarity: 0.6000000000000001
- proposed missing units: (2,4)
- explicit dev field threshold: 0.50
- cue replay current: threshold + epsilon = 0.500001 for zero-potential cue units
- recurrent edges: 1->2 = 0.60, 3->4 = 0.60
- spillover edge: 1->5 = 0.20
- deterministic expected replay units: (1,2,3,4)
- deterministic expected missing recovery: (2,4), fraction 1.0
- deterministic expected spillover: none
- recurrence-cut control: removing recurrent edges leaves only cue units (1,3), missing recovery 0.0.

Python syntax compilation of the persisted prototype and tests passed locally. Repository exact-package CI/check status was not observable from the available connector at close, so exact-package execution success is NOT claimed.

## Ordinary reduction

Strongest ordinary explanation: ordinary recurrent pattern completion / attractor-style replay plus content-addressable cue selection. This prototype deliberately relies on pre-existing recurrent edges to do the recruitment. The recurrence-cut control is expected to eliminate missing-unit recovery. Nothing here survives ordinary recurrence as a novelty claim.

## Engineering usefulness

PROMISING_NOT_YET_EXACT_PACKAGE_VERIFIED.

If exact-package execution confirms the test, this is a useful future integration seam for counterfactually asking whether a stored Assembly can be reinstated through existing recurrence before any live commit/re-injection path is designed. It is specifically safer than direct missing-unit forcing because the missing units must be recruited by the current field connectivity.

Usefulness, even if confirmed, would not establish scientific novelty.

## Scientific claim boundary

No claim of endogenous autonomous continuation, de-novo regeneration, new memory mechanism, causal necessity in the integrated SparkBrain runtime, superiority over ordinary attractor/recurrent completion, scientific candidate status, or canonical evidence.

Synthetic/dev behavior is development-only. The prototype does not access protected held-out/evaluator targets and creates no PRE_FORMAL/FORMAL/STARTED/evidence/sealed/freeze/preserve identity.

## Status / handoff

status: FORGE_PROTOTYPE
recommended_handoff: NONE_PENDING_EXACT_PACKAGE_VALIDATION
future_handoff_if_validated: SYSTEM_BUILD_INPUT
handoff_scope: FUTURE_INPUT_ONLY_NOT_SB001
MAIN_collision_check: PASS_NO_COLLISION
Utility_request: none

## Metrics

runs: 45
prototypes: 27
theory_probes: 3
theory_kills: 3
theory_survivors: 0
revisit_probes: 1
revisit_kills: 1
revisit_survivors: 0
dead_ends: 17
integration_prototypes: 6
integration_useful: 5
integration_ci_green: 4
system_build_input_recommendations: 5
later_build_input_admissions: 1

hard_floor_actions: NONE
