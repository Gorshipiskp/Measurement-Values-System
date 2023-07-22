from values_system import MathValue


timetests = True

answers = {
    1: MathValue(7.56, 2, kg=1, m=1, s=-2),
    2: MathValue(2.1084964598084132, -2, m=1),
    3: MathValue(9.201738966086792, 0, km=1, h=-1),
    4: MathValue(1.25, 2, N=1),
}


class Tests:
    @staticmethod
    def ex1() -> MathValue:
        P = lambda m, g, a: m * (a + g)

        m = MathValue(7, 1, kg=1)  # 70 kg
        a = MathValue(1, 0, m=1, s=-2)  # 1 m / s ** 2
        g = MathValue(9.8, 0, m=1, s=-2)  # 9.8 m / s ** 2

        return P(m, g, a)  # ~7.56 * 10 ** 2 kg * m / s ** 2

    @staticmethod
    def ex2() -> MathValue:
        to_mpersec = lambda v: MathValue(v / 3.6, 0, m=1, s=-1)
        h = lambda m, v, g, M: m ** 2 * v ** 2 / (2 * g * M ** 2)

        M = MathValue(2.8, 0, kg=1)  # 2.8 kg
        m = MathValue(10, -3, kg=1)  # 0.01 kg
        v = MathValue(6.48, 2, km=1, h=-1)  # 648 km/h
        g = MathValue(9.8, 0, m=1, s=-2)  # 9.8 m / s ** 2

        v = to_mpersec(v)  # Converting into km/s

        return h(m, v, g, M)  # ~0.021 m

    @staticmethod
    def ex3() -> MathValue:
        v = lambda M, g, h, m: (2 * M * g * h / (M + m)) ** 0.5
        to_kmperhour = lambda v: MathValue(v * 3.6, 0, km=1, h=-1)

        M = MathValue(1, 0, kg=1)  # 1 kg
        m = MathValue(500, -3, kg=1)  # 0.5 kg = 500 g
        h = MathValue(0.5, 0, m=1)  # 0.5 m
        g = MathValue(9.8, 0, m=1, s=-2)  # 9.8 m / s ** 2

        v = v(M, g, h, m)
        v = to_kmperhour(v)  # Converting into km/h

        v.ungroup()

        return v  # ~9.2 km/h

    @staticmethod
    def ex4() -> MathValue:
        F = lambda m, a: m * a

        m = MathValue(5, 0, kg=1)  # 5 kg
        a = MathValue(2.5, 1, m=1, s=-2)  # 25 m/s ** 2

        return F(m, a)  # 125 N (or 125 m * kg/s ** 2)


for exnum, answ in answers.items():
    print(f"TEST №{exnum} —", "SUCCESS" if Tests().__getattribute__(f"ex{exnum}")() == answ else "FAILED")


#  Time tests

if timetests:
    import timeit

    print()

    for exnum, answ in answers.items():
        time_ = timeit.timeit(Tests().__getattribute__(f"ex{exnum}"), number=10_000)
        print(f"TEST №{exnum} — {time_}s")
