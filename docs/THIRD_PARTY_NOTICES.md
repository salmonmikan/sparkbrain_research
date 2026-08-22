# Third-party notices for optional Brain Lab tooling

C03 does not add a mandatory runtime dependency to the SparkBrain reference engine. The following direct dependencies are confined to optional `lab` or `dev` extras. Tested versions are recorded in `requirements-lab.lock`.

| Package | C03 role | Tested version | Upstream license | Official source |
|---|---|---:|---|---|
| FastAPI | localhost REST/SSE application | 0.141.1 | MIT | <https://github.com/fastapi/fastapi/blob/master/LICENSE> |
| Uvicorn | loopback ASGI server | 0.52.4 | BSD 3-Clause | <https://github.com/Kludex/uvicorn/blob/main/LICENSE.md> |
| HTTPX | API tests only | 0.28.1 | BSD 3-Clause | <https://github.com/encode/httpx/blob/master/LICENSE.md> |

The bundled Brain Lab frontend uses native HTML, CSS, JavaScript, and SVG. It contains no third-party graph library, CDN asset, hosted font, analytics SDK, or copied browser-side package.

This notice records direct project choices. Installed transitive packages remain governed by their own upstream license files and package metadata.
