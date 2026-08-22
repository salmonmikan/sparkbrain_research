# Third-party notices for optional Brain Lab tooling

C03 does not add a mandatory runtime dependency to the SparkBrain reference engine. The following direct dependencies are confined to optional `lab` or `dev` extras. Tested versions are recorded in `requirements-lab.lock`.

| Package | C03 role | Tested version | Upstream license | Official source |
|---|---|---:|---|---|
| FastAPI | localhost REST/SSE application | 0.141.1 | MIT | <https://github.com/fastapi/fastapi/blob/master/LICENSE> |
| Uvicorn | loopback ASGI server | 0.52.4 | BSD 3-Clause | <https://github.com/Kludex/uvicorn/blob/main/LICENSE.md> |
| HTTPX | API tests only | 0.28.1 | BSD 3-Clause | <https://github.com/encode/httpx/blob/master/LICENSE.md> |

The bundled Brain Lab frontend uses native HTML, CSS, JavaScript, and SVG. It contains no third-party graph library, CDN asset, hosted font, analytics SDK, or copied browser-side package.

This notice records direct project choices. Installed transitive packages remain governed by their own upstream license files and package metadata.

## C06 external evaluation data

| Dataset | C06 role | Pinned revision | Declared license | Official source |
|---|---|---|---|---|
| Belief-R (`CAiRE/belief_r`) | official test-only external evaluation | `3719f5804c63318037465fecf298a7fd78d99121` | CC BY-SA 4.0 on the Hugging Face dataset card | <https://huggingface.co/datasets/CAiRE/belief_r> |

Belief-R text is acquired into a gitignored local cache and is not redistributed in this
repository. The separate `HLTCHKUST/belief-revision` GitHub repository did not display a
repository license when checked on 2026-08-23. Its code is not cloned, imported, executed,
copied, or treated as covered by the dataset-card license.

## Optional C05 learned baseline tooling

| Package | C05 role | Tested version | Upstream license | Official source |
|---|---|---:|---|---|
| PyTorch | CPU GRU/LSTM/Transformer/modular/explicit-state models and profiler substrate | 2.13.0+cpu | BSD-style 3-clause plus bundled component notices | <https://github.com/pytorch/pytorch/blob/v2.13.0/LICENSE> |

PyTorch is not a core runtime dependency and is installed only through the `learned` or
existing optional `spiking` extra.
