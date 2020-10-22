"""
Justin Baum
21 October 2020
point.py
Points on an elliptic curve
"""

from utils import multiplicative_inverse as m_inv

class Point:
    """
    Point Module
    Represents points in affine form on some curve
    """
    def __init__(self, x, y, curve):
        """
        Construct a point on some curve
        """
        self.x = x
        self.y = y
        self.curve = curve
    @staticmethod
    def infinity():
        """
        Return point at infinity
        """
        point = Point(0,0,None)
        point.infinity = True
        return point
    def copy(self):
        """
        Return a deep copy
        """
        return Point(self.x, self.y, self.curve)
    def double(self):
        """
        Returns a new point that is:
        p + p
        """
        if self.infinity:
            return self
        # 3x_1^2 + a
        m_slope = (3 * pow(self.x, 2, self.curve.modulus)) + self.curve.a
        m_slope *= m_inv(2 * self.y, self.curve.modulus)
        m_slope %= self.curve.modulus
        # m^2 - 2x1
        x_3 = pow(m_slope, 2, self.curve.modulus) + self.curve.a
        x_3 %= self.curve.modulus
        # m(x_3 - x_1) + y_1
        y_3 = m_slope * (x_3 - self.x) + self.y
        y_3 *= -1
        y_3 %= self.curve.modulus
        return Point(x_3, y_3, self.curve)
    def multiply(self, k):
        """
        Returns new point using 
        p1 * k
        """
        point = self.copy()
        while k > 1 and not point.infinity:
            if k & 1 == 1:
                point += point
                if not point.infinity:
                    point += self
                else:
                    # Loop around
                    return self.multiply((k >> 1) + 1)
            else:
                point += point
        return point
    def add(self, other):
        """
        Returns a new poin that is:
        p1 + p2
        """
        if self.infinity:
            return self
        if other.infinity:
            return other
        if self == other:
            return self.double()
        if self.x == other.x:
            # Geometrically this is the point at infinity
            return Point.infinity()
        # (y_2 - y_1) * (x_2 - x_1)^-1
        m_slope = (other.y - self.y)
        m_slope *= m_inv((other.x - self.x) % self.curve.modulus, self.curve.modulus)
        m_slope %= self.curve.modulus
        # m^2 - x_1 - x_2
        x_3 = pow(m_slope, 2, self.curve.modulus) - self.x - other.x
        x_3 %= self.curve.modulus
        # m(x_3 - x_1) + y_1
        y_3 = m_slope * (x_3 - self.x) + self.y
        y_3 %= self.curve.modulus
        y_3 *= -1
        y_3 %= self.curve.modulus
        return Point(x_3, y_3, self.curve)
    def 
    def order_multiplication(self):
        return []
    def order_exponentiation(self):
        return []
    def __add__(self, other):
        """
        Allows the use of +
        """
        return self.add(other)
    def __iadd__(self, other):
        """
        Allows the use of +=
        """
        return self + other
    def __mul__(self, k):
        """
        Allows the use of *
        """
        return self.multiply(k)
    def __imul__(self, k):
        """
        Allows the use of *=
        """
        return self * k
    def __eq__(self, other):
        """
        Allows the use of ==
        """
        return (
            self.x == other.x and
            self.y == other.y and
            self.curve == other.curve
            or
            (self.infinity and other.infinity)
        )
    def __str__(self):
        """
        Returns a pretty print of the point
        """
        return "<{}, {}>".format(self.x, self.y)
    def __hash__(self):
        """
        Allows the use of sets
        """
        return hash(0) if self.infinity else hash((self.x, self.y, self.curve.__str__()))