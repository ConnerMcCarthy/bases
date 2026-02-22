import pytest

from numbases.bases import from_base, to_base


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
