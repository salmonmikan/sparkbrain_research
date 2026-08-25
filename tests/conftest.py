from __future__ import annotations

import sys

# The packaged plain pytest command must not mutate a pristine release tree.
sys.dont_write_bytecode = True
