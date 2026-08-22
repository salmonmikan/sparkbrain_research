# Frozen primary result subset

This is the bounded release smoke subset, not the full evaluation suite.

| Result | Run | Accuracy/check fraction | Coverage | Evidence boundary |
|---|---|---:|---:|---|
| Phase-0 reference | R0001 | 0.6400 | 0.9367 | hand-authored software validation |
| C02 SwitchWorld | R0006 | 0.5965 | 0.9234 | controlled synthetic E2 |
| C02 MultiObjectWorld | R0006 | 0.0000 | 0.0000 | retained negative result |
| C04 learned held-out | R0008 | 0.6634 | 0.7796 | 60 controlled episodes; load collapse retained |
| C07 hybrid canonical | R0005 | 1.0000 | n/a | 9 frozen behavioral checks, one scenario |
