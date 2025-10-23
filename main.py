"""
CLI для численного интегрирования.

Примеры:
  python main.py --method simpson --expr "exp(x)/(1+exp(2*x))" -a 0 -b 1 -n 100
  python main.py --method trapezoid --expr "sin(x)" -a 0 -b 3.1415926535 -n 1000
  python main.py --method rect --mode midpoint --expr "x**2" -a 0 -b 1 -n 200
  python main.py --method mc --expr "exp(x)/(1+exp(2*x))" -a 0 -b 1 --samples 50000
"""

from __future__ import annotations

import argparse
from typing import List, Tuple

from integrators import (
    DEFAULT_EXPR,
    Step,
    integrate_monte_carlo,
    integrate_rectangle,
    integrate_simpson,
    integrate_trapezoidal,
)


def _print_steps(steps: List[Step]) -> None:
    print(f"{'i':>6} {'x':>16} {'term':>16} {'s':>16}")
    for st in steps:
        print(f"{st.i:>6d} {st.x:>16.8f} {st.term:>16.8f} {st.s:>16.8f}")


def main() -> None:
    p = argparse.ArgumentParser(description="Численное интегрирование")
    p.add_argument(
        "--method", choices=["trapezoid", "simpson", "rect", "mc"], required=True
    )
    p.add_argument(
        "--expr",
        type=str,
        default=DEFAULT_EXPR,
        help="Выражение f(x) или используйте свой callable",
    )
    p.add_argument("-a", type=float, required=True, help="Нижний предел интегрирования")
    p.add_argument(
        "-b", type=float, required=True, help="Верхний предел интегрирования"
    )
    p.add_argument("-n", type=int, help="Число разбиений (для trapezoid/simpson/rect)")
    p.add_argument(
        "--mode",
        choices=["left", "right", "midpoint"],
        default="midpoint",
        help="Режим для rect",
    )
    p.add_argument(
        "--samples", type=int, default=10000, help="Число выборок для Монте‑Карло"
    )
    p.add_argument("--verbose", action="store_true", help="Печатать таблицу шагов")

    args = p.parse_args()

    if args.method in {"trapezoid", "simpson", "rect"} and (args.n is None):
        p.error("Для выбранного метода требуется параметр -n")

    if args.method == "trapezoid":
        val, steps = integrate_trapezoidal(
            args.expr, args.a, args.b, args.n, verbose=args.verbose
        )
        print(f"Integral (trapezoid): {val}")
        if args.verbose:
            _print_steps(steps)
    elif args.method == "simpson":
        val, steps = integrate_simpson(
            args.expr, args.a, args.b, args.n, verbose=args.verbose
        )
        print(f"Integral (simpson): {val}")
        if args.verbose:
            _print_steps(steps)
    elif args.method == "rect":
        val, steps = integrate_rectangle(
            args.expr, args.a, args.b, args.n, mode=args.mode, verbose=args.verbose
        )
        print(f"Integral (rect/{args.mode}): {val}")
        if args.verbose:
            _print_steps(steps)
    else:  # mc
        val = integrate_monte_carlo(args.expr, args.a, args.b, samples=args.samples)
        print(f"Integral (monte-carlo): {val}")


if __name__ == "__main__":
    main()
