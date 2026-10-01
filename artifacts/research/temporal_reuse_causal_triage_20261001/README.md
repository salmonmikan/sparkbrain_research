# Retrospective PR169 trace arithmetic

This package explains the already-recorded negative result. It does not run a model, alter the old scoring gate, or execute the [proposed successor protocol](../../../docs/research/shared_prefix_plasticity_protocol_20261001.md).

- [Report](../../../docs/research/temporal_reuse_causal_triage_20261001.md)
- [Readable summary](SUMMARY.json)
- [Complete row arithmetic, compressed JSON](TRACE_AUDIT.json.gz)
- [Source hashes](SOURCE_PROVENANCE.json)
- [Artifact manifest](MANIFEST.json)
- [Data-only auditor](../../../scripts/audit_temporal_reuse_saved_traces.py)
- [Synthetic and publication tests](../../../tests/test_temporal_reuse_saved_trace_audit.py)

Source pin: `0bcb2c1b23c29e5107111343a757c57c1f7bbb41`.
Upstream evidence pin: `b6a872642df6889e9c6ce82148a5a2430db2c114` ([PR169 report](https://github.com/salmonmikan/sparkbrain_research/blob/b6a872642df6889e9c6ce82148a5a2430db2c114/docs/research/temporal_reuse_loop_results_20261001.md)).
Raw manifest SHA-256: `f224981074dde62b0f3c9a4d9b075714140c83ac1476533d70580e281c6b2b05`.

## Recompute from immutable upstream bytes

From the repository root with Python3.11+ and Git, fetch the upstream branch if the pinned objects are not already present. This fetch/extraction does not run the model. Use a fresh temporary directory; keep it to inspect the output.

```sh
git fetch origin research/temporal-loop-contract-20261001
work=$(mktemp -d)
git archive b6a872642df6889e9c6ce82148a5a2430db2c114 \
  artifacts/research/temporal_reuse_loop_20261001 \
  scripts/verify_temporal_reuse_evidence.py | tar -x -C "$work"
python "$work/scripts/verify_temporal_reuse_evidence.py" \
  --directory "$work/artifacts/research/temporal_reuse_loop_20261001" \
  --extract "$work/unpacked"
python scripts/audit_temporal_reuse_saved_traces.py \
  "$work/unpacked/run" "$work/recomputed.json"
python - "$work/recomputed.json" <<'PY'
import gzip, hashlib, json, pathlib, sys
p = pathlib.Path('artifacts/research/temporal_reuse_causal_triage_20261001')
m = json.loads((p / 'MANIFEST.json').read_text())
a = pathlib.Path(sys.argv[1]).read_bytes()
b = gzip.decompress((p / 'TRACE_AUDIT.json.gz').read_bytes())
assert a == b
assert hashlib.sha256(a).hexdigest() == m['output_json_sha256']
print('All retrospective arithmetic reproduced; model calls: 0')
PY
python -m pytest -q tests/test_temporal_reuse_saved_trace_audit.py
```

The audit opens its output exclusively and does not modify any existing input file. Place its output outside the upstream input tree, as shown above; the CLI does not impose a directory-containment restriction. It reconstructs 256 S/F routing/readout rows and 384 Q/H/R metric rows after checking all 232 files listed by the upstream run manifest. It does not claim new runtime replication, prospective evidence, comprehensive matcher correctness, or independent confirmation of every original guard. The exact spike-order sensitivity and prototype/readout behavior follow the pinned source contract.

`TRACE_AUDIT_RUN.log` is historical stdout from the same local arithmetic. The authoritative full output is the decompressed JSON bound by MANIFEST.json; gzip implementation details are not a model invariant. All original PR169 raw files and the original negative result stay at their upstream pin.
