rounding = True
extended_accurate = True
transl_units = True
caching = True


if caching:
    import functools


def cache(func):
    if caching:
        return functools.cache(func)
    return func


@cache
def gexp(num: float | int, expnum: bool = True, sepbase: int = 1) -> int | tuple[float, int]:
    exp: int = 0

    assert sepbase > 0, ('The power of ten cannot be less than or equal to zero', 3, "")

    while abs(num) >= 10 ** sepbase:
        num /= 10 ** sepbase
        exp += 1
    return (num, exp) if expnum else exp


@cache
def rndint(num: float | int, accuracy: int = 15) -> int | float:
    if not rounding:
        return num

    if abs(int(num) - num) < 10 ** -accuracy:
        return int(num)
    return round(num, accuracy) if extended_accurate else num
