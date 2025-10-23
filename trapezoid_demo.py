from integrand_utils import evaluate_function


def integrateTrapezoidal(expr, lowerBound, upperBound, steps):

    step = (upperBound - lowerBound) / steps

    def evaluate(e, x):
        return evaluate_function(e, x)

    a = float(lowerBound)
    b = float(upperBound)
    h = float(step)

    integral = 0.0
    values = []

    x = a
    while x < b:
        y0 = evaluate(expr, x)
        y1 = evaluate(expr, x + h)
        integral += ((y0 + y1) * h) / 2.0
        i = 0

        stepY = (y1 - y0) / (h / 0.2) if h != 0 else 0.0
        newX = x
        while newX < x + h:
            values.append({"x": f"{newX:.2f}", "y": y0 + stepY * i})
            newX += 0.2
            i += 1
        x += h

    return {"integral": integral, "values": values}


def main():

    expr = "exp(x) / (1 + exp(2 * x))"
    lower_bound = 0
    upper_bound = 1
    steps = 200

    result = integrateTrapezoidal(expr, lower_bound, upper_bound, steps)
    print(f"Integral: {result['integral']}")
    for value in result["values"]:
        print(f"x: {value['x']}, y: {value['y']}")


if __name__ == "__main__":
    main()
