# Measurement-Values-System

A convenient program for performing arithmetic operations on numbers with units of measurement and exponents. It can be useful for engineers (for efficient and convenient operation on such numbers). In any case, while this program is in beta testing.

---

## Explanation of the code:

## `units_system.py`:

**File `units_system.py` contains the definition of the `Unit` class, which represents a system of units of measurement and provides arithmetic operations with these units.**

The `Unit` class has the following methods and functionality:

`__init__(self, units: dict[str, int] = None, **units_: int)`: Constructor of the `Unit` class. Accepts the units dictionary and/or a variable number of units_ arguments representing units of measurement and their exponents. Creates a `Unit` object with the specified units of measurement.

`update_units(self, other: "Unit", add: bool = True) -> "Unit"`: Updates the units of the current `Unit` object by adding or subtracting units from another `Unit` object depending on the value of the add parameter. Returns a new `Unit` object with updated units of measurement.

`_clean_(self) -> None`: Removes zero values of units of measurement and sorts them in descending order of exponents.

`__str__(self) -> str`: Returns a string representation of the `Unit` object. If the object contains only one unit of measurement with a negative exponent, a string is returned in the format `"unit_of_measurement ** exponent_"`. In other cases, a string consisting of units of measurement and their exponents separated by multiplication and division signs is returned.

`__mul__(self, other: "Unit") -> "Unit"`: Overloaded multiplication operator. Combines the units of measurement of the current `Unit` object with the units of measurement of another `Unit` object. Returns a new `Unit` object with the combined units of measurement.

`__truediv__(self, other: "Unit") -> "Unit"`: Overloaded division operator. Divides the units of the current `Unit` object into units of another `Unit` object. Returns a new `Unit` object with separated units of measurement.

`__pow__(self, power, modulo=None) -> "Unit"`: Overloaded exponentiation operator. Raises the units of the current `Unit` object to the specified power degree. Returns a new `Unit` object with units of measurement raised to a power.

`__eq__(self, other: "Unit") -> bool`: Overloaded equality operator. Compares the units of measurement of the current `Unit` object with the units of measurement of another `Unit` object. Returns True if they are equal, and False otherwise.

`__ne__(self, other: "Unit") -> bool:` Overloaded inequality operator. Compares the units of measurement of the current `Unit` object with the units of measurement of another `Unit` object. Returns True if they are not equal, and False otherwise.

`__neg__(self) -> "Unit"`: Overloaded negation operator. Returns a new `Unit` object with units of measurement in which the exponents have been changed to opposite values.

---

## `math_utils.py`:

**File `math_utils.py` contains two functions: `gexp` and `rndint`, designed for performing mathematical operations and rounding numbers.**

`gexp(num: float | int, expnum: bool = True, sepbase: int = 1) -> int | tuple[float, int]`:

Accepts the number `num`, whose type can be `float` or `int`, as well as the parameters `expnum` (boolean `value`, by default `True`) and `sepbase` (`integer`, by default `1`).
`num` is a number for which the exponent of ten is calculated.
`expnum` determines whether to return the result as a `tuple` of the number `num` and the exponent, or only the exponent.
`sepbase` indicates the bit depth by which the number should be divided to calculate the exponent.
The function calculates the exponent of the number `num` relative to the specified `sepbase` bit depth. In this case, the number `num` is divided by 10 to the power of `sepbase` as long as its absolute value is greater than or equal to 10 to the power of `sepbase`.
Either only the exponent as an `integer` is returned, or a `tuple` of `num` and exponents, depending on the value of the `expnum` parameter.

`rndint(num: float | int, accuracy: int = 13)`:

Accepts the number `num`, the type of which can be `float` or `int`, as well as the `accuracy` parameter (an `integer`, by default `13`).
`num` is the number that needs to be rounded.
`accuracy` determines the accuracy of rounding.
The function rounds the number `num` and returns the result. If the difference between the integer part of the number `num` and the number `num` itself is less than 10 to the inverse of the specified accuracy, then the integer part of the number `num` is returned, otherwise the number `num` itself is returned.

---

## `values_system.py`:


File `values_system.py` contains the definition of the `MathValue` class, which represents numeric values with units of measurement and allows you to perform various arithmetic operations on them.

The `MathValue` class has the following methods and functions:

`__init__(self, value: float | int, exp: float | int = 0, sc: dict = None, **sc_: int | float)`: Constructor of the `MathValue` class. Accepts a numeric value `value` (type can be `float` or `int`), an exponent `exp` (type can be `float` or `int`, default `0`), a dictionary `sc` and named arguments `sc`_ (which also represent a `dictionary` of units of measurement).'

`content`: A property that provides access to the contents of the `MathValue` object.

`_content`: A private `property` that stores the contents of the `MathValue` object.

`_gexp_()`: A private method that calculates the exponent of a number and updates the contents of the `MathValue` object.

`rawcalc(self) -> int | float`: A method that calculates a numeric value without an exponent.

`calc(self)`: A method that returns a new `MathValue` object with a numeric value without an exponent.

`_perform_operation_(self, other: "MathValue", add: bool) -> "MathValue"`: A private method that performs an addition or subtraction operation between two `MathValue` objects.

`_check_(self, other: "MathValue") -> None`: A private method that checks the correspondence of the units of measurement of two `MathValue` objects before performing the operation.

`__str__(self) -> str`: An overloaded method for converting a `MathValue` object to a `string`.

Methods of overloading arithmetic operators (`__sub__`, `__add__`, `__mul__`, `__rmul__`, `__truediv__`, `__rtruediv__`, `__pow__`, `__neg__`) for performing subtraction, addition, multiplication, division and exponentiation.

Methods for overloading comparison operators (`__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`) for comparing `MathValue` objects.

`__round__(self, n=None) -> "MathValue"`: Overloaded number rounding method.
