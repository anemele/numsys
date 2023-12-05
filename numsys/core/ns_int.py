from ._ns import NumeralSystem as _NS


class NumeralSystem(_NS):
    def _int_to_any(self, number: int, base: int) -> str:
        tmp = []
        while number >= base:
            number, r = divmod(number, base)
            tmp.append(r)
        tmp.append(number)
        return ''.join(self._char[i] for i in tmp[::-1])

    def _any_to_int(self, number: str, base: int) -> int:
        decimal_number = 0
        for bit, char in enumerate(number[::-1]):
            decimal_number += self._dict[char] * base**bit
        return decimal_number

    def _check_input(self, number, to, base):
        if not isinstance(to, int) or not isinstance(base, int):
            raise TypeError('base expect `int`')
        if not 2 <= to <= self.__base:
            raise ValueError(f'`{to}` out of range [2, {self.__base}]')
        if not 2 <= base <= self.__base:
            raise ValueError(f'`{base}` out of range [2, {self.__base}]')

        if isinstance(number, int):
            number = str(number)
        elif not isinstance(number, str):
            raise TypeError(f'expect `str`, got `{type(number)}`')

        if not set(number).issubset(set(self._char[:base])):
            raise ValueError(f'out of base {base}')

        return number, to, base

    def convert(
        self, number: str | int, to: int, *, base: int = 10, show: bool = True
    ) -> str:
        """
        convert
        :param number: what to convert
        :param to: what base to convert
        :param base: current base
        :param show: if show the base as prefix, such as (2)1010
        :return: the result
        """
        number, to, base = self._check_input(number, to, base)

        if to == base:
            to_number = number
        else:
            tmp = self._any_to_int(number, base)
            to_number = self._int_to_any(tmp, to)
        prefix = f'({to})' if show else ''

        return f'{prefix}{to_number}'


ns_int = NumeralSystem().convert
