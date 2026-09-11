# RV01 R01-12D / R01-12F post-formal review

## Evidence boundary

- R01-12F is consumed, fixed, and not rerunnable.
- This review changes no architecture, threshold, comparator, candidate, or raw result.
- R01-12D retains an aggregate development manifest and world identity hashes, but **not the raw per-world/per-probe rows**. Development claims below are therefore restricted to values directly present in that retained manifest.
- R01-12F retains its formal result manifest and the fixed raw formal result. The formal manifest contains aggregate and family-level final-probe metrics.
- Only the Field has retained intermediate probe detail in the formal raw result; the reservoir has final probes only. Direct phase-by-phase architecture superiority is therefore not identifiable from the fixed evidence.
- The `future_untrained` label in a Field probe describes the route being queried. It is not, by itself, evidence that a route-unique unit activated before exposure. No such provenance claim is made here.

## Evidence binding

| evidence | source | retained binding | cardinality |
|---|---|---|---:|
| R01-12D | `b163117512daca23b613c8a109a544833af7d360` | development manifest payload hash `4f07d2f645fc9319647b49775a6186eba95af4cf567f99b6b5f8f64fbe0ff79e` | 15 worlds / 60 final route probes |
| R01-12F | `83d2c77d8ae3878727d2ed4e9e78bc169ce064b8` | raw SHA-256 `e3f0cef5428c1b9a550c986404c1435952bd23fd0bdc0cc24a73b8e0c9f70ff4` | 50 worlds / 200 final route probes |

The previously quoted R01-12D raw-file SHA is not used as a local reproducibility claim because that raw file is not retained in the repository.

## Reproducible aggregate comparison

These values are directly recoverable from the two retained result manifests.

| phase | architecture | ordered retention | exact-route rate | contamination / route |
|---|---|---:|---:|---:|
| R01-12D | Field | 1.0000 | 0.4000 | 3.6000 |
| R01-12D | reservoir | 0.9000 | 0.4000 | 2.9500 |
| R01-12F | Field | 1.0000 | 0.4000 | 3.6000 |
| R01-12F | reservoir | 0.9017 | 0.4000 | 2.9450 |

The aggregate signature is therefore reproducible from retained manifests: Field ordered retention is higher, exact-route recovery is tied, and Field contamination is higher. That is enough to reject a simple claim of cleaner or generally more selective Field memory.

R01-12D does not retain the raw rows required to independently reconstruct development family tables or phase-role diagnostics. This review no longer presents those unavailable details as independently recalculable development evidence.

## Formal R01-12F family comparison

The formal family values below are directly present in the retained formal manifest.

| family | Field retention | reservoir retention | Field exact | reservoir exact | Field contamination/route | reservoir contamination/route | first-hop F / R |
|---|---:|---:|---:|---:|---:|---:|---:|
| disjoint-routes | 1.0000 | 1.0000 | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 1.000 / 1.000 |
| shared-cue-branches | 1.0000 | 1.0000 | 0.0000 | 0.0000 | 6.0000 | 6.0000 | 1.000 / 1.000 |
| shared-prefix-branches | 1.0000 | 0.7778 | 0.0000 | 0.0000 | 4.0000 | 3.3333 | 1.000 / 1.000 |
| edge-reversal | 1.0000 | 0.9000 | 0.3333 | 0.3333 | 2.0000 | 1.3000 | 1.000 / 1.000 |
| dense-route-load | 1.0000 | 0.8750 | 0.5000 | 0.5000 | 4.5000 | 3.3750 | 1.000 / 0.875 |

### Formal-family interpretation

- **Disjoint routes:** no Field-specific advantage; both systems recover cleanly.
- **Shared cue:** both retain continuations, both fail exact branch recovery, and contamination is equal.
- **Shared prefix:** Field retains more ordered continuation, but exact recovery remains zero and contamination is higher.
- **Edge reversal:** Field retains more, but exact recovery is unchanged and contamination is higher.
- **Dense load:** Field has higher retention and first-hop coverage, but no exact-route advantage and substantially more contamination.

The fixed formal evidence therefore supports a broad continuation/coverage difference, not cleaner route isolation.

## What the fixed evidence does and does not establish

### Hypothesis A — Field is generally a stronger memory substrate

**Not supported as general selective-memory superiority.**

A narrower aggregate statement is supported: under this fixed setup, Field retains more ordered continuation while exact-route recovery is unchanged. The higher contamination prevents treating that as a general quality win.

### Hypothesis B — Field has higher continuation/coverage but lower precision

**Best-supported R01-12 interpretation.**

This simultaneously fits the formal family pattern and the aggregate replication: more ordered continuation, no exact-route advantage, and more off-route activation.

### Hypothesis C — the difference is only over-activation / broader activity

**Viable but unresolved by R01-12 alone.**

R01-12 shows that retention and contamination rise together, but it does not contain a registered activity/breadth-matched discriminator. The earlier wording that “untrained branches activate before exposure” was too strong: the route-role label is not activation provenance, and route-unique future-unit activation is not established by this review.

A later fresh development protocol, R01-13A, was created specifically to test the breadth/activity explanation without reopening R01-12F. Its result belongs to that separate fixed development record, not retroactively to R01-12F.

## Phase-analysis boundary

The formal Field raw includes intermediate-role probes, but the resource-matched reservoir does not retain corresponding intermediate-role records. Any Field-only phase description is therefore descriptive of Field dynamics only and cannot establish Field-versus-reservoir phase superiority.

To avoid turning route labels into causal provenance, this review does not use the `future_untrained` role to infer that an untrained route-specific branch physically activated before exposure. The claim-grade conclusions above rely only on retained aggregate and formal family metrics.

## A01 connection

A functional decomposition remains possible as an interpretation:

```text
RV01 Field
  provides broad continuation / candidate availability
        ↓
A01 external-evidence mechanism
  may later select, weaken, or correct candidates
```

This was not jointly tested by R01-12F and R01-12F was not used to tune A01. It must not be promoted into evidence of causal-lineage specificity.

## Preservation and reproducibility

The derived post-formal manifest is generated only from retained repository manifests by:

```bash
python scripts/build_rv01_r01_12_postformal_review.py
python scripts/build_rv01_r01_12_postformal_review.py --check
```

The generator intentionally excludes development family rows and the old Field training-role diagnostic table because the former cannot be reconstructed from retained R01-12D raw rows and the latter is not needed for the supported claim boundary.

The repository still needs a dated `docs/RESULTS_LEDGER.md` entry binding the R01-12 negative/selectivity findings to fixed evidence before this review should be considered fully merge-ready.

## One-sentence conclusion

> RV01のFieldはresource-matched reservoirより順序付きcontinuationを広く保持する一方、exact routeの回復精度は改善せずcontaminationが大きいため、R01-12単独では選択的記憶の優位性ではなく広い候補保持substrateとして解釈するのが妥当である。
