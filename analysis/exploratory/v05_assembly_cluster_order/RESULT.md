# EXPLORATORY / NON_EVIDENTIARY — v0.5 Assembly cluster order result

## Result status

- discovery_mode: `SYSTEM_DISCOVERY`
- proposed candidate: `CAND-V05-ASSEMBLY-CLUSTER-ORDER-DEPENDENCE-01`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- current-object claim_ceiling: `SYSTEM`
- proposed preformal_eligible: `false`
- terminal: `ORDER_DEPENDENT_CLUSTER_PARTITION`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

## Prospective binding / integrity

The prospective contract was committed at `7e2646cfb1a83f5cbbec0b22c5dcf2a706f8022d` before outcome-bearing execution. The first test-head CI (`35505600594`) stopped at lint in both Python jobs before Local readiness/Test and therefore exposed no scientific outcome. The only correction was import formatting; no pattern, threshold, similarity function, ordering, terminal, or comparator changed. Corrected exact-head CI `35505715764` on `fca8ad5a5214cc9ca67c157ef45c5d129a3f66d7` completed successfully on both Python 3.11 and 3.13.

## Fixed inputs

Three equal-length synthetic DEV patterns with threshold `0.66`:

- A: `(1,2,3,4)`
- B: `(1,2,3,5)`
- C: `(1,2,4,5)`
- all relative bins: `(0,1,2,3)`

Repository similarity values were fixed and confirmed by the passing probe:

- A-B = `0.7625`
- B-C = `0.7625`
- A-C = `0.6250`

Thus B is above threshold to both A and C while A and C are below threshold.

## Observation

The exact same pattern multiset partitions differently solely by presentation order:

- `A -> B -> C`: A creates the first candidate, B joins A because A-B is above threshold, but C is compared against the unchanged A prototype and falls below threshold. Result: `2` candidates; A/B together, C separate.
- `B -> A -> C`: B creates the first candidate, then both A and C join because both B-A and B-C are above threshold. Result: `1` candidate containing all three.

The source-level explanation is first-prototype anchoring: candidate prototypes are created from the first pattern and are not updated when later patterns join. This makes threshold clustering non-transitive and insertion-order-sensitive for bridge configurations.

## Interpretation / bounds

This is a SYSTEM architecture observation, not evidence for a cognitive mechanism or novelty claim. It shows a deterministic component-level order dependence in the current Assembly clustering contract on one fixed synthetic bridge triad. It does not establish how often such triads are reachable from integrated recurrent activity, whether supported episode ordering intentionally carries semantic information, or whether the partition difference changes downstream prediction/action behavior.

The current object should not be upgraded to MECHANISM. A future MECHANISM question, if any, requires a fresh candidate ID and prospective contract.

## Funnel v2.1 proposal

- proposed claim_ceiling: `SYSTEM`
- proposed preformal_eligible: `false`
- preliminary readiness: `N/A_FOR_SYSTEM_OBJECT`
- proposed hold_class: `null`
- proposed hold_reason: `null`
- proposed terminal_state: `ACTIVE`
- proposed queue_state: `QUEUED`
- candidate next research layer: `ARCHITECTURE_STUDY_ASSEMBLY_CLUSTER_ORDER_DEPENDENCE_CONTRACT`
- recommendation: `PROMOTE_TO_ARCHITECTURE_STUDY`

Architecture study should prospectively establish: supported integrated reachability of bridge-like pattern sets; whether input/episode order is contractually meaningful or an incidental degree of freedom; quantitative partition sensitivity across fixed development conditions; and whether candidate-partition changes produce downstream functional differences. It should not patch clustering or tune threshold/prototype rules against this observed result.

## Falsifier / reduction for next layer

Reduce the architecture concern if a prospectively fixed supported integrated probe shows that bridge-like non-transitive sets are unreachable under normal Assembly candidate generation, or if the supported API explicitly defines presentation order as part of the intended clustering semantics and no downstream functional consequence survives a matched order-invariant comparator. Those are future fresh tests, not additions to this Discovery object.

## Completion

No formal/held-out TEST, official scorer, consumed identity, immutable evidence, STARTED/control authority, freeze/formal/evidence ref, research merge, or stable-main mutation was used or created. Cycle 2 is not used to search for alternate triads or rescue the result.
