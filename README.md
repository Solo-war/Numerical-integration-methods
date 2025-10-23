# Численное интегрирование (Python)

Единый модуль интеграторов с безопасным парсингом выражений и CLI.

## Поддерживаемые методы
- Трапеций: `integrate_trapezoidal`
- Симпсона: `integrate_simpson` (n — чётное)
- Прямоугольников: `integrate_rectangle` (`left|right|midpoint`)
- Монте‑Карло: `integrate_monte_carlo`

Выражение задаётся строкой, например `"exp(x)/(1+exp(2*x))"`. Доступны функции из `math` (`sin`, `cos`, `exp`, `sqrt`, и т.п.), переменные `x`, `y`, `z`. Доступ к `__builtins__` закрыт.

## Быстрый старт (Windows/PowerShell)
- Запуск CLI (пример Симпсона):
  - `.venv\Scripts\python.exe .\main.py --method simpson --expr 'exp(x)/(1+exp(2*x))' -a 0 -b 1 -n 100`
- Трапеции:
  - `.venv\Scripts\python.exe .\main.py --method trapezoid --expr 'sin(x)' -a 0 -b 3.1415926535 -n 1000`
- Прямоугольники (серединные):
  - `.venv\Scripts\python.exe .\main.py --method rect --mode midpoint --expr 'x**2' -a 0 -b 1 -n 500`
- Монте‑Карло:
  - `.venv\Scripts\python.exe .\main.py --method mc --expr 'exp(x)/(1+exp(2*x))' -a 0 -b 1 --samples 20000`

Примечание: в PowerShell используйте одинарные кавычки вокруг выражения (`'...'`), чтобы не было проблем с `*` и скобками.

## Тесты
- Запуск тестов:
  - `.venv\Scripts\python.exe -m unittest discover -s tests -p 'test_*.py' -v`

Тесты сверяют методы с точным значением для `∫ exp(x)/(1+exp(2x)) dx = atan(e) − π/4`, проверяют сходимость прямоугольников и Монте‑Карло.

## Зависимости
- Стандартная библиотека Python (нет внешних зависимостей).

## Git
В репозитории добавлен `.gitignore`, исключающий `.venv/`, `.idea/`, `__pycache__/` и др. Можно безопасно публиковать на GitHub без лишних файлов IDE/виртуального окружения.
