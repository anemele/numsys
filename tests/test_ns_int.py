import os
import sys

sys.path.insert(0, os.getcwd())
import pytest

from numsys.core import NS_int as NumeralSystem


def test_repr():
    assert (
        repr(NumeralSystem())
        == "<class 'numsys.core.ns_int.NumeralSystem'> base=36 char=0123456789abcdefghijklmnopqrstuvwxyz"
    )
    assert (
        repr(NumeralSystem('123'))
        == "<class 'numsys.core.ns_int.NumeralSystem'> base=3 char=123"
    )
    assert (
        repr(NumeralSystem('1213'))
        == "<class 'numsys.core.ns_int.NumeralSystem'> base=3 char=123"
    )
    assert (
        repr(NumeralSystem('你好啊'))
        == "<class 'numsys.core.ns_int.NumeralSystem'> base=3 char=你好啊"
    )


def test_exception():
    with pytest.raises(ValueError):
        NumeralSystem('')
    with pytest.raises(ValueError):
        NumeralSystem('1')
    with pytest.raises(ValueError):
        NumeralSystem('好')


def test_convert_1():
    ns = NumeralSystem()
    assert ns.convert(520, 2) == '(2)1000001000'
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
