"""
Justin Baum
20 October 2020
test.py
Sanity Check
"""

import unittest
from curve import Curve
from point import Point
from random import randint
class PointOperations(unittest.TestCase):
    def test_example74(self):
        curve = Curve(-36, 0, 10*10)
        p = Point(-3, 9, curve)
        q = Point(-2, 8, curve)
        k = Point(6, 0, curve)
        self.assertEqual(p + q, k)
    def test_addition(self):
        curve = Curve(1, 1, 31)
        p1 = Point(0, 1, curve)
        p2 = Point(0, 1, curve)
        expected = Point(8, 26, curve)
        self.assertEqual(p1 + p2, expected)
    def test_multiplication(self):
        curve = Curve(1,1,31)
        p1 = Point(0, 1, curve)
        expected = Point(28, 8, curve)
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
        points = [Point(x, y, curve) for (x,y) in points]
        self.assertTrue(all([point in curve for point in points]))
    def test_points_all_11593(self):
        curve = Curve(101,13,11593)
        points = curve.all_points()
        self.assertTrue(all([point in curve for point in points]))
    def test_points_all_100003(self):
        curve = Curve(1234,8413,100003)
        points = curve.all_points()
        self.assertTrue(all([point in curve for point in points]))
    def test_order(self):
        curve = Curve(24323,34324,100003)
        point = None
        while not point:
            point = curve.point_from_x(randint(0,100000))
        point = point[0]
        order = point.order_of_point()
        self.assertTrue(len(order) > 0)
    def test_order_on_curve(self):
        """
        Testing speed
        """
        curve = Curve(13,17,1009)
        point = None
        while not point:
            point = curve.point_from_x(randint(0,1000000))
        point = point[0]
        order = point.order_of_point()
        orders = [(p * i) and (p * i) in curve for (i, p) in enumerate(order)]
        self.assertTrue(all(orders))


if __name__ == "__main__":
    unittest.main()
