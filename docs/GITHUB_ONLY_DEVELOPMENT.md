# GitHub-only authoring and CI verification

## Scope and current implementation status

A small engineering change can be authored through GitHub's file/Git-object APIs,
reviewed in a pull request, and checked by the existing GitHub Actions workflow
without preparing an editor-side Python environment. Actions still prepares its
own Python/dependency environment.

This is a code-authoring and engineering-verification route. It does not establish
local reproducibility, reproduce scientific results, authorize an experiment,
change a scientific claim, or replace the local command sequence required by
`AGENTS.md` and [LOCAL_EXECUTION_POLICY.md](LOCAL_EXECUTION_POLICY.md).

The CI evidence collector introduced here uses only the Python standard library.
Its tests construct synthetic metadata and temporary files; they do not import
the SparkBrain engine, a model, a scientific controller, or an external dataset.
GitHub-only implementation leaves the equivalent local validation pending until
it is actually run and recorded in an authorized local environment.

## Small-change loop

1. Read current `AGENTS.md`, the task's relevant policy, the exact base commit,
   and every file to be changed. Treat operational/scientific branches and frozen
   evidence according to their own contracts.
2. Use a dedicated task branch. Build a tree on the existing base tree and publish
   one commit for a coherent multi-file change; do not reconstruct the whole tree
   or force-update a branch. Re-fetch a moved branch before rebuilding a change.
3. Read back the remote head, changed contents, and PR diff. Open a draft PR.
4. Observe the existing `ci` runs and both `test (3.11)` and `test (3.13)` jobs.
   A listed or pending run is not a pass. Check the exact PR head and its run
   metadata again after every source update.
5. Obtain the required latest-change review and resolve substantive findings.
   An empty reviews array alone does not prove review completion: review bots may
   report through comments and reactions. A resolved thread is not proof that a
   newly updated head was reviewed.
6. Only an authorized merge owner can decide readiness. Any merge must preserve
   the required local-validation boundary and use the expected head SHA to reject
   a moved PR. The current main ruleset requires a PR and squash history; that
   does not independently enforce every project review/validation requirement.

Code publication, scientific execution, result publication, and local execution
remain separate actions. A generic development PR must not dispatch, rerun,
repurpose, or cancel a scientific one-way workflow. This guide does not change
any scheduler, persistence bridge, experiment authorization, or frozen source.

## What the existing CI checks

`.github/workflows/ci.yml` retains its existing commands:

```bash
python -m pip install -e ".[dev,learned,spiking]"
python -m ruff check .
python scripts/local_readiness_check.py
python -m pytest -q
python scripts/validate_bundle.py
```

The workflow runs on `ubuntu-latest` with Python 3.11 and 3.13 and pip caching.
It installs learned/spiking dependencies, so it is not a model-free or minimal
dependency check. The default pytest selection in `pyproject.toml` excludes the
scientific, reproduction, and external tiers; a green result is not a full
scientific/reproduction run. Bundle validation inspects retained files and emits
a validation manifest; it does not regenerate their historical science.

The dependency ranges, runner image, and cache can change. Hashing
`pyproject.toml` does not turn those inputs into a pinned, cold, offline restore.
For recovery work, record the separate recovery commands, lock identity, and
actual cold/offline outcomes rather than relabeling this CI as that proof.

## Downloadable verification record

After the existing checks, each test matrix job emits one bounded JSON job output
under its unique `py311` or `py313` name. It never uploads a producer-runner file.
Two lightweight `evidence` matrix jobs start on fresh standard hosted runners,
check out the exact event commit, and reconstruct one JSON file per version with:

- the run ID and attempt, event type, repository, and run URL;
- the actual checkout commit/tree from Git and the event commit;
- the PR head separately, because a pull-request job normally tests a generated
  merge checkout rather than the head commit alone;
- the test runner's reported Python implementation/version, OS name, and machine
  architecture (not the later evidence runner's interpreter);
- each original step's outcome, retaining failure, cancellation, and skip states;
- hashes of exactly `pyproject.toml`, `.github/workflows/ci.yml`, and, only when
  bundle validation succeeded, `artifacts/validation_manifest.json`;
- an explicit engineering-only scope with local reproduction, scientific
  establishment, dependency-environment reproduction, independent attestation,
  and successful artifact upload all marked unverified.

`configured_checks_passed` requires every configured step to succeed, Python to
match its matrix minor, checkout to match the event SHA, and tracked files to
remain unchanged except for the generated validation manifest. It is not the
final job conclusion, a full test inventory, a security attestation, or scientific
evidence. The upload happens afterward and must be verified separately.

The collector accepts only the declared context/outcome/runtime fields. The fresh
consumer treats job outputs as untrusted data: it caps each JSON input at 8 KiB,
rejects duplicate and extra keys, enforces exact field types and outcome/runtime
enums, and rebuilds the record against its own workflow/run context and clean
event checkout. Commit/tree identities and source-input hashes must match the
fresh checkout. The generated validation-manifest hash is only a well-formed
producer assertion; the consumer does not receive that manifest or revalidate
its contents.

The fresh job runs no package install, test hook, experiment, or model. It uses
isolated Python (`-I -B`) and does not carry files or background processes from
the test runner. This removes the concrete producer-file replacement window
between collection and upload. It does not defend against a maliciously changed
workflow or collector, prove that repository-controlled tests are truthful, or
provide an independent attestation. Those remain review/trust boundaries.

No process environment, credentials, package-index URLs, arbitrary stdout, local
paths, test fixtures, or raw research files are copied. GitHub context values and
job-output JSON are passed through environment variables, never interpolated into
shell source or executed as code.

Failure or skipped original checks can produce a valid negative record with a
false configured-check result. Consumer creation success is separate from that
result: upload requires the fresh collector step itself to have succeeded, and a
separate final step fails the evidence job when the recorded checks did not all
pass. An existing consumer output makes its exclusive write fail and upload skip.
Producer-side files are never read by the upload action.

A pre-existing validation manifest is not mistaken for new evidence when bundle
validation was skipped. Source/context/hash mismatches, malformed or missing job
outputs, unavailable checkout/interpreter, hard termination, or an unavailable
Actions service may prevent an artifact; absence is never a pass. A producer
record from an earlier run attempt cannot be relabeled as a new attempt. If
GitHub suppresses an output as potentially secret, the consumer also fails
closed instead of falling back to a producer file.

The pinned official `actions/upload-artifact` v4.6.2 commit is
`ea165f8d65b6e75b540449e92b4886f43607fa02`. The workflow has explicit
`contents: read` permission, no new secret, and uploads only the one JSON file.

## Retrieval and retention

Artifact names are
`ci-verification-<run_id>-<attempt>-py<major.minor>`. A completed two-version
matrix should have one for 3.11 and one for 3.13. Use the actual run's artifact
listing, inspect expiry, and download both; do not infer availability from the
recording step or an earlier attempt. The GitHub connector can list and download
workflow artifacts, while the run's Actions page provides the normal UI route.

Retention is requested as 30 days, subject to GitHub's repository/policy limits.
Artifacts and CI logs are temporary delivery, not permanent research storage.
An artifact download link alone is not a durable record. If long-term retention
is needed, explicitly preserve the downloaded bytes/checksum, run/attempt,
checkout/head identities, and validation limitations at an approved destination.
Do not silently commit generated files, publish a release, or change retention,
storage, or permissions to achieve that.

For public-repository standard GitHub-hosted runners, execution is in GitHub's
free tier. This is not approval to use larger paid runners or increase storage.
Keep records small and avoid adding scientific data or dependency archives.

## Corresponding local checks

With the already-authorized local environment available, the new collector's
synthetic tests can run independently of pytest or model dependencies:

```bash
python -m unittest discover -s tests -p test_ci_evidence.py
python -m ruff check scripts/write_ci_evidence.py tests/test_ci_evidence.py
```

The standard pytest suite also discovers these tests. Follow the full applicable
local validation sequence from `AGENTS.md` before claiming local completion.
These commands are provided, not asserted to have run locally by a GitHub-only
author. The producer mode is `--github-output`; only the fresh consumer uses `--output`.
Both modes expect genuine Actions run metadata; do not invent run IDs or local
values to manufacture a CI record.

## References

- [Git database API workflow](https://docs.github.com/en/rest/guides/using-the-rest-api-to-interact-with-your-git-database)
- [Official pinned upload-artifact source](https://github.com/actions/upload-artifact/tree/ea165f8d65b6e75b540449e92b4886f43607fa02)
- [Artifact and log retention](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/enabling-features-for-your-repository/managing-github-actions-settings-for-a-repository)
- [Actions billing](https://docs.github.com/en/billing/concepts/product-billing/github-actions)
