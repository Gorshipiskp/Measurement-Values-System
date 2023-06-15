def gexp(num: float | int, expnum: bool = True, sepbase: int = 1) -> int | tuple[float, int]:
    exp = 0

    if sepbase <= 0:
        raise ValueError('Степень десяти не может быть меньше или равна нулю')

    while abs(num) >= 10 ** sepbase:
        num /= 10 ** sepbase
        exp += 1
    return (num, exp) if expnum else exp


def rndint(num: float | int, accuracy: int):
    if abs(int(num) - num) < 10 ** -accuracy:
        return int(num)
    return num
