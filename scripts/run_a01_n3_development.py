import argparse
from pathlib import Path

from sparkbrain.v061_a01.recurrent_development import execute

parser = argparse.ArgumentParser(description="Source-pinned N3-DEV-001 only")
parser.add_argument("--output", type=Path, required=True)
parser.add_argument("--authorization", type=Path, required=True)
args = parser.parse_args()
execute(Path(__file__).resolve().parents[1], args.output, args.authorization)
