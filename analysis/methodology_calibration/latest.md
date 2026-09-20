# SparkBrain Methodology Calibration Audit — 2026-09-20 11:27 JST

schema_version: `2`  
generation_id: `METHCAL-20260920T112723+0900-R11-E3968ACE`  
producer_run_id: `methodology-calibration-auto-20260920T112723+0900-R11-E3968ACE`  
authority_scope: `METHODOLOGY_ADVISORY_ONLY`  
supersedes_generation_id: `LEGACY_GENERATION_UNKNOWN`

## Run disposition

**`MATERIAL_CALIBRATION_UPDATE`**

## Overall classification

**`MIXED_CALIBRATION`** — downgraded from `WELL_CALIBRATED`.

The scientific integrity floor, novelty bar, comparator discipline, reduction-first practice, and post-Architecture STOP behavior remain broadly well calibrated. The material change is the prospective **Funnel Correction v2**. Its motivation is supported by the recent lower-funnel history, but its field-level implementation is not yet observable in the current Control / Evidence Analyst / MAIN handoffs, and several v2 fields need semantic separation to avoid becoming a hidden second Formal gate.

This downgrade is therefore about **candidate-supply and funnel-observability calibration**, not about weakening or repudiating the existing scientific bar.

## Authoritative state independently re-fetched

- stable `main`: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- annotated `evidence/*`: 5 authoritative tags
- tag-based `formal/*`: 0
- tag-based `sealed/*`: 0
- tag-based `freeze/*`: 0
- preserve/control refs remain present; no new one-way Formal identity or evidence observed
- Control Brain: `b35068cbee426c99c3cc1f6dd23053778a2bd88a`
- Evidence Analyst generation: `EVA-20260920T105721+0900-R11-4B7D91C2` @ branch tip `6617b28dd983a4ada1ebb0622bada869ff17b19e`
- MAIN generation: `MAIN-20260920T111421+0900-PRIMARY-ASSEMBLY-LIFECYCLE-C1` @ report branch `5d232d6a5b771478b9d5ecb8b62df85955dd0fd6`
- SUB generation: `SUB-20260920T104200+0900-CKPT-7F3C2A91`
- Literature: `f399e9d14ef6d491135d19161b8c1d7986b94e5b`
- Independent Audit: `d3a9c8d4c4cf8a3e5a0152d7b0749633776ecb56`
- Repository Steward: `e53df976b98d56b8e37a5cbfc20f1aeb84caadeb`
- latest Assembly static Architecture head: `13239163f6fecb2b61ea2189a5a94ba12b6cb3d6`
- Assembly exact-head ordinary CI `35483714573`: `completed/success`
- open PRs remain #148/#149; no science authority change inferred from them

## What materially changed

### 1. Funnel Correction v2 addresses a real candidate-supply imbalance

The recent autonomous SUB window is strongly SYSTEM-heavy:

1. `HOMEOSTASIS_RECEPTOR_DEAD_MASK_DISCOVERY_CYCLE1` — Architecture/API observability semantics; ordinary all-field accounting reduction.
2. `RECEPTOR_SAMETIME_PERMUTATION_DISCOVERY_CYCLE1` — Architecture/API/reproducibility ordering semantics; ordinary stable tie-order + sequential gain reduction.
3. `V05_CHECKPOINT_CONTINUATION_EQUIVALENCE_DISCOVERY_CYCLE1` — engineering/reproducibility correctness; reduced and REJECTED.

That is **0/3 theory-backward MECHANISM selections** in the latest three safe, nonduplicative autonomous SUB selections. The immediately preceding delayed-outcome attribution line is also SYSTEM/API bookkeeping. This is not a retrospective violation — v2 is prospective — but it gives the new one-in-three theory-backward supply rule a traceable empirical motivation.

The correction is therefore not merely accumulated caution. It targets an observed opportunity-cost problem: productive API/config/reproducibility work can fill the lower funnel while central-theory mechanism supply remains empty.

### 2. v2 funnel observability is not yet operationally complete

Current Evidence Analyst state already uses `schema_version=2` for generation metadata, but its material candidate records do **not** yet persist `claim_ceiling`, `preformal_eligible`, v2 HOLD subtype, readiness status, or `funnel_metrics`. Current MAIN's fresh Assembly object likewise has no `claim_ceiling` or `preformal_eligible` field.

Therefore schema-v2 generation metadata must not be mistaken for Funnel Correction v2 adoption. At this audit boundary the correction is **directionally justified but not yet end-to-end observable**.

This is the strongest reason for `MIXED_CALIBRATION`.

### 3. Current MAIN behavior remains scientifically conservative without suppressing SYSTEM value

MAIN's current Assembly mature-capacity Architecture object mapped prospectively to `LIFECYCLE_UNSPECIFIED_AND_SUPPORTED_SATURATION_UNESTABLISHED`. It records the real resource-policy ambiguity — mature candidates have no current reclamation path — while refusing to manufacture saturation, turnover, a dynamic comparator, or novelty. Exact-head CI subsequently completed successfully.

Under v2 this object is naturally **SYSTEM**, not MECHANISM. It remains worth doing because it protects resource semantics and supported-reachability interpretation. That is exactly the kind of SYSTEM exception the new priority rule should preserve.

## Funnel Correction v2 calibration

### `claim_ceiling=MECHANISM|SYSTEM` — `CLARIFY`

The split is useful, but it must mean the **strongest defensible claim ceiling of the current prospective object**, not the topic's origin, prestige, or research worthiness. A SYSTEM object may generate a *fresh, independently motivated* MECHANISM successor if new mechanism evidence appears. The consumed SYSTEM object itself must not be upgraded post-outcome.

Without this transition rule, the binary split creates false-negative risk for legitimate SYSTEM -> fresh-MECHANISM transitions. With it, the split improves claim discipline.

### `preformal_eligible` — `CLARIFY`

This field should mean: *the object is a MECHANISM object that may in principle enter PRE_FORMAL once development choices are sufficiently closed*. It should **not** mean `READY` already, and it should not be granted merely because a candidate sounds mechanistic.

If `preformal_eligible=true` is only ever set when readiness is already `READY`, the two fields become duplicate guards. If it is set at first speculative mechanism wording, it becomes too permissive. Keep the states distinct.

### HOLD subtype taxonomy — `CLARIFY`

The required enum improves observability, especially `HOLD_SYSTEM_TERMINAL` versus `HOLD_MECHANISM_UNRESOLVED`, but the current values mix orthogonal dimensions:

- `HOLD_SYSTEM_TERMINAL` = claim/lifecycle disposition
- `HOLD_CONTRACT_AMBIGUITY` = epistemic reason
- `HOLD_METHOD_LIMITED` = methodological reason
- `HOLD_QUEUED` = scheduling state
- `HOLD_MECHANISM_UNRESOLVED` = claim-development state

These can logically co-occur. A terminal SYSTEM result can also be contract-ambiguous; a mechanism can be queued and method-limited. Keep the required primary subtype, but prospectively record separate machine-readable `hold_reason` and queue/terminal flags so the enum is not strategically selected to hide another state.

### Architecture portfolio MECHANISM / SYSTEM split — `KEEP`

This is scientifically useful so long as SYSTEM results retain genuine Architecture/system/engineering/testbed value and are not treated as failed mechanisms.

### MAIN MECHANISM priority with SYSTEM integrity exceptions — `KEEP`

The priority is a sensible opportunity-cost correction. Require a machine-readable exception reason whenever MAIN chooses SYSTEM over a comparably executable/informative MECHANISM object. Valid exceptions include testbed validity, evidence interpretation, supported reachability, reproducibility, Formal integrity, or no coherent MECHANISM target.

The current Assembly object would qualify through resource/reachability interpretation plus the absence of a coherent mechanism object.

### SUB one-in-three theory-backward Discovery — `CLARIFY`

The rule is evidence-driven by the 0/3 SYSTEM-heavy baseline, but its **effectiveness is not yet demonstrated prospectively**. It should count only safe, nonduplicative autonomous selections. A qualifying theory-backward selection must have a coherent mechanism-level falsifier/reduction question; naming a low-quality API question "mechanism" must not satisfy the quota.

When no coherent target exists, record the explicit no-target reason rather than manufacture one. The next rolling windows should be audited for information gain, not merely quota compliance.

### PRE_FORMAL readiness checklist — `CLARIFY`

The checklist is well motivated if it makes the old development gate explicit. It becomes overconservative if `READY` silently requires scientific success that PRE_FORMAL is supposed to test.

Interpret the fields prospectively as:

- support: claim-local adequacy to justify the next test, not a universal numeric support floor;
- reductions: ordinary alternatives have been specified/controlled enough to make the test informative, not already defeated conclusively;
- comparator: claim-local, matched and frozen where the claim requires one, not an overmatched alternative system;
- reachability: supported possibility appropriate to the claim, not prevalence unless prevalence is claimed;
- falsifier: prospectively specified, not already survived;
- open-choice accounting: outcome-responsive degrees of freedom are closed or explicitly bounded.

`READY` should mean **development readiness**, not likely-to-PASS.

### No universal numeric readiness threshold — `KEEP`

This is an important protection against accidental moving goalposts and against turning heterogeneous mechanism claims into one arbitrary conversion-rate gate.

## Mechanism-supply health

**`AT_RISK_SYSTEM_HEAVY_BASELINE`**

The latest three autonomous SUB Discovery selections are all SYSTEM/engineering/API questions. That strongly justifies a supply correction, but there is not yet enough post-v2 evidence to conclude that the one-in-three rule improves mechanism quality rather than merely changing labels.

The correct audit target for the next runs is the **quality and fate** of theory-backward selections: whether they are coherent, independently motivated, falsifiable, and not forced queue-fillers.

## Funnel observability

**`INCOMPLETE_V2_NOT_YET_PERSISTED`**

Current durable Evidence Analyst / MAIN state lacks the mandatory v2 candidate fields. This is an observability gap, not a scientific-integrity breach. It should be fixed prospectively before using funnel conversion or readiness metrics for policy conclusions.

Do not backfill consumed historical candidates merely to make dashboards look complete.

## PRE_FORMAL gate calibration

**`CONCEPTUALLY_SOUND_BUT_NOT_YET_EMPIRICALLY_CALIBRATED_UNDER_V2`**

No current PRE_FORMAL object exists, so no v2 `READY -> PRE_FORMAL` transition has yet demonstrated pass reachability. The checklist is appropriate if interpreted as development readiness. It would become a hidden second Formal gate if "reductions", "comparator", or "falsifier" are read as already-successful outcomes.

## Gate classifications

| Gate / rule | Classification | Finding |
| --- | --- | --- |
| Hard one-way integrity floor | `KEEP` | Unchanged and non-negotiable. |
| Prospective protocol / raw-before-score / preserve-before-read / exact binding | `KEEP` | No reason to weaken. |
| New-computational-principle novelty bar | `KEEP` | Still appropriate for strongest claim type. |
| Architecture/System value separate from novelty | `KEEP` | Existing lower funnel demonstrates the distinction. |
| `claim_ceiling=MECHANISM|SYSTEM` | `CLARIFY` | Current-object ceiling; allow only fresh prospective SYSTEM->MECHANISM successor, not post-outcome upgrade. |
| `preformal_eligible` | `CLARIFY` | Distinguish eligibility from `READY`. |
| HOLD subtype enum | `CLARIFY` | Useful primary state, but reason/queue/terminal dimensions should be separately observable. |
| Mandatory persistence of v2 funnel fields / metrics | `TIGHTEN` | Current durable streams do not yet expose them. |
| Architecture MECHANISM/SYSTEM portfolio split | `KEEP` | Improves claim separation. |
| MAIN MECHANISM priority | `KEEP` | Good opportunity-cost correction with explicit SYSTEM exceptions. |
| SYSTEM-over-MECHANISM exception logging | `TIGHTEN` | Needed to detect strategic gaming. |
| SUB one-in-three theory-backward rule | `CLARIFY` | Keep quality floor/no-target exception; effectiveness not yet demonstrated. |
| PRE_FORMAL readiness checklist | `CLARIFY` | Development readiness only, not prior scientific success. |
| No universal numeric readiness threshold | `KEEP` | Prevents hidden global gate inflation. |
| Equal-privilege comparator | `KEEP` | Still appropriate. |
| Comparator as claim-local readiness item | `CLARIFY` | Do not require irrelevant/overmatched comparator. |
| Signal-before-reduction | `KEEP` | For promotion/positive claims. Theory-backward Discovery selection may precede signal. |
| Ordinary-control-first reduction | `KEEP` | Prevents novelty inflation. |
| Fresh Analyst STOP after Architecture | `KEEP` | Continues to prevent rescue. |
| Public API permissiveness vs supported reachability | `KEEP` | Recent receptor case demonstrates correct use. |
| Legacy Top-k sparse-support gate | `TIGHTEN` | Historical local weakness remains. |
| Programme-wide replacement numeric support threshold | `INSUFFICIENT_EVIDENCE` | v2 explicitly should not create one. |
| Brittle literal/format-sensitive semantic detector | `TIGHTEN` | Historical extractor warning remains. |

## False-positive / false-negative balance

False-positive control remains strong: SYSTEM edge effects have repeatedly been reduced to ordinary API/resource/serialization semantics rather than laundered into novelty. v2 should further reduce novelty inflation if `claim_ceiling` is assigned before outcome-visible successor choice.

The new false-negative risk is mostly semantic: a rigid binary label could trap a scientifically useful SYSTEM observation even after it motivates a new mechanism question; `preformal_eligible` plus `READY` could duplicate each other; and a readiness comparator could become overmatched. The prospective fresh-successor rule and development-readiness interpretation resolve these risks without weakening integrity.

## Moving goalposts

**`LOW`**, conditional on prospective-only rollout.

Funnel v2 must not rescore, invalidate, upgrade, or relabel consumed/frozen historical experiments. Historical H5 and other one-way results remain calibration examples only. The correction is justified by candidate-supply/observability evidence, not by an attempt to rescue an inconvenient scientific outcome.

## PASS / PRE_FORMAL reachability

**`REACHABLE_BUT_NARROW`**, with one new qualification: **not yet demonstrated under Funnel v2**.

A genuine mechanism still has a realistic prospective path:

theory/native mechanism signal -> fresh `claim_ceiling=MECHANISM` object -> `preformal_eligible=true` once the mechanism question is coherent -> claim-local support/reductions/comparator/reachability/falsifier/open choices made development-ready -> machine-readable `READY` -> PRE_FORMAL -> one-way FORMAL integrity chain.

The historical H5 process demonstrates that the one-way Formal machinery itself is operational, but v2's new readiness transition has not yet been exercised. Do not make `READY` require that the candidate already survived the very falsifier or comparator that PRE_FORMAL/FORMAL is intended to test.

## Novelty versus research worthiness

Still well separated. Homeostasis, receptor ordering, delayed attribution, Assembly lifecycle, and checkpoint correctness all retain or resolve SYSTEM/engineering value without receiving mechanism/new-principle novelty credit. Funnel v2 should make this separation more explicit, not suppress SYSTEM research.

## External calibration

Current Literature and Independent Audit do not justify a stricter global admission threshold. Literature supports ordinary source/population and contract reductions; the H5 audit supports the exact registered algorithmic-work conclusion while explicitly narrowing its interpretation. External evidence should continue to calibrate claim scope and ordinary controls, not define universal readiness numbers.

## Prospective recommendations

1. Implement the mandatory v2 fields in Evidence Analyst candidate records and successor handoffs before treating `funnel_metrics` as policy evidence.
2. Define `claim_ceiling` as a current-object claim ceiling. Permit SYSTEM -> MECHANISM only through a fresh independently motivated prospective successor; never same-object post-outcome upgrade.
3. Keep `preformal_eligible` distinct from `READY`.
4. Keep the required HOLD subtype, but also persist orthogonal hold reason, terminal/nonterminal state, and queued/active state.
5. Log the reason whenever MAIN selects SYSTEM over a comparably executable/informative MECHANISM candidate.
6. Apply the one-in-three SUB rule with a mechanism-quality floor and explicit `NO_COHERENT_MECHANISM_TARGET` exception; audit the next rolling windows for information gain rather than quota compliance.
7. Treat readiness as development readiness. Do not require the candidate to have already won its comparator, reduction, or falsifier.
8. Do not add a programme-wide numeric readiness/support threshold.
9. Preserve SYSTEM Architecture value and testbed-integrity exceptions; do not turn mechanism priority into a ban on systems research.
10. Keep all v2 changes prospective. Do not backfill/rescore consumed historical results for cosmetic funnel completeness.

## Utility request

No new Methodology Utility request created. The highest-information calibration evidence will come from the first few live v2 candidate allocations, the next rolling SUB selections, and the first `READY -> PRE_FORMAL` transition. A separate synthetic prototype would duplicate the live prospective rollout.

## Hard-integrity-floor confirmation

Confirmed unchanged: no rerun/retune of consumed identities; frozen/prospective protocols; raw-before-score; preserve-before-read; exact identity/source/package/runtime/input binding; immutable evidence; no evaluator/target leakage; no silent post-outcome repair.

## Bottom line

The programme's **scientific bar remains well calibrated**, but the new candidate-supply/readiness correction is not yet sufficiently implemented or empirically exercised to call the *overall methodology* well calibrated. `MIXED_CALIBRATION` is the appropriate current classification: keep the hard science gates, tighten funnel observability, and clarify v2 semantics before judging its conversion rates or raising/lowering the scientific bar.
