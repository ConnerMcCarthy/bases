import pytest

from numbases.bases import (
    PHI,
    factors,
    from_base,
    from_non_integer_base,
    to_base,
    to_base_parenthesized,
    to_base_phi,
    to_non_integer_base,
)


def test_to_base_basic():
    assert to_base(0, 2) == "0"
    assert to_base(5, 2) == "101"
    assert to_base(31, 16) == "1F"
    assert to_base(-10, 10) == "-10"


def test_from_base_basic():
    assert from_base("0", 2) == 0
    assert from_base("101", 2) == 5
    assert from_base("1f", 16) == 31
    assert from_base("-10", 10) == -10


def test_invalid_digit():
    with pytest.raises(ValueError):
        from_base("2", 2)


def test_base_boundaries():
    assert to_base(5, 2) == "101"
    assert to_base(35, 36) == "Z"
    assert from_base("101", 2) == 5
    assert from_base("Z", 36) == 35


@pytest.mark.parametrize("base", [1, 37])
def test_invalid_base_range(base):
    with pytest.raises(ValueError):
        to_base(10, base)
    with pytest.raises(ValueError):
        from_base("10", base)


def test_invalid_base_type_string():
    with pytest.raises(TypeError):
        to_base(10, "10")  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        from_base("10", "10")  # type: ignore[arg-type]


def test_factors_positive_and_negative():
    assert factors(12) == [1, 2, 3, 4, 6, 12]
    assert factors(-12) == [1, 2, 3, 4, 6, 12]
    assert factors(13) == [1, 13]


def test_factors_zero_not_finite():
    with pytest.raises(ValueError):
        factors(0)


def test_factors_requires_int():
    with pytest.raises(TypeError):
        factors("12")  # type: ignore[arg-type]


def test_to_base_parenthesized():
    assert to_base_parenthesized(31, 16) == "1(15)"
    assert to_base_parenthesized(1256, 36) == "(34)(32)"
    assert to_base_parenthesized(-31, 16) == "-1(15)"
    assert to_base_parenthesized(9, 10) == "9"


def test_to_base_parenthesized_validation():
    with pytest.raises(ValueError):
        to_base_parenthesized(10, 1)
    with pytest.raises(TypeError):
        to_base_parenthesized(10, "16")  # type: ignore[arg-type]


def test_non_integer_base_round_trip():
    encoded = to_non_integer_base(10.5, PHI, precision=22)
    decoded = from_non_integer_base(encoded, PHI)
    assert abs(decoded - 10.5) < 1e-4


def test_non_integer_base_validation():
    with pytest.raises(ValueError):
        to_non_integer_base(10, 1.0)
    with pytest.raises(ValueError):
        from_non_integer_base("", PHI)


def test_to_base_phi_basic():
    out = to_base_phi(10)
    assert isinstance(out, str)
    assert out
