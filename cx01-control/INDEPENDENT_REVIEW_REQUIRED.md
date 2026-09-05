# CX01 Candidate-001 — Independent Freeze Review Required

Status: **OUTCOME-BLIND PACKAGE PREPARED / FORMAL CAPABILITY UNOPENED**

This control package was prepared from the exact frozen source:

```text
freeze ref: freeze/cx01-001
source SHA: f2c5ead5afda7d731033d585511ea68dc066a162
```

Candidate declaration:

```text
generation: cx01-candidate-001
seeds: 269810..269819
purpose: formal
```

Frozen hashes:

```text
candidate_spec_hash:      aba791ade53feb89950ef0f0b673c68f9ef91b82b1ed9f0560ab9f2576e2fc30
candidate_grid_hash:      6c81390a785deb0ea8fe30e35186361621dc31bb1e42fe09d7c63ab221575db7
declaration_bundle_hash:  c77ff6cb90207d9ce02be328fff245926d1f40e196bb86f9b5eeb5d533404613
freeze_manifest_hash:     e440dbb6fb6ba06e0196380d04c3c177f647a071a0a7c564fa2e817d6eebc915
```

Declarations are retained exactly as `declarations.jsonl.gz`. Its deterministic gzip and expanded-byte hashes are recorded in `declarations_encoding.json`.

## Independent reviewer checklist

The reviewer must be genuinely independent of the freeze builder and should verify, without executing candidate capability:

- `freeze/cx01-001` still resolves exactly to the frozen source SHA;
- candidate seeds do not overlap historical or CX01 development/test/fixture evidence;
- `candidate.json` recomputes the candidate specification hash;
- the frozen source recomputes candidate grid and declaration bundle hashes;
- all 420 declarations are `unscored`, with no capability result and no measurements;
- the complete freeze manifest recomputes byte-for-byte in semantic fields;
- comparator inventory, privilege inventory, schedule policy, scoring policy, result schema, and resource schema hashes match;
- no `execution_seal.json` exists before approval;
- no `STARTED.json` exists before approval;
- no formal candidate capability has been executed or inspected.

Only after independent approval may an execution seal be issued. Creation of `STARTED` remains a later, irreversible step.

## Explicit non-events

At package preparation time:

```text
formal capability executed: NO
formal outcome inspected:   NO
independent seal issued:     NO
persistent STARTED created:  NO
formal workflow dispatched:  NO
```
