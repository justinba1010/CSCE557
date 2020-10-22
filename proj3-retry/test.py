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
    @staticmethod
    def transform_points_to_Points(points, curve):
        return [Point(x,y,curve) for (x,y) in points]
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
    def test_multiplication(self):
        curve = Curve(1,1,31)
        p1 = Point(0,1,curve)
        expected = [
            (8, 26),
            (10,22),
            (22,21),
            (17,23),
            (19,20),
            (13,17),
            (23,16),
            (12,6),
            (28,8),
            (5,21),
            (11,17),
            (7,17),
            (21,13),
            (4,10),
            (3,0),
            (4,21),
            (21,18),
            (7,14),
            (11,14),
            (5,10),
            (28,23),
            (12,25),
            (23,15),
            (13,14),
            (19,11),
            (17,8),
            (22,10),
            (21,9),
            (8,5)
        ]
        expected = PointOperations.transform_points_to_Points(expected, curve)
        actual = [p1 * k for k in range(2,32)]
        self.assertTrue(all([actuali == expectedi for (actuali, expectedi) in zip(actual, expected)]))
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
        points = PointOperations.transform_points_to_Points(points, curve)
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
        order = point.order_multiplication()
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
        order = point.order_multiplication()
        orders = [(p * i) and (p * i) in curve for (i, p) in enumerate(order)]
        self.assertTrue(all(orders))


if __name__ == "__main__":
    unittest.main()
