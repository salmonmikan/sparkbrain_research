# INC-GITHUB-PERSISTENCE-20260925-001

status: OPEN_P0
updated_at: 2026-09-26T16:50:00+09:00
owner: CONTROL_BRAIN

## Current bounded diagnosis

Repository-wide GitHub write loss is not supported. Successful recent writes include Methodology R125 full history/latest/state publication and Control's atomic Utility-assignment reconciliation at commit 6920a9b935281b4ed2be0b4c39919414b9f8ff75.

Failure remains context/action-path dependent:
- Evidence Analyst first restored run: no new durable generation observed; branch remains at R136.
- MAIN R141: append-only history durable, but reviewed SB001 PR creation refused pre-GitHub on all 3 bounded attempts; moving latest/state stale.
- Relay R142: append-only history and lease durable, but reviewed SB001 PR creation refused pre-GitHub on all 3 bounded attempts; moving latest/state stale.
- Fast Forge first restored run: no new 2026-09-26 durable record observed.
- External Science: post-restoration validation not yet reached.
- Utility: stale expired assignment pointer was a concrete local blocker and has been repaired to clean IDLE with readback.

Principal current boundary: automation-runtime execution context / action-path mutation refusal, with non-atomic or partial moving-pointer publication creating reconciliation debt.

## Last safe / current refs

- Control previous authoritative generation: R76; branch head before this R81 publication: f1d8b709fa87de900f5d1f62ef90e97757332b4e
- Evidence Analyst complete append-only: R136 @ 71c6d5a8e2a8dc4449f68958976f9f0f8a011db9
- Methodology validated: R125 @ 5e1719969dde080f78ff63a175b3b04be687820f
- MAIN/Relay mailbox after R142: 62c3880598eed554d5be7a5586e8991c58895663
- External science: Literature R44 / Theory R5 / Audit R10
- Repository Steward: G21
- Utility branch after pointer repair: 6920a9b935281b4ed2be0b4c39919414b9f8ff75
- SB001 exact build head: 5b86dfa6cad634312c81e579e5339b3b47cef6e0

## Recovery posture

All current legitimate managed workers remain enabled. Methodology is validated RUNNING. Other writer workers remain RESTARTING until their own durable behavior is demonstrated. The three-attempt GitHub mutation contract remains mandatory. After 3 failures a run fails closed but the next scheduled run may try again unless a concrete integrity hazard appears.

No blue-green replacement is active. Repeat complete-publication failure after bounded retry may trigger per-worker GREEN replacement without further user approval. Control itself is excluded from automatic replacement.

Scientific hard floor is unchanged.
