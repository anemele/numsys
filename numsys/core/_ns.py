from typing import Dict, Iterable, Tuple

from ..log import logger


class NumeralSystem:
    def __init__(self, char_set: Iterable[str] | None = None) -> None:
        if char_set is None:
            import string

            char_set = string.digits + string.ascii_lowercase

        self._char, self._dict = self.__init(char_set)
        self._base = len(self._char)

    @classmethod
    def __init(cls, char_set: Iterable[str]) -> Tuple[str, Dict[str, int]]:
        _set = set()
        _char = []
        for c in char_set:
            if c in _set:
                logger.debug(f'repeated char will skip: {c}')
                continue
            _set.add(c)
            _char.append(c)

        if len(_char) < 2:
            raise ValueError('not enough char given')

        _dict = {c: i for i, c in enumerate(_char)}
        return ''.join(_char), _dict

    def __repr__(self):
        return f'{self.__class__} base={self._base} char={self._char}'

    def _check_input(self):
        return NotImplemented

    def convert(self):
        return NotImplemented
