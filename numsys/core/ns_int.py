from functools import wraps
from typing import Sequence

from ._ns import BASE_CHAR_SET
from ._ns import NumeralSystem as _NS


class NumeralSystem(_NS):
    def _int_to_any(self, number: int, base: int) -> str:
        def f():
            n = number
            while n != 0:
                n, i = divmod(n, base)
                yield self._char_seq[i]

        return ''.join(f())[::-1]

    def _any_to_int(self, number: str, base: int) -> int:
        return sum(base**p * self._char_dict[c] for p, c in enumerate(number[::-1]))

    def _check_base(self, to, base):
        if not 2 <= to <= self._base:
            raise ValueError(f'{to} out of range [2, {self._base}]')
        if not 2 <= base <= self._base:
            raise ValueError(f'{base} out of range [2, {self._base}]')

    def convert(self, number: str, to: int, *, base: int = 10, show: bool = True) -> str:
        """
        convert
        :param number: what to convert
        :param to: what base to convert
        :param base: current base
        :param show: if show the base as prefix, such as (2)1010
        :return: the result
        """
        self._check_base(to, base)

        if not set(number).issubset(set(self._char_seq[:base])):
            raise ValueError(f'{number} contains invalid char')

        if to == base:
            to_number = number
        else:
            tmp = self._any_to_int(number, base)
            to_number = self._int_to_any(tmp, to)
        prefix = f'({to})' if show else ''

        return f'{prefix}{to_number}'


convert_int = NumeralSystem().convert


def _check(func):
    @wraps(func)
    def wrapper(num: int | str, base: int, chars: Sequence[str]):
        len_chars = len(chars)
        char_set = set(chars)
        if len_chars > len(char_set):
            raise ValueError('requires no-repeat char sequence.')
        if base < 2 or base > len_chars:
            raise ValueError(f'base out of range [2, {len_chars}]')
        if isinstance(num, str) and not set(num).issubset(char_set):
            raise ValueError(f'{num} contains invalid char')

        return func(num, base, chars[:base])

    return wrapper


@_check
def any_to_int(num: str, base: int, chars: Sequence[str]) -> int:
    """convert any integer of any base to int, which is human friendly.
    `chars` is a no-repeat char sequence, user guaranteed."""

    char_dict = {c: i for i, c in enumerate(chars)}
    return sum(base**p * char_dict[c] for p, c in enumerate(num[::-1]))


@_check
def int_to_any(num: int, base: int, chars: Sequence[str]) -> str:
    """convert int to any base of any form.
    `num` is an integer, user guaranteed.
    `chars` is a no-repeat char sequence, user guaranteed."""

    if num < 0:
        return NotImplemented

    def f():
        n = num
        while n != 0:
            n, i = divmod(n, base)
            yield chars[i]

    return ''.join(f())[::-1]


def convert_any_int(
    num: str, base: int, to: int, from_set: Sequence[str], to_set: Sequence[str] | None
) -> str:
    return int_to_any(any_to_int(num, base, from_set), to, to_set or BASE_CHAR_SET)
