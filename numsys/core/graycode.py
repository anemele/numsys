from ..decorator import unsigned_int

__all__ = ['decimal_to_gray', 'gray_to_decimal']


@unsigned_int
def decimal_to_gray(dec: int) -> int:
    return dec ^ (dec >> 1)


@unsigned_int
def gray_to_decimal(gray: int) -> int:
    dec = gray
    while gray != 0:
        gray >>= 1
        dec ^= gray
    return dec
