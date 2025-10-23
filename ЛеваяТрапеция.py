import math


def left_rectangle_method(f, a, b, n):
    h = (b - a) / n
    result = 0
    print("i", "xi", "f(xi)", "Промежуточный Интеграл", sep="\t")
    for i in range(n):
        xi = a + i * h
        result += f(xi)
        print(i, round(xi, 4), round(f(xi), 4), round(result * h, 4), sep="\t")
    result *= h
    return result


# Функция, которую мы интегрируем
def f(x):
    return math.exp(x) / (1 + math.exp(2 * x))


# Вызов функции с 10 прямоугольниками
approx_integral = left_rectangle_method(f, 0, 1, 10)
print(f"Приближенное значение интеграла: {approx_integral}")
