#!/usr/bin/python
from math import sqrt
from random import random


class Point:
    """ Just a point, nothing to see here """

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.group = -1

    def distance_to(self, p):
        return sqrt((self.x - p.x)**2 + (self.y - p.y)**2)

    def sq_distance_to(self, p):
        return (self.x - p.x)**2 + (self.y - p.y)**2

    def __repr__(self):
        return "Point(%.2f, %.2f)" % (self.x, self.y)


class Circle:
    """ You know, a circle. The round things. Pylint makes me write these. """

    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r_squared = r**2

    def contains_point(self, p):
        """ Return bool representing if point is within self """
        return p.sq_distance_to(self) <= self.r_squared

    def num_within(self, pts):
        """ Given a set of points, return the number within self """
        total = 0
        for p in pts:
            if self.contains_point(p):
                total += 1
        return total

    def __repr__(self):
        return "Circle (%.2f, %.2f) radius %.2f" % (self.x, self.y, sqrt(self.r_squared))

    def pull_in_bounds(self):
        r = sqrt(self.r_squared)
        if self.x + r > 1:
            self.x -= self.x + r - 1
        elif self.x - r < 0:
            self.x += self.x - r

        if self.y + r > 1:
            self.y -= self.y + r - 1
        elif self.y - r < 0:
            self.y += self.y - r


def cluster(points):
    retVal = [[]]
    # get an estimate of the average distance between any two points
    avg_distance = -1
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            avg_distance += points[i].distance_to(points[j])
    avg_distance /= (len(points)**2 - len(points)) / 2

    curr_node, total_marked = points[0], 0
    while total_marked < len(points):
        # if we're not close to another cluster, form another
        if curr_node is None:
            for point in points:
                if point.group == -1:
                    curr_node = point
                    retVal.append([])
                    break

        # add to cluster
        retVal[len(retVal) - 1].append(curr_node)
        curr_node.group = len(retVal) - 1
        total_marked += 1

        # the closest point will be added to our cluster, iff it's below the average distance from us
        min_distance, min_point = avg_distance, None
        for point in points:
            if point.group != -1:
                continue
            dist = point.distance_to(curr_node)
            if dist <= min_distance:
                min_distance, min_point = dist, point
        curr_node = min_point
    return retVal


def solve(points):
    """ solve the problem """
    clusters = cluster(points)
    max_cluster = clusters[0]
    for c in clusters:
        if len(c) > len(max_cluster):
            max_cluster = c
    avg_x, avg_y = sum(p.x for p in max_cluster) / \
        len(max_cluster), sum(p.y for p in max_cluster) / len(max_cluster)
    c = Circle(avg_x, avg_y, min(avg_x, avg_y, 1 - avg_x, 1 - avg_y, .05))
    while c.num_within(points) < .5 * len(points) and c.r_squared < .5:
        c = Circle(c.x, c.y, sqrt(c.r_squared) + .05)
        c.pull_in_bounds()
    if c.num_within(points) != .5 * len(points):
        return -1
    return c.num_within(points), c


def main():
    """ Main function """
    points = []

    # get input
    for _ in range(int(input)):
        pt = [float(i) for i in input().split(" ")]
        points.append(Point(pt[0], pt[1]))

    solve(points)


def test(num):
    pts = []
    if num % 2 != 0:
        print("Invalid number of points (must be even)")
        return
    for _ in range(num):
        pts.append(Point(random(), random()))
    from pprint import pprint
    pprint(solve(pts))


# main()
test(4)
