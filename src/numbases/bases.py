"""Utilities for representing numbers in different bases.

Start with integer bases; non-integer bases like phi are stubbed for now.
"""
from __future__ import annotations

import math

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
