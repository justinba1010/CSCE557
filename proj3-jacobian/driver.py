#! /usr/bin/python3
"""
Justin Baum
21 October 2020
driver.py
Driver code for using the Elliptic Curve
"""
import argparse
from curve import Curve
from point import Point
from sys import exit
from utils import factors

def main():
    """
    Driver code
    """
    #pylint: disable=*

    # Parser Routine
    parser = argparse.ArgumentParser(description=
    """
    Elliptic Curves in Jacobian Coordinates
    """
    )
    parser.add_argument("-a", action="store", type=int, help="This is the value a in y^2 = x^3 + ax + b mod m", required=True)
    parser.add_argument("-b", action="store", type=int, help="This is the value b in y^2 = x^3 + ax + b mod m", required=True)
    parser.add_argument("-m", action="store", type=int, help="This is the value m in y^2 = x^3 + ax + b mod m", required=True)
    parser.add_argument("-px", action="store", type=int, help="This is the point value x for the generator", required=False)
    parser.add_argument("-py", action="store", type=int, help="This is the point value y for the generator", required=False)
    parser.add_argument("-pz", action="store", type=int, help="This is the point value z for the generator", required=False)
    parser.add_argument("-o", action="store", type=str, help="This is the path of the output file; stdout is default", required=False)
    parser.add_argument("--bv", action="store_true", help="This is verbose brute force", required=False)
    parser.add_argument("--brute", action="store_true", help="If the curve does not have order p where p is prime, the shortcut\
    is rendered useless, and exhaustive search can be done", required=False)
    args = parser.parse_args()

    # Parse Arguments
    a = args.a
    b = args.b
    m = args.m
    x = args.px
    y = args.py
    z = args.pz
    bv = args.bv
    brute = args.brute or bv
    o = args.o if args.o else "/dev/tty"
    curve = Curve(a,b,m)
    with open(o, "w") as f:
        # Point Routine
        # Go through order of point
        if x is not None:
            # we have a point
            z = z if z else 1
            point = Point(x,y,z,curve) if y else curve.point_from_x(x)
            if isinstance(point, list):
                if len(point) == 0:
                    f.write("This curve {} does not have a point at x = {}\n".format(curve, x))
                    exit(1)
                else:
                    point = point[0]
            if point not in curve:
                f.write("This point {} is not on the curve {}\n".format(point, curve))
                exit(1)
            for (i, kpoint) in enumerate(point.order_multiplication_generator()):
                s = "{}p = {}\n".format(i, kpoint)
                f.write(s)
        # Curve Routine
        else:
            for (i, point) in enumerate(curve.all_points()):
                f.write("{}\n".format(point))
            count_of_points = len(curve.points)
            f.write("{}\nThe curve\n{}\nhas {} affine points:\n".format("-"*80, curve, count_of_points))
            if not brute:
                f.write("The points with order {}(assuming {} is prime, this is the maximum order of the group) are: \n{}\n".format(count_of_points, count_of_points, "-"*80))
                # Turns out that does not work, instead we're going to cheapen our workload by checking the factors of
                # the cardinality of E +/- 1
                # This is observational based
                # This seems to work when the order of a point is equal to the cardinality of the curve
                total_count = 0
                for point in curve.points:
                    jumpy = False
                    for factor in factors(count_of_points + 1):
                        opposite_point = point * (factor - 1)
                        if (point + opposite_point).infinity:
                            jumpy  = True
                            continue
                    for factor in factors(count_of_points - 1):
                        opposite_point = point * (factor - 1)
                        if (point + opposite_point).infinity:
                            jumpy  = True
                            continue
                    for factor in factors(count_of_points):
                        opposite_point = point * (factor - 1)
                        if (point + opposite_point).infinity:
                            jumpy  = True
                            continue
                    if jumpy:
                        continue
                    opposite_point = point * (count_of_points)
                    # we are going to satisfy the equality
                    # P + -P = O
                    # because the order is prime, cycles of less than i do not exist
                    is_infinity = point + opposite_point
                    if is_infinity.infinity:
                        total_count += 1
                        f.write("{}\n".format(point))
                f.write("In total there are {} points with max order {}\n".format(total_count, count_of_points))
            else:
                # Brute force
                max_order = 0
                max_points = []
                for point in curve.all_points():
                    if bv:
                        f.write("The order for the point {} on curve {}\n{}\n".format(point, curve, "-"*80))
                    exponentiation = point.copy()
                    i = 0
                    if bv:
                        f.write("{}p = {}\n".format(i, Point.infinity()))
                    while not exponentiation.infinity:
                        i += 1
                        if bv:
                            f.write("{}p = {}\n".format(i, exponentiation))
                        exponentiation += point
                    if bv:
                            f.write("{}p = {}\n".format(i+1, exponentiation))
                    if i > max_order:
                        max_points = [point]
                        max_order = i
                    elif i == max_order:
                        max_points.append(point)
                f.write("The points with max order {} are\n{}\n".format(max_order, "-"*80))
                total_count = 0
                for point in max_points:
                    f.write("{}\n".format(point))
                    total_count += 1
                f.write("In total there are {} points with max order {}\n".format(total_count, count_of_points))


if __name__ == "__main__":
    main()
