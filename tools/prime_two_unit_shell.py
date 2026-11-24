"""Check the unit part of the Weil principal value at 2 using exact sums."""

from fractions import Fraction


def truncated_unit_integral(values: tuple[int, ...], depth: int, *, subtract_at_one: bool) -> Fraction:
    """Normalize unit Haar mass to one and omit the class of 1 modulo 2^depth."""
    modulus = 2**depth
    value_at_one = values[1 % len(values)] if subtract_at_one else 0
    weighted_sum = 0
    for unit in range(3, modulus, 2):
        difference = unit - 1
        # The lowest set bit of unit - 1 is 2^v₂(1 - unit).
        inverse_norm = difference & -difference
        weighted_sum += (values[unit % len(values)] - value_at_one) * inverse_norm
    return Fraction(weighted_sum, modulus // 2)


def main() -> None:
    # Tables are indexed by the residue of u. Only odd residues are used.
    cases = (
        ("trivial on units", (1,), 0, -1),
        ("primitive mod 4", (0, 1, 0, -1), -2, -3),
        ("primitive mod 8", (0, 1, 0, -1, 0, -1, 0, 1), -3, -4),
        ("indicator of 3 mod 4", (0, 0, 0, 1), 1, None),
        ("zero on units", (0,), 0, None),
    )
    for name, values, principal, raw_offset in cases:
        for depth in range(3, 11):
            raw = truncated_unit_integral(values, depth, subtract_at_one=False)
            regularized = truncated_unit_integral(values, depth, subtract_at_one=True)
            expected_raw = principal if raw_offset is None else depth + raw_offset
            if (raw, regularized) != (expected_raw, principal):
                raise ArithmeticError(f"{name}, depth {depth}: got {(raw, regularized)}")
        print(f"{name}: principal value / log(2) = {principal}, depths 3..10 agree")


if __name__ == "__main__":
    main()
