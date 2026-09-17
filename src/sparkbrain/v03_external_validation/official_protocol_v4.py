"""Preservation-qualified C19 official-v4 protocol identity.

Scientific semantics are inherited unchanged from official-v3.  The only changes are
fresh v4 authority identifiers and use of the separately qualified generic raw
preservation boundary.
"""

from __future__ import annotations

from sparkbrain.v03_external_validation import official_protocol_v3 as v3

for _name in v3.__all__:
    if _name not in {"PROTOCOL_ID", "PLANNED_IDENTITY", "PACKAGE_ID"}:
        globals()[_name] = getattr(v3, _name)

PROTOCOL_ID = "c19-external-v2-official-protocol-v4"
PLANNED_IDENTITY = "c19-external-v2-official-v4"
PACKAGE_ID = "c19-external-v2-official-package-v4"

__all__ = list(v3.__all__)
