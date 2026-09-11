# RV02-RD003 frozen development attempt 001 — failure record

Date: 2026-09-11  
Disposition: **FROZEN DEVELOPMENT ATTEMPT FAILED / NO SCIENTIFIC SCORE / SAME IDENTITY CONSUMED**

This record preserves the first execution of the frozen `rv02-rd003-online-hidden-eligibility-v1` development matrix. It is not a held-out or formal execution. No formal capability was opened.

## Immutable execution identity

- protocol: `rv02-rd003-online-hidden-eligibility-v1`
- frozen source SHA: `79a949568b2a9a8ee18c40e9b356c564422c0127`
- frozen source ref: `freeze/rv02-rd003-development-source`
- workflow run: `34569336139`
- workflow attempt: `1`
- Python: `3.11.15`
- artifact id: `10187176561`
- artifact name: `rv02-rd003-development-34569336139`
- artifact ZIP SHA-256: `77ca1540a2011dde368bcad071e04682c1399fe76a88cda4dcc649f322e169ca`
- manifest SHA-256: `1686f408f03861bc7a1aed42e59250e1b87659433badb315d82db1677a3d55a2`
- raw uncompressed SHA-256: `7b317bf39c69baab64db520ff2d6b01582317b0a0afe25a4cac99f45c7414fc4`
- raw compressed SHA-256: `375811343e49cd5598db3a76befb01c08c91652a07a6f0a2e0a416528ef7152c`
- summary SHA-256: `79ac2766fd79bf6a97556303a524df45a998006106ad4f861d587c83f40e6f58`

The retained compressed raw status bundle is stored at `artifacts/research/rv02/rd003/attempt_001/raw_cells.jsonl.gz` on this preservation line.

## Matrix outcome

Planned cells: 18.  
Complete cells: **0 / 18**.  
Scientific scoring: **NOT RUN / NOT ELIGIBLE**.

The matrix failed in two distinct ways:

| Family | Scales | Failure | Count |
|---|---|---|---:|
| disjoint-routes | 1, 3, 10 | probe cue scheduled at absolute 100 ms after online training had already advanced the Field clock beyond 100 ms | 3 |
| shared-cue | 1, 3, 10 | same past-time probe scheduling failure | 3 |
| shared-prefix | 1, 3, 10 | same past-time probe scheduling failure | 3 |
| opposing-reversal | 1, 3, 10 | `max_events_per_run exceeded` during online training | 3 |
| dense-load | 1, 3, 10 | past-time probe scheduling failure | 3 |
| capacity-pressure | 1, 3, 10 | past-time probe scheduling failure | 3 |

For the 15 non-opposing-reversal cells, training reached the probe boundary but the RD002 probe helper attempted to schedule its fixed absolute-time cue at `100.0 ms`; RD003 online training had already advanced the Field clock well beyond that timestamp. The runtime correctly rejected this with `ValueError: cannot schedule an arrival in the past`.

For all three opposing-reversal cells, online training itself hit the preregistered native event guard and failed with `RuntimeError: max_events_per_run exceeded` before probing. Under the RD003 contract these cells are incomplete and cannot contribute scientific metrics.

## Scientific interpretation boundary

This attempt does **not** establish a positive or negative result for the hidden-eligibility hypothesis. No cell produced a complete E0/E1/ES probe set, so no selective-organization comparison is scoreable.

The past-time probe error is an execution-contract defect caused by reusing the RD002 probe helper, whose absolute `100 ms` cue assumption was valid only when training did not advance the Field clock. Correcting that temporal anchor would change the executable runner after execution began. To avoid post-exposure repair under the same identity, this repository treats `rv02-rd003-online-hidden-eligibility-v1` as consumed by this failed attempt.

The opposing-reversal native-guard failures are separately retained as genuine feasibility failures under this frozen source; they must not be erased by increasing limits under the same identity.

## Next valid transition

Any corrected experiment must use a **new diagnostic identity** and a new preregistration/source freeze. It may preserve the scientific hypothesis and fixed gain/learner parameters, but it must explicitly preregister the probe clock anchor relative to the post-training Field clock and decide prospectively how native-guard failures are represented. It must not reinterpret or overwrite this attempt.

No formal/held-out boundary was crossed in this attempt.
