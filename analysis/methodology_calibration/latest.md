# SparkBrain Methodology Calibration Audit — R105

- schema_version: `2`
- generation_id: `METHCAL-20260924T123549+0900-R105-9F3C7A21`
- generated_at: `2026-09-24T12:35:49+09:00`
- authority_scope: `METHODOLOGY_ADVISORY_ONLY`
- supersedes: `METHCAL-20260924T111949+0900-R104-6B8E2D41`
- overall_classification: `WELL_CALIBRATED`
- new_scientific_result: `false`

## Executive calibration

This is a material positive transition from R104. The prior H7 end-to-end bridge/controller pin defect was repaired prospectively without changing H7 science. A fresh Evidence Analyst R114 independently re-fetched and exact-bound the repaired controller/bridge bundle and issued one-shot `GO_ONCE` authority. The bridge subsequently dispatched the exact formal workflow.

Authoritative repository refs now show one fresh H7 START identity and one remotely preserved target-blind raw artifact. The raw preserve commit is also referenced by a `freeze/h7-r5-*` tag. No H7 `formal/`, `sealed/`, or `evidence/` final tag is present at this audit snapshot. Therefore the current identity has crossed the irreversible START boundary and is `CONSUMED_ONE_WAY`, while final scoring/sealing remains unobserved.

Candidate #35 remains terminal. The independent treatment/readout support audit has now been canonically recognized only as orthogonal `REVISIT_TRIGGERED` metadata; no old ID was reopened, no successor exists, no Revisit Forge test was authorized, and no confirmatory credit was inherited.

## Prior-history-first reconstruction

R104 was read before current state. R104 classified the programme `MIXED_CALIBRATION` because (a) the repaired H7 controller was internally self-consistent but the dormant bridge/request still pinned the pre-repair controller, and (b) Candidate #35 had a plausible candidate-specific Revisit signal awaiting fresh Analyst adjudication.

Current authoritative reconstruction:
- stable main: `d16403414fc7abebd23075fc401240971b8eb91d`
- frozen H7 science: `2f30b93f8f3cf226ef55ed5af7e341089d2c3c80`
- repaired H7 controller: `af3aa97574c365e3e918c3d4d012faa4886760d0`
- current exact launch workflow blob: `1c4e2199740397c1afbbcc66e89d83f41fe54b21`
- Evidence Analyst R114 commit: `1824290d67fdf06494c3849fa687997ec29137cf`
- Control R55 commit: `7fad3ddb4d9c2fab9415c166a09de904358da529`
- bridge dispatch state: `977e0241f390f6504ebfa4a27a389a487751038c`
- START commit: `52b17b785364f96cc2e95507b2336252459d5352`
- preserve commit: `a5e76e7eb117e0270cfdc138fb9da30d696aa7c0`
- freeze tag points to the preserve commit
- existing authoritative `evidence/*` tags: exactly 5; no H7 final evidence tag at snapshot

Ops records are used only as control-history inputs. START/preserve/freeze and final-tag absence were independently re-fetched from repository refs.

## Development iteration calibration

`KEEP`.

The H7 development object was `RESULT_EXPOSED_DEVELOPMENT / R5_UNCHANGED` before formal launch. The preceding controller/bridge changes were implementation/binding repairs only: no metric, scorer meaning, comparator, threshold, seed/exclusion policy, intervention, resource contract, hypothesis, falsifier, success criterion, or scientific source changed.

The important state transition has now occurred: once `control/h7-r5-...-started` was created, this identity ceased to be development and became `CONSUMED_ONE_WAY`. From that point, even a purely infrastructural failure cannot authorize same-identity repair/retry. The current identity must be preserved as-is and later adjudicated by a fresh Analyst.

Cycle 3 remains a reassessment point, not an automatic cap. No evidence of cycle-count-driven terminalization was found.

## PRE_FORMAL calibration

`KEEP`.

The programme allowed meaningful bounded development and no-result infrastructure repair while H7 remained PRE_FORMAL, without awarding independent confirmatory credit. READY meant the next formal test was well-defined and launchable after exact binding, not that the candidate had already succeeded.

No hidden second formal gate was introduced: after exact preconditions were satisfied, one fresh identity was actually allowed to cross START.

## FORMAL one-way integrity

`KEEP`.

The current workflow prospectively enforced:
1. exact current Analyst generation/commit and one-shot authority;
2. exact controller and exact frozen science;
3. unused one-way namespaces before identity;
4. locked runtime/preflight before identity;
5. create-only START;
6. target-blind raw generation only after START;
7. remote raw preservation to a create-only preserve ref;
8. a freeze tag pointing to that exact preserve commit;
9. target-side scoring only after remote preservation is verified;
10. create-only final `formal/`, `sealed/`, and `evidence/` refs.

Observed repository state matches the critical early ordering:
- exactly one H7 START ref exists;
- the START bundle binds Analyst R114, controller, frozen science, runtime, scorer and protected-evaluation commitment;
- one preserve ref exists;
- its manifest says `preserve_before_target_access: true`;
- the freeze tag points to the preserve commit;
- no H7 final formal/evidence/sealed tag exists yet.

The workflow also checks the H7 one-way namespaces before identity. Therefore a rerun/re-entry after the existing START/preserve refs should fail before a new identity can be created. This materially protects the one-shot rule.

Current audit disposition: the H7 identity is already consumed. Do not rerun, retune, rescore, repair, or silently restart it. If scoring succeeds, independently verify final refs. If any infrastructure failure occurs after START, preserve that failure and require fresh Analyst adjudication rather than retrying.

## Revisit / resurrection calibration

`KEEP` for trigger sensitivity and anti-laundering; `INSUFFICIENT_EVIDENCE` for actual `REVISIT_FORGE_TEST` and `REVISIT_CANONICALIZE`.

Bootstrap remains complete for all 34 terminal current objects:
- `CLOSED_STRONG`: 1
- `DORMANT_REVISITABLE`: 19
- `DEFERRED_INDEPENDENT_REIDENTIFICATION`: 13
- `REVISIT_TRIGGERED`: 1

Candidate #35 is the sole triggered object. This is a useful live test of the ledger: a candidate-specific independent audit found that the old R100 treatment changed non-receptor state while the declared response was receptor spikes, so the treatment-to-readout causal opportunity was not demonstrated by that development negative.

Calibration is currently correct because:
- #35 remains `TERMINAL_FOR_CURRENT_OBJECT`;
- its historical result is not rewritten;
- confirmatory credit remains zero;
- no old ID is reactivated;
- no automatic successor is created;
- no Forge probe is run without a dedicated Revisit decision.

This is evidence against over-terminalization: the system noticed a meaningful changed-understanding trigger instead of forgetting the line. It is also evidence against zombie inflation: recognition of the trigger did not revive the old hypothesis.

The next valid step, if any, is a dedicated fresh Revisit decision. A `REVISIT_FORGE_TEST` may test only the new causal-opportunity/readout-sensitivity rationale and should try to kill it cheaply. It must not rerun or retune the old priming experiment. `REVISIT_CANONICALIZE` remains untested and would require a fresh candidate ID, a meaningfully distinct question, fresh reduction/comparator/falsifier contract, informative negative outcome, and zero inherited credit.

## SYSTEM / MECHANISM successors

`KEEP`.

No same-object post-outcome SYSTEM→MECHANISM upgrade was observed. Candidate #35 remains SYSTEM and terminal. No fresh successor has been manufactured merely by renaming the old object. The current Revisit trigger may eventually motivate a fresh successor, but only after independent Revisit gating and a full fresh prospective contract.

No concrete legitimate successor is currently being suppressed: #35 is no longer forgotten, but it has not yet earned a successor.

## Theory / Forge calibration

`KEEP`.

Theory and Fast Forge remain separated from canonical evidence and carry zero confirmatory credit. R114 reports no fresh Theory proposal, no Revisit proposal, no Revisit Forge referral and no successor. Fast Forge returned NO_OP rather than self-authorizing work from the #35 trigger. This is the correct anti-rescue behavior.

The actual Revisit Forge-test policy remains untested because no such test has run.

## Funnel / claim-type / observability

Claim-ceiling enforcement remains calibrated. H7 entered formal testing as a MECHANISM candidate under its existing frozen contract; terminal SYSTEM objects were not upgraded.

One observability clarification is now important: the designated Analyst state R114 was necessarily pre-START and described H7 as PRE_FORMAL/READY/QUEUED. Authoritative refs now supersede that operational snapshot for lifecycle reconstruction: the current identity is `CONSUMED_ONE_WAY`. This is not a reason to rewrite R114. The next fresh Analyst should explicitly record the post-START state, irrespective of whether scoring succeeds or fails.

Mechanism supply remains thin. Before launch, H7 was the sole active canonical candidate. This is a throughput risk but not a reason to relax evidence standards. Revisit, Theory and Forge remain appropriate zero-credit supply channels.

## Pass reachability

`KEEP`.

PASS is realistically reachable without weakening evidence standards. The programme has now crossed exact-bound START and target-blind raw preservation under the same prospective contract that enforces one-way scoring. That demonstrates the previous infrastructure gates were not a hidden requirement that demanded prior scientific success.

No PASS/FAIL is inferred by this audit. Final scoring/sealing/evidence refs were absent at the snapshot.

## False-positive / false-negative risks

False-positive / rescue risk: `LOW`.
The main live risk would be treating #35's Revisit trigger as proof or repeatedly probing old R100 conditions until a positive appears. Neither has happened.

False-negative / over-terminalization risk: `LOW_TO_MODERATE`.
Candidate supply remains sparse, but #35 shows that the Revisit ledger can catch a candidate-specific trigger without reopening the object. End-to-end Revisit behavior remains unproven until a real Revisit decision and, if warranted, a bounded new-trigger Forge probe occur.

## Gate classifications

- Hard integrity floor: `KEEP`
- Development-phase monotonicity: `KEEP`
- Cycle-3 reassessment: `KEEP`
- Science-invariant vs science-affecting repair distinction: `KEEP`
- Development observation credit: `KEEP`
- PRE_FORMAL genuine iteration: `KEEP`
- READY semantics / no hidden second FORMAL gate: `KEEP`
- Exact FORMAL binding: `KEEP`
- Fresh identity once / namespace collision guard: `KEEP`
- START → CONSUMED_ONE_WAY transition: `KEEP`
- Raw-before-score: `KEEP`
- Preserve-before-read: `KEEP`
- Same-identity post-START repair/retry: `KEEP` (forbidden and technically guarded)
- Terminal object non-reactivation: `KEEP`
- Fresh SYSTEM→MECHANISM successor contract: `KEEP`
- Revisit ledger coverage/conservatism: `KEEP`
- Revisit trigger sensitivity: `KEEP`
- Revisit rescue-laundering prevention: `KEEP`
- Revisit Forge new-trigger-only behavior: `INSUFFICIENT_EVIDENCE`
- Revisit canonicalization gate: `INSUFFICIENT_EVIDENCE`
- Theory/canonical separation: `KEEP`
- Fast Forge/canonical separation: `KEEP`
- Mechanism-supply health: `CLARIFY`
- Post-START funnel observability: `CLARIFY`
- PASS reachability without standard relaxation: `KEEP`

## Mandatory questions

1. Development phases consistent end-to-end? **Yes.** H7 crossed into a single consumed one-way identity only after fresh exact-bound authorization.
2. Cycle 3 mistaken for a hard cap? **No evidence of that.**
3. Science-invariant vs science-affecting distinguished? **Yes.**
4. Development observations excluded from independent evidence credit? **Yes.**
5. FORMAL one-way integrity unchanged? **Yes so far.** START is unique and raw preservation precedes scoring; final seal/evidence is still pending.
6. Legitimate SYSTEM→MECHANISM successors suppressed/manufactured? **Neither observed.**
7. PRE_FORMAL genuine development? **Yes.**
8. Terminal semantics calibrated? **Yes.** Old terminal objects remain terminal.
9. Revisit ledger catches genuinely changed conditions? **Yes for sensitivity:** #35 became `REVISIT_TRIGGERED` on candidate-specific independent input.
10. Revisit avoids rescue/zombies? **Yes so far.**
11. Revisit Forge probes test new triggers? **Insufficient evidence:** none has run.
12. Bootstrap complete/conservative? **Yes, 34/34.**
13. PASS reachable without weaker standards? **Yes.** The one-way path reached START and remote raw preservation under the unchanged hard floor.

## Prospective recommendations

1. Treat `h7-r5-285a3a206b34c5982b9d4045` as irrevocably consumed from START. No same-identity retry or repair is valid, including after infrastructure failure.
2. Do not infer H7 scientific outcome until create-only final formal/sealed/evidence refs exist and are independently re-fetched.
3. Next Analyst should reconstruct H7 from authoritative refs and explicitly record `CONSUMED_ONE_WAY`; do not rewrite the pre-START R114 history.
4. For #35, require a dedicated fresh Revisit decision before Forge. If Forge is selected, test only the new treatment-to-readout causal-opportunity/readout-sensitivity rationale and try to falsify it cheaply.
5. Keep #35 terminal and zero-credit. Any later canonical successor requires a fresh ID and complete prospective contract.

## Utility request

None. No additional utility proposal is needed to test calibration in this generation.

## Hard-floor confirmation

The auditor did not dispatch experiments, consume identities, mutate research/evidence refs, merge PRs, change schedulers or alter scientific criteria.

No consumed FORMAL identity was rerun, retuned or rescored by the auditor. No historical PASS/FAIL was rewritten. No terminal object was reactivated. No same-object SYSTEM→MECHANISM upgrade was performed. No evaluator/held-out leakage or silent post-FORMAL repair was observed in the audited transition.

## Confidence

`HIGH`.

## Questions for Control / Analyst

- After the observed H7 START, will the next canonical Analyst generation explicitly mark this identity `CONSUMED_ONE_WAY` regardless of whether the downstream score/seal succeeds or infrastructure fails?
- Will Candidate #35 receive a dedicated Revisit decision before any Forge action, with any probe restricted to the newly identified causal-opportunity/readout-sensitivity question?
