# A01 MD-002 P2 attribution-kernel technical review

Date: 2026-09-11  
Status: **TECHNICAL REVIEW COMPLETE / EXECUTION AUTHORITY REMAINS UNBOUND**

## Reviewed source

- Research line: `research/v061-a01-n3-adapter`
- Merge commit: `b960622a155194fe2abf531998e8c7ef28ef204d`
- Implemented via PR `#62`
- Reviewed implementation head: `f71416eb12dff4427485b750bf845c18fc17c60e`
- CI: success on Python 3.11 and 3.13 after a non-semantic Ruff line-wrap repair.

## Findings

The P2 attribution kernel is execution-disabled infrastructure, not an MD-002 capability runner. The reviewed code:

1. accepts only a subepisode already present in the fixed outcome-blind P2 schedule;
2. restores one bound P2 arm from the existing serialized L/F/C/R fixture;
3. lets the anonymous world relation, rather than a local-path label or expected outcome, select the returned response target;
4. registers a cloned boundary event and routes returned external evidence through the existing provenance/consistency/A01 credit path;
5. leaves Field state unchanged and explicitly checks this invariant;
6. treats withheld conditions as no-update controls for local learned state and learned consistency state;
7. does not iterate the full registered P2 matrix, open P3/P4/P5, issue an execution seal, or bind MD-002 execution authority.

The synthetic tests demonstrate the intended plumbing property: swapping only the anonymous world relation reverses exact credit/contradiction for the two proposal lineages, while withheld controls leave learned local/consistency state unchanged. This is an engineering validation of the attribution path only; it is not a scientific MD-002 result.

## Integrity boundary

`src/sparkbrain/v061_a01/md002_protocol.py` still leaves both `PINNED_TECHNICAL_REVIEW_ARTIFACT_SHA256` and `PINNED_EXECUTION_AUTHORITY_ARTIFACT_SHA256` unbound. This review does not fill either value and does not authorize capability execution.

No formal/held-out or one-way diagnostic boundary is crossed by this review. A later gate-binding change, if pursued, must remain prospective, bind immutable artifacts explicitly, and receive the authorization required by the governing protocol before any capability is opened.

## Review conclusion

No technical or scientific-integrity blocker was found in the execution-disabled P2 attribution kernel as merged. Safe construction work may continue around additional execution-disabled audit/plumbing, but MD-002 execution remains closed.
