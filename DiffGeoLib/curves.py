import numpy as np

class Curve:
    """The Curve class wraps a parametric curve f: R -> R^2 with methods for numerical differentiation
     and translation."""

    def __init__(self, f):
        """Arguments:
        f: R -> R^n"""

        self.f = f

    def __call__(self, s):
        """Return curve location at time s."""

        return self.f(s)

    def derivative(self, s, ds, order=1):
        """Return derivative of order 'order' (where 0 is the curve itself) in R^2"""

        def _recursive_derivative(s, ds, order):
            if order == 0:
                return self.f(s)
            elif order > 0:
                s_1 = s
                s_0 = s + ((-1)**order * ds)
                y_1 = _recursive_derivative(s_1, ds, order-1)
                y_0 = _recursive_derivative(s_0, ds, order-1)
                dy = np.subtract(y_1, y_0)
                dx = s_1 - s_0
                return np.divide(dy, dx)
            else:
                raise ValueError('order must be greater than or equal to 0')

        return tuple(_recursive_derivative(s, ds, order))