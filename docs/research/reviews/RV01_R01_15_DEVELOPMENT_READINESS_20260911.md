# RV01 R01-15 exposed-development readiness review

Date: 2026-09-11  
Status: **TECHNICAL REVIEW COMPLETE / USER-AUTHORIZED HUMAN-REVIEW GATE OVERRIDE / DEVELOPMENT ONLY**

## Scope reviewed

- Protocol: `rv01-r01-15-post-spike-suppression-v1`
- Protocol file: `docs/research/RV01_R01_15_POST_SPIKE_SUPPRESSION_PROTOCOL.md`
- Implementation PR: `#60` (`RV01 R01-15: add fixed exposed-development runner`)
- Reviewed implementation head: `6a0b6bc92141647f9859a33a5d556ad8574426ad`
- Merge commit on `research/rv01-endogenous-transition`: `cbd9d0cb2894b7680945af35bac6e4fd5ef5670c`
- CI on reviewed head: success on the repository Python 3.11 / 3.13 matrix.

No R01-15 development outcome had been opened when this review was written.

## Technical/semantic review

The implementation remains within the preregistered exposed-development boundary:

1. It binds the fresh development seeds `141500..141504` and keeps `141600..141609` reserved for held-out use.
2. A single ordinary trained Field checkpoint is created per fresh development world and F0/FA/FR/FAR are restored from the same serialized pre-probe state.
3. FA edits only post-spike adaptation state, FR only the future absolute-refractory interval, and FAR only those two registered post-spike fields.
4. Learned topology / weight / delay state is not retuned by the intervention; connection hashes and intervention records are retained for audit.
5. The fixed resource-matched reservoir remains a shared external reference rather than being tuned separately per Field arm.
6. The runner rejects held-out execution, uses the preregistered fixed development namespace, and refuses to overwrite an existing development result path.
7. Raw emitted-unit traces, intervention records, traversal/readout context, native guard outcomes, and the secondary route-retention/contamination firewall are retained.
8. No historical R01-12F, R01-13A or R01-14A evidence is rerun, modified, rescored or used as mutable input.

I found no technical or scientific-integrity blocker to the one-shot five-seed **exposed-development** execution defined by the protocol. This finding is not a scientific result and is not authorization for held-out or formal execution.

## Human-review governance

The protocol's initial execution boundary calls for independent code review before exposed-development execution. No literal independent human reviewer identity is available to this automation, and none is fabricated here.

The repository owner explicitly authorized progression through stages blocked only on human review. Accordingly, the independent-human condition is transparently recorded as:

`USER_AUTHORIZED_REVIEW_GATE_OVERRIDE / HUMAN_REVIEW_WAIVED_BY_USER`

This waiver applies only to the human-review governance condition. It does not waive the protocol, fresh-source, one-shot, evidence-preservation, held-out, or formal-execution restrictions.

## Allowed next step

After the one-shot development workflow itself is merged and the final exact source is frozen under a new immutable `freeze/rv01-r01-15-development-source` ref, the five-seed exposed-development grid may be executed exactly once from that frozen source. The reserved held-out namespace remains sealed.
