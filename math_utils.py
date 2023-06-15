def gexp(num: float | int, expnum: bool = True, sepbase: int = 1) -> int | tuple[float, int]:
    exp = 0

    assert sepbase > 0, ('The power of ten cannot be less than or equal to zero', 3, "")

    while abs(num) >= 10 ** sepbase:
        num /= 10 ** sepbase
        exp += 1
    return (num, exp) if expnum else exp


def rndint(num: float | int, accuracy: int = 13) -> int | float:
    if abs(int(num) - num) < 10 ** -accuracy:
        return int(num)
    return num
