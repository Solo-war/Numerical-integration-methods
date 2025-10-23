"""
Утилиты для безопасного вычисления выражений f(x[,y,z]) и CAS‑операций.

CAS: используется SymPy (производные и решение уравнений/выражений).
"""

from __future__ import annotations

from typing import List, Optional

# CAS (SymPy)
import sympy as sp

from integrators import safe_eval_expr


def evaluate_function(
    func_str: str, x: float, y: float = 0.0, z: float = 0.0
) -> Optional[float]:
    """Безопасно вычисляет выражение над x[,y,z]. Возвращает None при ошибке."""
    try:
        return safe_eval_expr(func_str, x=float(x), y=float(y), z=float(z))
    except Exception:
        return None


def replace_power_operator(expression: str) -> str:  # type: ignore[no-redef]
    """Совместимость: заменяет '**' на '^' (удобно для вывода)."""
    return expression.replace("**", "^")


def restore_power_operator(expression: str) -> str:  # type: ignore[no-redef]
    """Совместимость: заменяет '^' на '**' (нужно для Python/SymPy)."""
    return expression.replace("^", "**")


def _sympify(expr: str) -> sp.Expr:
    expr_py = restore_power_operator(expr)
    # Ограничиваем доступные имена для sympify (без неожиданных функций)
    syms = {"x": sp.Symbol("x"), "y": sp.Symbol("y"), "z": sp.Symbol("z")}
    allowed = {
        **syms,
        "pi": sp.pi,
        "E": sp.E,
        "sin": sp.sin,
        "cos": sp.cos,
        "tan": sp.tan,
        "asin": sp.asin,
        "acos": sp.acos,
        "atan": sp.atan,
        "sinh": sp.sinh,
        "cosh": sp.cosh,
        "tanh": sp.tanh,
        "exp": sp.exp,
        "log": sp.log,
        "sqrt": sp.sqrt,
        "cot": sp.cot,
    }
    return sp.sympify(expr_py, locals=allowed, convert_xor=False)


def derivative_function(func_str: str, var: str = "x") -> str:
    """Возвращает строку производной d/dvar func_str (Python‑совместимую)."""
    expr = _sympify(func_str)
    sym = sp.Symbol(var)
    d = sp.diff(expr, sym)
    return restore_power_operator(str(sp.simplify(d)))


def replace_strings(s: str, target: str, repl: str):
    """Возвращает варианты строки, где target заменён на repl, с разными сдвигами."""
    res, start = [], 0
    L = len(target)
    while True:
        i = s.find(target, start)
        if i == -1:
            break
        res.append(s[:i] + repl + s[i + L :])
        start = i + 1
    return res


def extract_variable(func_str: str, var: str = "y") -> List[str]:
    """Решает уравнение func_str == 0 относительно переменной var.

    Возвращает список решений (как строки Python‑совместимых выражений).
    """
    expr = _sympify(func_str)
    sym = sp.Symbol(var)
    sols = sp.solve(sp.Eq(expr, 0), sym, dict=False)
    out = [
        restore_power_operator(str(sp.simplify(s)))
        for s in (sols if isinstance(sols, list) else [sols])
    ]
    return out


def extract_variable_from_equation(func_str: str, ext: str = "y") -> List[str]:
    """Решает уравнение "left=right" относительно переменной ext.

    Если '=' нет, трактует как выражение == 0.
    """
    if "=" in func_str:
        left_str, right_str = func_str.split("=", 1)
        left = _sympify(left_str)
        right = _sympify(right_str)
        eq = sp.Eq(left, right)
    else:
        eq = sp.Eq(_sympify(func_str), 0)

    sym = sp.Symbol(ext)
    sols = sp.solve(eq, sym, dict=False)
    out = [
        restore_power_operator(str(sp.simplify(s)))
        for s in (sols if isinstance(sols, list) else [sols])
    ]
    return out


def split_by_comma(string: str):
    return string.split(",")
