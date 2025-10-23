from integrand_utils import (
    derivative_function,
    extract_variable,
    extract_variable_from_equation,
)

print("d/dx of x**3:", derivative_function("x**3", "x"))
print("d/dx of sin(x)**2:", derivative_function("sin(x)**2", "x"))
print("solve x**2-1=0 for x:", extract_variable_from_equation("x**2-1=0", "x"))
print("solve y**2 - x for y:", extract_variable("y**2 - x", "y"))
