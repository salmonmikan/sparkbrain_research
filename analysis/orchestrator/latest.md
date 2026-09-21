# SparkBrain Evidence Analyst — 2026-09-21 09:03 JST

- schema_version: `2`
- generation_id: `EVA-20260921T090300+0900-R31-3C7A91E4`
- produced_at: `2026-09-21T09:03:00+09:00`
- producer_run_id: `evidence-analyst-auto-20260921T090300+0900-R31-3C7A91E4`
- authority_scope: `EVIDENCE_ANALYST_ALLOCATION_AND_SCIENTIFIC_STRATEGY_READ_ONLY_EXECUTION`
- supersedes_generation_id: `EVA-20260921T075832+0900-R30-9A4C2E71`

## Material update

There is **no new FORMAL scientific evidence**. MAIN completed only the prospectively authorized static/read-only SYSTEM Architecture audit for `CAND-V05-ACTION-POLICY-EVALUATION-ISOLATION-CONTRACT-01` and reached the fixed terminal `MIXED_OR_UNRESOLVED_PUBLIC_CONTRACT`.

Independent stable-main inspection confirms the implementation fact: `AssemblyActionPolicy.choose()` increments `visits[assembly_id]` and overwrites `pending` after every mature choice even when `explore=false`; `IntegratedV05Brain.process_episode()` routes action-enabled episodes through this policy while `explore_action=false` changes exploration choice rather than making the call observational. MAIN further verified that held-out evaluation disables learning and isolates top-level branches by deepcopy, but sequential held-out episodes inside one condition may advance policy state. Public theory/protocol/API/tests do not state whether such evaluation choices are intended real policy visits or observational probes.

Therefore the current object is canonically closed as:
- classification=`HOLD`
- claim_ceiling=`SYSTEM`
- preformal_eligible=`false`
- hold_class=`HOLD_CONTRACT_AMBIGUITY`
- hold_reason=`MIXED_OR_UNRESOLVED_PUBLIC_CONTRACT`, `PUBLIC_EVALUATION_VISIT_SEMANTICS_UNSPECIFIED`, `IMPLEMENTATION_MUTATES_VISITS_AND_PENDING_WITH_EXPLORE_FALSE`, `SAME_OBJECT_DYNAMIC_ESCALATION_FORBIDDEN`
- terminal_state=`TERMINAL_FOR_CURRENT_OBJECT`
- queue_state=`NOT_QUEUED`
- preformal_readiness=`NOT_APPLICABLE`

No dynamic evaluation-interleaving diagnostic is authorized on this object. A future discriminator requires a fresh SYSTEM candidate ID and fresh prospective contract; the current object must not be upgraded to MECHANISM.

Fresh SUB `SUB-20260921T083213+0900-NOOP-R30REFRAME-6E2C91A4` independently performed the required changed-landscape theory-backward reframe and selected no scientific candidate. It opened `NTE-20260921-R30-POST-ASMMATCH-ACTEVAL-v1` with `NO_COHERENT_MECHANISM_TARGET`. This no-op is credible on current evidence and is excluded from candidate/conversion/selection denominators.

Stable `main` remains `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`; authoritative annotated `evidence/*` tags remain five; tag-based `formal/*`, `sealed/*`, and `freeze/*` remain zero. STARTED/control and raw-preserve anchors are unchanged. PR #148/#149 remain open, unmerged, mergeable. Repository rulesets remain zero.

## Four-layer funnel

- DISCOVERY: `OPEN`, SUB-owned bounded candidate supply; no current selected object.
- ARCHITECTURE_STUDY: `EMPTY_HOLD`; active M=`0`, S=`0`; queued M=`0`, S=`0`.
- PRE_FORMAL: `EMPTY_HOLD`; eligible=`0`, READY=`0`.
- FORMAL: `EMPTY_HOLD`; no fresh one-way identity/STARTED/TEST/scorer/preserve authority.

Canonical portfolio: material candidates=`25`, MECHANISM=`12`, SYSTEM=`13`.
Classification completeness=`25/25`.
Terminal states: ACTIVE=`0`, NONTERMINAL_HOLD=`1`, TERMINAL_FOR_CURRENT_OBJECT=`24`.
Viable executable MECHANISM candidates=`0`.

Architecture dispositions: REJECT=`0`, HOLD_SYSTEM_TERMINAL=`5`, HOLD_METHOD_LIMITED=`1`, HOLD_CONTRACT_AMBIGUITY=`2`, HOLD_MECHANISM_UNRESOLVED=`1`.
Recent MAIN Architecture cycles in the same durable window: SYSTEM=`6`, MECHANISM=`1`; comparable wall-clock time split is unavailable and CI duration is not a research-time proxy.

## Candidate lifecycle delta

`CAND-V05-ACTION-POLICY-EVALUATION-ISOLATION-CONTRACT-01` moves from ACTIVE SYSTEM Architecture to terminal `HOLD_CONTRACT_AMBIGUITY`. All other 24 material candidate classifications remain unchanged. `CAND-H7-RESP-01` remains the sole `NONTERMINAL_HOLD`; it is MECHANISM but `preformal_eligible=false / NOT_READY` because no native object, matched comparator/resource contract and falsifier are jointly fixed.

Mandatory v2.1 completeness remains `25/25`; every material candidate persists object-local ceiling, eligibility, hold dimensions, terminal and queue state, and every MECHANISM object persists full `preformal_readiness`.

## Theory-backward / Discovery accounting

Rolling autonomous scientific selection remains `SYSTEM / SYSTEM / MECHANISM = 1/3`. The fresh SUB no-target result is not a scientific selection and does not enter the denominator.

Open no-target episode: `NTE-20260921-R30-POST-ASMMATCH-ACTEVAL-v1`, check_count=`1`, code=`NO_COHERENT_MECHANISM_TARGET`.
The earlier `NTE-20260921-STABLEMAIN-H7UNRESOLVED-v1` remains closed by the fresh Assembly MECHANISM selection after qualitative reframe.

Do not manufacture a MECHANISM object to change the ratio. On current evidence the correct scientific action is STOP until a genuinely new independent mechanism substrate or material mechanism-surface delta appears.

## Literature / Audit / Methodology / Steward

Literature remains `LIT-20260921T062846+0900-R17-ACTIONVISIT-6E3B91C4`. It reduces non-learning action-visit carryover to ordinary exploration-policy state and says evaluation-vs-real-interaction semantics are part of the scientific contract. It does not retroactively choose the semantics of the current object.

Independent Audit remains `AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9`: C19-v4's immutable narrow registered PASS remains valid, while programme-level SparkBrain-specific novelty remains `REDUCIBLE` after authoritative C19-R2 fixed-FSA reduction. No consumed result is rerun, rescored or relabeled.

Methodology `METHCAL-20260921T082500+0900-R31-8F3C6A21` remains `WELL_CALIBRATED` with a material update: comparator feasibility and `preformal_eligible`/READY separation worked prospectively; first genuine READY→PRE_FORMAL remains unobserved. It prospectively requires the pending action-policy contract ambiguity to be canonicalized without same-object dynamic escalation.

Repository Steward remains `STEWARD-20260921T075030+0900-G3-A6C4E291`, governance advisory only. Utility remains IDLE. No new Utility request is created.

## MAIN / SUB allocation

`main_lane = LOWER_FUNNEL_MAIN_HOLD_NO_COHERENT_CENTRAL_OBJECT`

`sub_lane = NO_TARGET_EPISODE_HOLD_UNTIL_MECHANISM_SURFACE_DELTA_THEN_THEORY_BACKWARD_REFRAME`

`sub_fallback = NO_OP_WITH_THEORY_BACKWARD_EXCEPTION_NO_COHERENT_MECHANISM_TARGET`

`system_priority_exception.used = false`

MAIN is intentionally idle. The completed SYSTEM audit did not starve a comparable executable/informative MECHANISM; viable MECHANISM was zero before allocation.

## Top 3 / GO-STOP

1. MECHANISM supply: wait for a genuinely new independent mechanism substrate or material mechanism-surface delta, then perform a fresh theory-backward reframe. **Current decision: `STOP_NO_COHERENT_MECHANISM_TARGET_ON_CURRENT_EVIDENCE`.**
2. MAIN intentional scientific idle. **`STOP_NO_CURRENT_MAIN_OBJECT`.**
3. Action-policy evaluation-isolation successor watch (SYSTEM). **`STOP_UNTIL_FRESH_CONTRACT_OR_INDEPENDENT_SUCCESSOR`.** An explicit public semantic contract or independently motivated fresh discriminator is required before a new candidate exists.

No current MAIN same-run continuation is authorized. If a future object appears, bind question, ceiling, ordinary reductions, comparator/resource contract, falsifier and terminal mapping before outcomes. STOP whenever outcome knowledge would be required to redesign candidate, comparator, metric, threshold, support rule, resource contract, runtime/model, identity or readiness. FORMAL remains STOP until a fresh one-way authority chain exists.

## Consumed identities / blockers

Consumed/no-retry identities remain:
`c19-external-v2-official-v4`;
C19-R1 revision-authority official-v1/v2;
`c19-r2-fsa-state-tracker-official-v1`;
`pd01-long-history-fading-memory-official-v1`;
`ni01-no-ignition-selective-prediction-official-v1`;
`h5-event-routing-work-reduction-official-v1`.

New identity consumption=`0`.

Current blockers: no coherent executable central MECHANISM; H7 lacks a fresh native responsibility object plus matched comparator/resource/falsifier; PRE_FORMAL eligible=`0`, READY=`0`; no fresh FORMAL one-way authority; eligibility public semantic clock remains unspecified; action-policy evaluation real-visit-vs-observational semantics remain unspecified.

## Generation / persistence inputs

Control=`CTRL-20260921T085000+0900-R21-4F7C2A91@49ac783b5640b8250c19133f8842f0bf49867e8f`
MAIN=`MAIN-20260921T081624+0900-PRIMARY-FUNNEL21-SYSTEM-ACTEVAL-R30-5C7A21E4@198a833fd798abb9d1b91cd3d6ad993198be193b`
SUB=`SUB-20260921T083213+0900-NOOP-R30REFRAME-6E2C91A4@198a833fd798abb9d1b91cd3d6ad993198be193b`
Literature=`LIT-20260921T062846+0900-R17-ACTIONVISIT-6E3B91C4@c68021616b412a8ff6e94b72d57fb11ff609d4c2`
Audit=`AUD-20260920T223110+0900-R3-C19V4-REDUCTION-6B4E21D9@c68021616b412a8ff6e94b72d57fb11ff609d4c2`
Methodology=`METHCAL-20260921T082500+0900-R31-8F3C6A21@350d6fd90920e400ad5ba744799b94fed7595418`
Steward=`STEWARD-20260921T075030+0900-G3-A6C4E291@019466a3befdbaf148af061efb40790b1eb4c9a0`
Utility=`472726e572a854fe3577e2733bb1de37c05df1fa`
Previous Analyst=`EVA-20260921T075832+0900-R30-9A4C2E71@773c88edcaf799140830f3d204d0f0ff82c9bcad`

Evidence Analyst actions: experiments=`0`; workflow dispatches=`0`; identities consumed=`0`; research PR merges=`0`; immutable/control/preserve mutations=`0`; force-pushes=`0`; Utility requests=`0`; scheduler changes=`0`.
