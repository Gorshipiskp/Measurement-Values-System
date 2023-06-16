# Measurement-Values-System

A convenient program for performing arithmetic operations on numbers with units of measurement and exponents. It can be useful for engineers who need to efficiently and conveniently work with such numbers. Please note that the program is currently in beta testing.

#### _Information is current as of the 9th commit_

---

## Usage examples:

``` python
a = MathValue(3, 1, W=1)
b = MathValue(1.5, 2, W=1)
c = MathValue(2, 2, cm=2)
d = MathValue(3, 1, s=-1)

f = a * b / c / d
print(f)  # 0.75 W ** 2 * s / cm ** 2
```

## Explanation:

First, let's calculate the numerical values:

``` python
# a = 3 * 10 ** 1,
# because MathValue(value, exponent_of_ten, units_of_measurement)
# a = value * 10 ** exponent_of_ten

a * b / c / d == (3 * 10 ** 1) * (1.5 * 10 ** 2) / (2 * 10 ** 2) / (3 * 10 ** 1) == 30 * 150 / 200 / 30 == 0.75
```

As we can see, the numerical value is correct. Now let's determine the units of measurement:

``` python
# d = s ** -1,
# but the expression a / s ** -1 = a * s is also true
# since we change the sign and then the operands
# that is why if there are several units of measurement, the first one will always have a positive exponent (if there is one)

a * b / c / d == W * W / cm ** 2 / s ** -1 == W ** 2 / cm ** 2 * s

# Sort by sign (multiplication - first, division - second):

W ** 2 * s / cm ** 2
```

Putting it all together:

`0.75 W ** 2 * s / cm ** 2`

The answer calculated manually matches the answer calculated by the program.

---

## Explanation of the code:


## `units_system.py`:

**File `units_system.py` contains the definition of the `Unit` class, which represents a system of units of measurement and provides arithmetic operations with these units.**

The `Unit` class provides the following methods and functionality:

- `__init__(self, units: dict[str, int] = None, **units_: int)`: Constructor of the `Unit` class. Accepts a dictionary of units (`units`) and/or a variable number of keyword arguments (`units_`) representing units of measurement and their exponents. Creates a `Unit` object with the specified units of measurement.
- `update_units(self, other: "Unit", add: bool = True) -> "Unit"`: Updates the units of the current `Unit` object by adding or subtracting units from another `Unit` object based on the `add` parameter. Returns a new `Unit` object with the updated units of measurement.
- `_clean_(self) -> None`: Removes zero-valued units of measurement and sorts them in descending order of exponents.
- `__str__(self) -> str`: Returns a string representation of the `Unit` object. If the object contains only one unit of measurement with a negative exponent, it returns a string in the format `"unit_of_measurement ** exponent_"`. Otherwise, it returns a string consisting of units of measurement and their exponents separated by multiplication and division signs.
- Methods for overloaded

 arithmetic operators (`__mul__`, `__truediv__`, `__pow__`) to perform multiplication, division, and exponentiation.
- Methods for overloaded comparison operators (`__eq__`, `__ne__`) to compare `Unit` objects.
- Methods for overloaded unary operators (`__neg__`) for negation.

## `math_utils.py`:

**File `math_utils.py` contains two functions: `gexp` and `rndint`, designed for performing mathematical operations and rounding numbers.**

- `gexp(num: float | int, expnum: bool = True, sepbase: int = 1) -> int | tuple[float, int]`: Accepts a number (`num`) of type `float` or `int`, along with optional parameters `expnum` (a boolean indicating whether to return the result as a tuple of the number `num` and the exponent) and `sepbase` (an integer indicating the bit depth by which the number should be divided to calculate the exponent). The function calculates the exponent of the number `num` relative to the specified `sepbase` bit depth. It returns either only the exponent as an integer or a tuple of `num` and the exponent, depending on the `expnum` parameter.
- `rndint(num: float | int, accuracy: int = 12)`: Accepts a number (`num`) of type `float` or `int`, along with an optional `accuracy` parameter (an integer indicating the accuracy of rounding). The function rounds the number `num` and returns the result. If the difference between the integer part of `num` and `num` itself is less than 10 to the power of the inverse of the specified accuracy, the integer part is returned. Otherwise, `num` itself is returned.

## `values_system.py`:

**File `values_system.py` contains the definition of the `MathValue` class, which represents numeric values with units of measurement and allows various arithmetic operations to be performed on them.**

The `MathValue` class provides the following methods and functionality:

- `__init__(self, value: float | int, exp: float | int = 0, sc: dict | Unit = None, **sc_: int | float)`: Constructor of the `MathValue` class. Accepts a numeric value (`value`) of type `float` or `int`, an exponent (`exp`) of type `float` or `int` (default is `0`), a `sc` dictionary, and named arguments (`sc_`) representing units of measurement and their exponents.
- `content`: A property that provides access to the contents of the `MathValue` object.
- `_content`: A private property that stores the contents of the `MathValue` object.
- `_gexp_()`: A private method that calculates the exponent of a number and updates the contents of the `MathValue` object.
- `rawcalc(self) -> int | float`: A method that calculates the numeric value without the exponent.
- `calc(self)`: A method that returns a new `MathValue` object with the numeric value without the exponent.
- `_perform_operation_(self, other: "MathValue", add: bool) -> "MathValue"`: A private method that performs addition or subtraction operations between two `MathValue` objects.
- `_check_(self, other: "MathValue") -> None`: A private method that checks the correspondence of the units of measurement of two `MathValue` objects before performing an operation.
- `__str__(self) -> str`: An overloaded method that converts a `MathValue` object to a string.
- Methods for overloading arithmetic operators (`__sub__`, `__add__`, `__mul__`, `__truediv__`, `__pow__`, `__neg__`) to perform subtraction, addition, multiplication, division, exponentiation, and negation.
- Methods for overloading comparison operators (`__eq__`, `__ne__`, `__lt__`, `__le__`, `__gt__`, `__ge__`) to compare `MathValue` objects.
- `__round__(self, n=None) -> "MathValue"`: An overloaded method for rounding a `MathValue` object.

---

## Errors' code

### `1 – MathValueTypeError`
This error is raised when attempting to perform an operation on two non-equatable `MathValue` objects, such as adding two `MathValue` objects with different units of measurement.

### `2 – ExponentTypeError`
This error is raised when attempting to raise a `MathValue` to a non-numeric power.

### `3 – TenPowerError`
This error is raised when attempting to run the `gexp` function (from `math_utils.py`) with a `sepbase` parameter less than or equal to zero.