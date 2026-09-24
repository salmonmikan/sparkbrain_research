"""TH002-FORGE-001-STATIC-ADDRESSABILITY-KILL.

NON_EVIDENTIARY / NONCANONICAL Fast Forge probe.
Fresh synthetic construction only; no terminal fixture or held-out evaluator input.

The construction uses three anonymous content-derived physical signatures. Their
order is irrelevant at merge. A delayed cue supplies one of the same physical
signatures and requests a scalar revision of the corresponding history.

The point of the probe is adversarial: determine whether the carrier is anything
more than an ordinary associative / separable address-plus-state memory.
"""

from itertools import permutations

KEYS = (
    (1.0, 1.0, 1.0, -1.0),
    (1.0, 1.0, -1.0, 1.0),
    (1.0, -1.0, 1.0, 1.0),
)
VALUES = (0.25, -0.50, 0.75)
DIM = 4
DELTA = 0.20


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def merge(order, values=VALUES):
    """Permutation-symmetric superposition carrier M = sum(v_i k_i / DIM)."""
    m = [0.0] * DIM
    for idx in order:
        for j, x in enumerate(KEYS[idx]):
            m[j] += values[idx] * x / DIM
    return tuple(m)


def read(carrier, key):
    """Delayed content cue retrieves the scalar bound to that signature."""
    return dot(carrier, key)


def revise(carrier, key, delta):
    """Revision via the same content signature."""
    return tuple(x + delta * k / DIM for x, k in zip(carrier, key))


def kv_table(order, values=VALUES):
    """Ordinary comparator with exactly the same content keys available."""
    return tuple((KEYS[idx], values[idx]) for idx in order)


def kv_read(table, query):
    matches = [value for key, value in table if key == query]
    assert len(matches) == 1
    return matches[0]


def kv_revise(table, query, delta):
    out = []
    matched = 0
    for key, value in table:
        if key == query:
            out.append((key, value + delta))
            matched += 1
        else:
            out.append((key, value))
    assert matched == 1
    return tuple(out)


def main():
    gram = tuple(tuple(dot(a, b) for b in KEYS) for a in KEYS)
    assert gram == (
        (4.0, 0.0, 0.0),
        (0.0, 4.0, 0.0),
        (0.0, 0.0, 4.0),
    )

    canonical = merge((0, 1, 2))
    assert all(merge(p) == canonical for p in permutations(range(3)))

    decoded = tuple(read(canonical, k) for k in KEYS)
    assert decoded == VALUES

    for order in permutations(range(3)):
        table = kv_table(order)
        for query in KEYS:
            assert read(canonical, query) == kv_read(table, query)
            revised_carrier = revise(canonical, query, DELTA)
            revised_table = kv_revise(table, query, DELTA)
            for probe_key in KEYS:
                assert round(read(revised_carrier, probe_key), 12) == round(
                    kv_read(revised_table, probe_key), 12
                )

    print("permutation_equivariance=PASS")
    print("target_selective_revision=PASS")
    print("matched_access_kv_equivalence=PASS")
    print("disposition=FORGE_DEAD_END")
    print("reduction=ASSOCIATIVE_KEY_VALUE_OR_SEPARABLE_ADDRESS_PLUS_STATE")


if __name__ == "__main__":
    main()
