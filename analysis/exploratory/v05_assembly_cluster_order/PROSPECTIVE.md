# EXPLORATORY / NON_EVIDENTIARY — v0.5 Assembly cluster order discovery

## Prospective contract

- discovery_mode: `SYSTEM_DISCOVERY`
- proposed candidate: `CAND-V05-ASSEMBLY-CLUSTER-ORDER-DEPENDENCE-01`
- cycle: `1/3`
- claim_ceiling: `SYSTEM`
- preformal_eligible_pre_outcome: `false`
- evidentiary_status: `NON_EVIDENTIARY`
- stable_base: `main@ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- analyst_authority: `EVA-20260920T190536+0900-R18-AC1DB49E@fec9320a8e8c868f4df91dafb1af75c640ae995a`
- main_generation_observed: `MAIN-20260920T191546+0900-PRIMARY-FUNNEL21-HOLD-R18-8C2F41D7`
- previous_sub_generation: `SUB-20260920T184410+0900-THEORY-CONTEXTPRED-7A4C2E91`

Question: can `TemporalAssemblyMemory` assign a different candidate partition to the same multiset of development patterns solely because the first-seen immutable prototype changes with presentation order?

This is independent of MAIN because MAIN has no active scientific object. It does not reopen the terminal Assembly lifecycle/capacity object, partial-completion object, pre-semantic transfer object, H7, FORMAL/TEST/scoring, or any consumed/frozen identity.

## Terminal/API semantic preflight

Stable-main `src/sparkbrain/v05/assemblies.py` was read before execution. `TemporalAssemblyMemory.observe()` compares each new pattern to the stored candidate `prototype`, creates a new candidate when best similarity is below `AssemblyConfig.similarity_threshold`, and never updates an existing candidate prototype. Candidate count/membership and returned `assembly_id` are therefore the bound terminal observables.

## Fixed synthetic construction

Use threshold `0.66`, `mature_episodes=3`, and three equal-length development-only `ActivityPattern` objects with bins `(0,1,2,3)`:

- A ordered units `(1,2,3,4)`
- B ordered units `(1,2,3,5)`
- C ordered units `(1,2,4,5)`

Prospectively fixed similarities under repository `pattern_similarity` are A-B=`0.7625`, B-C=`0.7625`, A-C=`0.6250`. Thus B bridges A and C while A and C are below threshold.

Compare two arms using the exact same pattern multiset and unique episode IDs:

- arm ABC: observe A, then B, then C;
- arm BAC: observe B, then A, then C.

No threshold, pattern, similarity function, or candidate configuration may be changed after outcome exposure.

## Fixed terminals

- `ORDER_DEPENDENT_CLUSTER_PARTITION`: candidate count or pattern-to-assembly assignment differs across arms. Recommend SYSTEM Architecture study; do not infer mechanism novelty.
- `ORDER_INVARIANT_CLUSTER_PARTITION`: candidate count and assignments are equivalent modulo assembly-ID renaming. Reject current object.
- `POST_OUTCOME_TERMINAL_SEMANTIC_DEFECT`: bound public/API semantics prove wrong after outcome exposure. Stop as method-limited; do not repair/rerun for scientific closure.

## STOP

Stop after the first mapped terminal. No cycle-2 search for alternate triads. Any mitigation or alternative clustering rule is a fresh object, not rescue tuning.
