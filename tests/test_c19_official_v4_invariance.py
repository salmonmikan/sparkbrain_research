from __future__ import annotations

from sparkbrain.v03_external_validation import official_protocol_v3 as v3
from sparkbrain.v03_external_validation import official_protocol_v4 as v4


def test_v4_scientific_contract_is_exact_v3_inheritance() -> None:
    identity_only = {"PROTOCOL_ID", "PLANNED_IDENTITY", "PACKAGE_ID"}
    for name in v3.__all__:
        if name in identity_only:
            continue
        assert getattr(v4, name) == getattr(v3, name), name

    assert v4.PROTOCOL_ID == "c19-external-v2-official-protocol-v4"
    assert v4.PLANNED_IDENTITY == "c19-external-v2-official-v4"
    assert v4.PACKAGE_ID == "c19-external-v2-official-package-v4"
    assert v4.expected_row_inventory() == v3.expected_row_inventory()
