import pytest

from .ns_int import NumeralSystem, any_to_int, int_to_any


def test_repr():
    assert (
        repr(NumeralSystem())
        == "<class 'NumeralSystem'> base=36 char=0123456789abcdefghijklmnopqrstuvwxyz"
    )
    assert repr(NumeralSystem('123')) == "<class 'NumeralSystem'> base=3 char=123"
    assert repr(NumeralSystem('你好啊')) == "<class 'NumeralSystem'> base=3 char=你好啊"


def test_exception():
    with pytest.raises(ValueError):
        NumeralSystem('')
    with pytest.raises(ValueError):
        NumeralSystem('1')
    with pytest.raises(ValueError):
        NumeralSystem('好')
    with pytest.raises(ValueError):
        NumeralSystem('1213')


def test_convert_1():
    ns = NumeralSystem()
    assert ns.convert('520', 2) == '(2)1000001000'
    assert ns.convert('ff', 10, base=16) == '(10)255'
    assert ns.convert('abc', 10, base=16, show=False) == '2748'


def test_covert_2():
    ns = NumeralSystem('你好啊')
    assert ns.convert('你好啊', 2, base=3) == '(2)好你好'
    assert ns.convert('啊你好', 2, base=3) == '(2)好你你好好'


def test_covert_3():
    import string

    ns = NumeralSystem(string.digits + string.ascii_letters)
    assert ns.convert('abcdefg', 60, base=50) == '(60)3prsRwK'
    assert ns.convert('3prsRwK', 50, base=60) == '(50)abcdefg'


def test_exception_any_to_int():
    with pytest.raises(ValueError, match='repeat'):
        any_to_int('', 2, '121')
    with pytest.raises(ValueError, match='out of range'):
        any_to_int('', 1, '12')
    with pytest.raises(ValueError, match='out of range'):
        any_to_int('', 3, '12')
    with pytest.raises(ValueError, match='invalid char'):
        any_to_int('3', 2, '12')


def test_any_to_int():
    assert any_to_int('100', 3, '012') == 9
    assert any_to_int('100', 2, '012') == 4
    assert any_to_int('cba', 4, 'abcdef') == 36


def test_exception_int_to_any():
    with pytest.raises(ValueError, match='repeat'):
        int_to_any(0, 2, '121')
    with pytest.raises(ValueError, match='out of range'):
        int_to_any(0, 1, '12')
    with pytest.raises(ValueError, match='out of range'):
        int_to_any(0, 3, '12')
    assert int_to_any(-1, 2, '12') == NotImplemented


def test_int_to_any():
    assert int_to_any(9, 3, '012') == '100'
    assert int_to_any(4, 2, '012') == '100'
    assert int_to_any(36, 4, 'abcdef') == 'cba'
