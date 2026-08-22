# Platform matrix

This matrix records tested environments; it is not a claim that unlisted platforms are
unsupported. The dependency-free deterministic reference engine remains the minimum local
path. Learned and spiking experiments use optional extras.

| Environment | Python | Scope | Evidence | Status |
|---|---:|---|---|---|
| Windows 11 10.0.26200 AMD64 | 3.13.3 | core, lab, C02, C03, C07, release tooling | local full suite, Ruff, readiness, bundle validation | pass |
| GitHub Actions `ubuntu-latest` | 3.11 | `.[dev,spiking]`, Ruff, readiness, full suite, bundle | CI run `32596771889`, job `97088902834` | pass |
| GitHub Actions `ubuntu-latest` | 3.13 | `.[dev,spiking]`, Ruff, readiness, full suite, bundle | CI run `32596771889`, job `97088903012` | pass |

## Boundaries

- The CI runner label is recorded exactly as configured. This document does not infer a fixed
  Ubuntu release from the moving `ubuntu-latest` label.
- macOS, ARM, CUDA, MPS, and neuromorphic hardware have not been validated in this release.
- The local learned and spiking evidence is CPU evidence. It is not a hardware-energy result.
- Optional external datasets are acquired separately and are not included in the repository or
  release archive.
