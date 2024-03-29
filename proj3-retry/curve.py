"""
Justin Baum
20 October 2020
curve.py
Implementing an Elliptic Curve
"""

from point import Point
from utils import eulers_criterion

class Curve:
    """
    Curve Module
    """
    def __init__(self, a, b, modulus):
        self.a = a
        self.b = b
        self.modulus = modulus
        self.residues = {}
        self.points = None
        self.residue_precomputation()
    def residue_precomputation(self):
        """
        Use pre-computation to speed things up
        https://math.stackexchange.com/questions/1145325/how-to-find-all-the-quadratic-residues-modulo-p
        I believe I have residues and squares mixed up
        This also finds all valid y coordinates
        """
        # x^2 = a mod m
        # key = a (residue)
        # value = x1, ...
        self.residues = {}
        for x_value in range(self.modulus // 2 + 1):
            # x^2 = (-x)^2
            x_value2 = - x_value % self.modulus
            residue = pow(x_value, 2, self.modulus)
            if residue not in self.residues:
                self.residues[residue] = [x_value, x_value2]
            else:
                self.residues[residue] += [x_value, x_value2]
    def on_curve(self, point):
        """
        Check if the point is on the curve,
        as in
        y^2 = x^3 + ax + b
        for (x,y)
        """
        return (
            pow(point.y, 2, self.modulus)
            ==
            (
                pow(point.x, 3, self.modulus)
                +
                (self.a * point.x + self.b)
            )
            %
            self.modulus
        )
    def point_from_x(self, x):
        """
        Find y coordinates
        I tried tonelli shanks, but it was too difficult
        I also tried some baby-step giant-leap ideas, but
        was not successful with such
        """
        y_squared = pow(x, 3, self.modulus) + (self.a * x) + self.b
        y_squared %= self.modulus
        if y_squared in self.residues:
            # Then there exists a solution to
            # y^2 = x^3 + ax + b mod m
            # for this x
            return [Point(x, y, self) for y in self.residues[y_squared]]
        return []
    def all_points(self):
        """
        Brute force
        """
        # Optimization
        if self.points:
            return self.points
        points = []
        for x_value in range(self.modulus):
            for point in self.point_from_x(x_value):
                points.append(point)
        self.points = points
        return points
    def __contains__(self, point):
        """
        Allows the keyword in
        """
        return self.on_curve(point)
    def __str__(self):
        """
        Pretty print
        """
        return "y^2 = x^3 + {}x + {} mod {}".format(self.a, self.b, self.modulus)
    def __hash__(self):
        """
        Unique value
        """
        return hash(self.__str__())