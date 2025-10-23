import math
import random


def monte_carlo_integration(f, a, b, samples=1000):
    sum_of_samples = 0.0
    for _ in range(samples):
        x = random.uniform(a, b)
        sum_of_samples += f(x)
    return (b - a) * sum_of_samples / samples


def function_to_integrate(x):
    return math.exp(x) / (1 + math.exp(2 * x))  # Replace with your function


lower_bound = 0
upper_bound = 1


num_samples = 10000


integral_estimate = monte_carlo_integration(
    function_to_integrate, lower_bound, upper_bound, num_samples
)
print(f"Расчетное значение интеграла составляет: {integral_estimate}")
