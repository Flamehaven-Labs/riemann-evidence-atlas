"""Check the dyadic Fourier shell masses in the unfolded trace calculation."""

from fractions import Fraction
import json


def ball_character_integral(a: Fraction, exponent: int) -> Fraction:
    """Integrate by summing an exact character on a finite quotient of the ball."""
    radius = Fraction(2) ** exponent
    phase = a / radius
    order = phase.denominator
    if order == 1:
        return radius

    # The phases are powers of a primitive root of order 2^r. Opposite
    # powers cancel, so keep their integer coefficients in paired bins.
    if order & (order - 1):
        raise ValueError("the character on the ball must have dyadic order")
    half = order // 2
    coefficients = [0] * half
    for point in range(order):
        power = (phase.numerator * point) % order
        coefficients[power % half] += 1 if power < half else -1
    if any(coefficients):
        raise ArithmeticError("the finite character sum did not cancel")
    return Fraction(0)


def weighted_shell_sum(a: Fraction, depth: int) -> Fraction:
    """Return the log-2 coefficient, including the exact low-radius tail."""
    if depth < 1:
        raise ValueError("depth must be positive")
    previous = ball_character_integral(a, -depth - 1)
    if previous != Fraction(2) ** (-depth - 1):
        raise ValueError("the character must be trivial below the truncation")
    # Here the shell masses are 2^(j-1) for j < -depth.
    total = -(depth + 2) * previous
    for j in range(-depth, 2):
        current = ball_character_integral(a, j)
        total += j * (current - previous)
        previous = current
    return total


if __name__ == "__main__":
    depths = (8, 16, 24)
    norm_two = [weighted_shell_sum(Fraction(1, 2), depth) for depth in depths]
    unit_control = [weighted_shell_sum(Fraction(1), depth) for depth in depths]
    assert norm_two == [-1] * len(depths)
    assert unit_control == [-2] * len(depths)
    print(json.dumps({
        "depths": depths,
        "norm_two_log_weights": list(map(str, norm_two)),
        "unit_control_log_weights": list(map(str, unit_control)),
        "norm_two_coefficient_before_f_and_log_two": str(-norm_two[0] / 2),
    }, indent=2, sort_keys=True))
