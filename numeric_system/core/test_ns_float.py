import pytest

from .ns_float import NumeralSystem


def test_exception():
    with pytest.raises(Exception):
        raise Exception


@pytest.mark.skip
def test_convert():
    ns = NumeralSystem()
    assert ns.convert(0.25, 2) == '(2)0.01'
    assert ns.convert(0.75, 2) == '(2)0.11'
    assert ns.convert('0.125', 2) == '(2)0.001'
    assert ns.convert(1.75, 16, show=False) == '1.a'
    assert ns.convert(-1.75, 16, show=False) == '-1.a'
