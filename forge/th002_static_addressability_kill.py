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


def explicit_register_read(registers, target_index):
    return registers[target_index]


def explicit_register_revise(registers, target_index, delta):
    out = list(registers)
    out[target_index] += delta
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

    for target in range(3):
        revised_carrier = revise(canonical, KEYS[target], DELTA)
        decoded_after = tuple(round(read(revised_carrier, k), 12) for k in KEYS)
        register_after = tuple(
            round(x, 12)
            for x in explicit_register_revise(VALUES, target, DELTA)
        )
        assert decoded_after == register_after
        assert round(read(canonical, KEYS[target]), 12) == round(
            explicit_register_read(VALUES, target), 12
        )

    print("permutation_equivariance=PASS")
    print("target_selective_revision=PASS")
    print("register_equivalence=PASS")
    print("disposition=FORGE_DEAD_END")
    print("reduction=ASSOCIATIVE_KEY_VALUE_OR_SEPARABLE_ADDRESS_PLUS_STATE")


if __name__ == "__main__":
    main()
