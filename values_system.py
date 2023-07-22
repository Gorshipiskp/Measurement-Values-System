import functools
from units_system import Unit
from math_utils import gexp, rndint
from typing import SupportsRound
from json import load
from itertools import groupby


base_exponent = 1
autogrouping = True
metrics_units = load(open("metrics_units.json", "r"))  # https://en.wikipedia.org/wiki/List_of_physical_quantities


class MathValue(SupportsRound):
    __slots__ = ('_value', '_exp', '_unit')

    def __init__(self, value: float | int, exp: float | int = 0, sc: dict | Unit = None, **sc_: int | float):
        if isinstance(value, MathValue):
            value = value.rawcalc()

        if isinstance(sc, Unit):
            newunit: Unit = sc
        else:
            newunit: Unit = Unit(sc | sc_ if sc else sc_)

        self._unit: Unit = newunit

        if exp == 0:
            value, exp = gexp(value, sepbase=base_exponent)

        self._exp: int = exp
        self.value: int | float = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value
        self._gexp_()

    @property
    def exp(self):
        return self._exp

    @exp.setter
    def exp(self, value):
        self._exp = value
        self._gexp_()

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, value):
        self._unit = value
        self._gexp_()

    def _gexp_(self):
        if autogrouping:
            self.ungroup()
            self.group(do_gexp=False)

        gexp_ = gexp(self.rawcalc(), sepbase=base_exponent)

        self._value = gexp_[0]
        self._exp = gexp_[1] * base_exponent
        self._unit = Unit(self.unit.units)

    def group(self, do_gexp: bool = True):
        units: dict[str, int] = self.unit.units

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
        units = self.unit.units.copy()

        for sym, val in units.items():
            if sym not in metrics_units:
                continue

            for sym2, val2 in metrics_units[sym]["SI_units"].items():
                self.unit.units[sym2] = self.unit.units.get(sym2, 0) + val2 * int(val / abs(val))
            del self.unit.units[sym]

    def rawcalc(self) -> int | float:
        return self.value * 10 ** self.exp

    def calc(self):
        return MathValue(self.rawcalc(), 0, self.unit.units)

    def _perform_operation_(self, other: "MathValue", add: bool) -> "MathValue":
        self._check_(other)

        new_val, exp = gexp(self.rawcalc() + other.rawcalc() * int(add / abs(add)), sepbase=base_exponent)

        return MathValue(new_val, exp * base_exponent, self.unit.units)

    def _check_(self, other: "MathValue") -> None:
        assert self.unit == other.unit, ("An error occurred during the operation - A mismatch of "
                                         "measurement units", 1, "MathValueTypeError")

    def __str__(self) -> str:
        if self.exp == 0:
            expon = ''
        elif self.exp == 1:
            expon = f' * {10 ** base_exponent}'
        else:
            expon = f" * {10 ** base_exponent} ** {rndint(self.exp / base_exponent)}"

        return f"{rndint(self.value)}{expon}{f' {self.unit}' if not self.unit is None else ''}"

    def __round__(self, n=None) -> "MathValue":
        return MathValue(round(self.rawcalc(), n), 0, self.unit.units)

    def __add__(self, other: "MathValue") -> "MathValue":
        return self._perform_operation_(other, True)

    def __sub__(self, other: "MathValue") -> "MathValue":
        return self._perform_operation_(other, False)

    def __mul__(self, other) -> "MathValue":  # other): "MathValue" | int | float
        if isinstance(other, int | float):
            return MathValue(self.value * other, self.exp, self.unit.units)
        return MathValue(self.value * other.value,
                         self.exp + other.exp,
                         (self.unit * other.unit).units)

    def __rmul__(self, other: int | float) -> "MathValue":
        return MathValue(self.value * other, self.exp, self.unit.units)

    def __truediv__(self, other) -> "MathValue":  # other: "MathValue" | int | float
        if isinstance(other, int | float):
            return MathValue(self.value / other, self.exp, self.unit.units)
        return MathValue(self.value / other.value,
                         self.exp - other.exp,
                         (self.unit / other.unit).units)

    def __rtruediv__(self, other: int | float) -> "MathValue":
        return MathValue(other / self.value, self.exp, self.unit.units)

    def __pow__(self, exponent) -> "MathValue":  # exponent: "MathValue" | int | float
        assert isinstance(exponent, int | float), ("The exponent for exponentiation of Math Value must be a number",
                                                   2, "ExponentTypeError")
        return MathValue(self.value ** exponent, self.exp * exponent, (self.unit ** exponent).units)

    def __neg__(self) -> "MathValue":
        return MathValue(-self.value, self.exp, self.unit.units)

    def __eq__(self, other: "MathValue") -> bool:
        return all((self.value == other.value,
                    self.exp == other.exp,
                    self.unit == other.unit))

    def __ne__(self, other: "MathValue") -> bool:
        return any((self.value != other.value,
                    self.exp != other.exp,
                    self.unit != other.unit))

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
