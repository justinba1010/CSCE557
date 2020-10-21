"""
Justin Baum
20 October 2020
test.py
Sanity Check
"""

import unittest
from curve import Curve
from point import Point

class PointOperations(unittest.TestCase):
    def test_example74(self):
        curve = Curve(-36, 0, 10*10)
        p = Point(-3, 9, 1, curve)
        q = Point(-2, 8, 1, curve)
        k = Point(6, 0, 1, curve)
        self.assertEqual(p + q, k)
    def test_addition(self):
        curve = Curve(1, 1, 31)
        p1 = Point(0, 1, 1, curve)
        p2 = Point(0, 1, 1, curve)
        expected = Point(8, 26, 1, curve)
        self.assertEqual(p1 + p2, expected)
    def test_multiplication(self):
        curve = Curve(1,1,31)
        p1 = Point(0, 1, 1, curve)
        expected = Point(28, 8, 1, curve)
        k = 10
        self.assertEqual(p1 * k, expected)
    def test_points(self):
        curve = Curve(1,6,11)
        points = [
                (2,4),
                (2,7),
                (3,5),
                (3,6),
                (5,2),
                (5,9),
                (7,2),
                (7,9),
                (8,3),
                (8,8),
                (10,2),
                (10,9)
                ]
        points = [Point(x, y, 1, curve) for (x,y) in points]
        self.assertTrue(all([point in curve for point in points]))

if __name__ == "__main__":
    unittest.main()
