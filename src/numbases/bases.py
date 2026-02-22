"""Utilities for representing numbers in different bases.

Start with integer bases; non-integer bases like phi are stubbed for now.
"""
from __future__ import annotations

DIGITS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


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


def to_base_phi(_: int) -> str:
    """Stub for base-phi (golden ratio) representation.

    Implementation pending; requires non-integer base algorithms.
    """
    raise NotImplementedError("base-phi conversion not implemented yet")
