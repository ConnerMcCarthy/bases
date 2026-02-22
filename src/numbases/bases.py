"""Utilities for representing numbers in different bases.

Start with integer bases; non-integer bases like phi are stubbed for now.
"""
from __future__ import annotations

import math
from functools import lru_cache

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
PHI = (1 + math.sqrt(5)) / 2


def to_base(n: int, base: int) -> str:
    """Convert an integer to a string in the given integer base (2..36)."""
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if not isinstance(base, int):
        raise TypeError("base must be an int")
    if base < 2 or base > len(DIGITS):
        raise ValueError(f"base must be between 2 and {len(DIGITS)}")

    if n == 0:
        return "0"

    negative = n < 0
    n = abs(n)
    digits = []
    while n > 0:
        n, rem = divmod(n, base)
        digits.append(DIGITS[rem])

    if negative:
        digits.append("-")
    return "".join(reversed(digits))


def to_base_parenthesized(n: int, base: int) -> str:
    """Convert an integer and render digits >= 10 as parenthesized numbers."""
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if not isinstance(base, int):
        raise TypeError("base must be an int")
    if base < 2 or base > len(DIGITS):
        raise ValueError(f"base must be between 2 and {len(DIGITS)}")

    if n == 0:
        return "0"

    negative = n < 0
    n = abs(n)
    tokens = []
    while n > 0:
        n, rem = divmod(n, base)
        if rem < 10:
            tokens.append(str(rem))
        else:
            tokens.append(f"({rem})")

    rendered = "".join(reversed(tokens))
    return f"-{rendered}" if negative else rendered


def from_base(s: str, base: int) -> int:
    """Parse a string in the given integer base (2..36) into an int."""
    if not isinstance(s, str) or not s:
        raise ValueError("s must be a non-empty string")
    if not isinstance(base, int):
        raise TypeError("base must be an int")
    if base < 2 or base > len(DIGITS):
        raise ValueError(f"base must be between 2 and {len(DIGITS)}")

    s = s.strip().upper()
    negative = s.startswith("-")
    if negative:
        s = s[1:]
    if not s:
        raise ValueError("invalid number string")

    value = 0
    for ch in s:
        idx = DIGITS.find(ch)
        if idx == -1 or idx >= base:
            raise ValueError(f"invalid digit '{ch}' for base {base}")
        value = value * base + idx

    return -value if negative else value


def factors(n: int) -> list[int]:
    """Return sorted positive factors of a non-zero integer."""
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n == 0:
        raise ValueError("factors for 0 are not finite")

    n_abs = abs(n)
    low: list[int] = []
    high: list[int] = []
    i = 1
    while i * i <= n_abs:
        if n_abs % i == 0:
            low.append(i)
            if i != n_abs // i:
                high.append(n_abs // i)
        i += 1
    return low + list(reversed(high))


def to_non_integer_base(value: float, base: float, precision: int = 16) -> str:
    """Convert a real number to a base representation for base > 1.

    This uses a greedy digit selection with digit set 0..floor(base).
    Output is approximate for irrational bases or finite precision.
    """
    if not isinstance(value, (int, float)):
        raise TypeError("value must be numeric")
    if not isinstance(base, (int, float)):
        raise TypeError("base must be numeric")
    if not isinstance(precision, int) or precision < 0:
        raise ValueError("precision must be an integer >= 0")

    value = float(value)
    base = float(base)
    if not math.isfinite(value):
        raise ValueError("value must be finite")
    if not math.isfinite(base) or base <= 1:
        raise ValueError("base must be finite and greater than 1")

    max_digit = int(math.floor(base))
    if max_digit < 1:
        raise ValueError("base must allow at least digits 0 and 1")
    if max_digit >= len(DIGITS):
        raise ValueError(f"base must be <= {len(DIGITS)}")

    if value == 0:
        return "0"

    negative = value < 0
    x = abs(value)
    eps = 1e-12

    if x >= 1:
        k = int(math.floor(math.log(x, base)))
        while base ** (k + 1) <= x + eps:
            k += 1
    else:
        k = -1

    digits: list[str] = []
    for exp in range(k, -precision - 1, -1):
        place = base**exp
        digit = int(math.floor((x + eps) / place))
        if digit > max_digit:
            digit = max_digit
        if digit < 0:
            digit = 0
        x -= digit * place
        if x < 0:
            x = 0.0
        digits.append(DIGITS[digit])
        if exp == 0 and precision > 0:
            digits.append(".")

    rendered = "".join(digits)
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    rendered = rendered.lstrip("0") if not rendered.startswith("0.") else rendered
    if not rendered:
        rendered = "0"

    return f"-{rendered}" if negative else rendered


def from_non_integer_base(s: str, base: float) -> float:
    """Parse a non-integer base string (0-9A-Z with optional '.') into float."""
    if not isinstance(s, str) or not s.strip():
        raise ValueError("s must be a non-empty string")
    if not isinstance(base, (int, float)):
        raise TypeError("base must be numeric")
    base = float(base)
    if not math.isfinite(base) or base <= 1:
        raise ValueError("base must be finite and greater than 1")

    s = s.strip().upper()
    negative = s.startswith("-")
    if negative:
        s = s[1:]
    if not s:
        raise ValueError("invalid number string")

    if s.count(".") > 1:
        raise ValueError("invalid number string")

    if "." in s:
        int_part, frac_part = s.split(".", 1)
    else:
        int_part, frac_part = s, ""
    if not int_part:
        int_part = "0"

    max_digit = int(math.floor(base))
    int_value = 0.0
    for ch in int_part:
        idx = DIGITS.find(ch)
        if idx == -1 or idx > max_digit:
            raise ValueError(f"invalid digit '{ch}' for base {base}")
        int_value = int_value * base + idx

    frac_value = 0.0
    place = base
    for ch in frac_part:
        idx = DIGITS.find(ch)
        if idx == -1 or idx > max_digit:
            raise ValueError(f"invalid digit '{ch}' for base {base}")
        frac_value += idx / place
        place *= base

    total = int_value + frac_value
    return -total if negative else total


def to_base_phi(n: int) -> str:
    """Convert an integer to an approximate base-phi representation.

    Uses greedy non-integer-base conversion with finite precision.
    """
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    return to_non_integer_base(float(n), PHI, precision=18)


@lru_cache(maxsize=None)
def _phi_power_pair(exp: int) -> tuple[int, int]:
    """Return integer pair (a, b) representing phi^exp = a + b*phi."""
    a, b = 1, 0  # phi^0
    if exp > 0:
        for _ in range(exp):
            a, b = b, a + b
    elif exp < 0:
        for _ in range(-exp):
            # Invert the forward recurrence: (a, b) -> (b, a + b).
            # Solve a_prev, b_prev from a = b_prev and b = a_prev + b_prev.
            a, b = b - a, a
    return a, b


def _parse_phi_digits(s: str) -> tuple[bool, str, str]:
    if not isinstance(s, str) or not s.strip():
        raise ValueError("s must be a non-empty string")
    s = s.strip()
    negative = s.startswith("-")
    if negative:
        s = s[1:]
    if not s:
        raise ValueError("invalid base-phi digit string")
    if s.count(".") > 1:
        raise ValueError("invalid base-phi digit string")

    allowed = {"0", "1", "."}
    if any(ch not in allowed for ch in s):
        raise ValueError("base-phi digits must use only 0/1 and optional '.'")

    if "." in s:
        int_part, frac_part = s.split(".", 1)
    else:
        int_part, frac_part = s, ""
    if not int_part:
        int_part = "0"
    return negative, int_part, frac_part


def _phi_digits_to_pair_unsigned(int_part: str, frac_part: str) -> tuple[int, int]:
    a_total, b_total = 0, 0
    for idx, ch in enumerate(int_part):
        if ch == "1":
            exp = len(int_part) - 1 - idx
            a, b = _phi_power_pair(exp)
            a_total += a
            b_total += b
    for idx, ch in enumerate(frac_part):
        if ch == "1":
            exp = -1 - idx
            a, b = _phi_power_pair(exp)
            a_total += a
            b_total += b
    return a_total, b_total


def _coeffs_from_parts(int_part: str, frac_part: str) -> dict[int, int]:
    coeffs: dict[int, int] = {}
    for idx, ch in enumerate(int_part):
        if ch == "1":
            exp = len(int_part) - 1 - idx
            coeffs[exp] = coeffs.get(exp, 0) + 1
    for idx, ch in enumerate(frac_part):
        if ch == "1":
            exp = -1 - idx
            coeffs[exp] = coeffs.get(exp, 0) + 1
    return coeffs


def _canonicalize_phi_coeffs(coeffs_in: dict[int, int]) -> dict[int, int]:
    """Normalize coefficients to canonical base-phi digits (0/1, no adjacent ones)."""
    coeffs = {k: v for k, v in coeffs_in.items() if v}

    changed = True
    while changed:
        changed = False
        keys = sorted(coeffs.keys())
        for e in keys:
            while coeffs.get(e, 0) >= 2:
                coeffs[e] -= 2
                coeffs[e + 1] = coeffs.get(e + 1, 0) + 1
                coeffs[e - 2] = coeffs.get(e - 2, 0) + 1
                changed = True
            if coeffs.get(e, 0) == 0:
                coeffs.pop(e, None)

        keys = sorted(coeffs.keys(), reverse=True)
        for e in keys:
            if coeffs.get(e, 0) and coeffs.get(e - 1, 0):
                coeffs[e] -= 1
                coeffs[e - 1] -= 1
                coeffs[e + 1] = coeffs.get(e + 1, 0) + 1
                if coeffs.get(e, 0) == 0:
                    coeffs.pop(e, None)
                if coeffs.get(e - 1, 0) == 0:
                    coeffs.pop(e - 1, None)
                changed = True

    for exp, v in list(coeffs.items()):
        if v <= 0:
            coeffs.pop(exp, None)
    return coeffs


def _render_phi_coeffs(coeffs: dict[int, int]) -> str:
    if not coeffs:
        return "0"
    highest = max(coeffs.keys())
    lowest = min(coeffs.keys())
    render_lowest = min(lowest, 0)

    digits: list[str] = []
    for exp in range(highest, render_lowest - 1, -1):
        digits.append("1" if coeffs.get(exp, 0) else "0")
        if exp == 0 and render_lowest < 0:
            digits.append(".")
    rendered = "".join(digits)
    if "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return rendered


def phi_digits_to_pair(s: str) -> tuple[int, int]:
    """Convert base-phi digits to exact pair (a, b) meaning a + b*phi."""
    negative, int_part, frac_part = _parse_phi_digits(s)
    a, b = _phi_digits_to_pair_unsigned(int_part, frac_part)
    return (-a, -b) if negative else (a, b)


def _pair_to_float(a: int, b: int) -> float:
    return a + b * PHI


def _phi_pair_to_digits_unsigned(
    a_target: int,
    b_target: int,
    min_exp: int = -24,
    max_exp: int = 24,
    no_adjacent: bool = True,
    max_nodes: int | None = None,
) -> str:
    if a_target == 0 and b_target == 0:
        return "0"

    exps = list(range(max_exp, min_exp - 1, -1))
    pairs = [_phi_power_pair(e) for e in exps]
    n = len(exps)

    # Pruning bounds on remaining reachable ranges with digits 0/1.
    suffix_min_a = [0] * (n + 1)
    suffix_max_a = [0] * (n + 1)
    suffix_min_b = [0] * (n + 1)
    suffix_max_b = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        pa, pb = pairs[i]
        suffix_min_a[i] = suffix_min_a[i + 1] + (pa if pa < 0 else 0)
        suffix_max_a[i] = suffix_max_a[i + 1] + (pa if pa > 0 else 0)
        suffix_min_b[i] = suffix_min_b[i + 1] + (pb if pb < 0 else 0)
        suffix_max_b[i] = suffix_max_b[i + 1] + (pb if pb > 0 else 0)

    nodes = 0

    @lru_cache(maxsize=None)
    def dfs(i: int, prev_one: int, a_rem: int, b_rem: int) -> tuple[int, ...] | None:
        nonlocal nodes
        nodes += 1
        if max_nodes is not None and nodes > max_nodes:
            raise ValueError("search limit exceeded")
        if i == n:
            return () if a_rem == 0 and b_rem == 0 else None
        if (
            a_rem < suffix_min_a[i]
            or a_rem > suffix_max_a[i]
            or b_rem < suffix_min_b[i]
            or b_rem > suffix_max_b[i]
        ):
            return None

        pa, pb = pairs[i]
        # Prefer placing a 1 earlier for a canonical "left-greedy" form.
        if (no_adjacent and prev_one == 0) or (not no_adjacent):
            with_one = dfs(i + 1, 1, a_rem - pa, b_rem - pb)
            if with_one is not None:
                return (1,) + with_one

        with_zero = dfs(i + 1, 0, a_rem, b_rem)
        if with_zero is not None:
            return (0,) + with_zero
        return None

    bits = dfs(0, 0, a_target, b_target)
    if bits is None:
        raise ValueError("could not find finite canonical base-phi representation")

    exp_to_bit = {e: bit for e, bit in zip(exps, bits) if bit}
    if not no_adjacent:
        exp_to_bit = _canonicalize_phi_coeffs(exp_to_bit)
    return _render_phi_coeffs(exp_to_bit)


def is_canonical_phi_digits(s: str) -> bool:
    """Canonical rule: digits in {0,1}, no adjacent ones across the radix point."""
    _, int_part, frac_part = _parse_phi_digits(s)
    compact = int_part + frac_part
    return "11" not in compact


def canonicalize_phi_digits(s: str) -> str:
    """Canonicalize finite base-phi digits to no-adjacent-ones form."""
    negative, int_part, frac_part = _parse_phi_digits(s)
    coeffs = _coeffs_from_parts(int_part, frac_part)
    rendered = _render_phi_coeffs(_canonicalize_phi_coeffs(coeffs))
    return f"-{rendered}" if negative and rendered != "0" else rendered


def to_base_phi_exact(n: int) -> str:
    """Convert an integer to exact canonical base-phi digits."""
    if not isinstance(n, int):
        raise TypeError("n must be an int")
    if n == 0:
        return "0"
    negative = n < 0
    target = abs(n)

    # Bounded search with pruning. Grow fractional depth gradually to avoid hangs.
    max_exp = max(2, int(math.ceil(math.log(target + 1, PHI))) + 2)
    rendered: str | None = None
    for extra_neg in (2, 4, 6, 8, 10, 12, 14, 16):
        try:
            rendered = _phi_pair_to_digits_unsigned(
                target,
                0,
                min_exp=-extra_neg,
                max_exp=max_exp,
                no_adjacent=True,
                max_nodes=200_000,
            )
            break
        except ValueError:
            continue
    if rendered is None:
        raise ValueError("could not find exact canonical base-phi representation")
    return f"-{rendered}" if negative else rendered


def from_base_phi_exact(s: str) -> int:
    """Parse base-phi digits exactly and return integer if representable."""
    a, b = phi_digits_to_pair(s)
    if b != 0:
        raise ValueError("base-phi value is not an integer exactly")
    return a


def phi_digits_to_expression(s: str) -> str:
    """Convert a base-phi digit string (0/1 with optional '.') to symbolic form."""
    if not isinstance(s, str) or not s.strip():
        raise ValueError("s must be a non-empty string")

    negative, int_part, frac_part = _parse_phi_digits(s)

    terms: list[str] = []

    def term_for_exp(exp: int) -> str:
        if exp == 0:
            return "1"
        if exp == 1:
            return "phi"
        return f"phi^{exp}"

    for idx, ch in enumerate(int_part):
        if ch == "1":
            exp = len(int_part) - 1 - idx
            terms.append(term_for_exp(exp))
    for idx, ch in enumerate(frac_part):
        if ch == "1":
            exp = -1 - idx
            terms.append(term_for_exp(exp))

    if not terms:
        return "0"

    expr = "+".join(terms)
    return f"-({expr})" if negative else expr
