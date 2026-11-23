"""Outward exponential enclosures using exact rational arithmetic.

The series remainder after term N is bounded by a_(N+1)/(1-y/(N+2))
for 0 <= y <= 1/2. Negative arguments use reciprocal bounds.
"""

from fractions import Fraction

PRECISIONS = (128, 256, 512)


def _precision(bits: int) -> None:
    if type(bits) is not int or bits not in PRECISIONS:
        raise ValueError("precision must be 128, 256 or 512 fractional bits")


def _round(bounds: tuple[Fraction, Fraction], bits: int) -> tuple[Fraction, Fraction]:
    lo, hi = bounds
    if lo > hi:
        raise ValueError("inverted interval")
    scale = 1 << bits
    a, b = lo * scale, hi * scale
    return Fraction(a.numerator // a.denominator, scale), Fraction(
        -((-b.numerator) // b.denominator), scale
    )


def _positive_product(
    a: tuple[Fraction, Fraction], b: tuple[Fraction, Fraction], bits: int
) -> tuple[Fraction, Fraction]:
    if not (0 <= a[0] <= a[1] and 0 <= b[0] <= b[1]):
        raise ValueError("ordered nonnegative intervals required")
    return _round((a[0] * b[0], a[1] * b[1]), bits)


def _small_exp(y: Fraction, bits: int, *, minus_one: bool = False) -> tuple[Fraction, Fraction]:
    if not isinstance(y, Fraction) or not 0 <= y <= Fraction(1, 2):
        raise ValueError("small exponential argument outside [0, 1/2]")
    term = Fraction(1)
    total = Fraction(0 if minus_one else 1)
    tolerance = Fraction(1, 1 << (bits + 4))
    for n in range(1, 1025):
        term *= y / n
        total += term
        next_term = term * y / (n + 1)
        remainder = next_term / (1 - y / (n + 2))
        if remainder <= tolerance:
            return _round((total, total + remainder), bits)
    raise ValueError("UNRESOLVED[BACKEND_ENCLOSURE_BUDGET_EXCEEDED]")


def exp_bounds(x: Fraction, bits: int = 128) -> tuple[Fraction, Fraction]:
    """Enclose exp(x), |x|<=16. Precision is fractional bits, not integer size."""
    _precision(bits)
    if not isinstance(x, Fraction) or abs(x) > 16:
        raise ValueError("exact rational argument within [-16, 16] required")
    work_bits = bits + 64
    y, squarings = abs(x), 0
    while y > Fraction(1, 2):
        y /= 2
        squarings += 1
    bounds = _small_exp(y, work_bits)
    for _ in range(squarings):
        bounds = _positive_product(bounds, bounds, work_bits)
    if x < 0:
        if bounds[0] <= 0:
            raise ValueError("nonpositive reciprocal denominator")
        bounds = 1 / bounds[1], 1 / bounds[0]
    return _round(bounds, bits)


def expm1_bounds(t: Fraction, bits: int = 128) -> tuple[Fraction, Fraction]:
    """Positive small expm1 via its own series, without subtracting near ones."""
    _precision(bits)
    if not isinstance(t, Fraction) or not 0 <= t <= Fraction(1, 2):
        raise ValueError("exact rational t in [0, 1/2] required")
    return _small_exp(t, bits, minus_one=True)
