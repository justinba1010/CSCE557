"""
Justin Baum
20 October 2020
curve.py
Implementing an Elliptic Curve using Jacobian Coordinates
"""
from curve_types import TPoint, TCurve

class Curve:
    """
    Curve Module
    """
    def __init__(self, a : int, b : int, modulus : int) -> TCurve:
        """
        Create a Curve
        """
        self.a = a  # pylint: disable=invalid-name
        self.b = b  # pylint: disable=invalid-name
        self.modulus = modulus
    def on_curve(self : TCurve, point : TPoint) -> bool:
        """
        Check if the point satisfies the equality:
        y^2 = x^3 + ax + b
        """
        return \
                (pow(point.y, 2, self.modulus))\
                ==\
                (\
                    (pow(point.x, 3, self.modulus))\
                    +\
                    (self.a * point.x) + self.b\
                ) % self.modulus

    # Private Functions
    def __contains__(self : TCurve, point : TPoint):
        return self.on_curve(point)
    def __eq__(self :TCurve, other : TCurve):
        return\
                self.a == other.a and\
                self.b == other.b and\
                self.modulus == other.modulus
