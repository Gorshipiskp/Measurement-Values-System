class Unit:
    def __init__(self, units: dict[str, int] = None, **units_: int):
        self.units = units_ if not units else units | units_
        self._clean_()

    def update_units(self, other: "Unit", add: bool = True) -> "Unit":
        new_units = self.units.copy()

        for char, val in other.units.items():
            new_units[char] = new_units.get(char, 0) + (val if add else -val)
        return Unit(new_units)

    def _clean_(self) -> None:
        self.units = {key: value for key, value in self.units.items() if value != 0}
        self.units = {key: self.units[key] for key in sorted(self.units, key=self.units.get, reverse=True)}

    def __str__(self) -> str:
        if len(self.units) == 1 and tuple(self.units.values())[0] < 0:
            return f"{tuple(self.units.keys())[0]} ** {tuple(self.units.values())[0]}"

        units = []

        for cur_id, (char, val) in enumerate(self.units.items()):
            if cur_id == 0:
                if val == 1:
                    units.append(char)
                else:
                    units.append(f"{char}{f' ** {val}' if val != 1 else ''}")
            else:
                units.append("*" if val > 0 else "/")
                units.append(f"{char}{f' ** {abs(val)}' if abs(val) != 1 else ''}")
        return " ".join(units)

    def __mul__(self, other: "Unit") -> "Unit":
        return self.update_units(other, add=True)

    def __truediv__(self, other: "Unit") -> "Unit":
        return self.update_units(other, add=False)

    def __pow__(self, power, modulo=None) -> "Unit":
        new_units = self.units.copy()

        for key in new_units.keys():
            new_units[key] *= power
        return Unit(new_units)

    def __eq__(self, other: "Unit") -> bool:
        return self.units == other.units

    def __ne__(self, other: "Unit") -> bool:
        return self.units != other.units

    def __neg__(self) -> "Unit":
        return Unit({unit: -exponent for unit, exponent in self.units.items()})
