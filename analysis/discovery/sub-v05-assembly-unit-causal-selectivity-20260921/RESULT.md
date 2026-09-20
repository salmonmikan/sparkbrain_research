# SUB Discovery Result — Assembly-unit causal selectivity

- candidate_id: `CAND-V05-ASSEMBLY-UNIT-CAUSAL-SELECTIVITY-01`
- target: `V05_ASSEMBLY_UNIT_CAUSAL_SELECTIVITY_DISCOVERY_CYCLE1`
- discovery_mode: `THEORY_BACKWARD_MECHANISM_DISCOVERY`
- cycle: `1/3`
- evidentiary_status: `NON_EVIDENTIARY`
- prospective_contract: `eb5ae27f3ef7f8cca2bcc521e2c3f027a5ab6c42`
- outcome_bearing_commit: `1a571db21ff82001407f01cb2c5449f253bfd4e5`
- diagnostic_workflow_run: `35539567864`
- terminal: `SELECTIVE_TARGETED_FUNCTION_LOSS`

## Fixed-input outcome

The fixed DEV seed-501 training path yielded `assembly-0001` as the prospectively selected motif-X Assembly (`motif_x=10`, `motif_y=0`, delta=`+10`). On the single fixed DEV probe `seed-501-episode-24-motif`, baseline strongest activation was `assembly-0001` at similarity `0.9433062621147579`, with prediction `outcome-0` and nine lower-field spikes.

The selected Assembly prototype contained exactly three units, so the bounded target set was `[45, 56, 63]`. Each produced one baseline probe spike. The prospectively defined nearest baseline-spike-participation nonmember matching selected `[16, 17, 18]`; each produced zero baseline probe spikes because no exact one-spike nonmember match was available under the fixed pool.

Suppressing the three Assembly-member units reduced lower-field spikes from 9 to 6, removed the strongest mature Assembly activation, and changed the prediction from `outcome-0` to `null`. Suppressing the same number of prospectively matched nonmember units left the baseline trajectory at nine spikes, retained `assembly-0001` at the same similarity, and retained prediction `outcome-0`.

Per the preregistered terminal mapping, this is `SELECTIVE_TARGETED_FUNCTION_LOSS`.

## Interpretation boundary

This is a bounded NON_EVIDENTIARY Discovery observation only. It supports a narrow causal-selectivity signal against the prospectively fixed equal-cardinality nearest activity-participation comparator, but does not establish a PRE_FORMAL result or a novelty claim.

Comparator quality is incomplete: all three targeted units had one baseline spike while the best available nonmember comparators had zero. Therefore exact activity-load equivalence was not achieved. Graph centrality/topological load also remains prospectively identified as unresolved. These are readiness limitations, not grounds for outcome-responsive repair in this object.

## Funnel v2.1 proposal

- proposed claim_ceiling: `MECHANISM`
- proposed preformal_eligible: `true`
- preliminary readiness:
  - claim_type: `mechanism`
  - supported_reachability: `PARTIAL`
  - functional_consequence: `SELECTIVE_TARGETED_PREDICTION_LOSS_OBSERVED_ON_ONE_FIXED_DEV_PROBE`
  - ordinary reductions specified/controlled: `equal-cardinality nearest baseline-spike-participation nonmember lesion`
  - reductions unresolved: `exact activity-load matching; graph centrality/topological load`
  - comparator status: `PROSPECTIVELY_FIXED_BUT_ACTIVITY_MATCH_IMPERFECT`
  - qualitative support breadth: `single bounded DEV seed/probe`
  - falsifier definition: `fixed prospectively in PROSPECTIVE_CONTRACT.md`
  - open scientific choices: `exact active nonmember comparator reachability; topology/centrality matching contract`
  - formal claim ceiling: `assembly-member causal selectivity beyond matched activity lesion`
  - status: `NOT_READY`
- proposed hold dimensions:
  - hold_class: `HOLD_MECHANISM_UNRESOLVED_REDUCTION`
  - hold_reason: `POSITIVE_SELECTIVE_SIGNAL_BUT_EXACT_ACTIVITY_MATCH_AND_TOPOLOGY_REDUCTIONS_UNRESOLVED`
  - terminal_state: `NONTERMINAL_HOLD`
  - queue_state: `QUEUED`
- candidate next layer: `ARCHITECTURE_STUDY`
- recommendation: `CONTINUE_EXPLORING_VIA_PROSPECTIVE_ARCHITECTURE_READINESS_STUDY`

No cycle-2 rescue, alternate seed, second probe, held-out evaluation, official scorer, FORMAL/PRE_FORMAL execution, threshold change, or post-outcome terminal-semantic repair was performed. Any new outcome-bearing comparator design must be prospectively authorized before execution.
