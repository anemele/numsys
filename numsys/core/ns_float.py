import math

from ._ns import NumeralSystem as _NS
from .ns_int import ns_int as _ns_int


class NumeralSystem(_NS):
    def __init__(self) -> None:
        super().__init__()

    def _covert_frac(self, number: float, to: int, base: int, accuracy: int) -> str:
        # TODO
        return ''

    def _check_input(self):
        pass

    def convert(
        self,
        number: float | str | int,
        to: int,
        *,
        base: int = 10,
        accuracy: int = 16,
        show: bool = True,
    ) -> str:
        # TODO check input
        f_number: float = float(number)

        f, i = math.modf(f_number)
        i = _ns_int(round(i), to, base=base, show=False)
        if f == 0.0:
            dot = ''
        else:
            dot = '.'
            f = self._covert_frac(f, to, base, accuracy)
        prefix = f'({to})' if show else ''

        return f'{prefix}{i}{dot}{f}'


ns_float = NumeralSystem().convert
