# A01 MD-002 P2 candidate-002 — consumed development run

This record preserves the exactly-once development execution state. It is not a formal or held-out result.

- Execution identity: `a01-md002-p2-candidate-002-ef73823f4c667aee2655d0e2`
- Exact source: `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d`
- Source freeze: `freeze/a01-md002-p2-candidate-002-source-20260915`
- STARTED/control: `control/a01-md002-p2-candidate-002-started-20260915`
- Workflow run: `34936519897`, attempt `1`
- Python: `3.11.16`
- Runner: `ubuntu-24.04`, image `20260907.300.1`
- Input digest: `51e589907eb59af863a311cb92b5d0a1bbd4c1dc774f01e21e4f8bce15624c2a`
- Raw Actions artifact ID: `10383369145`
- Raw Actions ZIP digest: `sha256:665846c679228df1d1a7529f437f3b9f3d5824cc4f3b2e4e17c18ac3e9d20228`
- `raw.json` SHA-256: `80871f493d04987a0787135a16b343d7fa462f44cdc77767c581c63a8da2ca7f`
- Canonical raw-envelope SHA-256: `930a32dc257f25fff2fc50e33f039e720009c8938adc12289586510368af0ebe`

## One-way execution outcome

The source/runtime guard passed. Candidate manifest binding passed. Raw acquisition completed exactly once and the raw bundle was successfully uploaded before scoring.

The workflow then failed in the verification step before the frozen scorer ran. The cause was a path-handling error in the verification shell: after changing into `artifacts/v061/a01/md002-p2-candidate-002`, `sha256sum -c raw.sha256` attempted to open the path `artifacts/v061/a01/md002-p2-candidate-002/raw.json` relative to that directory. GitHub Actions therefore reported `No such file or directory` and stopped before producing the workflow-scored artifact.

This failure is preserved as part of the consumed identity. The workflow MUST NOT be rerun and candidate-002 MUST NOT be retuned or reacquired.

## Independent preserved-raw verification and score

The already-uploaded raw artifact was downloaded after the run. Its exact `raw.json` bytes independently match the preregistered digest `80871f493d04987a0787135a16b343d7fa462f44cdc77767c581c63a8da2ca7f`; the manifest, runtime contract, Python-version file, and source-SHA file also match the digests written before acquisition.

Applying only the already-frozen `_score` predicate from `src/sparkbrain/v061_a01/md002_p2_shared_probe.py` at the exact source commit to those preserved observations yields `SUPPORTED_SELECTIVE_CIRCULATION`. No candidate acquisition was rerun and no threshold, protocol, arm meaning, or scoring rule was changed.

Observed development pattern:

- Withheld evidence: both proposals remain co-maximal at confidence `0.5` and both are selected.
- Exact match: the causally addressed target rises from `0.5` to `0.6666666666666666` and is selected alone.
- Exact contradiction: the causally addressed target falls from `0.5` to `0.3333333333333333` and is not selected.
- The non-causal target remains at `0.5`.
- Predicted arrival remains `162.0 ms` throughout.
- The anonymous-world permutation swaps exact-match versus exact-contradiction status for both fixed proposal identities.

The independently derived score is stored in `independent_score.json`. This is a development-only scientific result from the immutable preserved raw evidence, while the workflow itself remains recorded as a terminal pre-score tooling failure. It does not make full MD-002 formal/held-out claims available and does not open N3, P3, P4, or P5 gates.
