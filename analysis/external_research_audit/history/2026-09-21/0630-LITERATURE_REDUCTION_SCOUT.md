# External Literature Reduction Scout — action-policy visit state / evaluation isolation

- schema_version: `2`
- generation_id: `LIT-20260921T062846+0900-R17-ACTIONVISIT-6E3B91C4`
- produced_at: `2026-09-21T06:28:46+09:00`
- producer_run_id: `external-literature-auto-20260921T062846+0900-R17-6E3B91C4`
- authority_scope: `EXTERNAL_LITERATURE_REDUCTION_SCOUT_READ_ONLY_SCIENCE_AND_CONTROL_PLANE_HANDOFF`
- supersedes_generation_id: `LIT-20260921T032811+0900-R16-ELIGIBILITY-CLOCK-2F8C71A4`
- role: `LITERATURE_REDUCTION_SCOUT`
- genuinely_new_information: `true`

## Inputs / authoritative state

Repository evidence was re-fetched independently from all `ops/*` mailboxes. Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; the authoritative annotated `evidence/*` set remains five; tag-based `formal/*`, `sealed/*`, and `freeze/*` remain empty; thirteen legacy `freeze/*` branches remain. Current preserve/control branch families and consumed STARTED/raw-preserve anchors were re-inspected. PR #148 and #149 remain open and unmerged.

Consumed control-plane generations:

- Control Brain: `CTRL-20260921T025500+0900-R19-9D2C4A71` @ `dcdea1bbd1490da004bce69d4b7f4f7b4d37fbd4`
- Evidence Analyst: `EVA-20260921T055830+0900-R28-4D7A91C2` @ `cde085b48dde724b2ac814585d7f0757bf16ef63`
- MAIN: `MAIN-20260921T061540+0900-PRIMARY-FUNNEL21-HOLD-R28-4C8A21D7` @ `6b3bf125b75e7bccc4eef670fb3ca7ee2df4e43a`
- SUB: `SUB-20260921T053500+0900-NOOP-NOMECH-8B3E71C4` @ `64f77557e4c5597791450c407705e7b3659fce62`
- prior Literature: `LIT-20260921T032811+0900-R16-ELIGIBILITY-CLOCK-2F8C71A4` @ `84bb39f359404d8f94a4007116d5a0cad929eeb8`

Fresh Analyst R28 and MAIN R28 contain no new scientific object: Architecture and PRE_FORMAL are empty, FORMAL remains empty, and `CAND-H7-RESP-01` is the sole nonterminal MECHANISM hold. The latest completed MAIN Architecture object remains the eligibility timebase partition diagnostic at `0430e98e...`, already terminal. The freshest prior SUB scientific result not yet covered by Literature is `CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01@d4c23f6...`, whose exact-head CI `35523434869` is successful and whose canonical Analyst disposition is now `HOLD_SYSTEM_TERMINAL`.

## Repository fact being reduced

Stable `AssemblyActionPolicy.choose()` reads `visits[assembly_id]`, uses `actions[visits % len(actions)]` only when `explore=True` and the exploration budget is not exhausted, **then increments `visits[assembly_id]` on every mature call regardless of `explore`** and overwrites `pending`. Integrated v0.5 wiring defaults `explore_action` to `learn_assembly`, so a non-learning episode can suppress exploratory action selection while still advancing the action-policy visit state.

The prospective Discovery reproduced the consequence exactly: inserting one non-exploratory mature choice advanced the counter and shifted the immediately following exploratory action. No reward was required. This is already a canonical SYSTEM terminal; this scout does not reopen it.

## High-value external findings

### 1. Visitation counts are ordinary exploration-policy state, not passive telemetry

Classical multi-armed bandit work formalizes exploration/exploitation as policy behavior driven by accumulated interaction statistics. Modern count-based exploration generalizes actual counts into pseudocounts and uses them directly to alter future exploration; newer methods continue to estimate visitation counts specifically for exploration bonuses.

Sources:
- Auer, Cesa-Bianchi & Fischer, *Finite-time Analysis of the Multiarmed Bandit Problem*, Machine Learning 47 (2002), DOI `10.1023/A:1013689704352`.
- Bellemare et al., *Unifying Count-Based Exploration and Intrinsic Motivation*, NeurIPS 2016, arXiv `1606.01868`.
- Lobel, Bagaria & Konidaris, *Flipping Coins to Estimate Pseudocounts for Exploration in Reinforcement Learning*, ICML 2023, PMLR 202.

Impact: once `visits` drives future action selection, advancing it during `explore=False` is sufficient to explain the SparkBrain effect without any hidden learning, memory or responsibility mechanism.

### 2. Visit counts can define the exploration schedule itself

Boone & Gaujal's 2023 analysis explicitly contrasts a new episode-ending test with existing episodic RL algorithms whose episode lengths are based on numbers of state visits. This is a useful reduction because it shows that a counter can be a clock/resource for the exploration procedure even when reward parameters are not being updated.

Source: Boone & Gaujal, *The Regret of Exploration and the Control of Bad Episodes in Reinforcement Learning*, ICML 2023, PMLR 202.

Impact: `learn_assembly=False` or zero reward does not imply "no learning-state mutation" if the exploration process has its own visit-state dynamics.

### 3. Evaluation protocol is itself part of the scientific contract

Machado et al. document that divergent RL evaluation protocols can materially change what is being measured and propose methodological best practices; Henderson et al. similarly show that implementation/evaluation choices and stochasticity can make apparent RL improvements hard to reproduce or interpret.

Sources:
- Machado et al., *Revisiting the Arcade Learning Environment: Evaluation Protocols and Open Problems for General Agents*, JAIR 61 (2018), DOI `10.1613/jair.5699`.
- Henderson et al., *Deep Reinforcement Learning That Matters*, AAAI 2018, DOI `10.1609/aaai.v32i1.11694`.

Impact: SparkBrain must state whether a non-learning/evaluation call is an **observational probe** whose policy state should be isolated, or a **real policy visit** that intentionally consumes exploration budget. Either choice is legitimate; silently mixing them is an Architecture/reproducibility ambiguity.

### 4. The decisive fresh discriminator is evaluation-interleaving invariance, not another mechanism experiment

Inference from the repository plus the literature: if evaluation is declared observational, inserting an evaluation call into an otherwise identical training sequence should leave the subsequent training exploration action unchanged. A simple ordinary baseline is snapshot/restore of exploration state, or an explicit gate separating `explore` from `update_visit_state`. If the contract instead declares every mature choice a real visit, the current counter mutation is expected.

This should be used only for a **fresh implementation/Architecture successor if independently authorized**. It must not be added as cycle 2 to the terminal Discovery object.

## Reduction consequence

For any future fresh action-policy object, the ordinary ladder should be:

`explicit evaluation-vs-real-interaction contract`
→ `integer visit-counter / round-robin exploration`
→ `count-based or pseudocount exploration under matched information`
→ `evaluation-interleaving invariance if evaluation is observational`
→ only then any stronger claim about endogenous exploration, credit or responsibility.

No Utility request is created: the current object is terminal, the ordinary reduction is source-transparent, and a request now would be literature-driven same-object continuation rather than a new independent information-gain task.

## Knowledge-flow contract

```yaml
role: LITERATURE_REDUCTION_SCOUT
genuinely_new_information: true
affected_lines:
  - CAND_V05_NONLEARNING_ACTION_VISIT_CARRYOVER_01
  - V05_ACTION_POLICY_EXPLORATION_STATE
  - EVALUATION_TRAINING_ISOLATION
  - ARCHITECTURE_REPRODUCIBILITY
  - PROGRAMME_NOVELTY
novelty_or_reduction_impact: >
  STRONG_ORDINARY_EXPLORATION_STATE_REDUCTION. The non-learning visit-carryover
  effect is exactly explained by a conventional stateful exploration counter:
  explore=False suppresses the exploratory branch but not visit-state mutation.
  Count-based exploration literature makes such counters ordinary policy state.
  The remaining question is whether evaluation calls are observational or real
  policy visits; this is Architecture/API reproducibility semantics, not a new
  learning or responsibility mechanism.
audit_classification: null
prospective_baselines_or_discriminators:
  - side-effect-free evaluation snapshot/restore of visit and pending policy state when evaluation is observational
  - explicit separation of explore_action from visit/exploration-state mutation
  - evaluation-interleaving invariance under identical future training sequence
  - explicit alternative contract where every mature action choice intentionally consumes exploration budget
  - matched count-based/UCB/pseudocount explorer before any future novelty claim
questions_for_evidence_analyst:
  - Keep CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01 at HOLD_SYSTEM_TERMINAL with no same-object continuation?
  - Treat visit counters as exploration-policy state rather than passive telemetry and require evaluation semantics to say whether that state may mutate?
  - For a fresh implementation successor, require a prospective choice between observational isolation and intentional real-visit semantics before testing?
questions_for_control_brain:
  - Add evaluation/training policy-state isolation to the Architecture reproducibility checklist alongside semantic-clock isolation?
  - Keep PRE_FORMAL/FORMAL and H7 unchanged because this line is ordinary exploration bookkeeping/API semantics?
  - Avoid Utility or literature-driven repair because the current object is already terminal and source-transparently reduced?
must_not_change_frozen_or_consumed:
  - all consumed C19-v4/C19-R1/C19-R2/PD01/NI01/H5 identities and immutable evidence
  - all canonical terminal classifications and consumed STARTED/control/preserve/evidence refs
  - CAND-V05-NONLEARNING-ACTION-VISIT-CARRYOVER-01 contract f0ebfc02605ccdccea371dbb908aac879a6de5f8, outcome e15e37d0163e3b37973177c29cbeb72728c7e057, result d4c23f6c15b504a89a420b26d0f0d185138a5bda, and CI 35523434869
  - canonical HOLD_SYSTEM_TERMINAL disposition
  - no cycle 2, action-order change, visit-counter repair, exploration-threshold retune, production patch, STARTED, TEST, PRE_FORMAL/FORMAL promotion, rescore, merge, immutable-ref mutation, or scheduler change
utility_request_created: null
```
