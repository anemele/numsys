import pytest

from numsys._ns2 import _any_to_int, _int_to_any


def test_exception_any_to_int():
    with pytest.raises(ValueError, match="repeat"):
        _any_to_int("", 2, "121")
    with pytest.raises(ValueError, match="out of range"):
        _any_to_int("", 1, "12")
    with pytest.raises(ValueError, match="out of range"):
        _any_to_int("", 3, "12")
    with pytest.raises(ValueError, match="invalid char"):
        _any_to_int("3", 2, "12")


def test_any_to_int():
    assert _any_to_int("100", 3, "012") == 9
    assert _any_to_int("100", 2, "012") == 4
    assert _any_to_int("cba", 4, "abcdef") == 36


def test_exception_int_to_any():
    with pytest.raises(ValueError, match="repeat"):
        _int_to_any(0, 2, "121")
    with pytest.raises(ValueError, match="out of range"):
        _int_to_any(0, 1, "12")
    with pytest.raises(ValueError, match="out of range"):
        _int_to_any(0, 3, "12")
    assert _int_to_any(-1, 2, "12") == NotImplemented


def test_int_to_any():
    assert _int_to_any(9, 3, "012") == "100"
    assert _int_to_any(4, 2, "012") == "100"
    assert _int_to_any(36, 4, "abcdef") == "cba"
