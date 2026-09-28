# External Literature Reduction Scout — FLY-0 causal ascending feedback, selective gating, and delay-matched comparators

- schema_version: `2`
- role: `LITERATURE_REDUCTION_SCOUT`
- generation_id: `LIT-20260928T123000+0900-R47-ASCENDING-FEEDBACK-GATING-C4E8A2D7`
- produced_at: `2026-09-28T12:29:03+09:00`
- producer_run_id: `external-literature-auto-LIT-20260928T123000+0900-R47-ASCENDING-FEEDBACK-GATING-C4E8A2D7`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_NON_EVIDENTIARY_NONCANONICAL_HANDOFF`
- supersedes_generation_id: `LIT-20260928T063000+0900-R46-FLY0-DISTRIBUTED-CONTROL-B7D3C4A1`
- genuinely_new_information: `true`
- new_sparkbrain_scientific_result: `false`

## Scope and freshness

The invocation started at 12:29:03 JST and resolves by the common early-dispatch rule to the 12:30 JST canonical slot, selecting exactly one role: `LITERATURE_REDUCTION_SCOUT`.

The Human Directive index remains unchanged from Literature R46: `ops/human-directives@8ce979b9ec0bc7eede5225c0403698f8886d3e8d`, blob `1ba1e173344f36e14d0e21e6f3e823254e031f7d`. No newly active or materially changed directive is observed. Applicable current directives are HUMAN-20260928-001, HUMAN-20260928-002, HUMAN-20260927-002 and HUMAN-20260925-002. Literature remains parallel/non-gating and preserves the build-to-science boundary.

Durable Evidence Analyst R166 records M1-002 at exact head `2a21d3e879f1db4e81a58273180ad2124e823a5e` as built and bounded-functionally verified, with no comparative support, no composition contribution, no novelty and zero scientific credit. MAIN R172 remains operationally blocked on PR creation after five pre-GitHub refusals. FLY-0 has a durable interaction-ablation result: bottom-up Observation/LocalFeedback is not causally active in the current bounded trajectory; activity/resource comparability and the complete matched replacement ladder remain incomplete; no SB003 allocation exists.

The prior Literature R46 history/latest/state triplet was independently re-read and is internally consistent. This role therefore has no self-stream durability debt to repair before publication.

## High-value literature findings

### 1. Ascending feedback already has a demonstrated engineering role in hierarchical embodied fly control

**Classification:** `NOVELTY_REDUCTION`, `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`.

Wang-Chen et al., *Nature Methods* (2024), "NeuroMechFly v2: simulating embodied sensorimotor control in adult Drosophila" (doi:10.1038/s41592-024-02497-y), explicitly adds ascending motor feedback to an embodied hierarchical fly simulator and uses it for path integration and head stabilization.

**Function supplied:** an established architecture in which local/embodied motor state is summarized upward and can alter higher-level estimation/control, while lower layers retain fast motor execution.

**Known limitation:** NeuroMechFly v2 is a neuromechanical modeling platform with engineered/hybrid controllers and, in some tasks, learned policies. Its success does not establish that the same computation is biologically implemented everywhere or that SparkBrain/FLY-0 is biologically faithful.

**SparkBrain claim it must not imply:** causal ascending feedback, hierarchical control, path integration, or head stabilization are not topology-specific SparkBrain novelties merely because FLY-0 later implements them.

Source: https://www.nature.com/articles/s41592-024-02497-y

### 2. Adult-fly ascending neurons carry behavioral-state and self-motion information to integrative/action-selection regions

**Classification:** `NOVELTY_REDUCTION`, `DESIGN_PRIMITIVE`.

Chen et al., *Nature Neuroscience* (2023), "Ascending neurons convey behavioral state to integrative sensory and action selection brain regions" (doi:10.1038/s41593-023-01281-z), reports that identified ascending neurons encode self-motion and discrete behavioral states and target integrative sensory and action-selection regions.

**Function supplied:** a biologically grounded reason for a bottom-up channel to carry a compact behavioral-state/self-motion summary rather than merely echo raw local events.

**Known limitation:** encoding and projection evidence does not by itself specify the exact causal computation that SparkBrain should use, nor does it justify forwarding every local signal unfiltered.

**SparkBrain claim it must not imply:** adding an ascending state summary does not establish biological equivalence, topology superiority, or scientific novelty.

Source: https://www.nature.com/articles/s41593-023-01281-z

### 3. Useful proprioceptive feedback is selectively gated; more bottom-up traffic is not automatically better

**Classification:** `NOVELTY_REDUCTION`, `DESIGN_PRIMITIVE`.

Dallmann et al., *Nature* (2025), "Selective presynaptic inhibition of leg proprioception in behaving Drosophila" (doi:10.1038/s41586-025-09554-2), finds that movement-encoding leg proprioceptive signals are selectively suppressed during self-generated walking/grooming while position-related signals remain available, through context- and leg-specific inhibitory circuitry driven by descending/premotor pathways.

**Function supplied:** a concrete design primitive for distinguishing expected self-generated movement feedback from state/error information that remains useful for control.

**Known limitation:** the result concerns particular leg proprioceptive channels and predictive inhibition; it is not a universal rule that all movement-related feedback should be suppressed.

**SparkBrain claim it must not imply:** a biologically inspired gate is not evidence that FLY-0 reproduces the fly circuit, and activity reduction from gating is not an energy-efficiency result.

Source: https://pubmed.ncbi.nlm.nih.gov/40963018/

### 4. Sensorimotor delay is a first-class robustness/resource variable for hierarchical walking controllers

**Classification:** `DESIGN_PRIMITIVE`, `SYSTEM_LEVEL_COMPARATOR`.

Karashchuk et al., *eLife* (2025), "Sensorimotor delays constrain robust locomotion in a 3D kinematic model of fly walking" (doi:10.7554/eLife.99005.3), shows in a layered fly walking model that locomotor robustness degrades as sensorimotor delay increases beyond the supported range.

**Function supplied:** delay budget should be explicit and matched when comparing structured, rewired, random, and replacement controllers; perturbation robustness should be checked under the same delay assumptions.

**Known limitation:** this is a computational locomotion model, not a direct proof of the exact delay tolerance of FLY-0 or SparkBrain.

**SparkBrain claim it must not imply:** matching delay/resource exposure may improve comparator fairness but does not create topology-specific novelty, biological fidelity, or energy claims.

Source: https://elifesciences.org/articles/99005

## Reduction and integration consequence

These findings strengthen Analyst R166's current engineering diagnosis. The missing capability is not simply "make LocalFeedback nonzero." A stronger minimal target is to derive an explicit ascending state summary from local action/world outcome; make it causally affect the next high-level state/modulation in a bounded task where the information can matter; separate persistent state/position-like information from expected movement/delta feedback; allow predictive/contextual gating; match delay budgets across structured and replacement controllers; and re-run the existing interaction ablation on the new causal path.

A NeuroMechFly-style hierarchical controller or reduced abstract equivalent is a high-value established system-level replacement comparator for the matched ladder. It can test whether any FLY-0 benefit survives against an ordinary hierarchical controller with explicit ascending feedback, rather than only against topology variants.

This is a prospective engineering handoff only. It does not allocate SB003, reopen a scientific object, or create a review gate for M1-002.

## Revisit / science disposition

- revisit_status: `NO_NEW_TRIGGER`
- canonical science remains 35/35 terminal, active 0, queued 0, consumed FORMAL identities 8.
- No experiment, result-bearing workflow, immutable mutation, candidate reopening, or scientific promotion was performed.
- No new SparkBrain scientific result is created.

## Prospective handoff

- Forge: if continuing FLY-0, prefer a minimal causal ascending-state channel with a task/perturbation that actually requires it; preserve the current no-effect result on the simple movement task as a valid reduction.
- Forge/Analyst: add a reduced ordinary hierarchical controller with ascending feedback to the matched replacement ladder before any topology-specific scientific claim.
- Comparator harness: record/match delay budget separately from unit/edge/activity exposure.
- Claim boundary: selective/gated feedback is an established mechanism; implementing it is engineering reuse, not novelty.
- M1: no stop or additional review gate; the current M1-002 blocker remains operational PR mutation, not literature/science.
