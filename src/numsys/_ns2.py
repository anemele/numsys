import string
from functools import wraps
from typing import Sequence

BASE_CHAR_SET = string.digits + string.ascii_lowercase


def _check(func):
    @wraps(func)
    def wrapper(num: int | str, base: int, chars: Sequence[str]):
        len_chars = len(chars)
        char_set = set(chars)
        if len_chars > len(char_set):
            raise ValueError("requires no-repeat char sequence.")
        if base < 2 or base > len_chars:
            raise ValueError(f"base out of range [2, {len_chars}]")
        if isinstance(num, str) and not set(num).issubset(char_set):
            raise ValueError(f"{num} contains invalid char")

        return func(num, base, chars[:base])

    return wrapper


@_check
def _any_to_int(num: str, base: int, chars: Sequence[str]) -> int:
    """convert any integer of any base to int, which is human friendly.
    `chars` is a no-repeat char sequence, user guaranteed."""

    char_dict = {c: i for i, c in enumerate(chars)}
    return sum(base**p * char_dict[c] for p, c in enumerate(num[::-1]))


@_check
def _int_to_any(num: int, base: int, chars: Sequence[str]) -> str:
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

    return "".join(f())[::-1]


def convert_any_int(
    num: str,
    base: int,
    to: int,
    from_seq: Sequence[str] | None = None,
    to_seq: Sequence[str] | None = None,
    show: bool = True,
) -> str:
    ret = _int_to_any(
        _any_to_int(num, base, from_seq or BASE_CHAR_SET),
        to,
        to_seq or BASE_CHAR_SET,
    )
    prefix = f"({to})" if show else ""
    return prefix + ret
