from pathlib import Path

path = Path("tests/test_rv01_r01_17_real_delay.py")
text = path.read_text(encoding="utf-8")
old = '''        def arm(
            *, delays_from_pre: bool, times: list[float], state_hash: str
        ) -> dict[str, object]:
            source_rows = pre_rows if delays_from_pre else post_rows
'''
new = '''        def arm(
            *,
            source_rows: list[dict[str, object]],
            times: list[float],
            state_hash: str,
        ) -> dict[str, object]:
'''
if old not in text:
    raise SystemExit("expected synthetic arm helper not found")
text = text.replace(old, new, 1)
text = text.replace(
    '''                    "F0": arm(
                        delays_from_pre=False, times=f0_times, state_hash="post"
                    ),
                    "FD": arm(
                        delays_from_pre=True, times=fd_times, state_hash="pre"
                    ),
                    "SHAM": arm(
                        delays_from_pre=False, times=f0_times, state_hash="post"
                    ),
''',
    '''                    "F0": arm(
                        source_rows=post_rows, times=f0_times, state_hash="post"
                    ),
                    "FD": arm(
                        source_rows=pre_rows, times=fd_times, state_hash="pre"
                    ),
                    "SHAM": arm(
                        source_rows=post_rows, times=f0_times, state_hash="post"
                    ),
''',
    1,
)
path.write_text(text, encoding="utf-8")
