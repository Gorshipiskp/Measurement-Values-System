from units_system import Unit
from math_utils import gexp, rndint
from typing import SupportsRound


base_exponent = 1


class MathValue(SupportsRound):
    def __init__(self, value: float | int, exp: float | int = 0, sc: dict | Unit = None, **sc_: int | float):
        if isinstance(value, MathValue):
            value = value.rawcalc()

        if isinstance(sc, Unit):
            newunit: Unit = sc
        else:
            newunit: Unit = Unit(sc | sc_ if sc else sc_)

        if exp == 0:
            value, exp = gexp(value, sepbase=base_exponent)
            self.content: tuple[int | float, int, Unit] = (value, exp, newunit)
        else:
            self.content: tuple[int | float, int, Unit] = (value, exp, newunit)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        self._gexp_()

    def _gexp_(self):
        gexp_ = gexp(self.rawcalc(), sepbase=base_exponent)
        self._content = (gexp_[0], gexp_[1] * base_exponent, Unit(self.content[2].units))

    def rawcalc(self) -> int | float:
        return self.content[0] * 10 ** self.content[1]

    def calc(self):
        return MathValue(self.rawcalc(), 0, self.content[2].units)

    def _perform_operation_(self, other: "MathValue", add: bool) -> "MathValue":
        self._check_(other)

        val1 = self.rawcalc()
        val2 = other.rawcalc() * (1 if add else -1)

        new_val, exp = gexp(val1 + val2, sepbase=base_exponent)

        return MathValue(new_val, exp * base_exponent, self.content[2].units)

    def _check_(self, other: "MathValue") -> None:
        assert self.content[2] == other.content[2], ("An error occurred during the operation - A mismatch of "
                                                     "measurement units", 1, "MathValueTypeError")

    def __str__(self) -> str:
        if self.content[1] == 0:
            expon = ''
        elif self.content[1] == 1:
            expon = f' * {10 ** base_exponent}'
        else:
            expon = f" * {10 ** base_exponent} ** {rndint(self.content[1] / base_exponent)}"

        return f"{rndint(self.content[0])}{expon}{f' {self.content[2]}' if not self.content[2] is None else ''}"

    def __round__(self, n=None) -> "MathValue":
        return MathValue(round(self.rawcalc(), n), 0, self.content[2].units)

    def __add__(self, other: "MathValue") -> "MathValue":
        return self._perform_operation_(other, True)

    def __sub__(self, other: "MathValue") -> "MathValue":
        return self._perform_operation_(other, False)

    def __mul__(self, other) -> "MathValue":  # other: "MathValue" | int | float
        if isinstance(other, int | float):
            return MathValue(self.content[0] * other, self.content[1], self.content[2].units)
        else:
            new_unit = self.content[2] * other.content[2]
            new_val = self.content[0] * other.content[0]
            new_exp = self.content[1] + other.content[1]
        return MathValue(new_val, new_exp, new_unit.units)

    def __rmul__(self, other: int | float) -> "MathValue":
        return MathValue(self.content[0] * other, self.content[1], self.content[2].units)

    def __truediv__(self, other) -> "MathValue":  # other: "MathValue" | int | float
        if isinstance(other, int | float):
            return MathValue(self.content[0] / other, self.content[1], self.content[2].units)
        else:
            new_unit = self.content[2] / other.content[2]
            new_val = self.content[0] / other.content[0]
            new_exp = self.content[1] - other.content[1]
        return MathValue(new_val, new_exp, new_unit.units)

    def __rtruediv__(self, other: int | float) -> "MathValue":
        return MathValue(other / self.content[0], self.content[1], self.content[2].units)

    def __pow__(self, exponent) -> "MathValue":  # exponent: "MathValue" | int | float
        assert isinstance(exponent, int | float), ("The exponent for exponentiation of Math Value must be a number",
                                                   2, "ExponentTypeError")

        new_val = self.content[0] ** exponent
        new_exp = self.content[1] * exponent
        new_unit = self.content[2] ** exponent
        return MathValue(new_val, new_exp, new_unit.units)

    def __neg__(self) -> "MathValue":
        return MathValue(-self.content[0], self.content[1], self.content[2].units)

    def __eq__(self, other: "MathValue") -> bool:
        return all((self.content[0] == other.content[0],
                    self.content[1] == other.content[1],
                    self.content[2] == other.content[2]))

    def __ne__(self, other: "MathValue") -> bool:
        return any((self.content[0] != other.content[0],
                    self.content[1] != other.content[1],
                    self.content[2] != other.content[2]))

    def __lt__(self, other: "MathValue") -> bool:
        self._check_(other)
        return self.rawcalc() < other.rawcalc()

    def __le__(self, other: "MathValue") -> bool:
        self._check_(other)
        return self.rawcalc() <= other.rawcalc()

    def __gt__(self, other: "MathValue") -> bool:
        self._check_(other)
        return self.rawcalc() > other.rawcalc()

    def __ge__(self, other: "MathValue") -> bool:
        self._check_(other)
        return self.rawcalc() >= other.rawcalc()
