import numpy as np


def main() -> None:
    # Demo arrays
    x = np.array([0.3, 0.7, 0.9, 1.4, 1.7, 1.9, 2.3, 2.6])
    y = np.array([-4.3, -1.6, 0.4, 0.9, 1.2, 1.4, 1.5, 1.5])

    integral = float(np.trapz(y, x))
    print(f"Integral (np.trapz): {integral}")


if __name__ == "__main__":
    main()
