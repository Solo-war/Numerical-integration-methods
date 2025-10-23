import math


def central_rectangle_method(f, a, b, n):
    width = (b - a) / n
    total_area = 0
    results_table = []  # Список для хранения промежуточных результатов

    for i in range(n):
        mid_point = a + width * (i + 0.5)
        area = f(mid_point) * width
        total_area += area
        results_table.append(
            (mid_point, area)
        )  # Добавляем пару (середина интервала, площадь) в список

    return total_area, results_table


# Функция для вывода таблицы результатов
def print_results_table(results):
    print(f"{'Mid Point':>10} | {'Area':>10}")
    print("-" * 24)
    for mid_point, area in results:
        print(f"{mid_point:>10.6f} | {area:>10.6f}")


# Определение функции для интегрирования
def function_to_integrate(x):
    return math.exp(x) / (1 + math.exp(2 * x))


# Установка пределов интегрирования
lower_limit = 0
upper_limit = 1

# Установка количества прямоугольников
num_rectangles = 100

# Вызов метода
result, results_table = central_rectangle_method(
    function_to_integrate, lower_limit, upper_limit, num_rectangles
)

# Вывод результатов

print(" i | xi | f(xi) | Промежуточный Интеграл")
print("-" * 40)
for i, (mid_point, area) in enumerate(results_table):
    print(
        f"{i:>2} | {mid_point:>4.2f} | {function_to_integrate(mid_point):>6.4f} | {area:>20.6f}"
    )
