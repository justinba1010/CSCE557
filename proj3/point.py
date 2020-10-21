"""
Justin Baum
20 October 2020
point.py
Implementing Jacobian Coordinates on an Elliptic Curve
"""
from curve_types import TCurve, TPoint
from utils import multiplicative_inverse as m_inv

DEBUG = False

class Point:
    """
    Point Module
    """
    def __init__(self, x : int, y : int, z : int, curve : TCurve) -> TPoint:
        """
        Create a point on some curve
        """
        self.x = x  # pylint: disable=invalid-name
        self.y = y  # pylint: disable=invalid-name
        self.z = z  # pylint: disable=invalid-name
        self.curve = curve
        self.on_curve = self in curve

    def double(self : TPoint) -> TPoint:
        """
        p1 = 2p1
        """
        # pylint: disable=invalid-name

        # 3x1^2 + a
        m = (3*pow(self.x, 2, self.curve.modulus)) + self.curve.a
        m *= m_inv(2*self.y, self.curve.modulus)
        m %= self.curve.modulus
        # x3 = m^2 - 2x1
        x3 = pow(m, 2, self.curve.modulus) - 2*self.x
        x3 %= self.curve.modulus
        # y3 = m(x3 - x1) + y1
        y3 = m * (x3 - self.x) + self.y
        # reflect y over x axis
        y3 *= -1
        y3 %= self.curve.modulus
        return Point(x3, y3, 1, self.curve)
    def __add__(self : TPoint, other : TPoint) -> TPoint:
        if self == other:
            return self.double()
        if self.x == other.x:
            # This is geometrically the point at infinity
            # Also avoids division by 0
            return None
        # m = (y2 - y1) * (x2 - x1)^ -1
        m = (other.y - self.y) % self.curve.modulus
        if DEBUG: print("M: " + str(m))
        i = m_inv((other.x - self.x) % self.curve.modulus, self.curve.modulus)
        if DEBUG: print("I: " + str(i))
        m *= i
        m %= self.curve.modulus
        if DEBUG: print("M: " + str(m))
        # x3 = m^2 - x1 - x2
        x3 = pow(m, 2, self.curve.modulus) - self.x - other.x
        x3 %= self.curve.modulus
        if DEBUG: print("x3: " + str(x3))
        y3 = m * (x3 - self.x) + self.y
        y3 %= self.curve.modulus
        y3 *= -1
        y3 %= self.curve.modulus
        return Point(x3, y3, 1, self.curve)

    def __iadd__(self : TPoint, other : TPoint) -> TPoint:
        """
        p1 += p2
        """
        return self + other
    def __internal__mul__(self : TPoint, k : int, original_point : TPoint):
        while k > 1 and self:
            if k & 1 == 1:
                self += self
                if self:
                    self += original_point
                else:
                    if DEBUG: print("Huh")
                    k -= 2
                    break
            else:
                self += self
            k >>= 1
        if k > 1:
            # We hit infinity, go around
            return original_point * k
        return self

    def __mul__(self : TPoint, k : int) -> TPoint:
        new_point = Point(self.x, self.y, self.z, self.curve)
        return new_point.__internal__mul__(k, self)
    def __eq__(self : TPoint, other : TPoint) -> bool:
        return\
                self.x == other.x and\
                self.y == other.y and\
                self.z == other.z and\
                self.curve == other.curve
