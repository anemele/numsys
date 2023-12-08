import string
from typing import Sequence

BASE_CHAR_SET = string.digits + string.ascii_lowercase


class NumeralSystem:
    def __init__(self, char_set: Sequence[str] | None = None) -> None:
        if char_set is None:
            char_set = BASE_CHAR_SET

        length = len(char_set)
        if length < 2:
            raise ValueError
        elif length > len(set(char_set)):
            raise ValueError

        self._char_seq = char_set
        self._char_dict = {c: i for i, c in enumerate(char_set)}
        self._base = len(self._char_seq)

    def __repr__(self):
        return f'{self.__class__} base={self._base} char={self._char_seq}'

    def _check_input(self):
        return NotImplemented

    def convert(self):
        return NotImplemented
