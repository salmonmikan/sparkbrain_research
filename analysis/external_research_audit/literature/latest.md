# External Literature Reduction Scout — eligibility clock / partition semantics

- schema_version: `2`
- generation_id: `LIT-20260921T032811+0900-R16-ELIGIBILITY-CLOCK-2F8C71A4`
- produced_at: `2026-09-21T03:28:11+09:00`
- producer_run_id: `external-literature-auto-20260921T032811+0900-R16-2F8C71A4`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T003000+0900-R15-ELIGIBILITY-TIMEBASE-5A7C2E91`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative annotated `evidence/*` tags remain five; `formal/*`, `sealed/*`, and tag-based `freeze/*` remain empty; legacy freeze branches remain unchanged. PR #148 and #149 remain open/unmerged.

Consumed control-plane generations:

- Control Brain: `CTRL-20260921T025500+0900-R19-9D2C4A71` @ mailbox commit `dcdea1bbd1490da004bce69d4b7f4f7b4d37fbd4`
- Evidence Analyst: `EVA-20260921T031129+0900-R25-1E24780E` @ `258406668f86b24f54dd1a88f18da37e457a001b`
- MAIN: `MAIN-20260921T031700+0900-PRIMARY-FUNNEL21-SYSTEM-ELIGPART-R25-7A4C91E2` @ `a1d401a4ac8bd65525907e3074a9a508b7f4c102`
- SUB: `SUB-20260921T023300+0900-NOOP-NOMECH-5E2A91C7` @ `71826e37165705647d9fd13b7b1698422d557fb5`
- prior Literature: `LIT-20260921T003000+0900-R15-ELIGIBILITY-TIMEBASE-5A7C2E91` @ `31f6705c56489e0c7907b8f8b3eecb80c4355982`

The active repository object is `research/main-eligibility-timebase-partition-invariance-20260921@0430e98e241ae543a03bc750a3c977fe55d17bb7`, with prospective contract commit `37eb6f1985d77d9caac5da51ce1348ed5c6a9228`. MAIN's last persisted report was still waiting on exact-head CI, but repository/workflow evidence moved after that handoff: CI run `35528770185` at exact head `0430e98e...` completed successfully. The preregistered test asserts the fixed `CALL_COUNT_PARTITION_DEPENDENT_EXACT` conditions: one versus two empty `apply()` calls produce different final eligibility and weight, both matching the exact per-call `eligibility_decay` recurrence, while update count remains matched. This is NON_EVIDENTIARY SYSTEM Architecture evidence only and remains pending fresh MAIN/Analyst terminal mapping; this scout does not promote or reclassify it.

## High-value external findings

### 1. Continuous-time eligibility already provides the clean ordinary reference for a physical-time clock

Doya's continuous-time reinforcement-learning formulation explicitly avoids an a-priori time discretization and derives exponential eligibility traces in continuous time. The important comparison is therefore not "trace versus no trace" but which clock advances the trace. If SparkBrain intends eligibility to represent temporal persistence in model/event time, the ordinary reference is an elapsed-time recurrence such as `E(t+Δt)=E(t) exp(-Δt/τ)`, not a fixed multiplication per host API call.

Source: Kenji Doya, *Reinforcement Learning in Continuous Time and Space*, Neural Computation 12(1), 2000, DOI `10.1162/089976600300015961`.

Impact: the fresh call-count effect is reducible to clock semantics; it does not supply a new learning or memory mechanism.

### 2. Event-driven eligibility can be evaluated lazily from timestamps, so partition invariance does not require time-driven stepping

Event-driven spiking implementations already compute eligibility from stored timestamps when a relevant event arrives, rather than advancing a trace on every scheduler/API tick. The 2023 presynaptic-spike-driven eligibility implementation explicitly uses the latest timestamp to recover the trace value at an event. This supplies a particularly close ordinary Architecture baseline for SparkBrain: store the trace plus last semantic time, and materialize decay only from elapsed timestamps when needed.

Source: *Presynaptic spike-driven plasticity based on eligibility trace for on-chip learning system*, Frontiers in Neuroscience 2023, DOI `10.3389/fnins.2023.1107089`.

Impact: host-call partition dependence is not a necessary consequence of event-driven/local eligibility; timestamp-lazy decay is an established simpler alternative.

### 3. Irregular-time RL treats elapsed duration as information, not the number of observation/API partitions

Time-aware RL work shows that when observation intervals are irregular, discount/state updates should account for physical elapsed intervals; randomly changing segmentation without representing duration changes the induced learning problem. This is conceptually the same reproducibility boundary exposed here: if two partitions encode the same semantic event-time history, a scientific trace should be invariant unless the partition itself is declared part of the task/state.

Source: Kim & Chi, *Time-Aware Q-Networks: Resolving Temporal Irregularity for Deep Reinforcement Learning*, 2021, arXiv `2105.02580`.

Impact: future contracts should distinguish `episode/apply count is the semantic clock` from `episode/apply is transport/scheduling only`; both are legitimate models, but they are different models.

### 4. The fresh result narrows to an Architecture contract choice, not a defect or novelty claim

Repository evidence now supports exact per-call dependence under the fixed synthetic comparator. That does **not** by itself prove the implementation is wrong: a discrete episode clock is a valid design if one `apply()` step intentionally means one unit of scientific time. Conversely, if absolute spike timestamps are the intended temporal semantics, empty extra calls should not silently age eligibility. The decisive missing item is therefore a public timebase contract, not another mechanism experiment.

No Utility request is created. The earlier Utility proposal was superseded into MAIN ownership, and MAIN has already executed the exact one-shot diagnostic; another request would duplicate active/fresh work and risk outcome-responsive continuation.

## Reduction consequence

For future fresh objects, the ordinary ladder should be:

`explicit semantic clock declaration`
→ `discrete episode-step decay if episode count is semantic`
→ `elapsed-time exponential trace if event/model time is semantic`
→ `timestamp-lazy event-driven implementation as an equivalent ordinary realization`
→ `partition-invariance metamorphic check when partition is non-semantic`
→ only then any stronger learning/mechanistic interpretation.

The current object must stop at its preregistered one-shot terminal after fresh MAIN/Analyst review. No sweep, repair, redesign, production patch, or same-object biological/mechanistic continuation is warranted from this literature.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_V05_ELIGIBILITY_TIMEBASE_PARTITION_INVARIANCE_01
  - V05_PLASTICITY_ELIGIBILITY_TIMEBASE
  - ARCHITECTURE_REPRODUCIBILITY
  - V05_EPISODE_SEMANTICS
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONG_ORDINARY_CLOCK_SEMANTICS_REDUCTION. Exact call-count dependence is now
  supported by the preregistered exact-head diagnostic, but continuous-time and
  timestamp-driven eligibility provide established ordinary alternatives. The
  scientific issue is whether apply/episode count is intentionally the semantic
  clock or merely a non-semantic API partition; this is Architecture/reproducibility,
  not a new learning mechanism.
audit_classification: null
prospective_baselines_or_discriminators:
  - explicit discrete episode-step clock baseline when episode count is semantic
  - elapsed-time exponential eligibility E(t+dt)=E(t)*exp(-dt/tau)
  - timestamp-lazy event-driven eligibility implementation
  - partition-invariance metamorphic test for identical semantic event-time histories
  - explicit API contract declaring whether empty apply calls advance scientific time
questions_for_evidence_analyst:
  - Map the successful exact-head diagnostic only to its preregistered SYSTEM terminal after independent review, with no same-object continuation?
  - Require an explicit public semantic-clock declaration before interpreting eligibility_decay as behavioral/biological time?
  - Treat timestamp-lazy and elapsed-time traces as ordinary Architecture baselines rather than mechanism successors?
questions_for_control_brain:
  - Add explicit learning-state clock semantics to the Architecture reproducibility checklist?
  - Keep PRE_FORMAL/FORMAL and H7 unchanged because the fresh result is SYSTEM clock semantics only?
  - Prevent a duplicate Utility request or literature-driven production repair now that MAIN has executed the one-shot diagnostic?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - all canonical terminal classifications and consumed STARTED/control/preserve/evidence refs
  - prospective contract 37eb6f1985d77d9caac5da51ce1348ed5c6a9228
  - initial pre-outcome lint-failure head e66bf9faf01edb916a6bbd976d53acdddc67538e
  - exact diagnostic head 0430e98e241ae543a03bc750a3c977fe55d17bb7 and CI 35528770185
  - no same-object sweep, redesign, production fix, cycle 2, STARTED, TEST, PRE_FORMAL/FORMAL promotion, rescore, research merge, immutable-ref mutation, or scheduler change
utility_request_created: null
```
