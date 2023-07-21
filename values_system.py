from units_system import Unit
from math_utils import gexp, rndint
from typing import SupportsRound
from json import load
from itertools import groupby


base_exponent = 1
autogrouping = True
metrics_units = load(open("metrics_units.json", "r"))  # https://en.wikipedia.org/wiki/List_of_physical_quantities


class MathValue(SupportsRound):
    __slots__ = ('_content', 'units_cl')

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
        self.units_cl = self.content[2].units

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        self._content = value
        self._gexp_()

    def _gexp_(self):
        if autogrouping:
            self.ungroup()
            self.group(do_gexp=False)

        gexp_ = gexp(self.rawcalc(), sepbase=base_exponent)
        self._content = (gexp_[0], gexp_[1] * base_exponent, Unit(self.content[2].units))

    def group(self, do_gexp: bool = True):
        units: dict[str, int] = self.content[2].units

        for sym, info in metrics_units.items():
            for sym_units in info['units']:
                if not all(unit in units for unit in sym_units):
                    return

                alll: groupby = groupby([units[unit] ^ val >= 0 for unit, val in sym_units.items()])

                if not (next(alll, True) and not next(alll, False)):
                    continue

                units_counts: list[int] = [int(units[unit] / val) for unit, val in sym_units.items()]
                min_unit: int = min(map(abs, units_counts))

                if min_unit <= 0:
                    continue

                sign: int = int(units_counts[0] / abs(units_counts[0]))

                for unit, val in sym_units.items():
                    if val * min_unit * sign == units[unit]:
                        del units[unit]
                    else:
                        units[unit] -= val * min_unit * sign

                units[sym] = min_unit * sign

                if do_gexp:
                    self._gexp_()
                break

    def ungroup(self):
        units = self.content[2].units.copy()

        for sym, val in units.items():
            if sym not in metrics_units:
                continue

            for sym2, val2 in metrics_units[sym]["SI_units"].items():
                self.content[2].units[sym2] = self.content[2].units.get(sym2, 0) + val2 * int(val / abs(val))
            del self.content[2].units[sym]

    def rawcalc(self) -> int | float:
        return self.content[0] * 10 ** self.content[1]

    def calc(self):
        return MathValue(self.rawcalc(), 0, self.units_cl)

    def _perform_operation_(self, other: "MathValue", add: bool) -> "MathValue":
        self._check_(other)

        val1: float | int = self.rawcalc()
        val2: float | int = other.rawcalc() * int(add / abs(add))

        new_val, exp = gexp(val1 + val2, sepbase=base_exponent)

        return MathValue(new_val, exp * base_exponent, self.units_cl)

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
        return MathValue(round(self.rawcalc(), n), 0, self.units_cl)

    def __add__(self, other: "MathValue") -> "MathValue":
        return self._perform_operation_(other, True)

    def __sub__(self, other: "MathValue") -> "MathValue":
        return self._perform_operation_(other, False)

    def __mul__(self, other) -> "MathValue":  # other): "MathValue" | int | float
        if isinstance(other, int | float):
            return MathValue(self.content[0] * other, self.content[1], self.units_cl)
        else:
            new_unit = self.content[2] * other.content[2]
            new_val = self.content[0] * other.content[0]
            new_exp = self.content[1] + other.content[1]
        return MathValue(new_val, new_exp, new_unit.units)

    def __rmul__(self, other: int | float) -> "MathValue":
        return MathValue(self.content[0] * other, self.content[1], self.units_cl)

    def __truediv__(self, other) -> "MathValue":  # other: "MathValue" | int | float
        if isinstance(other, int | float):
            return MathValue(self.content[0] / other, self.content[1], self.units_cl)

        new_unit = self.content[2] / other.content[2]
        new_val = self.content[0] / other.content[0]
        new_exp = self.content[1] - other.content[1]
        return MathValue(new_val, new_exp, new_unit.units)

    def __rtruediv__(self, other: int | float) -> "MathValue":
        return MathValue(other / self.content[0], self.content[1], self.units_cl)

    def __pow__(self, exponent) -> "MathValue":  # exponent: "MathValue" | int | float
        assert isinstance(exponent, int | float), ("The exponent for exponentiation of Math Value must be a number",
                                                   2, "ExponentTypeError")

        new_val = self.content[0] ** exponent
        new_exp = self.content[1] * exponent
        new_unit = self.content[2] ** exponent
        return MathValue(new_val, new_exp, new_unit.units)

    def __neg__(self) -> "MathValue":
        return MathValue(-self.content[0], self.content[1], self.units_cl)

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
