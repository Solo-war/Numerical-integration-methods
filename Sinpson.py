import math


def integrate_simpson(f, a, b, n):

    h = (b - a) / n
    x = a
    s = f(a) + f(b)
    print(f"{'i':<5}{'x':<20}{'term':<20}{'s':<20}")
    print(f"{'0':<5}{x:<20}{s:<20}{s:<20}")

    for i in range(1, n, 2):
        x += h
        term = 4 * f(x)
        s += term
        print(f"{i:<5}{x:<20}{term:<20}{s:<20}")
        x += h
        term = 2 * f(x)
        s += term
        print(f"{i+1:<5}{x:<20}{term:<20}{s:<20}")

    result = (h / 3) * s
    print(f"Итоговый результат: {result}")
    return result


# Пример использования:
def f(x):
    return math.exp(x) / (1 + math.exp(2 * x))


result = integrate_simpson(f, 0, 1, 10)
