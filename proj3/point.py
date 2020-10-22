"""
Justin Baum
20 October 2020
point.py
Points on an elliptic curve
"""
from curve_types import TCurve, TPoint
from utils import multiplicative_inverse as m_inv

LOOP = True


class Point:
    """
    Point Module
    """
    def __init__(self, x : int, y : int, curve : TCurve) -> TPoint:
        """
        Create a point on some curve
        """
        self.x = x  # pylint: disable=invalid-name
        self.y = y  # pylint: disable=invalid-name
        self.curve = curve
        self.on_curve = curve.on_curve(self) if curve else False
    def copy(self):
        """
        Returns a deep copy of the point
        """
        return Point(self.x, self.y, self.curve)

    def double(self : TPoint) -> TPoint:
        # pylint: disable=invalid-name
        """
        Returns the point doubled
        p1 = 2p1
        """

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
        return Point(x3, y3, self.curve)
    def order_of_point(self : TPoint):
        """
        This possibly may be in the wrong place as far as APIs go
        """
        points = [self]
        pointy = self.copy()
        while pointy:
            pointy += self
            if not pointy or pointy in points:
                break
            points.append(pointy)
        return points
    def __add__(self : TPoint, other : TPoint) -> TPoint:
        # pylint: disable=invalid-name
        """
        Returns the new point
        Usage:
        `p3 = p1 + p2`
        """
        if self == other:
            return self.double()
        if self.x == other.x:
            # This is geometrically the point at infinity
            # Also avoids division by 0
            return None
        # m = (y2 - y1) * (x2 - x1)^ -1
        m = (other.y - self.y) % self.curve.modulus
        i = m_inv((other.x - self.x) % self.curve.modulus, self.curve.modulus)
        m *= i
        m %= self.curve.modulus
        # x3 = m^2 - x1 - x2
        x3 = pow(m, 2, self.curve.modulus) - self.x - other.x
        x3 %= self.curve.modulus
        y3 = m * (x3 - self.x) + self.y
        y3 %= self.curve.modulus
        y3 *= -1
        y3 %= self.curve.modulus
        return Point(x3, y3, self.curve)

    def __iadd__(self : TPoint, other : TPoint) -> TPoint:
        """
        Returns a new point, for the += operator
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
                    return None
            else:
                self += self
            k >>= 1
        if LOOP and k > 1:
            # We hit infinity, go around
            overflow = original_point * k
            if overflow: overflow.overflow = True
            return overflow
        if k > 1:
            return None
        return self

    def __mul__(self : TPoint, k : int) -> TPoint:
        """
        Returns the result of point multiplication
        p3 = p1 * n
        where n is an integer
        """
        new_point = Point(self.x, self.y, self.curve)
        return new_point.__internal__mul__(k, self)
    def __eq__(self : TPoint, other : TPoint) -> bool:
        """
        Returns the results of equality
        """
        return\
                self.x == other.x and\
                self.y == other.y and\
                self.curve == other.curve
    def __str__(self):
        """
        Returns a pretty print of the point
        """
        return "<{}, {}>".format(self.x, self.y)
    def __hash__(self):
        """
        Returns the hash value
        """
        return hash((self.x, self.y, self.curve.__str__()))
