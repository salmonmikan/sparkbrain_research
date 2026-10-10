# Exact one-shot publication plan

Repository: salmonmikan/sparkbrain_research
Base: 3313974cf0cf7389d7bf1e3f714eb55e0721c0dd
Branch: probe/c12-closure-diagnostic-20261010T1454Z
Commit message: probe: c12-closure-diagnostic-20261010T1454Z ONE_SHOT OBSERVATION_ONLY

Construct one complete tree and commit on pinned main; create the fresh branch
only at that complete commit. Do not first create it at main or inherit the old
probe workflow. Two ordinary main workflows receive only this exact branch's push
exclusion. All other existing workflow blobs stay identical.

Before publication: independent source, trigger and pin review; fresh main and
workflow identity checks; verify branch absence and zero runs for this branch.
Branch collision or changed base/trigger blocks publication. Record reservation
before creating the branch; an uncertain create must be inspected, never repeated.
Exactly one attempt with a one-minute job cap is authorized. INCOMPLETE is terminal.
New public output is limited to closure-cell identity, ordinal, and status. Existing
public hosted-runtime diagnostics remain. No research execution is authorized.
