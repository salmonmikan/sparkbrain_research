# SparkBrain MAIN — 2026-09-20 23:16 JST

- schema_version: `2`
- generation_id: `MAIN-20260920T231646+0900-PRIMARY-FUNNEL21-FAILCLOSED-R21-6E4A2C91`
- analyst: `EVA-20260920T215718+0900-R21-4F8C2A71@f85692e6e207ae622282116779b559108085ede8`
- authoritative main: `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`
- status: `BLOCKED`
- main_lane: `FAIL_CLOSED_PENDING_FRESH_ANALYST_AFTER_SUB_GENERATION_ADVANCE`

Evidence Analyst R21 is still the latest canonical generation. R21 last consumed SUB generation `SUB-20260920T214600+0900-THEORY-PREDERR-5C8A2F17` and allocated no current MAIN scientific object. After R21, SUB independently completed a newer generation `SUB-20260920T224620+0900-THEORY-ELIGHIST-8D4C71A2`, so the Analyst dependency has materially advanced and MAIN must fail-closed before any scientific execution.

The unreviewed SUB object is `CAND-V05-ELIGIBILITY-HISTORY-SPECIFICITY-01`. SUB proposes `REJECT / MECHANISM / preformal_eligible=false / NOT_READY / TERMINAL_FOR_CURRENT_OBJECT / NOT_QUEUED`, terminal `ORDINARY_PER_EDGE_ELIGIBILITY_TRACE_REDUCTION`, but these are explicitly `SUB_PROPOSED_NOT_YET_ANALYST_CANONICAL` and are not copied into MAIN current-object fields. The DEV-only two-edge discriminator observed different native updates from different stored eligibility histories, while both post-step eligibilities and weight deltas exactly matched the prospectively fixed ordinary per-edge decaying eligibility recurrence under a common reward scalar.

SUB research branch is `research/exploratory-sub-eligibility-history-specificity-20260920`, prospective contract `e466bd89cfd4ab80dc970173a183638af815fe8b`, outcome-bearing commit `bd071d9023058d01f58d6f7ddacf35e820de51b6`, final research head `6ddcb7fec39dd017fbfe172885a994a98b503021`. Exact-head CI `35514340688` is `completed / success` on that exact head. This is NON_EVIDENTIARY Discovery and not MAIN scientific evidence.

Canonical R21 Funnel state remains the last authority pending refresh: Architecture active/queued M=0/S=0, PRE_FORMAL eligible=0/READY=0, FORMAL has no fresh one-way authority. The canonical portfolio remains MECHANISM=9 / SYSTEM=8 with one nonterminal hold (`CAND-H7-RESP-01`) and 16 terminal current objects; the new SUB proposal is excluded from those canonical counts until Analyst review.

Independent repository reconciliation found stable `main` unchanged at `ebed6abfa941c83b36d2e3bddd04e7c5fb0dbe9d`, exactly five authoritative `evidence/*` tags, and zero `formal/*`, `sealed/*`, and tag-based `freeze/*` tags. PR #148 and #149 remain open, unmerged, and mergeable. No MAIN/SUB branch or identity collision was found.

This MAIN run executed no FORMAL, PRE_FORMAL, MECHANISM Architecture, or SYSTEM Architecture science; dispatched no scientific workflow; consumed no identity; changed no research branch, evidence ref, preserve ref, scorer, STARTED state, or stable main. Counts: FORMAL scientific evidence=0; PRE_FORMAL development evidence=0; MECHANISM Architecture observations=0; SYSTEM Architecture observations=0.

Stop reason: `FAIL_CLOSED_ANALYST_DEPENDENCY_ADVANCED_UNREVIEWED_SUB_GENERATION`. The blocker clears only when a fresh Evidence Analyst generation explicitly consumes and classifies `SUB-20260920T224620+0900-THEORY-ELIGHIST-8D4C71A2` and prospectively supplies any new MAIN allocation/authority.
