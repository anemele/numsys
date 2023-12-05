from typing import Dict, Iterable, Set, Tuple

from ..log import logger


class NumeralSystem:
    def __init__(self, char_set: Iterable[str] | None = None) -> None:
        if char_set is None:
            import string

            char_set = string.digits + string.ascii_lowercase

        self.__char_set, self._char, self._dict = self.__init(char_set)
        self.__base = len(self.__char_set)

    @classmethod
    def __init(cls, char_set: Iterable[str]) -> Tuple[Set[str], str, Dict[str, int]]:
        _set = set()
        _char = []
        for c in char_set:
            if c in _set:
                logger.debug(f'redundant char will skip: {c}')
                continue
            _set.add(c)
            _char.append(c)

        if len(_set) < 2:
            raise ValueError('not enough char given')

        _dict = {c: i for i, c in enumerate(_char)}
        return _set, ''.join(_char), _dict

    def __repr__(self):
        return f'{self.__class__} base={self.__base} char={self._char}'

    def _check_input(self):
        return NotImplemented

    def convert(self):
        return NotImplemented
