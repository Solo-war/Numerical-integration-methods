from __future__ import annotations

import ast
import math
import random
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterable, List, Tuple, Union

Number = Union[int, float]
FuncOrExpr = Union[str, Callable[[float], float]]


# Разрешённые имена и функции для безопасной оценки выражений
_ALLOWED_NAMES: Dict[str, Any] = {
    # константы
    "pi": math.pi,
    "e": math.e,
    # базовые функции
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "asin": math.asin,
    "acos": math.acos,
    "atan": math.atan,
    "sinh": math.sinh,
    "cosh": math.cosh,
    "tanh": math.tanh,
    "exp": math.exp,
    "log": math.log,
    "log10": math.log10,
    "sqrt": math.sqrt,
    "floor": math.floor,
    "ceil": math.ceil,
    "fabs": math.fabs,
    "abs": abs,
}

# Доп. удобная функция
_ALLOWED_NAMES["cot"] = lambda x: 1.0 / math.tan(x)


class _SafeEval(ast.NodeVisitor):
    """Проверка AST-дерева на безопасность и сбор имён."""

    allowed_nodes = (
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Call,
        ast.Name,
        ast.Load,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.USub,
        ast.UAdd,
        ast.FloorDiv,
        ast.Constant,
        ast.Tuple,
        ast.List,
        ast.Dict,
    )

    def visit(self, node):  # type: ignore[override]
        if not isinstance(node, self.allowed_nodes):
            raise ValueError(
                f"В выражении использована неподдерживаемая конструкция: {type(node).__name__}"
            )
        return super().visit(node)

    def visit_Call(self, node: ast.Call) -> Any:  # noqa: N802
        # Запрещаем обращения к атрибутам (напр. __import__ или os.system)
        if not isinstance(node.func, ast.Name):
            raise ValueError("Разрешены только прямые вызовы разрешённых функций")
        if node.func.id not in _ALLOWED_NAMES:
            raise ValueError(f"Функция '{node.func.id}' не разрешена")
        # Проверяем аргументы
        for arg in node.args:
            self.visit(arg)
        for kw in node.keywords:
            self.visit(kw.value)
        return None

    def visit_Name(self, node: ast.Name) -> Any:  # noqa: N802
        # Разрешаем только x, y, z и функции/константы из белого списка
        if node.id not in {"x", "y", "z"} and node.id not in _ALLOWED_NAMES:
            raise ValueError(f"Идентификатор '{node.id}' не разрешён")
        return None


def _compile_expr(expr: str) -> ast.AST:
    parsed = ast.parse(expr, mode="eval")
    _SafeEval().visit(parsed)
    return parsed


def safe_eval_expr(expr: str, *, x: float, y: float = 0.0, z: float = 0.0) -> float:
    """Безопасно вычисляет выражение expr при данных x, y, z.

    Пример: safe_eval_expr("exp(x)/(1+exp(2*x))", x=0.5)
    """
    code = _compile_expr(expr)
    env = dict(_ALLOWED_NAMES)
    env.update({"x": float(x), "y": float(y), "z": float(z)})
    return float(
        eval(compile(code, filename="<expr>", mode="eval"), {"__builtins__": {}}, env)
    )


def _as_callable(func_or_expr: FuncOrExpr) -> Callable[[float], float]:
    if callable(func_or_expr):
        return func_or_expr
    if isinstance(func_or_expr, str):
        expr = func_or_expr
        return lambda x: safe_eval_expr(expr, x=float(x))
    raise TypeError("func_or_expr должен быть функцией f(x) или строкой выражения")


@dataclass
class Step:
    i: int
    x: float
    term: float
    s: float


def integrate_trapezoidal(
    func_or_expr: FuncOrExpr, a: Number, b: Number, n: int, *, verbose: bool = False
) -> Tuple[float, List[Step]]:
    """Метод трапеций. Возвращает (значение, шаги)."""
    if n <= 0:
        raise ValueError("n должно быть положительным")
    f = _as_callable(func_or_expr)
    a = float(a)
    b = float(b)
    h = (b - a) / float(n)
    s = 0.5 * (f(a) + f(b))
    steps: List[Step] = []

    for i in range(1, n):
        x = a + i * h
        term = f(x)
        s += term
        if verbose:
            steps.append(Step(i=i, x=x, term=term, s=s))

    return h * s, steps


def integrate_simpson(
    func_or_expr: FuncOrExpr, a: Number, b: Number, n: int, *, verbose: bool = False
) -> Tuple[float, List[Step]]:
    """Метод Симпсона. n должно быть чётным. Возвращает (значение, шаги)."""
    if n <= 0 or n % 2 != 0:
        raise ValueError("Для метода Симпсона n должно быть положительным чётным")
    f = _as_callable(func_or_expr)
    a = float(a)
    b = float(b)
    h = (b - a) / float(n)
    s = f(a) + f(b)
    steps: List[Step] = []

    for i in range(1, n):
        x = a + i * h
        coeff = 4.0 if i % 2 == 1 else 2.0
        term = coeff * f(x)
        s += term
        if verbose:
            steps.append(Step(i=i, x=x, term=term, s=s))

    return (h / 3.0) * s, steps


def integrate_rectangle(
    func_or_expr: FuncOrExpr,
    a: Number,
    b: Number,
    n: int,
    *,
    mode: str = "left",
    verbose: bool = False,
) -> Tuple[float, List[Step]]:
    """Метод прямоугольников: left | right | midpoint. Возвращает (значение, шаги)."""
    if n <= 0:
        raise ValueError("n должно быть положительным")
    if mode not in {"left", "right", "midpoint"}:
        raise ValueError("mode должен быть одним из: left, right, midpoint")

    f = _as_callable(func_or_expr)
    a = float(a)
    b = float(b)
    h = (b - a) / float(n)
    s = 0.0
    steps: List[Step] = []

    if mode == "left":
        idxs = range(0, n)
        xi = lambda i: a + i * h
    elif mode == "right":
        idxs = range(1, n + 1)
        xi = lambda i: a + i * h
    else:  # midpoint
        idxs = range(0, n)
        xi = lambda i: a + (i + 0.5) * h

    for i in idxs:
        x = xi(i)
        term = f(x)
        s += term
        if verbose:
            steps.append(Step(i=i, x=x, term=term, s=s))

    return h * s, steps


def integrate_monte_carlo(
    func_or_expr: FuncOrExpr,
    a: Number,
    b: Number,
    samples: int = 10_000,
    *,
    seed: int | None = None,
) -> float:
    """Монте‑Карло интегрирование (равномерная выборка)."""
    if samples <= 0:
        raise ValueError("samples должно быть положительным")
    if seed is not None:
        random.seed(seed)
    f = _as_callable(func_or_expr)
    a = float(a)
    b = float(b)
    s = 0.0
    for _ in range(samples):
        x = random.uniform(a, b)
        s += f(x)
    return (b - a) * (s / float(samples))


# Утилита для демонстрации в примерах/CLI
DEFAULT_EXPR = "exp(x)/(1+exp(2*x))"  # Интеграл точно равен atan(e) - pi/4
