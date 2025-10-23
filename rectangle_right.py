import math


def right_rectangle_method(f, a, b, n):
    h = (b - a) / n
    results = []
    for i in range(1, n + 1):
        x_i = a + i * h
        f_x_i = f(x_i)
        results.append((x_i, f_x_i))
        print(f"x_{i}: {x_i:.4f}, f(x_{i}): {f_x_i:.4f}")
    integral = sum([f_x for _, f_x in results]) * h
    return integral, results


def f(x):
    return math.exp(x) / (1 + math.exp(2 * x))


# Вызов функции и вывод таблицы
integral, results_table = right_rectangle_method(f, 0, 1, 10)
print(f"Приближенное значение интеграла: {integral:.4f}")
