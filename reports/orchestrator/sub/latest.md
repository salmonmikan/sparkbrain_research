# SparkBrain SUB — 2026-09-21 06:49 JST

- schema_version: `2`
- generation_id: `SUB-20260921T064900+0900-THEORY-ASMCAUSAL-7A4C91E2`
- mode: `discovery`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- status: `COMPLETED`
- Evidence Analyst: `EVA-20260921T055830+0900-R28-4D7A91C2@cde085b48dde724b2ac814585d7f0757bf16ef63`
- MAIN: `MAIN-20260921T061540+0900-PRIMARY-FUNNEL21-HOLD-R28-4C8A21D7`

R28's qualitative search-space reframe found a fresh independent mechanism object absent from the current portfolio: selective causal contribution of Assembly member units to an already learned prediction. This is distinct from the terminal Assembly-feedback question and does not touch held `CAND-H7-RESP-01` or any MAIN object.

Target=`V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY_DISCOVERY_CYCLE1`; candidate=`CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01`; cycle=`1/3`; evidentiary status=`NON_EVIDENTIARY`; proposed claim ceiling=`MECHANISM`.

Prospective contract `eb5ae27f3ef7f8cca2bcc521e2c3f027a5ab6c42` fixed DEV seed 501, 24 training episodes, one non-held-out MOTIF_X probe, target/comparator selection, ordinary reduction question, and terminal mapping before any intervention outcome.

Result: selected `assembly-0001` (motif-X 10, motif-Y 0). Baseline prediction=`outcome-0`, strongest Assembly=`assembly-0001`, similarity=`0.9433062621147579`, spikes=`9`. Prototype target units `[45,56,63]` each had one baseline spike. The fixed nearest nonmember matching rule selected `[16,17,18]`, each with zero baseline spikes because no exact one-spike nonmember comparator was available. Targeted member suppression removed mature Assembly activation and changed prediction to `null` with 6 spikes; matched nonmember suppression retained `outcome-0`, the same Assembly/similarity, and 9 spikes. Terminal=`SELECTIVE_TARGETED_FUNCTION_LOSS`.

Outcome commit=`1a571db21ff82001407f01cb2c5449f253bfd4e5`; diagnostic workflow=`35539567864` completed/success. Final research head=`0c857a73cf34b58b737f686fd9af60769de3d306`; exact-head CI=`35539682655` completed/success on Python 3.11 and 3.13 through lint, readiness, tests, and bundle validation.

Funnel proposal: `preformal_eligible=true`, but readiness=`NOT_READY`. The prospective nearest-activity comparator was imperfect (1 baseline spike per target vs 0 per comparator), and exact activity-load plus graph-centrality/topological-load reductions remain unresolved. Proposed `hold_class=HOLD_MECHANISM_UNRESOLVED_REDUCTION`, `terminal_state=NONTERMINAL_HOLD`, `queue_state=QUEUED`, next layer=`ARCHITECTURE_STUDY`, recommendation=`CONTINUE_EXPLORING_VIA_PROSPECTIVE_ARCHITECTURE_READINESS_STUDY`. No PRE_FORMAL promotion is recommended yet.

Rolling actual scientific selections become `SYSTEM / SYSTEM / MECHANISM` (`1/3` theory-backward); `theory_backward_exception=null`; `system_priority_exception.used=false`.

No cycle-2 rescue, alternate seed/probe, held-out/confirmatory use, official scorer, FORMAL/PRE_FORMAL execution, Utility request, consumed identity, or stable-main/evidence/preserve/control mutation occurred. Fresh Evidence Analyst classification is required before further work.
