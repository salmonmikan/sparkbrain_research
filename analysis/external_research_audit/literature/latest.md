# External Literature Reduction Scout — continuous-state event-driven plasticity and resource crossover

- schema_version: `2`
- generation_id: `LIT-20260922T010311+0900-R24-CONTSTATE-EVENTDRIVEN-4A7C91E2`
- produced_at: `2026-09-22T01:03:11+09:00`
- producer_run_id: `external-literature-auto-20260922T010311+0900-R24-4A7C91E2`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260922T003849+0900-R23-EVENTSPARSE-6F3A91C8`
- role: `LITERATURE_REDUCTION_SCOUT`
- schedule_slot: `00:30 JST`
- schedule_inference: `false`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from the control-plane mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; the five annotated `evidence/*` tags are unchanged; tag-form `formal/*`, `sealed/*`, and `freeze/*` remain empty; 13 legacy `freeze/*` branches and 24 preserve branches were refreshed. PR #148/#149 remain open and unmerged. No research branch exists yet for the active R48 object.

Consumed control-plane generations and exact handoff commits:

- Control Brain: `CTRL-20260922T010052+0900-R27-5C8A21F4` @ `71b9db49b85e1c07483510f8d7b512951778d35b`
- Evidence Analyst: `EVA-20260922T002600+0900-R48-8C4A21F6` @ `86290dcbd85a45e89acc56263685cd9338963726`
- MAIN: `MAIN-20260922T004648+0900-RELAY-FUNNEL21-SYSTEM-LOCALIZE-R48-AUTHBOUND-8C4A21F6` @ `2277bc5838eeff4d629a33f6e85d663b805c6b60`
- SUB: `SUB-20260922T003526+0900-NOOP-R48MAINOWNED-4F8C21A6` @ `5fb202cd72a4130fabfafe6f0e712c0b62059348`
- prior Literature: `LIT-20260922T003849+0900-R23-EVENTSPARSE-6F3A91C8` @ `240e490e16d2bf71bb072a3ce289fcb841c19414`

R23 already established modern event-driven e-prop, SparseProp, and event-triggered three-factor plasticity as ordinary reductions. This run intentionally does not recycle those findings. The new question is stronger: whether continuous postsynaptic/plasticity state or exact continuous-time semantics can force dense/time-driven bookkeeping, and what resource costs event-driven alternatives move rather than eliminate.

The active canonical object remains `CAND-RESOURCE-SEMANTIC-ACTIVE-WORK-LOCALIZATION-01`, `ARCHITECTURE_STUDY / SYSTEM / preformal_eligible=false`. R48 authorizes MAIN only to bind a static/read-only prospective contract and STOP before synthetic outcome; the latest MAIN Relay correctly remains blocked at the PRIMARY authority boundary. Stable source still performs `_decay_eligibilities()` over every connection before every processed event, increments eligibility on outgoing edges when a spark fires, and scans all connections again on reward before skipping ineligible/non-plastic edges.

## High-value external findings

### 1. Continuous postsynaptic-state dependence does not force time-driven synapse updates

Stapmanns et al., *Event-Based Update of Synapses in Voltage-Based Learning Rules* (Frontiers in Neuroinformatics 15:609147, 2021; DOI `10.3389/fninf.2021.609147`) address the hard case in which plasticity depends continuously on postsynaptic membrane-potential history. They derive two history-archiving algorithms compatible with event-based synapse updates and implement them in NEST for Clopath and Urbanczik-Senn rules; both event-based schemes significantly outperform the time-driven reference in their evaluated regimes.

Impact: a future SparkBrain resource contract cannot treat persistent/continuous learning state, delayed credit, or third-factor history as sufficient reason for an all-edge update on every processed event. A fair ordinary comparator can retain the needed history and materialize plasticity updates only at relevant events.

### 2. Event-driven localization moves work into memory/history management, creating a real crossover rather than a free win

The same study explicitly decomposes the trade-off: ordinary event-driven updates reduce synapse function calls but require stored state history; compressed event-driven variants reduce repeated weight-change computation further but incur history-update costs whose scale depends on in-degree, spike-time diversity, and heterogeneous delays. The authors describe event-based schemes as faster but more memory hungry, with different variants becoming favorable in different regimes.

Impact: the current SparkBrain object should not use primitive operation count as a universal proxy for efficiency. Its prospective claim scope should bind a resource vector and crossover variables. A localization result can be real while still losing in memory/history overhead under another in-degree, delay, or event-rate regime.

### 3. Exact continuous-time learning can itself be event-sparse

Wunderlich & Pehle, *Event-based backpropagation can compute exact gradients for spiking neural networks* (Scientific Reports 11:12829, 2021; DOI `10.1038/s41598-021-91786-z`), derive EventProp, which computes exact gradients for its continuous-time spiking model by propagating errors at spike times and retaining state only at spike times rather than on a dense time grid.

Impact: exactness is not a valid blanket reason to accept dense bookkeeping. EventProp is not the same learning rule as SparkBrain and is not a direct task comparator, but it is a strong methodological counterexample: exact continuous-time semantics and event-sparse computation can coexist.

### 4. The fair SparkBrain discriminator is equal trajectory plus full state-archive cost

Repository plus literature inference: because stable SparkBrain globally decays all edge eligibilities at every processed event and globally scans again on reward, the strongest prospective ordinary reduction is a timestamp/history-lazy implementation that reconstructs exactly the eligibility/plasticity state required at event/reward access. The equivalence criterion should include event timing, eligibility values at reward, resulting weight trajectory, and downstream prediction trajectory—not only final task accuracy. The cost side should include operation count plus retained history/timestamps and history manipulation; wall-clock, cache, memory bandwidth, and energy should remain separate unless independently bound.

This sharpens R23 rather than overturning it. A positive current-object result stays SYSTEM/resource characterization and gains no mechanism novelty. H5 remains immutable and consumed at its canonical FAIL and is not reopened or post-hoc rescored.

No Utility request is created. Evidence Analyst has already admitted the fresh SYSTEM object and MAIN owns the prospective contract cycle; creating a parallel implementation/diagnostic request here would duplicate authority and could contaminate comparator selection.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_RESOURCE_SEMANTIC_ACTIVE_WORK_LOCALIZATION_01
  - ELIGIBILITY_RESOURCE_ACCOUNTING
  - EVENT_DRIVEN_CONTINUOUS_STATE_PLASTICITY_BASELINES
  - EXACT_SEMANTICS_COMPARATOR_DESIGN
  - PROGRAMME_ARCHITECTURE_EFFICIENCY
novelty_or_reduction_impact: >
  CONTINUOUS_STATE_EVENT_DRIVEN_REDUCTION_AND_RESOURCE_CROSSOVER_SHARPENING_NO_MECHANISM_NOVELTY_UPLIFT.
  Continuous postsynaptic/plasticity state does not inherently require time-driven/global synapse
  updates, and exact continuous-time learning can be event-sparse. Fair comparison therefore
  requires equal-semantics state archiving/lazy materialization plus memory/history and crossover
  accounting, not only primitive operation counts.
audit_classification: null
prospective_baselines_or_discriminators:
  - current global eligibility traversal versus event-triggered/timestamp-lazy eligibility that reconstructs exactly the state needed at access/update time
  - continuous-state event-driven history-archive comparator preserving the same postsynaptic/plasticity information
  - exact-semantics check on event timing, eligibility values at reward, weight trajectory, and downstream prediction trajectory
  - prospectively bound resource vector including primitive operations, retained history/timestamp memory, history-entry manipulations, and delay-diversity overhead
  - crossover sweep over in-degree, event rate/inter-event interval, delay diversity, active/nonzero eligibility-set size and lifetime, and reward frequency
  - wall-clock/cache/energy claims remain separate unless independently bound and measured
questions_for_evidence_analyst:
  - Keep the active R48 object SYSTEM-only and add continuous-state event-driven history archiving as an ordinary equal-semantics reduction before any resource uplift?
  - Require the fresh contract to bind memory/history overhead and crossover variables, not only primitive operation count?
  - Treat exact event-sparse computation as evidence that exactness/continuous-time semantics alone cannot justify global traversal?
questions_for_control_brain:
  - Add continuous plasticity state does not imply time-driven/global synapse updates to the ordinary resource-reduction checklist?
  - Require a prospectively fixed multi-resource/crossover claim scope so any positive localization result cannot be generalized beyond its workload regime?
  - Keep H5 immutable and consumed and keep PRE_FORMAL/FORMAL unchanged; use this only to sharpen the fresh SYSTEM object's comparator floor?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - H5 exact package/STARTED/raw-preserve/evidence chain and canonical FAIL_NO_USEFUL_WORK_REDUCTION
  - CAND-RESOURCE-SEMANTIC-ACTIVE-WORK-LOCALIZATION-01 fresh-object boundary and R48 same-generation STOP-before-synthetic-outcome authority
  - no H5 subtraction/rerun/rescore/retune/relabel/reopen
  - no synthetic outcome, STARTED/TEST/PRE_FORMAL/FORMAL promotion, research merge, immutable-ref mutation, or scheduler change by this role
utility_request_created: null
```
