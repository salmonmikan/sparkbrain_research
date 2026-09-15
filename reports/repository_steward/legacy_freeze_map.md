# Legacy freeze branch map

Governance inventory only. This file does **not** redefine canonical scientific status or results. Canonical science remains in git-managed research status/docs and immutable evidence. Existing legacy `freeze/*` branches remain authoritative historical anchors and must not be moved, rewritten, deleted, or force-migrated.

Observed 2026-09-16 06:32 JST.

| Legacy freeze branch | Exact commit SHA | Retained evidence pointer(s), when obvious |
|---|---|---|
| `freeze/a01-md002-p2-candidate-002-source-20260915` | `8044b25f3a7b7767bf1262ea6a99cd6b795e3e8d` | `preserve/a01-md002-p2-candidate-002-34936519897-20260915@d7d48a8ad482acdb18de783c9506c32377530e1e` |
| `freeze/a01-md002-p3-candidate-001-source-20260916` | `cf784e24b0d97a81b382988783ea8490cfc333dd` | raw `preserve/a01-md002-p3-candidate-001-raw-20260916@908e3d35f2ced7efe01b778d19f22882543154bc`; scored `preserve/a01-md002-p3-candidate-001-scored-20260916@8ffe8dfa8057595c2998c4a7b634d37a80ffa7b5` |
| `freeze/cx01-001` | `f2c5ead5afda7d731033d585511ea68dc066a162` | no exact one-to-one preserve pointer asserted here |
| `freeze/cx01-002-package` | `c104be281285d52a732d5366fe36209d5688d973` | formal preserve `preserve/cx01-candidate-002-formal-34742073336@6d45928827209cd763a2879494d85838df38b96f` |
| `freeze/cx01-002-source` | `e8483968ce43076b4c3fd04c76e62106e2031769` | formal preserve `preserve/cx01-candidate-002-formal-34742073336@6d45928827209cd763a2879494d85838df38b96f` |
| `freeze/rv01-r01-15-development-source` | `a46096458446e3d101c5a951dba4efd7db1ee0ae` | `preserve/rv01-r01-15-attempt-001@cdce4490f4be9e4b6ccc42342c941de0a2f05187` |
| `freeze/rv01-r01-16-capability-source-20260915` | `02b3d80744d0eb10cb0d90fc38d3c55729d7ab99` | `preserve/rv01-r01-16-capability-20260915@0a25eac227d7ac0e8dbd5532d450ed2d50efa105` |
| `freeze/rv01-r01-16-construction-census-source` | `7ed3a7532fc66ac81d78f20da819442eae1b4780` | canonical attempt `preserve/rv01-r01-16-construction-census-34881254582@63cdf08edb438290e4a04f2fdb12d0cfdca0d6f8`; duplicate integrity incident `preserve/rv01-r01-16-construction-census-34881331776@bd0274833f1ce75466c83ee5f9b9f06259456ad1` |
| `freeze/rv01-r01-17-real-delay-source-20260915` | `5ecb459b609b393ff837f57cc138f1eb44c1b255` | raw `preserve/rv01-r01-17-real-delay-raw-20260915@fceb3663c7a880d82593e6c1efe52fcd1ad0c00a`; scored `preserve/rv01-r01-17-real-delay-scored-20260915@d4737d52ecbb2306d9f00f99366f0ad6424327be` |
| `freeze/rv02-rd003-development-source` | `79a949568b2a9a8ee18c40e9b356c564422c0127` | `preserve/rv02-rd003-attempt-001@cfe0903b6f2e1d16a6b5581ae004502dabdf62b5` |
| `freeze/rv02-rd004-development-source` | `75268dd804f0ef113869be172adf575ac22523a0` | `preserve/rv02-rd004-attempt-001@2efaf81119a32087b2102bbdbff1af61cbc6bf16` |
| `freeze/rv02-rd005-d1-source-c60b7fd8-20260914` | `c60b7fd8d3889ee969f505d921e7d31c990871e6` | `preserve/rv02-rd005-d1-96634541-20260914@d1fdd67ea197b879c52942c4a34e7d39a0a40698` |

## Prospective migration rule

When safe annotated-tag creation and namespace protection are available, a legacy branch may receive a tag mirror **only** when the mapping is scientifically unambiguous and the tag points to exactly the same commit SHA. The legacy branch remains preserved after mirroring. Never retarget or delete an authoritative tag after creation/consumption.

Current migration status: **0 legacy branch mirrors created; 12 legacy freeze branches inventoried; Git tags = 0; repository rulesets = 0.**
