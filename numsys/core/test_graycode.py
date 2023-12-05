import pytest

from .graycode import decimal_to_gray, gray_to_decimal


def test_exception():
    with pytest.raises(TypeError):
        gray_to_decimal('1')  # type: ignore
    with pytest.raises(ValueError):
        gray_to_decimal(-1)
    with pytest.raises(TypeError):
        decimal_to_gray('1')  # type: ignore
    with pytest.raises(ValueError):
        decimal_to_gray(-1)


def test_decimal_to_gray():
    assert decimal_to_gray(0) == 0
    assert decimal_to_gray(1) == 1
    assert decimal_to_gray(2) == 3
    assert decimal_to_gray(3) == 2
    assert decimal_to_gray(4) == 6
    assert decimal_to_gray(5) == 7
    assert decimal_to_gray(6) == 5
    assert decimal_to_gray(7) == 4
    assert decimal_to_gray(8) == 12
    assert decimal_to_gray(9) == 13
    assert decimal_to_gray(10) == 15
    assert decimal_to_gray(11) == 14
    assert decimal_to_gray(12) == 10
    assert decimal_to_gray(13) == 11
    assert decimal_to_gray(14) == 9
    assert decimal_to_gray(15) == 8


def test_gray_to_decimal():
    assert gray_to_decimal(0) == 0
    assert gray_to_decimal(1) == 1
    assert gray_to_decimal(3) == 2
    assert gray_to_decimal(2) == 3
    assert gray_to_decimal(6) == 4
    assert gray_to_decimal(7) == 5
    assert gray_to_decimal(5) == 6
    assert gray_to_decimal(4) == 7
    assert gray_to_decimal(12) == 8
    assert gray_to_decimal(13) == 9
    assert gray_to_decimal(15) == 10
    assert gray_to_decimal(14) == 11
    assert gray_to_decimal(10) == 12
    assert gray_to_decimal(11) == 13
    assert gray_to_decimal(9) == 14
    assert gray_to_decimal(8) == 15
