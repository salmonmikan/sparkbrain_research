# C19 External Validation — Blocked Engineering Readiness

## Outcome

C19 engineering readiness is complete at source
`052413136229dcfa63f08cebe19585134f7cfb98`. C19 and G09 are not accepted. Scientific status is
`not_evaluated`: the official Belief-R test examples were not opened, read, verified, or evaluated,
and no prediction or attribution row was produced.

The retained exact-nine bundle is
`artifacts/v03/c19_external_validation/blocked-readiness-v1/`. Independent validation confirmed
that all nine retained files exactly match the deterministic source generation.

## Preflight result

The machine reason is `missing_truth_free_belief_r_symbolic_adapter`. C19 preregistered an I2
symbolic Oracle condition, but the repository does not contain a preregistered truth-free adapter
from Belief-R natural language to that symbolic-event contract. Using evaluator truth to create the
representation would leak the target, so execution stops before the cache is opened.

This is a blocked engineering-readiness result, not a failed scientific hypothesis. Autonomous,
Oracle, attribution, condition metrics, paired statistics, and baseline outcomes remain
`not_evaluated` or null.

## Exact execution plan

The run manifest contains exactly 85 rows in frozen order:

1. 60 official condition rows: five seeds 5901--5905, each with the 12 ordered combinations of
   three input tracks, two gates, and two entity conditions.
2. 25 baseline rows: the same five seeds, each with the five ordered baseline families.

Every row is blocked during preflight, reports zero output rows, and records that official examples
were not read. `raw_predictions.jsonl` and `attribution_rows.jsonl` are both empty. The baseline
document sets compute, data, optimization, and parameter matching to false for every family and
forbids a winner claim.

## Frozen provenance

- C19 source: `052413136229dcfa63f08cebe19585134f7cfb98`
- Initial disabled preregistration SHA-256:
  `97a2448e2918f3b0a4583520ad2f35d5d47d99813585be7bb3fae32e0b340cfe`
- Accepted C18 source: `3f561254dc7bd2f97cb4784f0632fe0be48093cd`
- C18 execution pin: `c0c242d848588d76015734a309f72fed0bd1d380`
- C18 contract SHA-256:
  `567724ab1088e5e9259c9bb2151ae513eb0ef579fbce6b287c3f6850ed328df8`
- Belief-R revision: `3719f5804c63318037465fecf298a7fd78d99121`
- Belief-R specification SHA-256:
  `ed092dd97a176813f011cdf007d4e34a0b9bcc7c855c22983a31ff82e7b0d63c`
- Belief-R cache SHA-256 recorded as metadata only:
  `b584c18328965cf3eb3d36f2f9ef145c1e15c9bf57bba084982ba18df1fa4153`

The cache content was not read or verified during this readiness work.

## Artifact hashes

| Artifact | SHA-256 |
| --- | --- |
| `attribution_rows.jsonl` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `baseline_matching.json` | `91b144836a0b00cc68fa9aab28d5c1981f7d5570d59200f4e63ead59b7c6c657` |
| `failure_examples.jsonl` | `0640595c93d2e78c4fcf4d5a98eb1ecd78fa6e32745952cc99e0ed2e22d835e5` |
| `frozen_protocol.json` | `ad4562c75f968cca8b9cb0280fcf929f21a69986cf7d6d278b1371e4d8da6496` |
| `metrics_by_condition.json` | `1955bdbaf10d0c01deb94fa5b6987fb397cddd56cd1547a3fb344d13d2a8fd2a` |
| `paired_statistics.json` | `d98b7140359fa039ba9f6203de1bc2e5025839375c3419abdef8848e9522eb6b` |
| `raw_predictions.jsonl` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `report.md` | `e8ca65ae8c877a5ec1161fed98953326c5355d018ab1b894665851977bed9ced` |
| `run_manifest.jsonl` | `00f2485f7484448472987f23c979b8b5829430ff991c2d4b9312c1ac99c75087` |

## Claim boundary

C06 remains the existing negative external result and is neither replaced nor upgraded. C19 adds
no scientific evidence grade. A future official evaluation requires a new preregistration and
protocol after a truth-free adapter is specified and independently audited. The blocked bundle is
immutable readiness evidence and cannot be reclassified as an official C19 run.

Package 0.2.1, persisted schema 0.2, schemas, release metadata, C06/C08 evidence, the initial C19
preregistration, and existing claim grades remain unchanged.
