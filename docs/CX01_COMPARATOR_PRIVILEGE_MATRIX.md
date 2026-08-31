# CX01 Comparator Privilege Matrix

Status: **normative for CX01 Wave 1 development**

Privilege metadata is architecture-interpretation information. It does not itself decide pass/fail, but an undisclosed privilege mismatch is an integrity failure.

| Capability / privilege | G3 | G4 | G5 | G6 | G7 | G8-P | G8-R |
|---|---:|---:|---:|---:|---:|---:|---:|
| anonymous token input | yes | yes | yes | yes | yes | yes | yes |
| precise event timestamp used | no | no | no | no | no | yes | yes |
| explicit episode boundary used | no | implicit Assembly segmentation | no | yes | yes | yes | yes |
| higher-order context state | no | explicit sequence Assembly | no | yes | yes | yes | yes |
| fixed anonymous SDR | no | no | no | no | yes | no | no |
| explicit Assembly state | no | **yes** | no | no | no | no | no |
| typed functional heads | no | no | **yes** | no | no | no | no |
| scalar reward privilege in historical architecture | no | no | **yes** | no | no | no | no |
| predictive-state readout | no | no | typed head | no | **yes** | **yes** | timing/replay state |
| global replay / excitability switch | no | no | no | no | no | no | **yes** |
| generated event may train model | **no** | **no** | **no** | **no** | **no** | **no** | **no** |
| evaluator context ID visible | **no** | **no** | **no** | **no** | **no** | **no** | **no** |
| correct target visible | **no** | **no** | **no** | **no** | **no** | **no** | **no** |

## Interpretation rules

### G3 vs G6

A G6-only improvement may be attributed to higher-order recent context only after the `max_order=1` equivalence test remains green.

### G6/G7 vs G8

The TIMING family intentionally holds the anonymous token sequence constant while changing temporal spacing. G6/G7 do not use precise timestamps; G8 does. Therefore G8-only success in TIMING is an intended capability separation rather than an efficiency or global-superiority claim.

### G8-P vs G8-R

G8-P and G8-R share the same local learned association substrate. G8-R alone has an explicit replay/excitability mode that permits multi-step autonomous continuation. Any G8-R-only causal-intervention benefit must be reported together with this privilege.

### G4/G5 historical privilege

G4 and G5 are retained as historical v0.6-era anchors. Their original architecture privileges are disclosed even when a particular CX01 family does not actively exercise all privileged heads.

## Prohibited hidden inputs

No CX01 comparator adapter may receive:

```text
correct target
correct branch
semantic label
human role label
future test event
held-out score
Primary internal state
evaluator-selected winner
```

If a future comparator genuinely requires an additional architectural input, that input must be added to this matrix before formal candidate generation and must be supplied by a shared architecture-neutral world contract where applicable.
