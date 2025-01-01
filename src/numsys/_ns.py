import string
from typing import Sequence

BASE_CHAR_SET = string.digits + string.ascii_lowercase


class NumeralSystem:
    def __init__(self, char_set: Sequence[str] = BASE_CHAR_SET) -> None:
        length = len(char_set)
        if length < 2:
            raise ValueError("requires at least 2 char in char_set")
        if length > len(set(char_set)):
            raise ValueError("requires no-repeat char sequence.")

        self._char_seq = char_set
        self._char_dict = {c: i for i, c in enumerate(char_set)}
        self._base = length

    def __repr__(self):
        return f"<class '{self.__class__.__name__}'> base={self._base} char={self._char_seq}"

    def _int_to_any(self, number: int, base: int) -> str:
        def f():
            n = number
            while n != 0:
                n, i = divmod(n, base)
                yield self._char_seq[i]

        return "".join(f())[::-1]

    def _any_to_int(self, number: str, base: int) -> int:
        return sum(base**p * self._char_dict[c] for p, c in enumerate(number[::-1]))

    def _check_base(self, to, base):
        _base = self._base
        if not 2 <= to <= _base:
            raise ValueError(f"{to} out of range [2, {_base}]")
        if not 2 <= base <= _base:
            raise ValueError(f"{base} out of range [2, {_base}]")

    def convert(
        self, number: str, to: int, *, base: int = 10, show: bool = True
    ) -> str:
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
            raise ValueError(f"{number} contains invalid char")

        if to == base:
            to_number = number
        else:
            tmp = self._any_to_int(number, base)
            to_number = self._int_to_any(tmp, to)
        prefix = f"({to})" if show else ""

        return f"{prefix}{to_number}"


cvt_num = NumeralSystem().convert
