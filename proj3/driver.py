"""
Justin Baum
20 October 2020
driver.py
    1. Find all points
    2. Find order of all points
"""

from sys import argv
from curve import Curve
from point import Point
from utils import factors

BRUTE = True

def main():
    if len(argv) != 2:
        print("Please enter a filename as an argument, the filename should have format as noted in README")
    inputname = argv[1]
    with open(inputname, "r") as filey:
        (a, b, modulus) = [int(i) for i in filey.readline().split()]
        curve = Curve(a, b, modulus)

    print("Working with the following curve:")
    print("-"*80)
    print(curve)
    points = curve.all_points()
    points = list(set(points))
    points.sort(key=lambda x: x.x)
    print("-"*80)
    print("This curve has the following {} points:".format(len(points)))
    print("\n".join([str(p) for p in points]))
    max_point = []
    max_order = 0
    # Brute Force is too slow
    if BRUTE:
        for point in points:
            print("-"*80)
            order = point.order_of_point()
            orderlen = len(order)
            print("The point: " + str(point) + " has order: " + str(orderlen))
            if orderlen > max_order:
                max_order = orderlen
                max_point = [point]
            elif orderlen == max_order:
                max_point.append(point)
            for (i, point) in enumerate(order):
                print("{}p = {}".format(i + 1, point))
        print("-"*80)
        print("The points with maximum order {} on curve {}".format(max_order, curve))
    max_order = len(points)
    for point in max_point:
        print(point)
    # New solution after reading description
    max_point = []
    for point in points:
        """
        Because the maximum order is prime, the cycle cannot repeat in p steps
        We're just going to check if any point has the same x at p-1
        """
        point_p_1 = point * (max_order)
        if point_p_1 and point_p_1.x == point.x:
            max_point.append(point_p_1)
    
    print("The points with maximum order {} on curve {}".format(max_order, curve))
    for point in max_point:
        print(point)


if __name__ == "__main__":
    main()
