# SparkBrain Theory Synthesis — R10 NO_PROPOSAL

- schema_version: 2
- generation_id: THEORY-20260927T192843+0900-R10-NO-PROPOSAL-EPOCH-FENCING-7C4E91A2
- produced_at: 2026-09-27T19:28:43+09:00
- producer_run_id: external-theory-auto-THEORY-20260927T192843+0900-R10-NO-PROPOSAL-EPOCH-FENCING-7C4E91A2
- authority_scope: NON_EVIDENTIARY_NONCANONICAL_THEORY_SYNTHESIS_ZERO_EXECUTION_AUTHORITY
- supersedes_generation_id: THEORY-20260927T153101+0900-R9-NO-PROPOSAL-TRANSACTION-IDEMPOTENCE-2C7A91E4
- role: THEORY_SYNTHESIS_ARCHITECT
- schedule_slot: 19:30 JST
- genuinely_new_information: true
- theory_status: NO_PROPOSAL
- revisit_status: NO_REVISIT_PROPOSAL
- new_sparkbrain_scientific_result: false

## Role selection and boundary

The permanent role map assigns the 19:30 JST slot to THEORY_SYNTHESIS_ARCHITECT. Exactly that role was performed. No experiment, scientific scoring, result-bearing dispatch, candidate mutation, immutable-ref mutation, scheduler change or SYSTEM_BUILD allocation was performed.

## New information inspected

1. Forge added a bounded exact-receipt ledger and then an epoch-fenced rotation adapter. The current adapter preserves revision-coordinator state while retiring the delivery namespace, resetting current-epoch receipts and the conservative identity filter, and rejecting stale or unopened future epochs. Its exact prototype head passed the reported Python 3.11/3.13 CI.
2. The adapter explicitly reduces to ordinary epoch fencing, log rotation, rolling hash-chain summarization, POSIX advisory locking and atomic local snapshot replacement. It does not supply distributed consensus, broker fencing, producer quiescence or proof against a producer relabelling an old payload with a new epoch.
3. Evidence Analyst R153 keeps all 35 canonical candidates terminal and authorizes only RD006 v4 learner-boundary definition, implementation and synthetic preflight. Result-bearing work remains stopped. The v4 change is confined to ordinary external-learning eligibility for existing PORT-to-hidden edges while hidden-return learning remains off.

## Decision

No new SCIENTIFIC THEORY PROPOSAL or INTEGRATION DESIGN PROPOSAL is justified.

Theory R6 remains the retained integration design:

`ID-SB-LATENT-SCOPE-PLURAL-REVISION-001`

Its target loop is unchanged:

`observation -> internal scope inference -> plural hypotheses -> abstain/select -> later evidence -> selective revision -> next prediction/action`

The new Forge work closes another operational seam around delivery-state retention. It does not change the target capability, introduce a reduction-resistant mechanism, add a scientific prediction or create a falsifier that would distinguish SparkBrain from established alternatives.

## Retained design reconciliation

A future separately allocated R6 SYSTEM_BUILD may optionally separate:

- semantic revision state: allocator, hypothesis support and committed revision state;
- transport state: epoch, sequence, exact receipts, conservative compacted-identity filter and retired-epoch chain digest.

Rotation may preserve the former while replacing the latter only at an explicit fence. The transport epoch must never encode or proxy latent scope, regime, episode, truth, target, evaluator identity or a correct routing answer. It is delivery metadata, not a learned context identity.

This sharpens the existing R6 acceptance surface without creating a new design:

1. accept only the immediately following epoch at the exact locked next-sequence fence;
2. preserve revision-coordinator state while resetting only current delivery receipts/filter/sequence;
3. reject stale epochs, unopened future epochs, noncontiguous rotation and fence mismatch with complete no-write;
4. preserve epoch/fence/digest state across checkpoint and deterministic replay;
5. fail closed on checkpoint-integrity corruption;
6. demonstrate the producer-mislabel counterexample and avoid an exactly-once or distributed-fencing claim;
7. keep component replacement distinct from interaction ablation.

## Known reductions and limitations

Epoch fencing, bounded logs, Bloom-style conservative filters, hash chains, advisory locks and atomic snapshot replacement are established engineering patterns. They may make a local SYSTEM_BUILD safer and replayable but provide zero inherited scientific credit.

The current prototype does not reconstruct retired receipts, prove membership in the retired history, fence an untrusted producer, coordinate a broker rotation, handle distributed consensus or multi-host leases, or bound all semantic coordinator state. The fixed routing/allocator components remain uncalibrated, and no continuous task, matched comparator, resource comparison or interaction ablation has been run.

## Canonical science and revisit scan

- Canonical funnel: 35/35 terminal; no active or scientifically queued candidate.
- RD005: consumed identity preserved; no reopen, rerun, retune or rescore.
- RD006 v1/v2/v3: closed with zero scientific credit; v4 is construction/synthetic-preflight only.
- SB001: integrated complete NON_EVIDENTIARY_BUILD; unchanged.
- H7: no trigger.
- TH-002: killed; no trigger.
- A01, C19, Candidate #34 and Candidate #35: no trigger.
- R6/Forge reuse is not a Revisit trigger and does not reopen any terminal object.

## Claim boundary

- COMPONENT_FUNCTION: bounded local epoch-fenced receipt rotation is supported only by the reported Forge tests.
- SYSTEM_BUILD: not allocated for R6.
- COMPOSITION_CONTRIBUTION: not established.
- SCIENTIFIC_NOVELTY: not established; scientific credit 0.

## Input generations and refs inspected

- main: cf0bc45262824f1fe282ccd7b785b3ea50be2099
- Human Directives: 3f8bc8d387ad6c8333c43c90b81a80dc3241f0f7
- prior Theory: THEORY-20260927T153101+0900-R9-NO-PROPOSAL-TRANSACTION-IDEMPOTENCE-2C7A91E4 at cf3c49a4affa31e21ed9229983766da7ee064587
- Literature: LIT-20260927T062709+0900-R45-RV02-RD006-REACHABILITY-91C4A8E2
- Independent Audit: AUD-20260924T103104+0900-R10-CAND35-TREATMENT-READOUT-SUPPORT-4E7A2C91
- Evidence Analyst: EVA-20260927T185823+0900-R153-RD006-V4-LEARNER-BOUNDARY-PREFLIGHT at 3ab32e673ad23749da2283db4eab2aa3cf31b4ec
- Forge epoch-fencing prototype: af5fe79be6120a7fc385a441f33c9f4c25365f2c
- Forge epoch-fencing handoff: 13d523fd2aab2f14842ff5a5722946a694b5322c

## Handoff

Evidence Analyst may optionally retain the epoch-fencing adapter as an engineering input if it later allocates the R6 design to a fresh SYSTEM_BUILD. Theory creates no build ID, candidate, contract, execution request or scientific mutation.

No new SparkBrain scientific result.
