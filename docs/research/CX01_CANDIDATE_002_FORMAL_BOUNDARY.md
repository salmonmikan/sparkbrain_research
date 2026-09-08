# CX01 candidate-002 formal boundary

This document defines the one-way boundary between an outcome-blind pre-start package and formal capability execution. It does not authorize execution by itself.

## Current status

| item | status |
|---|---|
| candidate | `cx01-candidate-002` |
| seed band | `370110..370119` |
| independent review | `PENDING` until an exact-package approval is recorded |
| execution seal | `NOT ISSUED` |
| persistent `STARTED` | `ABSENT` |
| formal capability | `NOT EXECUTED` |
| formal score | `NONE` |
| candidate consumed | `NO` |

`cx01-candidate-001`, its rejected freeze `freeze/cx01-001`, and its seed band `269810..269819` remain excluded from reuse.

## Preconditions for any seal

All conditions below are conjunctive. Missing evidence is a hard stop, not permission to infer success.

1. `freeze/cx01-002-source` exists and is immutable.
2. `prepare/cx01-candidate-002` exists and is immutable.
3. The package manifest names the exact source SHA at `freeze/cx01-002-source`.
4. Every package checksum verifies byte-for-byte.
5. The package contains exactly 60 candidate worlds and 420 unscored declarations.
6. The structural novelty audit passes separately for topology, timing, exposure/schedule, and contingency where applicable; anonymous token relabeling is not counted as structural novelty.
7. Ordinary CI and development validation passed at the exact frozen source SHA.
8. The package contains no capability result, formal score, execution seal, or `STARTED` marker.
9. A reviewer distinct from the package/source builder recorded `APPROVE_PRESTART` against the exact package commit.
10. The approval was not superseded by a later package commit or a later request-changes review.
11. No comparator threshold, scoring definition, privilege contract, world, or comparator implementation changed after package review.
12. No result prediction or outcome-directed adjustment was used in source or package preparation.

An approval against a branch name alone is insufficient. It must bind the exact source SHA and package commit.

## Seal contents

A valid execution seal must be created once and contain at least:

- candidate ID and seed band;
- exact source SHA;
- exact package commit and package tree hash;
- complete package checksum digest;
- structural-audit digest;
- privilege, schedule, scoring, schema, and comparator-inventory hashes;
- exact execution command and its digest;
- independent-review PR/review identifiers, reviewer identity, reviewed commit, and submitted time;
- execution environment declaration;
- explicit `rerun_allowed: false`;
- explicit `repair_after_started_allowed: false`;
- explicit `candidate_replacement_after_started_allowed: false`.

The seal must not contain capability outcomes or scores.

## Persistent STARTED semantics

`STARTED` must be committed and pushed before the first capability-producing instruction is executed.

Once `STARTED` exists:

- the candidate is consumed even if the process crashes;
- no rerun is allowed;
- no repair is allowed under the same candidate ID;
- no world or comparator change is allowed;
- no threshold or scoring change is allowed;
- partial artifacts and failure diagnostics must be preserved;
- a replacement experiment requires a new source revision, candidate ID, and disjoint seed band.

This prevents an unsuccessful formal attempt from being silently converted back into a pre-start candidate.

## One-way formal sequence

1. Revalidate exact source/package/review bindings.
2. Create and preserve the execution seal.
3. Commit and push persistent `STARTED`.
4. Execute the frozen formal command once with retry disabled.
5. Preserve stdout, stderr, environment, exit status, and all partial artifacts.
6. Hash and lock raw capability artifacts before scoring.
7. Apply only the frozen scoring implementation to the locked raw artifacts.
8. Preserve scored outputs and a final status record without modifying raw evidence.

## Failure semantics

| failure point | disposition |
|---|---|
| before seal | remain `NOT STARTED`; correct preparation evidence or reject candidate as appropriate |
| after seal, before `STARTED` | no capability execution; investigate seal transaction without changing candidate evidence |
| after `STARTED`, before raw completion | candidate consumed; preserve failure/partial evidence; no rerun |
| after raw lock, scoring failure | raw remains authoritative; repair scoring only under a separately reviewed scoring-recovery protocol that does not rerun capability |
| checksum or binding mismatch | hard stop; do not issue seal or start |
| review no longer applies to exact package | return to independent review; do not start |

## Non-authorizations

This document does not authorize:

- formal execution without exact-package independent approval;
- self-approval by the builder;
- reuse of candidate-001;
- rapid-cycle or comparator-specific tuning;
- result-driven world redesign;
- rerun after `STARTED`;
- interpreting package/audit success as comparator capability success.
