"""
Justin Baum
20 October 2020
curve.py
Implementing an Elliptic Curve
"""
from curve_types import TPoint, TCurve, TPairPoint
from point import Point
# from math import sqrt
from utils import eulers_criterion

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
        self.quadratic_residues()
    def quadratic_residues(self):
        """
        Use pre-computation to speed things up
        https://math.stackexchange.com/questions/1145325/how-to-find-all-the-quadratic-residues-modulo-p
        I believe I have residues and squares mixed up
        """
        self.residues = {}
        for residue in range(self.modulus // 2 + 1):
            square = pow(residue, 2, self.modulus)
            if square not in self.residues:
                self.residues[square] = [residue]
            else:
                self.residues[square].append(residue)
        
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
    def point_from_x(self, x : int):
        """
        Using precomputation generate all points with value x
        https://math.stackexchange.com/questions/1145325/how-to-find-all-the-quadratic-residues-modulo-p
        """
        y_squared = pow(x, 3, self.modulus)\
                + (self.a * x) + self.b
        y_squared %= self.modulus
        if y_squared in self.residues:
            solutions = self.residues[y_squared]
            # Add (-y)^2 == y^2
            solutions += [-solution % self.modulus for solution in solutions]
            return [Point(x, solution, self) for solution in solutions]
        return None


    def _point_from_x(self, x : int) -> TPairPoint:
        # pylint: disable=invalid-name
        """
        Generate points where x = x, that are on the curve
        Brute force, I was reading into legendre's method
        and quadratic residues,
        but the brute force was surprisingly fast for 1000003
        """

        y_squared = pow(x, 3, self.modulus)\
                + (self.a * x) + self.b
        y_squared %= self.modulus
        for i in range(self.modulus):
            if pow(i, 2, self.modulus) == y_squared:
                if i == 0:
                    return (Point(x, i, self), None)
                return (Point(x, i, self), Point(x, -i % self.modulus, self))
        return None
        # s = int(sqrt(self.modulus))
        """
        if eulers_criterion(y_squared, self.modulus):
            # There exists 2 points with x
            # Check if there is a trivial square
            # I thought this would be faster,
            # It is incredibly slow
            # y = int(sqrt(y_squared))
            # if y**2 == y_squared:
                # return (Point(x,y,1,self), Point(x,-y % self.modulus, 1, self))
            #for i in range(self.modulus):
                # Exhaustively search
                #if pow(i, 2, self.modulus) == y_squared:
                    #return (Point(x,i,1,self), Point(x,i % self.modulus, 1, self))
            y_solution_1 = tonelli(y_squared, self.modulus)
            y_solution_2 = -y_solution_1
            y_solution_2 %= self.modulus
            return (Point(x, y_solution_1, self), Point(x, y_solution_2, self))
        """
        return None

    def all_points(self):
        """
        Brute force all points
        This goes through all x values and uses `point_from_x`
        """
        points = []
        for i in range(self.modulus):
            xpoints = self.point_from_x(i)
            if xpoints:
                points += xpoints
        return points

    def all_points_x_y(self):
        """
        Just a handy function for debug
        """
        return [(p.x, p.y) for p in self.all_points()]


    # Private Functions
    def __contains__(self : TCurve, point : TPoint):
        """
        Allows
        p1 in curve
        to return boolean
        """
        return self.on_curve(point)
    def __eq__(self :TCurve, other : TCurve):
        """
        Allows us to use sets, and other tools
        """
        return\
                self.a == other.a and\
                self.b == other.b and\
                self.modulus == other.modulus
    def __str__(self):
        """
        Pretty print
        """
        return "y^2 = x^3 + {}x + {} mod {}".format(self.a, self.b, self.modulus)
