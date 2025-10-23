import math
import unittest

from integrators import (
    DEFAULT_EXPR,
    integrate_monte_carlo,
    integrate_rectangle,
    integrate_simpson,
    integrate_trapezoidal,
    safe_eval_expr,
)


def exact_integral_exp_expr(a=0.0, b=1.0):
    # ∫ exp(x)/(1+exp(2x)) dx = atan(exp(x)) от a до b
    return math.atan(math.e**b) - math.atan(math.e**a)


class TestIntegrators(unittest.TestCase):
    def test_safe_eval(self):
        val = safe_eval_expr("exp(x)/(1+exp(2*x))", x=0.5)
        self.assertAlmostEqual(val, math.exp(0.5) / (1 + math.exp(1.0)))

    def test_trapezoid(self):
        exact = exact_integral_exp_expr(0.0, 1.0)
        val, _ = integrate_trapezoidal(DEFAULT_EXPR, 0.0, 1.0, 2000)
        self.assertAlmostEqual(val, exact, places=6)

    def test_simpson(self):
        exact = exact_integral_exp_expr(0.0, 1.0)
        val, _ = integrate_simpson(DEFAULT_EXPR, 0.0, 1.0, 200)
        # Симпсон обычно точнее: проверим погрешность строже
        self.assertAlmostEqual(val, exact, places=8)

    def test_rect_midpoint(self):
        exact = exact_integral_exp_expr(0.0, 1.0)
        val, _ = integrate_rectangle(DEFAULT_EXPR, 0.0, 1.0, 5000, mode="midpoint")
        self.assertAlmostEqual(val, exact, places=6)

    def test_rect_left_right(self):
        f = "x**2"
        exact = 1.0 / 3.0
        val_left, _ = integrate_rectangle(f, 0.0, 1.0, 10_000, mode="left")
        val_right, _ = integrate_rectangle(f, 0.0, 1.0, 10_000, mode="right")
        self.assertAlmostEqual(val_left, exact, places=4)
        # Правый прямоугольник сходится медленнее (O(1/n)) — проверим 3 знака
        self.assertAlmostEqual(val_right, exact, places=3)

    def test_monte_carlo(self):
        exact = exact_integral_exp_expr(0.0, 1.0)
        val = integrate_monte_carlo(DEFAULT_EXPR, 0.0, 1.0, samples=100_000, seed=42)
        self.assertAlmostEqual(val, exact, places=3)


if __name__ == "__main__":
    unittest.main(verbosity=2)
