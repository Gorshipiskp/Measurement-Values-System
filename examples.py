def ex1():
    from values_system import MathValue

    P = lambda m, g, a: m * (a + g)

    m = MathValue(7, 1, kg=1)  # 70 kg
    a = MathValue(1, 0, m=1, s=-2)  # 1 m / s ** 2
    g = MathValue(9.8, 0, m=1, s=-2)  # 9.8 m / s ** 2

    print(P(m, g, a))  # 7.56 * 10 ** 2 kg * m / s ** 2


def ex2():
    from values_system import MathValue

    to_mpersec = lambda v: MathValue(v / 3.6, 0, m=1, s=-1)
    h = lambda m, v, g, M: m ** 2 * v ** 2 / (2 * g * M ** 2)

    M = MathValue(2.8, 0, kg=1)  # 2.8 kg
    m = MathValue(10, -3, kg=1)  # 0.01 kg
    v = MathValue(6.48, 2, km=1, h=-1)  # 648 km/h
    g = MathValue(9.8, 0, m=1, s=-2)  # 9.8 m / s ** 2

    v = to_mpersec(v)  # Converting into km/s

    print(round(h(m, v, g, M), 3))  # 0.021 m


def ex3():
    from values_system import MathValue

    v = lambda M, g, h, m: (2 * M * g * h / (M + m)) ** 0.5
    to_kmperhour = lambda v: MathValue(v * 3.6, 0, km=1, h=-1)

    M = MathValue(1, 0, kg=1)  # 1 kg
    m = MathValue(500, -3, kg=1)  # 0.5 kg = 500 g
    h = MathValue(0.5, 0, m=1)  # 0.5 m
    g = MathValue(9.8, 0, m=1, s=-2)  # 9.8 m / s ** 2

    v = v(M, g, h, m)
    v = to_kmperhour(v)  # Converting into km/h

    print(round(v, 1))  # 9.2 km/h


ex3()
