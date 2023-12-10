import math

from .ns_int import NumeralSystem as _NS


class NumeralSystem(_NS):
    def __init__(self) -> None:
        super().__init__()

    def _covert_frac(self, number: float, to: int, base: int, accuracy: int) -> str:
        # TODO convert fractional part
        return ''

    def _check_input(self, number, to, base, accuracy):
        super()._check_base(to, base)

        if not isinstance(accuracy, int):
            raise TypeError(f'expect int, go {type(accuracy)}')
        if accuracy < 0:
            raise ValueError(f'requires none-negative number')

        # TODO check number
        number = float(number)

        return number, to, base, accuracy

    def convert(
        self,
        number: float | str | int,
        to: int,
        *,
        base: int = 10,
        accuracy: int = 16,
        show: bool = True,
    ) -> str:
        number, to, base, accuracy = self._check_input(number, to, base, accuracy)

        f, i = math.modf(number)
        i = super().convert(round(i), to, base=base, show=False)
        if f == 0.0:
            dot = ''
        else:
            dot = '.'
            f = self._covert_frac(f, to, base, accuracy)
        prefix = f'({to})' if show else ''

        return f'{prefix}{i}{dot}{f}'


convert_float = NumeralSystem().convert
