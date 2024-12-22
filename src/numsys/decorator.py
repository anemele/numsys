from functools import wraps
from warnings import warn


def deprecated(msg: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            warn(msg, DeprecationWarning)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def unsigned_int(func):
    @wraps(func)
    def wrapper(num):
        if not isinstance(num, int):
            raise TypeError(f"expect int, got {type(num)}")
        if num < 0:
            raise ValueError("expect positive number")
        return func(num)

    return wrapper
